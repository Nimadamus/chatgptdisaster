import re

# Read the original index.html
with open('C:/Users/Nima/chatgptdisaster/index.html', 'r', encoding='utf-8') as f:
    original = f.read()

# Extract body content
body_match = re.search(r'<body[^>]*>(.*?)</body>', original, re.DOTALL)
body_content = body_match.group(1)

# Extract head meta/scripts (not styles)
head_match = re.search(r'<head[^>]*>(.*?)</head>', original, re.DOTALL)
head_content = head_match.group(1)

# Get meta tags and scripts
meta_tags = re.findall(r'<meta[^>]*>', head_content)
title_match = re.search(r'<title[^>]*>.*?</title>', head_content, re.DOTALL)
script_matches = re.findall(r'<script type="application/ld\+json">.*?</script>', head_content, re.DOTALL)

preserved_head = ""

# New SEO-optimized title for ChatGPT review site
new_title = '<title>ChatGPT 5.2 Review 2026 - Honest User Reviews & Real Performance Tests</title>'
preserved_head += new_title + "\n"

# Update meta tags for review site positioning
for meta in meta_tags:
    # Replace description
    if 'name="description"' in meta:
        meta = '<meta name="description" content="The most comprehensive ChatGPT 5.2 review site. Real user reviews, performance tests, comparisons with Claude & Gemini. Unbiased analysis of GPT-5 problems, bugs, and whether it\'s worth the subscription in 2026.">'
    # Replace keywords
    elif 'name="keywords"' in meta:
        meta = '<meta name="keywords" content="ChatGPT 5.2 review, ChatGPT review 2026, GPT-5 review, ChatGPT Plus review, is ChatGPT worth it, ChatGPT vs Claude, ChatGPT problems, ChatGPT honest review, GPT-5.2 bugs, ChatGPT performance test">'
    # Replace og:title
    elif 'property="og:title"' in meta:
        meta = '<meta property="og:title" content="ChatGPT 5.2 Review 2026 - Honest User Reviews & Real Performance Tests">'
    # Replace og:description
    elif 'property="og:description"' in meta:
        meta = '<meta property="og:description" content="The most comprehensive ChatGPT 5.2 review. Real user experiences, performance benchmarks, and honest analysis.">'
    # Replace twitter:title
    elif 'name="twitter:title"' in meta:
        meta = '<meta name="twitter:title" content="ChatGPT 5.2 Review 2026 - Honest User Reviews & Performance Tests">'
    # Replace twitter:description
    elif 'name="twitter:description"' in meta:
        meta = '<meta name="twitter:description" content="The most comprehensive ChatGPT 5.2 review. Real user experiences and honest analysis.">'
    preserved_head += meta + "\n"

for script in script_matches:
    # Update the NewsArticle schema
    if 'NewsArticle' in script:
        script = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": {
    "@type": "SoftwareApplication",
    "name": "ChatGPT 5.2",
    "applicationCategory": "AI Assistant",
    "operatingSystem": "Web, iOS, Android"
  },
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "2.5",
    "bestRating": "5",
    "worstRating": "1"
  },
  "author": {
    "@type": "Organization",
    "name": "ChatGPT Review Hub"
  },
  "datePublished": "2026-01-29",
  "reviewBody": "Comprehensive review of ChatGPT 5.2 based on thousands of real user experiences, performance tests, and comparisons with alternatives like Claude and Gemini."
}
</script>'''
    preserved_head += script + "\n"

# New hero section (no corner brackets) - Review site focused
new_hero = '''
    <!-- Hero - New Large Design -->
    <section class="hero">
        <div class="hero-glow"></div>

        <div class="hero-content">
            <p class="hero-tagline">Honest Reviews From Real Users</p>

            <h1 class="hero-title">
                <span class="the-word">THE</span>
                <span class="main-line"><span class="white">CHAT</span><span class="gold">GPT</span></span>
                <span class="disaster-line">5.2 REVIEW</span>
            </h1>

            <div class="hero-divider"></div>

            <p class="hero-subtitle">Real performance tests &bull; User experiences &bull; Unbiased analysis</p>

            <div class="hero-actions">
                <a href="stories.html" class="btn btn-primary">Read User Reviews</a>
                <a href="alternatives.html" class="btn btn-secondary">Compare Alternatives</a>
                <a href="performance-decline.html" class="btn btn-secondary">Performance Tests</a>
            </div>
        </div>
    </section>
'''

# Replace the old hero section
old_hero_pattern = r'<!-- Hero Section -->.*?(?=<!-- Stats Dashboard -->)'
body_content = re.sub(old_hero_pattern, new_hero + '\n\n    ', body_content, flags=re.DOTALL)

# Clean up navigation for homepage:
# 1. Remove the exclamation mark icon
body_content = re.sub(r'<div class="nav-logo-icon">!</div>\s*', '', body_content)

# 2. Remove the theme toggle (moon icon)
body_content = re.sub(r'<button class="theme-toggle"[^>]*>.*?</button>\s*', '', body_content)

# 3. Remove "Home" link from homepage nav (it's redundant on the homepage)
body_content = re.sub(r'<li class="nav-item">\s*<a href="index\.html" class="nav-link active">Home</a>\s*</li>\s*', '', body_content)

# 4. Update logo text to reflect review site
body_content = body_content.replace('ChatGPT <span>Disaster</span>', 'ChatGPT <span>Review Hub</span>')

# 5. Remove the "ChatGPT Disaster Home" link from the footer (redundant on homepage)
body_content = re.sub(r'<li><a href="index\.html"[^>]*>ChatGPT Disaster Home</a></li>\s*', '', body_content)

# 4. Remove the news ticker completely
body_content = re.sub(r'<!-- Breaking News Ticker -->.*?</div>\s*</div>\s*(?=<!-- Navigation -->)', '', body_content, flags=re.DOTALL)

# 5. Remove the Stats Dashboard section (the numbers)
body_content = re.sub(r'<!-- Stats Dashboard -->.*?(?=<!-- Main Content Intro -->)', '', body_content, flags=re.DOTALL)

# 6. Change "Real Users. Real Suffering. Real Stories." to just "Real Users. Real Stories."
body_content = body_content.replace('Real Users. Real Suffering. Real Stories.', 'Real Users. Real Stories.')

# 7. Change "Major Outlets Are Finally Covering the Truth" to "Major Outlets Covering the Truth"
body_content = body_content.replace('Major Outlets Are Finally Covering the Truth', 'Major Outlets Covering the Truth')

# 9. Change "delivered failure" to "delivered something else" - more understated and credible
body_content = body_content.replace('delivered failure', 'delivered something else')

# 10. Change "They Delivered a Nightmare" to "They Delivered Something Else"
body_content = body_content.replace('They Delivered a Nightmare', 'They Delivered Something Else')

# 11. Change "ChatGPT: Promise vs. Reality" to "Promises vs. Reality"
body_content = body_content.replace('ChatGPT: Promise vs. Reality', 'Promises vs. Reality')

# 8. Swap Wall of Shame and Crisis Categories sections
wall_of_shame_match = re.search(r'(<!-- Wall of Shame -->.*?</section>)', body_content, re.DOTALL)
crisis_categories_match = re.search(r'(<!-- Crisis Categories -->.*?</section>)', body_content, re.DOTALL)

if wall_of_shame_match and crisis_categories_match:
    wall_of_shame = wall_of_shame_match.group(1)
    crisis_categories = crisis_categories_match.group(1)
    # Replace wall of shame with a placeholder
    body_content = body_content.replace(wall_of_shame, '<!--PLACEHOLDER_CRISIS-->')
    # Replace crisis categories with wall of shame
    body_content = body_content.replace(crisis_categories, wall_of_shame)
    # Replace placeholder with crisis categories
    body_content = body_content.replace('<!--PLACEHOLDER_CRISIS-->', crisis_categories)

# Count to verify
counts = {
    'ticker': len(re.findall(r'<span class="ticker-item">', body_content)),
    'testimonials': len(re.findall(r'class="testimonial-card"', body_content)),
    'executives': len(re.findall(r'class="executive-card"', body_content)),
    'press': len(re.findall(r'class="press-article', body_content)),
    'crisis': len(re.findall(r'class="crisis-card"', body_content)),
    'faq': len(re.findall(r'class="faq-item', body_content)),
    'docs': len(re.findall(r'class="docs-category', body_content))
}

print("Content verification:")
for k, v in counts.items():
    print(f"  {k}: {v}")

# Read the CSS from file
with open('C:/Users/Nima/chatgptdisaster/black_gold_styles.css', 'r', encoding='utf-8') as f:
    css_styles = f.read()

# Build final HTML
html_output = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{preserved_head}

<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
{css_styles}
</style>
</head>
<body>
{body_content}
</body>
</html>
'''

# Write final file
with open('C:/Users/Nima/chatgptdisaster/PREVIEW-BLACK-GOLD-FINAL.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print(f"\nCreated PREVIEW-BLACK-GOLD-FINAL.html ({len(html_output)} chars)")
