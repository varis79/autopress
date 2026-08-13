"""i18n del 'chrome' del medio: un medio en inglés se ve en inglés. Offline.

    cd starter && PYTHONPATH=. python3 -m unittest tests.test_i18n
"""
from __future__ import annotations
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from scripts.lib.site import render_edition_page, render_archive_page  # noqa: E402
from scripts.lib.i18n import t  # noqa: E402

ED = {"title": "M", "date": "2026-08-10", "stub": False,
      "cover": {"headline": "H", "deck": "D", "sources": []},
      "stories": [{"headline": "H", "summary": "S", "sources": []}]}


def _cfg(lang):
    # newsletter activa para poder comprobar los textos del formulario en cada idioma
    return {"site": {"name": "M", "language": lang, "theme": {}},
            "newsletter": {"enabled": True}}


class I18nTest(unittest.TestCase):
    def test_english_chrome(self):
        html = render_edition_page(ED, canonical="/", config=_cfg("en"), css="")
        for s in ["Latest", "Archive", "Subscribe", "Made with", "Content written with AI"]:
            self.assertIn(s, html)
        self.assertNotIn("Última", html)
        self.assertNotIn("Suscribirme", html)

    def test_spanish_default(self):
        html = render_edition_page(ED, canonical="/", config=_cfg("es"), css="")
        self.assertIn("Última", html)
        self.assertIn("Suscribirme", html)
        self.assertIn("Hecho con", html)

    def test_unknown_lang_falls_back_to_english(self):
        self.assertEqual(t("fr", "nav_latest"), "Latest")

    def test_archive_localized(self):
        html = render_archive_page([], canonical="/archive.html", config=_cfg("en"), css="")
        self.assertIn("Archive", html)
        self.assertNotIn("Archivo", html)


if __name__ == "__main__":
    unittest.main()
