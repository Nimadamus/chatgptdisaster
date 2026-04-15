from __future__ import annotations

import datetime as dt
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SITE = "https://chatgptdisaster.com"
TODAY = dt.date.today().isoformat()

TRUST_LINKS = """
<section class="editorial-trust-panel" style="max-width:900px;margin:40px auto;padding:24px;background:rgba(255,255,255,0.045);border:1px solid rgba(255,255,255,0.14);border-radius:12px;color:inherit;">
  <h2 style="font-size:1.25rem;margin:0 0 12px;color:inherit;">Editorial Standards and Source Transparency</h2>
  <p style="margin:0 0 14px;line-height:1.6;">ChatGPT Disaster documents AI failures, lawsuits, research, outages, and user-reported harms. We separate primary sources, court filings, peer-reviewed research, mainstream reporting, company statements, and user-submitted accounts so readers can judge the strength of each claim.</p>
  <div style="display:flex;flex-wrap:wrap;gap:10px;">
    <a href="/trust-center.html" style="color:#4fc3f7;text-decoration:none;">Trust Center</a>
    <a href="/about.html" style="color:#4fc3f7;text-decoration:none;">About</a>
    <a href="/editorial-policy.html" style="color:#4fc3f7;text-decoration:none;">Editorial Policy</a>
    <a href="/source-methodology.html" style="color:#4fc3f7;text-decoration:none;">Source Methodology</a>
    <a href="/evidence-register.html" style="color:#4fc3f7;text-decoration:none;">Evidence Register</a>
    <a href="/corrections.html" style="color:#4fc3f7;text-decoration:none;">Corrections</a>
    <a href="/ai-disclosure.html" style="color:#4fc3f7;text-decoration:none;">AI Disclosure</a>
  </div>
</section>
""".strip()


POLICY_PAGES = {
    "trust-center.html": {
        "title": "Trust Center | ChatGPT Disaster",
        "description": "The ChatGPT Disaster trust center for editorial standards, source methodology, corrections, AI disclosure, evidence classification, and accountability policies.",
        "h1": "Trust Center",
        "body": """
<p>The Trust Center centralizes the policies that support factual accountability across ChatGPT Disaster. The site covers high-stakes AI topics, so readers need to know how claims are sourced, how user stories are handled, and how corrections are made.</p>
<h2>Trust Resources</h2>
<ul>
  <li><a href="/about.html">About ChatGPT Disaster</a> explains the site's purpose and independence.</li>
  <li><a href="/editorial-policy.html">Editorial Policy</a> explains sourcing, sensitive-topic standards, and independence.</li>
  <li><a href="/source-methodology.html">Source Methodology</a> ranks source strength and explains how evidence is classified.</li>
  <li><a href="/evidence-register.html">Evidence Register</a> provides the evidence labels used across the site.</li>
  <li><a href="/corrections.html">Corrections Policy</a> explains how readers can request factual updates or clarifications.</li>
  <li><a href="/ai-disclosure.html">AI Use Disclosure</a> explains how AI-assisted tools may be used and what humans remain responsible for.</li>
</ul>
<h2>Reader Standard</h2>
<p>For court cases, medical risks, mental health claims, safety failures, and financial harms, readers should prioritize primary documents and clearly sourced reporting over anonymous posts or viral screenshots. User stories are important evidence of patterns, but they should be treated as accounts unless independently documented.</p>
""",
    },
    "evidence-register.html": {
        "title": "Evidence Register | ChatGPT Disaster",
        "description": "Evidence labels and source-strength standards used by ChatGPT Disaster for AI lawsuits, studies, outages, user reports, company statements, and editorial analysis.",
        "h1": "Evidence Register",
        "body": """
<p>The Evidence Register defines the labels used to evaluate claims across ChatGPT Disaster. It is designed to make source strength visible instead of forcing readers to guess whether a claim comes from a filing, a study, a news report, a company statement, or a user account.</p>
<h2>Evidence Labels</h2>
<ul>
  <li><strong>Primary source:</strong> court filings, regulatory records, official company statements, status pages, public datasets, transcripts, and original documents.</li>
  <li><strong>Peer-reviewed research:</strong> published academic or clinical research, including journal articles and conference papers where methodology is available.</li>
  <li><strong>Institutional report:</strong> reports from universities, nonprofits, government agencies, safety organizations, or standards bodies.</li>
  <li><strong>Mainstream reporting:</strong> named reporting from established newsrooms, trade publications, or specialist outlets with editorial accountability.</li>
  <li><strong>Company statement:</strong> statements, blog posts, release notes, policy updates, status pages, or public comments from AI companies or their executives.</li>
  <li><strong>User-submitted account:</strong> direct submission, forum post, Reddit comment, social post, email, or interview account. These are treated as testimony unless corroborated.</li>
  <li><strong>Editorial analysis:</strong> conclusions, rankings, comparisons, or interpretations drawn from multiple sources.</li>
</ul>
<h2>High-Stakes Claim Standard</h2>
<p>Claims involving death, self-harm, psychiatric harm, medical advice, legal sanctions, financial loss, minors, private individuals, or criminal allegations should be tied to the strongest available source and updated when the public record changes.</p>
<h2>What This Does Not Mean</h2>
<p>A label is not a guarantee that a claim is final or undisputed. Lawsuits contain allegations. User reports contain personal accounts. Company statements can be incomplete. The label tells readers what kind of evidence is being used.</p>
""",
    },
    "about.html": {
        "title": "About ChatGPT Disaster | Independent AI Failure Documentation",
        "description": "About ChatGPT Disaster, an independent documentation project tracking AI failures, lawsuits, outages, research, user reports, and source-backed accountability coverage.",
        "h1": "About ChatGPT Disaster",
        "body": """
<p>ChatGPT Disaster is an independent documentation project focused on AI product failures, user harms, model reliability problems, legal claims, research findings, outages, and public accountability.</p>
<p>The site is not affiliated with OpenAI, Anthropic, Google, Microsoft, xAI, or any AI vendor. Product names and trademarks belong to their respective owners.</p>
<h2>What We Cover</h2>
<ul>
  <li>AI chatbot lawsuits, court filings, settlements, and regulatory actions.</li>
  <li>Documented hallucination cases in law, medicine, education, media, and business.</li>
  <li>AI service outages, reliability failures, product rollbacks, and degraded user workflows.</li>
  <li>User-submitted stories clearly distinguished from independently verified claims.</li>
  <li>Research, safety reports, and public statements from companies, regulators, journalists, and academics.</li>
</ul>
<h2>How To Read This Site</h2>
<p>High-stakes claims should be evaluated by source quality. A court filing, peer-reviewed study, or named institutional report carries more weight than a social media post or anonymous user report. We preserve strong user language when it is central to the story, but we aim to make the evidence trail visible.</p>
""",
    },
    "editorial-policy.html": {
        "title": "Editorial Policy | ChatGPT Disaster",
        "description": "The ChatGPT Disaster editorial policy for sourcing, verification, corrections, sensitive topics, user stories, AI-assisted production, and independence.",
        "h1": "Editorial Policy",
        "body": """
<p>Our editorial goal is to document AI failures aggressively while keeping the evidence trail clear. The site can have a point of view, but factual claims should be traceable to sources.</p>
<h2>Evidence Labels</h2>
<ul>
  <li><strong>Primary source:</strong> court filing, regulatory document, company statement, status page, research paper, dataset, transcript, or original document.</li>
  <li><strong>Mainstream reporting:</strong> established news organizations, trade publications, or specialist outlets with named authors and editorial accountability.</li>
  <li><strong>User-submitted:</strong> direct reader submissions, social media posts, forums, Reddit comments, or anonymous accounts. These are treated as testimony unless independently verified.</li>
  <li><strong>Editorial analysis:</strong> our interpretation of documented events, user reports, or product behavior.</li>
</ul>
<h2>Sensitive Claims</h2>
<p>Articles involving suicide, self-harm, mental health, medical advice, legal advice, financial loss, minors, or named private individuals require extra care. We avoid presenting allegations as proven facts unless they have been established by a court, regulator, company admission, or other authoritative source.</p>
<h2>Independence</h2>
<p>We do not represent OpenAI or any AI company. If affiliate links, sponsorships, consulting offers, or paid placements are ever used, they should be disclosed on the relevant page.</p>
""",
    },
    "source-methodology.html": {
        "title": "Source Methodology | ChatGPT Disaster",
        "description": "How ChatGPT Disaster classifies sources, evaluates evidence strength, handles user reports, and updates AI failure documentation.",
        "h1": "Source Methodology",
        "body": """
<p>Every claim should be judged by source strength. This page explains how we classify evidence across the site.</p>
<h2>Source Strength Ranking</h2>
<ol>
  <li><strong>Primary documents:</strong> court records, regulatory filings, research papers, company status pages, official statements, and original datasets.</li>
  <li><strong>Named institutional reporting:</strong> articles from recognized publications with clear authorship and editorial review.</li>
  <li><strong>Expert commentary:</strong> named researchers, attorneys, clinicians, engineers, or policy specialists speaking within their expertise.</li>
  <li><strong>User testimony:</strong> direct experiences from users, forums, Reddit, emails, or submissions. Useful for pattern detection but not treated as independently verified fact by itself.</li>
  <li><strong>Editorial inference:</strong> conclusions drawn from multiple sources. These should be signaled as analysis.</li>
</ol>
<h2>User Stories</h2>
<p>User stories are valuable because they show patterns and lived experience, but they can be incomplete, emotional, or disputed. We preserve them as accounts and avoid converting them into proven institutional facts unless independent documentation supports them.</p>
<h2>Updates</h2>
<p>AI products, lawsuits, and safety policies change quickly. Pages should be updated when new filings, research, status reports, or company statements materially change the record.</p>
""",
    },
    "corrections.html": {
        "title": "Corrections Policy | ChatGPT Disaster",
        "description": "How to request a correction, clarification, source update, privacy review, or right-of-reply for ChatGPT Disaster coverage.",
        "h1": "Corrections Policy",
        "body": """
<p>Accuracy matters, especially on topics involving health, safety, lawsuits, financial harm, and named people or companies. If something is wrong, incomplete, outdated, or missing context, request a correction.</p>
<h2>What To Send</h2>
<ul>
  <li>The URL of the page.</li>
  <li>The exact sentence or claim you believe needs correction.</li>
  <li>Supporting documentation, preferably a primary source.</li>
  <li>Whether you are requesting a factual correction, clarification, update, privacy review, or right-of-reply.</li>
</ul>
<h2>Correction Standard</h2>
<p>Material factual errors should be corrected directly on the page. Significant updates should preserve reader trust by noting what changed and when. Minor copy edits may be made silently when they do not alter the substance of the article.</p>
<p>Use the contact page to submit correction requests: <a href="/contact.html">contact ChatGPT Disaster</a>.</p>
""",
    },
    "ai-disclosure.html": {
        "title": "AI Use Disclosure | ChatGPT Disaster",
        "description": "Disclosure for AI-assisted drafting, editing, research organization, and human review standards on ChatGPT Disaster.",
        "h1": "AI Use Disclosure",
        "body": """
<p>ChatGPT Disaster covers AI systems and may use AI-assisted tools for drafting support, formatting, summarization, source organization, headline ideation, and technical maintenance.</p>
<h2>Human Responsibility</h2>
<p>AI assistance does not replace editorial responsibility. Claims involving lawsuits, medical issues, mental health, deaths, financial harm, or named people should be checked against source material before publication.</p>
<h2>What AI Should Not Decide</h2>
<ul>
  <li>Whether an allegation is true.</li>
  <li>Whether a medical, legal, or mental-health claim is established fact.</li>
  <li>Whether a private person should be named.</li>
  <li>Whether a source is sufficient for a high-stakes claim.</li>
</ul>
<p>AI may help organize the work. Humans remain responsible for publishing decisions, corrections, and context.</p>
""",
    },
}


LLMS_TXT = """# ChatGPT Disaster

ChatGPT Disaster is an independent documentation site covering AI failures, ChatGPT reliability issues, AI hallucinations, lawsuits, outages, mental-health and safety concerns, user reports, and alternatives.

Canonical site: https://chatgptdisaster.com/

## Trust and Editorial Pages
- About: https://chatgptdisaster.com/about.html
- Trust Center: https://chatgptdisaster.com/trust-center.html
- Editorial Policy: https://chatgptdisaster.com/editorial-policy.html
- Source Methodology: https://chatgptdisaster.com/source-methodology.html
- Evidence Register: https://chatgptdisaster.com/evidence-register.html
- Corrections: https://chatgptdisaster.com/corrections.html
- AI Disclosure: https://chatgptdisaster.com/ai-disclosure.html

## Core Hubs
- Documentation Index: https://chatgptdisaster.com/documentation-index.html
- OpenAI Lawsuits Hub: https://chatgptdisaster.com/hub-openai-lawsuits.html
- AI Hallucinations Hub: https://chatgptdisaster.com/hub-ai-hallucinations.html
- ChatGPT Problems Hub: https://chatgptdisaster.com/hub-chatgpt-problems.html
- AI Failures Hub: https://chatgptdisaster.com/hub-ai-failures.html

Use the trust pages to interpret source strength. User-submitted stories should be treated as personal accounts unless corroborated by primary documents, institutional reports, or named reporting.
"""


HUMANS_TXT = """/* TEAM */
Site: ChatGPT Disaster Documentation Project
URL: https://chatgptdisaster.com/
Contact: https://chatgptdisaster.com/contact.html

/* PURPOSE */
Independent documentation of AI failures, ChatGPT reliability problems, lawsuits, hallucinations, outages, safety concerns, user reports, and alternatives.

/* TRUST */
Trust Center: https://chatgptdisaster.com/trust-center.html
Editorial Policy: https://chatgptdisaster.com/editorial-policy.html
Source Methodology: https://chatgptdisaster.com/source-methodology.html
Corrections: https://chatgptdisaster.com/corrections.html

/* SITE */
Language: English
Standards: HTML, CSS, JSON-LD, robots.txt, sitemap.xml, llms.txt
"""


SECURITY_TXT = """Contact: https://chatgptdisaster.com/contact.html
Policy: https://chatgptdisaster.com/corrections.html
Preferred-Languages: en
Canonical: https://chatgptdisaster.com/.well-known/security.txt
"""


GITIGNORE = """# Local drafts and design concepts
_redesign-concepts-archive/

# Local runtime/cache files
*.log
*.tmp
__pycache__/
"""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def page_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{SITE}/"
    return f"{SITE}/{rel}"


def extract_title(text: str, fallback: str) -> str:
    match = re.search(r"<title>\s*(.*?)\s*</title>", text, flags=re.I | re.S)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    h1 = re.search(r"<h1[^>]*>\s*(.*?)\s*</h1>", text, flags=re.I | re.S)
    if h1:
        return re.sub(r"<[^>]+>", "", h1.group(1)).strip()
    return fallback


def extract_description(text: str) -> str:
    match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']\s*/?>', text, flags=re.I | re.S)
    if match:
        return html.unescape(match.group(1)).strip()
    return "Independent documentation of AI failures, ChatGPT reliability problems, lawsuits, research, outages, user reports, and source-backed accountability coverage."


def remove_duplicate_head_tags(head: str) -> str:
    singleton_patterns = [
        r'<link\s+rel=["\']canonical["\'][^>]*>\s*',
        r'<meta\s+property=["\']og:url["\'][^>]*>\s*',
        r'<meta\s+property=["\']og:site_name["\'][^>]*>\s*',
        r'<meta\s+name=["\']author["\'][^>]*>\s*',
        r'<meta\s+name=["\']robots["\'][^>]*>\s*',
        r'<meta\s+property=["\']article:author["\'][^>]*>\s*',
        r'<meta\s+property=["\']article:publisher["\'][^>]*>\s*',
    ]
    for pattern in singleton_patterns:
        head = re.sub(pattern, "", head, flags=re.I)
    return head


def ensure_head_metadata(text: str, path: Path) -> str:
    head_match = re.search(r"<head>(.*?)</head>", text, flags=re.I | re.S)
    if not head_match:
        return text

    head = remove_duplicate_head_tags(head_match.group(1))
    url = page_url(path)
    title = extract_title(text, path.stem.replace("-", " ").title())
    description = extract_description(text)
    escaped_url = html.escape(url, quote=True)
    json_title = json.dumps(title, ensure_ascii=False)
    json_description = json.dumps(description, ensure_ascii=False)
    json_url = json.dumps(url, ensure_ascii=False)

    additions = f"""
<meta name="author" content="ChatGPT Disaster Documentation Project">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{escaped_url}">
<meta property="og:url" content="{escaped_url}">
<meta property="og:site_name" content="ChatGPT Disaster">
<meta property="article:publisher" content="ChatGPT Disaster Documentation Project">
<script type="application/ld+json" data-trust-schema="true">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "ChatGPT Disaster Documentation Project",
  "url": "{SITE}/",
  "sameAs": [],
  "publishingPrinciples": "{SITE}/editorial-policy.html",
  "correctionsPolicy": "{SITE}/corrections.html",
  "ethicsPolicy": "{SITE}/source-methodology.html"
}}
</script>
<script type="application/ld+json" data-page-schema="true">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": {json_title},
  "description": {json_description},
  "url": {json_url},
  "isPartOf": {{
    "@type": "WebSite",
    "name": "ChatGPT Disaster",
    "url": "{SITE}/"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "ChatGPT Disaster Documentation Project"
  }}
}}
</script>
""".strip()

    # Remove prior script runs before reinserting.
    head = re.sub(r'\s*<script type="application/ld\+json" data-trust-schema="true">.*?</script>', "", head, flags=re.I | re.S)
    head = re.sub(r'\s*<script type="application/ld\+json" data-page-schema="true">.*?</script>', "", head, flags=re.I | re.S)

    if "</title>" in head.lower():
        head = re.sub(r"</title>", "</title>\n" + additions, head, count=1, flags=re.I)
    else:
        head = additions + "\n" + head

    return text[: head_match.start(1)] + head + text[head_match.end(1) :]


def add_trust_panel(text: str) -> str:
    if "editorial-trust-panel" in text:
        return text
    if re.search(r"</footer>", text, flags=re.I):
        return re.sub(r"<footer([^>]*)>", TRUST_LINKS + "\n\n<footer\\1>", text, count=1, flags=re.I)
    if re.search(r"</body>", text, flags=re.I):
        return re.sub(r"</body>", TRUST_LINKS + "\n\n</body>", text, count=1, flags=re.I)
    return text.rstrip() + "\n\n" + TRUST_LINKS + "\n"


def normalize_html(path: Path) -> None:
    text = read(path)
    original = text
    text = ensure_head_metadata(text, path)
    text = add_trust_panel(text)
    if text != original:
        write(path, text)


def policy_template(filename: str, data: dict[str, str]) -> str:
    url = f"{SITE}/{filename}"
    title = html.escape(data["title"], quote=True)
    desc = html.escape(data["description"], quote=True)
    h1 = html.escape(data["h1"])
    body = data["body"].strip()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="ChatGPT Disaster Documentation Project">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:site_name" content="ChatGPT Disaster">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<style>
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family: Inter, Segoe UI, Arial, sans-serif; background:#101322; color:#f4f5f7; line-height:1.7; }}
a {{ color:#67d5ff; }}
.wrap {{ max-width:900px; margin:0 auto; padding:32px 20px 56px; }}
header {{ padding:28px 0; border-bottom:1px solid rgba(255,255,255,.14); margin-bottom:32px; }}
.kicker {{ color:#ffcc66; text-transform:uppercase; letter-spacing:.08em; font-size:.82rem; font-weight:700; }}
h1 {{ font-size:clamp(2rem,5vw,3.5rem); line-height:1.05; margin:10px 0 14px; }}
h2 {{ margin-top:32px; color:#ffcc66; }}
p, li {{ color:#d9dde7; }}
.nav {{ display:flex; flex-wrap:wrap; gap:12px; margin-top:20px; }}
.nav a {{ text-decoration:none; border:1px solid rgba(103,213,255,.35); padding:8px 12px; border-radius:8px; }}
main {{ background:rgba(255,255,255,.035); border:1px solid rgba(255,255,255,.12); border-radius:14px; padding:28px; }}
footer {{ margin-top:32px; color:#aab1c3; font-size:.92rem; }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="kicker">Trust Center</div>
    <h1>{h1}</h1>
    <p>{desc}</p>
    <nav class="nav" aria-label="Trust navigation">
      <a href="/">Home</a>
      <a href="/about.html">About</a>
      <a href="/trust-center.html">Trust Center</a>
      <a href="/editorial-policy.html">Editorial Policy</a>
      <a href="/source-methodology.html">Source Methodology</a>
      <a href="/evidence-register.html">Evidence Register</a>
      <a href="/corrections.html">Corrections</a>
      <a href="/ai-disclosure.html">AI Disclosure</a>
    </nav>
  </header>
  <main>
    {body}
  </main>
  <footer>
    <p>ChatGPT Disaster Documentation Project. Independent site. Not affiliated with OpenAI.</p>
  </footer>
</div>
</body>
</html>
"""


def write_policy_pages() -> None:
    for filename, data in POLICY_PAGES.items():
        write(ROOT / filename, policy_template(filename, data))


def include_in_sitemap(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("_"):
        return False
    if rel.startswith("archive/"):
        return True
    excluded_names = {
        "index-backup-20260308.html",
        "index-redesign.html",
        "reddit-testimonials.html",
    }
    if path.name in excluded_names:
        return False
    return True


def should_normalize(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("_redesign-concepts-archive/"):
        return False
    if path.name in {"index-backup-20260308.html", "index-redesign.html", "reddit-testimonials.html"}:
        return False
    return True


def write_robots() -> None:
    write(
        ROOT / "robots.txt",
        """# Robots.txt for ChatGPT Disaster
User-agent: *
Allow: /

# Keep drafts, concept archives, and local maintenance files out of the index
# while allowing search and AI answer engines to crawl the public site.
Disallow: /_redesign-concepts-archive/
Disallow: /index-backup-20260308.html
Disallow: /index-redesign.html
Disallow: /*.py$
Disallow: /*.ps1$
Disallow: /*.bat$
Disallow: /*.log$
Disallow: /*.json$

Sitemap: https://chatgptdisaster.com/sitemap.xml

# AI-readable site guide:
# https://chatgptdisaster.com/llms.txt
""",
    )


def write_llms_txt() -> None:
    write(ROOT / "llms.txt", LLMS_TXT)


def write_humans_and_security() -> None:
    write(ROOT / "humans.txt", HUMANS_TXT)
    security_dir = ROOT / ".well-known"
    security_dir.mkdir(exist_ok=True)
    write(security_dir / "security.txt", SECURITY_TXT)


def write_gitignore() -> None:
    write(ROOT / ".gitignore", GITIGNORE)


def write_sitemap() -> None:
    urls = []
    for path in sorted(ROOT.rglob("*.html")):
        if not include_in_sitemap(path):
            continue
        lastmod = dt.date.fromtimestamp(path.stat().st_mtime).isoformat()
        loc = page_url(path)
        priority = "1.0" if path.name == "index.html" and path.parent == ROOT else "0.7"
        if path.name in POLICY_PAGES:
            priority = "0.5"
        urls.append((loc, lastmod, priority))

    body = "\n".join(
        f"""  <url>
    <loc>{html.escape(loc)}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
  </url>"""
        for loc, lastmod, priority in urls
    )
    write(
        ROOT / "sitemap.xml",
        f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
""",
    )


def write_apache_redirects() -> None:
    write(
        ROOT / ".htaccess",
        """RewriteEngine On

# Canonical host and HTTPS.
RewriteCond %{HTTPS} !=on [OR]
RewriteCond %{HTTP_HOST} ^www\\.chatgptdisaster\\.com$ [NC]
RewriteRule ^(.*)$ https://chatgptdisaster.com/$1 [R=301,L]

# Collapse /index.html to the root page.
RewriteRule ^index\\.html$ https://chatgptdisaster.com/ [R=301,L]

# Prevent directory listing.
Options -Indexes

<FilesMatch "\\.(html|htm)$">
  Header set Cache-Control "public, max-age=300"
</FilesMatch>
""",
    )


def main() -> None:
    write_policy_pages()
    write_llms_txt()
    write_humans_and_security()
    write_gitignore()
    for path in sorted(ROOT.rglob("*.html")):
        if not should_normalize(path):
            continue
        normalize_html(path)
    write_robots()
    write_sitemap()
    write_apache_redirects()


if __name__ == "__main__":
    main()
