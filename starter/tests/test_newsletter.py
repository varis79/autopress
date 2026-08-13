"""Tokens de newsletter: firma HMAC, doble opt-in y baja. Offline, sin red.

    cd starter && PYTHONPATH=. python3 -m unittest tests.test_newsletter
"""
from __future__ import annotations
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from scripts.newsletter import make_token, verify_token, CONFIRM, UNSUBSCRIBE  # noqa: E402

SECRET = "clave-de-prueba"
NOW = 1_000_000
EXP = NOW + 3600


class NewsletterTokenTest(unittest.TestCase):
    def test_round_trip_and_normalizes_email(self):
        t = make_token(CONFIRM, "  Ana@Example.COM ", EXP, secret=SECRET)
        self.assertEqual(verify_token(t, CONFIRM, NOW, secret=SECRET), "ana@example.com")

    def test_tampered_token_rejected(self):
        t = make_token(CONFIRM, "a@x.com", EXP, secret=SECRET)
        self.assertIsNone(verify_token(t + "x", CONFIRM, NOW, secret=SECRET))

    def test_wrong_secret_rejected(self):
        t = make_token(CONFIRM, "a@x.com", EXP, secret=SECRET)
        self.assertIsNone(verify_token(t, CONFIRM, NOW, secret="otra"))

    def test_action_cannot_be_reused(self):
        # un token de baja NO sirve para confirmar alta (ni al revés).
        t = make_token(UNSUBSCRIBE, "a@x.com", EXP, secret=SECRET)
        self.assertIsNone(verify_token(t, CONFIRM, NOW, secret=SECRET))
        self.assertEqual(verify_token(t, UNSUBSCRIBE, NOW, secret=SECRET), "a@x.com")

    def test_expired_rejected(self):
        t = make_token(CONFIRM, "a@x.com", EXP, secret=SECRET)
        self.assertIsNone(verify_token(t, CONFIRM, EXP + 1, secret=SECRET))  # ya caducó


if __name__ == "__main__":
    unittest.main()
