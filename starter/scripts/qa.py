"""QA de la edición — con niveles (blocking / review_required / warning).

Versión inicial del núcleo de credibilidad. En modo LOCAL nada impide publicar
(solo informa), pero el status refleja los niveles para que el workflow decida
según el perfil de riesgo. La versión completa (más checks) llega en el
siguiente incremento.
"""
from __future__ import annotations

from scripts.lib.text import number_tokens, registrable_domain
from scripts import risk as risk_mod


def _independent_domains(sources) -> set:
    """Dominios registrables distintos entre las fuentes de una historia. Dos URLs del
    mismo editor NO cuentan como corroboración independiente."""
    return {d for s in (sources or []) if (d := registrable_domain(s.get("url", "")))}


def _rendered_units(edition: dict) -> list:
    """Lo que se RENDERIZA de verdad: la portada + las tarjetas (stories[1:]).
    stories[0] no se pinta como tarjeta (es la portada), así que no se revisa dos veces."""
    units = []
    cov = edition.get("cover", {})
    if cov:
        units.append(cov)
    units += edition.get("stories", [])[1:]
    return units


def _unsupported_numbers(unit: dict) -> list:
    """Cifras que aparecen en la redacción pero NO en su fuente. min_len=1 para cubrir también
    números de un dígito (muertos, heridos, %…), de alto impacto en noticias: '2→9 muertos' no
    debe colarse. (number_tokens agrupa dígitos en secuencias, así que no bloquea por dígitos
    sueltos dentro de un número mayor.)"""
    text = f"{unit.get('headline', '')} {unit.get('summary', '') or unit.get('deck', '')}"
    out = number_tokens(text, min_len=1)
    src = number_tokens(unit.get("_evidence", ""), min_len=1)
    return sorted(n for n in out if n not in src)


def qa(edition: dict, config: dict = None) -> dict:
    config = config or {}
    risk = config.get("risk_profile", "review")
    checks = []

    # blocking: portada presente
    has_cover = bool(edition.get("cover", {}).get("headline"))
    checks.append({"level": "blocking", "name": "cover",
                   "ok": has_cover,
                   "detail": "portada presente" if has_cover else "falta titular de portada"})

    # blocking: cifras inventadas — toda cifra de la redacción debe existir en la fuente.
    # Solo se evalúan unidades que traen evidencia (`_evidence`); las fabricadas a mano
    # sin evidencia no se bloquean (evita falsos positivos en tests/ediciones externas).
    bad = [(u, miss) for u in _rendered_units(edition)
           if "_evidence" in u and (miss := _unsupported_numbers(u))]
    checks.append({"level": "blocking", "name": "numbers_supported",
                   "ok": not bad,
                   "detail": "todas las cifras aparecen en la fuente" if not bad
                   else f"{len(bad)} bloque(s) con cifras sin fuente: "
                        + "; ".join(", ".join(m) for _, m in bad)[:180]})

    # blocking (TODOS los perfiles · riesgo POR ARTÍCULO): una ACUSACIÓN no se publica si no
    # está atribuida ("según…") Y corroborada por ≥N fuentes independientes. Así un medio en
    # `review`/`auto` tampoco puede colar una acusación sin respaldo.
    min_corr = config.get("publishing", {}).get("min_independent_sources", 2)
    weak_sensitive = []
    for u in _rendered_units(edition):
        text = f"{u.get('headline', '')} {u.get('summary', '') or u.get('deck', '')}"
        if risk_mod.BLOCKING_LABELS & risk_mod.tags(text):
            ok = risk_mod.has_attribution(text) and len(_independent_domains(u.get("sources", []))) >= min_corr
            if not ok:
                weak_sensitive.append(u)
    checks.append({"level": "blocking", "name": "sensitive_support",
                   "ok": not weak_sensitive,
                   "detail": "sin acusaciones sin respaldo" if not weak_sensitive
                   else f"{len(weak_sensitive)} acusación(es) sin atribución + ≥{min_corr} fuentes independientes"})

    # blocking (SOLO en perfil strict): cada historia con corroboración de ≥N fuentes
    # INDEPENDIENTES (dominios distintos). Sostiene el guardarraíl de temas sensibles.
    if risk == "strict":
        min_ind = config.get("publishing", {}).get("min_independent_sources", 2)
        weak = [u for u in _rendered_units(edition)
                if u.get("sources") and len(_independent_domains(u["sources"])) < min_ind]
        checks.append({"level": "blocking", "name": "independent_sources",
                       "ok": not weak,
                       "detail": f"todas con ≥{min_ind} fuentes independientes" if not weak
                       else f"{len(weak)} bloque(s) con <{min_ind} fuentes independientes (strict)"})

    # review_required: cada historia con al menos una fuente citada.
    # El modelo guarda fuentes numeradas en `sources` (lista); `source_url`
    # se acepta como forma antigua por compatibilidad.
    def _has_source(s):
        return bool(s.get("sources")) or bool(s.get("source_url"))
    no_src = [s for s in edition.get("stories", []) if not _has_source(s)]
    checks.append({"level": "review_required", "name": "sources",
                   "ok": not no_src,
                   "detail": "todas las historias citan su fuente" if not no_src
                   else f"{len(no_src)} historia(s) sin fuente"})

    # warning: stub (no debe llegar a producción)
    stub = bool(edition.get("stub"))
    checks.append({"level": "warning", "name": "stub",
                   "ok": not stub,
                   "detail": "sin stub" if not stub else "edición en modo stub (no publicar en producción)"})

    blocking_fail = [c for c in checks if c["level"] == "blocking" and not c["ok"]]
    any_fail = [c for c in checks if not c["ok"]]
    if blocking_fail:
        status = "blocked"
    elif any_fail:
        status = "ok-qa-warn"
    else:
        status = "ok"
    return {"status": status, "checks": checks}
