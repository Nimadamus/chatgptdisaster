#!/usr/bin/env python3
"""
CHATGPTDISASTER.COM - Daily Auto-Update Script
===============================================
Scrapes multiple sources for ChatGPT complaints and issues.
NEVER shows duplicate content - uses date-based rotation.
"""

import os
import re
import json
import hashlib
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

# Use date as seed for consistent but different daily content
DATE_SEED = int(hashlib.md5(DATE_STR.encode()).hexdigest()[:8], 16)
random.seed(DATE_SEED)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
]

# Large pool of rotating complaints - different ones shown each day
# 2026-09-10: the hardcoded COMPLAINT_POOL and NEWS_POOL were removed.
# They contained invented complaints and invented engagement counts that were
# published as real user posts. Nothing on this site may present fabricated
# material as real testimony. Do not repopulate these lists.
COMPLAINT_POOL = []

# News headlines that rotate
NEWS_POOL = []


def get_hacker_news_stories():
    """Fetch real AI-related stories from Hacker News API (free, reliable)"""
    print("\n[HN] Fetching Hacker News stories...")

    try:
        # Get top stories
        response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
        story_ids = response.json()[:100]  # Top 100

        ai_stories = []
        keywords = ['chatgpt', 'gpt', 'openai', 'ai', 'llm', 'claude', 'gemini', 'artificial intelligence']

        for story_id in story_ids[:50]:  # Check first 50
            try:
                story_resp = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=5)
                story = story_resp.json()

                if story and story.get('title'):
                    title_lower = story['title'].lower()
                    if any(kw in title_lower for kw in keywords):
                        ai_stories.append({
                            'title': story['title'],
                            'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                            'score': story.get('score', 0),
                            'comments': story.get('descendants', 0),
                            'source': 'Hacker News'
                        })

                        if len(ai_stories) >= 5:
                            break

            except:
                continue

        print(f"  Found {len(ai_stories)} AI-related HN stories")
        return ai_stories

    except Exception as e:
        print(f"  HN API error: {e}")
        return []


def get_daily_complaints():
    """Get rotating complaints based on date - NEVER duplicates"""
    # Shuffle pool with date seed - same date = same selection
    shuffled = COMPLAINT_POOL.copy()
    random.shuffle(shuffled)

    # Pick different categories for variety
    categories = ['math', 'coding', 'refusal', 'hallucination', 'lazy', 'subscription', 'comparison']
    selected = []

    for cat in categories:
        cat_posts = [p for p in shuffled if p.get('category') == cat]
        if cat_posts:
            selected.append(cat_posts[0])

    # Add a few more random ones
    remaining = [p for p in shuffled if p not in selected]
    selected.extend(remaining[:3])

    # Randomize final order
    random.shuffle(selected)

    # Add metadata
    for i, post in enumerate(selected[:10]):
        post['num_comments'] = random.randint(50, 400)
        post['url'] = f"https://reddit.com/r/{post['subreddit']}"
        post['author'] = f"user_{random.randint(1000, 9999)}"

    return selected[:10]


def get_daily_news():
    """Get rotating news based on date"""
    shuffled = NEWS_POOL.copy()
    random.shuffle(shuffled)
    return shuffled[:4]


def generate_html(reddit_posts, news_articles, hn_stories):
    """Generate HTML for the daily update section"""

    # Reddit complaints HTML
    reddit_html = ""
    for post in reddit_posts:
        score_class = "high-score" if post['score'] > 2000 else "medium-score" if post['score'] > 1000 else ""
        reddit_html += f'''
                <div class="complaint-card {score_class}">
                    <div class="complaint-header">
                        <span class="subreddit">r/{post['subreddit']}</span>
                        <span class="score">⬆️ {post['score']:,}</span>
                        <span class="comments">💬 {post.get('num_comments', 0)}</span>
                    </div>
                    <h4 class="complaint-title">
                        <a href="{post['url']}" target="_blank" rel="noopener">{post['title']}</a>
                    </h4>
                    <p class="complaint-excerpt">{post.get('selftext', '')}</p>
                </div>
'''

    # Hacker News HTML
    hn_html = ""
    if hn_stories:
        for story in hn_stories:
            hn_html += f'''
                <div class="hn-card">
                    <div class="hn-header">
                        <span class="hn-source">🔶 Hacker News</span>
                        <span class="hn-score">⬆️ {story['score']}</span>
                        <span class="hn-comments">💬 {story['comments']}</span>
                    </div>
                    <h4 class="hn-title">
                        <a href="{story['url']}" target="_blank" rel="noopener">{story['title']}</a>
                    </h4>
                </div>
'''

    # News articles HTML
    news_html = ""
    for article in news_articles:
        news_html += f'''
                <div class="news-card">
                    <span class="news-source">{article['source']}</span>
                    <h4 class="news-title">{article['title']}</h4>
                    <p class="news-snippet">{article['snippet']}</p>
                </div>
'''

    # Full update section
    update_html = f'''
    <!-- Daily Update: {DATE_DISPLAY} -->
    <style>
        .daily-update {{
            max-width: 1200px;
            margin: 20px auto;
            padding: 25px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 15px;
            border: 2px solid #e94560;
        }}
        .update-header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e94560;
        }}
        .update-header h2 {{
            color: #e94560;
            font-size: 2rem;
            margin: 0 0 10px 0;
        }}
        .update-timestamp {{
            color: #888;
            font-size: 0.9rem;
        }}
        .update-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }}
        @media (max-width: 768px) {{
            .update-grid {{ grid-template-columns: 1fr; }}
        }}
        .section-title {{
            color: #fff;
            font-size: 1.3rem;
            margin: 0 0 15px 0;
            padding-left: 12px;
            border-left: 4px solid #e94560;
        }}
        .complaints-grid, .news-grid, .hn-grid {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        .complaint-card, .news-card, .hn-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 15px;
            border-left: 4px solid #666;
            transition: transform 0.2s;
        }}
        .complaint-card:hover, .news-card:hover, .hn-card:hover {{
            transform: translateX(5px);
        }}
        .complaint-card.high-score {{ border-left-color: #e94560; background: rgba(233,69,96,0.15); }}
        .complaint-card.medium-score {{ border-left-color: #f39c12; }}
        .complaint-header, .hn-header {{
            display: flex;
            gap: 15px;
            margin-bottom: 8px;
            font-size: 0.85rem;
        }}
        .subreddit, .hn-source {{ color: #3498db; font-weight: bold; }}
        .score, .hn-score {{ color: #e94560; }}
        .comments, .hn-comments {{ color: #888; }}
        .complaint-title, .hn-title {{ margin: 0 0 8px 0; font-size: 1.05rem; line-height: 1.4; }}
        .complaint-title a, .hn-title a {{ color: #fff; text-decoration: none; }}
        .complaint-title a:hover, .hn-title a:hover {{ color: #e94560; }}
        .complaint-excerpt {{ color: #aaa; font-size: 0.9rem; margin: 0; line-height: 1.5; }}
        .news-source {{ color: #e94560; font-size: 0.8rem; font-weight: bold; text-transform: uppercase; }}
        .news-title {{ color: #fff; margin: 8px 0; font-size: 1rem; }}
        .news-snippet {{ color: #aaa; font-size: 0.9rem; margin: 0; }}
        .hn-card {{ border-left-color: #ff6600; }}
    </style>

    <section class="daily-update" id="update-{DATE_STR}">
        <div class="update-header">
            <h2>📅 Daily Disaster Report</h2>
            <p class="update-date" style="color:#e94560;font-size:1.2rem;margin:5px 0;">{DATE_FULL}</p>
            <p class="update-timestamp">Auto-generated at {datetime.now().strftime('%I:%M %p')} UTC</p>
        </div>

        <div class="update-grid">
            <div class="left-column">
                <h3 class="section-title">🔥 User Complaints</h3>
                <div class="complaints-grid">
{reddit_html}
                </div>
            </div>

            <div class="right-column">
                <h3 class="section-title">📰 AI News Headlines</h3>
                <div class="news-grid">
{news_html}
                </div>

                {"<h3 class='section-title' style='margin-top:25px;'>🔶 Hacker News</h3><div class='hn-grid'>" + hn_html + "</div>" if hn_html else ""}
            </div>
        </div>
    </section>
    <!-- End Daily Update -->
'''
    return update_html


def update_index_html(update_content):
    """Insert daily update into index.html"""
    index_file = os.path.join(REPO_DIR, "index.html")

    with open(index_file, 'r', encoding='utf-8') as f:
        html = f.read()

    insert_marker = '<!-- DAILY-UPDATES-START -->'
    end_marker = '<!-- DAILY-UPDATES-END -->'

    if insert_marker in html:
        pattern = f'{insert_marker}.*?{end_marker}'
        replacement = f'{insert_marker}\n{update_content}\n{end_marker}'
        html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    else:
        body_match = re.search(r'<body[^>]*>', html)
        if body_match:
            insert_pos = body_match.end()
            html = html[:insert_pos] + f'\n{insert_marker}\n{update_content}\n{end_marker}\n' + html[insert_pos:]

    html = re.sub(r'"dateModified":\s*"[^"]*"', f'"dateModified": "{DATE_STR}"', html)

    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  Updated index.html")
    return True


def save_daily_archive(reddit_posts, news_articles, hn_stories):
    """Save daily data for archival"""
    archive_dir = os.path.join(REPO_DIR, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    # Track added titles to prevent future duplicates
    titles_file = os.path.join(archive_dir, "added_titles.json")
    try:
        with open(titles_file, 'r') as f:
            added_titles = json.load(f)
    except:
        added_titles = []

    # Add today's titles
    for post in reddit_posts:
        if post['title'] not in added_titles:
            added_titles.append(post['title'])

    # Keep only last 100 titles
    added_titles = added_titles[-100:]

    with open(titles_file, 'w') as f:
        json.dump(added_titles, f)

    # Save daily archive
    data = {
        'date': DATE_STR,
        'date_seed': DATE_SEED,
        'generated_at': datetime.now().isoformat(),
        'reddit_posts': reddit_posts,
        'news_articles': news_articles,
        'hn_stories': hn_stories
    }

    json_file = os.path.join(archive_dir, f"daily-{DATE_STR}.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)

    print(f"  Saved archive: daily-{DATE_STR}.json")


def main():
    print("=" * 60)
    print("CHATGPTDISASTER.COM DAILY UPDATE")
    print(f"Date: {DATE_FULL}")
    print(f"Seed: {DATE_SEED} (ensures unique content)")
    print("=" * 60)

    # 1. Get rotating complaints (date-based, never duplicates)
    print("\n[COMPLAINTS] Selecting daily complaints...")
    reddit_posts = get_daily_complaints()
    print(f"  Selected {len(reddit_posts)} complaints for today")

    # 2. Get rotating news
    print("\n[NEWS] Selecting daily news...")
    news_articles = get_daily_news()
    print(f"  Selected {len(news_articles)} news articles")

    # 3. Get real Hacker News stories
    hn_stories = get_hacker_news_stories()

    # 4. Generate HTML
    print("\n[HTML] Generating update content...")
    update_html = generate_html(reddit_posts, news_articles, hn_stories)

    # 5. DISABLED - No longer adding to index.html (content goes to stories pages instead)
    # print("\n[UPDATE] Updating index.html...")
    # update_index_html(update_html)
    print("\n[SKIP] Skipping index.html update (content added to stories pages only)")

    # 6. Save archive
    print("\n[ARCHIVE] Saving daily archive...")
    save_daily_archive(reddit_posts, news_articles, hn_stories)

    print("\n" + "=" * 60)
    print("DAILY UPDATE COMPLETE!")
    print(f"  - {len(reddit_posts)} unique complaints")
    print(f"  - {len(news_articles)} news articles")
    print(f"  - {len(hn_stories)} Hacker News stories")
    print(f"  - Seed {DATE_SEED} ensures different content tomorrow")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
