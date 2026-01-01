"""
Finalize monetization by replacing placeholders with real links.
- Replace affiliate placeholder URLs with actual product links
- Update email capture forms
- Update consulting CTA to link to contact page
- Update report download link
"""

import os
import re
from pathlib import Path

REPO_DIR = r'C:\Users\Nima\chatgptdisaster'

# Affiliate link replacements (product links - can be converted to affiliate later)
AFFILIATE_REPLACEMENTS = {
    # AI alternatives
    'PLACEHOLDER-AFFILIATE-LINK.com/claude-enterprise': 'claude.ai/business',
    'PLACEHOLDER-AFFILIATE-LINK.com/ai-alternatives': 'chatgptdisaster.com/alternatives.html',
    'PLACEHOLDER-AFFILIATE-LINK.com/smart-ai': 'claude.ai',
    'PLACEHOLDER-AFFILIATE-LINK.com/enterprise-ai': 'claude.ai/business',
    'PLACEHOLDER-AFFILIATE-LINK.com/ai-comparison': 'chatgptdisaster.com/alternatives.html',
    'PLACEHOLDER-AFFILIATE-LINK.com/coding-assistant': 'cursor.com',

    # Tools
    'PLACEHOLDER-AFFILIATE-LINK.com/ai-content-checker': 'originality.ai',
    'PLACEHOLDER-AFFILIATE-LINK.com/ai-benchmark-tools': 'artificialanalysis.ai',

    # Mental health
    'PLACEHOLDER-AFFILIATE-LINK.com/online-therapy': 'betterhelp.com',

    # Legal resources
    'PLACEHOLDER-AFFILIATE-LINK.com/legal-ai-cases': 'chatgptdisaster.com/lawsuits.html',
}

# Form and CTA updates
FORM_REPLACEMENTS = {
    # Email capture - using Formspree pattern
    'action="https://PLACEHOLDER-EMAIL-SERVICE.com/subscribe"': 'action="https://formspree.io/f/chatgptdisaster" ',

    # Report link
    '<strong>"10 Real ChatGPT Failures That Cost Companies Money"</strong>': '<strong>"10 Real ChatGPT Failures That Cost Companies Money"</strong> (<a href="report.html" style="color: #ffc107;">read it here</a>)',
}

# Consulting CTA update
OLD_CONSULTING_CTA = '''<div class="consulting-cta">
<h4>Need Help Fixing AI Mistakes?</h4>
<p>We offer AI content audits, workflow failure analysis, and compliance reviews for organizations dealing with AI-generated content issues.</p>
<p><a href="mailto:consulting@chatgptdisaster.com">Contact us</a> for a confidential assessment.</p>
</div>'''

NEW_CONSULTING_CTA = '''<div class="consulting-cta">
<h4>Need Help Fixing AI Mistakes?</h4>
<p>We offer AI content audits, workflow failure analysis, and compliance reviews for organizations dealing with AI-generated content issues.</p>
<p><a href="contact.html">Request a consultation</a> for a confidential assessment.</p>
</div>'''

def update_file(filepath):
    """Update a single file with real links."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    original_content = content
    changes_made = []

    # Replace affiliate placeholders
    for placeholder, real_url in AFFILIATE_REPLACEMENTS.items():
        if placeholder in content:
            # Use https:// prefix for external links
            if not real_url.startswith('chatgptdisaster'):
                full_url = f'https://{real_url}'
            else:
                full_url = real_url.replace('chatgptdisaster.com/', '')
            content = content.replace(f'https://{placeholder}', full_url)
            changes_made.append(f'affiliate: {placeholder[:30]}...')

    # Replace form placeholders
    for old, new in FORM_REPLACEMENTS.items():
        if old in content:
            content = content.replace(old, new)
            changes_made.append('form update')

    # Update consulting CTA
    if OLD_CONSULTING_CTA in content:
        content = content.replace(OLD_CONSULTING_CTA, NEW_CONSULTING_CTA)
        changes_made.append('consulting CTA')

    # Also handle variations of the consulting CTA (with extra whitespace, etc.)
    if 'mailto:consulting@chatgptdisaster.com' in content:
        content = content.replace(
            'mailto:consulting@chatgptdisaster.com">Contact us</a>',
            'contact.html">Request a consultation</a>'
        )
        if 'mailto fix' not in changes_made:
            changes_made.append('mailto fix')

    # Save if changed
    if content != original_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {os.path.basename(filepath)} ({', '.join(changes_made)})")
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False

    return False

def process_all_files():
    """Process all HTML files."""
    updated_count = 0

    for root, dirs, files in os.walk(REPO_DIR):
        dirs[:] = [d for d in dirs if d not in ['.git', '.github', 'archive', 'scripts', '__pycache__']]
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if update_file(filepath):
                    updated_count += 1

    return updated_count

if __name__ == '__main__':
    print("Finalizing monetization links...")
    print("=" * 50)
    count = process_all_files()
    print("=" * 50)
    print(f"\nUpdated {count} files")
    print("\nNOTE: Formspree form ID is set to 'chatgptdisaster'")
    print("Create a Formspree account and update the form ID in the HTML files.")
