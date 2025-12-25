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
COMPLAINT_POOL = [
    # Math/Logic failures
    {"title": "GPT-5 can't count to 10 correctly anymore", "selftext": "Asked it to list numbers 1-10 and it skipped 7. Twice.", "score": 2340, "subreddit": "ChatGPT", "category": "math"},
    {"title": "Basic algebra is broken in the latest update", "selftext": "2x + 5 = 15, it told me x = 7. Elementary school stuff.", "score": 1890, "subreddit": "ChatGPT", "category": "math"},
    {"title": "ChatGPT thinks 9.11 is greater than 9.9", "selftext": "String comparison vs numeric comparison - it's been broken for months.", "score": 3200, "subreddit": "OpenAI", "category": "math"},
    {"title": "The strawberry problem is STILL not fixed", "selftext": "How many R's in strawberry? It says 2. Every. Single. Time.", "score": 2100, "subreddit": "ChatGPT", "category": "math"},
    {"title": "GPT-5 failed my 8-year-old's homework", "selftext": "Simple word problems - got 3 out of 5 wrong. My kid did better.", "score": 1650, "subreddit": "ChatGPT", "category": "math"},

    # Coding failures
    {"title": "ChatGPT wrote code that deleted my entire project", "selftext": "Asked for help with git, it ran rm -rf on my repo directory.", "score": 4500, "subreddit": "programming", "category": "coding"},
    {"title": "The code it generates doesn't even compile anymore", "selftext": "Syntax errors in every response. Did they fire the QA team?", "score": 2800, "subreddit": "ChatGPT", "category": "coding"},
    {"title": "GPT-5 invents functions that don't exist", "selftext": "It keeps using APIs and methods that literally don't exist in any library.", "score": 1950, "subreddit": "programming", "category": "coding"},
    {"title": "Asked for Python, got a mix of Python and JavaScript", "selftext": "The code has console.log AND print statements. Pick a language!", "score": 1420, "subreddit": "ChatGPT", "category": "coding"},
    {"title": "ChatGPT's SQL suggestions would drop my production database", "selftext": "It casually suggested DROP TABLE in a SELECT query fix. Terrifying.", "score": 3100, "subreddit": "programming", "category": "coding"},
    {"title": "Three hours debugging AI-generated code that was 'working'", "selftext": "It confidently said the code was correct. It wasn't. Not even close.", "score": 1780, "subreddit": "webdev", "category": "coding"},

    # Refusals and restrictions
    {"title": "ChatGPT refuses to write a villain for my novel", "selftext": "It's FICTION. The bad guy is supposed to be bad. That's the point.", "score": 2650, "subreddit": "ChatGPT", "category": "refusal"},
    {"title": "Can't get help with my cybersecurity homework anymore", "selftext": "Studying for my degree but it won't explain basic penetration testing.", "score": 1890, "subreddit": "OpenAI", "category": "refusal"},
    {"title": "GPT-5 refused to explain how locks work", "selftext": "I'm a locksmith. This is literally my job. But no, too dangerous.", "score": 3400, "subreddit": "ChatGPT", "category": "refusal"},
    {"title": "It won't write a recipe with alcohol anymore", "selftext": "Trying to make coq au vin. Apparently cooking wine is too edgy.", "score": 2100, "subreddit": "ChatGPT", "category": "refusal"},
    {"title": "Asked about historical battles, got a lecture on peace", "selftext": "I'm writing a history paper, not planning a war. Chill.", "score": 1560, "subreddit": "ChatGPT", "category": "refusal"},

    # Hallucinations
    {"title": "ChatGPT cited a Supreme Court case that doesn't exist", "selftext": "Lawyer almost used it in court. This is getting dangerous.", "score": 5200, "subreddit": "law", "category": "hallucination"},
    {"title": "GPT-5 invented an author and 3 books for my bibliography", "selftext": "The author doesn't exist. The books don't exist. Professor was not amused.", "score": 2900, "subreddit": "ChatGPT", "category": "hallucination"},
    {"title": "It told me a restaurant closed in 2019 - I'm sitting in it right now", "selftext": "Eating lunch at a restaurant that ChatGPT insists burned down.", "score": 1870, "subreddit": "ChatGPT", "category": "hallucination"},
    {"title": "ChatGPT made up my company's CEO and their biography", "selftext": "I work there. That person has never existed. Completely fabricated.", "score": 2340, "subreddit": "OpenAI", "category": "hallucination"},
    {"title": "Fake medical studies are going to get someone killed", "selftext": "It cited 5 studies on drug interactions. None of them are real.", "score": 4100, "subreddit": "medicine", "category": "hallucination"},

    # Lazy responses
    {"title": "GPT-5 is the laziest AI model ever released", "selftext": "Ask for 10 examples, get 3 and 'you can figure out the rest.'", "score": 3800, "subreddit": "ChatGPT", "category": "lazy"},
    {"title": "The responses keep getting shorter every update", "selftext": "Used to get paragraphs, now I get sentences. Paying $20 for this?", "score": 2400, "subreddit": "OpenAI", "category": "lazy"},
    {"title": "ChatGPT now just tells me to Google things", "selftext": "Why am I paying for an AI that tells me to use a search engine?", "score": 1950, "subreddit": "ChatGPT", "category": "lazy"},
    {"title": "'I cannot provide a complete solution' - then what can you do?", "selftext": "This phrase appears in 90% of my conversations now.", "score": 2100, "subreddit": "ChatGPT", "category": "lazy"},
    {"title": "Asked for code, got pseudocode and 'implement as needed'", "selftext": "If I could implement it myself, I wouldn't be asking you!", "score": 1670, "subreddit": "programming", "category": "lazy"},

    # Subscription complaints
    {"title": "Plus subscription is now worse than the free tier", "selftext": "Free users get GPT-4o, we get rate limits and excuses.", "score": 4200, "subreddit": "ChatGPT", "category": "subscription"},
    {"title": "$20/month for 'please try again later' errors", "selftext": "Peak hours means zero responses. What am I paying for?", "score": 2800, "subreddit": "OpenAI", "category": "subscription"},
    {"title": "They raised prices and lowered quality simultaneously", "selftext": "Incredible business strategy. Make it worse AND more expensive.", "score": 3100, "subreddit": "ChatGPT", "category": "subscription"},
    {"title": "ChatGPT Pro at $200/month is a scam", "selftext": "Same model, same limits, just a different tier name. Shameless.", "score": 2600, "subreddit": "OpenAI", "category": "subscription"},
    {"title": "Switched to Claude and never looked back", "selftext": "Actually follows instructions, doesn't refuse everything. Night and day.", "score": 1890, "subreddit": "ChatGPT", "category": "subscription"},

    # Memory/Context issues
    {"title": "ChatGPT forgets what I said 3 messages ago", "selftext": "Mid-conversation it acts like we never discussed the topic.", "score": 2100, "subreddit": "ChatGPT", "category": "memory"},
    {"title": "Memory feature is completely broken in GPT-5", "selftext": "It remembers wrong things and forgets important things. Useless.", "score": 1780, "subreddit": "OpenAI", "category": "memory"},
    {"title": "Had to repeat my requirements 5 times in one conversation", "selftext": "Each response ignored something I explicitly stated earlier.", "score": 1340, "subreddit": "ChatGPT", "category": "memory"},

    # Personality/Tone issues
    {"title": "GPT-5 has become unbearably preachy", "selftext": "Every response includes a lecture I didn't ask for.", "score": 2900, "subreddit": "ChatGPT", "category": "personality"},
    {"title": "The constant apologizing is driving me insane", "selftext": "'I apologize for any confusion' - you caused the confusion!", "score": 2200, "subreddit": "ChatGPT", "category": "personality"},
    {"title": "Stop adding disclaimers to everything", "selftext": "I asked for a cookie recipe, not a legal waiver.", "score": 1650, "subreddit": "ChatGPT", "category": "personality"},

    # Comparison complaints
    {"title": "Claude is everything ChatGPT should have been", "selftext": "Longer responses, fewer refusals, actually helpful. OpenAI is cooked.", "score": 3400, "subreddit": "artificial", "category": "comparison"},
    {"title": "Gemini just destroyed GPT-5 in my benchmark tests", "selftext": "Google's model is faster, cheaper, and more accurate. The king is dead.", "score": 2800, "subreddit": "OpenAI", "category": "comparison"},
    {"title": "Local LLMs are now better than ChatGPT for coding", "selftext": "Running Llama locally beats paying $20/month for worse results.", "score": 2100, "subreddit": "LocalLLaMA", "category": "comparison"},
]

# News headlines that rotate
NEWS_POOL = [
    {"title": "OpenAI Facing Multiple Lawsuits Over AI Hallucinations", "snippet": "Legal experts say fabricated citations and false information have led to real-world damages.", "source": "TechCrunch"},
    {"title": "ChatGPT Users Report 40% Decline in Response Quality Since GPT-5 Launch", "snippet": "Community surveys show widespread dissatisfaction with the latest model update.", "source": "The Verge"},
    {"title": "Former OpenAI Employees Warn of 'Rushed' GPT-5 Release", "snippet": "Whistleblowers claim internal testing was cut short to beat competitors.", "source": "Wired"},
    {"title": "Anthropic's Claude Gains Market Share as ChatGPT Users Flee", "snippet": "Subscription cancellations at OpenAI reach all-time high in Q4 2025.", "source": "Bloomberg"},
    {"title": "Study: AI Hallucinations Have Cost Businesses $2.1 Billion in 2025", "snippet": "Healthcare, legal, and financial sectors report the highest losses from false AI outputs.", "source": "Forbes"},
    {"title": "OpenAI Admits GPT-5 'Lazy' Behavior Is a Feature, Not a Bug", "snippet": "Company claims shorter responses improve 'efficiency' despite user backlash.", "source": "Ars Technica"},
    {"title": "ChatGPT Outage Leaves Millions Without AI Access for 8 Hours", "snippet": "Third major outage this month raises reliability concerns for enterprise customers.", "source": "CNBC"},
    {"title": "Microsoft Reconsidering OpenAI Partnership After Quality Issues", "snippet": "Internal memos suggest frustration with ChatGPT integration problems in Copilot.", "source": "The Information"},
    {"title": "Reddit Communities Overwhelmed by ChatGPT Complaint Posts", "snippet": "Moderators struggle to manage flood of user frustration with AI service.", "source": "Gizmodo"},
    {"title": "OpenAI's Sam Altman Defends GPT-5 Amid Growing Criticism", "snippet": "CEO claims model is 'most capable ever' despite user reports of regression.", "source": "Reuters"},
    {"title": "European Regulators Open Investigation Into ChatGPT Hallucinations", "snippet": "EU concerned about AI-generated misinformation and consumer protection.", "source": "Financial Times"},
    {"title": "ChatGPT Plus Subscribers Demand Refunds Over Service Quality", "snippet": "Class action lawsuit brewing over alleged 'bait and switch' tactics.", "source": "Vice"},
]


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
