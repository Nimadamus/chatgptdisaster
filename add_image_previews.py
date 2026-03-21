"""
Add image previews to all press-cards on chatgptdisaster.com homepage.
- Uses real og:image from article pages where available
- Creates CSS gradient previews with category icons for the rest
"""

import re
import os

SITE_DIR = r"C:\Users\Nima\chatgptdisaster"
INDEX_PATH = os.path.join(SITE_DIR, "index.html")

# Category -> emoji/icon mapping
CATEGORY_ICONS = {
    'breaking': '&#9888;',        # ⚠ warning
    'crisis': '&#128680;',        # 🚨 rotating light
    'investigation': '&#128269;', # 🔍 magnifying glass
    'report': '&#128203;',        # 📋 clipboard
    'analysis': '&#128202;',      # 📊 chart
    'mental health': '&#129504;', # 🧠 brain
    'healthcare': '&#127973;',    # 🏥 hospital
    'financial': '&#128200;',     # 📈 chart up
    'safety': '&#128737;',        # 🛡 shield
    'copyright': '&#169;',        # © copyright
    'security': '&#128274;',      # 🔒 lock
    'education': '&#127891;',     # 🎓 grad cap
    'legal': '&#9878;',           # ⚖ scales
    'whistleblower': '&#128227;', # 📣 megaphone
    'exodus': '&#128682;',        # 🚪 door
    'military': '&#127894;',      # 🎖 medal
    'default': '&#128308;',       # 🔴 red circle
}

# Category -> gradient colors
CATEGORY_GRADIENTS = {
    'breaking': ('rgba(239,68,68,0.4)', 'rgba(139,0,0,0.6)'),
    'crisis': ('rgba(239,68,68,0.4)', 'rgba(180,20,60,0.6)'),
    'investigation': ('rgba(139,92,246,0.4)', 'rgba(88,28,135,0.6)'),
    'report': ('rgba(239,68,68,0.35)', 'rgba(120,40,40,0.5)'),
    'analysis': ('rgba(59,130,246,0.35)', 'rgba(30,58,138,0.5)'),
    'mental health': ('rgba(239,68,68,0.4)', 'rgba(127,29,29,0.6)'),
    'healthcare': ('rgba(239,68,68,0.35)', 'rgba(153,27,27,0.5)'),
    'financial': ('rgba(249,115,22,0.4)', 'rgba(154,52,18,0.6)'),
    'safety': ('rgba(139,92,246,0.35)', 'rgba(76,29,149,0.5)'),
    'copyright': ('rgba(236,72,153,0.35)', 'rgba(131,24,67,0.5)'),
    'security': ('rgba(239,68,68,0.35)', 'rgba(127,29,29,0.5)'),
    'education': ('rgba(59,130,246,0.35)', 'rgba(29,78,216,0.5)'),
    'legal': ('rgba(234,179,8,0.35)', 'rgba(133,77,14,0.5)'),
    'whistleblower': ('rgba(239,68,68,0.4)', 'rgba(153,27,27,0.6)'),
    'exodus': ('rgba(249,115,22,0.35)', 'rgba(154,52,18,0.5)'),
    'military': ('rgba(34,197,94,0.3)', 'rgba(21,128,61,0.5)'),
    'default': ('rgba(139,92,246,0.3)', 'rgba(88,28,135,0.5)'),
}

DEFAULT_OG = "https://chatgptdisaster.com/images/og-default.png"

def get_og_image(article_filename):
    """Read article file and extract og:image if it's not the default."""
    filepath = os.path.join(SITE_DIR, article_filename)
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(5000)  # Only need the head section
        match = re.search(r'og:image.*?content="([^"]+)"', content)
        if match:
            img = match.group(1)
            if img != DEFAULT_OG and 'og-default' not in img:
                return img
    except:
        pass
    return None

def detect_category(source_text):
    """Detect category from the source/tag text."""
    lower = source_text.lower()
    for key in CATEGORY_ICONS:
        if key in lower:
            return key
    # Additional mappings
    if 'pentagon' in lower or 'military' in lower or 'defense' in lower:
        return 'military'
    if 'leak' in lower or 'breach' in lower or 'hack' in lower:
        return 'security'
    if 'law' in lower or 'sued' in lower or 'court' in lower or 'legal' in lower:
        return 'legal'
    if 'school' in lower or 'student' in lower or 'academic' in lower:
        return 'education'
    if 'safety' in lower or 'exodus' in lower:
        return 'safety'
    if 'money' in lower or 'stock' in lower or 'financial' in lower or 'crash' in lower:
        return 'financial'
    if 'health' in lower or 'medical' in lower or 'death' in lower or 'suicide' in lower:
        return 'crisis'
    if 'whistleblower' in lower:
        return 'whistleblower'
    return 'default'

def make_css_preview(category, source_text):
    """Create a CSS gradient preview div for cards without real images."""
    grad = CATEGORY_GRADIENTS.get(category, CATEGORY_GRADIENTS['default'])
    icon = CATEGORY_ICONS.get(category, CATEGORY_ICONS['default'])

    # Extract short label from source text
    label = source_text.strip()
    if '/' in label:
        label = label.split('/')[-1].strip()
    if len(label) > 30:
        label = label[:27] + '...'

    return (
        f'<div class="press-card-img-wrap" style="'
        f'background: linear-gradient(135deg, {grad[0]}, {grad[1]}); '
        f'display:flex; align-items:center; justify-content:center; height:140px; '
        f'position:relative;">'
        f'<span style="font-size:48px; opacity:0.7; filter:grayscale(20%);">{icon}</span>'
        f'</div>'
    )

def make_real_image_preview(img_url, alt_text="Article preview"):
    """Create an image preview div with a real image."""
    return (
        f'<div class="press-card-img-wrap">'
        f'<img src="{img_url}" alt="{alt_text}" loading="lazy">'
        f'</div>'
    )

def process_index():
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find all press-cards in the press-preview-grid
    # Pattern: <a href="..." class="press-card"...>...(optional img-wrap)...<p class="source"...>...</a>

    # We need to find press-cards that DON'T already have press-card-img-wrap
    # and add one after the opening <a> tag

    cards_updated = 0
    cards_already_have_img = 0
    cards_failed = 0

    # Find each press-card block
    # Pattern: <a href="file.html" class="press-card"...>
    card_pattern = re.compile(
        r'(<a\s+href="([^"]+\.html)"\s+class="press-card"[^>]*>)\s*\n'
        r'(\s*)((?:<div class="press-card-img-wrap">.*?</div>\s*)?)'
        r'(\s*<p class="source"[^>]*>([^<]*(?:<[^>]+>[^<]*)*)</p>)',
        re.DOTALL
    )

    def replace_card(match):
        nonlocal cards_updated, cards_already_have_img, cards_failed

        opening_tag = match.group(1)  # <a href="..." class="press-card"...>
        href = match.group(2)         # filename.html
        indent = match.group(3)       # whitespace indent
        existing_img = match.group(4) # existing img-wrap if any
        source_line = match.group(5)  # <p class="source"...>...</p>
        source_text = match.group(6)  # inner text of source

        # Skip if already has an image
        if existing_img and 'press-card-img-wrap' in existing_img:
            cards_already_have_img += 1
            return match.group(0)

        # Try to get real image from article
        real_img = get_og_image(href)

        # Clean source text of HTML tags for category detection
        clean_source = re.sub(r'<[^>]+>', '', source_text).strip()
        category = detect_category(clean_source)

        if real_img:
            preview_html = make_real_image_preview(real_img, f"Article: {clean_source}")
            cards_updated += 1
        else:
            preview_html = make_css_preview(category, clean_source)
            cards_updated += 1

        # Reconstruct the card with the image preview inserted
        return f'{opening_tag}\n{indent}    {preview_html}\n{source_line}'

    new_html = card_pattern.sub(replace_card, html)

    # If regex didn't catch everything, try a simpler approach
    if cards_updated + cards_already_have_img < 10:
        print(f"Regex approach only matched {cards_updated + cards_already_have_img} cards. Trying line-by-line approach...")
        cards_updated = 0
        cards_already_have_img = 0

        lines = html.split('\n')
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]

            # Check if this line opens a press-card
            card_match = re.search(r'<a\s+href="([^"]+\.html)"\s+class="press-card"', line)
            if card_match:
                href = card_match.group(1)
                new_lines.append(line)
                i += 1

                # Check if next non-empty line already has img-wrap
                next_content = ''
                lookahead = i
                while lookahead < len(lines) and lookahead < i + 3:
                    next_content += lines[lookahead]
                    lookahead += 1

                if 'press-card-img-wrap' in next_content:
                    cards_already_have_img += 1
                    # Don't modify, just continue
                    continue

                # Find the source line to detect category
                source_text = ''
                for j in range(i, min(i + 5, len(lines))):
                    src_match = re.search(r'<p class="source"[^>]*>(.*?)</p>', lines[j])
                    if src_match:
                        source_text = re.sub(r'<[^>]+>', '', src_match.group(1)).strip()
                        break

                # Get indent from next line
                if i < len(lines):
                    indent_match = re.match(r'^(\s+)', lines[i])
                    indent = indent_match.group(1) if indent_match else '                '
                else:
                    indent = '                '

                # Try real image
                real_img = get_og_image(href)
                category = detect_category(source_text)

                if real_img:
                    preview = make_real_image_preview(real_img, f"Article: {source_text}")
                else:
                    preview = make_css_preview(category, source_text)

                new_lines.append(f'{indent}{preview}')
                cards_updated += 1
            else:
                new_lines.append(line)
                i += 1

        new_html = '\n'.join(new_lines)

    # Write the updated file
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"\nResults:")
    print(f"  Cards updated with previews: {cards_updated}")
    print(f"  Cards already had images: {cards_already_have_img}")
    print(f"  Total: {cards_updated + cards_already_have_img}")

if __name__ == '__main__':
    process_index()
