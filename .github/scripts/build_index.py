import os
import re
import html

EXCLUDE_DIRS = {'.git', '.github'}
cards = []

for entry in sorted(os.listdir('.')):
    if os.path.isdir(entry) and entry not in EXCLUDE_DIRS and not entry.startswith('.'):
        index_path = os.path.join(entry, 'index.html')
        if os.path.isfile(index_path):
            with open(index_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Extract <title> from the NotebookLM HTML file
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if title_match and title_match.group(1).strip():
                title = html.unescape(title_match.group(1).strip())
            else:
                title = entry.replace('-', ' ').replace('_', ' ').title()

            # Extract <meta name="description"> if present
            desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
            desc = html.unescape(desc_match.group(1).strip()) if desc_match else f"Interactive NotebookLM site: /{entry}/"

            cards.append(f"""    <div class="site-card">
      <h2><a href="./{entry}/">{html.escape(title)}</a></h2>
      <p>{html.escape(desc)}</p>
    </div>""")

cards_html = "\n".join(cards) if cards else "    <p>No sites published yet.</p>"

page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Interactive Sites – John Coady</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      max-width: 720px;
      margin: 3rem auto;
      padding: 0 1.5rem;
      line-height: 1.6;
      color: #1a1a1a;
    }}
    header {{
      border-bottom: 1px solid #e5e7eb;
      padding-bottom: 1rem;
      margin-bottom: 2rem;
    }}
    nav a {{
      margin-right: 1rem;
      color: #2563eb;
      text-decoration: none;
    }}
    .site-card {{
      border: 1px solid #e5e7eb;
      border-radius: 8px;
      padding: 1.25rem;
      margin-bottom: 1rem;
    }}
    .site-card h2 {{
      margin: 0 0 0.5rem 0;
      font-size: 1.25rem;
    }}
    .site-card a {{
      color: #2563eb;
      text-decoration: none;
    }}
    .site-card a:hover {{
      text-decoration: underline;
    }}
    .site-card p {{
      margin: 0;
      color: #4b5563;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Interactive Sites &amp; Models</h1>
    <nav>
      <a href="https://github.io">← Back to Blog</a>
    </nav>
  </header>
  <main>
{cards_html}
  </main>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(page_html)
