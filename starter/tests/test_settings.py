"""Catálogo de settings: integridad, filtro y valor actual. Offline.

    cd starter && PYTHONPATH=. python3 -m unittest tests.test_settings
"""
from __future__ import annotations
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from scripts.settings import SETTINGS, render, _current, _REQUIRED_FIELDS  # noqa: E402


class SettingsTest(unittest.TestCase):
    def test_registry_integrity(self):
        keys = set()
        for s in SETTINGS:
            self.assertEqual(len(s), _REQUIRED_FIELDS, f"entrada mal formada: {s}")
            self.assertNotIn(s[0], keys, f"key duplicada: {s[0]}")
            keys.add(s[0])
            self.assertIn(s[2], ("config", "env", "prompt", "workflow", "host"))

    def test_render_all_mentions_known_keys(self):
        out = render()
        self.assertIn("site.name", out)
        self.assertIn("risk_profile", out)
        self.assertIn("site.timezone", out)     # el huso horario que pidió el usuario

    def test_filter_narrows(self):
        out = render("newsletter")
        self.assertIn("RESEND_API_KEY", out)
        self.assertNotIn("site.name", out)       # el filtro deja fuera lo no relacionado

    def test_shows_current_value_from_config(self):
        cfg = {"site": {"name": "Radar Real"}, "risk_profile": "strict"}
        out = render("identidad", cfg)
        self.assertIn("Radar Real", out)         # muestra el valor actual, no el default
        self.assertEqual(_current(cfg, "site.name"), "Radar Real")
        self.assertIsNone(_current(cfg, "site.nope"))


if __name__ == "__main__":
    unittest.main()
