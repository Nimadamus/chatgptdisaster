"""
Add hub page links to all article pages on chatgptdisaster.com.
Inserts a "Browse by Topic" hub links section before the footer on every page
that doesn't already have one. This ensures every article has internal links
pointing to the 5 hub pages, which in turn link to all articles in that cluster.
"""
import os
import re
import sys

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HUB_LINKS_HTML = """
<!-- Hub Navigation - Internal Link Amplification -->
<section style="max-width:900px;margin:40px auto;padding:32px;background:rgba(255,215,0,0.03);border:2px solid rgba(255,215,0,0.25);border-radius:16px;font-family:'Inter','Segoe UI',sans-serif;">
    <h3 style="font-size:16px;font-weight:700;color:#ffd700;margin-bottom:20px;padding-bottom:12px;border-bottom:2px solid rgba(255,215,0,0.4);letter-spacing:1px;text-transform:uppercase;">Browse by Topic</h3>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:10px;">
        <a href="hub-ai-failures.html" style="display:block;padding:14px 18px;background:rgba(255,68,68,0.08);border:1px solid rgba(255,68,68,0.25);border-radius:10px;color:#ff6b6b;text-decoration:none;font-size:15px;font-weight:600;transition:all 0.3s;">AI Failures Hub</a>
        <a href="hub-chatgpt-problems.html" style="display:block;padding:14px 18px;background:rgba(255,149,0,0.08);border:1px solid rgba(255,149,0,0.25);border-radius:10px;color:#ff9500;text-decoration:none;font-size:15px;font-weight:600;transition:all 0.3s;">ChatGPT Problems Hub</a>
        <a href="hub-openai-lawsuits.html" style="display:block;padding:14px 18px;background:rgba(168,85,247,0.08);border:1px solid rgba(168,85,247,0.25);border-radius:10px;color:#a855f7;text-decoration:none;font-size:15px;font-weight:600;transition:all 0.3s;">OpenAI Lawsuits Hub</a>
        <a href="hub-ai-hallucinations.html" style="display:block;padding:14px 18px;background:rgba(0,212,255,0.08);border:1px solid rgba(0,212,255,0.25);border-radius:10px;color:#00d4ff;text-decoration:none;font-size:15px;font-weight:600;transition:all 0.3s;">AI Hallucinations Hub</a>
        <a href="hub-gpt-bugs.html" style="display:block;padding:14px 18px;background:rgba(0,204,136,0.08);border:1px solid rgba(0,204,136,0.25);border-radius:10px;color:#00cc88;text-decoration:none;font-size:15px;font-weight:600;transition:all 0.3s;">GPT Bugs & Issues Hub</a>
    </div>
    <p style="color:#888;font-size:13px;margin-top:16px;text-align:center;">Explore our complete documentation organized by topic</p>
</section>
"""

SKIP_FILES = {
    'index.html', 'sitemap.html', 'contact.html', 'report.html',
    'hub-ai-failures.html', 'hub-chatgpt-problems.html',
    'hub-openai-lawsuits.html', 'hub-ai-hallucinations.html',
    'hub-gpt-bugs.html'
}

MARKER = 'Hub Navigation - Internal Link Amplification'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Skip if already has hub links
    if MARKER in content:
        return False

    # Find insertion point - before </footer> or before </body>
    # Try before <footer first
    footer_match = re.search(r'<footer', content, re.IGNORECASE)
    if footer_match:
        insert_pos = footer_match.start()
        new_content = content[:insert_pos] + HUB_LINKS_HTML + '\n' + content[insert_pos:]
    else:
        # Try before </body>
        body_match = re.search(r'</body>', content, re.IGNORECASE)
        if body_match:
            insert_pos = body_match.start()
            new_content = content[:insert_pos] + HUB_LINKS_HTML + '\n' + content[insert_pos:]
        else:
            return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main():
    updated = 0
    skipped = 0

    # Process root HTML files
    for filename in sorted(os.listdir(SITE_DIR)):
        if not filename.endswith('.html'):
            continue
        if filename.startswith(('PREVIEW-', 'BG-', 'temp_', 'index-', 'index_')):
            continue
        if filename in SKIP_FILES:
            continue

        filepath = os.path.join(SITE_DIR, filename)
        if process_file(filepath):
            updated += 1
            print(f'  + {filename}')
        else:
            skipped += 1

    # Process subdirectory HTML files
    for subdir in ['articles', 'archive', 'failures', 'petitions']:
        subpath = os.path.join(SITE_DIR, subdir)
        if not os.path.isdir(subpath):
            continue
        for filename in sorted(os.listdir(subpath)):
            if not filename.endswith('.html'):
                continue
            if filename in SKIP_FILES:
                continue
            filepath = os.path.join(subpath, filename)
            if process_file(filepath):
                updated += 1
                print(f'  + {subdir}/{filename}')
            else:
                skipped += 1

    print(f'\nDone: {updated} files updated, {skipped} skipped (already had hub links)')

if __name__ == '__main__':
    main()
