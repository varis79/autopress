"""Test del ingest (offline, contra un feed de ejemplo en fixtures/feeds/).

    cd starter && PYTHONPATH=. python3 -m unittest tests.test_ingest
"""
from __future__ import annotations
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # starter/
sys.path.insert(0, ROOT)

from scripts.ingest import parse_feed, ingest  # noqa: E402

FEED = os.path.join(ROOT, "fixtures", "feeds", "demo-wire.xml")


class IngestTest(unittest.TestCase):
    def test_parse_feed_normalizes(self):
        with open(FEED, encoding="utf-8") as f:
            items = parse_feed(f.read(), source_name="Demo Wire")
        self.assertEqual(len(items), 3)
        first = items[0]
        self.assertEqual(first["title"], "Regulator approves new compliance law in Mexico")
        self.assertEqual(first["published"], "2026-08-09")
        self.assertEqual(first["source_name"], "Demo Wire")
        # HTML eliminado del resumen:
        self.assertNotIn("<", first["summary"])
        self.assertIn("regulator", first["summary"].lower())
        # id estable y con prefijo:
        self.assertTrue(first["id"].startswith("s"))

    def test_ingest_applies_lookback_window(self):
        # as_of 2026-08-10, ventana 8 días → el ítem del 1 de julio se descarta.
        items = ingest([{"name": "Demo Wire", "url": FEED}],
                       as_of="2026-08-10", lookback_days=8, allow_local=True)
        urls = [it["url"] for it in items]
        self.assertEqual(len(items), 2)
        self.assertFalse(any("n3" in u for u in urls))

    def test_ingest_reports_per_source_status(self):
        # una fuente OK y una caída → el diagnóstico las distingue (no 'vacía').
        diag = []
        ingest([{"name": "Demo Wire", "url": FEED},
                {"name": "Caída", "url": "/ruta/inexistente/feed.xml"}],
               as_of="2026-08-10", lookback_days=8, diagnostics=diag, allow_local=True)
        by = {d["name"]: d for d in diag}
        self.assertEqual(by["Demo Wire"]["status"], "ok")
        self.assertEqual(by["Demo Wire"]["count"], 2)
        self.assertEqual(by["Caída"]["status"], "error")
        self.assertIn("error", by["Caída"])


if __name__ == "__main__":
    unittest.main()
