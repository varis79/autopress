"""Núcleo determinista del pipeline: classify → dedupe → select.

Corre sin API key ni cuentas. Uso:
    PYTHONPATH=. python3 -m scripts.pipeline_core fixtures/raw.jsonl fixtures/config.json
"""
from __future__ import annotations
import json
import sys

from scripts.classify import classify
from scripts.dedupe import dedupe
from scripts.select_stories import select


def run_full(raw_items, config: dict):
    """Devuelve (selección, ítems deduplicados). Los ítems deduplicados llevan
    la procedencia (`merged`) que compose usa para las citas numeradas."""
    classified = classify(raw_items, config["taxonomy"])
    threshold = config.get("dedupe", {}).get("title_similarity_threshold", 0.82)
    deduped = dedupe(classified, threshold)
    selection = select(deduped, config)
    return selection, deduped


def run(raw_items, config: dict) -> dict:
    """Solo la selección (contrato del test golden)."""
    selection, _ = run_full(raw_items, config)
    return selection


def _load_jsonl(path: str):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main(argv):
    raw = _load_jsonl(argv[1])
    with open(argv[2], encoding="utf-8") as f:
        config = json.load(f)
    print(json.dumps(run(raw, config), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
