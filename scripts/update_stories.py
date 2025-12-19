#!/usr/bin/env python3
"""Add new testimonials to stories.html from Reddit scrape data."""

import os
import re
import json
from datetime import datetime

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE_DISPLAY = datetime.now().strftime("%B %d, %Y")

def categorize_complaint(title, selftext):
    text = (title + ' ' + selftext).lower()
    if any(w in text for w in ['memory', 'forgot', 'remember', 'context']):
        return 'memory-issues', 'Memory Issues'
    elif any(w in text for w in ['personality', 'tone', 'cold', 'robotic']):
        return 'lost-personality', 'Lost Personality'
    elif any(w in text for w in ['forced', 'upgrade', 'model picker']):
        return 'forced-upgrade', 'Forced Upgrades'
    elif any(w in text for w in ['mental', 'therapy', 'depression']):
        return 'mental-health', 'Mental Health'
    else:
        return 'performance-issues', 'Performance Issues'

def format_score(score):
    if score >= 1000:
        return f"{score/1000:.1f}k"
    return str(score)

def generate_story_card(post, is_hot=False):
    category_id, category_label = categorize_complaint(post['title'], post.get('selftext', ''))
    title = post['title'][:120] + ('...' if len(post['title']) > 120 else '')
    selftext = post.get('selftext', '').strip()
    description = selftext[:300] + '...' if selftext and len(selftext) > 300 else selftext
    if not description:
        description = f"A user on r/{post['subreddit']} shared their frustration with ChatGPT."
    quote = post['title'][:200]
    badge_html = '<div class="featured-badge">NEW</div>' if is_hot else ''
    author = post.get('author', 'RedditUser')
    if author == '[deleted]':
        author = 'Anonymous'
    
    return f'''<article class="story-card" data-category="{category_id}">
{badge_html}
<div class="category-tag">{category_label}</div>
<div class="story-header">
<div class="reddit-icon">r/</div>
<div class="story-meta">
<h2>{title}</h2>
<div class="story-info">u/{author} - r/{post['subreddit']} - {DATE_DISPLAY}</div>
</div>
</div>
<div class="story-content">
<p>{description}</p>
<div class="quote-highlight">"{quote}"</div>
</div>
<div class="story-stats">
<div class="stat-item upvotes">Up {format_score(post['score'])}</div>
<div class="stat-item comments">{post.get('num_comments', 0)} comments</div>
<div class="stat-item">{DATE_DISPLAY}</div>
</div>
</article>
'''

def main():
    print("[STORIES] Updating stories.html with new testimonials...")
    
    # Load latest archive
    archive_dir = os.path.join(REPO_DIR, "archive")
    today = datetime.now().strftime("%Y-%m-%d")
    archive_file = os.path.join(archive_dir, f"daily-{today}.json")
    
    if not os.path.exists(archive_file):
        print(f"  No archive found for today: {archive_file}")
        return 1
    
    with open(archive_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    reddit_posts = data.get('reddit_posts', [])
    if not reddit_posts:
        print("  No Reddit posts in archive")
        return 1
    
    # Load stories.html
    stories_file = os.path.join(REPO_DIR, "stories.html")
    if not os.path.exists(stories_file):
        print("  stories.html not found")
        return 1
    
    with open(stories_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Load previously added titles
    added_titles_file = os.path.join(archive_dir, "added_titles.json")
    if os.path.exists(added_titles_file):
        with open(added_titles_file, 'r', encoding='utf-8') as f:
            added_titles = set(json.load(f))
    else:
        added_titles = set()
    
    # Filter new posts
    new_posts = [p for p in reddit_posts if p['title'] not in added_titles]
    if not new_posts:
        print("  No new unique testimonials to add")
        return 0
    
    # Take top 5 new posts
    posts_to_add = new_posts[:5]
    
    # Generate cards
    new_cards = f"\n<!-- AUTO-ADDED TESTIMONIALS: {DATE_DISPLAY} -->\n"
    for i, post in enumerate(posts_to_add):
        is_hot = (i == 0 and post['score'] > 100)
        new_cards += generate_story_card(post, is_hot)
    new_cards += f"<!-- END AUTO-ADDED -->\n"
    
    # Insert into stories.html
    insert_marker = '<div class="stories-grid" id="storiesGrid">'
    if insert_marker in html:
        insert_pos = html.find(insert_marker) + len(insert_marker)
        html = html[:insert_pos] + "\n" + new_cards + html[insert_pos:]
    else:
        print("  Could not find stories-grid")
        return 1
    
    # Update count in meta
    count_match = re.search(r'(\d+)\+? Real ChatGPT', html)
    if count_match:
        old_count = int(count_match.group(1))
        new_count = old_count + len(posts_to_add)
        html = re.sub(r'\d+\+? Real ChatGPT', f'{new_count}+ Real ChatGPT', html)
    
    # Save
    with open(stories_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Update added titles
    added_titles.update([p['title'] for p in posts_to_add])
    with open(added_titles_file, 'w', encoding='utf-8') as f:
        json.dump(list(added_titles), f, indent=2)
    
    print(f"  Added {len(posts_to_add)} new testimonials to stories.html!")
    return 0

if __name__ == "__main__":
    exit(main())
