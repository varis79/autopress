"""SSRF: hosts privados/loopback rechazados; ficheros locales solo con allow_local. Offline
(usa IPs literales y ficheros locales; no hace DNS de dominios reales).

    cd starter && PYTHONPATH=. python3 -m unittest tests.test_ssrf
"""
from __future__ import annotations
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from scripts.ingest import _is_public_host, _read_source  # noqa: E402

FEED = os.path.join(ROOT, "fixtures", "feeds", "demo-wire.xml")


class SsrfTest(unittest.TestCase):
    def test_private_and_loopback_hosts_rejected(self):
        for h in ("127.0.0.1", "10.0.0.1", "192.168.1.1", "169.254.169.254", "localhost", "0.0.0.0"):
            self.assertFalse(_is_public_host(h), h)

    def test_local_file_blocked_without_allow_local(self):
        with self.assertRaises(ValueError):
            _read_source("file:///etc/hosts")
        with self.assertRaises(ValueError):
            _read_source("/etc/hosts")

    def test_private_http_host_blocked(self):
        with self.assertRaises(ValueError):
            _read_source("http://127.0.0.1/feed.xml")

    def test_local_file_allowed_with_flag(self):
        data = _read_source(FEED, allow_local=True)
        self.assertIn(b"<", data)   # leyó el XML del fixture


if __name__ == "__main__":
    unittest.main()
