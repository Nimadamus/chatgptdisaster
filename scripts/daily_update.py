#!/usr/bin/env python3
"""
CHATGPTDISASTER.COM - Daily Auto-Update Script
===============================================
Scrapes Reddit and news sources for ChatGPT complaints and issues.
Generates HTML content and updates the site.
"""

import os
import re
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time

# Configuration
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.now()
DATE_STR = TODAY.strftime("%Y-%m-%d")
DATE_DISPLAY = TODAY.strftime("%B %d, %Y")
DATE_FULL = TODAY.strftime("%A, %B %d, %Y")

# Reddit API (no auth needed for public posts)
REDDIT_HEADERS = {
    'User-Agent': 'ChatGPTDisaster/1.0 (Educational Research Bot)'
}

# Subreddits to scrape for ChatGPT complaints
SUBREDDITS = ['ChatGPT', 'OpenAI', 'artificial', 'singularity']

# Keywords for filtering relevant posts
COMPLAINT_KEYWORDS = [
    'worse', 'broken', 'stupid', 'dumb', 'useless', 'trash', 'garbage',
    'downgrade', 'nerf', 'lobotomized', 'lazy', 'refuses', 'won\'t',
    'can\'t', 'doesn\'t work', 'not working', 'bug', 'error', 'issue',
    'problem', 'frustrated', 'disappointed', 'terrible', 'awful',
    'disaster', 'nightmare', 'regression', 'degraded', 'ruined',
    'hate', 'sucks', 'fail', 'failed', 'failing', 'hallucination',
    'wrong', 'incorrect', 'inaccurate', 'lying', 'made up', 'fake',
    'gpt-5', 'gpt5', 'update', 'latest version', 'new model'
]


class RedditScraper:
    """Scrape Reddit for ChatGPT complaints"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(REDDIT_HEADERS)
        self.posts = []

    def get_subreddit_posts(self, subreddit, limit=50, sort='hot'):
        """Fetch posts from a subreddit"""
        url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"

        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()

            posts = []
            for child in data.get('data', {}).get('children', []):
                post = child.get('data', {})
                posts.append({
                    'title': post.get('title', ''),
                    'selftext': post.get('selftext', '')[:500],
                    'score': post.get('score', 0),
                    'num_comments': post.get('num_comments', 0),
                    'url': f"https://reddit.com{post.get('permalink', '')}",
                    'subreddit': subreddit,
                    'created_utc': post.get('created_utc', 0),
                    'author': post.get('author', '[deleted]')
                })

            return posts

        except Exception as e:
            print(f"  Error fetching r/{subreddit}: {e}")
            return []

    def is_complaint(self, post):
        """Check if post is a complaint about ChatGPT"""
        text = (post['title'] + ' ' + post['selftext']).lower()

        # Must mention ChatGPT, GPT, or OpenAI
        if not any(term in text for term in ['chatgpt', 'gpt-4', 'gpt-5', 'gpt4', 'gpt5', 'openai', 'claude']):
            return False

        # Must contain complaint keywords
        return any(keyword in text for keyword in COMPLAINT_KEYWORDS)

    def scrape_all(self):
        """Scrape all configured subreddits"""
        print("\n[REDDIT] Scraping for ChatGPT complaints...")

        all_posts = []
        for subreddit in SUBREDDITS:
            print(f"  Checking r/{subreddit}...")

            # Get hot and new posts
            hot_posts = self.get_subreddit_posts(subreddit, limit=50, sort='hot')
            new_posts = self.get_subreddit_posts(subreddit, limit=25, sort='new')

            all_posts.extend(hot_posts)
            all_posts.extend(new_posts)

            time.sleep(1)  # Rate limiting

        # Filter to complaints only
        complaints = [p for p in all_posts if self.is_complaint(p)]

        # Remove duplicates by URL
        seen = set()
        unique = []
        for p in complaints:
            if p['url'] not in seen:
                seen.add(p['url'])
                unique.append(p)

        # Sort by score (popularity)
        unique.sort(key=lambda x: x['score'], reverse=True)

        # Filter to recent posts (last 7 days)
        week_ago = datetime.now().timestamp() - (7 * 24 * 60 * 60)
        recent = [p for p in unique if p['created_utc'] > week_ago]

        print(f"  Found {len(recent)} recent complaints")
        self.posts = recent[:20]  # Top 20
        return self.posts


class NewsScraper:
    """Scrape news for ChatGPT-related articles"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.articles = []

    def search_google_news(self, query, num_results=10):
        """Search Google News for articles"""
        # Using DuckDuckGo as it doesn't require API key
        url = f"https://html.duckduckgo.com/html/?q={query}+site:news"

        try:
            response = self.session.get(url, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')

            articles = []
            for result in soup.select('.result')[:num_results]:
                title_elem = result.select_one('.result__title')
                snippet_elem = result.select_one('.result__snippet')
                link_elem = result.select_one('.result__url')

                if title_elem:
                    articles.append({
                        'title': title_elem.get_text(strip=True),
                        'snippet': snippet_elem.get_text(strip=True) if snippet_elem else '',
                        'url': link_elem.get('href', '') if link_elem else '',
                        'source': 'News'
                    })

            return articles

        except Exception as e:
            print(f"  Error searching news: {e}")
            return []

    def scrape_all(self):
        """Search for ChatGPT news articles"""
        print("\n[NEWS] Searching for ChatGPT articles...")

        queries = [
            'ChatGPT problems 2025',
            'GPT-5 issues complaints',
            'OpenAI ChatGPT bugs',
            'ChatGPT worse update',
            'ChatGPT controversy'
        ]

        all_articles = []
        for query in queries:
            print(f"  Searching: {query}")
            articles = self.search_google_news(query, num_results=5)
            all_articles.extend(articles)
            time.sleep(1)

        # Remove duplicates
        seen = set()
        unique = []
        for a in all_articles:
            if a['title'] not in seen:
                seen.add(a['title'])
                unique.append(a)

        print(f"  Found {len(unique)} articles")
        self.articles = unique[:10]
        return self.articles


def generate_html(reddit_posts, news_articles):
    """Generate HTML for the daily update section"""

    # Reddit complaints HTML
    reddit_html = ""
    for i, post in enumerate(reddit_posts[:10], 1):
        score_class = "high-score" if post['score'] > 100 else "medium-score" if post['score'] > 20 else ""
        reddit_html += f'''
        <div class="complaint-card {score_class}">
            <div class="complaint-header">
                <span class="subreddit">r/{post['subreddit']}</span>
                <span class="score">⬆️ {post['score']:,}</span>
                <span class="comments">💬 {post['num_comments']}</span>
            </div>
            <h4 class="complaint-title">
                <a href="{post['url']}" target="_blank" rel="noopener">{post['title'][:150]}</a>
            </h4>
            <p class="complaint-excerpt">{post['selftext'][:200]}...</p>
            <div class="complaint-meta">
                <span class="author">u/{post['author']}</span>
            </div>
        </div>
'''

    # News articles HTML
    news_html = ""
    for article in news_articles[:5]:
        news_html += f'''
        <div class="news-card">
            <h4 class="news-title">
                <a href="{article['url']}" target="_blank" rel="noopener">{article['title']}</a>
            </h4>
            <p class="news-snippet">{article['snippet']}</p>
            <span class="news-source">{article['source']}</span>
        </div>
'''

    # Full update section
    update_html = f'''
    <!-- Daily Update: {DATE_DISPLAY} -->
    <section class="daily-update" id="update-{DATE_STR}">
        <div class="update-header">
            <h2>📅 Daily Update: {DATE_FULL}</h2>
            <p class="update-timestamp">Auto-generated at {datetime.now().strftime('%I:%M %p ET')}</p>
        </div>

        <div class="section-reddit">
            <h3>🔥 Top Reddit Complaints This Week</h3>
            <div class="complaints-grid">
{reddit_html}
            </div>
        </div>

        <div class="section-news">
            <h3>📰 Latest ChatGPT News</h3>
            <div class="news-grid">
{news_html}
            </div>
        </div>
    </section>
    <!-- End Daily Update -->
'''

    return update_html


def update_index_html(update_content):
    """Insert daily update into index.html"""
    index_file = os.path.join(REPO_DIR, "index.html")

    if not os.path.exists(index_file):
        print(f"  [ERROR] index.html not found at {index_file}")
        return False

    with open(index_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find insertion point (after header, before main content)
    # Look for a marker comment or specific element
    insert_marker = '<!-- DAILY-UPDATES-START -->'
    end_marker = '<!-- DAILY-UPDATES-END -->'

    if insert_marker in html:
        # Replace existing updates section
        pattern = f'{insert_marker}.*?{end_marker}'
        replacement = f'{insert_marker}\n{update_content}\n{end_marker}'
        html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    else:
        # Insert after opening body or main element
        if '<main' in html:
            html = html.replace('<main', f'{insert_marker}\n{update_content}\n{end_marker}\n<main', 1)
        elif '<body' in html:
            # Find end of body tag
            body_match = re.search(r'<body[^>]*>', html)
            if body_match:
                insert_pos = body_match.end()
                html = html[:insert_pos] + f'\n{insert_marker}\n{update_content}\n{end_marker}\n' + html[insert_pos:]

    # Update the dateModified in schema
    html = re.sub(
        r'"dateModified":\s*"[^"]*"',
        f'"dateModified": "{DATE_STR}"',
        html
    )

    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  Updated index.html with daily content")
    return True


def save_daily_archive(reddit_posts, news_articles, update_html):
    """Save daily data for archival"""
    archive_dir = os.path.join(REPO_DIR, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    # Save JSON data
    data = {
        'date': DATE_STR,
        'generated_at': datetime.now().isoformat(),
        'reddit_posts': reddit_posts,
        'news_articles': news_articles
    }

    json_file = os.path.join(archive_dir, f"daily-{DATE_STR}.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    # Save HTML archive
    html_file = os.path.join(archive_dir, f"daily-{DATE_STR}.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(update_html)

    print(f"  Saved archive: daily-{DATE_STR}.json/.html")


def main():
    print("=" * 60)
    print("CHATGPTDISASTER.COM DAILY UPDATE")
    print(f"Date: {DATE_FULL}")
    print("=" * 60)

    # 1. Scrape Reddit
    reddit = RedditScraper()
    reddit_posts = reddit.scrape_all()

    # 2. Scrape News
    news = NewsScraper()
    news_articles = news.scrape_all()

    if not reddit_posts and not news_articles:
        print("\n[WARNING] No content found - skipping update")
        return 1

    # 3. Generate HTML
    print("\n[HTML] Generating update content...")
    update_html = generate_html(reddit_posts, news_articles)

    # 4. Update index.html
    print("\n[UPDATE] Updating index.html...")
    update_index_html(update_html)

    # 5. Save archive
    print("\n[ARCHIVE] Saving daily archive...")
    save_daily_archive(reddit_posts, news_articles, update_html)

    print("\n" + "=" * 60)
    print("DAILY UPDATE COMPLETE!")
    print(f"  - {len(reddit_posts)} Reddit complaints")
    print(f"  - {len(news_articles)} news articles")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
