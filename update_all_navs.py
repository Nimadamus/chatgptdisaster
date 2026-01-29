import os
import re
from pathlib import Path

# The new consistent navigation bar HTML (with Home link for non-homepage)
NEW_NAV = '''
<!-- Navigation -->
<nav class="main-nav">
    <div class="nav-container">
        <a href="index.html" class="nav-logo">
            <div class="nav-logo-text">ChatGPT <span>Review Hub</span></div>
        </a>

        <ul class="nav-menu">
            <li class="nav-item">
                <a href="index.html" class="nav-link">Home</a>
            </li>

            <li class="nav-item">
                <a href="#" class="nav-link">
                    Crisis Docs <span class="nav-dropdown-arrow">▼</span>
                </a>
                <div class="nav-dropdown">
                    <a href="mental-health-crisis.html" class="nav-dropdown-link">Mental Health Crisis</a>
                    <a href="clinical-cases.html" class="nav-dropdown-link">AI-Induced Psychosis</a>
                    <a href="victims.html" class="nav-dropdown-link">Victims Memorial</a>
                    <a href="chatgpt-death-lawsuits.html" class="nav-dropdown-link">8 Death Lawsuits</a>
                    <div class="nav-dropdown-divider"></div>
                    <a href="january-2026-crisis.html" class="nav-dropdown-link">January 2026 Crisis</a>
                    <a href="year-end-2025-meltdown.html" class="nav-dropdown-link">2025 Year-End Meltdown</a>
                    <a href="code-red-crisis-2025.html" class="nav-dropdown-link">Code Red Crisis 2025</a>
                </div>
            </li>

            <li class="nav-item">
                <a href="#" class="nav-link">
                    Performance <span class="nav-dropdown-arrow">▼</span>
                </a>
                <div class="nav-dropdown">
                    <a href="performance-decline.html" class="nav-dropdown-link">Performance Decline</a>
                    <a href="chatgpt-getting-dumber.html" class="nav-dropdown-link">ChatGPT Getting Dumber</a>
                    <a href="chatgpt-not-working.html" class="nav-dropdown-link">ChatGPT Not Working</a>
                    <a href="stealth-downgrades.html" class="nav-dropdown-link">Stealth Downgrades</a>
                    <div class="nav-dropdown-divider"></div>
                    <a href="gpt-5-bugs.html" class="nav-dropdown-link">GPT-5 Bugs</a>
                    <a href="gpt-52-user-backlash.html" class="nav-dropdown-link">GPT-5.2 Backlash</a>
                    <a href="silent-failure-ai-code.html" class="nav-dropdown-link">AI Code Silent Failures</a>
                </div>
            </li>

            <li class="nav-item">
                <a href="#" class="nav-link">
                    Outages <span class="nav-dropdown-arrow">▼</span>
                </a>
                <div class="nav-dropdown">
                    <a href="chatgpt-status-tracker.html" class="nav-dropdown-link" style="color: #ff4444; font-weight: 600;">Live Status Tracker</a>
                    <a href="what-to-do-chatgpt-down.html" class="nav-dropdown-link">ChatGPT Down? What To Do</a>
                    <div class="nav-dropdown-divider"></div>
                    <a href="chatgpt-outage-december-2025.html" class="nav-dropdown-link">December 2025 Outage</a>
                    <a href="december-2025-outages-recap.html" class="nav-dropdown-link">December 2025 Recap</a>
                    <a href="api-reliability-crisis.html" class="nav-dropdown-link">API Reliability Crisis</a>
                </div>
            </li>

            <li class="nav-item">
                <a href="stories.html" class="nav-link">User Stories</a>
            </li>

            <li class="nav-item">
                <a href="timeline.html" class="nav-link">Timeline</a>
            </li>

            <li class="nav-item">
                <a href="lawsuits.html" class="nav-link">Lawsuits</a>
            </li>

            <li class="nav-item">
                <a href="alternatives.html" class="nav-link">Alternatives</a>
            </li>
        </ul>

        <div class="nav-actions">
            <a href="petitions/" class="nav-cta">Sign Petitions</a>
        </div>
    </div>
</nav>
'''

# CSS to inject for the nav bar
NAV_CSS = '''
<style>
/* Navigation Styles */
.main-nav {
    background: rgba(0, 0, 0, 0.95);
    border-bottom: 1px solid rgba(255, 215, 0, 0.25);
    position: sticky;
    top: 0;
    z-index: 1000;
    backdrop-filter: blur(20px);
}
.nav-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 40px 0 0;
    max-width: 1600px;
    margin: 0 auto;
    height: 80px;
}
.nav-logo {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: #fff;
    flex-shrink: 0;
    padding-left: 20px;
}
.nav-logo-text {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.5rem;
    white-space: nowrap;
}
.nav-logo-text span {
    color: #ffd700;
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
}
.nav-menu {
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    gap: 0;
    list-style: none;
    flex: 1;
    margin: 0 40px;
    padding: 0;
}
.nav-item {
    position: relative;
    flex: 1;
    text-align: center;
}
.nav-link {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 20px 24px;
    color: #fff;
    text-decoration: none;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 17px;
    font-weight: 700;
    letter-spacing: 0.5px;
    border-radius: 0;
    transition: all 150ms ease;
    white-space: nowrap;
}
.nav-link:hover {
    color: #ffd700;
    background: rgba(255, 215, 0, 0.08);
}
.nav-dropdown-arrow {
    font-size: 10px;
    transition: transform 150ms ease;
}
.nav-item:hover .nav-dropdown-arrow {
    transform: rotate(180deg);
}
.nav-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    min-width: 240px;
    background: rgba(10, 10, 10, 0.98);
    border: 1px solid rgba(255, 215, 0, 0.25);
    border-top: 3px solid #ffd700;
    border-radius: 10px;
    box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.6);
    opacity: 0;
    visibility: hidden;
    transform: translateY(10px);
    transition: all 150ms ease;
    padding: 8px;
    z-index: 100;
}
.nav-item:hover .nav-dropdown {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}
.nav-dropdown-link {
    display: block;
    padding: 10px 14px;
    color: rgba(255, 255, 255, 0.75);
    text-decoration: none;
    font-size: 14px;
    border-radius: 6px;
    transition: all 150ms ease;
}
.nav-dropdown-link:hover {
    color: #ffd700;
    background: rgba(255, 215, 0, 0.1);
    padding-left: 20px;
}
.nav-dropdown-divider {
    height: 1px;
    background: rgba(255, 215, 0, 0.25);
    margin: 8px 0;
}
.nav-actions {
    display: flex;
    align-items: center;
    flex-shrink: 0;
    margin-left: auto;
    padding-right: 20px;
}
.nav-cta {
    padding: 14px 28px;
    background: #ffd700;
    color: #000;
    text-decoration: none;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 700;
    border-radius: 6px;
    transition: all 150ms ease;
    white-space: nowrap;
}
.nav-cta:hover {
    background: #ffea00;
    transform: translateY(-1px);
}
</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
'''

def update_html_file(filepath):
    """Update a single HTML file with the new navigation."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        original_content = content

        # Skip if it's the preview file or index.html
        filename = os.path.basename(filepath)
        if 'PREVIEW' in filename or filename == 'index.html':
            return False, "Skipped (preview or index)"

        # Check if file has basic HTML structure
        if '<html' not in content.lower():
            return False, "Not a valid HTML file"

        # Remove existing header/nav sections (various patterns)
        # Pattern 1: <header>...</header>
        content = re.sub(r'<header[^>]*>.*?</header>', '', content, flags=re.DOTALL | re.IGNORECASE)

        # Pattern 2: <!-- Navigation -->...<nav>...</nav>
        content = re.sub(r'<!--\s*Navigation\s*-->.*?</nav>', '', content, flags=re.DOTALL | re.IGNORECASE)

        # Pattern 3: <nav class="main-nav">...</nav>
        content = re.sub(r'<nav[^>]*class="[^"]*main-nav[^"]*"[^>]*>.*?</nav>', '', content, flags=re.DOTALL | re.IGNORECASE)

        # Pattern 4: Simple nav
        content = re.sub(r'<nav[^>]*>.*?</nav>', '', content, flags=re.DOTALL | re.IGNORECASE)

        # Add CSS before </head>
        if NAV_CSS not in content:
            content = content.replace('</head>', NAV_CSS + '\n</head>')

        # Add nav after <body> tag
        body_match = re.search(r'<body[^>]*>', content, re.IGNORECASE)
        if body_match:
            insert_pos = body_match.end()
            content = content[:insert_pos] + '\n' + NEW_NAV + '\n' + content[insert_pos:]

        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Updated"
        else:
            return False, "No changes needed"

    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    base_dir = Path('C:/Users/Nima/chatgptdisaster')

    # Find all HTML files
    html_files = list(base_dir.rglob('*.html'))

    updated = 0
    skipped = 0
    errors = 0

    print(f"Found {len(html_files)} HTML files")
    print("="*60)

    for filepath in html_files:
        success, message = update_html_file(filepath)
        rel_path = filepath.relative_to(base_dir)

        if success:
            print(f"[UPDATED] {rel_path}")
            updated += 1
        elif "Error" in message:
            print(f"[ERROR]   {rel_path}: {message}")
            errors += 1
        else:
            print(f"[SKIP]    {rel_path}: {message}")
            skipped += 1

    print("="*60)
    print(f"Updated: {updated}")
    print(f"Skipped: {skipped}")
    print(f"Errors:  {errors}")
    print("="*60)

if __name__ == '__main__':
    main()
