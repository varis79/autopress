"""Asistente de configuración: build_config, taxonomía real, master-prompt, niveles. Offline.

    cd starter && PYTHONPATH=. python3 -m unittest tests.test_setup
"""
from __future__ import annotations
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import re  # noqa: E402
import tempfile  # noqa: E402

from scripts.setup import build_config, render_master_prompt, unlocked_level, fill_legal  # noqa: E402
from scripts.validate_config import validate_dict  # noqa: E402


class SetupTest(unittest.TestCase):
    def test_minimal_is_valid_but_needs_taxonomy(self):
        cfg = build_config({"name": "Radar"})
        self.assertEqual(validate_dict(cfg), [])            # config válido y ejecutable
        self.assertEqual(cfg["risk_profile"], "review")     # default seguro
        self.assertEqual(cfg["site"]["domain"], "")         # sin dominio → no bloquea
        self.assertTrue(cfg["meta"]["needs_taxonomy"])      # sin temas/mercados → placeholder
        self.assertEqual(cfg["meta"]["origin"], "setup")

    def test_taxonomy_comes_from_answers_not_fixtures(self):
        cfg = build_config({"name": "Q", "topics": ["quantum"], "markets": ["Japan"]})
        self.assertIn("quantum", cfg["taxonomy"]["topics"])
        self.assertIn("japan", cfg["taxonomy"]["markets"])
        self.assertNotIn("regulation", cfg["taxonomy"]["topics"])   # NADA de los fixtures
        self.assertNotIn("mx", cfg["taxonomy"]["markets"])
        self.assertFalse(cfg["meta"]["needs_taxonomy"])
        self.assertEqual(validate_dict(cfg), [])

    def test_with_feeds_and_domain(self):
        a = {"name": "Radar", "domain": "https://radar.example", "risk_profile": "strict",
             "topics": ["regulación"], "markets": ["México"],
             "sources": [{"name": "x.com", "url": "https://x.com/feed"}]}
        cfg = build_config(a)
        self.assertEqual(validate_dict(cfg), [])
        self.assertEqual(cfg["risk_profile"], "strict")
        self.assertEqual(len(cfg["sources"]), 1)

    def test_master_prompt_fills_placeholders(self):
        with open(os.path.join(ROOT, "prompts", "master-prompt.example.md"), encoding="utf-8") as f:
            tpl = f.read()
        out = render_master_prompt({"name": "Radar", "topic": "flotas", "language": "es",
                                    "tone": "sobrio", "markets_str": "México, España"}, tpl)
        self.assertIn("Radar", out)
        self.assertIn("flotas", out)
        self.assertNotIn("<NOMBRE_MEDIO>", out)             # placeholders resueltos

    def test_fill_legal_removes_placeholders(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "legal"))
            with open(os.path.join(d, "legal", "privacidad.md"), "w", encoding="utf-8") as f:
                f.write("# <NOMBRE_MEDIO>\nContacto: <EMAIL_CONTACTO>. Fecha <FECHA>. "
                        "País <DOMICILIO_O_PAIS>. Plazo <PLAZO, p. ej. 72 h>.")
            fill_legal({"name": "Radar", "email": "a@b.com", "country": "España",
                        "language": "es"}, d)
            with open(os.path.join(d, "legal", "privacidad.md"), encoding="utf-8") as f:
                txt = f.read()
            self.assertIn("Radar", txt)
            self.assertIn("a@b.com", txt)
            self.assertIsNone(re.search(r"<[A-ZÁÉÍÓÚÑ][^>]*>", txt))   # sin placeholders

    def test_levels_are_incremental(self):
        self.assertIn("0", unlocked_level({}))
        self.assertIn("1", unlocked_level({"name": "R"}))
        self.assertIn("3", unlocked_level({"name": "R", "api_key": "k"}))


if __name__ == "__main__":
    unittest.main()
