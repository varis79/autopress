"""approve — aprueba una edición needs_review REVALIDANDO todos los gates, y reconstruye.

Es el paso HUMANO del flujo review/strict. NO se salta nada: antes de marcar `approved`
vuelve a comprobar config, taxonomía, legal, stub, QA y quality-gate. Si algo falla, NO
aprueba. Escritura atómica. `<slug>` es normalmente `<fecha>-edicion`.

    cd starter && PYTHONPATH=. python3 -m scripts.approve <slug> [--config config.json]
"""
from __future__ import annotations
import json
import os
import sys

from scripts.publish import publish
from scripts.qa import qa
from scripts.editorial_gate import evaluate as quality_eval
from scripts.validate_config import validate_dict
from scripts.legal import pending as legal_pending

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # starter/


def _arg_value(argv, flag):
    if flag in argv:
        i = argv.index(flag)
        if i + 1 < len(argv):
            return argv[i + 1]
    return None


def _blockers(edition: dict, config: dict) -> list:
    problems = []
    if validate_dict(config):
        problems.append("config-invalid")
    if config.get("meta", {}).get("needs_taxonomy"):
        problems.append("taxonomy-placeholder")
    lang = config.get("site", {}).get("language", "es")
    if legal_pending(ROOT, lang):
        problems.append("legal-placeholders")
    if edition.get("stub"):
        problems.append("stub")
    if qa(edition, config)["status"] == "blocked":
        problems.append("qa-blocked")
    if not quality_eval(edition, config)["ok"]:
        problems.append("quality-gate")
    return problems


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0].startswith("-"):
        print("Uso: python3 -m scripts.approve <slug> [--config <ruta>]")
        return 2
    slug = argv[0]
    store = os.path.join(ROOT, "data", "editions")
    path = os.path.join(store, f"{slug}.json")
    if not os.path.exists(path):
        print(f"No existe la edición '{slug}' en {store}")
        return 1

    with open(path, encoding="utf-8") as f:
        edition = json.load(f)
    cfg_path = _arg_value(argv, "--config") or os.path.join(ROOT, "fixtures", "config.json")
    with open(cfg_path, encoding="utf-8") as f:
        config = json.load(f)

    # REVALIDAR: aprobar NO puede saltarse ningún gate.
    problems = _blockers(edition, config)
    if problems:
        print(json.dumps({"approved": False, "slug": slug, "problems": problems},
                         ensure_ascii=False, indent=2))
        return 1

    # Escritura atómica del nuevo estado.
    edition["status"] = "approved"
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(edition, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)

    result = publish(edition, config, out_dir=os.path.join(ROOT, "site"),
                     production=True, store_dir=store, persist=False)
    print(json.dumps({"approved": slug, "indexable_total": result["indexable_total"]},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
