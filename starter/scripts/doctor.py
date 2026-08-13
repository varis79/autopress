"""doctor.py — diagnóstico "listo / no listo" para el operador.

Comprueba en segundos lo esencial y termina con un veredicto claro y arreglos
concretos. Pensado para que un no-técnico entienda qué falta.

Uso:
    cd starter && python3 scripts/doctor.py

Bloqueantes para modo LOCAL (fixtures, sin cuentas):
  · Config válida
  · Fixtures presentes
  · El núcleo determinista reproduce la salida golden
No bloqueantes (avisos): dependencias/opcionales y variables de entorno (solo
hacen falta al conectar LLM, newsletter o deploy).
"""
from __future__ import annotations
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # starter/
sys.path.insert(0, ROOT)

OK, WARN, BAD = "✅", "⚠️ ", "❌"


def _load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_python():
    ok = sys.version_info >= (3, 11)
    return ok, f"Python {sys.version_info.major}.{sys.version_info.minor} " + (
        "(ok, >=3.11)" if ok else "→ necesitas Python 3.11+")


def check_config():
    from scripts.validate_config import validate
    path = os.path.join(ROOT, "fixtures", "config.json")
    if not os.path.exists(path):
        return False, "fixtures/config.json no existe."
    errors = validate(path)
    if errors:
        return False, f"Config inválida: {errors[0]}" + (" …" if len(errors) > 1 else "")
    return True, "fixtures/config.json válida."


def check_fixtures():
    need = ["fixtures/raw.jsonl", "fixtures/config.json", "fixtures/expected/selection.json"]
    missing = [p for p in need if not os.path.exists(os.path.join(ROOT, p))]
    if missing:
        return False, "Faltan fixtures: " + ", ".join(missing)
    return True, "Fixtures presentes."


def check_golden():
    try:
        from scripts.pipeline_core import run
        raw = [json.loads(l) for l in open(os.path.join(ROOT, "fixtures", "raw.jsonl"), encoding="utf-8") if l.strip()]
        cfg = _load_json(os.path.join(ROOT, "fixtures", "config.json"))
        exp = _load_json(os.path.join(ROOT, "fixtures", "expected", "selection.json"))
        return (run(raw, cfg) == exp), ("El núcleo reproduce la salida golden."
                                        if run(raw, cfg) == exp else
                                        "El núcleo NO reproduce la golden — el pipeline determinista está roto.")
    except Exception as e:  # noqa: BLE001
        return False, f"Error ejecutando el núcleo: {e}"


def check_optional_deps():
    deps = ["feedparser", "bs4", "yaml", "requests", "anthropic", "jsonschema"]
    present = [d for d in deps if importlib.util.find_spec(d) is not None]
    missing = [d for d in deps if d not in present]
    msg = f"presentes: {', '.join(present) or 'ninguna'}"
    if missing:
        msg += f" · faltan (solo para fases posteriores): {', '.join(missing)}"
    return True, msg  # nunca bloquea el modo local


def check_env():
    names = ["ANTHROPIC_API_KEY", "RESEND_API_KEY", "RESEND_AUDIENCE_ID", "NEWSLETTER_SECRET", "DEPLOY_HOOK"]
    set_ = [n for n in names if os.environ.get(n)]
    unset = [n for n in names if not os.environ.get(n)]
    msg = f"definidas: {', '.join(set_) or 'ninguna'}"
    if unset:
        msg += f" · sin definir (necesarias al conectar LLM/newsletter/deploy): {', '.join(unset)}"
    return True, msg  # nunca bloquea el modo local


def main() -> int:
    print("\nAutopress · doctor\n" + "-" * 40)
    blocking = [
        ("Python", check_python()),
        ("Config", check_config()),
        ("Fixtures", check_fixtures()),
        ("Núcleo (golden)", check_golden()),
    ]
    advisory = [
        ("Dependencias", check_optional_deps()),
        ("Variables de entorno", check_env()),
    ]

    ready = True
    for label, (ok, msg) in blocking:
        mark = OK if ok else BAD
        if not ok:
            ready = False
        print(f"{mark} {label}: {msg}")
    for label, (_, msg) in advisory:
        print(f"{WARN}{label}: {msg}")

    print("-" * 40)
    if ready:
        print("LISTO para modo local (fixtures, sin cuentas).")
        print("Siguiente: correr el pipeline con tus fuentes, luego conectar LLM/host/newsletter.")
        return 0
    print("NO LISTO. Corrige los ❌ de arriba y vuelve a ejecutar doctor.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
