"""update.py — actualiza el MOTOR de Autopress sin tocar tu contenido.

Descarga la última versión publicada del kit y sobrescribe SOLO el código del
motor. Hace una copia de seguridad antes. NUNCA toca lo tuyo:
config.json · .env · data/ · site/ · prompts/ · legal/ · examples/

Uso:
    python3 -m scripts.update            # comprueba y, si hay novedad, actualiza
    python3 -m scripts.update --check    # solo dice si hay versión nueva (no cambia nada)
    python3 -m scripts.update --docs     # además refresca las guías (.md) y en/
    python3 -m scripts.update --yes      # sin preguntar (para automatizar)

Fuente (upstream): variable de entorno AUTOPRESS_UPSTREAM (owner/repo) o, por
defecto, el repo oficial del proyecto. Solo librería estándar: sin dependencias.
"""
from __future__ import annotations
import argparse
import datetime as _dt
import json
import os
import shutil
import sys
import tempfile
import zipfile
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
INSTALL_ROOT = os.path.dirname(HERE)                       # raíz del kit (contiene scripts/)
UPSTREAM = os.environ.get("AUTOPRESS_UPSTREAM", "varis79/autopress")

# Motor (se sobrescribe) y contenido del operador (NUNCA se toca).
ENGINE = ["scripts", "tests", "functions",
          "autopress.schema.json", "requirements.txt", "AGENTS.md"]
NEVER = {"config.json", ".env", "data", "site", "prompts", "legal", "examples"}


# ---- núcleo testeable (sin red) --------------------------------------------

def _semver(s: str):
    """'v1.2.3' | '1.2.3' → (1,2,3). Tolerante; lo no numérico cuenta como 0."""
    s = (s or "").strip().lstrip("vV")
    parts = (s.split("-")[0].split("+")[0]).split(".")
    out = []
    for p in parts[:3]:
        out.append(int(p) if p.isdigit() else 0)
    while len(out) < 3:
        out.append(0)
    return tuple(out)


def _is_newer(remote: str, local: str) -> bool:
    return _semver(remote) > _semver(local)


def _find_pkg_root(extracted: str) -> str:
    """Raíz del kit dentro de lo descomprimido (la carpeta que contiene scripts/)."""
    if os.path.isdir(os.path.join(extracted, "scripts")):
        return extracted
    for n in sorted(os.listdir(extracted)):
        d = os.path.join(extracted, n)
        if os.path.isdir(d) and os.path.isdir(os.path.join(d, "scripts")):
            return d
    return extracted


def _doc_names(pkg_root: str):
    """Guías a refrescar con --docs: todos los .md de la raíz del paquete + en/."""
    names = [n for n in sorted(os.listdir(pkg_root))
             if n.endswith(".md") and os.path.isfile(os.path.join(pkg_root, n))]
    if os.path.isdir(os.path.join(pkg_root, "en")):
        names.append("en")
    return names


def apply_update(pkg_root: str, install_root: str, names, ts: str):
    """Copia `names` de pkg_root → install_root, con backup previo. Devuelve
    (actualizados, ruta_backup). Ignora por seguridad cualquier ruta en NEVER."""
    names = [n for n in names if n.split("/")[0] not in NEVER]
    bdir = os.path.join(install_root, ".autopress-backups")
    os.makedirs(bdir, exist_ok=True)
    bpath = os.path.join(bdir, f"backup-{ts}.zip")
    with zipfile.ZipFile(bpath, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            tgt = os.path.join(install_root, n)
            if os.path.isdir(tgt):
                for root, _d, files in os.walk(tgt):
                    for f in files:
                        fp = os.path.join(root, f)
                        z.write(fp, os.path.relpath(fp, install_root))
            elif os.path.isfile(tgt):
                z.write(tgt, os.path.relpath(tgt, install_root))

    updated = []
    for n in names:
        src = os.path.join(pkg_root, n)
        if not os.path.exists(src):
            continue
        tgt = os.path.join(install_root, n)
        if os.path.isdir(src):
            if os.path.isdir(tgt):
                shutil.rmtree(tgt)
            shutil.copytree(src, tgt)
        else:
            os.makedirs(os.path.dirname(tgt) or ".", exist_ok=True)
            shutil.copy2(src, tgt)
        updated.append(n)
    return updated, bpath


# ---- red (GitHub Releases) --------------------------------------------------

def _api(url: str):
    req = urllib.request.Request(url, headers={
        "User-Agent": "AutopressUpdater/1.0",
        "Accept": "application/vnd.github+json",
    })
    with urllib.request.urlopen(req, timeout=30) as r:   # noqa: S310 (host fijo de GitHub)
        return json.loads(r.read().decode("utf-8"))


def latest_release(repo: str):
    """Devuelve (tag, url_del_zip) de la última Release publicada."""
    data = _api(f"https://api.github.com/repos/{repo}/releases/latest")
    tag = data.get("tag_name", "")
    zip_url = ""
    for a in data.get("assets", []):
        if a.get("name", "").endswith(".zip"):
            zip_url = a.get("browser_download_url", "")
            break
    return tag, zip_url


def _download(url: str, dest: str):
    req = urllib.request.Request(url, headers={"User-Agent": "AutopressUpdater/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:  # noqa: S310
        shutil.copyfileobj(r, f)


def _safe_extract(zf: "zipfile.ZipFile", dest: str):
    """Extrae rechazando rutas absolutas o con '..' (anti *zip-slip*): un miembro malicioso
    no debe escribir fuera de `dest`. La allowlist NEVER solo filtra el COPIADO posterior, no
    la extracción, así que el saneo tiene que ir aquí, en la propia feature de auto-update."""
    dest_abs = os.path.realpath(dest)
    for name in zf.namelist():
        target = os.path.realpath(os.path.join(dest, name))
        if target != dest_abs and not target.startswith(dest_abs + os.sep):
            raise ValueError(f"ruta insegura en el ZIP (posible zip-slip): {name!r}")
    zf.extractall(dest)


def _read_local_version(install_root: str) -> str:
    p = os.path.join(install_root, "VERSION")
    try:
        with open(p, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return "0.0.0"


# ---- main -------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="scripts.update", description="Actualiza el motor de Autopress.")
    ap.add_argument("--check", action="store_true", help="Solo comprueba si hay versión nueva.")
    ap.add_argument("--docs", action="store_true", help="También refresca las guías (.md) y en/.")
    ap.add_argument("--yes", action="store_true", help="No preguntar (automatizado).")
    args = ap.parse_args(argv)

    local = _read_local_version(INSTALL_ROOT)
    print(f"Autopress · update\nInstalado: v{local}  ·  upstream: {UPSTREAM}")
    try:
        tag, zip_url = latest_release(UPSTREAM)
    except Exception as e:  # noqa: BLE001
        print(f"❌ No pude consultar las versiones ({e}).")
        if "CERTIFICATE_VERIFY" in str(e):
            print("   Tu Python no tiene certificados SSL. En Mac (Python de python.org): abre")
            print("   'Applications/Python 3.x/Install Certificates.command'. O usa el Python de")
            print("   Homebrew (brew install python). Luego reintenta.")
        else:
            print("   ¿Sin conexión? Reintenta más tarde.")
        return 1
    if not tag:
        print("❌ El upstream no tiene ninguna Release publicada todavía.")
        return 1

    if not _is_newer(tag, local):
        print(f"✅ Ya estás en la última versión (v{local}). Nada que hacer.")
        return 0

    print(f"⬆️  Hay una versión nueva: {tag} (tienes v{local}).")
    if args.check:
        print("   (--check: no he cambiado nada. Corre 'python3 -m scripts.update' para aplicarla.)")
        return 0
    if not zip_url:
        print("❌ La Release no trae el ZIP adjunto; no puedo actualizar automáticamente.")
        return 1
    if not args.yes:
        r = input("¿Actualizo el motor ahora? (no toco tu config/datos) [s/N] ").strip().lower()
        if r not in ("s", "si", "sí", "y", "yes"):
            print("Cancelado. No he cambiado nada.")
            return 0

    ts = _dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    with tempfile.TemporaryDirectory() as tmp:
        zpath = os.path.join(tmp, "kit.zip")
        print("   Descargando…")
        try:
            _download(zip_url, zpath)
        except Exception as e:  # noqa: BLE001
            print(f"❌ Falló la descarga ({e}).")
            return 1
        ex = os.path.join(tmp, "ex")
        with zipfile.ZipFile(zpath) as z:
            _safe_extract(z, ex)   # anti zip-slip: valida rutas antes de escribir
        pkg = _find_pkg_root(ex)
        if not os.path.isdir(os.path.join(pkg, "scripts")):
            print("❌ El ZIP no parece un kit válido (sin scripts/). Aborto sin tocar nada.")
            return 1

        names = list(ENGINE)
        if args.docs:
            for n in _doc_names(pkg):
                if n not in names:
                    names.append(n)
        updated, backup = apply_update(pkg, INSTALL_ROOT, names, ts)

    # actualizar el marcador de versión
    try:
        with open(os.path.join(INSTALL_ROOT, "VERSION"), "w", encoding="utf-8") as f:
            f.write(_semver_str(tag) + "\n")
    except OSError:
        pass

    print(f"✅ Motor actualizado a {tag}. Copia de seguridad en: {os.path.relpath(backup, INSTALL_ROOT)}")
    print(f"   Actualizado: {', '.join(updated)}")
    print("   Tu config.json, .env, data/ y contenido NO se han tocado.")
    print("   Comprueba que todo sigue en verde:  PYTHONPATH=. python3 -m unittest discover tests")
    return 0


def _semver_str(tag: str) -> str:
    return ".".join(str(x) for x in _semver(tag))


if __name__ == "__main__":
    sys.exit(main())
