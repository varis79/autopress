"""Test de compose: procedencia (rechazo de fuentes/historias inventadas) y
fallback a stub sin clave. Offline, no gasta API.

    cd starter && PYTHONPATH=. python3 -m unittest tests.test_compose
"""
from __future__ import annotations
import json
import os
import sys
import types
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

    def test_assemble_drops_empty_stories(self):
        selection, by_id, _ = _load()
        rid = selection["stories"][0]["id"]
        data = {"cover": {"headline": "H", "deck": "D"},
                "stories": [{"ref_id": rid, "headline": "", "summary": ""}]}  # tarjeta en blanco
        with self.assertRaises(ValueError):   # sin contenido útil → el pipeline caería a stub
            assemble(data, selection, by_id, META)

    def test_assemble_keeps_only_nonempty(self):
        selection, by_id, _ = _load()
        r0, r1 = selection["stories"][0]["id"], selection["stories"][1]["id"]
        data = {"cover": {}, "stories": [
            {"ref_id": r0, "headline": "", "summary": "cuerpo"},      # sin headline → descartada
            {"ref_id": r1, "headline": "Titular ok", "summary": "Cuerpo ok"}]}
        ed = assemble(data, selection, by_id, META)
        self.assertEqual(len(ed["stories"]), 1)
        self.assertEqual(ed["stories"][0]["headline"], "Titular ok")

    def test_truncated_response_falls_to_stub_with_cause(self):
        """stop_reason='max_tokens' → stub con causa 'truncated' (no parsea JSON a medias)."""
        selection, by_id, config = _load()

        class _Resp:
            stop_reason = "max_tokens"
            content = []

            class usage:
                input_tokens, output_tokens = 10, 8000

        class _Msgs:
            def create(self, **kw):
                return _Resp()

        class _FakeClient:
            def __init__(self, *a, **k):
                self.messages = _Msgs()

        fake = types.ModuleType("anthropic")
        fake.Anthropic = _FakeClient
        old_mod = sys.modules.get("anthropic")
        sys.modules["anthropic"] = fake
        os.environ["ANTHROPIC_API_KEY"] = "test-key"
        try:
            diag = {}
            ed = compose(selection, by_id, META, config, root=ROOT, diag=diag)
            self.assertTrue(ed["stub"])
            self.assertEqual(ed["_compose_error"], "truncated")
            self.assertEqual(diag["stop_reason"], "max_tokens")
        finally:
            os.environ.pop("ANTHROPIC_API_KEY", None)
            if old_mod is not None:
                sys.modules["anthropic"] = old_mod
            else:
                sys.modules.pop("anthropic", None)

    def test_retired_model_gives_actionable_cause(self):
        """404 (modelo retirado o ID mal escrito) → causa 'model-not-found'.

        Sin esto la causa sería 'NotFoundError': el operador ve una edición en
        stub y una palabra que no le dice que el arreglo está en su config.
        """
        selection, by_id, config = _load()

        class _NotFound(Exception):
            status_code = 404          # así lo expone el SDK de anthropic

        class _Msgs:
            def create(self, **kw):
                raise _NotFound("model: claude-opus-4-1-20250805")

        class _FakeClient:
            def __init__(self, *a, **k):
                self.messages = _Msgs()

        fake = types.ModuleType("anthropic")
        fake.Anthropic = _FakeClient
        old_mod = sys.modules.get("anthropic")
        sys.modules["anthropic"] = fake
        os.environ["ANTHROPIC_API_KEY"] = "test-key"
        try:
            diag = {}
            ed = compose(selection, by_id, META, config, root=ROOT, diag=diag)
            self.assertTrue(ed["stub"])                      # nunca rompe
            self.assertEqual(ed["_compose_error"], "model-not-found")
            self.assertEqual(diag["cause"], "model-not-found")
        finally:
            os.environ.pop("ANTHROPIC_API_KEY", None)
            if old_mod is not None:
                sys.modules["anthropic"] = old_mod
            else:
                sys.modules.pop("anthropic", None)

    def test_other_failures_keep_their_own_cause(self):
        """Solo el 404 se traduce: un fallo de red sigue diciendo qué fue."""
        selection, by_id, config = _load()

        class _Boom(Exception):
            status_code = 500

        class _Msgs:
            def create(self, **kw):
                raise _Boom("upstream")

        class _FakeClient:
            def __init__(self, *a, **k):
                self.messages = _Msgs()

        fake = types.ModuleType("anthropic")
        fake.Anthropic = _FakeClient
        old_mod = sys.modules.get("anthropic")
        sys.modules["anthropic"] = fake
        os.environ["ANTHROPIC_API_KEY"] = "test-key"
        try:
            ed = compose(selection, by_id, META, config, root=ROOT)
            self.assertEqual(ed["_compose_error"], "_Boom")
        finally:
            os.environ.pop("ANTHROPIC_API_KEY", None)
            if old_mod is not None:
                sys.modules["anthropic"] = old_mod
            else:
                sys.modules.pop("anthropic", None)

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
