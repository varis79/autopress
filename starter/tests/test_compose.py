"""Test de compose: procedencia (rechazo de fuentes/historias inventadas) y
fallback a stub sin clave. Offline, no gasta API.

    cd starter && PYTHONPATH=. python3 -m unittest tests.test_compose
"""
from __future__ import annotations
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from scripts.pipeline_core import run_full  # noqa: E402
from scripts.compose import compose, assemble  # noqa: E402


def _load():
    with open(os.path.join(ROOT, "fixtures", "raw.jsonl"), encoding="utf-8") as f:
        raw = [json.loads(l) for l in f if l.strip()]
    with open(os.path.join(ROOT, "fixtures", "config.json"), encoding="utf-8") as f:
        config = json.load(f)
    selection, deduped = run_full(raw, config)
    by_id = {it["id"]: it for it in deduped}
    return selection, by_id, config


META = {"title": "T", "date": "2026-08-10"}


class ComposeTest(unittest.TestCase):
    def test_assemble_rejects_hallucinated_source(self):
        selection, by_id, _ = _load()
        rid = selection["stories"][1]["id"]  # historia con 2 fuentes reales
        data = {"cover": {"headline": "H", "deck": "D"},
                "stories": [{"ref_id": rid, "headline": "Titular", "summary": "Resumen",
                             "source_refs": [rid, "sFAKE00000"]}]}
        ed = assemble(data, selection, by_id, META)
        srcs = ed["stories"][0]["sources"]
        self.assertTrue(all(s["ref_id"] != "sFAKE00000" for s in srcs))  # inventada descartada
        self.assertGreaterEqual(len(srcs), 1)
        self.assertFalse(ed["stub"])

    def test_assemble_drops_unknown_story(self):
        selection, by_id, _ = _load()
        data = {"cover": {}, "stories": [{"ref_id": "sUNKNOWN", "headline": "x", "summary": "y"}]}
        with self.assertRaises(ValueError):  # sin historias válidas → error (el pipeline caería a stub)
            assemble(data, selection, by_id, META)

    def test_no_key_falls_back_to_stub(self):
        selection, by_id, config = _load()
        old = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            ed = compose(selection, by_id, META, config, root=ROOT)
            self.assertTrue(ed["stub"])  # sin clave → stub, nunca se rompe
        finally:
            if old is not None:
                os.environ["ANTHROPIC_API_KEY"] = old


if __name__ == "__main__":
    unittest.main()
