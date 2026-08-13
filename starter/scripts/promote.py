"""promote — aprueba TODAS las ediciones needs_review que pasen los gates, y reconstruye.

Se ejecuta al mergear la PR de review/strict (push a main): el merge humano ES la
aprobación. Reusa `approve` (que revalida config/QA/quality/legal/taxonomía y escribe
atómico), así que una edición que no pase los gates se queda en needs_review.

    cd starter && PYTHONPATH=. python3 -m scripts.promote [--config config.json]
"""
from __future__ import annotations
import json
import os
import sys

from scripts import approve

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # starter/


def _pending(store: str) -> list:
    out = []
    if not os.path.isdir(store):
        return out
    for name in sorted(os.listdir(store)):
        if not name.endswith(".json"):
            continue
        try:
            with open(os.path.join(store, name), encoding="utf-8") as f:
                if json.load(f).get("status") == "needs_review":
                    out.append(name[:-5])   # slug
        except Exception:
            continue
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    cfg = approve._arg_value(argv, "--config")
    passthrough = (["--config", cfg] if cfg else [])
    store = os.path.join(ROOT, "data", "editions")

    approved, refused = [], []
    for slug in _pending(store):
        rc = approve.main([slug] + passthrough)
        (approved if rc == 0 else refused).append(slug)

    print(json.dumps({"approved": approved, "refused": refused}, ensure_ascii=False, indent=2))
    return 1 if refused else 0


if __name__ == "__main__":
    raise SystemExit(main())
