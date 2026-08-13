"""editorial_gate — quality-gate D1: qué edición merece indexarse.

Solo una edición **approved** puede indexarse en producción. Una edición es indexable si:
no es stub, QA no la bloquea, tiene suficientes historias (no thin) y todas citan fuente.
Devuelve un `quality_report` que se guarda junto a la edición (auditable).
"""
from __future__ import annotations

from scripts.qa import qa


def evaluate(edition: dict, config: dict) -> dict:
    checks = []

    def add(name, ok, detail):
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    min_stories = config.get("modes", {}).get("min_normal", 4)
    # Cuenta lo que SE RENDERIZA (portada + tarjetas), no la selección: si el LLM
    # devolvió menos historias, la edición es thin y NO debe indexarse.
    rendered = len(edition.get("stories", []))

    stub = bool(edition.get("stub"))
    add("not_stub", not stub, "no es stub" if not stub else "es stub → nunca indexable")

    qstatus = qa(edition, config)["status"]
    add("qa_ok", qstatus != "blocked", f"qa={qstatus}")

    add("enough_stories", rendered >= min_stories,
        f"{rendered} historias renderizadas (mínimo para indexar: {min_stories})")

    units = [edition.get("cover", {})] + edition.get("stories", [])[1:]
    unsourced = [u for u in units if u and not u.get("sources")]
    add("all_sourced", not unsourced, f"{len(unsourced)} unidad(es) sin fuente")

    return {"ok": all(c["ok"] for c in checks), "checks": checks}
