"""serve — construye el sitio (preview) y lo sirve en local para verlo.

    cd starter && PYTHONPATH=. python3 -m scripts.serve

Usa `config.json` si existe (tu medio), o los fixtures (demo). Es SIEMPRE preview
(noindex): para publicar de verdad se usa `scripts.pipeline --production`.
"""
from __future__ import annotations
import functools
import http.server
import os
import socketserver
import sys

from scripts import pipeline

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # starter/


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    port = 8000
    for i, x in enumerate(argv):
        if x == "--port" and i + 1 < len(argv):
            port = int(argv[i + 1])

    # 1. Construir (preview). Con config.json usa tu medio; si no, los fixtures.
    cfg = os.path.join(ROOT, "config.json")
    build_args = ["--config", cfg] if os.path.exists(cfg) else []
    print("Construyendo el sitio (preview)…")
    rc = pipeline.main(build_args)
    if rc != 0:
        print(f"\n⚠️  El build terminó con código {rc}: no sirvo un sitio posiblemente incorrecto. "
              "Revisa el estado de arriba (config inválida, etc.).")
        return rc

    # 2. Servir site/ en local.
    site = os.path.join(ROOT, "site")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=site)
    print(f"\n▶ Tu medio en  http://localhost:{port}   (Ctrl-C para parar)")
    with socketserver.TCPServer(("", port), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nparado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
