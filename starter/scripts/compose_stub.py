"""compose_stub — construye una 'edición' desde la selección SIN LLM.

Modo stub: no gasta API. Usa el título/resumen originales y resuelve las
**fuentes numeradas** de forma determinista desde el ítem y sus duplicados
fusionados (`merged`). La atribución NO la inventa un modelo: se copia del
registro validado (diseño de procedencia). La edición va marcada `stub=True`.
"""
from __future__ import annotations
from urllib.parse import urlsplit

from scripts.lib.text import canonical_url, safe_url


def _source_name(url: str) -> str:
    try:
        host = urlsplit(url).netloc.lower()
        return host[4:] if host.startswith("www.") else host
    except Exception:
        return "fuente"


def _evidence_text(item: dict) -> str:
    """Texto fuente de una historia (título + resumen + títulos de duplicados).
    QA lo usa para comprobar que las cifras de la redacción existen en la fuente."""
    parts = [item.get("title", ""), item.get("summary", "")]
    for m in item.get("merged", []):
        parts += [m.get("title", ""), m.get("summary", "")]   # evidencia de las fuentes fusionadas
    return " ".join(p for p in parts if p)


def _sources_for(item: dict) -> list:
    """Fuentes numeradas de una historia: el propio ítem + sus duplicados
    fusionados, deduplicadas por URL canónica. Solo esquemas http/https."""
    raw = [{"url": item.get("url", ""), "id": item.get("id")}]
    for m in item.get("merged", []):
        raw.append({"url": m.get("url", ""), "id": m.get("id")})
    out, seen, n = [], set(), 0
    for s in raw:
        url = safe_url(s["url"])
        cu = canonical_url(url)
        if not url or cu in seen:
            continue
        seen.add(cu)
        n += 1
        out.append({"n": n, "name": _source_name(url), "url": url, "ref_id": s["id"]})
    return out


def compose_stub(selection: dict, by_id: dict, meta: dict) -> dict:
    stories = []
    for s in selection.get("stories", []):
        it = by_id.get(s["id"], {})
        stories.append({
            "headline": it.get("title", ""),
            "summary": it.get("summary", ""),
            "topic": s.get("topic"),
            "market": s.get("market"),
            "sources": _sources_for(it),
            "_evidence": _evidence_text(it),
        })
    cover = stories[0] if stories else {"headline": "", "summary": "", "topic": None,
                                        "sources": [], "_evidence": ""}
    return {
        "title": meta.get("title", "Edición demo"),
        "date": meta.get("date", ""),
        "stub": True,
        "cover": {"headline": cover["headline"], "deck": cover["summary"],
                  "kicker": cover.get("topic"), "sources": cover.get("sources", []),
                  "_evidence": cover.get("_evidence", "")},
        "stories": stories,
    }
