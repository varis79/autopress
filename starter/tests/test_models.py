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
        self.assertEqual(models.superseded("claude-opus-4-1-20250805"), "claude-opus-5")

    def test_current_model_not_flagged(self):
        # un modelo vigente o desconocido NO se marca (evita falsos positivos)
        self.assertIsNone(models.superseded("claude-sonnet-5"))
        self.assertIsNone(models.superseded("claude-opus-5"))
        self.assertIsNone(models.superseded("un-modelo-futuro-inventado"))
        self.assertIsNone(models.superseded(""))
        self.assertIsNone(models.advisory("claude-sonnet-5"))
        self.assertIsNone(models.describe("claude-sonnet-5"))

    def test_status_derives_from_date_not_from_a_hand_written_flag(self):
        """El mismo ID es 'heredado' antes de su fecha y 'retirado' después.

        Es la propiedad que hace que el aviso siga siendo correcto aunque el
        operador lleve meses sin actualizar el kit.
        """
        mid = "claude-opus-4-1-20250805"        # retirada anunciada: 2026-08-05
        antes = models.advisory(mid, today="2026-08-04")
        despues = models.advisory(mid, today="2026-08-05")   # el día mismo ya cuenta
        self.assertEqual(antes["status"], models.LEGACY)
        self.assertEqual(despues["status"], models.RETIRED)
        self.assertEqual(despues["replacement"], "claude-opus-5")
        self.assertEqual(despues["retires"], "2026-08-05")

    def test_deprecated_without_date_is_legacy_forever(self):
        # sin fecha anunciada nunca lo damos por retirado (no inventamos hechos)
        adv = models.advisory("claude-sonnet-4-20250514", today="2030-01-01")
        self.assertEqual(adv["status"], models.LEGACY)
        self.assertIsNone(adv["retires"])

    def test_describe_is_explicit_about_being_broken(self):
        retirado = models.describe("claude-3-opus-20240229", today="2026-08-20")
        self.assertIn("RETIRADO", retirado)
        self.assertIn("claude-opus-5", retirado)       # dice a qué cambiarlo
        self.assertIn("compose.model", retirado)       # y dónde tocarlo
        heredado = models.describe("claude-sonnet-4-20250514", today="2026-08-20")
        self.assertNotIn("RETIRADO", heredado)
        self.assertIn("claude-sonnet-5", heredado)

    def test_every_entry_is_well_formed(self):
        """Guardarraíl de mantenimiento: al añadir un ID a mano es fácil colar
        una fecha con otro formato o un reemplazo que a su vez está en la lista."""
        for mid, (replacement, retires) in models.KNOWN.items():
            self.assertTrue(replacement, f"{mid} sin reemplazo")
            self.assertNotIn(replacement, models.KNOWN,
                             f"{mid} apunta a '{replacement}', que también es heredado")
            if retires is not None:
                self.assertRegex(retires, r"^\d{4}-\d{2}-\d{2}$",
                                 f"{mid}: fecha '{retires}' no es ISO YYYY-MM-DD")


class TestDoctorModelCheck(unittest.TestCase):
    def test_check_model_runs_and_is_advisory(self):
        ok, msg = doctor.check_model()
        self.assertTrue(ok)                      # nunca bloquea
        self.assertIsInstance(msg, str)
        self.assertTrue(len(msg) > 0)


if __name__ == "__main__":
    unittest.main()
