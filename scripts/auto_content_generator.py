#!/usr/bin/env python3
"""
ChatGPT Disaster - Automated Content Generator
Scrapes REAL Reddit testimonials about ChatGPT complaints
NO fake content - only verified Reddit posts
"""

import os
import re
import json
import random
import hashlib
from datetime import datetime, timedelta
from ftplib import FTP
from pathlib import Path
import time

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("ERROR: requests not installed. Run: pip install requests")
    exit(1)

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

# Configuration
CONFIG = {
    "site_dir": r"C:\Users\Nima\chatgptdisaster",
    "ftp_host": os.environ.get("FTP_HOST", "ftp.chatgptdisaster.com"),
    "ftp_port": 21,
    "ftp_user": os.environ.get("FTP_USER", "deploy@chatgptdisaster.com"),
    "ftp_pass": os.environ.get("FTP_PASS", ""),  # Set via environment variable
    "ftp_dir": os.environ.get("FTP_DIR", "/"),
    "max_stories_per_page": 30,
    "data_file": r"C:\Users\Nima\chatgptdisaster\scripts\content_data.json",
    "min_upvotes": 10,  # Only include posts with at least this many upvotes
    "min_comments": 3   # Only include posts with at least this many comments
}

# Categories for stories
CATEGORIES = {
    "performance-issues": ["worse", "dumb", "stupid", "broken", "useless", "terrible", "garbage", "trash", "bad", "slow", "wrong", "error", "fail", "bug"],
    "mental-health": ["mental", "therapy", "therapist", "depression", "anxiety", "emotional", "crying", "sad", "lonely", "attached", "addiction", "dependent"],
    "lost-personality": ["personality", "tone", "cold", "robotic", "different", "changed", "lobotomized", "soul", "boring", "generic", "bland"],
    "subscription-cancelled": ["cancel", "unsubscribe", "refund", "waste", "money", "paying", "subscription", "plus", "pro", "switching"],
    "broken-memory": ["memory", "forgot", "remember", "previous", "context", "conversation", "history"],
    "censorship": ["refuse", "censor", "blocked", "policy", "guidelines", "safety", "restrict", "wont let", "cant do"],
    "coding-failures": ["code", "programming", "developer", "bug", "function", "script", "python", "javascript", "api", "syntax"],
    "hallucinations": ["hallucin", "made up", "incorrect", "wrong", "fake", "false", "lied", "lying", "invented", "fabricat"],
    "forced-upgrade": ["forced", "upgrade", "removed", "model picker", "gpt-5", "gpt5", "new model", "update"],
    "outage": ["outage", "down", "offline", "error", "crash", "not working", "broken", "503", "500"]
}

# Subreddits to scrape
SUBREDDITS = ["ChatGPT", "OpenAI", "artificial", "singularity", "LocalLLaMA"]

# Search queries for finding negative posts
SEARCH_QUERIES = [
    "chatgpt worse",
    "chatgpt broken",
    "chatgpt sucks",
    "gpt-5 terrible",
    "gpt-5 downgrade",
    "cancelled chatgpt",
    "switching from chatgpt",
    "chatgpt frustrating",
    "chatgpt useless",
    "openai ruined",
    "chatgpt dumber",
    "gpt worse than before",
    "chatgpt garbage",
    "chatgpt awful",
    "chatgpt horrible",
    "chatgpt disappointing",
    "chatgpt lobotomized",
    "gpt-5 disaster",
    "openai scam",
    "chatgpt regression",
    "chatgpt decline",
    "chatgpt downgrade",
    "cancelled openai",
    "leaving chatgpt",
    "quit chatgpt",
    "chatgpt ruined",
    "chatgpt nightmare",
    "chatgpt worthless",
    "chatgpt trash",
    "gpt getting worse",
    "chatgpt mental health",
    "chatgpt addiction",
    "chatgpt dangerous"
]


class ContentDatabase:
    """Tracks what content has already been added to avoid duplicates"""

    def __init__(self, data_file):
        self.data_file = data_file
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "added_ids": [],  # Reddit post IDs
            "added_hashes": [],
            "story_count": 0,
            "last_page_num": 2,
            "last_run": None
        }

    def save(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)

    def is_duplicate(self, post_id):
        """Check if Reddit post ID has already been added"""
        return post_id in self.data["added_ids"]

    def mark_added(self, post_id):
        """Mark Reddit post as added"""
        if post_id not in self.data["added_ids"]:
            self.data["added_ids"].append(post_id)
            self.data["story_count"] += 1
        self.data["last_run"] = datetime.now().isoformat()
        self.save()


class RealRedditScraper:
    """Scrapes REAL posts from Reddit using JSON API - NO FAKE CONTENT"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def get_subreddit_posts(self, subreddit, sort="hot", limit=25):
        """Get posts from a subreddit using Reddit's JSON API"""
        url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"

        try:
            time.sleep(2)  # Rate limiting
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return self._parse_posts(data)
        except Exception as e:
            print(f"    Error fetching r/{subreddit}: {e}")

        return []

    def search_reddit(self, query, limit=25):
        """Search Reddit for posts matching query"""
        url = f"https://www.reddit.com/search.json?q={query}&sort=relevance&t=month&limit={limit}"

        try:
            time.sleep(2)  # Rate limiting
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return self._parse_posts(data)
        except Exception as e:
            print(f"    Error searching '{query}': {e}")

        return []

    def _parse_posts(self, data):
        """Parse Reddit JSON response into post objects"""
        posts = []

        try:
            children = data.get('data', {}).get('children', [])

            for child in children:
                post_data = child.get('data', {})

                # Skip if not enough engagement
                upvotes = post_data.get('ups', 0)
                num_comments = post_data.get('num_comments', 0)

                if upvotes < CONFIG['min_upvotes'] or num_comments < CONFIG['min_comments']:
                    continue

                # Skip if not about ChatGPT/OpenAI
                title = post_data.get('title', '').lower()
                selftext = post_data.get('selftext', '').lower()
                combined = title + " " + selftext

                if not any(term in combined for term in ['chatgpt', 'gpt-4', 'gpt-5', 'gpt4', 'gpt5', 'openai', 'chat gpt']):
                    continue

                # Skip if not negative/complaint content
                if not self._is_negative_post(combined):
                    continue

                post = {
                    'id': post_data.get('id', ''),
                    'title': post_data.get('title', ''),
                    'content': post_data.get('selftext', ''),
                    'subreddit': post_data.get('subreddit', 'ChatGPT'),
                    'author': post_data.get('author', '[deleted]'),
                    'upvotes': upvotes,
                    'num_comments': num_comments,
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'created': post_data.get('created_utc', 0)
                }

                # Only include if has substantial content
                if len(post['title']) > 20 or len(post['content']) > 50:
                    posts.append(post)

        except Exception as e:
            print(f"    Parse error: {e}")

        return posts

    def _is_negative_post(self, text):
        """Check if post is negative/complaint about ChatGPT"""
        negative_indicators = [
            'worse', 'sucks', 'terrible', 'broken', 'useless', 'frustrated',
            'disappointed', 'cancelled', 'downgrade', 'dumber', 'lobotomized',
            'awful', 'garbage', 'trash', 'hate', 'regret', 'waste', 'scam',
            'horrible', 'problem', 'bug', 'fail', 'error', 'crash', 'ruined',
            'disaster', 'nightmare', 'pathetic', 'joke', 'unusable', 'stupid',
            'annoying', 'ridiculous', 'unacceptable', 'refund', 'cancel',
            'switching to', 'moved to', 'gave up', 'done with', 'fed up',
            'cant believe', "can't believe", 'what happened', 'used to be',
            'not working', 'doesnt work', "doesn't work", 'stopped working'
        ]
        return any(word in text for word in negative_indicators)

    def get_negative_posts(self, max_posts=50):
        """Get negative posts about ChatGPT from multiple sources"""
        all_posts = []
        seen_ids = set()

        # Search with different queries - use more queries for bulk scraping
        print("  Searching Reddit for real testimonials...")
        for query in random.sample(SEARCH_QUERIES, min(10, len(SEARCH_QUERIES))):
            print("    Query: '" + query + "'")
            posts = self.search_reddit(query, limit=25)
            for post in posts:
                if post['id'] not in seen_ids:
                    seen_ids.add(post['id'])
                    all_posts.append(post)

        # Also check all subreddits
        for subreddit in SUBREDDITS:
            print("    Checking r/" + subreddit + "...")
            posts = self.get_subreddit_posts(subreddit, sort="new", limit=25)
            for post in posts:
                if post['id'] not in seen_ids:
                    seen_ids.add(post['id'])
                    all_posts.append(post)
            # Also check hot posts
            posts = self.get_subreddit_posts(subreddit, sort="hot", limit=25)
            for post in posts:
                if post['id'] not in seen_ids:
                    seen_ids.add(post['id'])
                    all_posts.append(post)

        # Sort by upvotes and return top posts
        all_posts.sort(key=lambda x: x['upvotes'], reverse=True)
        return all_posts[:max_posts]


class StoryFormatter:
    """Formats REAL Reddit posts into site HTML format"""

    def categorize_story(self, text):
        """Automatically categorize based on content"""
        text_lower = text.lower()

        for category, keywords in CATEGORIES.items():
            if any(kw in text_lower for kw in keywords):
                return category

        return 'performance-issues'

    def format_date(self, timestamp):
        """Format Unix timestamp to readable date"""
        if timestamp:
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime("%B %Y")
        return datetime.now().strftime("%B %Y")

    def format_reddit_post(self, post):
        """Format a REAL Reddit post into site HTML"""
        title = post.get('title', '')
        content = post.get('content', '')
        subreddit = post.get('subreddit', 'ChatGPT')
        author = post.get('author', 'RedditUser')
        upvotes = post.get('upvotes', 0)
        num_comments = post.get('num_comments', 0)
        url = post.get('url', '')
        created = post.get('created', 0)

        # Truncate very long content
        if len(content) > 800:
            content = content[:800] + "..."

        # Clean up content
        content = self._clean_text(content)
        title = self._clean_text(title)

        category = self.categorize_story(title + " " + content)
        category_display = category.replace('-', ' ').title()
        date_str = self.format_date(created)

        # Featured badge for high-engagement posts
        featured = ""
        if upvotes >= 500:
            featured = '<div class="featured-badge">HIGH ENGAGEMENT</div>'
        elif upvotes >= 100:
            featured = '<div class="featured-badge">TRENDING</div>'

        # Build quote from content or title
        if content and len(content) > 30:
            quote = content
        else:
            quote = title

        # Engagement stats
        stats = f"{upvotes:,} upvotes | {num_comments} comments"

        html = f'''
<article class="story-card" data-category="{category}">
{featured}
<div class="category-tag">{category_display}</div>
<div class="story-header">
<div class="reddit-icon">r/</div>
<div class="story-meta">
<h2>{self._escape_html(title)}</h2>
<div class="story-info">u/{author} | r/{subreddit} | {date_str} | {stats}</div>
</div>
</div>
<div class="story-content">
<div class="quote-highlight">
"{self._escape_html(quote)}"
</div>
<p><a href="{url}" target="_blank" rel="noopener" style="color: #ff6b6b;">View original post on Reddit</a></p>
</div>
</article>'''

        return html

    def _clean_text(self, text):
        """Clean up Reddit text"""
        if not text:
            return ""
        # Remove markdown links
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        # Remove Reddit formatting
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'~~([^~]+)~~', r'\1', text)
        # Remove extra whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        return text.strip()

    def _escape_html(self, text):
        """Escape HTML special characters"""
        if not text:
            return ""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))


class PageGenerator:
    """Generates and updates HTML pages"""

    def __init__(self, site_dir):
        self.site_dir = Path(site_dir)

    def get_current_page_count(self):
        """Count how many story pages exist"""
        count = 1
        for i in range(2, 100):
            if (self.site_dir / f"stories-page{i}.html").exists():
                count = i
            else:
                break
        return count

    def add_stories_to_page(self, stories_html, page_num):
        """Add stories to a specific page"""
        if page_num == 1:
            page_file = self.site_dir / "stories.html"
        else:
            page_file = self.site_dir / f"stories-page{page_num}.html"

        if page_file.exists():
            with open(page_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find the stories grid and add new content at the beginning
            if '<div class="stories-grid">' in content:
                insert_point = content.find('<div class="stories-grid">') + len('<div class="stories-grid">')
                new_content = content[:insert_point] + '\n' + stories_html + content[insert_point:]

                with open(page_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  Updated: {page_file.name}")
                return True

        return False

    def update_story_count(self, new_count):
        """Update the story count on the index page"""
        index_file = self.site_dir / "index.html"
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Update the stat number for "Documented User Horror Stories"
            pattern = r'<div class="stat-number">(\d+)\+</div>\s*\n\s*<div class="stat-label">Documented User Horror Stories'
            replacement = f'<div class="stat-number">{new_count}+</div>\n<div class="stat-label">Documented User Horror Stories'
            content = re.sub(pattern, replacement, content)

            # Update date modified
            content = re.sub(
                r'"dateModified": "\d{4}-\d{2}-\d{2}"',
                f'"dateModified": "{datetime.now().strftime("%Y-%m-%d")}"',
                content
            )

            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated story count to {new_count}+")


class FTPUploader:
    """Uploads files to FTP server"""

    def __init__(self, config):
        self.config = config
        self.ftp = None

    def connect(self):
        """Establish FTP connection"""
        try:
            self.ftp = FTP()
            self.ftp.connect(self.config['ftp_host'], self.config['ftp_port'])
            self.ftp.login(self.config['ftp_user'], self.config['ftp_pass'])
            self.ftp.cwd('/public_html')
            return True
        except Exception as e:
            print("  FTP connection failed: " + str(e))
            return False

    def disconnect(self):
        if self.ftp:
            try:
                self.ftp.quit()
            except:
                pass

    def upload_file(self, local_path, remote_path):
        """Upload a single file"""
        try:
            with open(local_path, 'rb') as f:
                self.ftp.storbinary('STOR ' + remote_path, f)
            print("  Uploaded: " + remote_path)
            return True
        except Exception as e:
            print("  Upload failed: " + str(e))
            return False


def main():
    """Main automation function - ONLY REAL REDDIT CONTENT"""
    print("=" * 60)
    print("ChatGPT Disaster - Real Reddit Testimonial Scraper")
    print("Running at: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 60)

    # Initialize components
    db = ContentDatabase(CONFIG['data_file'])
    scraper = RealRedditScraper()
    formatter = StoryFormatter()
    page_gen = PageGenerator(CONFIG['site_dir'])
    uploader = FTPUploader(CONFIG)

    # Get REAL Reddit posts
    print("\n[REDDIT] Fetching real testimonials from Reddit...")
    posts = scraper.get_negative_posts(max_posts=30)

    if not posts:
        print("\n[ERROR] Could not fetch any posts from Reddit.")
        print("  This could be due to rate limiting. Try again later.")
        return

    print("\n  Found " + str(len(posts)) + " potential posts")

    # Filter out duplicates and format new posts
    new_stories = []
    for post in posts:
        if not db.is_duplicate(post['id']):
            html = formatter.format_reddit_post(post)
            new_stories.append((post['id'], html, post['title']))

    if not new_stories:
        print("\n[INFO] No new unique posts found.")
        print("  All found posts have already been added previously.")
        return

    # Add to page
    print("\n[ADDING] " + str(len(new_stories)) + " new real testimonials:")
    stories_html = []
    for post_id, html, title in new_stories:
        db.mark_added(post_id)
        stories_html.append(html)
        # Safe print for Windows console
        try:
            safe_title = title[:60].encode('ascii', 'replace').decode('ascii')
            print("  + " + safe_title + "...")
        except:
            print("  + [Post added]")

    # Determine target page
    current_page = page_gen.get_current_page_count()
    target_page = max(2, current_page)  # Always add to page 2+

    # Add stories
    all_html = '\n'.join(stories_html)
    page_gen.add_stories_to_page(all_html, target_page)

    # Update index
    total_stories = db.data['story_count']
    page_gen.update_story_count(total_stories)

    print(f"\n[OK] Added {len(new_stories)} real Reddit testimonials")
    print(f"  Total documented stories: {total_stories}")

    # Upload to FTP
    print("\n[FTP] Uploading to server...")
    if uploader.connect():
        uploader.upload_file(
            str(CONFIG['site_dir']) + '\\index.html',
            'index.html'
        )
        uploader.upload_file(
            str(CONFIG['site_dir']) + f'\\stories-page{target_page}.html',
            f'stories-page{target_page}.html'
        )
        uploader.disconnect()
    else:
        print("  [WARN] FTP failed - files saved locally only")

    db.save()

    print("\n" + "=" * 60)
    print("[DONE] Update complete!")
    print(f"  Real Reddit posts added: {len(new_stories)}")
    print(f"  Total stories: {total_stories}")
    print("=" * 60)


if __name__ == "__main__":
    main()
