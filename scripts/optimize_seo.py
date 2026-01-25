#!/usr/bin/env python3
"""
ChatGPT Disaster SEO Optimization Script
Adds OG images, JSON-LD schema, and internal linking to all pages
"""

import os
import re
from datetime import datetime
from pathlib import Path

REPO_DIR = Path(r'C:\Users\Nima\chatgptdisaster')
SITE_URL = 'https://chatgptdisaster.com'
OG_IMAGE_URL = f'{SITE_URL}/images/og-default.png'
LOGO_URL = f'{SITE_URL}/images/logo.png'

# Page categories for internal linking
CATEGORIES = {
    'performance': [
        'chatgpt-getting-dumber.html',
        'why-chatgpt-is-getting-worse.html',
        'is-chatgpt-getting-worse.html',
        'performance-decline.html',
        'stealth-downgrades.html',
        'gpt-5-bugs.html',
        'gpt-5-2-review.html',
        'gpt-52-user-backlash.html',
        'gpt-5-problems-2026.html',
        'gpt-5-complete-disaster-timeline.html',
        'ai-coding-quality-decline-2026.html',
        'ai-coding-productivity-paradox-2026.html',
    ],
    'outages': [
        'chatgpt-status-tracker.html',
        'chatgpt-live-checker.html',
        'chatgpt-down-january-2026.html',
        'chatgpt-not-working.html',
        'chatgpt-not-working-2026.html',
        'chatgpt-outage-december-2025.html',
        'december-2025-outages-recap.html',
        'code-red-crisis-2025.html',
        'january-2026-crisis.html',
        'api-reliability-crisis.html',
        'what-to-do-chatgpt-down.html',
    ],
    'safety': [
        'ai-ethics-crisis-2026.html',
        'chatgpt-addiction.html',
        'chatgpt-addiction-2026.html',
        'clinical-cases.html',
        'mental-health-crisis.html',
        'privacy-nightmare.html',
        'ai-misinformation-2026.html',
        'is-chatgpt-safe-2026.html',
        'chatgpt-security-risks-january-2026.html',
        'ai-brain-rot-research.html',
        'victims.html',
        'chatgpt-death-lawsuits.html',
        'ai-actress-suicide-pod-january-2026.html',
    ],
    'failures': [
        'business-failures.html',
        'financial-failures.html',
        'healthcare-failures.html',
        'education-failures.html',
        'enterprise-disaster.html',
        'developer-exodus.html',
        'silent-failure-ai-code.html',
        'replit-database-disaster.html',
        'bellingham-bid-rigging.html',
        'why-ai-hallucinations-happen.html',
        'why-chatbots-sound-confident.html',
        'model-collapse-ai-training.html',
    ],
    'legal': [
        'lawsuits.html',
        'chatgpt-death-lawsuits.html',
        'openai-lawsuit-2026.html',
        'openai-controversy-2026.html',
        'openai-internal-chaos.html',
        'eightfold-ai-hiring-lawsuit-2026.html',
        'character-ai-google-settlement-2026.html',
        'dublin-drops-x-grok-scandal-2026.html',
    ],
    'alternatives': [
        'alternatives.html',
        'chatgpt-alternatives-2026.html',
        'chatgpt-vs-claude-2026.html',
        'chatgpt-vs-gemini-2026.html',
        'how-to-cancel-chatgpt.html',
    ],
    'trends': [
        'ai-bubble-2026.html',
        'ai-layoffs-2026.html',
        'ai-replacing-jobs-2026.html',
        'year-end-2025-meltdown.html',
        'weekly-ai-failure-roundup-jan-15-2026.html',
        'weekly-ai-failure-roundup-jan-20-2026.html',
        'weekly-ai-failure-roundup-jan-24-2026.html',
        'strengths-and-limits-of-ai.html',
    ],
    'stories': [
        'stories.html',
        'stories-page2.html',
        'stories-page3.html',
        'stories-page4.html',
        'stories-page5.html',
        'stories-page6.html',
        'stories-page7.html',
        'stories-page8.html',
        'stories-page9.html',
        'stories-page10.html',
        'stories-page11.html',
        'reddit-testimonials.html',
        'submit-your-experience.html',
    ],
}

# Friendly category names for display
CATEGORY_NAMES = {
    'performance': 'Performance Issues',
    'outages': 'Outages & Status',
    'safety': 'Safety & Ethics',
    'failures': 'Failure Documentation',
    'legal': 'Legal & Lawsuits',
    'alternatives': 'Alternatives',
    'trends': 'AI Industry Trends',
    'stories': 'User Stories',
}

def get_page_category(filename):
    """Determine which category a page belongs to"""
    for category, pages in CATEGORIES.items():
        if filename in pages:
            return category
    return None

def get_related_pages(filename, max_links=5):
    """Get related pages from same category for internal linking"""
    category = get_page_category(filename)
    if not category:
        # Default to some high-value pages
        return [
            ('index.html', 'ChatGPT Disaster Home'),
            ('chatgpt-getting-dumber.html', 'Is ChatGPT Getting Dumber?'),
            ('alternatives.html', 'ChatGPT Alternatives'),
            ('stories.html', 'User Stories'),
            ('lawsuits.html', 'ChatGPT Lawsuits'),
        ]

    related = []
    for page in CATEGORIES[category]:
        if page != filename and os.path.exists(REPO_DIR / page):
            # Create a nice title from filename
            title = page.replace('.html', '').replace('-', ' ').title()
            related.append((page, title))
            if len(related) >= max_links:
                break

    # Add cross-category links if we don't have enough
    if len(related) < max_links:
        extras = [
            ('index.html', 'ChatGPT Disaster Home'),
            ('chatgpt-getting-dumber.html', 'Is ChatGPT Getting Dumber?'),
            ('alternatives.html', 'ChatGPT Alternatives'),
        ]
        for page, title in extras:
            if page != filename and (page, title) not in related:
                related.append((page, title))
                if len(related) >= max_links:
                    break

    return related

def extract_title(html):
    """Extract title from HTML"""
    match = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return 'ChatGPT Disaster'

def extract_description(html):
    """Extract meta description from HTML"""
    match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return 'Documentation of ChatGPT failures, problems, and user experiences.'

def has_og_image(html):
    """Check if page already has og:image"""
    return 'og:image' in html and 'content="https://' in html

def has_json_ld(html):
    """Check if page already has JSON-LD schema"""
    return 'application/ld+json' in html

def create_json_ld(filename, title, description):
    """Create JSON-LD schema for article"""
    now = datetime.now().isoformat()

    # Determine article type
    if 'stories' in filename:
        article_type = 'Article'
    elif any(x in filename for x in ['roundup', 'crisis', 'outage', '2026', '2025']):
        article_type = 'NewsArticle'
    else:
        article_type = 'Article'

    schema = {
        "@context": "https://schema.org",
        "@type": article_type,
        "headline": title[:110],  # Google truncates at 110
        "description": description[:160],
        "image": OG_IMAGE_URL,
        "author": {
            "@type": "Organization",
            "name": "ChatGPT Disaster Documentation Project"
        },
        "publisher": {
            "@type": "Organization",
            "name": "ChatGPT Disaster",
            "logo": {
                "@type": "ImageObject",
                "url": LOGO_URL
            }
        },
        "datePublished": now,
        "dateModified": now,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"{SITE_URL}/{filename}"
        }
    }

    import json
    return f'''<script type="application/ld+json">
{json.dumps(schema, indent=2)}
</script>'''

def create_internal_links_section(filename):
    """Create internal links HTML section"""
    related = get_related_pages(filename)
    category = get_page_category(filename)
    category_name = CATEGORY_NAMES.get(category, 'Related Content')

    links_html = f'''
<!-- Internal Links Section - Added by SEO Optimizer -->
<div class="related-articles" style="margin: 40px 0; padding: 25px; background: rgba(255, 68, 68, 0.1); border: 1px solid rgba(255, 68, 68, 0.3); border-radius: 10px;">
    <h3 style="color: #ff6b6b; margin-bottom: 15px; font-size: 1.2rem;">Related: {category_name}</h3>
    <ul style="list-style: none; padding: 0; margin: 0;">
'''
    for page, title in related:
        links_html += f'        <li style="margin: 8px 0;"><a href="{page}" style="color: #4fc3f7; text-decoration: none; transition: color 0.2s;">{title}</a></li>\n'

    links_html += '''    </ul>
</div>
<!-- End Internal Links Section -->
'''
    return links_html

def add_og_image_tags(html):
    """Add og:image and twitter:image tags"""
    # Check if already has og:image with actual URL
    if re.search(r'og:image.*content="https://', html):
        return html

    og_image_tag = f'<meta property="og:image" content="{OG_IMAGE_URL}">'
    twitter_image_tag = f'<meta name="twitter:image" content="{OG_IMAGE_URL}">'

    # Find where to insert (after existing og tags or twitter tags)
    if '<meta property="og:site_name"' in html:
        html = re.sub(
            r'(<meta property="og:site_name"[^>]+>)',
            r'\1\n' + og_image_tag,
            html
        )
    elif '<meta property="og:description"' in html:
        html = re.sub(
            r'(<meta property="og:description"[^>]+>)',
            r'\1\n' + og_image_tag,
            html
        )
    elif '<!-- Open Graph' in html:
        html = re.sub(
            r'(<!-- Open Graph[^>]*-->)',
            r'\1\n' + og_image_tag,
            html
        )
    else:
        # Insert before </head>
        html = html.replace('</head>', og_image_tag + '\n</head>')

    # Add twitter:image
    if 'twitter:image' not in html:
        if '<meta name="twitter:description"' in html:
            html = re.sub(
                r'(<meta name="twitter:description"[^>]+>)',
                r'\1\n' + twitter_image_tag,
                html
            )
        elif '<meta name="twitter:card"' in html:
            html = re.sub(
                r'(<meta name="twitter:card"[^>]+>)',
                r'\1\n' + twitter_image_tag,
                html
            )
        else:
            html = html.replace('</head>', twitter_image_tag + '\n</head>')

    return html

def add_json_ld_schema(html, filename, title, description):
    """Add JSON-LD schema if not present"""
    if has_json_ld(html):
        return html

    schema = create_json_ld(filename, title, description)

    # Insert before </head>
    html = html.replace('</head>', schema + '\n</head>')
    return html

def add_internal_links(html, filename):
    """Add internal links section before footer"""
    # Skip certain pages
    skip_pages = ['sitemap.html', 'contact.html', 'report.html', 'submit-your-experience.html']
    if filename in skip_pages:
        return html

    # Check if already has related-articles section
    if 'class="related-articles"' in html:
        return html

    links_section = create_internal_links_section(filename)

    # Try to insert before footer
    if '</main>' in html:
        html = html.replace('</main>', links_section + '</main>')
    elif '<footer' in html:
        html = re.sub(r'(<footer)', links_section + r'\1', html)
    else:
        # Insert before </body>
        html = html.replace('</body>', links_section + '</body>')

    return html

def process_file(filepath):
    """Process a single HTML file"""
    filename = os.path.basename(filepath)

    # Skip non-content pages
    skip_files = ['sitemap.html']
    if filename in skip_files:
        return False, 'Skipped (utility page)'

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()

        original = html
        title = extract_title(html)
        description = extract_description(html)

        # Add OG image
        html = add_og_image_tags(html)

        # Add JSON-LD schema
        html = add_json_ld_schema(html, filename, title, description)

        # Add internal links
        html = add_internal_links(html, filename)

        if html != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            return True, 'Updated'
        else:
            return False, 'No changes needed'

    except Exception as e:
        return False, f'Error: {str(e)}'

def main():
    """Main function to process all HTML files"""
    print("=" * 60)
    print("ChatGPT Disaster SEO Optimization")
    print("=" * 60)
    print()

    # Create images directory if needed
    images_dir = REPO_DIR / 'images'
    if not images_dir.exists():
        images_dir.mkdir()
        print(f"Created: {images_dir}")

    # Process all HTML files
    html_files = list(REPO_DIR.glob('*.html'))

    updated = 0
    skipped = 0
    errors = 0

    for filepath in sorted(html_files):
        filename = filepath.name
        success, message = process_file(filepath)

        if success:
            print(f"[UPDATED] {filename}")
            updated += 1
        elif 'Error' in message:
            print(f"[ERROR] {filename}: {message}")
            errors += 1
        else:
            print(f"[SKIP] {filename}: {message}")
            skipped += 1

    print()
    print("=" * 60)
    print(f"SUMMARY: {updated} updated, {skipped} skipped, {errors} errors")
    print("=" * 60)
    print()
    print("NEXT STEPS:")
    print("1. Create an OG image at: images/og-default.png (1200x630px)")
    print("2. Create a logo at: images/logo.png")
    print("3. Commit and push changes")

if __name__ == '__main__':
    main()
