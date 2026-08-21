"""doctor.py — diagnóstico "listo / no listo" para el operador.

Comprueba en segundos lo esencial y termina con un veredicto claro y arreglos
concretos. Pensado para que un no-técnico entienda qué falta.

Uso:
    cd starter && PYTHONPATH=. python3 -m scripts.doctor
    (opcional) PYTHONPATH=. python3 -m scripts.doctor --smoke   # 1 llamada real al LLM (requiere clave)

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
    op = os.path.join(ROOT, "config.json")               # el config REAL del operador
    demo = os.path.join(ROOT, "fixtures", "config.json")  # fallback demo
    # Prioriza el config del operador: un 'LISTO' que solo mira los fixtures oculta que el
    # medio real del no-técnico tenga una config inválida (luego serve/pipeline fallan).
    path = op if os.path.exists(op) else demo
    which = "config.json" if path == op else "fixtures/config.json (demo; aún sin config propia)"
    if not os.path.exists(path):
        return False, "no hay config.json ni fixtures/config.json."
    errors = validate(path)
    if errors:
        return False, f"{which} INVÁLIDA: {errors[0]}" + (" …" if len(errors) > 1 else "")
    return True, f"{which} válida."


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


def check_model():
    """Avisa si el modelo configurado está retirado o es una generación heredada.

    Nunca bloquea: el modo local (stub) funciona igual sin LLM. Pero un modelo
    RETIRADO sí rompe la redacción real, así que el texto lo dice sin rodeos.
    """
    from scripts.lib import models as models_mod
    path = os.path.join(ROOT, "config.json")           # el config del operador
    if not os.path.exists(path):
        path = os.path.join(ROOT, "fixtures", "config.json")   # fallback: demo
    try:
        cfg = _load_json(path)
    except Exception:  # noqa: BLE001
        return True, "sin config legible para comprobar el modelo."
    model = (cfg.get("compose") or {}).get("model", "")
    aviso = models_mod.describe(model)
    if aviso:
        return True, (f"{aviso} Corre 'python3 -m scripts.update' para traer la "
                      f"lista más reciente.")
    return True, (f"modelo '{model or '(por defecto)'}' sin avisos. Si Anthropic cambia "
                  f"el ID, actualiza compose.model y verifica en console.anthropic.com.")


def check_llm_ready():
    """Aviso cruzado: clave presente pero SDK 'anthropic' ausente → la edición caería a STUB
    en silencio (típico en una terminal nueva con el venv sin activar)."""
    has_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
    has_sdk = importlib.util.find_spec("anthropic") is not None
    if has_key and not has_sdk:
        return True, ("tienes ANTHROPIC_API_KEY pero falta el paquete 'anthropic' "
                      "(¿venv sin activar?): la edición caería a STUB. Activa el venv y "
                      "'pip install -r requirements.txt', o corre 'doctor --smoke'.")
    if has_key and has_sdk:
        return True, "clave y SDK presentes. Verifica en vivo con 'python3 -m scripts.doctor --smoke'."
    return True, "sin clave (modo stub). Añade ANTHROPIC_API_KEY para redactar de verdad."


def check_env():
    names = ["ANTHROPIC_API_KEY", "RESEND_API_KEY", "RESEND_AUDIENCE_ID", "NEWSLETTER_SECRET", "DEPLOY_HOOK"]
    set_ = [n for n in names if os.environ.get(n)]
    unset = [n for n in names if not os.environ.get(n)]
    msg = f"definidas: {', '.join(set_) or 'ninguna'}"
    if unset:
        msg += f" · sin definir (necesarias al conectar LLM/newsletter/deploy): {', '.join(unset)}"
    return True, msg  # nunca bloquea el modo local


def smoke() -> int:
    """Prueba de humo OPT-IN del camino LLM: UNA llamada real (fixture de 1 historia).

    Requiere ANTHROPIC_API_KEY. Aislado: no toca el pipeline ni publica nada. Sirve para
    verificar EN VIVO que la clave, el ID del modelo y el parseo funcionan de verdad —el
    primer contacto con la API no debería ser en producción. Muestra stop_reason y usage.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print(f"{BAD} smoke: falta ANTHROPIC_API_KEY. Expórtala y reintenta.")
        return 1
    if importlib.util.find_spec("anthropic") is None:
        print(f"{BAD} smoke: falta el paquete 'anthropic' (pip install anthropic).")
        return 1
    from scripts.pipeline_core import run_full
    from scripts.compose import compose
    raw = [json.loads(l) for l in open(os.path.join(ROOT, "fixtures", "raw.jsonl"),
                                       encoding="utf-8") if l.strip()]
    cfg = _load_json(os.path.join(ROOT, "config.json") if os.path.exists(
        os.path.join(ROOT, "config.json")) else os.path.join(ROOT, "fixtures", "config.json"))
    selection, deduped = run_full(raw, cfg)
    selection = {**selection, "stories": selection.get("stories", [])[:1]}  # 1 historia = coste mínimo
    by_id = {it["id"]: it for it in deduped}
    diag: dict = {}
    ed = compose(selection, by_id, {"title": "Smoke", "date": "2026-01-01"},
                 cfg, root=ROOT, diag=diag)
    print("\nAutopress · doctor --smoke\n" + "-" * 40)
    print(f"modelo: {diag.get('model', '?')} · thinking: {diag.get('thinking', '?')}")
    print(f"stop_reason: {diag.get('stop_reason', '?')} · usage: {diag.get('usage', '?')}")
    print("-" * 40)
    if ed.get("stub"):
        cause = diag.get("cause") or ed.get("_compose_error")
        print(f"{BAD} La llamada NO produjo una edición real (cayó a stub). Causa: {cause}")
        if cause == "model-not-found":
            # 404: el arreglo es editar el config, no reintentar. Dilo explícito.
            from scripts.lib import models as models_mod
            aviso = models_mod.describe(diag.get("model", ""))
            print(f"   {aviso}" if aviso else
                  f"   El modelo '{diag.get('model', '?')}' NO existe: ID mal escrito o "
                  f"retirado por el proveedor. Cambia compose.model en config.json por un "
                  f"ID vigente (p. ej. '{models_mod.SUGGESTED_DEFAULT}'); "
                  f"consúltalos en console.anthropic.com.")
        else:
            print("   Revisa el ID del modelo (console.anthropic.com), la clave y el saldo.")
        return 1
    print(f"{OK} Edición real compuesta: stub=False, {len(ed.get('stories', []))} "
          f"historia(s), JSON parseado. El camino LLM funciona en vivo.")
    return 0


def feeds() -> int:
    """Diagnóstico de FUENTES: ok / vacía / caída por feed. Reusa el `diagnostics` que ya
    calcula ingest, para que el operador vea en 5s por qué una edición salió corta (feed
    muerto) en vez de creer que 'no había noticias'. Toca la red (opt-in)."""
    import datetime as _dt
    from scripts.ingest import ingest
    op = os.path.join(ROOT, "config.json")
    cfg_path = op if os.path.exists(op) else os.path.join(ROOT, "fixtures", "config.json")
    cfg = _load_json(cfg_path)
    sources = cfg.get("sources", [])
    print("\nAutopress · doctor --feeds\n" + "-" * 40)
    if not sources:
        print(f"{WARN}No hay 'sources' en {os.path.basename(cfg_path)} (aún usas fixtures). "
              "Añade tus feeds RSS al config para diagnosticarlos.")
        return 0
    as_of = _dt.date.today().isoformat()
    diags: list = []
    ingest(sources, as_of, diagnostics=diags)
    icon = {"ok": OK, "empty": WARN, "error": BAD}
    for d in diags:
        line = f"{icon.get(d['status'], WARN)} {d.get('name') or d.get('url')}: " \
               f"{d['status']} ({d.get('count', 0)} ítems)"
        if d.get("status") == "error":
            line += f" — {d.get('error', '')}"
        print(line)
    down = [d for d in diags if d["status"] == "error"]
    print("-" * 40)
    print(f"{len(diags)} fuentes · {len(down)} caída(s).")
    return 1 if down else 0


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
        ("Modelo LLM", check_model()),
        ("IA en vivo", check_llm_ready()),
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
    if "--smoke" in sys.argv:
        sys.exit(smoke())
    if "--feeds" in sys.argv:
        sys.exit(feeds())
    sys.exit(main())
