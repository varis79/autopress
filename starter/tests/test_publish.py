"""Persistencia de ediciones: el sitio se reconstruye desde TODAS las ediciones
guardadas (archivo/RSS acumulan histórico). Offline.

    cd starter && PYTHONPATH=. python3 -m unittest tests.test_publish
"""
from __future__ import annotations
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from scripts.publish import publish  # noqa: E402

CONFIG = {"site": {"name": "M", "domain": "https://m.com",
                   "theme": {"style": "editorial", "palette": "warm"}}}


def _ed(date, hl, status="approved"):
    return {"title": "M", "date": date, "stub": False, "status": status,
            "cover": {"headline": hl, "deck": "d " + hl, "kicker": "k", "sources": []},
            "stories": [{"headline": hl, "summary": "s " + hl,
                         "topic": "t", "market": "mx", "sources": []}]}


class PublishStoreTest(unittest.TestCase):
    def test_archive_accumulates_editions(self):
        with tempfile.TemporaryDirectory() as store, tempfile.TemporaryDirectory() as out:
            publish(_ed("2026-08-03", "Uno"), CONFIG, out, store_dir=store, persist=True)
            r = publish(_ed("2026-08-10", "Dos"), CONFIG, out, store_dir=store, persist=True)
            self.assertEqual(r["editions_total"], 2)          # el histórico se acumula
            with open(os.path.join(out, "archive.html"), encoding="utf-8") as f:
                archive = f.read()
            self.assertIn("2026-08-03", archive)
            self.assertIn("2026-08-10", archive)
            self.assertTrue(os.path.exists(os.path.join(out, "magazines", "2026-08-03-edicion.html")))
            self.assertTrue(os.path.exists(os.path.join(out, "magazines", "2026-08-10-edicion.html")))
            with open(os.path.join(out, "index.html"), encoding="utf-8") as f:
                self.assertIn("Dos", f.read())                # home = la más reciente

    def test_seo_metadata_present(self):
        with tempfile.TemporaryDirectory() as store, tempfile.TemporaryDirectory() as out:
            publish(_ed("2026-08-10", "Uno"), CONFIG, out, store_dir=store,
                    persist=True, production=True)   # approved + producción → indexable
            with open(os.path.join(out, "index.html"), encoding="utf-8") as f:
                idx = f.read()
            self.assertIn("application/ld+json", idx)     # datos estructurados
            self.assertIn('"@type": "NewsArticle"', idx)
            self.assertIn("og:title", idx)                # Open Graph
            self.assertIn("index, follow", idx)           # approved en producción → indexable
            with open(os.path.join(out, "sitemap.xml"), encoding="utf-8") as f:
                self.assertIn("<lastmod>2026-08-10</lastmod>", f.read())

    def test_needs_review_is_noindex_and_absent_from_sitemap(self):
        with tempfile.TemporaryDirectory() as store, tempfile.TemporaryDirectory() as out:
            publish(_ed("2026-08-10", "Uno", status="needs_review"), CONFIG, out,
                    store_dir=store, persist=True, production=True)
            with open(os.path.join(out, "index.html"), encoding="utf-8") as f:
                self.assertIn("noindex", f.read())        # needs_review nunca se indexa
            with open(os.path.join(out, "sitemap.xml"), encoding="utf-8") as f:
                self.assertNotIn("/magazines/", f.read())  # sitemap sin borradores

    def test_orphan_pages_removed_on_rebuild(self):
        # Retirar una edición del store y reconstruir → su página desaparece (base de `retract`).
        with tempfile.TemporaryDirectory() as store, tempfile.TemporaryDirectory() as out:
            publish(_ed("2026-08-03", "Uno"), CONFIG, out, store_dir=store, persist=True)
            publish(_ed("2026-08-10", "Dos"), CONFIG, out, store_dir=store, persist=True)
            self.assertTrue(os.path.exists(os.path.join(out, "magazines", "2026-08-03-edicion.html")))
            os.remove(os.path.join(store, "2026-08-03-edicion.json"))
            publish(_ed("2026-08-10", "Dos"), CONFIG, out, store_dir=store, persist=False)
            self.assertFalse(os.path.exists(os.path.join(out, "magazines", "2026-08-03-edicion.html")))

    def test_preview_does_not_persist(self):
        with tempfile.TemporaryDirectory() as store, tempfile.TemporaryDirectory() as out:
            publish(_ed("2026-08-03", "Uno"), CONFIG, out, store_dir=store, persist=False)
            self.assertEqual(len([n for n in os.listdir(store) if n.endswith(".json")]), 0)


if __name__ == "__main__":
    unittest.main()
