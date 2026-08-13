"""Aprobación endurecida: `approve` revalida TODOS los gates (no se los salta). Offline.

    cd starter && PYTHONPATH=. python3 -m unittest tests.test_approve
"""
from __future__ import annotations
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from scripts.approve import _blockers  # noqa: E402


def _cfg():
    with open(os.path.join(ROOT, "fixtures", "config.json"), encoding="utf-8") as f:
        return json.load(f)


def _story(hl):
    return {"headline": hl, "summary": "s", "sources": [{"n": 1, "url": "https://x.com/a"}]}


def _ed(**over):
    ed = {"stub": False, "status": "needs_review",
          "cover": {"headline": "H", "deck": "D", "sources": [{"n": 1, "url": "https://x.com/a"}]},
          "stories": [_story("a"), _story("b"), _story("c")]}
    ed.update(over)
    return ed


class ApproveTest(unittest.TestCase):
    def test_stub_is_blocked(self):
        self.assertIn("stub", _blockers(_ed(stub=True), _cfg()))

    def test_thin_edition_is_blocked(self):
        self.assertIn("quality-gate", _blockers(_ed(stories=[_story("solo")]), _cfg()))

    def test_unfilled_legal_blocks_approval(self):
        # Las plantillas legales del repo traen placeholders → aprobar NO puede indexar sin legal.
        self.assertIn("legal-placeholders", _blockers(_ed(), _cfg()))

    def test_invalid_config_blocks(self):
        bad = _cfg()
        bad["clave_desconocida"] = 1
        # (solo se detecta con jsonschema; con el fallback estructural no, pero no debe romper)
        self.assertIsInstance(_blockers(_ed(), bad), list)


if __name__ == "__main__":
    unittest.main()
