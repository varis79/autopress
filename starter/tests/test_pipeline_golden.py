"""Test determinista del núcleo del pipeline contra una salida 'golden'.

Corre sin API key, sin cuentas y sin dependencias externas (solo stdlib):
    cd starter && PYTHONPATH=. python3 -m unittest tests.test_pipeline_golden

Si este test no pasa, el pipeline determinista está roto: arréglalo ANTES de
conectar el LLM. La salida 'golden' (fixtures/expected/selection.json) es el
contrato que dos agentes distintos deben reproducir idéntico.
"""
from __future__ import annotations
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # starter/
sys.path.insert(0, ROOT)

from scripts.pipeline_core import run  # noqa: E402


def _load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class GoldenPipelineTest(unittest.TestCase):
    def test_selection_matches_golden(self):
        raw = _load_jsonl(os.path.join(ROOT, "fixtures", "raw.jsonl"))
        config = _load_json(os.path.join(ROOT, "fixtures", "config.json"))
        expected = _load_json(os.path.join(ROOT, "fixtures", "expected", "selection.json"))
        got = run(raw, config)
        self.assertEqual(got, expected)

    def test_competitor_is_filtered(self):
        # i6 menciona un competidor de la blacklist: nunca debe aparecer.
        raw = _load_jsonl(os.path.join(ROOT, "fixtures", "raw.jsonl"))
        config = _load_json(os.path.join(ROOT, "fixtures", "config.json"))
        ids = [s["id"] for s in run(raw, config)["stories"]]
        self.assertNotIn("i6", ids)

    def test_duplicate_is_deduped(self):
        # i5 es un duplicado de i1 por título: no deben aparecer ambos.
        raw = _load_jsonl(os.path.join(ROOT, "fixtures", "raw.jsonl"))
        config = _load_json(os.path.join(ROOT, "fixtures", "config.json"))
        ids = [s["id"] for s in run(raw, config)["stories"]]
        self.assertNotIn("i5", ids)


if __name__ == "__main__":
    unittest.main()
