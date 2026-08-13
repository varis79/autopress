"""pack — arma el TEMPLATE compartible con `starter/` en la RAÍZ y lo empaqueta.

El repo de desarrollo tiene `autopress/` como raíz y `starter/` dentro. GitHub solo
reconoce `.github/workflows/` en la RAÍZ del repo, así que el template que se distribuye
debe tener el contenido de `starter/` en la raíz. Este script produce esa estructura:

  <template>/               = contenido de starter/ (scripts, tests, .github, legal, …)
  ├── README.md             = README público (front-door)
  ├── AGENTS.md             = entrada para el agente (reglas de construcción)
  ├── HOWTO.md ARCHITECTURE.md
  ├── 00-…-12-*.md  BLUEPRINT…  en/*.md   (guías a nivel raíz)
  └── docs de mantenedor EXCLUIDOS (PROGRESO, REVISION-EXTERNA, KIT-v2)

Uso:  python3 pack.py [<carpeta_build>]
"""
from __future__ import annotations
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))          # autopress/
STARTER = os.path.join(ROOT, "starter")

GUIDES = ["EMPIEZA-AQUI.md", "GUIA-COMPLETA.md",
          "00-QUICKSTART.md", "01-ANTES-DE-EMPEZAR.md", "02-CUENTAS-Y-DOMINIO.md",
          "03-COSTES.md", "04-DESPLIEGUE.md", "05-CUESTIONARIO.md",
          "06-ADAPTACION-TEMATICA.md", "07-GUARDARRAILES.md", "08-MODO-INDEPENDIENTE.md",
          "10-SEO.md", "12-TROUBLESHOOTING.md", "BLUEPRINT-MEDIO-AUTONOMO.md"]


def _rewrite_root(t: str) -> str:
    t = t.replace("](../docs/ARCHITECTURE.md)", "](ARCHITECTURE.md)")
    t = t.replace("](../docs/", "](")
    t = t.replace("](../AGENTS.md)", "](05-CUESTIONARIO.md)")
    t = t.replace("](docs/ARCHITECTURE.md)", "](ARCHITECTURE.md)")
    t = t.replace("](starter/", "](")
    t = re.sub(r"\]\(\.\./", "](", t)        # cualquier ../ restante (a nivel raíz) → plano
    return t


def _rewrite_subdir(t: str) -> str:
    t = t.replace("](../../", "](../")       # guías: antes dos niveles arriba, ahora en la raíz
    t = t.replace("](../starter/", "](../")
    return t


# Docs de mantenedor que NO viajan en el template: sus enlaces se convierten en texto plano.
_EXCLUDED = ("PROGRESO.md", "REVISION-EXTERNA.md", "KIT-v2-DECISIONES-Y-PLAN.md")


def _strip_excluded_links(t: str) -> str:
    for name in _EXCLUDED:
        t = re.sub(r"\[([^\]]+)\]\((?:\.\./)*" + re.escape(name) + r"\)", r"\1", t)
    return t


def _rewrite_commands(t: str) -> str:
    """En el template la raíz ES el starter: no hay `cd starter` ni prefijo `starter/`."""
    t = t.replace("cd starter && ", "")
    t = t.replace("cd starter/", "cd ")
    t = t.replace("`cd starter`", "el directorio raíz")
    t = t.replace("starter/", "")        # rutas en comandos/prosa: starter/scripts → scripts
    t = re.sub(r"cd starter\b", "cd .", t)   # catch-all (p. ej. `cd starter` en su propia línea)
    return t


def build(dest: str):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(STARTER, dest,
                    ignore=shutil.ignore_patterns("__pycache__", "site", ".venv", ".env",
                                                  "*.pyc", ".DS_Store"))
    # limpiar logs/estado generado (mantener READMEs de data/)
    for sub in ("operations", "editions"):
        d = os.path.join(dest, "data", sub)
        if os.path.isdir(d):
            for n in os.listdir(d):
                if n.endswith(".json"):
                    os.remove(os.path.join(d, n))

    # starter/README.md (arquitectura) → HOWTO.md; README público a la raíz
    if os.path.exists(os.path.join(dest, "README.md")):
        os.replace(os.path.join(dest, "README.md"), os.path.join(dest, "HOWTO.md"))
    shutil.copy2(os.path.join(ROOT, "README.md"), os.path.join(dest, "README.md"))
    shutil.copy2(os.path.join(ROOT, "LICENSE"), os.path.join(dest, "LICENSE"))
    # VERSION al template: scripts.update lo lee para saber qué versión tiene.
    if os.path.exists(os.path.join(ROOT, "VERSION")):
        shutil.copy2(os.path.join(ROOT, "VERSION"), os.path.join(dest, "VERSION"))
    shutil.copy2(os.path.join(ROOT, "docs", "ARCHITECTURE.md"),
                 os.path.join(dest, "ARCHITECTURE.md"))
    for g in GUIDES:
        src = os.path.join(ROOT, g)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dest, g))
    if os.path.isdir(os.path.join(ROOT, "en")):
        shutil.copytree(os.path.join(ROOT, "en"), os.path.join(dest, "en"))

    # reescribir enlaces según la profundidad del fichero
    for cur, _dirs, files in os.walk(dest):
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(cur, name)
            with open(path, encoding="utf-8") as f:
                txt = f.read()
            at_root = (os.path.dirname(path) == dest)
            new = _rewrite_root(txt) if at_root else _rewrite_subdir(txt)
            new = _strip_excluded_links(new)
            new = _rewrite_commands(new)   # comandos/paths: sin `cd starter` ni `starter/`
            if new != txt:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)

    # LICENSE: quitar la referencia a `starter/` (en el template el código está en la raíz).
    lic = os.path.join(dest, "LICENSE")
    if os.path.exists(lic):
        with open(lic, encoding="utf-8") as f:
            lt = f.read()
        lt = lt.replace("bajo `starter/`", "en la raíz del proyecto").replace("starter/", "")
        with open(lic, "w", encoding="utf-8") as f:
            f.write(lt)
    return dest


def main(argv):
    dest = argv[1] if len(argv) > 1 else os.path.join(ROOT, "..", "autopress-template")
    dest = os.path.abspath(dest)
    build(dest)
    archive = shutil.make_archive(dest, "zip", root_dir=dest)
    print(f"template en: {dest}\nzip: {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
