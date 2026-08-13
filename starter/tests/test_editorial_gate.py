"""Quality-gate D1: qué edición merece indexarse (approved). Offline.

    cd starter && PYTHONPATH=. python3 -m unittest tests.test_editorial_gate
"""
from __future__ import annotations
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from scripts.editorial_gate import evaluate  # noqa: E402

CONFIG = {"modes": {"min_normal": 2}}


def _story(hl):
    return {"headline": hl, "summary": "s", "sources": [{"n": 1, "url": "https://x.com/a"}]}


def _ed(**over):
    ed = {"stub": False, "cover": {"headline": "H", "deck": "D",
          "sources": [{"n": 1, "url": "https://x.com/a"}]},
          "stories": [_story("a"), _story("b"), _story("c")]}
    ed.update(over)
    return ed


class EditorialGateTest(unittest.TestCase):
    def test_good_edition_is_approvable(self):
        self.assertTrue(evaluate(_ed(), CONFIG)["ok"])       # 3 historias renderizadas

    def test_stub_never_approvable(self):
        self.assertFalse(evaluate(_ed(stub=True), CONFIG)["ok"])

    def test_thin_edition_not_approvable(self):
        thin = _ed()
        thin["stories"] = [thin["stories"][0]]               # solo 1 historia renderizada
        self.assertFalse(evaluate(thin, CONFIG)["ok"])       # cuenta lo renderizado, no la selección

    def test_unsourced_not_approvable(self):
        ed = _ed()
        ed["stories"][1]["sources"] = []                     # una tarjeta sin fuente
        self.assertFalse(evaluate(ed, CONFIG)["ok"])


if __name__ == "__main__":
    unittest.main()
