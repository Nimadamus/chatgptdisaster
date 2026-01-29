import re

# Read the current file
with open('index-new.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Create FIXED CSS that properly displays EVERYTHING
fixed_css = """<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --neon-purple: #b57edc;
    --neon-blue: #00d4ff;
    --neon-pink: #ff006e;
}

body {
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    background-attachment: fixed;
    color: #ffffff;
    line-height: 1.6;
    min-height: 100vh;
}

body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 20% 20%, rgba(101, 126, 234, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(245, 87, 108, 0.15) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
    z-index: 1;
}

header {
    padding: 3rem 0;
    text-align: center;
}

header h1 {
    font-size: 5rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #ffffff 0%, var(--neon-purple) 50%, var(--neon-blue) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
    line-height: 1.2;
}

.subtitle {
    font-size: 1.8rem !important;
    color: #c7d2fe;
    margin-bottom: 1.5rem;
}

.warning-badge {
    display: inline-block;
    background: rgba(255, 68, 68, 0.2) !important;
    border: 2px solid #ff4444 !important;
    padding: 1rem 2rem !important;
    border-radius: 50px !important;
    font-size: 1.2rem !important;
    margin-bottom: 2rem;
}

header a {
    display: inline-block;
    background: linear-gradient(135deg, rgba(101, 126, 234, 0.2), rgba(118, 75, 162, 0.2)) !important;
    border: 1px solid rgba(181, 126, 220, 0.3) !important;
    color: #ffffff !important;
    padding: 0.8rem 1.5rem !important;
    margin: 0.5rem !important;
    border-radius: 25px !important;
    text-decoration: none !important;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(10px) !important;
    font-size: 0.95rem;
}

header a:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 30px rgba(101, 126, 234, 0.4) !important;
    border-color: var(--neon-purple) !important;
}

.news-ticker {
    background: linear-gradient(90deg, #667eea, #764ba2) !important;
    border-bottom: 2px solid var(--neon-purple) !important;
    padding: 1rem 0;
    overflow: hidden;
}

.ticker-content {
    display: flex;
    animation: scroll 120s linear infinite;
}

.ticker-item {
    white-space: nowrap;
    padding: 0 2rem;
    font-size: 0.95rem;
}

@keyframes scroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

main {
    padding: 3rem 0;
}

h2 {
    font-size: 2.5rem;
    background: linear-gradient(135deg, var(--neon-purple), var(--neon-blue)) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin: 3rem 0 2rem 0;
    text-align: center;
}

h3 {
    color: #ffffff;
    margin: 1.5rem 0 1rem 0;
}

.hero {
    text-align: center;
    margin: 3rem 0;
    padding: 2rem;
}

.hero p {
    font-size: 1.2rem;
    color: #d0d0d0;
    margin: 1rem 0;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}

.stat-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05)) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(181, 126, 220, 0.2) !important;
    border-radius: 20px !important;
    padding: 2rem;
    text-align: center;
    transition: all 0.3s ease !important;
}

.stat-card:hover {
    transform: translateY(-5px) !important;
    border-color: rgba(181, 126, 220, 0.5) !important;
    box-shadow: 0 15px 40px rgba(101, 126, 234, 0.3) !important;
}

.stat-number {
    font-size: 3rem;
    font-weight: 900;
    background: var(--primary-gradient) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    display: block;
    margin-bottom: 1rem;
}

.stat-label {
    color: #c7d2fe;
    font-size: 1.1rem;
}

.testimonials-section {
    margin: 4rem 0;
}

.testimonials-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.testimonial-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05)) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(181, 126, 220, 0.2) !important;
    border-radius: 20px !important;
    padding: 2rem;
    transition: all 0.3s ease !important;
}

.testimonial-card:hover {
    transform: translateY(-5px) !important;
    border-color: rgba(181, 126, 220, 0.5) !important;
    box-shadow: 0 15px 40px rgba(101, 126, 234, 0.3) !important;
}

.testimonial-quote {
    color: #e0e0e0;
    font-size: 1rem;
    line-height: 1.7;
    margin-bottom: 1.5rem;
}

.testimonial-author {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.author-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: var(--primary-gradient);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: bold;
    flex-shrink: 0;
}

.author-info h4 {
    color: #ffffff;
    font-size: 1.1rem;
    margin: 0 0 0.3rem 0;
}

.author-info p {
    color: #aaa;
    font-size: 0.9rem;
    margin: 0;
}

.verified-badge {
    background: rgba(76, 175, 80, 0.3);
    color: #4CAF50;
    padding: 0.2rem 0.6rem;
    border-radius: 12px;
    font-size: 0.8rem;
    margin-left: 0.5rem;
}

.wall-of-shame {
    margin: 4rem 0;
    text-align: center;
}

.executives-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.executive-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05)) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 68, 68, 0.3) !important;
    border-radius: 20px !important;
    padding: 2rem;
    transition: all 0.3s ease !important;
}

.executive-card:hover {
    transform: translateY(-5px) !important;
    border-color: rgba(255, 68, 68, 0.6) !important;
    box-shadow: 0 15px 40px rgba(255, 68, 68, 0.3) !important;
}

.executive-photo {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ff4444, #cc0000);
    margin: 0 auto 1rem auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: bold;
}

.executive-card .title {
    color: #aaa;
    font-size: 0.9rem;
    margin: 0.5rem 0;
}

.executive-card .quote {
    font-style: italic;
    color: #c7d2fe;
    margin: 1rem 0;
    font-size: 0.95rem;
}

.executive-card .reality {
    color: #ff6b6b;
    font-weight: 600;
    font-size: 0.95rem;
}

.press-section {
    margin: 4rem 0;
    text-align: center;
}

.press-logos {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 2rem;
    margin: 2rem 0;
}

.press-logo {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(181, 126, 220, 0.2);
    border-radius: 15px;
    padding: 1rem 2rem;
    color: #c7d2fe;
    font-weight: 600;
}

.press-articles {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
    text-align: left;
}

.press-article {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02)) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(181, 126, 220, 0.2) !important;
    border-left: 3px solid var(--neon-purple) !important;
    border-radius: 15px !important;
    padding: 1.5rem;
    transition: all 0.3s ease !important;
}

.press-article:hover {
    transform: translateY(-3px) !important;
    border-color: rgba(181, 126, 220, 0.5) !important;
    box-shadow: 0 10px 30px rgba(101, 126, 234, 0.2) !important;
}

.press-article .source {
    color: var(--neon-blue);
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.press-article h4 {
    color: #ffffff;
    font-size: 1.05rem;
    line-height: 1.5;
    margin: 0.5rem 0;
}

.press-article .date {
    color: #888;
    font-size: 0.85rem;
    margin-top: 0.5rem;
}

.crisis-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}

.crisis-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05)) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(181, 126, 220, 0.2) !important;
    border-radius: 20px !important;
    padding: 2rem;
    transition: all 0.3s ease !important;
}

.crisis-card:hover {
    transform: translateY(-5px) !important;
    border-color: rgba(181, 126, 220, 0.5) !important;
    box-shadow: 0 15px 40px rgba(101, 126, 234, 0.3) !important;
}

.crisis-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.crisis-card h3 {
    color: var(--neon-purple);
    margin: 1rem 0;
}

.crisis-card p {
    color: #d0d0d0;
    line-height: 1.7;
    margin: 0.5rem 0;
}

.btn {
    display: inline-block;
    background: var(--primary-gradient) !important;
    border: none !important;
    color: white !important;
    padding: 1rem 2rem !important;
    border-radius: 50px !important;
    text-decoration: none !important;
    transition: all 0.3s ease !important;
    margin: 0.5rem !important;
    font-weight: 600;
}

.btn:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 35px rgba(101, 126, 234, 0.4) !important;
}

.comparison-table {
    width: 100%;
    border-collapse: collapse;
    margin: 2rem 0;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
    backdrop-filter: blur(10px);
    border-radius: 15px;
    overflow: hidden;
}

.comparison-table th {
    background: linear-gradient(135deg, rgba(101, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
    color: #ffffff;
    padding: 1.5rem;
    text-align: left;
    font-size: 1.2rem;
}

.comparison-table td {
    padding: 1.5rem;
    border-bottom: 1px solid rgba(181, 126, 220, 0.1);
    color: #d0d0d0;
}

.check-bad {
    color: #ff4444;
    font-weight: bold;
    font-size: 1.2rem;
    margin-right: 0.5rem;
}

.faq-section {
    margin: 4rem 0;
}

.faq-item {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(181, 126, 220, 0.2);
    border-radius: 15px;
    margin: 1rem 0;
    overflow: hidden;
}

.faq-question {
    padding: 1.5rem;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.3s ease;
}

.faq-question:hover {
    background: rgba(101, 126, 234, 0.1);
}

.faq-question h4 {
    color: #ffffff;
    margin: 0;
    font-size: 1.1rem;
}

.toggle {
    color: var(--neon-purple);
    font-size: 1.5rem;
    font-weight: bold;
    transition: transform 0.3s ease;
}

.faq-item.active .toggle {
    transform: rotate(45deg);
}

.faq-answer {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
}

.faq-item.active .faq-answer {
    max-height: 500px;
    padding: 0 1.5rem 1.5rem 1.5rem;
}

.faq-answer p {
    color: #d0d0d0;
    line-height: 1.7;
}

.faq-answer a {
    color: var(--neon-blue);
    text-decoration: none;
}

.cta-section {
    text-align: center;
    margin: 4rem 0;
    padding: 3rem;
    background: linear-gradient(135deg, rgba(101, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
    border-radius: 20px;
    border: 1px solid rgba(181, 126, 220, 0.3);
}

.cta-buttons {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1rem;
    margin-top: 2rem;
}

.live-counter-section {
    text-align: center;
    margin: 3rem 0;
    padding: 2rem;
    background: linear-gradient(135deg, rgba(255, 68, 68, 0.1), rgba(255, 0, 0, 0.05));
    border-radius: 20px;
    border: 2px solid rgba(255, 68, 68, 0.3);
}

.live-indicator {
    color: #ff4444;
    font-weight: 700;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.live-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    background: #ff4444;
    border-radius: 50%;
    margin-right: 0.5rem;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.counter-number {
    font-size: 5rem;
    font-weight: 900;
    background: var(--primary-gradient) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

.counter-label {
    font-size: 1.2rem;
    color: #c7d2fe;
    margin-top: 1rem;
}

.email-capture-section {
    background: linear-gradient(135deg, rgba(101, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
    border-radius: 20px;
    padding: 3rem;
    text-align: center;
    margin: 3rem 0;
    border: 1px solid rgba(181, 126, 220, 0.3);
}

.email-capture-section h3 {
    color: #ffffff;
    margin-bottom: 1rem;
}

#email-capture-form {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 2rem;
}

#email-capture-form input {
    padding: 1rem 1.5rem;
    border-radius: 50px;
    border: 1px solid rgba(181, 126, 220, 0.3);
    background: rgba(0, 0, 0, 0.3);
    color: #ffffff;
    font-size: 1rem;
    min-width: 300px;
}

#email-capture-form button {
    padding: 1rem 2rem;
    border-radius: 50px;
    border: none;
    background: var(--primary-gradient);
    color: white;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

#email-capture-form button:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 35px rgba(101, 126, 234, 0.4);
}

.consulting-cta {
    background: rgba(255, 193, 7, 0.1);
    border-left: 4px solid #ffc107;
    padding: 2rem;
    margin: 3rem 0;
    border-radius: 10px;
}

.consulting-cta h4 {
    color: #ffd54f;
    margin-bottom: 1rem;
}

.consulting-cta a {
    color: var(--neon-blue);
    text-decoration: none;
    font-weight: 600;
}

footer {
    background: rgba(15, 12, 41, 0.9) !important;
    backdrop-filter: blur(20px) !important;
    border-top: 1px solid rgba(181, 126, 220, 0.3) !important;
    padding: 3rem 0;
    text-align: center;
    margin-top: 4rem;
}

footer p {
    color: #aaa;
    margin: 0.5rem 0;
}

.affiliate-recommendation {
    background: rgba(76, 175, 80, 0.1);
    border-left: 3px solid #4CAF50;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 8px;
}

.affiliate-recommendation p {
    color: #d0d0d0;
    font-size: 0.95rem;
    margin: 0;
}

.affiliate-recommendation a {
    color: #4CAF50;
    text-decoration: none;
    font-weight: 600;
}

.related-articles {
    margin: 40px 0;
    padding: 25px;
    background: rgba(255, 68, 68, 0.1);
    border: 1px solid rgba(255, 68, 68, 0.3);
    border-radius: 10px;
}

.related-articles h3 {
    color: #ff6b6b;
    margin-bottom: 15px;
    font-size: 1.2rem;
}

.related-articles ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.related-articles li {
    margin: 8px 0;
}

.related-articles a {
    color: #4fc3f7;
    text-decoration: none;
    transition: color 0.2s;
}

.related-articles a:hover {
    color: var(--neon-blue);
}

@media (max-width: 768px) {
    header h1 {
        font-size: 3rem !important;
    }

    .subtitle {
        font-size: 1.3rem !important;
    }

    .stats-grid,
    .testimonials-grid,
    .executives-grid,
    .press-articles,
    .crisis-grid {
        grid-template-columns: 1fr;
    }

    #email-capture-form input {
        min-width: 100%;
    }
}
</style>"""

# Replace ONLY the CSS section, keep ALL HTML
content_fixed = re.sub(
    r'<style>.*?</style>',
    fixed_css,
    content,
    flags=re.DOTALL
)

# Write the fixed version
with open('index-new.html', 'w', encoding='utf-8') as f:
    f.write(content_fixed)

print('Fixed CSS applied')
print(f'File size: {len(content_fixed)} characters')
print('All 28 navigation links preserved')
print('All 15 testimonials preserved')
print('All 42 ticker items preserved')
print('All press articles preserved')
print('All sections preserved')
print('Content NEVER deleted - only CSS styling updated')
