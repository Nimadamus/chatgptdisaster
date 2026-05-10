"""
Story count safeguard for ChatGPTDisaster.com.

Run before and after changing stories.html or stories-pageN.html.
It counts rendered story cards from the current source files, syncs exact
archive count strings, and writes an audit report/manifest.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
MANIFEST_PATH = BASE / "scripts" / "story_manifest.json"
REPORT_PATH = BASE / "scripts" / "story_count_audit.md"
STORY_CARD_RE = re.compile(r'<article\s+class="story-card"')
COUNT_TEXT_RE = re.compile(r"1,099|1099|1,046|1046|1,064|1064|1,042|1042|1,060|1060|1,100|1100")


def story_pages() -> list[Path]:
    pages = [BASE / "stories.html"]
    pages.extend(
        sorted(
            BASE.glob("stories-page*.html"),
            key=lambda path: int(re.search(r"stories-page(\d+)\.html", path.name).group(1)),
        )
    )
    return [page for page in pages if page.exists()]


def count_cards(path: Path) -> int:
    return len(STORY_CARD_RE.findall(path.read_text(encoding="utf-8")))


def load_manifest() -> dict | None:
    if not MANIFEST_PATH.exists():
        return None
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def comma(n: int) -> str:
    return f"{n:,}"


def exact_count_locations(total: int) -> list[dict]:
    expected = comma(total)
    checks = []
    stories = BASE / "stories.html"
    html = stories.read_text(encoding="utf-8")

    patterns = {
        "title/meta/social/schema/hidden-h1 exact count": r"ChatGPT User Complaints Library 2026: ([\d,]+) Verified Reports",
        "visible documented experiences": r"Real stories from real users\. ([\d,]+) documented experiences\.",
        "footer archive count": r"User Stories Archive - ([\d,]+) Stories",
    }

    for label, pattern in patterns.items():
        values = sorted(set(re.findall(pattern, html)))
        checks.append(
            {
                "label": label,
                "values": values,
                "expected": expected,
                "ok": values == [expected],
            }
        )

    sitemap = BASE / "sitemap.xml"
    if sitemap.exists():
        sitemap_text = sitemap.read_text(encoding="utf-8")
        story_urls = re.findall(r"https://chatgptdisaster\.com/stories(?:-page\d+)?\.html", sitemap_text)
        checks.append(
            {
                "label": "sitemap story-page URL count",
                "values": [str(len(set(story_urls)))],
                "expected": str(len(story_pages())),
                "ok": len(set(story_urls)) == len(story_pages()),
            }
        )

    return checks


def sync_stories_html(total: int) -> bool:
    stories = BASE / "stories.html"
    html = stories.read_text(encoding="utf-8")
    updated = html
    count = comma(total)

    # Exact archive-count claims only. Leave unrelated approximate claims, such
    # as "1,000+ cases catalogued", untouched.
    updated = re.sub(
        r"ChatGPT User Complaints Library 2026: [\d,]+ Verified Reports",
        f"ChatGPT User Complaints Library 2026: {count} Verified Reports",
        updated,
    )
    updated = re.sub(
        r"[\d,]+ verified ChatGPT user complaints from 2025-2026",
        f"{count} verified ChatGPT user complaints from 2025-2026",
        updated,
    )
    updated = re.sub(
        r"Real stories from real users\. [\d,]+ documented experiences\.",
        f"Real stories from real users. {count} documented experiences.",
        updated,
    )
    updated = re.sub(
        r"User Stories Archive - [\d,]+ Stories",
        f"User Stories Archive - {count} Stories",
        updated,
    )

    if updated != html:
        stories.write_text(updated, encoding="utf-8", newline="")
        return True
    return False


def write_manifest(counts: dict[str, int], total: int, previous: dict | None) -> dict:
    previous_pages = set((previous or {}).get("pages", {}))
    current_pages = set(counts)
    manifest = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "selector": '<article\\s+class="story-card"',
        "total": total,
        "story_files_found": len(counts),
        "newly_added_story_files": sorted(current_pages - previous_pages),
        "removed_story_files": sorted(previous_pages - current_pages),
        "pages": counts,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def write_report(manifest: dict, previous: dict | None, checks: list[dict], synced: bool) -> None:
    prev_total = (previous or {}).get("total")
    delta = None if prev_total is None else manifest["total"] - prev_total
    lines = [
        "# Story Count Audit",
        "",
        f"- Date of last count update: {manifest['date']}",
        f"- Selector: `{manifest['selector']}`",
        f"- Total story files found: {manifest['story_files_found']}",
        f"- Total story cards found: {manifest['total']}",
        f"- Previous manifest total: {prev_total if prev_total is not None else 'none'}",
        f"- Change since previous manifest: {delta if delta is not None else 'n/a'}",
        f"- Newly added story files: {', '.join(manifest['newly_added_story_files']) or 'none'}",
        f"- Removed story files: {', '.join(manifest['removed_story_files']) or 'none'}",
        f"- stories.html count sync applied: {'yes' if synced else 'no'}",
        "",
        "## Per-File Counts",
        "",
    ]
    lines.extend(f"- {name}: {count}" for name, count in manifest["pages"].items())
    lines.extend(["", "## Count Consistency Checks", ""])
    for check in checks:
        status = "OK" if check["ok"] else "MISMATCH"
        lines.append(
            f"- {status}: {check['label']} values={check['values']} expected={check['expected']}"
        )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    accept_verified_baseline = "--accept-verified-baseline" in sys.argv
    pages = story_pages()
    counts = {page.name: count_cards(page) for page in pages}
    total = sum(counts.values())
    previous = load_manifest()

    if previous:
        previous_pages = set(previous.get("pages", {}))
        current_pages = set(counts)
        removed_files = previous_pages - current_pages
        previous_total = previous.get("total", 0)
        if total < previous_total and not removed_files and not accept_verified_baseline:
            print(f"ALERT: story count dropped from {previous_total} to {total}.")
            print("No story page files were removed. Refusing to update manifest.")
            print("If this is an audited correction to a bad old baseline, rerun with --accept-verified-baseline.")
            return 1

    synced = sync_stories_html(total)
    checks = exact_count_locations(total)
    manifest = write_manifest(counts, total, previous)
    checks = exact_count_locations(total)
    write_report(manifest, previous, checks, synced)

    print(f"Story cards: {total}")
    print(f"Story files: {len(counts)}")
    print(f"Manifest: {MANIFEST_PATH}")
    print(f"Report: {REPORT_PATH}")
    for check in checks:
        if not check["ok"]:
            print(f"MISMATCH: {check['label']} values={check['values']} expected={check['expected']}")
    return 0 if all(check["ok"] for check in checks) else 2


if __name__ == "__main__":
    raise SystemExit(main())
