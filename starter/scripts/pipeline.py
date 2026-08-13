"""pipeline — orquestador local (sin cuentas ni claves, modo stub).

Ejecuta: fixtures → classify → dedupe → select → compose_stub → qa → publish,
y escribe un sitio navegable en starter/site/. Imprime un JSON de estado.

    cd starter && PYTHONPATH=. python3 -m scripts.pipeline
"""
from __future__ import annotations
import datetime as dt
import json
import os
import sys

from scripts.pipeline_core import run_full
from scripts.compose import compose
from scripts.ingest import ingest
from scripts.qa import qa
from scripts.editorial_gate import evaluate as quality_eval
from scripts.validate_config import validate_dict
from scripts.legal import pending as legal_pending
from scripts import seen
from scripts.publish import publish

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # starter/


def _load_jsonl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def _arg_value(argv, flag):
    """Valor de `--flag valor` en argv (o None)."""
    if flag in argv:
        i = argv.index(flag)
        if i + 1 < len(argv):
            return argv[i + 1]
    return None


def _write_ops(report, production):
    """Deja el estado del run en data/operations/ (operabilidad: saber qué pasó y por qué).
    `latest.json` siempre; un fichero con timestamp solo en producción (historial)."""
    ops = os.path.join(ROOT, "data", "operations")
    os.makedirs(ops, exist_ok=True)
    with open(os.path.join(ops, "latest.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    if production:
        ts = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
        with open(os.path.join(ops, f"{ts}.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)


def _load_dotenv(path):
    """Carga ROOT/.env al entorno (solo claves ausentes). Sin dependencias."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k and v and k not in os.environ:
                os.environ[k] = v


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--help" in argv or "-h" in argv:
        print("Uso: python3 -m scripts.pipeline [--config <ruta>] [--production] [--fixtures]")
        return 0
    _known = {"--production", "--fixtures", "--config", "--help", "-h"}
    unknown = [a for a in argv if a.startswith("-") and a not in _known]
    if unknown:
        print(f"Argumento desconocido: {unknown[0]}. Usa --help.")
        return 2
    # Producción = publica de verdad (indexable). Preview (default) = genera el sitio
    # local en `noindex` para que lo veas, sin arriesgar indexar borradores.
    production = ("--production" in argv
                  or os.environ.get("AUTOPRESS_ENV", "").lower() == "production")

    _load_dotenv(os.path.join(ROOT, ".env"))
    # El operador de producción apunta a su propia config con --config <ruta>.
    config_path = _arg_value(argv, "--config") or os.path.join(ROOT, "fixtures", "config.json")
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    # --- El contrato de config GOBIERNA la ejecución: config inválida → no se corre. ---
    cfg_errors = validate_dict(config)
    if cfg_errors:
        print(json.dumps({"status": "config-invalid", "config": config_path,
                          "errors": cfg_errors[:20]}, ensure_ascii=False, indent=2))
        return 2

    # `as_of` (fecha de referencia): la del config si la fija (fixtures reproducibles),
    # o la de hoy en runtime. Siempre presente antes de seleccionar.
    if not config.get("as_of"):
        config["as_of"] = dt.date.today().isoformat()

    # --- Origen de los ítems crudos ---
    # Con `sources` en el config (y sin --fixtures) se ingiere de feeds reales; si no,
    # se usan los fixtures (demo/tests, reproducible con el as_of fijado en el config).
    sources = config.get("sources")
    use_fixtures = ("--fixtures" in argv) or not sources
    feeds_report = []
    if use_fixtures:
        raw = _load_jsonl(os.path.join(ROOT, "fixtures", "raw.jsonl"))
    else:
        icfg = config.get("ingest", {})
        _dom = config.get("site", {}).get("domain")
        _ua = f"AutopressBot/0.1 (+{_dom})" if _dom else None   # el crawler se identifica con TU web
        raw = ingest(sources, config["as_of"],
                     lookback_days=icfg.get("lookback_days", 8),
                     max_per_source=icfg.get("max_per_source", 20),
                     diagnostics=feeds_report, allow_local=False,  # feeds reales: nunca ficheros locales
                     user_agent=_ua)
        already = seen.load()                                       # memoria entre semanas
        raw = [it for it in raw if it.get("id") not in already]

    selection, deduped = run_full(raw, config)
    by_id = {it["id"]: it for it in deduped}
    site = config.get("site", {})
    # compose() usa el LLM si hay ANTHROPIC_API_KEY; si no, cae a stub.
    edition = compose(selection, by_id,
                      {"title": site.get("name", "Edición demo"),
                       "date": config.get("as_of", "")},
                      config, root=ROOT)
    qa_report = qa(edition, config)
    quality = quality_eval(edition, config)

    # --- Puerta de publicación (gate) ---
    publishing = config.get("publishing", {})
    risk = config.get("risk_profile", "review")
    reasons = []
    if qa_report["status"] == "blocked":
        reasons.append("qa-blocked")
    if selection["mode"] == "pause":
        reasons.append("mode-pause")
    if edition.get("stub"):
        reasons.append("stub")            # INVARIANTE: un stub nunca se publica en producción
    if config.get("meta", {}).get("needs_taxonomy"):
        reasons.append("taxonomy-placeholder")   # config sin temas/mercados reales → no producción
    if production and use_fixtures:
        reasons.append("fixtures-in-production")  # los fixtures son demo/tests, nunca producción
    if production and not site.get("domain"):
        reasons.append("no-domain")               # sin dominio absoluto: sitemap/canónicas rotas
    if production and legal_pending(ROOT, site.get("language", "es")):
        reasons.append("legal-placeholders")      # legales (del idioma) sin rellenar → no medio público
    gated = bool(reasons)

    # Estado editorial. Por integridad, la INDEXACIÓN AUTOMÁTICA está DESACTIVADA por defecto:
    # ni siquiera `auto` indexa salvo opt-in explícito (`publishing.allow_auto_index`). Sin él,
    # todo pasa por revisión humana (`approve.py`). Así el quality-gate actual no "certifica" solo.
    allow_auto_index = publishing.get("allow_auto_index", False)
    approved = (risk == "auto" and allow_auto_index and quality["ok"] and not edition.get("stub"))
    edition["status"] = "approved" if approved else "needs_review"
    edition["quality_report"] = quality
    indexable = production and edition["status"] == "approved"
    pending_review = production and not gated and edition["status"] == "needs_review"

    status = {
        "status": qa_report["status"],
        "source": "fixtures" if use_fixtures else "feeds",
        "raw_count": len(raw),
        "mode": selection["mode"],
        "count": selection["count"],
        "production": production,
        "risk_profile": risk,
        "edition_status": edition["status"],
        "quality_ok": quality["ok"],
        "gated": gated,
        "gate_reasons": reasons,
        "indexable": indexable,
        "pending_review": pending_review,
        "compose_error": edition.get("_compose_error"),
        "qa": qa_report["checks"],
        "quality": quality["checks"],
    }
    if feeds_report:
        status["feeds"] = feeds_report

    # En producción, un gate ACTIVO detiene la publicación (nada se escribe) y sale ≠ 0.
    if production and gated:
        status["published"] = False
        _write_ops(status, production)
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return 1

    result = publish(edition, config, out_dir=os.path.join(ROOT, "site"),
                     production=production,
                     store_dir=os.path.join(ROOT, "data", "editions"),
                     persist=production and not gated)   # solo acumula lo publicado de verdad
    if production:
        seen.add(s["id"] for s in selection["stories"])   # no repetir estas noticias
    # En preview NO se "publica": se genera un sitio local para verlo. Sé honesto en el estado.
    status.update(published=production, preview=(not production),
                  edition_url=result["edition_url"],
                  editions_total=result["editions_total"],
                  indexable_total=result["indexable_total"],
                  out_dir=result["out_dir"], files=result["files"])
    _write_ops(status, production)
    print(json.dumps(status, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
