"""
Add internal links between related articles for SEO.
Adds 1 related article link per page in the "See also" format.
"""

import os
import re
from pathlib import Path

REPO_DIR = r'C:\Users\Nima\chatgptdisaster'

# Define relationships between pages
RELATED_PAGES = {
    'business-failures.html': ('enterprise-disaster.html', 'enterprise disaster cases'),
    'enterprise-disaster.html': ('business-failures.html', 'more business failure stories'),
    'stealth-downgrades.html': ('chatgpt-getting-dumber.html', 'ChatGPT getting dumber'),
    'chatgpt-getting-dumber.html': ('performance-decline.html', 'performance decline data'),
    'mental-health-crisis.html': ('clinical-cases.html', 'documented clinical cases'),
    'clinical-cases.html': ('mental-health-crisis.html', 'the mental health crisis'),
    'developer-exodus.html': ('alternatives.html', 'alternatives developers are using'),
    'performance-decline.html': ('stealth-downgrades.html', 'stealth downgrade evidence'),
    'lawsuits.html': ('business-failures.html', 'business failure documentation'),
    'promises-vs-reality.html': ('performance-decline.html', 'performance decline data'),
    'victims.html': ('mental-health-crisis.html', 'the mental health crisis'),
    'timeline.html': ('stories.html', 'user stories'),
    'chatgpt-not-working.html': ('december-2025-outages-recap.html', 'December 2025 outages'),
    'chatgpt-outage-december-2025.html': ('enterprise-disaster.html', 'enterprise impact'),
    'december-2025-outages-recap.html': ('chatgpt-outage-december-2025.html', 'specific outage details'),
    'openai-internal-chaos.html': ('developer-exodus.html', 'developer exodus'),
    'year-end-2025-meltdown.html': ('december-2025-outages-recap.html', 'December outage details'),
    'gpt-5-bugs.html': ('performance-decline.html', 'performance decline trends'),
}

# "See Also" section HTML template
SEE_ALSO_TEMPLATE = '''
<div style="background: rgba(255, 255, 255, 0.03); border-left: 3px solid rgba(255, 68, 68, 0.4); padding: 15px 20px; margin: 30px 0; border-radius: 0 8px 8px 0;">
<p style="margin: 0; color: #aaa; font-size: 14px;"><strong style="color: #ff6b6b;">Related:</strong> {link_html}</p>
</div>
'''

def add_internal_link(filepath, target_page, anchor_text):
    """Add a 'See Also' link to a file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    # Check if link already exists
    if target_page in content and 'Related:' in content:
        print(f"Skipped (link exists): {filepath}")
        return False

    # Create the link HTML
    link_html = f'<a href="{target_page}" style="color: #ff6b6b; text-decoration: none;">Read more about {anchor_text} &rarr;</a>'
    see_also_html = SEE_ALSO_TEMPLATE.format(link_html=link_html)

    # Find insertion point - before email-capture-section or consulting-cta
    insertion_patterns = [
        r'<div class="email-capture-section">',
        r'<div class="consulting-cta">',
        r'</main>',
        r'<footer',
    ]

    inserted = False
    for pattern in insertion_patterns:
        match = re.search(pattern, content)
        if match:
            pos = match.start()
            content = content[:pos] + see_also_html + '\n' + content[pos:]
            inserted = True
            break

    if inserted:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added link: {os.path.basename(filepath)} -> {target_page}")
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False

    return False

def process_all_files():
    """Process all files that need internal links."""
    added_count = 0

    for filename, (target, anchor) in RELATED_PAGES.items():
        filepath = os.path.join(REPO_DIR, filename)
        if os.path.exists(filepath):
            if add_internal_link(filepath, target, anchor):
                added_count += 1
        else:
            print(f"File not found: {filepath}")

    return added_count

if __name__ == '__main__':
    print("Adding internal links for SEO...")
    print("=" * 50)
    count = process_all_files()
    print("=" * 50)
    print(f"\nAdded internal links to {count} pages")
