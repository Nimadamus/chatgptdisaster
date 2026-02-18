#!/usr/bin/env python3
"""Sync all testimonial counts across chatgptdisaster.com pages."""

import re
import json
from pathlib import Path

SITE_DIR = Path(r"C:\Users\Nima\chatgptdisaster")
DATA_FILE = SITE_DIR / "scripts" / "content_data.json"


def get_count():
    """Read the current story count from content_data.json"""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("story_count", 0)


def update_file(filepath, replacements):
    """Apply regex replacements to a file. Returns True if changed."""
    content = filepath.read_text(encoding="utf-8")
    original = content
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    if content != original:
        filepath.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    count = get_count()
    print(f"[SYNC] Syncing all pages to {count}+ testimonials")

    # 1. stories.html - title, meta, OG, twitter, JSON-LD
    f = SITE_DIR / "stories.html"
    if f.exists():
        changed = update_file(f, [
            (r'\d+\+?\s*Real ChatGPT Horror Stories', f'{count}+ Real ChatGPT Horror Stories'),
            (r'Read \d+\+?\s*real user reports', f'Read {count}+ real user reports'),
            (r'"name":\s*"\d+\+?\s*Real ChatGPT User Horror Stories"',
             f'"name": "{count}+ Real ChatGPT User Horror Stories"'),
            (r'Read \d+\+?\s*real user stories', f'Read {count}+ real user stories'),
        ])
        print(f"  stories.html: {'UPDATED' if changed else 'already current'}")

    # 2. stories-pageN.html
    for i in range(2, 100):
        f = SITE_DIR / f"stories-page{i}.html"
        if not f.exists():
            break
        changed = update_file(f, [
            (r'<div class="number">\d+\+?</div>(\s*\n\s*<div class="label">Total Documented User Horror Stories)',
             f'<div class="number">{count}+</div>\\1'),
            (r'\d+\+?\s*Real ChatGPT Horror Stories', f'{count}+ Real ChatGPT Horror Stories'),
        ])
        if changed:
            print(f"  stories-page{i}.html: UPDATED")

    # 3. archive/index.html
    f = SITE_DIR / "archive" / "index.html"
    if f.exists():
        content = f.read_text(encoding="utf-8")
        original = content
        # Match the stat-number near "User Testimonials" or "Stories" label
        content = re.sub(
            r'(<div class="stat-number">)\d+\+?(</div>\s*\n\s*<div class="stat-label">User Testimonials)',
            rf'\g<1>{count}+\g<2>',
            content
        )
        if content != original:
            f.write_text(content, encoding="utf-8")
            print(f"  archive/index.html: UPDATED")
        else:
            print(f"  archive/index.html: already current")

    print(f"\n[DONE] All counts synced to {count}+")


if __name__ == "__main__":
    main()
