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
from scripts.lib.text import safe_url


def _esc(s) -> str:
    return html.escape(s if s is not None else "")


# Valores válidos de tema (los que implementa theme.css). Cualquier otro → default:
# evita inyección de atributos HTML vía `style`/`palette` del config (XSS).
_VALID_STYLES = {"editorial", "modern", "technical", "magazine", "minimal", "newsprint"}
_VALID_PALETTES = {"ink", "warm", "cool", "forest", "signal"}


def _og_locale(site: dict) -> str:
    """Locale OpenGraph desde site.locale (override xx_YY) o derivado de site.language de forma
    HONESTA: 'es-ES'→'es_ES'; 'es'→'es' (sin inventar región)."""
    override = (site.get("locale") or "").strip()
    if override:
        return override
    parts = (site.get("language") or "").replace("_", "-").split("-")
    if not parts or not parts[0]:
        return ""
    loc = parts[0].lower()
    if len(parts) > 1 and parts[1]:
        loc += "_" + parts[1].upper()
    return loc


def _og_image_url(site: dict, base: str) -> str:
    """URL absoluta de la og:image ESTÁTICA que aporta el operador (site.og_image.mode='static').
    Rechaza .svg (los sociales lo ignoran como og:image: sería una promesa falsa)."""
    og = site.get("og_image") or {}
    if og.get("mode") != "static":
        return ""
    path = (og.get("path") or "").strip()
    if not path or path.lower().endswith(".svg"):
        return ""
    if path.startswith(("http://", "https://")):
        return safe_url(path)
    if not base:
        return ""
    return base + (path if path.startswith("/") else "/" + path)


def _og(title: str, description: str, url: str, site: dict, og_type: str) -> str:
    """Open Graph + Twitter cards + og:locale + og:image estática (compartir en redes)."""
    base = (site.get("domain") or "").rstrip("/")
    tags = [("og:title", title), ("og:description", description), ("og:type", og_type),
            ("og:url", url), ("og:site_name", site.get("name", "")),
            ("og:locale", _og_locale(site))]
    img = _og_image_url(site, base)
    if img:
        tags.append(("og:image", img))
    out = "".join(f'<meta property="{p}" content="{_esc(c)}">\n' for p, c in tags if c)
    # Twitter cards SIEMPRE: mejora el preview aunque no haya imagen (solo-texto → summary).
    tw = [("twitter:card", "summary_large_image" if img else "summary"),
          ("twitter:title", title), ("twitter:description", description)]
    if img:
        tw.append(("twitter:image", img))
    out += "".join(f'<meta name="{n}" content="{_esc(c)}">\n' for n, c in tw if c)
    return out


def _jsonld_edition(edition: dict, site: dict, url: str) -> str:
    """Datos estructurados Schema.org (NewsArticle + BreadcrumbList) — solo con datos REALES
    (nada inventado): inLanguage, publisher/author con url y logo (si lo aporta el operador),
    y sameAs solo si config.site.same_as trae URLs http/https propias."""
    from scripts.lib.i18n import base_lang
    cov = edition.get("cover", {})
    name = site.get("name", "")
    domain = safe_url((site.get("domain") or "").rstrip("/")) or ""
    publisher = {"@type": "Organization", "name": name}
    if domain:
        publisher["url"] = domain
    logo = safe_url(site.get("logo", ""))
    if logo:
        publisher["logo"] = {"@type": "ImageObject", "url": logo}
    same_as = [u for u in (site.get("same_as") or []) if safe_url(u)]
    if same_as:
        publisher["sameAs"] = same_as
    author = {"@type": "Organization", "name": name}
    if domain:
        author["url"] = domain
    data = {
        "@context": "https://schema.org", "@type": "NewsArticle",
        "headline": cov.get("headline", ""),
        "description": (cov.get("deck") or "")[:200],
        "inLanguage": base_lang(site.get("language", "es")),
        "datePublished": edition.get("date", ""),
        "dateModified": edition.get("date", ""),
        "url": url,
        "publisher": publisher,
        "author": author,
        "isAccessibleForFree": True,
    }
    # BreadcrumbList (home › edición) como 2º bloque: navegación estructurada para Google.
    crumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": name, "item": domain + "/" if domain else "/"},
            {"@type": "ListItem", "position": 2, "name": cov.get("headline", ""), "item": url},
        ],
    }
    def _script(d):
        # `<` escapado para no poder romper el <script> desde el contenido.
        return ('<script type="application/ld+json">'
                + json.dumps(d, ensure_ascii=False).replace("<", "\\u003c") + "</script>\n")
    return _script(data) + _script(crumb)


def _topbar(site: dict, active: str, lang: str = "es") -> str:
    def link(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cur}>{_esc(label)}</a>'
    return (
        '  <header class="topbar">\n'
        f'    <a class="brand" href="/">{_esc(site.get("name", ""))}</a>\n'
        f'    <nav>{link("/", t(lang, "nav_latest"), "home")}'
        f'{link("/archive.html", t(lang, "nav_archive"), "archive")}'
        f'{link("/methodology.html", t(lang, "nav_method"), "method")}'
        f'{link("/about.html", t(lang, "nav_about"), "about")}'
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


def _edition_nav(prev_href: str, next_href: str, lang: str) -> str:
    """Navegación entre ediciones (prev=más antigua, next=más nueva). Enlazado interno
    determinista, 0 páginas nuevas."""
    if not (prev_href or next_href):
        return ""
    left = (f'<a rel="prev" href="{_esc(prev_href)}">{_esc(t(lang, "nav_prev"))}</a>'
            if prev_href else "<span></span>")
    right = (f'<a rel="next" href="{_esc(next_href)}">{_esc(t(lang, "nav_next"))}</a>'
             if next_href else "<span></span>")
    return f'  <nav class="edition-nav">{left}{right}</nav>\n'


def render_edition_page(edition: dict, *, canonical: str, config: dict, css: str,
                        indexable: bool = False, prev_href: str = "", next_href: str = "") -> str:
    site = config.get("site", {})
    cov = edition.get("cover", {})
    name = site.get("name", "")
    headline = (cov.get("headline") or "").strip()
    # <title> con el TITULAR (keywords reales en la SERP), no solo nombre·fecha.
    title = (f"{headline} · {name}" if headline else f"{name} · {edition.get('date', '')}")[:65]
    desc = (cov.get("deck") or "")[:155]
    lang = site.get("language", "es")
    newsletter = bool(config.get("newsletter", {}).get("enabled", False))
    curator = config.get("editorial", {}).get("curator", "")
    linkrel = ""
    if prev_href:
        linkrel += f'<link rel="prev" href="{_esc(prev_href)}">\n'
    if next_href:
        linkrel += f'<link rel="next" href="{_esc(next_href)}">\n'
    extra = (_og(title, desc, canonical, site, "article")
             + _jsonld_edition(edition, site, canonical) + linkrel)
    content = (edition_inner(edition, lang, newsletter, curator)
               + _edition_nav(prev_href, next_href, lang))
    return render_page(content, title=title, description=desc, canonical=canonical,
                       config=config, css=css, active="home", indexable=indexable,
                       extra_head=extra)


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


def render_robots(base: str, indexable: bool) -> str:
    """robots.txt: en producción invita a rastrear y apunta al sitemap; en preview lo bloquea
    entero (refuerza el review-first: los borradores no se rastrean por vía canónica)."""
    if not indexable:
        return "User-agent: *\nDisallow: /\n"
    lines = ["User-agent: *", "Allow: /"]
    if base:
        lines.append(f"Sitemap: {base}/sitemap.xml")
    return "\n".join(lines) + "\n"


# ===== Páginas E-E-A-T (deterministas, desde el config; señal de confianza para Google) =====

def _page_section(heading: str, inner_html: str) -> str:
    return (f'  <section class="page">\n    <h1>{_esc(heading)}</h1>\n{inner_html}\n  </section>\n')


def render_static_page(*, body: str, title: str, description: str, canonical: str,
                       config: dict, css: str, active: str, indexable: bool = False) -> str:
    site = config.get("site", {})
    extra = _og(title, description, canonical, site, "website")
    return render_page(body, title=title, description=description, canonical=canonical,
                       config=config, css=css, active=active, indexable=indexable, extra_head=extra)


def about_content(config: dict, lang: str):
    """(title, description, body) de /about.html desde config (tagline, curador, contacto)."""
    site = config.get("site", {})
    ed = config.get("editorial", {})
    name = site.get("name", "")
    parts = []
    if site.get("tagline"):
        parts.append(f'<p>{_esc(site["tagline"])}</p>')
    if ed.get("curator"):
        parts.append(f'<p>{_esc(t(lang, "byline_curated"))} <strong>{_esc(ed["curator"])}</strong>.</p>')
    if ed.get("contact_email"):
        parts.append(f'<p><a href="mailto:{_esc(ed["contact_email"])}">{_esc(ed["contact_email"])}</a></p>')
    parts.append(f'<p>{_esc(t(lang, "method_ai"))} '
                 f'<a href="/methodology.html">{_esc(t(lang, "nav_method"))}</a>.</p>')
    body = _page_section(t(lang, "about_heading"), "    " + "\n    ".join(parts))
    return (f'{t(lang, "about_heading")} · {name}',
            (site.get("tagline") or t(lang, "about_heading"))[:155], body)


def methodology_content(config: dict, lang: str):
    """(title, description, body) de /methodology.html: alcance honesto, IA, cadencia, riesgo."""
    site = config.get("site", {})
    ed = config.get("editorial", {})
    name = site.get("name", "")
    risk = config.get("risk_profile", "review")
    risk_key = {"auto": "risk_auto", "review": "risk_review", "strict": "risk_strict"}.get(risk, "risk_review")
    cadence = ed.get("cadence") or t(lang, "cadence_weekly")
    corrections = ed.get("corrections") or t(lang, "method_corrections")
    rows = [
        f'<p>{_esc(t(lang, "method_scope"))}</p>',
        f'<p>{_esc(t(lang, "method_ai"))}</p>',
        f'<p><strong>{_esc(t(lang, "method_cadence"))}:</strong> {_esc(cadence)}</p>',
        f'<p><strong>{_esc(t(lang, "method_risk"))}:</strong> {_esc(t(lang, risk_key))}</p>',
        f'<p>{_esc(corrections)}</p>',
        f'<p>{_esc(t(lang, "method_sources_intro"))} '
        f'<a href="/sources.html">{_esc(t(lang, "nav_sources"))}</a>.</p>',
    ]
    body = _page_section(t(lang, "method_heading"), "    " + "\n    ".join(rows))
    return (f'{t(lang, "method_heading")} · {name}', t(lang, "method_scope")[:155], body)


def sources_content(config: dict, lang: str):
    """(title, description, body) de /sources.html: los feeds del config, con su dominio."""
    from scripts.lib.text import registrable_domain, safe_url
    site = config.get("site", {})
    name = site.get("name", "")
    lis = []
    for s in config.get("sources", []):
        url = safe_url(s.get("url", ""))
        dom = registrable_domain(url)
        label = s.get("name") or dom or url
        if url:
            lis.append(f'<li><a href="{_esc(url)}" rel="noopener nofollow">{_esc(label)}</a> '
                       f'<span class="src">{_esc(dom)}</span></li>')
        else:
            lis.append(f'<li>{_esc(label)}</li>')
    inner = (f'    <p>{_esc(t(lang, "method_sources_intro"))}</p>\n'
             f'    <ul class="sources">\n      ' + "\n      ".join(lis) + "\n    </ul>")
    body = _page_section(t(lang, "sources_heading"), inner)
    return (f'{t(lang, "sources_heading")} · {name}', t(lang, "method_sources_intro")[:155], body)


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
