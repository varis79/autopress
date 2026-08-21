"""publish — genera el sitio estático navegable a partir de TODAS las ediciones.

"Git como base de datos": cada edición publicada se guarda como JSON en el almacén
(`data/editions/<slug>.json`, versionado en el repo). El sitio se reconstruye entero
desde ese almacén, así que el archivo, el RSS y el sitemap **acumulan el histórico**
(no solo la última edición).

Escribe: index.html (home = última edición), magazines/<slug>.html (permalink de cada
edición), archive.html, sitemap.xml, rss.xml. Aplica el theme de config.site.theme.
"""
from __future__ import annotations
import json
import os
import shutil

from scripts.lib.site import (
    render_edition_page, render_archive_page, render_sitemap, render_rss,
    render_robots, render_static_page, about_content, methodology_content, sources_content,
)
from scripts import legal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # starter/


def _write(path: str, content: str):
    """Escritura ATÓMICA: escribe a un temporal y reemplaza (evita ficheros a medias)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp, path)


def _slug(edition: dict) -> str:
    return f"{edition.get('date', '')}-edicion"


def _load_store(store_dir: str) -> list:
    """Todas las ediciones guardadas (una por fichero JSON)."""
    if not store_dir or not os.path.isdir(store_dir):
        return []
    out = []
    for name in os.listdir(store_dir):
        if name.endswith(".json"):
            try:
                with open(os.path.join(store_dir, name), encoding="utf-8") as f:
                    out.append(json.load(f))
            except Exception:
                continue
    return out


def _meta(edition: dict, site: dict) -> dict:
    return {"title": f'{site.get("name", "")} · {edition.get("date", "")}',
            "date": edition.get("date", ""),
            "url": f"/magazines/{_slug(edition)}.html",
            "description": (edition.get("cover", {}).get("deck") or "")[:155]}


def _indexable(edition: dict, production: bool) -> bool:
    """Una edición se indexa SOLO si es producción, está 'approved' y no es stub.
    (Los previews locales y las ediciones needs_review/stub nacen noindex.)"""
    return bool(production) and edition.get("status") == "approved" and not edition.get("stub")


def publish(edition: dict, config: dict, out_dir: str, production: bool = False,
            store_dir: str = None, persist: bool = False) -> dict:
    site = config.get("site", {})
    base = site.get("domain", "").rstrip("/")

    with open(os.path.join(ROOT, "theme", "theme.css"), encoding="utf-8") as f:
        css = f.read()

    # Enlaces legales para el footer (según qué plantillas existen, en el idioma del sitio).
    config["_legal_links"] = legal.links_for(ROOT, site.get("language", "es"))

    # 1. Persistir la edición actual en el almacén (solo cuando se publica de verdad).
    if store_dir and persist:
        _write(os.path.join(store_dir, f"{_slug(edition)}.json"),
               json.dumps(edition, ensure_ascii=False, indent=2))

    # 2. Cargar el histórico y unir la edición actual (que manda, por contenido fresco).
    by_slug = {_slug(e): e for e in _load_store(store_dir)}
    by_slug[_slug(edition)] = edition
    all_eds = sorted(by_slug.values(), key=lambda e: e.get("date", ""), reverse=True)

    # 3. Permalink de cada edición (indexable según SU estado). Se LIMPIA magazines/ antes,
    #    así una edición retirada del store desaparece del sitio (no quedan huérfanas).
    shutil.rmtree(os.path.join(out_dir, "magazines"), ignore_errors=True)
    n = len(all_eds)
    for i, e in enumerate(all_eds):
        url = f"/magazines/{_slug(e)}.html"
        # all_eds va de más nueva a más antigua: prev = la más antigua (i+1), next = la más nueva (i-1).
        prev_href = f"/magazines/{_slug(all_eds[i + 1])}.html" if i + 1 < n else ""
        next_href = f"/magazines/{_slug(all_eds[i - 1])}.html" if i > 0 else ""
        _write(os.path.join(out_dir, "magazines", f"{_slug(e)}.html"),
               render_edition_page(e, canonical=base + url, config=config, css=css,
                                   indexable=_indexable(e, production),
                                   prev_href=prev_href, next_href=next_href))

    # 4. Home = edición más reciente (su 'anterior' es la 2ª más nueva; no tiene 'siguiente').
    home = all_eds[0]
    home_prev = f"/magazines/{_slug(all_eds[1])}.html" if n > 1 else ""
    _write(os.path.join(out_dir, "index.html"),
           render_edition_page(home, canonical=base + "/", config=config, css=css,
                               indexable=_indexable(home, production), prev_href=home_prev))

    # 5. Archivo (índice; noindex salvo que se decida indexar el índice).
    metas = [_meta(e, site) for e in all_eds]
    _write(os.path.join(out_dir, "archive.html"),
           render_archive_page(metas, canonical=base + "/archive.html", config=config,
                               css=css, indexable=False))

    # 5b. Páginas E-E-A-T (evergreen; deterministas desde config). URLs estables (i18n en el
    #     texto, no en la ruta); indexables en producción como señal de confianza para Google.
    lang = site.get("language", "es")
    eeat_pages = [
        ("about.html", "about", about_content(config, lang)),
        ("methodology.html", "method", methodology_content(config, lang)),
        ("sources.html", "sources", sources_content(config, lang)),
    ]
    for fname, active, (ptitle, pdesc, pbody) in eeat_pages:
        _write(os.path.join(out_dir, fname),
               render_static_page(body=pbody, title=ptitle, description=pdesc,
                                  canonical=f"{base}/{fname}", config=config, css=css,
                                  active=active, indexable=production))

    # 5c. robots.txt: producción invita a rastrear + apunta al sitemap; preview lo bloquea todo.
    _write(os.path.join(out_dir, "robots.txt"), render_robots(base, production))

    # 6. Sitemap SOLO con páginas approved & indexables (nada de borradores noindex).
    indexable_eds = [e for e in all_eds if _indexable(e, production)]
    entries = []
    if indexable_eds:
        latest = indexable_eds[0].get("date", "")
        entries = ([("/", latest)]
                   + [(f"/magazines/{_slug(e)}.html", e.get("date", "")) for e in indexable_eds])
    if production:   # las páginas E-E-A-T son evergreen: al sitemap aunque no haya edición approved
        entries += [("/about.html", None), ("/methodology.html", None), ("/sources.html", None)]
    _write(os.path.join(out_dir, "sitemap.xml"), render_sitemap(base, entries))

    # 7. RSS: SOLO ediciones aprobadas (un borrador needs_review no es público).
    approved_metas = [_meta(e, site) for e in all_eds if e.get("status") == "approved"]
    _write(os.path.join(out_dir, "rss.xml"), render_rss(base, approved_metas, site))

    # 8. Páginas legales (las plantillas rellenadas) con el theme del sitio.
    legal.render(ROOT, config, css, out_dir, indexable=production)

    return {"out_dir": out_dir, "edition_url": f"/magazines/{_slug(edition)}.html",
            "editions_total": len(all_eds), "indexable_total": len(indexable_eds),
            "files": ["index.html", f"magazines/{_slug(edition)}.html", "archive.html",
                      "about.html", "methodology.html", "sources.html",
                      "robots.txt", "sitemap.xml", "rss.xml"]}
