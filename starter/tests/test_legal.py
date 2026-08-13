"""Legal: md→HTML, detección de placeholders, footer (ai_disclosure + enlaces). Offline.

    cd starter && PYTHONPATH=. python3 -m unittest tests.test_legal
"""
from __future__ import annotations
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from scripts.legal import md_to_html, pending  # noqa: E402
from scripts.lib.templating import _footer_html  # noqa: E402


class LegalTest(unittest.TestCase):
    def test_md_to_html(self):
        h = md_to_html("# T\n\nHola **mundo** y [x](https://x.com).\n\n- a\n- b")
        self.assertIn("<h1>T</h1>", h)
        self.assertIn("<strong>mundo</strong>", h)
        self.assertIn('<a href="https://x.com"', h)
        self.assertIn("<li>a</li>", h)

    def test_pending_detects_unfilled_placeholders(self):
        # las plantillas que se envían traen <PLACEHOLDER> → están 'pending'.
        self.assertIn("privacidad", pending(ROOT))

    def test_footer_respects_ai_disclosure(self):
        on = _footer_html("es", {"editorial": {"ai_disclosure": True}})
        off = _footer_html("es", {"editorial": {"ai_disclosure": False}})
        self.assertIn("asistencia de IA", on)
        self.assertNotIn("asistencia de IA", off)

    def test_footer_shows_legal_links(self):
        f = _footer_html("es", {"_legal_links": [("Privacidad", "/legal/privacidad.html")]})
        self.assertIn("/legal/privacidad.html", f)
        self.assertIn("Privacidad", f)


if __name__ == "__main__":
    unittest.main()
