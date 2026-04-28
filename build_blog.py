#!/usr/bin/env python3
"""Convert Faro markdown blog posts to HTML pages for GitHub Pages."""

import os, re, html

BLOG_DIR = os.path.dirname(os.path.abspath(__file__)) + "/blog"
CONTENT_DIR = "/Users/tony/.openclaw/workspace/faro/content/blog"

TEAL = "#01696F"
TEAL_DARK = "#015559"
TEAL_LIGHT = "#e6f4f4"
NAVY = "#1B3A4B"

# ── Shared CSS ──────────────────────────────────────────────────────────────
SHARED_CSS = """
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; font-size: 16px; }
  body {
    font-family: 'Inter', sans-serif;
    color: #1B3A4B;
    background: #FFFFFF;
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
  }
  a { color: #01696F; text-decoration: underline; }
  a:hover { color: #015559; }
  img { max-width: 100%; display: block; }

  :root {
    --teal: #01696F; --teal-dark: #015559; --teal-light: #e6f4f4;
    --navy: #1B3A4B; --white: #FFFFFF; --bg: #F4F9F9;
    --text-muted: #5a7a8a; --radius: 12px;
    --shadow: 0 4px 24px rgba(1,105,111,0.10);
  }

  .container { max-width: 820px; margin: 0 auto; padding: 0 24px; }

  /* Navbar */
  .navbar {
    background: #fff; border-bottom: 1px solid #e8f2f2;
    padding: 0; position: sticky; top: 0; z-index: 100;
  }
  .navbar .inner {
    max-width: 820px; margin: 0 auto; padding: 14px 24px;
    display: flex; align-items: center; justify-content: space-between; gap: 16px;
  }
  .navbar-brand { display:flex; align-items:center; gap:10px; text-decoration:none; }
  .navbar-logo { height: 32px; width: auto; }
  .navbar-wordmark {
    font-size: 1.25rem; font-weight: 800; color: var(--navy); letter-spacing: -0.5px;
  }
  .navbar-wordmark span { color: var(--teal); }
  .navbar-links { display:flex; align-items:center; gap:20px; }
  .navbar-links a {
    font-size: 0.9rem; font-weight: 500; color: var(--text-muted);
    text-decoration: none; transition: color 0.15s;
  }
  .navbar-links a:hover { color: var(--teal); }
  .btn-nav {
    background: var(--teal); color: #fff !important;
    padding: 8px 18px; border-radius: 50px;
    font-size: 0.875rem !important; font-weight: 600 !important;
    text-decoration: none !important; transition: background 0.2s;
  }
  .btn-nav:hover { background: var(--teal-dark) !important; }

  /* Breadcrumb */
  .breadcrumb {
    padding: 16px 0 0;
    font-size: 0.85rem; color: var(--text-muted);
  }
  .breadcrumb a { color: var(--teal); text-decoration: none; }
  .breadcrumb a:hover { text-decoration: underline; }
  .breadcrumb span { margin: 0 6px; }

  /* Article header */
  .article-header { padding: 32px 0 24px; }
  .article-tag {
    display: inline-block;
    background: var(--teal-light); color: var(--teal);
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.06em;
    text-transform: uppercase; padding: 5px 12px; border-radius: 50px;
    margin-bottom: 14px;
  }
  .article-header h1 {
    font-size: clamp(1.6rem, 4vw, 2.2rem);
    font-weight: 800; line-height: 1.2; color: var(--navy);
    margin-bottom: 12px;
  }
  .article-meta { font-size: 0.85rem; color: var(--text-muted); }

  /* Disclosure box */
  .disclosure {
    background: #FFF8E6; border-left: 4px solid #C9993A;
    padding: 12px 16px; border-radius: 0 8px 8px 0;
    font-size: 0.875rem; color: #6b5100; margin: 20px 0;
    font-style: italic;
  }

  /* Article body */
  .article-body { padding-bottom: 48px; }
  .article-body h2 {
    font-size: 1.4rem; font-weight: 700; color: var(--navy);
    margin: 36px 0 14px; line-height: 1.25;
  }
  .article-body h3 {
    font-size: 1.1rem; font-weight: 700; color: var(--navy);
    margin: 24px 0 10px;
  }
  .article-body p { margin-bottom: 16px; }
  .article-body ul, .article-body ol {
    padding-left: 24px; margin-bottom: 16px;
  }
  .article-body li { margin-bottom: 6px; }
  .article-body hr {
    border: none; border-top: 1px solid #e0ecec; margin: 32px 0;
  }
  .article-body blockquote {
    background: var(--teal-light); border-left: 4px solid var(--teal);
    padding: 14px 18px; border-radius: 0 8px 8px 0; margin: 20px 0;
    font-size: 0.95rem;
  }
  .article-body blockquote p { margin: 0; }
  .article-body em { font-style: italic; }
  .article-body strong { font-weight: 700; }

  /* Tables */
  .table-wrap { overflow-x: auto; margin: 20px 0; }
  table {
    width: 100%; border-collapse: collapse;
    font-size: 0.9rem;
  }
  thead th {
    background: var(--teal); color: #fff;
    padding: 10px 14px; text-align: left; font-weight: 600;
  }
  tbody tr:nth-child(even) { background: var(--teal-light); }
  tbody td { padding: 10px 14px; border-bottom: 1px solid #daeaea; }

  /* Wise note */
  .wise-note {
    background: #f0f8ff; border: 1px solid #b3d9f7;
    border-radius: 8px; padding: 14px 18px; margin: 16px 0;
    font-size: 0.9rem;
  }
  .wise-note a { color: var(--teal); }

  /* CTA box */
  .cta-box {
    background: var(--teal); color: #fff;
    border-radius: 14px; padding: 28px 32px;
    text-align: center; margin: 40px 0 32px;
  }
  .cta-box p { color: #fff; margin: 0; font-size: 1.05rem; font-weight: 500; }
  .cta-box a {
    color: #fff; font-weight: 700;
    text-decoration: underline;
  }
  .cta-box a:hover { opacity: 0.85; }

  /* Footer */
  footer {
    background: var(--navy); color: #a0bcc8;
    padding: 28px 24px; text-align: center; font-size: 0.85rem;
  }
  footer a { color: #7ac4cc; text-decoration: none; }
  footer a:hover { text-decoration: underline; }

  /* Responsive */
  @media (max-width: 600px) {
    .navbar .inner { padding: 12px 16px; }
    .container { padding: 0 16px; }
    .cta-box { padding: 20px 18px; }
    .article-header h1 { font-size: 1.5rem; }
  }
"""

HTML_HEAD = """<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | Faro</title>
  <meta name="description" content="{desc}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
  <style>
""" + SHARED_CSS + """
  </style>
</head>
"""

NAVBAR_HTML = """<nav class="navbar">
  <div class="inner">
    <a href="/" class="navbar-brand">
      <img src="/brand/logo-final.png" alt="Faro" class="navbar-logo">
      <div class="navbar-wordmark">tu<span>faro</span>.io</div>
    </a>
    <div class="navbar-links">
      <a href="/blog/">Blog</a>
      <a href="/impuesto/" style="color:var(--text-muted);text-decoration:none;">Calculadora</a>
      <a href="https://wa.me/15005550006" class="btn-nav" target="_blank" rel="noopener">Probar Faro</a>
    </div>
  </div>
</nav>"""

FOOTER_HTML = """<footer>
  <p>© 2026 Faro · <a href="/">tufaro.io</a> · <a href="/blog/">Blog</a> · <a href="mailto:hola@tufaro.io">hola@tufaro.io</a></p>
  <p style="margin-top:8px;font-size:0.78rem;opacity:0.7;">Las tasas son referenciales. Verifica siempre antes de enviar. Faro no es un servicio de transferencia de dinero.</p>
</footer>"""


def parse_frontmatter(text):
    """Extract YAML frontmatter from markdown."""
    meta = {}
    if text.startswith("---"):
        end = text.index("---", 3)
        fm = text[3:end].strip()
        body = text[end+3:].strip()
        for line in fm.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
    else:
        body = text
    return meta, body


def md_to_html(md):
    """Convert markdown body to HTML (simplified converter)."""
    lines = md.split("\n")
    out = []
    in_table = False
    table_lines = []
    in_list = False
    list_type = None

    def flush_table():
        nonlocal in_table, table_lines
        if not table_lines:
            return
        html_t = ['<div class="table-wrap"><table>']
        header = None
        body_rows = []
        separator_idx = None
        for i, tl in enumerate(table_lines):
            cells = [c.strip() for c in tl.strip("|").split("|")]
            if i == 0:
                header = cells
            elif all(re.match(r"^[-:]+$", c.strip()) for c in cells if c.strip()):
                separator_idx = i
            else:
                body_rows.append(cells)
        if header:
            html_t.append("<thead><tr>")
            for c in header:
                html_t.append(f"<th>{inline_md(c)}</th>")
            html_t.append("</tr></thead>")
        html_t.append("<tbody>")
        for row in body_rows:
            html_t.append("<tr>")
            for c in row:
                html_t.append(f"<td>{inline_md(c)}</td>")
            html_t.append("</tr>")
        html_t.append("</tbody></table></div>")
        out.append("\n".join(html_t))
        table_lines = []
        in_table = False

    def flush_list():
        nonlocal in_list, list_type
        if in_list:
            out.append(f"</{list_type}>")
            in_list = False
            list_type = None

    def inline_md(text):
        """Process inline markdown."""
        # Bold
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        # Italic (but not the disclosure line processed separately)
        text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
        # Links
        text = re.sub(r"\[([^\]]+)\]\((https?://[^\)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
        # Checkmarks
        text = text.replace("✅", "✅").replace("❌", "❌")
        return text

    i = 0
    while i < len(lines):
        line = lines[i]

        # Blank line
        if not line.strip():
            flush_list()
            i += 1
            continue

        # HR
        if re.match(r"^---+$", line.strip()):
            flush_list()
            flush_table()
            out.append("<hr>")
            i += 1
            continue

        # Headings
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            flush_list()
            flush_table()
            level = len(m.group(1))
            content = inline_md(m.group(2))
            out.append(f"<h{level}>{content}</h{level}>")
            i += 1
            continue

        # Table row
        if line.strip().startswith("|"):
            flush_list()
            in_table = True
            table_lines.append(line)
            i += 1
            continue
        elif in_table:
            flush_table()

        # Blockquote
        if line.strip().startswith(">"):
            flush_list()
            content = line.strip().lstrip("> ")
            out.append(f'<blockquote><p>{inline_md(content)}</p></blockquote>')
            i += 1
            continue

        # Unordered list
        m = re.match(r"^[-*]\s+(.+)$", line)
        if m:
            if not in_list or list_type != "ul":
                flush_list()
                out.append("<ul>")
                in_list = True
                list_type = "ul"
            out.append(f"<li>{inline_md(m.group(1))}</li>")
            i += 1
            continue

        # Ordered list
        m = re.match(r"^\d+\.\s+(.+)$", line)
        if m:
            if not in_list or list_type != "ol":
                flush_list()
                out.append("<ol>")
                in_list = True
                list_type = "ol"
            out.append(f"<li>{inline_md(m.group(1))}</li>")
            i += 1
            continue

        # Disclosure / italic paragraph (starts and ends with *)
        if line.strip().startswith("*") and line.strip().endswith("*") and not line.strip().startswith("**"):
            flush_list()
            content = line.strip().strip("*")
            out.append(f'<div class="disclosure">*{html.escape(content)}*</div>')
            i += 1
            continue

        # Regular paragraph
        flush_list()
        out.append(f"<p>{inline_md(line.strip())}</p>")
        i += 1

    flush_list()
    flush_table()
    return "\n".join(out)


def build_article_page(meta, body, lang, depth=2):
    """Build a full article HTML page."""
    title = meta.get("title", "")
    desc = meta.get("meta_description", "")
    slug = meta.get("slug", "").lstrip("/")  # e.g. blog/cheapest-ways...
    updated = meta.get("updated", "2026")
    lang_attr = lang

    # Detect disclosure line and pull it out to style specially
    # (already handled in md_to_html via the disclosure CSS class)

    body_html = md_to_html(body)

    # Wrap Wise CTA lines in wise-note div
    body_html = re.sub(
        r'<p>(Wise (?:is currently|actualmente)[^<]*<a href="https://wise\.prf\.hn[^<]*</a>)</p>',
        r'<div class="wise-note"><p>\1</p></div>',
        body_html
    )

    # Wrap Faro CTA paragraph
    body_html = re.sub(
        r'<p>(<strong>(?:Want real-time|¿Quieres comparar)[^<]*</strong>.*?)</p>',
        r'<div class="cta-box"><p>\1</p></div>',
        body_html
    )

    tag_label = "Guía" if lang == "es" else "Guide"

    page = HTML_HEAD.replace("{lang}", lang_attr).replace("{title}", html.escape(title)).replace("{desc}", html.escape(desc))
    page += f"""<body>
{NAVBAR_HTML}
<main>
  <div class="container">
    <nav class="breadcrumb">
      <a href="/blog/">Blog</a><span>›</span>{html.escape(title[:60])}{"…" if len(title) > 60 else ""}
    </nav>
    <header class="article-header">
      <div class="article-tag">{tag_label}</div>
      <h1>{html.escape(title)}</h1>
      <p class="article-meta">Faro · {updated}</p>
    </header>
    <article class="article-body">
      {body_html}
    </article>
  </div>
</main>
{FOOTER_HTML}
</body>
</html>"""
    return page


# ── Article metadata for blog index ─────────────────────────────────────────
ARTICLES = [
    {
        "file": "cheapest-ways-send-money-honduras.md",
        "slug": "cheapest-ways-send-money-honduras",
        "lang": "en",
    },
    {
        "file": "cost-send-money-honduras.md",
        "slug": "cost-send-money-honduras",
        "lang": "en",
    },
    {
        "file": "cuanto-cuesta-enviar-dinero-honduras.md",
        "slug": "cuanto-cuesta-enviar-dinero-honduras",
        "lang": "es",
    },
    {
        "file": "formas-baratas-enviar-dinero-honduras.md",
        "slug": "formas-baratas-enviar-dinero-honduras",
        "lang": "es",
    },
    {
        "file": "remitly-vs-western-union-honduras-en.md",
        "slug": "remitly-vs-western-union-honduras-en",
        "lang": "en",
    },
    {
        "file": "remitly-vs-western-union-honduras.md",
        "slug": "remitly-vs-western-union-honduras",
        "lang": "es",
    },
    {
        "file": "worldremit-honduras-en.md",
        "slug": "worldremit-honduras-en",
        "lang": "en",
    },
    {
        "file": "worldremit-honduras.md",
        "slug": "worldremit-honduras",
        "lang": "es",
    },
]


def build_blog_index(articles_meta):
    """Build the /blog/index.html listing page."""
    cards = ""
    for a in articles_meta:
        lang_badge = "🇺🇸 EN" if a["lang"] == "en" else "🇭🇳 ES"
        cards += f"""
    <article class="blog-card">
      <div class="card-inner">
        <div class="card-meta">
          <span class="lang-badge">{lang_badge}</span>
          <span class="card-date">{a.get("updated", "Abril 2026")}</span>
        </div>
        <h2 class="card-title"><a href="/blog/{a["slug"]}/">{html.escape(a["title"])}</a></h2>
        <p class="card-desc">{html.escape(a["meta_description"])}</p>
        <a href="/blog/{a["slug"]}/" class="card-link">Leer más →</a>
      </div>
    </article>"""

    index_css = SHARED_CSS + """
    .blog-hero {
      background: linear-gradient(135deg, var(--teal) 0%, var(--teal-dark) 100%);
      color: #fff; padding: 56px 24px 48px; text-align: center;
    }
    .blog-hero h1 {
      font-size: clamp(1.8rem, 5vw, 2.8rem); font-weight: 800; margin-bottom: 14px;
    }
    .blog-hero p { font-size: 1.1rem; opacity: 0.88; max-width: 520px; margin: 0 auto; }
    .blog-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 24px; padding: 48px 0;
    }
    .blog-card {
      border: 1px solid #daeaea; border-radius: var(--radius);
      overflow: hidden; transition: box-shadow 0.2s, transform 0.2s;
      background: #fff;
    }
    .blog-card:hover { box-shadow: var(--shadow); transform: translateY(-2px); }
    .card-inner { padding: 24px; display: flex; flex-direction: column; height: 100%; }
    .card-meta { display:flex; align-items:center; gap:10px; margin-bottom:10px; }
    .lang-badge {
      font-size: 0.75rem; font-weight: 700; background: var(--teal-light);
      color: var(--teal); padding: 3px 10px; border-radius: 50px;
    }
    .card-date { font-size: 0.8rem; color: var(--text-muted); }
    .card-title {
      font-size: 1.05rem; font-weight: 700; color: var(--navy);
      margin-bottom: 10px; line-height: 1.3;
    }
    .card-title a { text-decoration: none; color: var(--navy); }
    .card-title a:hover { color: var(--teal); }
    .card-desc { font-size: 0.875rem; color: var(--text-muted); flex: 1; margin-bottom: 16px; }
    .card-link {
      font-size: 0.875rem; font-weight: 600; color: var(--teal);
      text-decoration: none; align-self: flex-start;
    }
    .card-link:hover { text-decoration: underline; }
    @media (max-width: 600px) {
      .blog-grid { grid-template-columns: 1fr; }
    }
    """

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Blog — Guías de envío de dinero a Honduras | Faro</title>
  <meta name="description" content="Guías actualizadas para enviar dinero a Honduras: comparativas de precios, tasas de cambio, y cómo ahorrar en cada transferencia." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
  <style>
  {index_css}
  </style>
</head>
<body>
{NAVBAR_HTML}
<section class="blog-hero">
  <h1>Blog Faro</h1>
  <p>Guías honestas para enviar dinero a Honduras. Sin letra chica.</p>
</section>
<main>
  <div class="container">
    <div class="blog-grid">
      {cards}
    </div>
  </div>
</main>
{FOOTER_HTML}
</body>
</html>"""


# ── Main build ───────────────────────────────────────────────────────────────
def main():
    os.makedirs(BLOG_DIR, exist_ok=True)
    articles_meta = []

    for a in ARTICLES:
        path = os.path.join(CONTENT_DIR, a["file"])
        with open(path, encoding="utf-8") as f:
            text = f.read()

        meta, body = parse_frontmatter(text)
        meta.update(a)  # ensure slug/lang from our list

        # Build article page
        page_html = build_article_page(meta, body, a["lang"])
        out_dir = os.path.join(BLOG_DIR, a["slug"])
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"✅ {a['slug']}/index.html")

        articles_meta.append(meta)

    # Build blog index
    index_html = build_blog_index(articles_meta)
    with open(os.path.join(BLOG_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("✅ blog/index.html")
    print("Done!")


if __name__ == "__main__":
    main()
