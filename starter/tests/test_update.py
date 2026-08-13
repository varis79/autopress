"""Tests del auto-actualizador (scripts.update) — sin red, solo el núcleo."""
import os
import sys
import shutil
import tempfile
import unittest
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import update  # noqa: E402


class TestSemver(unittest.TestCase):
    def test_parse_and_compare(self):
        self.assertEqual(update._semver("v0.5.0"), (0, 5, 0))
        self.assertEqual(update._semver("1.2.3"), (1, 2, 3))
        self.assertEqual(update._semver("2.0"), (2, 0, 0))
        self.assertTrue(update._is_newer("v0.6.0", "0.5.0"))
        self.assertTrue(update._is_newer("1.0.0", "0.9.9"))
        self.assertFalse(update._is_newer("0.5.0", "0.5.0"))
        self.assertFalse(update._is_newer("0.4.0", "0.5.0"))

    def test_semver_str(self):
        self.assertEqual(update._semver_str("v0.6.0"), "0.6.0")


class TestFindPkgRoot(unittest.TestCase):
    def test_flat_and_nested(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "flat", "scripts"))
            self.assertEqual(update._find_pkg_root(os.path.join(d, "flat")),
                             os.path.join(d, "flat"))
            nested = os.path.join(d, "nested")
            os.makedirs(os.path.join(nested, "autopress-v1", "scripts"))
            self.assertEqual(update._find_pkg_root(nested),
                             os.path.join(nested, "autopress-v1"))


class TestApplyUpdate(unittest.TestCase):
    def _install(self, root):
        # kit "instalado" con motor viejo + contenido del operador
        os.makedirs(os.path.join(root, "scripts"))
        with open(os.path.join(root, "scripts", "pipeline.py"), "w") as f:
            f.write("VERSION_MOTOR = 'viejo'\n")
        with open(os.path.join(root, "config.json"), "w") as f:
            f.write('{"mio": true}')
        os.makedirs(os.path.join(root, "data"))
        with open(os.path.join(root, "data", "edicion.json"), "w") as f:
            f.write('{"mi": "contenido"}')
        with open(os.path.join(root, ".env"), "w") as f:
            f.write("ANTHROPIC_API_KEY=secreto\n")

    def _pkg(self, root):
        os.makedirs(os.path.join(root, "scripts"))
        with open(os.path.join(root, "scripts", "pipeline.py"), "w") as f:
            f.write("VERSION_MOTOR = 'nuevo'\n")
        # el paquete nuevo también trae un config.json (de ejemplo) que NO debe pisar
        with open(os.path.join(root, "config.json"), "w") as f:
            f.write('{"ejemplo": true}')

    def test_engine_updated_content_preserved(self):
        with tempfile.TemporaryDirectory() as base:
            inst = os.path.join(base, "inst")
            pkg = os.path.join(base, "pkg")
            os.makedirs(inst); os.makedirs(pkg)
            self._install(inst)
            self._pkg(pkg)

            updated, backup = update.apply_update(pkg, inst, ["scripts", "config.json"], "TS")

            # el motor se actualizó
            with open(os.path.join(inst, "scripts", "pipeline.py")) as f:
                self.assertIn("nuevo", f.read())
            # config.json NO se tocó aunque estaba en la lista (está en NEVER)
            with open(os.path.join(inst, "config.json")) as f:
                self.assertIn("mio", f.read())
            self.assertIn("scripts", updated)
            self.assertNotIn("config.json", updated)
            # existe la copia de seguridad y contiene el motor viejo
            self.assertTrue(os.path.exists(backup))
            with zipfile.ZipFile(backup) as z:
                names = z.namelist()
                self.assertTrue(any("scripts/pipeline.py" in n for n in names))

    def test_never_content_untouched(self):
        with tempfile.TemporaryDirectory() as base:
            inst = os.path.join(base, "inst")
            pkg = os.path.join(base, "pkg")
            os.makedirs(inst); os.makedirs(pkg)
            self._install(inst)
            self._pkg(pkg)
            # aunque pidamos explícitamente data/ y .env, NEVER los protege
            update.apply_update(pkg, inst, ["scripts", "data", ".env"], "TS2")
            with open(os.path.join(inst, "data", "edicion.json")) as f:
                self.assertIn("mi", f.read())
            with open(os.path.join(inst, ".env")) as f:
                self.assertIn("secreto", f.read())


if __name__ == "__main__":
    unittest.main()
