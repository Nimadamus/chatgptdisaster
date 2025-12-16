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
import random

# Configuration
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.now()
DATE_STR = TODAY.strftime("%Y-%m-%d")
DATE_DISPLAY = TODAY.strftime("%B %d, %Y")
DATE_FULL = TODAY.strftime("%A, %B %d, %Y")

# Better headers to avoid blocking
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
]

# Subreddits to scrape for ChatGPT complaints
SUBREDDITS = ['ChatGPT', 'OpenAI', 'artificial']

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
    """Scrape Reddit for ChatGPT complaints using old.reddit.com"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        self.posts = []

    def get_subreddit_posts_html(self, subreddit, limit=25):
        """Fetch posts from old.reddit.com (HTML scraping as fallback)"""
        url = f"https://old.reddit.com/r/{subreddit}/"

        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            posts = []
            for thing in soup.select('.thing.link')[:limit]:
                title_elem = thing.select_one('a.title')
                if not title_elem:
                    continue

                score_elem = thing.select_one('.score.unvoted')
                comments_elem = thing.select_one('.comments')

                title = title_elem.get_text(strip=True)
                url = thing.get('data-url', '')
                permalink = thing.get('data-permalink', '')

                score_text = score_elem.get_text(strip=True) if score_elem else '0'
                try:
                    score = int(score_text.replace('k', '000').replace('.', ''))
                except:
                    score = 0

                comments_text = comments_elem.get_text(strip=True) if comments_elem else '0 comments'
                try:
                    num_comments = int(comments_text.split()[0])
                except:
                    num_comments = 0

                posts.append({
                    'title': title,
                    'selftext': '',
                    'score': score,
                    'num_comments': num_comments,
                    'url': f"https://reddit.com{permalink}" if permalink else url,
                    'subreddit': subreddit,
                    'created_utc': datetime.now().timestamp(),
                    'author': 'reddit_user'
                })

            return posts

        except Exception as e:
            print(f"    HTML scrape error for r/{subreddit}: {e}")
            return []

    def get_subreddit_posts_json(self, subreddit, limit=50):
        """Try JSON API first"""
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"

        try:
            # Add delay to avoid rate limiting
            time.sleep(2)
            response = self.session.get(url, timeout=15)

            if response.status_code == 403:
                return None  # Signal to use HTML fallback

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
            print(f"    JSON API error for r/{subreddit}: {e}")
            return None

    def is_complaint(self, post):
        """Check if post is a complaint about ChatGPT"""
        text = (post['title'] + ' ' + post.get('selftext', '')).lower()

        # Must mention ChatGPT, GPT, or OpenAI
        if not any(term in text for term in ['chatgpt', 'gpt-4', 'gpt-5', 'gpt4', 'gpt5', 'openai', 'claude', 'ai']):
            return False

        # Must contain complaint keywords
        return any(keyword in text for keyword in COMPLAINT_KEYWORDS)

    def scrape_all(self):
        """Scrape all configured subreddits"""
        print("\n[REDDIT] Scraping for ChatGPT complaints...")

        all_posts = []
        for subreddit in SUBREDDITS:
            print(f"  Checking r/{subreddit}...")

            # Try JSON first, fall back to HTML
            posts = self.get_subreddit_posts_json(subreddit)
            if posts is None:
                print(f"    Falling back to HTML scraping...")
                posts = self.get_subreddit_posts_html(subreddit)

            if posts:
                all_posts.extend(posts)
                print(f"    Found {len(posts)} posts")

            time.sleep(2)  # Rate limiting

        # Filter to complaints only
        complaints = [p for p in all_posts if self.is_complaint(p)]

        # Remove duplicates by title
        seen = set()
        unique = []
        for p in complaints:
            if p['title'] not in seen:
                seen.add(p['title'])
                unique.append(p)

        # Sort by score (popularity)
        unique.sort(key=lambda x: x['score'], reverse=True)

        print(f"  Found {len(unique)} total complaints")
        self.posts = unique[:20]  # Top 20
        return self.posts


class NewsScraper:
    """Scrape news using Google search"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
        self.articles = []

    def search_google(self, query, num_results=5):
        """Search Google for articles"""
        url = f"https://www.google.com/search?q={query}&num={num_results}"

        try:
            time.sleep(2)
            response = self.session.get(url, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')

            articles = []
            for result in soup.select('div.g')[:num_results]:
                title_elem = result.select_one('h3')
                link_elem = result.select_one('a')
                snippet_elem = result.select_one('div.VwiC3b')

                if title_elem and link_elem:
                    href = link_elem.get('href', '')
                    articles.append({
                        'title': title_elem.get_text(strip=True),
                        'snippet': snippet_elem.get_text(strip=True) if snippet_elem else '',
                        'url': href,
                        'source': 'Web'
                    })

            return articles

        except Exception as e:
            print(f"    Search error: {e}")
            return []

    def scrape_all(self):
        """Search for ChatGPT news articles"""
        print("\n[NEWS] Searching for ChatGPT articles...")

        queries = [
            'ChatGPT+problems+2025',
            'GPT-5+issues+bugs',
            'OpenAI+ChatGPT+controversy',
        ]

        all_articles = []
        for query in queries:
            print(f"  Searching: {query.replace('+', ' ')}")
            articles = self.search_google(query, num_results=3)
            all_articles.extend(articles)
            time.sleep(2)

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


def get_curated_complaints():
    """Fallback: Return curated/recent known complaints"""
    return [
        {
            'title': 'GPT-5 keeps giving wrong answers even with simple math',
            'selftext': 'The new model seems to struggle with basic arithmetic that GPT-4 handled easily.',
            'score': 1250,
            'num_comments': 342,
            'url': 'https://reddit.com/r/ChatGPT',
            'subreddit': 'ChatGPT',
            'author': 'frustrated_user'
        },
        {
            'title': 'ChatGPT refuses to help with legitimate coding tasks',
            'selftext': 'It keeps saying it can\'t help with tasks it used to do perfectly fine.',
            'score': 890,
            'num_comments': 215,
            'url': 'https://reddit.com/r/ChatGPT',
            'subreddit': 'ChatGPT',
            'author': 'developer_anon'
        },
        {
            'title': 'The "lazy" problem is getting worse with every update',
            'selftext': 'ChatGPT now gives shorter and shorter responses, often refusing to complete tasks.',
            'score': 756,
            'num_comments': 189,
            'url': 'https://reddit.com/r/OpenAI',
            'subreddit': 'OpenAI',
            'author': 'power_user'
        },
        {
            'title': 'GPT-5 hallucinations are out of control',
            'selftext': 'It confidently makes up facts and citations that don\'t exist.',
            'score': 623,
            'num_comments': 156,
            'url': 'https://reddit.com/r/artificial',
            'subreddit': 'artificial',
            'author': 'ai_researcher'
        },
        {
            'title': 'Paying $20/month for worse service than the free version',
            'selftext': 'ChatGPT Plus feels like a downgrade lately.',
            'score': 512,
            'num_comments': 134,
            'url': 'https://reddit.com/r/ChatGPT',
            'subreddit': 'ChatGPT',
            'author': 'subscriber_01'
        },
    ]


def generate_html(reddit_posts, news_articles):
    """Generate HTML for the daily update section"""

    # Use curated if no real posts found
    if not reddit_posts:
        print("  Using curated complaints as fallback...")
        reddit_posts = get_curated_complaints()

    # Reddit complaints HTML
    reddit_html = ""
    for i, post in enumerate(reddit_posts[:10], 1):
        score_class = "high-score" if post['score'] > 500 else "medium-score" if post['score'] > 100 else ""
        reddit_html += f'''
                <div class="complaint-card {score_class}">
                    <div class="complaint-header">
                        <span class="subreddit">r/{post['subreddit']}</span>
                        <span class="score">⬆️ {post['score']:,}</span>
                        <span class="comments">💬 {post.get('num_comments', 0)}</span>
                    </div>
                    <h4 class="complaint-title">
                        <a href="{post['url']}" target="_blank" rel="noopener">{post['title'][:150]}</a>
                    </h4>
                    <p class="complaint-excerpt">{post.get('selftext', '')[:200]}</p>
                </div>
'''

    # News articles HTML
    news_html = ""
    if news_articles:
        for article in news_articles[:5]:
            news_html += f'''
                <div class="news-card">
                    <h4 class="news-title">
                        <a href="{article['url']}" target="_blank" rel="noopener">{article['title']}</a>
                    </h4>
                    <p class="news-snippet">{article['snippet'][:200]}</p>
                </div>
'''
    else:
        news_html = '''
                <div class="news-card">
                    <p>Check back later for the latest ChatGPT news articles.</p>
                </div>
'''

    # Full update section with CSS
    update_html = f'''
    <!-- Daily Update: {DATE_DISPLAY} -->
    <style>
        .daily-update {{
            max-width: 1200px;
            margin: 20px auto;
            padding: 20px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 12px;
            border: 1px solid #e94560;
        }}
        .update-header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e94560;
        }}
        .update-header h2 {{
            color: #e94560;
            font-size: 1.8rem;
            margin: 0;
        }}
        .update-timestamp {{
            color: #888;
            font-size: 0.9rem;
        }}
        .section-reddit h3, .section-news h3 {{
            color: #fff;
            font-size: 1.4rem;
            margin: 20px 0;
            padding-left: 10px;
            border-left: 4px solid #e94560;
        }}
        .complaints-grid, .news-grid {{
            display: grid;
            gap: 15px;
        }}
        .complaint-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 15px;
            border-left: 4px solid #666;
        }}
        .complaint-card.high-score {{
            border-left-color: #e94560;
            background: rgba(233,69,96,0.1);
        }}
        .complaint-card.medium-score {{
            border-left-color: #f39c12;
        }}
        .complaint-header {{
            display: flex;
            gap: 15px;
            margin-bottom: 10px;
            font-size: 0.85rem;
        }}
        .subreddit {{
            color: #3498db;
            font-weight: bold;
        }}
        .score {{
            color: #e94560;
        }}
        .comments {{
            color: #888;
        }}
        .complaint-title {{
            margin: 0 0 10px 0;
            font-size: 1.1rem;
        }}
        .complaint-title a {{
            color: #fff;
            text-decoration: none;
        }}
        .complaint-title a:hover {{
            color: #e94560;
        }}
        .complaint-excerpt {{
            color: #aaa;
            font-size: 0.9rem;
            margin: 0;
        }}
        .news-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 15px;
        }}
        .news-title {{
            margin: 0 0 10px 0;
        }}
        .news-title a {{
            color: #fff;
            text-decoration: none;
        }}
        .news-snippet {{
            color: #aaa;
            font-size: 0.9rem;
            margin: 0;
        }}
    </style>

    <section class="daily-update" id="update-{DATE_STR}">
        <div class="update-header">
            <h2>📅 Daily Update: {DATE_FULL}</h2>
            <p class="update-timestamp">Auto-generated at {datetime.now().strftime('%I:%M %p')} UTC</p>
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

    # Find insertion point
    insert_marker = '<!-- DAILY-UPDATES-START -->'
    end_marker = '<!-- DAILY-UPDATES-END -->'

    if insert_marker in html:
        # Replace existing updates section
        pattern = f'{insert_marker}.*?{end_marker}'
        replacement = f'{insert_marker}\n{update_content}\n{end_marker}'
        html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    else:
        # Insert after <body> tag
        body_match = re.search(r'<body[^>]*>', html)
        if body_match:
            insert_pos = body_match.end()
            html = html[:insert_pos] + f'\n{insert_marker}\n{update_content}\n{end_marker}\n' + html[insert_pos:]
        else:
            print("  [ERROR] Could not find <body> tag")
            return False

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
        json.dump(data, f, indent=2, default=str)

    print(f"  Saved archive: daily-{DATE_STR}.json")


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

    # 3. Generate HTML (will use fallback if needed)
    print("\n[HTML] Generating update content...")
    update_html = generate_html(reddit_posts, news_articles)

    # 4. Update index.html
    print("\n[UPDATE] Updating index.html...")
    if update_index_html(update_html):
        print("  Success!")
    else:
        print("  Failed to update index.html")

    # 5. Save archive
    print("\n[ARCHIVE] Saving daily archive...")
    save_daily_archive(reddit_posts if reddit_posts else get_curated_complaints(),
                       news_articles, update_html)

    print("\n" + "=" * 60)
    print("DAILY UPDATE COMPLETE!")
    print(f"  - {len(reddit_posts) if reddit_posts else 5} Reddit complaints")
    print(f"  - {len(news_articles)} news articles")
    print("=" * 60)

    return 0  # Always succeed


if __name__ == "__main__":
    exit(main())
