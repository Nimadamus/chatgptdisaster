"""
STORY COUNTER & INTEGRITY CHECKER
Run this before and after any changes to stories pages.
Saves a manifest so we can detect if stories are ever lost.
"""
import re
import os
import json
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(BASE, "scripts", "story_manifest.json")

FILES = ["stories.html"] + [f"stories-page{i}.html" for i in range(2, 13)]

def count_stories():
    counts = {}
    total = 0
    for fname in FILES:
        path = os.path.join(BASE, fname)
        if not os.path.exists(path):
            counts[fname] = 0
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        cards = len(re.findall(r'<article class="story-card"', content))
        divs = len(re.findall(r'<div class="story">', content))
        count = cards + divs
        counts[fname] = count
        total += count
    return counts, total

def load_manifest():
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r") as f:
            return json.load(f)
    return None

def save_manifest(counts, total):
    manifest = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": total,
        "pages": counts
    }
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)
    return manifest

if __name__ == "__main__":
    counts, total = count_stories()
    prev = load_manifest()

    print("=" * 50)
    print("  CHATGPT DISASTER - STORY COUNT")
    print("=" * 50)
    for fname in FILES:
        c = counts[fname]
        diff = ""
        if prev and fname in prev["pages"]:
            d = c - prev["pages"][fname]
            if d > 0:
                diff = f"  (+{d})"
            elif d < 0:
                diff = f"  (!!LOST {abs(d)}!!)"
        print(f"  {fname}: {c}{diff}")
    print("-" * 50)
    print(f"  TOTAL: {total}")

    if prev:
        d = total - prev["total"]
        if d > 0:
            print(f"  Change: +{d} since last check ({prev['date']})")
        elif d < 0:
            print(f"\n  !!!!! ALERT: LOST {abs(d)} STORIES SINCE {prev['date']} !!!!!")
            print(f"  Previous total was {prev['total']}, now {total}")
            print(f"  DO NOT PUSH UNTIL THIS IS FIXED")
            exit(1)
        else:
            print(f"  No change since last check ({prev['date']})")
    else:
        print("  (First run - no previous manifest)")

    save_manifest(counts, total)
    print(f"\n  Manifest saved. Run again after changes to verify.")
    print("=" * 50)
