from __future__ import annotations

import datetime as dt
import html
import json
import posixpath
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
    <a href="/affiliate-disclosure.html" style="color:#4fc3f7;text-decoration:none;">Affiliate Disclosure</a>
    <a href="/newsletter.html" style="color:#4fc3f7;text-decoration:none;">Newsletter</a>
    <a href="/support.html" style="color:#4fc3f7;text-decoration:none;">Support</a>
  </div>
</section>
""".strip()


MONETIZATION_PANELS = {
    "index.html": {
        "heading": "Get the Weekly AI Failure Briefing",
        "body": "Track lawsuits, hallucinations, outages, safety failures, and model-quality decline without sorting through scattered feeds.",
        "primary": ("Join the briefing", "/newsletter.html"),
        "secondary": ("Support the archive", "/support.html"),
    },
    "documentation-index.html": {
        "heading": "Turn the Archive Into a Weekly Briefing",
        "body": "Get the most important AI failure cases, source updates, and accountability links in one digest.",
        "primary": ("Join the briefing", "/newsletter.html"),
        "secondary": ("View topic clusters", "/topic-clusters.html"),
    },
    "lawsuits.html": {
        "heading": "Follow the AI Lawsuit Tracker",
        "body": "Get updates when new filings, settlements, regulatory actions, or court outcomes change the record.",
        "primary": ("Join the briefing", "/newsletter.html"),
        "secondary": ("Get the report", "/ai-failure-report-2026.html"),
    },
    "mental-health-crisis.html": {
        "heading": "Track AI Safety and Mental-Health Updates",
        "body": "Receive source-backed updates on lawsuits, research, policy changes, and safety claims.",
        "primary": ("Join the briefing", "/newsletter.html"),
        "secondary": ("Support independent documentation", "/support.html"),
    },
    "chatgpt-alternatives-2026.html": {
        "heading": "Need Safer AI Tool Choices?",
        "body": "Use the comparison guide with source-handling, reliability, privacy, and workflow risk in mind.",
        "primary": ("Read the disclosure", "/affiliate-disclosure.html"),
        "secondary": ("Get the report", "/ai-failure-report-2026.html"),
    },
    "stories.html": {
        "heading": "Help Document AI Failure Patterns",
        "body": "Submit an experience, support the archive, or follow updates as more reports are categorized.",
        "primary": ("Submit your experience", "/submit-your-experience.html"),
        "secondary": ("Support the archive", "/support.html"),
    },
    "performance-decline.html": {
        "heading": "Track Model Quality Decline",
        "body": "Get updates on benchmarks, user reports, outages, model changes, and reproducible AI quality tests.",
        "primary": ("Join the briefing", "/newsletter.html"),
        "secondary": ("Get the report", "/ai-failure-report-2026.html"),
    },
}


EVIDENCE_PANELS = {
    "lawsuits.html": {
        "heading": "Evidence Quality Summary",
        "intro": "This legal hub should be read as a tracker of allegations, filings, settlements, and reported legal actions. Lawsuits are not proof of liability unless a court, settlement, or admission establishes the outcome.",
        "items": [
            ("Primary sources", "Court filings, case captions, docket entries, regulatory complaints, and settlement documents carry the most weight."),
            ("Reported sources", "Named reporting from legal, technology, and mainstream publications is used to summarize procedural history and public claims."),
            ("Status standard", "Case counts and outcomes should be updated when filings, rulings, dismissals, settlements, or appeals change the record."),
        ],
    },
    "mental-health-crisis.html": {
        "heading": "Sensitive-Topic Evidence Standard",
        "intro": "Mental-health and self-harm coverage is high-stakes. Treat user accounts as reports, not diagnoses, unless supported by clinical records, court filings, official statements, or named reporting.",
        "items": [
            ("Clinical caution", "This page does not provide medical advice, diagnosis, or emergency guidance."),
            ("Source priority", "Primary documents, institutional research, regulator complaints, and named reporting should be prioritized over anonymous posts."),
            ("Reader safety", "If someone may be at immediate risk, contact local emergency services or a qualified crisis-support resource."),
        ],
    },
    "documentation-index.html": {
        "heading": "How This Index Is Organized",
        "intro": "This index is the central crawl and reader map for ChatGPT Disaster. It groups content by evidence type, topic cluster, and user intent so readers and search engines can understand the site structure.",
        "items": [
            ("Core hubs", "Failure, hallucination, lawsuit, ChatGPT problem, and GPT bug hubs act as primary topic clusters."),
            ("Trust pages", "The Trust Center, Evidence Register, Editorial Policy, and Source Methodology explain how claims should be interpreted."),
            ("Legacy routes", "Bridge pages preserve old links and point readers to the strongest current destination."),
        ],
    },
    "chatgpt-alternatives-2026.html": {
        "heading": "Comparison Methodology",
        "intro": "Alternative rankings should be read as editorial analysis based on use case fit, reliability, pricing, source handling, and user workflow needs.",
        "items": [
            ("Best for research", "Prioritize tools that cite sources, expose retrieval context, and make verification easier."),
            ("Best for writing", "Prioritize controllability, long-form coherence, revision quality, and tone control."),
            ("Best for coding", "Prioritize repository context, testability, code explanation, and low-friction integration with developer workflows."),
        ],
    },
    "stories.html": {
        "heading": "User Story Verification Standard",
        "intro": "User stories are valuable evidence of patterns and lived experience, but they are not automatically independent verification of every factual claim inside an account.",
        "items": [
            ("User-submitted", "Personal reports are treated as accounts unless corroborated by documents or named reporting."),
            ("Pattern evidence", "Repeated reports can show recurring product issues even when individual stories remain unverified."),
            ("Corrections", "Readers can request removals, corrections, clarifications, or right-of-reply through the Corrections page."),
        ],
    },
    "performance-decline.html": {
        "heading": "Performance Evidence Standard",
        "intro": "Performance-decline claims should distinguish reproducible benchmarks, user reports, company release notes, and editorial testing.",
        "items": [
            ("Benchmarks", "Repeatable prompts, dated outputs, and documented methodology are stronger than one-off anecdotes."),
            ("User reports", "Community complaints are useful for pattern detection, but they need context and corroboration."),
            ("Product changes", "Release notes, model routing changes, outages, and moderation changes can affect perceived quality."),
        ],
    },
}


FAQ_PANELS = {
    "lawsuits.html": [
        ("What lawsuits are covered on ChatGPT Disaster?", "The lawsuits hub tracks public legal actions, regulatory complaints, settlements, and reported claims involving ChatGPT, OpenAI, and related AI systems."),
        ("Does a lawsuit mean OpenAI has been found liable?", "No. A lawsuit is an allegation unless a court ruling, settlement, regulator action, or company admission establishes an outcome."),
        ("What sources should readers prioritize for legal claims?", "Court filings, docket records, regulator documents, settlement papers, and named legal reporting should carry more weight than anonymous commentary."),
        ("How often should lawsuit pages be updated?", "Legal pages should be updated when new filings, dismissals, settlements, rulings, appeals, or regulator actions materially change the public record."),
    ],
    "mental-health-crisis.html": [
        ("Is this page medical advice?", "No. The mental-health crisis page is documentation and analysis, not medical advice, diagnosis, treatment guidance, or emergency support."),
        ("How are self-harm and psychiatric-harm claims evaluated?", "The strongest evidence comes from court filings, clinical records, institutional research, regulator documents, company statements, and named reporting."),
        ("Are user stories treated as verified medical facts?", "No. User stories are treated as personal accounts unless they are corroborated by documents, named reporting, clinical records, or legal filings."),
        ("What should someone do in an immediate crisis?", "If someone may be at immediate risk, contact local emergency services or a qualified crisis-support resource in their country."),
    ],
    "documentation-index.html": [
        ("What is the documentation index?", "The documentation index is the central map of ChatGPT Disaster pages, including lawsuits, hallucinations, failures, outages, safety concerns, user stories, and alternatives."),
        ("Which pages are the main topic hubs?", "The main hubs include AI failures, ChatGPT problems, OpenAI lawsuits, AI hallucinations, GPT bugs, user stories, and the trust center."),
        ("Why does the site use hub pages?", "Hub pages help readers and search engines understand how individual incidents connect to larger recurring AI failure patterns."),
        ("How should readers evaluate claims across the site?", "Readers should use the Evidence Register, Source Methodology, Editorial Policy, and Corrections pages to understand source strength and update standards."),
    ],
    "chatgpt-alternatives-2026.html": [
        ("What is the best ChatGPT alternative for research?", "Tools that cite sources, expose retrieval context, and make verification easier are usually stronger for research workflows."),
        ("What is the best ChatGPT alternative for writing?", "The best writing alternative depends on long-form coherence, revision quality, tone control, file handling, and how much factual verification the user needs."),
        ("What is the best ChatGPT alternative for coding?", "The best coding alternative depends on repository context, test integration, code explanation quality, and whether the tool fits the developer workflow."),
        ("Should users rely on one AI tool for everything?", "No. High-stakes work should use multiple tools, source checking, domain expertise, and human review instead of relying on one chatbot."),
    ],
    "stories.html": [
        ("Are all user stories independently verified?", "No. User stories are treated as accounts unless they are corroborated by primary documents, institutional records, or named reporting."),
        ("Why publish user stories if they are not all independently verified?", "Repeated user reports can show recurring patterns, product pain points, and failure modes that deserve investigation and documentation."),
        ("Can someone request a correction or removal?", "Yes. Readers can use the Corrections page to request corrections, clarifications, removals, privacy review, or right-of-reply."),
        ("How should readers interpret anonymous stories?", "Anonymous stories should be read as personal testimony and pattern evidence, not as final proof of every factual claim inside the account."),
    ],
    "performance-decline.html": [
        ("Is ChatGPT getting worse?", "Some users and researchers have reported degraded outputs, but performance claims should distinguish benchmarks, dated examples, model changes, outages, and anecdotes."),
        ("What is the strongest evidence for performance decline?", "Repeatable benchmarks, dated outputs, transparent methodology, release notes, and reproducible comparisons are stronger than one-off complaints."),
        ("Can product changes affect perceived quality?", "Yes. Model routing, system prompts, moderation changes, outages, context limits, and UI changes can all affect perceived quality."),
        ("How should users test AI quality?", "Users should keep dated prompts, save outputs, compare across tools, rerun tests, and document model or product changes when possible."),
    ],
}


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
        "kicker": "Trust Center",
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
    "affiliate-disclosure.html": {
        "title": "Affiliate Disclosure | ChatGPT Disaster",
        "description": "Affiliate, sponsorship, advertising, and monetization disclosure for ChatGPT Disaster, including how editorial independence is protected.",
        "h1": "Affiliate Disclosure",
        "kicker": "Disclosure",
        "body": """
<p>ChatGPT Disaster may earn revenue from affiliate links, sponsorships, paid reports, reader support, newsletter products, or advertising. This page explains how monetization should be handled without confusing readers about editorial judgment.</p>
<h2>Affiliate Links</h2>
<p>Some pages may link to products, services, tools, books, reports, or subscriptions. If a reader buys through an affiliate link, ChatGPT Disaster may earn a commission at no extra cost to the reader.</p>
<h2>Editorial Independence</h2>
<p>Affiliate or sponsor relationships should not determine whether a claim is true, whether a tool is recommended, or whether an AI company is criticized. Rankings and recommendations should remain editorial and should consider reliability, safety, source transparency, privacy, workflow fit, and reader risk.</p>
<h2>Sponsored Placements</h2>
<p>Sponsored placements, if used, should be labeled clearly. Sponsors do not receive control over legal, medical, mental-health, safety, or accountability coverage.</p>
<h2>Advertising</h2>
<p>Display advertising may appear on the site in the future. Ads should not be interpreted as endorsements unless a page explicitly says a product is recommended.</p>
<h2>Reader Standard</h2>
<p>Before buying any product mentioned on this site, readers should evaluate the vendor, pricing, privacy policy, refund terms, data practices, and whether the tool is appropriate for their use case.</p>
""",
    },
    "newsletter.html": {
        "title": "Weekly AI Failure Briefing | ChatGPT Disaster",
        "description": "Join the Weekly AI Failure Briefing for source-backed updates on AI lawsuits, hallucinations, outages, safety failures, model decline, and accountability research.",
        "h1": "Weekly AI Failure Briefing",
        "kicker": "Newsletter",
        "body": """
<p>The Weekly AI Failure Briefing is the email layer for ChatGPT Disaster: a concise digest of lawsuits, hallucinations, outages, mental-health and safety concerns, model-quality decline, research, and user-report patterns.</p>
<h2>What Readers Get</h2>
<ul>
  <li>New lawsuit, regulator, and court-document updates.</li>
  <li>AI hallucination cases in law, medicine, education, media, and business.</li>
  <li>Outage, downgrade, model-quality, and reliability tracking.</li>
  <li>New user-story patterns and corrections to the public archive.</li>
  <li>Links to the strongest source material added that week.</li>
</ul>
<h2>Launch Status</h2>
<p>The briefing is being prepared as the site finishes its crawl and trust rebuild. Use the contact page to request early access, sponsorship information, or report availability.</p>
<p><a href="/contact.html">Request newsletter access</a></p>
<h2>Future Paid Tier</h2>
<p>A paid tier may include monthly PDF reports, lawsuit tracker updates, source spreadsheets, and deeper analysis for journalists, educators, legal teams, risk teams, and researchers.</p>
""",
    },
    "support.html": {
        "title": "Support Independent AI Accountability Documentation | ChatGPT Disaster",
        "description": "Support ChatGPT Disaster's independent documentation of AI failures, lawsuits, hallucinations, outages, safety issues, user reports, and source-backed accountability work.",
        "h1": "Support Independent AI Accountability Documentation",
        "kicker": "Support",
        "body": """
<p>ChatGPT Disaster is an independent documentation project. Reader support helps preserve, organize, and update source-backed coverage of AI failures, lawsuits, hallucinations, outages, safety issues, and user reports.</p>
<h2>What Support Funds</h2>
<ul>
  <li>Maintaining the public archive and sitemap.</li>
  <li>Tracking legal, research, product, and policy updates.</li>
  <li>Improving evidence labels, source methodology, and correction workflows.</li>
  <li>Preparing public reports and briefings for readers who need a faster way to understand AI risk patterns.</li>
</ul>
<h2>Current Support Options</h2>
<p>Payment links are not active yet. Use the contact page for sponsorship, donation, report, or partnership inquiries while the public support flow is being configured.</p>
<p><a href="/contact.html">Contact the project</a></p>
<h2>Trust Standard</h2>
<p>Reader support does not buy editorial control, source placement, favorable coverage, or removal of documented criticism.</p>
""",
    },
    "ai-failure-report-2026.html": {
        "title": "2026 AI Failure Report | ChatGPT Disaster",
        "description": "A planned ChatGPT Disaster report covering AI lawsuits, hallucinations, outages, mental-health risks, model decline, user stories, and accountability evidence from 2026.",
        "h1": "2026 AI Failure Report",
        "kicker": "Report",
        "body": """
<p>The 2026 AI Failure Report is the planned paid research product for ChatGPT Disaster. It will package the site's public archive into a cleaner, source-forward format for readers who need a faster briefing.</p>
<h2>Planned Sections</h2>
<ul>
  <li>OpenAI and chatbot lawsuit tracker.</li>
  <li>AI hallucination casebook across law, medicine, education, media, and business.</li>
  <li>ChatGPT outage, downgrade, and model-quality decline timeline.</li>
  <li>Mental-health and safety documentation with source-strength labels.</li>
  <li>User-report pattern analysis and evidence caveats.</li>
  <li>Enterprise, school, parent, journalist, and researcher risk checklists.</li>
</ul>
<h2>Who It Is For</h2>
<p>The report is intended for journalists, attorneys, educators, researchers, parents, enterprise risk teams, creators, and policy readers who need an organized map of AI failure evidence.</p>
<h2>Availability</h2>
<p>The report is in preparation. Use the contact page to request early access, bulk access, sponsorship information, or a notification when the report is released.</p>
<p><a href="/contact.html">Request report access</a></p>
<h2>Disclosure</h2>
<p>Paid products should not change the public evidence standard. High-stakes claims still need source labels, corrections, and clear distinction between allegations, user accounts, reporting, and established facts.</p>
""",
    },
    "topic-clusters.html": {
        "title": "AI Failure Topic Clusters | ChatGPT Disaster",
        "description": "Topical authority map for ChatGPT Disaster covering AI lawsuits, hallucinations, ChatGPT failures, outages, mental-health risks, user stories, alternatives, and trust resources.",
        "h1": "AI Failure Topic Clusters",
        "kicker": "Topic Map",
        "body": """
<p>This page maps the core topic clusters on ChatGPT Disaster. It is built for readers who want the fastest path from a broad AI failure topic to the strongest supporting pages.</p>
<h2>Core Ranking Hubs</h2>
<ul>
  <li><a href="/documentation-index.html">Documentation Index</a> - complete site map for AI failures, ChatGPT problems, lawsuits, user reports, and research.</li>
  <li><a href="/hub-ai-failures.html">AI Failures Hub</a> - central coverage of AI failures across law, medicine, media, education, business, and software.</li>
  <li><a href="/hub-chatgpt-problems.html">ChatGPT Problems Hub</a> - reliability, quality, outage, downgrade, and user-experience failures.</li>
  <li><a href="/hub-openai-lawsuits.html">OpenAI Lawsuits Hub</a> - legal actions, complaints, settlements, and court-related documentation.</li>
  <li><a href="/hub-ai-hallucinations.html">AI Hallucinations Hub</a> - fake citations, fabricated cases, false medical claims, and reliability research.</li>
  <li><a href="/hub-gpt-bugs.html">GPT Bugs Hub</a> - GPT-5 issues, regressions, launch failures, and model quality complaints.</li>
</ul>
<h2>High-Intent Reader Paths</h2>
<ul>
  <li><a href="/lawsuits.html">ChatGPT Lawsuits</a> - legal claims, evidence standards, and lawsuit status tracking.</li>
  <li><a href="/mental-health-crisis.html">ChatGPT Mental Health Crisis</a> - sensitive-topic documentation, crisis-risk claims, and safety concerns.</li>
  <li><a href="/performance-decline.html">ChatGPT Performance Decline</a> - quality degradation, benchmark evidence, and user-reported decline.</li>
  <li><a href="/stories.html">ChatGPT User Stories</a> - user reports, complaints, and recurring product-harm patterns.</li>
  <li><a href="/chatgpt-alternatives-2026.html">ChatGPT Alternatives</a> - safer or more reliable options by workflow.</li>
  <li><a href="/chatgpt-not-working.html">ChatGPT Not Working</a> - outage and troubleshooting coverage.</li>
</ul>
<h2>Trust and Source Evaluation</h2>
<ul>
  <li><a href="/trust-center.html">Trust Center</a> - standards and accountability policies.</li>
  <li><a href="/evidence-register.html">Evidence Register</a> - source labels and evidence-strength definitions.</li>
  <li><a href="/source-methodology.html">Source Methodology</a> - how claims are classified and evaluated.</li>
  <li><a href="/editorial-policy.html">Editorial Policy</a> - source handling, corrections, sensitive-topic standards, and independence.</li>
</ul>
<h2>How To Use This Map</h2>
<p>Start with a hub page when researching a broad topic. Use individual articles for incidents, timelines, studies, court filings, or user reports. Use the trust pages to judge whether a claim is based on a primary source, reporting, user testimony, or editorial analysis.</p>
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
- Topic Clusters: https://chatgptdisaster.com/topic-clusters.html
- Affiliate Disclosure: https://chatgptdisaster.com/affiliate-disclosure.html
- Newsletter: https://chatgptdisaster.com/newsletter.html
- Support: https://chatgptdisaster.com/support.html
- 2026 AI Failure Report: https://chatgptdisaster.com/ai-failure-report-2026.html

## Core Hubs
- Documentation Index: https://chatgptdisaster.com/documentation-index.html
- Topic Clusters: https://chatgptdisaster.com/topic-clusters.html
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


ROOT_PAGES = {
    "index.html",
    "stories.html",
    "timeline.html",
    "lawsuits.html",
    "alternatives.html",
    "mental-health-crisis.html",
    "clinical-cases.html",
    "victims.html",
    "chatgpt-death-lawsuits.html",
    "january-2026-crisis.html",
    "year-end-2025-meltdown.html",
    "code-red-crisis-2025.html",
    "performance-decline.html",
    "chatgpt-getting-dumber.html",
    "chatgpt-not-working.html",
    "stealth-downgrades.html",
    "gpt-5-bugs.html",
    "gpt-52-user-backlash.html",
    "silent-failure-ai-code.html",
    "chatgpt-status-tracker.html",
    "what-to-do-chatgpt-down.html",
    "chatgpt-outage-december-2025.html",
    "december-2025-outages-recap.html",
    "api-reliability-crisis.html",
    "hub-ai-failures.html",
    "hub-chatgpt-problems.html",
    "hub-openai-lawsuits.html",
    "hub-ai-hallucinations.html",
    "hub-gpt-bugs.html",
    "resources.html",
    "documentation-index.html",
    "topic-clusters.html",
    "newsletter.html",
    "support.html",
    "affiliate-disclosure.html",
    "ai-failure-report-2026.html",
}


ALIAS_PAGES = {
    "blog.html": {
        "target": "/documentation-index.html",
        "title": "ChatGPT Disaster Blog and Documentation Index",
        "description": "Browse ChatGPT Disaster articles, evidence pages, issue hubs, user reports, legal coverage, and AI failure documentation.",
        "h1": "ChatGPT Disaster Blog and Documentation Index",
    },
    "testimonials.html": {
        "target": "/stories.html",
        "title": "ChatGPT User Testimonials and Stories",
        "description": "Read user-submitted ChatGPT experiences, reliability complaints, safety concerns, and documented user stories.",
        "h1": "ChatGPT User Testimonials and Stories",
    },
    "articles.html": {
        "target": "/documentation-index.html",
        "title": "ChatGPT Disaster Articles",
        "description": "Browse ChatGPT Disaster articles on AI failures, hallucinations, lawsuits, outages, reliability problems, and alternatives.",
        "h1": "ChatGPT Disaster Articles",
    },
    "articles/index.html": {
        "target": "/documentation-index.html",
        "title": "ChatGPT Disaster Articles Archive",
        "description": "Article archive for ChatGPT Disaster coverage of AI failures, lawsuits, hallucinations, outages, and product reliability problems.",
        "h1": "ChatGPT Disaster Articles Archive",
    },
    "blog/index.html": {
        "target": "/documentation-index.html",
        "title": "ChatGPT Disaster Blog Archive",
        "description": "Blog archive for ChatGPT Disaster investigations, AI failure coverage, lawsuits, product issues, and user reports.",
        "h1": "ChatGPT Disaster Blog Archive",
    },
    "ai-hallucinations-getting-worse-2026.html": {
        "target": "/hub-ai-hallucinations.html",
        "title": "Are AI Hallucinations Getting Worse in 2026?",
        "description": "A hub for AI hallucination evidence, legal cases, research, examples, and ChatGPT reliability problems in 2026.",
        "h1": "Are AI Hallucinations Getting Worse in 2026?",
    },
    "chatgpt-failure-archive.html": {
        "target": "/documentation-index.html",
        "title": "ChatGPT Failure Archive",
        "description": "Archive of documented ChatGPT failures, outages, hallucinations, lawsuits, safety concerns, and user reports.",
        "h1": "ChatGPT Failure Archive",
    },
    "ai-security-risks-2026.html": {
        "target": "/chatgpt-security-risks-january-2026.html",
        "title": "AI Security Risks in 2026",
        "description": "Security-risk coverage for ChatGPT and AI systems, including privacy, agent security, data exposure, and reliability failures.",
        "h1": "AI Security Risks in 2026",
    },
}


TITLE_OVERRIDES = {
    "0303-ai-chatbot-sexualized-student-book-report.html": "AI Chatbot Sexualized Student Book Report: Early Coverage",
}


DESCRIPTION_OVERRIDES = {
    "0303-ai-chatbot-sexualized-student-book-report.html": "Early ChatGPT Disaster coverage of the California school AI chatbot book report incident and the safety concerns it raised for students and classrooms.",
    "reddit-testimonials.html": "Legacy redirect page for Reddit testimonial coverage now consolidated into the ChatGPT Disaster user stories archive.",
    "articles/openclaw-ai-chaos-2026-02-03.html": "Archived article coverage of OpenClaw and AI agent security concerns, preserved as part of the ChatGPT Disaster article archive.",
}


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
    fallback_key = fallback
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
        r'<meta\s+charset=["\'][^"\']+["\'][^>]*>\s*',
        r'<meta\s+name=["\']viewport["\'][^>]*>\s*',
        r'<meta\b(?=[^>]*\bname=["\']description["\'])[^>]*>\s*',
        r'<link\s+rel=["\']canonical["\'][^>]*>\s*',
        r'<meta\b(?=[^>]*\bproperty=["\']og:url["\'])[^>]*>\s*',
        r'<meta\b(?=[^>]*\bproperty=["\']og:site_name["\'])[^>]*>\s*',
        r'<meta\b(?=[^>]*\bproperty=["\']og:title["\'])[^>]*>\s*',
        r'<meta\b(?=[^>]*\bproperty=["\']og:description["\'])[^>]*>\s*',
        r'<meta\b(?=[^>]*\bname=["\']author["\'])[^>]*>\s*',
        r'<meta\b(?=[^>]*\bname=["\']robots["\'])[^>]*>\s*',
        r'<meta\b(?=[^>]*\bname=["\']twitter:title["\'])[^>]*>\s*',
        r'<meta\b(?=[^>]*\bname=["\']twitter:description["\'])[^>]*>\s*',
        r'<meta\b(?=[^>]*\bproperty=["\']article:author["\'])[^>]*>\s*',
        r'<meta\b(?=[^>]*\bproperty=["\']article:publisher["\'])[^>]*>\s*',
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
    rel = path.relative_to(ROOT).as_posix()
    title = TITLE_OVERRIDES.get(rel, title)
    description = DESCRIPTION_OVERRIDES.get(rel, description)
    escaped_url = html.escape(url, quote=True)
    json_title = json.dumps(title, ensure_ascii=False)
    json_description = json.dumps(description, ensure_ascii=False)
    json_url = json.dumps(url, ensure_ascii=False)

    rel_parts = path.relative_to(ROOT).parts
    breadcrumb_items = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": f"{SITE}/",
        }
    ]
    if len(rel_parts) > 1:
        section = rel_parts[0].replace("-", " ").title()
        breadcrumb_items.append({
            "@type": "ListItem",
            "position": 2,
            "name": section,
            "item": f"{SITE}/{rel_parts[0]}/",
        })
    breadcrumb_items.append({
        "@type": "ListItem",
        "position": len(breadcrumb_items) + 1,
        "name": title,
        "item": url,
    })
    breadcrumb_json = json.dumps(breadcrumb_items, ensure_ascii=False, indent=2)
    modified_date = dt.date.fromtimestamp(path.stat().st_mtime).isoformat()
    is_article = path.suffix == ".html" and path.name not in {
        "index.html",
        "about.html",
        "trust-center.html",
        "editorial-policy.html",
        "source-methodology.html",
        "evidence-register.html",
        "corrections.html",
        "ai-disclosure.html",
        "sitemap.html",
    } and path.relative_to(ROOT).as_posix() not in ALIAS_PAGES
    article_schema = ""
    if is_article:
        article_schema = f"""
<script type="application/ld+json" data-article-schema="true">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": {json_title},
  "description": {json_description},
  "mainEntityOfPage": {json_url},
  "dateModified": "{modified_date}",
  "author": {{
    "@type": "Organization",
    "name": "ChatGPT Disaster Documentation Project",
    "url": "{SITE}/about.html"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "ChatGPT Disaster Documentation Project",
    "url": "{SITE}/"
  }},
  "isAccessibleForFree": true
}}
</script>
""".strip()
    faq_schema = ""
    if rel in FAQ_PANELS:
        faq_entities = [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": answer,
                },
            }
            for question, answer in FAQ_PANELS[rel]
        ]
        faq_json = json.dumps(faq_entities, ensure_ascii=False, indent=2)
        faq_schema = f"""
<script type="application/ld+json" data-faq-schema="true">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": {faq_json}
}}
</script>
""".strip()

    additions = f"""
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{html.escape(description, quote=True)}">
<meta name="author" content="ChatGPT Disaster Documentation Project">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{escaped_url}">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{html.escape(description, quote=True)}">
<meta property="og:url" content="{escaped_url}">
<meta property="og:site_name" content="ChatGPT Disaster">
<meta property="article:publisher" content="ChatGPT Disaster Documentation Project">
<meta name="twitter:title" content="{html.escape(title, quote=True)}">
<meta name="twitter:description" content="{html.escape(description, quote=True)}">
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
<script type="application/ld+json" data-breadcrumb-schema="true">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": {breadcrumb_json}
}}
</script>
{article_schema}
{faq_schema}
""".strip()

    # Remove prior script runs before reinserting.
    head = re.sub(r'\s*<script type="application/ld\+json" data-trust-schema="true">.*?</script>', "", head, flags=re.I | re.S)
    head = re.sub(r'\s*<script type="application/ld\+json" data-page-schema="true">.*?</script>', "", head, flags=re.I | re.S)
    head = re.sub(r'\s*<script type="application/ld\+json" data-breadcrumb-schema="true">.*?</script>', "", head, flags=re.I | re.S)
    head = re.sub(r'\s*<script type="application/ld\+json" data-article-schema="true">.*?</script>', "", head, flags=re.I | re.S)
    head = re.sub(r'\s*<script type="application/ld\+json" data-faq-schema="true">.*?</script>', "", head, flags=re.I | re.S)

    if rel in TITLE_OVERRIDES:
        head = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", head, count=1, flags=re.I | re.S)

    if "</title>" in head.lower():
        head = re.sub(r"</title>", "</title>\n" + additions, head, count=1, flags=re.I)
    else:
        head = additions + "\n" + head

    return text[: head_match.start(1)] + head + text[head_match.end(1) :]


def ensure_hidden_h1(text: str, path: Path) -> str:
    if len(re.findall(r"<h1\b", text, flags=re.I)) != 0:
        return text
    title = TITLE_OVERRIDES.get(path.relative_to(ROOT).as_posix(), extract_title(text, path.stem.replace("-", " ").title()))
    hidden_h1 = f'<h1 style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;">{html.escape(title)}</h1>'
    if re.search(r"<body([^>]*)>", text, flags=re.I):
        return re.sub(r"<body([^>]*)>", r"<body\1>\n" + hidden_h1, text, count=1, flags=re.I)
    return hidden_h1 + "\n" + text


def demote_duplicate_brand_h1(text: str) -> str:
    if len(re.findall(r"<h1\b", text, flags=re.I)) <= 1:
        return text
    text = re.sub(
        r'<h1([^>]*class=["\'][^"\']*site-title[^"\']*["\'][^>]*)>',
        r"<div\1>",
        text,
        count=1,
        flags=re.I,
    )
    return re.sub(r"</h1>", "</div>", text, count=1, flags=re.I)


def normalize_subdirectory_links(text: str, path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if "/" not in rel:
        return text

    def repl(match: re.Match[str]) -> str:
        quote = match.group(1)
        href = match.group(2).strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            return match.group(0)
        if re.match(r"^[a-z][a-z0-9+.-]*:", href, flags=re.I):
            return match.group(0)
        clean_href = href.split("#", 1)[0].split("?", 1)[0]
        suffix = href[len(clean_href):]
        clean_no_slash = clean_href.lstrip("/").rstrip("/")
        if clean_no_slash in ROOT_PAGES:
            return f'href={quote}/{clean_no_slash}{suffix}{quote}'
        if clean_no_slash in {"petitions", "failures"}:
            return f'href={quote}/{clean_no_slash}/{suffix}{quote}'
        normalized = posixpath.normpath(posixpath.join(posixpath.dirname(rel), clean_href)).lstrip("./")
        if clean_href.rstrip("/") in {"petitions", "petitions/"}:
            return f'href={quote}/petitions/{suffix}{quote}'
        if normalized in ROOT_PAGES:
            return f'href={quote}/{normalized}{suffix}{quote}'
        if normalized == "petitions":
            return f'href={quote}/petitions/{suffix}{quote}'
        return match.group(0)

    return re.sub(r'href=(["\'])([^"\']+)\1', repl, text, flags=re.I)


def add_trust_panel(text: str) -> str:
    if "editorial-trust-panel" in text:
        return text
    if re.search(r"</footer>", text, flags=re.I):
        return re.sub(r"<footer([^>]*)>", TRUST_LINKS + "\n\n<footer\\1>", text, count=1, flags=re.I)
    if re.search(r"</body>", text, flags=re.I):
        return re.sub(r"</body>", TRUST_LINKS + "\n\n</body>", text, count=1, flags=re.I)
    return text.rstrip() + "\n\n" + TRUST_LINKS + "\n"


def evidence_panel_html(data: dict[str, object]) -> str:
    items = "\n".join(
        f'    <li><strong>{html.escape(label)}:</strong> {html.escape(body)}</li>'
        for label, body in data["items"]
    )
    return f"""
<section class="evidence-quality-panel" style="max-width:900px;margin:34px auto;padding:24px;background:rgba(103,213,255,0.055);border:1px solid rgba(103,213,255,0.2);border-radius:12px;color:inherit;">
  <h2 style="font-size:1.25rem;margin:0 0 12px;color:inherit;">{html.escape(data["heading"])}</h2>
  <p style="margin:0 0 14px;line-height:1.6;">{html.escape(data["intro"])}</p>
  <ul style="margin:0;padding-left:20px;line-height:1.7;">
{items}
  </ul>
  <p style="margin:14px 0 0;font-size:.95rem;opacity:.86;">See also: <a href="/evidence-register.html" style="color:#4fc3f7;">Evidence Register</a> and <a href="/source-methodology.html" style="color:#4fc3f7;">Source Methodology</a>.</p>
</section>
""".strip()


def faq_panel_html(faqs: list[tuple[str, str]]) -> str:
    items = "\n".join(
        f"""  <div style="margin:0 0 18px;">
    <h3 style="font-size:1.05rem;margin:0 0 6px;color:inherit;">{html.escape(question)}</h3>
    <p style="margin:0;line-height:1.65;">{html.escape(answer)}</p>
  </div>"""
        for question, answer in faqs
    )
    return f"""
<section class="seo-faq-panel" style="max-width:900px;margin:34px auto;padding:24px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.14);border-radius:12px;color:inherit;">
  <h2 style="font-size:1.25rem;margin:0 0 16px;color:inherit;">Frequently Asked Questions</h2>
{items}
</section>
""".strip()


def add_faq_panel(text: str, path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel not in FAQ_PANELS:
        return text
    panel = faq_panel_html(FAQ_PANELS[rel])
    if "seo-faq-panel" in text:
        return re.sub(r'<section class="seo-faq-panel".*?</section>', panel, text, count=1, flags=re.I | re.S)
    if re.search(r'<section class="evidence-quality-panel"', text, flags=re.I):
        return re.sub(r'<section class="evidence-quality-panel"', panel + '\n\n<section class="evidence-quality-panel"', text, count=1, flags=re.I)
    if re.search(r'<section class="editorial-trust-panel"', text, flags=re.I):
        return re.sub(r'<section class="editorial-trust-panel"', panel + '\n\n<section class="editorial-trust-panel"', text, count=1, flags=re.I)
    if re.search(r"</main>", text, flags=re.I):
        return re.sub(r"</main>", panel + "\n</main>", text, count=1, flags=re.I)
    return re.sub(r"</body>", panel + "\n</body>", text, count=1, flags=re.I)


def monetization_panel_html(data: dict[str, object]) -> str:
    primary_label, primary_href = data["primary"]
    secondary_label, secondary_href = data["secondary"]
    return f"""
<section class="reader-support-panel" style="max-width:900px;margin:34px auto;padding:24px;background:linear-gradient(135deg,rgba(255,204,102,0.12),rgba(103,213,255,0.08));border:1px solid rgba(255,204,102,0.28);border-radius:12px;color:inherit;">
  <h2 style="font-size:1.25rem;margin:0 0 12px;color:inherit;">{html.escape(data["heading"])}</h2>
  <p style="margin:0 0 16px;line-height:1.6;">{html.escape(data["body"])}</p>
  <div style="display:flex;flex-wrap:wrap;gap:10px;">
    <a href="{html.escape(primary_href)}" style="display:inline-block;color:#101322;background:#ffcc66;text-decoration:none;font-weight:700;padding:10px 14px;border-radius:8px;">{html.escape(primary_label)}</a>
    <a href="{html.escape(secondary_href)}" style="display:inline-block;color:#67d5ff;text-decoration:none;font-weight:700;padding:10px 14px;border:1px solid rgba(103,213,255,0.38);border-radius:8px;">{html.escape(secondary_label)}</a>
  </div>
  <p style="margin:14px 0 0;font-size:.9rem;opacity:.78;">Reader support, paid reports, sponsorships, and affiliate links help fund the archive. See the <a href="/affiliate-disclosure.html" style="color:#4fc3f7;">Affiliate Disclosure</a>.</p>
</section>
""".strip()


def add_monetization_panel(text: str, path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel not in MONETIZATION_PANELS:
        return text
    panel = monetization_panel_html(MONETIZATION_PANELS[rel])
    if "reader-support-panel" in text:
        return re.sub(r'<section class="reader-support-panel".*?</section>', panel, text, count=1, flags=re.I | re.S)
    if re.search(r'<section class="seo-faq-panel"', text, flags=re.I):
        return re.sub(r'<section class="seo-faq-panel"', panel + '\n\n<section class="seo-faq-panel"', text, count=1, flags=re.I)
    if re.search(r'<section class="evidence-quality-panel"', text, flags=re.I):
        return re.sub(r'<section class="evidence-quality-panel"', panel + '\n\n<section class="evidence-quality-panel"', text, count=1, flags=re.I)
    if re.search(r'<section class="editorial-trust-panel"', text, flags=re.I):
        return re.sub(r'<section class="editorial-trust-panel"', panel + '\n\n<section class="editorial-trust-panel"', text, count=1, flags=re.I)
    if re.search(r"</main>", text, flags=re.I):
        return re.sub(r"</main>", panel + "\n</main>", text, count=1, flags=re.I)
    return re.sub(r"</body>", panel + "\n</body>", text, count=1, flags=re.I)


def add_evidence_panel(text: str, path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel not in EVIDENCE_PANELS or "evidence-quality-panel" in text:
        return text
    panel = evidence_panel_html(EVIDENCE_PANELS[rel])
    if re.search(r'<section class="editorial-trust-panel"', text, flags=re.I):
        return re.sub(r'<section class="editorial-trust-panel"', panel + '\n\n<section class="editorial-trust-panel"', text, count=1, flags=re.I)
    if re.search(r"</main>", text, flags=re.I):
        return re.sub(r"</main>", panel + "\n</main>", text, count=1, flags=re.I)
    return re.sub(r"</body>", panel + "\n</body>", text, count=1, flags=re.I)


def normalize_html(path: Path) -> None:
    text = read(path)
    original = text
    text = normalize_subdirectory_links(text, path)
    text = ensure_head_metadata(text, path)
    text = demote_duplicate_brand_h1(text)
    text = ensure_hidden_h1(text, path)
    text = add_monetization_panel(text, path)
    text = add_faq_panel(text, path)
    text = add_evidence_panel(text, path)
    text = add_trust_panel(text)
    if text != original:
        write(path, text)


def alias_template(filename: str, data: dict[str, str]) -> str:
    url = f"{SITE}/{filename}"
    target = data["target"]
    canonical = f"{SITE}{target}"
    title = html.escape(data["title"], quote=True)
    desc = html.escape(data["description"], quote=True)
    h1 = html.escape(data["h1"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta http-equiv="refresh" content="0; url={target}">
<style>
body {{ margin:0; font-family: Inter, Segoe UI, Arial, sans-serif; background:#101322; color:#f4f5f7; line-height:1.7; }}
main {{ max-width:760px; margin:0 auto; padding:56px 20px; }}
a {{ color:#67d5ff; }}
</style>
</head>
<body>
<main>
<h1>{h1}</h1>
<p>{desc}</p>
<p>Continue to <a href="{target}">{target}</a>.</p>
</main>
</body>
</html>
"""


def write_alias_pages() -> None:
    for filename, data in ALIAS_PAGES.items():
        path = ROOT / filename
        path.parent.mkdir(exist_ok=True)
        write(path, alias_template(filename, data))


def policy_template(filename: str, data: dict[str, str]) -> str:
    url = f"{SITE}/{filename}"
    title = html.escape(data["title"], quote=True)
    desc = html.escape(data["description"], quote=True)
    h1 = html.escape(data["h1"])
    kicker = html.escape(data.get("kicker", "Trust Center"))
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
    <div class="kicker">{kicker}</div>
    <h1>{h1}</h1>
    <p>{desc}</p>
    <nav class="nav" aria-label="Trust navigation">
      <a href="/">Home</a>
      <a href="/about.html">About</a>
      <a href="/trust-center.html">Trust Center</a>
      <a href="/editorial-policy.html">Editorial Policy</a>
      <a href="/source-methodology.html">Source Methodology</a>
      <a href="/evidence-register.html">Evidence Register</a>
      <a href="/topic-clusters.html">Topic Clusters</a>
      <a href="/newsletter.html">Newsletter</a>
      <a href="/support.html">Support</a>
      <a href="/affiliate-disclosure.html">Disclosure</a>
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
    if path.name in {"index-backup-20260308.html", "index-redesign.html"}:
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
        rel = path.relative_to(ROOT).as_posix()
        if path.name in POLICY_PAGES:
            priority = "0.5"
            if path.name in {"trust-center.html", "evidence-register.html"}:
                priority = "0.6"
            if path.name in {"newsletter.html", "support.html", "ai-failure-report-2026.html", "topic-clusters.html"}:
                priority = "0.7"
        if rel in ALIAS_PAGES:
            priority = "0.3"
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
    write_alias_pages()
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
