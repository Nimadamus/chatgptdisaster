"""
ChatGPT Disaster Monetization Script
Adds affiliate sections, email capture, and consulting CTA to all pages.
Safe, conservative approach - preserves existing content and SEO.
"""

import os
import re
from pathlib import Path

REPO_DIR = r'C:\Users\Nima\chatgptdisaster'

# CSS for monetization components (inserted once per page)
MONETIZATION_CSS = '''
/* Monetization Styles */
.affiliate-recommendation {
    background: linear-gradient(145deg, rgba(76, 175, 80, 0.12), rgba(76, 175, 80, 0.05));
    border: 1px solid rgba(76, 175, 80, 0.3);
    border-left: 4px solid #4CAF50;
    border-radius: 0 10px 10px 0;
    padding: 20px 25px;
    margin: 30px 0;
}

.affiliate-recommendation p {
    color: #c8c8c8;
    font-size: 15px;
    line-height: 1.7;
    margin: 0;
}

.affiliate-recommendation a {
    color: #4CAF50;
    text-decoration: none;
    font-weight: 600;
}

.affiliate-recommendation a:hover {
    color: #66BB6A;
    text-decoration: underline;
}

.email-capture-section {
    background: linear-gradient(145deg, rgba(255, 193, 7, 0.1), rgba(255, 193, 7, 0.05));
    border: 1px solid rgba(255, 193, 7, 0.3);
    border-radius: 12px;
    padding: 30px;
    margin: 40px 0;
    text-align: center;
}

.email-capture-section h3 {
    color: #ffc107;
    font-size: 1.4rem;
    margin-bottom: 10px;
}

.email-capture-section p {
    color: #bbb;
    font-size: 15px;
    margin-bottom: 20px;
}

.email-capture-section input[type="email"] {
    padding: 12px 20px;
    border: 1px solid rgba(255, 193, 7, 0.3);
    border-radius: 25px;
    background: rgba(0, 0, 0, 0.3);
    color: #fff;
    font-size: 15px;
    width: 280px;
    max-width: 100%;
    margin-right: 10px;
}

.email-capture-section input[type="email"]::placeholder {
    color: #888;
}

.email-capture-section button {
    padding: 12px 25px;
    background: linear-gradient(145deg, #ffc107, #ff9800);
    border: none;
    border-radius: 25px;
    color: #000;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
}

.email-capture-section button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255, 193, 7, 0.3);
}

.consulting-cta {
    background: rgba(255, 255, 255, 0.03);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding: 30px;
    margin-top: 40px;
    text-align: center;
}

.consulting-cta h4 {
    color: #888;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
    font-weight: 500;
}

.consulting-cta p {
    color: #aaa;
    font-size: 14px;
    margin-bottom: 15px;
}

.consulting-cta a {
    color: #ff6b6b;
    text-decoration: none;
}

.consulting-cta a:hover {
    color: #ff8888;
    text-decoration: underline;
}

@media (max-width: 600px) {
    .email-capture-section input[type="email"] {
        width: 100%;
        margin-right: 0;
        margin-bottom: 10px;
    }
    .email-capture-section button {
        width: 100%;
    }
}
'''

# Affiliate recommendations by page topic
AFFILIATE_SECTIONS = {
    'business-failures': '''
<div class="affiliate-recommendation">
<p>If AI hallucinations have cost your business money, you're not alone. Consider using <a href="https://PLACEHOLDER-AFFILIATE-LINK.com/ai-content-checker" target="_blank" rel="noopener">AI content verification tools</a> to catch errors before they reach clients. These tools cross-reference AI outputs against reliable sources - something ChatGPT should do but doesn't.</p>
</div>
''',
    'enterprise-disaster': '''
<div class="affiliate-recommendation">
<p>Enterprise teams burned by ChatGPT are switching to more reliable alternatives. <a href="https://PLACEHOLDER-AFFILIATE-LINK.com/claude-enterprise" target="_blank" rel="noopener">Claude for Business</a> offers better uptime guarantees and doesn't secretly route you to inferior models during peak hours.</p>
</div>
''',
    'stealth-downgrades': '''
<div class="affiliate-recommendation">
<p>Want to know exactly which model you're getting? <a href="https://PLACEHOLDER-AFFILIATE-LINK.com/ai-benchmark-tools" target="_blank" rel="noopener">AI benchmarking tools</a> can help you detect when your AI provider is silently downgrading your service. Knowledge is power when dealing with opaque AI vendors.</p>
</div>
''',
    'mental-health-crisis': '''
<div class="affiliate-recommendation">
<p>If you or someone you know is experiencing distress related to AI interactions, professional support is available. <a href="https://PLACEHOLDER-AFFILIATE-LINK.com/online-therapy" target="_blank" rel="noopener">Licensed online therapists</a> can help you process these experiences and develop healthier digital boundaries.</p>
</div>
''',
    'developer-exodus': '''
<div class="affiliate-recommendation">
<p>Developers leaving ChatGPT are finding better options. <a href="https://PLACEHOLDER-AFFILIATE-LINK.com/coding-assistant" target="_blank" rel="noopener">Specialized coding assistants</a> offer more reliable code generation without the sudden quality drops that plague ChatGPT's API.</p>
</div>
''',
    'alternatives': '''
<div class="affiliate-recommendation">
<p>Ready to make the switch? Many alternatives offer free trials so you can experience the difference yourself. <a href="https://PLACEHOLDER-AFFILIATE-LINK.com/ai-comparison" target="_blank" rel="noopener">Compare AI platforms side-by-side</a> to find the best fit for your needs.</p>
</div>
''',
    'performance-decline': '''
<div class="affiliate-recommendation">
<p>If you need consistent AI performance for critical work, consider platforms with transparent quality metrics. <a href="https://PLACEHOLDER-AFFILIATE-LINK.com/enterprise-ai" target="_blank" rel="noopener">Enterprise-grade AI services</a> offer SLAs and accountability that OpenAI refuses to provide.</p>
</div>
''',
    'lawsuits': '''
<div class="affiliate-recommendation">
<p>If you've suffered damages from AI failures, documenting your experience is crucial. <a href="https://PLACEHOLDER-AFFILIATE-LINK.com/legal-ai-cases" target="_blank" rel="noopener">AI litigation resources</a> can help you understand your options and connect with attorneys handling similar cases.</p>
</div>
''',
    'chatgpt-getting-dumber': '''
<div class="affiliate-recommendation">
<p>Frustrated by ChatGPT's declining intelligence? Users are finding better results with alternatives that haven't been dumbed down. <a href="https://PLACEHOLDER-AFFILIATE-LINK.com/smart-ai" target="_blank" rel="noopener">Compare AI reasoning capabilities</a> to find a model that still works as advertised.</p>
</div>
''',
    'default': '''
<div class="affiliate-recommendation">
<p>Considering alternatives to ChatGPT? <a href="https://PLACEHOLDER-AFFILIATE-LINK.com/ai-alternatives" target="_blank" rel="noopener">Compare top AI assistants</a> to find options that prioritize reliability, privacy, and honest performance over hype.</p>
</div>
'''
}

# Email capture section
EMAIL_CAPTURE = '''
<div class="email-capture-section">
<h3>Get the Full Report</h3>
<p>Download our free PDF: <strong>"10 Real ChatGPT Failures That Cost Companies Money"</strong> - with prevention strategies.</p>
<form id="email-capture-form" action="https://PLACEHOLDER-EMAIL-SERVICE.com/subscribe" method="POST">
<input type="email" name="email" placeholder="Enter your email" required>
<button type="submit">Get Free Report</button>
</form>
<p style="font-size: 12px; color: #666; margin-top: 15px;">No spam. Unsubscribe anytime.</p>
</div>
'''

# Consulting CTA
CONSULTING_CTA = '''
<div class="consulting-cta">
<h4>Need Help Fixing AI Mistakes?</h4>
<p>We offer AI content audits, workflow failure analysis, and compliance reviews for organizations dealing with AI-generated content issues.</p>
<p><a href="mailto:consulting@chatgptdisaster.com">Contact us</a> for a confidential assessment.</p>
</div>
'''

def get_affiliate_section(filename):
    """Get the appropriate affiliate section for a page based on its name."""
    base_name = Path(filename).stem.lower()
    for key in AFFILIATE_SECTIONS:
        if key in base_name:
            return AFFILIATE_SECTIONS[key]
    return AFFILIATE_SECTIONS['default']

def has_monetization(content):
    """Check if page already has monetization elements."""
    return 'affiliate-recommendation' in content or 'email-capture-section' in content or 'consulting-cta' in content

def add_css_to_page(content):
    """Add monetization CSS before </style> tag."""
    if 'affiliate-recommendation' in content:
        return content  # Already has CSS

    # Find the closing style tag
    style_close = content.rfind('</style>')
    if style_close == -1:
        return content

    # Insert CSS before </style>
    new_content = content[:style_close] + MONETIZATION_CSS + content[style_close:]
    return new_content

def find_affiliate_insertion_point(content):
    """Find a good place to insert affiliate section - after a problem/case study."""
    # Look for patterns indicating a problem has been described
    patterns = [
        (r'</div>\s*<h2>', '</div>'),  # After a case study div, before h2
        (r'</blockquote>\s*<p>', '</blockquote>'),  # After a blockquote
        (r'</div>\s*<h3>', '</div>'),  # After a div, before h3
        (r'<h2>[^<]*Hidden Cost', '<h2>'),  # Before "Hidden Costs" sections
        (r'<h2>[^<]*What (You Can|to) Do', '<h2>'),  # Before "What to Do" sections
        (r'<h2>[^<]*Bottom Line', '<h2>'),  # Before "Bottom Line" sections
    ]

    for pattern, marker in patterns:
        match = re.search(pattern, content)
        if match:
            # Find position after the marker
            pos = match.start() + len(marker)
            return pos

    return None

def add_monetization_to_file(filepath):
    """Add monetization elements to a single HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    # Skip if already has monetization
    if has_monetization(content):
        print(f"Skipped (already monetized): {filepath}")
        return False

    # Skip non-content pages
    filename = os.path.basename(filepath)
    skip_pages = ['sitemap.html', 'sitemap.xml', 'robots.txt']
    if filename in skip_pages:
        print(f"Skipped (non-content): {filepath}")
        return False

    original_content = content

    # 1. Add CSS
    content = add_css_to_page(content)

    # 2. Add affiliate section (find good insertion point)
    affiliate_pos = find_affiliate_insertion_point(content)
    affiliate_section = get_affiliate_section(filename)

    if affiliate_pos:
        content = content[:affiliate_pos] + '\n' + affiliate_section + '\n' + content[affiliate_pos:]

    # 3. Add email capture before footer or at end of main
    # Look for </main> or <footer
    email_insert_patterns = [
        (r'</main>', '</main>'),
        (r'<footer', '<footer'),
        (r'<a[^>]*class="back-link"[^>]*>[^<]*</a>\s*</main>', 'back-link'),
    ]

    email_inserted = False
    for pattern, marker in email_insert_patterns:
        match = re.search(pattern, content)
        if match:
            pos = match.start()
            content = content[:pos] + '\n' + EMAIL_CAPTURE + '\n' + content[pos:]
            email_inserted = True
            break

    # 4. Add consulting CTA before </footer> or </body>
    consulting_patterns = [
        (r'<footer', '<footer'),
        (r'</body>', '</body>'),
    ]

    for pattern, marker in consulting_patterns:
        match = re.search(pattern, content)
        if match:
            pos = match.start()
            # Don't add if already in the recently added content
            if 'consulting-cta' not in content[pos-500:pos]:
                content = content[:pos] + '\n' + CONSULTING_CTA + '\n' + content[pos:]
            break

    # Only write if content changed
    if content != original_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False

    return False

def add_internal_links(filepath):
    """Add 1 internal link per article to a related page."""
    related_pages = {
        'business-failures.html': ('enterprise-disaster.html', 'enterprise disaster stories'),
        'enterprise-disaster.html': ('business-failures.html', 'more business failure cases'),
        'stealth-downgrades.html': ('chatgpt-getting-dumber.html', 'evidence of ChatGPT getting dumber'),
        'chatgpt-getting-dumber.html': ('performance-decline.html', 'performance decline data'),
        'mental-health-crisis.html': ('clinical-cases.html', 'documented clinical cases'),
        'clinical-cases.html': ('mental-health-crisis.html', 'the broader mental health crisis'),
        'developer-exodus.html': ('alternatives.html', 'alternatives developers are choosing'),
        'performance-decline.html': ('stealth-downgrades.html', 'evidence of stealth downgrades'),
        'lawsuits.html': ('business-failures.html', 'business failure stories'),
    }

    filename = os.path.basename(filepath)
    if filename not in related_pages:
        return False

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return False

    related_page, anchor_text = related_pages[filename]
    link_html = f'<a href="{related_page}">{anchor_text}</a>'

    # Check if link already exists
    if related_page in content:
        return False

    # Find a good place to add the link (in a paragraph near the end)
    # Look for the last substantial paragraph before footer
    pattern = r'(<p>[^<]{100,}</p>)\s*(?:<div class="(?:email-capture|consulting)|</main>|<footer)'
    match = re.search(pattern, content)

    if match:
        paragraph = match.group(1)
        # Add link suggestion at end of paragraph
        new_paragraph = paragraph.replace('</p>', f' See also: {link_html}.</p>')
        content = content.replace(paragraph, new_paragraph)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added internal link: {filepath} -> {related_page}")
            return True
        except:
            return False

    return False

def process_all_files():
    """Process all HTML files in the repository."""
    updated_count = 0

    # Get all HTML files
    html_files = []
    for root, dirs, files in os.walk(REPO_DIR):
        # Skip .git directory
        dirs[:] = [d for d in dirs if d not in ['.git', '.github', 'archive', 'scripts']]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    print(f"Found {len(html_files)} HTML files to process")
    print("=" * 50)

    # Process each file
    for filepath in html_files:
        if add_monetization_to_file(filepath):
            updated_count += 1

    print("=" * 50)
    print(f"\nMonetization added to {updated_count} files")

    # Add internal links
    print("\nAdding internal links...")
    links_added = 0
    for filepath in html_files:
        if add_internal_links(filepath):
            links_added += 1

    print(f"Internal links added to {links_added} files")

    return updated_count

if __name__ == '__main__':
    print("ChatGPT Disaster Monetization Script")
    print("=" * 50)
    updated = process_all_files()
    print("\nDone!")
    print("\nNOTE: Affiliate links are placeholders (PLACEHOLDER-AFFILIATE-LINK.com)")
    print("Replace with actual affiliate URLs when programs are selected.")
