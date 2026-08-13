"""seen — memoria de ítems ya publicados (evita repetir la misma noticia entre semanas).

Persiste en `data/seen.json` (versionado). El pipeline filtra los ítems cuyo id ya se
publicó antes de seleccionar, y añade los de cada edición publicada de verdad.
"""
from __future__ import annotations
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # starter/
_PATH = os.path.join(ROOT, "data", "seen.json")


def load() -> set:
    try:
        with open(_PATH, encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def add(ids) -> None:
    s = load() | {i for i in ids if i}
    os.makedirs(os.path.dirname(_PATH), exist_ok=True)
    tmp = _PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(sorted(s), f, ensure_ascii=False)
    os.replace(tmp, _PATH)
