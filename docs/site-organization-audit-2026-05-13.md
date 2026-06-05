# ChatGPT Disaster Site Organization Audit

Date: 2026-05-13
Scope: live public site audit plus local structure review
Status: planning only, no production changes made

## Guardrails

- Do not edit `sitemap.xml` without a separate explicit approval.
- Do not change canonical URLs, redirects, or indexed URL paths during the organization pass.
- Preserve existing article URLs and long-tail search pages.
- Treat legal, medical, mental-health, death, lawsuit, and mass-shooting content as high-risk editorial content.
- Keep current live content available while improving navigation and discovery.

## Current Live Site Findings

- `https://chatgptdisaster.com/` returns HTTP 200.
- `https://chatgptdisaster.com/sitemap.xml` returns HTTP 200.
- Sitemap contains 232 URLs.
- Sitemap crawl found no 3xx, 4xx, or 5xx responses.
- Homepage internal-link crawl checked 218 unique internal URLs and found no broken links.
- Homepage is very large: about 244 KB of HTML, 287 links, and 39 images.
- `stories.html` is larger: about 328 KB with 218 H2 headings.
- The site has one H1 per crawled sitemap page, which is good.
- Duplicate title tags were not found in the sitemap crawl.

## Main Organization Problems

1. Homepage scope is too broad.
   The homepage tries to be a landing page, archive, story directory, press page, comparison page, petition funnel, and latest-post index at the same time.

2. Navigation is dense.
   Top navigation has multiple dropdowns plus standalone links, then the homepage repeats many of the same destinations in bento cards, story chips, archive links, and press cards.

3. Homepage H1 is misaligned.
   Current H1 is `THE CHATGPT 5.2 REVIEW`, while the title/meta position the site as a broader AI failures, lawsuits, outages, and safety archive.

4. Story pages are too heavy.
   `stories.html` and several `stories-pageN.html` files are huge and hard to scan. They should remain live, but users need a more navigable story hub.

5. Evidence labels are inconsistent.
   High-risk pages mix verified facts, allegations, user reports, lawsuits, and opinion without a consistent visible labeling system.

6. Archive concepts overlap.
   `archive.html`, `archive/index.html`, `latest.html`, `documentation-index.html`, `stories.html`, `topic-clusters.html`, and homepage static discovery all compete for the same "find content" role.

7. SEO metadata needs selective cleanup.
   The crawl found 121 title tags over 70 characters and 7 short meta descriptions. This should be handled gradually, not as a broad automated rewrite.

8. Local repo hygiene needs attention.
   The active-looking repo has many dirty files. Separate publish copies also contain sensitive deployment artifacts that should be cleaned outside the content redesign.

## Recommended Information Architecture

Use six top-level hubs:

1. Start Here
   - Mission
   - Editorial standards
   - Source labels
   - Latest major investigations

2. User Reports
   - Story library
   - Category filters
   - Submit your experience
   - Story count methodology

3. Safety and Mental Health
   - Mental health crisis
   - Clinical cases
   - Victims memorial
   - Death lawsuits
   - Crisis resources

4. Reliability and Performance
   - Performance decline
   - GPT-5/GPT-5.2 backlash
   - ChatGPT not working
   - Coding failures
   - Status tracker
   - Outage guides

5. Legal and Business
   - Lawsuits
   - Legal hallucinations
   - Enterprise failures
   - Business impact
   - Media coverage

6. Alternatives and Guides
   - Alternatives
   - What to do when ChatGPT is down
   - When not to trust ChatGPT
   - Verification guides
   - Support the archive

## Homepage Restructure Proposal

Keep the homepage as an orienting dashboard, not an archive dump.

Recommended homepage order:

1. Hero
   - Clear H1: `ChatGPT Disaster`
   - Supporting line: `An independent archive of AI failures, safety incidents, lawsuits, outages, and user reports.`
   - Primary CTA: `Start Here`
   - Secondary CTA: `Browse User Reports`

2. Four Primary Paths
   - User Reports
   - Safety and Mental Health
   - Reliability and Performance
   - Legal and Business

3. Latest Investigations
   - 6 to 9 article cards only.
   - Link to `latest.html` or `archive.html` for the full list.

4. Evidence Library
   - Compact links to Documentation Index, Timeline, Lawsuits, Press Coverage, Status Tracker.

5. Source Transparency
   - Short explanation of labels:
     - Verified fact
     - Allegation
     - User report
     - Court filing
     - Analysis/opinion

6. Story Funnel
   - One short module for stories.
   - Do not show all story page chips on the homepage.

7. Support / Petition
   - Keep as a restrained final section.

## Navigation Proposal

Desktop nav:

- Start Here
- User Reports
- Safety
- Reliability
- Legal
- Alternatives
- Latest
- Support

Mobile nav should use the same labels, no large dropdown wall.

Dropdowns, if kept, should have a maximum of 5 visible links each.

## Editorial Labeling System

Every high-risk page should display one primary label near the headline:

- `Verified fact`
- `Court filing`
- `Allegation`
- `User report`
- `Research summary`
- `Opinion / analysis`

Use this to protect credibility. A lawsuit page should not visually read the same as a verified incident page or an opinion page.

## Priority Fix List

### Phase 1: Planning and Mockup

- Create non-production homepage mockup.
- Create category map from existing URLs to the six hubs.
- Create a source-label taxonomy.
- Do not publish.

### Phase 2: Low-Risk Local Build

- Build a replacement homepage in a separate file.
- Keep all current URLs.
- Keep current sitemap untouched.
- Build a compact navigation include/template if the static setup supports it.
- Add a visual source-label component.

### Phase 3: Controlled Review

- Compare old and new homepage side by side.
- Check all homepage links.
- Check title/H1 alignment.
- Check mobile rendering.
- Only then consider replacing `index.html`.

### Phase 4: Gradual Content Cleanup

- Fix short meta descriptions one page at a time.
- Shorten only the worst title tags first.
- Split story library discovery into smaller category hubs while preserving existing story pages.
- Do not mass rewrite article content.

## Files To Avoid Without Explicit Approval

- `sitemap.xml`
- `.htaccess`
- `robots.txt`
- Any canonical link changes
- Existing article filename changes
- Existing article deletion
- Existing archive URL changes

## Proposed Next Decision

Review the mockup concept at:

```text
_redesign-concepts-archive/homepage-organization-mockup-2026-05-13.html
```

If the structure is approved, the next step is a local replacement homepage draft that preserves the live URL set and can be audited before publication.
