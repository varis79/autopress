"""Riesgo por artículo (A-05): una acusación sin atribución+corroboración no se publica.

    cd starter && PYTHONPATH=. python3 -m unittest tests.test_risk
"""
from __future__ import annotations
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from scripts import risk  # noqa: E402
from scripts.qa import qa  # noqa: E402


def _ed(headline, summary, sources):
    return {"stub": False, "stories": [],
            "cover": {"headline": headline, "deck": summary, "sources": sources}}


ONE = [{"n": 1, "url": "https://a.com/x"}]
TWO_INDEP = [{"n": 1, "url": "https://a.com/x"}, {"n": 2, "url": "https://b.com/y"}]


class RiskTest(unittest.TestCase):
    def test_tags_and_attribution(self):
        self.assertIn("allegation", risk.tags("La empresa cometió fraude"))
        self.assertIn("health", risk.tags("nuevo tratamiento contra el cáncer"))
        self.assertFalse(risk.tags("La empresa lanzó un coche eléctrico"))
        self.assertTrue(risk.has_attribution("Según el fiscal, hubo fraude"))
        self.assertFalse(risk.has_attribution("Hubo fraude"))

    def test_unattributed_allegation_blocks_even_in_review(self):
        # perfil por defecto (review): igualmente NO se publica una acusación sin respaldo.
        ed = _ed("Escándalo", "La empresa cometió fraude masivo", ONE)
        rep = qa(ed)   # sin config → review
        self.assertEqual(rep["status"], "blocked")
        chk = next(c for c in rep["checks"] if c["name"] == "sensitive_support")
        self.assertFalse(chk["ok"])

    def test_attributed_and_corroborated_allegation_passes(self):
        ed = _ed("Caso", "Según el fiscal, la empresa cometió fraude", TWO_INDEP)
        chk = next(c for c in qa(ed)["checks"] if c["name"] == "sensitive_support")
        self.assertTrue(chk["ok"])

    def test_non_allegation_is_fine(self):
        ed = _ed("Lanzamiento", "La empresa presentó un coche eléctrico", ONE)
        chk = next(c for c in qa(ed)["checks"] if c["name"] == "sensitive_support")
        self.assertTrue(chk["ok"])


if __name__ == "__main__":
    unittest.main()
