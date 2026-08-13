"""legal — renderiza las páginas legales y detecta placeholders sin rellenar.

Las plantillas viven en `legal/*.md` (con `<PLACEHOLDER>`). El operador (o su agente) las
rellena. Este módulo:
- `pending(root)` → plantillas que AÚN tienen placeholders (el pipeline no publica en
  producción si quedan: un medio público necesita su legal de verdad).
- `render(...)` → convierte las rellenadas a `/legal/*.html` con el theme del sitio y
  devuelve los enlaces para el footer.
"""
from __future__ import annotations
import html
import os
import re

from scripts.lib.site import render_page
from scripts.lib.text import safe_url
from scripts.lib.i18n import base_lang

# Enlaces entre plantillas legales → su página renderizada.
_LEGAL_MD_HTML = {"privacidad.md": "privacidad.html", "divulgacion-ia.md": "ia.html",
                  "derechos-fuentes.md": "fuentes.html", "terminos.md": "terminos.html"}


def _href(url: str) -> str:
    """Href seguro para enlaces del Markdown legal: mapea hermanos .md→.html, permite
    http/https (vía safe_url) y rutas relativas; neutraliza esquemas activos (javascript:…)."""
    if url in _LEGAL_MD_HTML:
        return _LEGAL_MD_HTML[url]
    if url.startswith(("http://", "https://")):
        return safe_url(url) or "#"
    if url.startswith(("#", "/")) or url.endswith(".html"):
        return url
    return "#"

# (fichero en legal/,  slug de la url,  etiqueta del footer ES)
LEGAL = [
    ("privacidad", "privacidad", "Privacidad"),
    ("divulgacion-ia", "ia", "IA"),
    ("derechos-fuentes", "fuentes", "Fuentes"),
    ("terminos", "terminos", "Términos"),
]

# Etiquetas del footer por idioma (slug → label).
_LABELS_I18N = {
    "en": {"privacidad": "Privacy", "ia": "AI", "fuentes": "Sources", "terminos": "Terms"},
}


def _label(slug: str, default: str, lang: str) -> str:
    return _LABELS_I18N.get(base_lang(lang), {}).get(slug, default)

_PLACEHOLDER = re.compile(r"<[A-ZÁÉÍÓÚÑ][^>\n]*>")   # <NOMBRE_MEDIO>, <FECHA, …>, …


def _has_placeholders(text: str) -> bool:
    return bool(_PLACEHOLDER.search(text or ""))


def _src(root: str, name: str, lang: str) -> str:
    """Ruta de la plantilla legal para el idioma: `legal/<lang>/<name>.md` si existe,
    si no `legal/<name>.md` (la de por defecto/ES)."""
    localized = os.path.join(root, "legal", base_lang(lang), f"{name}.md")
    return localized if os.path.exists(localized) else os.path.join(root, "legal", f"{name}.md")


def pending(root: str, lang: str = "es") -> list:
    """Plantillas legales (del idioma) que todavía tienen placeholders sin rellenar."""
    out = []
    for name, _slug, _label in LEGAL:
        path = _src(root, name, lang)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                if _has_placeholders(f.read()):
                    out.append(name)
    return out


def _inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
               lambda m: f'<a href="{html.escape(_href(m.group(2)))}" rel="noopener">{m.group(1)}</a>', s)
    return s


def md_to_html(md: str) -> str:
    """Conversor Markdown mínimo (títulos, párrafos, listas, cita, negrita, enlaces)."""
    out, ul, para = [], [], []

    def flush_para():
        if para:
            out.append("<p>" + " ".join(_inline(x) for x in para) + "</p>")
            para.clear()

    def flush_ul():
        if ul:
            out.append("<ul>" + "".join(f"<li>{_inline(x)}</li>" for x in ul) + "</ul>")
            ul.clear()

    for raw in (md or "").splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush_para(); flush_ul(); continue
        if line.startswith("### "):
            flush_para(); flush_ul(); out.append(f"<h3>{_inline(line[4:])}</h3>")
        elif line.startswith("## "):
            flush_para(); flush_ul(); out.append(f"<h2>{_inline(line[3:])}</h2>")
        elif line.startswith("# "):
            flush_para(); flush_ul(); out.append(f"<h1>{_inline(line[2:])}</h1>")
        elif line.startswith("> "):
            flush_para(); flush_ul(); out.append(f"<blockquote>{_inline(line[2:])}</blockquote>")
        elif line.lstrip().startswith(("- ", "* ")):
            flush_para(); ul.append(line.lstrip()[2:])
        else:
            flush_ul(); para.append(line.strip())
    flush_para(); flush_ul()
    return "\n".join(out)


def links_for(root: str, lang: str = "es") -> list:
    """(label, href) de las páginas legales existentes, para el footer."""
    out = []
    for name, slug, label in LEGAL:
        if os.path.exists(_src(root, name, lang)):
            out.append((_label(slug, label, lang), f"/legal/{slug}.html"))
    return out


def render(root: str, config: dict, css: str, out_dir: str, indexable: bool = False) -> list:
    """Renderiza las páginas legales (del idioma del sitio) a out_dir/legal/*.html."""
    site = config.get("site", {})
    base = site.get("domain", "").rstrip("/")
    lang = site.get("language", "es")
    links = []
    for name, slug, label in LEGAL:
        src = _src(root, name, lang)
        if not os.path.exists(src):
            continue
        with open(src, encoding="utf-8") as f:
            body = md_to_html(f.read())
        canonical = f"{base}/legal/{slug}.html"
        label = _label(slug, label, lang)
        html_page = render_page(f'<article class="legal">{body}</article>',
                                title=f'{label} · {site.get("name", "")}',
                                description=label, canonical=canonical, config=config,
                                css=css, active="", indexable=indexable)
        path = os.path.join(out_dir, "legal", f"{slug}.html")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_page)
        links.append((label, f"/legal/{slug}.html"))
    return links
