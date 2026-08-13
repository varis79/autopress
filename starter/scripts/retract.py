"""retract — retira una edición: la borra del almacén y reconstruye el sitio.

Como `publish` limpia `magazines/` antes de renderizar, la página de la edición retirada
**desaparece** del sitio (no queda huérfana). `<slug>` es normalmente `<fecha>-edicion`.

    cd starter && PYTHONPATH=. python3 -m scripts.retract <slug> [--config config.json]
"""
from __future__ import annotations
import json
import os
import sys

from scripts.publish import publish, _load_store
from scripts import approve

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # starter/


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0].startswith("-"):
        print("Uso: python3 -m scripts.retract <slug> [--config <ruta>]")
        return 2
    slug = argv[0]
    store = os.path.join(ROOT, "data", "editions")
    path = os.path.join(store, f"{slug}.json")
    if not os.path.exists(path):
        print(f"No existe la edición '{slug}' en {store}")
        return 1
    os.remove(path)

    cfg_path = approve._arg_value(argv, "--config") or os.path.join(ROOT, "fixtures", "config.json")
    with open(cfg_path, encoding="utf-8") as f:
        config = json.load(f)

    remaining = sorted(_load_store(store), key=lambda e: e.get("date", ""), reverse=True)
    current = remaining[0] if remaining else {"date": "", "stub": False, "status": "needs_review",
                                              "cover": {"headline": ""}, "stories": []}
    result = publish(current, config, out_dir=os.path.join(ROOT, "site"),
                     production=True, store_dir=store, persist=False)
    print(json.dumps({"retracted": slug, "editions_total": result["editions_total"]},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
