"""Tests del conocimiento de modelos y del aviso de doctor."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.lib import models  # noqa: E402
from scripts import doctor  # noqa: E402


class TestModels(unittest.TestCase):
    def test_superseded_flags_legacy(self):
        self.assertEqual(models.superseded("claude-3-opus-20240229"), "claude-opus-5")
        self.assertEqual(models.superseded("claude-3-5-sonnet-20241022"), "claude-sonnet-5")

    def test_current_model_not_flagged(self):
        # un modelo vigente o desconocido NO se marca (evita falsos positivos)
        self.assertIsNone(models.superseded("claude-sonnet-5"))
        self.assertIsNone(models.superseded("claude-opus-5"))
        self.assertIsNone(models.superseded("un-modelo-futuro-inventado"))
        self.assertIsNone(models.superseded(""))


class TestDoctorModelCheck(unittest.TestCase):
    def test_check_model_runs_and_is_advisory(self):
        ok, msg = doctor.check_model()
        self.assertTrue(ok)                      # nunca bloquea
        self.assertIsInstance(msg, str)
        self.assertTrue(len(msg) > 0)


if __name__ == "__main__":
    unittest.main()
