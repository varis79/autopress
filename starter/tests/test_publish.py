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

    def test_seo_signals_and_eeat(self):
        cfg = {"site": {"name": "M", "domain": "https://m.com", "language": "es",
                        "theme": {"style": "editorial", "palette": "warm"}},
               "editorial": {"curator": "Ana"}, "risk_profile": "review",
               "sources": [{"name": "Alfa", "url": "https://alfa.com/feed"}]}
        two = [{"n": 1, "url": "https://a.com/x", "name": "a"},
               {"n": 2, "url": "https://b.com/y", "name": "b"}]
        ed = {"title": "M", "date": "2026-08-10", "stub": False, "status": "approved",
              "cover": {"headline": "Portada clave", "deck": "deck", "kicker": "k", "sources": two},
              "stories": [{"headline": "Portada clave", "summary": "s", "sources": []},
                          {"headline": "Segunda historia", "summary": "s2", "topic": "t",
                           "market": "mx", "sources": two}]}
        with tempfile.TemporaryDirectory() as store, tempfile.TemporaryDirectory() as out:
            publish(ed, cfg, out, store_dir=store, persist=True, production=True)
            idx = open(os.path.join(out, "index.html"), encoding="utf-8").read()
            self.assertIn("Portada clave · M", idx)              # F1 <title> con titular
            self.assertIn("La semana en breve", idx)             # F4 tldr (2 titulares)
            self.assertIn("2 fuentes", idx)                      # F5 badge de corroboración
            self.assertIn("Curado por Ana", idx)                 # byline (E-E-A-T)
            for p in ("about.html", "methodology.html", "sources.html"):  # F3
                self.assertTrue(os.path.exists(os.path.join(out, p)))
            method = open(os.path.join(out, "methodology.html"), encoding="utf-8").read()
            self.assertIn("index, follow", method)               # indexable en producción
            self.assertIn("digest", method.lower())              # alcance honesto declarado
            srcs = open(os.path.join(out, "sources.html"), encoding="utf-8").read()
            self.assertIn("alfa.com", srcs)                      # fuente del config listada
            robots = open(os.path.join(out, "robots.txt"), encoding="utf-8").read()  # F2
            self.assertIn("Sitemap: https://m.com/sitemap.xml", robots)
            sm = open(os.path.join(out, "sitemap.xml"), encoding="utf-8").read()
            self.assertIn("/methodology.html", sm)

    def test_backport_og_locale_twitter_jsonld_prevnext(self):
        cfg = {"site": {"name": "M", "domain": "https://m.com", "language": "es-ES",
                        "theme": {"style": "editorial", "palette": "warm"},
                        "same_as": ["https://x.com/medio"], "logo": "https://m.com/logo.png",
                        "og_image": {"mode": "static", "path": "/social.png"}}}
        with tempfile.TemporaryDirectory() as store, tempfile.TemporaryDirectory() as out:
            publish(_ed("2026-08-03", "Uno"), cfg, out, store_dir=store, persist=True, production=True)
            publish(_ed("2026-08-10", "Dos"), cfg, out, store_dir=store, persist=True, production=True)
            idx = open(os.path.join(out, "index.html"), encoding="utf-8").read()
            self.assertIn('property="og:locale" content="es_ES"', idx)   # G3 (es-ES→es_ES)
            self.assertIn('name="twitter:card" content="summary_large_image"', idx)  # G2 (con imagen)
            self.assertIn('property="og:image" content="https://m.com/social.png"', idx)  # G2 estática
            self.assertIn('"inLanguage": "es"', idx)                     # G4 aditivo
            self.assertIn('"@type": "BreadcrumbList"', idx)             # G4 breadcrumb
            self.assertIn('"sameAs"', idx)                              # G4 sameAs opt-in
            # G1 prev/next: la home (Dos) enlaza a la anterior (Uno)
            self.assertIn('/magazines/2026-08-03-edicion.html', idx)
            older = open(os.path.join(out, "magazines", "2026-08-03-edicion.html"), encoding="utf-8").read()
            self.assertIn('rel="next"', older)                          # la antigua tiene 'siguiente'

    def test_backport_rejects_svg_og_image(self):
        cfg = {"site": {"name": "M", "domain": "https://m.com", "language": "es",
                        "theme": {"style": "editorial", "palette": "warm"},
                        "og_image": {"mode": "static", "path": "/card.svg"}}}
        with tempfile.TemporaryDirectory() as store, tempfile.TemporaryDirectory() as out:
            publish(_ed("2026-08-10", "Uno"), cfg, out, store_dir=store, persist=True, production=True)
            idx = open(os.path.join(out, "index.html"), encoding="utf-8").read()
            self.assertNotIn("og:image", idx)                          # SVG rechazado como og:image
            self.assertIn('name="twitter:card" content="summary"', idx)  # sin imagen → summary

    def test_robots_preview_disallows(self):
        with tempfile.TemporaryDirectory() as store, tempfile.TemporaryDirectory() as out:
            publish(_ed("2026-08-10", "Uno"), CONFIG, out, store_dir=store, persist=True)  # preview
            robots = open(os.path.join(out, "robots.txt"), encoding="utf-8").read()
            self.assertIn("Disallow: /", robots)

    def test_preview_does_not_persist(self):
        with tempfile.TemporaryDirectory() as store, tempfile.TemporaryDirectory() as out:
            publish(_ed("2026-08-03", "Uno"), CONFIG, out, store_dir=store, persist=False)
            self.assertEqual(len([n for n in os.listdir(store) if n.endswith(".json")]), 0)


if __name__ == "__main__":
    unittest.main()
