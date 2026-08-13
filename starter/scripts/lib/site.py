"""Render de las páginas del sitio (home, permalink, archivo) + sitemap + rss.

El theme (estilo + paleta) se toma de config.site.theme y se aplica en el
elemento raíz. El CSS va inline por página (autocontenida). En producción el
agente puede enlazar un fichero compartido; aquí se inlinea para simplicidad.
"""
from __future__ import annotations
import html
import json

from scripts.lib.templating import edition_inner, _footer_html
from scripts.lib.i18n import t


def _esc(s) -> str:
    return html.escape(s if s is not None else "")


# Valores válidos de tema (los que implementa theme.css). Cualquier otro → default:
# evita inyección de atributos HTML vía `style`/`palette` del config (XSS).
_VALID_STYLES = {"editorial", "modern", "technical", "magazine", "minimal", "newsprint"}
_VALID_PALETTES = {"ink", "warm", "cool", "forest", "signal"}


def _og(title: str, description: str, url: str, site: dict, og_type: str) -> str:
    """Etiquetas Open Graph (compartir en redes/mensajería)."""
    tags = [("og:title", title), ("og:description", description), ("og:type", og_type),
            ("og:url", url), ("og:site_name", site.get("name", ""))]
    return "".join(f'<meta property="{p}" content="{_esc(c)}">\n' for p, c in tags if c)


def _jsonld_edition(edition: dict, site: dict, url: str) -> str:
    """Datos estructurados Schema.org (NewsArticle) — con divulgación de autoría."""
    cov = edition.get("cover", {})
    data = {
        "@context": "https://schema.org", "@type": "NewsArticle",
        "headline": cov.get("headline", ""),
        "description": (cov.get("deck") or "")[:200],
        "datePublished": edition.get("date", ""),
        "dateModified": edition.get("date", ""),
        "url": url,
        "publisher": {"@type": "Organization", "name": site.get("name", "")},
        "author": {"@type": "Organization", "name": site.get("name", "")},
        "isAccessibleForFree": True,
    }
    # `<` escapado para no poder romper el <script> desde el contenido.
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    return f'<script type="application/ld+json">{payload}</script>\n'


def _topbar(site: dict, active: str, lang: str = "es") -> str:
    def link(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cur}>{_esc(label)}</a>'
    return (
        '  <header class="topbar">\n'
        f'    <a class="brand" href="/">{_esc(site.get("name", ""))}</a>\n'
        f'    <nav>{link("/", t(lang, "nav_latest"), "home")}'
        f'{link("/archive.html", t(lang, "nav_archive"), "archive")}'
        '<a href="/rss.xml">RSS</a></nav>\n'
        "  </header>\n"
    )


def render_page(content: str, *, title: str, description: str, canonical: str,
                config: dict, css: str, active: str, indexable: bool = False,
                extra_head: str = "") -> str:
    site = config.get("site", {})
    theme = site.get("theme", {})
    style = theme.get("style", "editorial")
    style = style if style in _VALID_STYLES else "editorial"
    palette = theme.get("palette", "warm")
    palette = palette if palette in _VALID_PALETTES else "warm"
    lang = site.get("language", "es")
    # noindex por defecto: solo la publicación de producción (real, sin stub y con QA
    # en verde) pide index. Cualquier preview/borrador nace noindex.
    robots = ("index, follow, max-snippet:-1, max-image-preview:large" if indexable
              else "noindex, nofollow")
    head = (
        "<!doctype html>\n"
        f'<html lang="{_esc(lang)}" data-style="{style}" data-palette="{palette}" data-theme="light">\n'
        "<head>\n<meta charset=\"utf-8\">\n"
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<meta name="robots" content="{robots}">\n'
        f"<title>{_esc(title)}</title>\n"
        f'<meta name="description" content="{_esc(description)}">\n'
        f'<link rel="canonical" href="{_esc(canonical)}">\n'
        '<link rel="alternate" type="application/rss+xml" href="/rss.xml">\n'
        + extra_head
        + f"<style>\n{css}\n</style>\n</head>\n<body>\n"
    )
    body = ('<div class="wrap">\n' + _topbar(site, active, lang) + content + "\n"
            + _footer_html(lang, config) + "\n</div>\n")
    return head + body + "</body>\n</html>\n"


def render_edition_page(edition: dict, *, canonical: str, config: dict, css: str,
                        indexable: bool = False) -> str:
    site = config.get("site", {})
    desc = (edition.get("cover", {}).get("deck") or "")[:155]
    title = f'{site.get("name", "")} · {edition.get("date", "")}'
    lang = site.get("language", "es")
    newsletter = bool(config.get("newsletter", {}).get("enabled", False))
    extra = _og(title, desc, canonical, site, "article") + _jsonld_edition(edition, site, canonical)
    return render_page(edition_inner(edition, lang, newsletter), title=title, description=desc,
                       canonical=canonical, config=config, css=css, active="home",
                       indexable=indexable, extra_head=extra)


def render_archive_page(editions: list, *, canonical: str, config: dict, css: str,
                        indexable: bool = False) -> str:
    site = config.get("site", {})
    cards = []
    for e in editions:
        cards.append(
            '<article class="card">\n'
            f'  <h3><a href="{_esc(e["url"])}">{_esc(e["title"])}</a></h3>\n'
            f'  <div class="meta"><span class="tag">{_esc(e["date"])}</span>'
            f'<span class="src">{_esc(e.get("description", ""))}</span></div>\n'
            "</article>"
        )
    lang = site.get("language", "es")
    body = (
        f'  <section class="cover">\n    <h2>{_esc(t(lang, "archive_heading"))}</h2>\n'
        f'    <p>{_esc(t(lang, "archive_intro"))}</p>\n  </section>\n'
        '  <div class="stories">\n    ' + "\n    ".join(cards) + "\n  </div>"
    )
    title = f'{t(lang, "archive_heading")} · {site.get("name", "")}'
    desc = t(lang, "archive_desc")
    extra = _og(title, desc, canonical, site, "website")
    return render_page(body, title=title,
                       description=desc, canonical=canonical,
                       config=config, css=css, active="archive", indexable=indexable,
                       extra_head=extra)


def render_sitemap(base: str, entries: list) -> str:
    """`entries`: cada elemento es una ruta (str) o `(ruta, lastmod)` (fecha ISO)."""
    rows = ""
    for e in entries:
        path, lastmod = (e if isinstance(e, (list, tuple)) else (e, None))
        lm = f"<lastmod>{_esc(lastmod)}</lastmod>" if lastmod else ""
        rows += f"  <url><loc>{_esc(base + path)}</loc>{lm}</url>\n"
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + rows + "</urlset>\n")


def render_rss(base: str, editions: list, site: dict) -> str:
    items = ""
    for e in editions:
        loc = base + e["url"]
        items += (
            "  <item>\n"
            f"    <title>{_esc(e['title'])}</title>\n"
            f"    <link>{_esc(loc)}</link>\n"
            f"    <guid>{_esc(loc)}</guid>\n"
            f"    <description>{_esc(e.get('description', ''))}</description>\n"
            "  </item>\n"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0"><channel>\n'
        f'  <title>{_esc(site.get("name", ""))}</title>\n'
        f'  <link>{_esc(base + "/")}</link>\n'
        f'  <description>{_esc(site.get("tagline", ""))}</description>\n'
        + items + "</channel></rss>\n"
    )
