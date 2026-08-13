"""Deduplicación determinista: URL canónica + similitud difusa de títulos.

Con MEMORIA de procedencia: cuando dos ítems son el mismo hecho, en vez de
tirar el duplicado se **adjunta como fuente adicional** (`merged`) del ítem que
se conserva. Así una historia puede citar varias fuentes (mismo hecho contado
por varios medios → varias fuentes). Habilita las citas numeradas y el
guardarraíl de ≥2 fuentes independientes.
"""
from __future__ import annotations
from difflib import SequenceMatcher
from scripts.lib.text import canonical_url


def _title_sim(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").lower(), (b or "").lower()).ratio()


def dedupe(items, threshold: float = 0.82):
    kept, by_url = [], {}
    for it in items:
        cu = canonical_url(it.get("url", ""))
        dup = by_url.get(cu) if cu else None
        if dup is None:
            for k in kept:
                if _title_sim(it.get("title", ""), k.get("title", "")) >= threshold:
                    dup = k
                    break
        if dup is not None:
            dup.setdefault("merged", []).append({
                "id": it.get("id"), "url": it.get("url"),
                "source_name": it.get("source_name"), "title": it.get("title"),
                "summary": it.get("summary", ""),   # evidencia de la fuente secundaria
            })
            continue
        kept.append(it)
        if cu:
            by_url[cu] = it
    return kept
