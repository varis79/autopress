"""Valida un fichero de configuración contra autopress.schema.json.

Uso:
    cd starter && python3 scripts/validate_config.py fixtures/config.json

- Si la librería `jsonschema` está instalada, hace validación completa del
  esquema (recomendado).
- Si no, usa una comprobación estructural mínima (solo stdlib) para que
  funcione en cualquier sitio sin dependencias.
- Soporta JSON siempre; YAML solo si `pyyaml` está instalado.

Salida: lista de errores (o "OK") y código de salida 0/1.
"""
from __future__ import annotations
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # starter/
SCHEMA_PATH = os.path.join(ROOT, "autopress.schema.json")


def load_config(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        if path.endswith((".yml", ".yaml")):
            try:
                import yaml  # type: ignore
            except ImportError:
                raise SystemExit("ERROR: el config es YAML pero falta pyyaml. Instálalo o usa JSON.")
            return yaml.safe_load(f)
        return json.load(f)


def _structural_check(cfg: dict) -> list[str]:
    """Comprobación mínima sin jsonschema (solo lo esencial)."""
    errors: list[str] = []

    def require(cond: bool, msg: str):
        if not cond:
            errors.append(msg)

    require(isinstance(cfg, dict), "El config debe ser un objeto.")
    if not isinstance(cfg, dict):
        return errors

    for key in ("taxonomy", "selection", "modes"):
        require(key in cfg, f"Falta la sección obligatoria '{key}'.")

    tax = cfg.get("taxonomy", {})
    require(isinstance(tax.get("topics"), dict) and tax.get("topics"),
            "taxonomy.topics debe ser un objeto no vacío.")
    require(isinstance(tax.get("markets"), dict) and tax.get("markets"),
            "taxonomy.markets debe ser un objeto no vacío.")
    for m, mc in (tax.get("markets") or {}).items():
        require(isinstance(mc, dict) and mc.get("tier") in ("primary", "secondary", "tertiary", "other"),
                f"taxonomy.markets.{m}.tier inválido.")
        require(isinstance(mc.get("keywords"), list) and mc.get("keywords"),
                f"taxonomy.markets.{m}.keywords debe ser una lista no vacía.")

    sel = cfg.get("selection", {})
    sc = sel.get("scoring", {})
    for f in ("topic_match", "market_primary", "recency_max_bonus", "recency_decay_per_day"):
        require(isinstance(sc.get(f), (int, float)), f"selection.scoring.{f} debe ser numérico.")

    modes = cfg.get("modes", {})
    for f in ("target_normal", "min_normal", "min_short"):
        require(isinstance(modes.get(f), int), f"modes.{f} debe ser un entero.")

    rp = cfg.get("risk_profile")
    require(rp in (None, "auto", "review", "strict"), "risk_profile debe ser auto|review|strict.")
    return errors


def validate_dict(cfg: dict) -> list[str]:
    """Valida un config ya cargado (dict). Devuelve lista de errores ([] = válido)."""
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)
    try:
        import jsonschema  # type: ignore
        validator = jsonschema.Draft202012Validator(schema)
        return [f"{list(e.path)}: {e.message}" for e in sorted(validator.iter_errors(cfg), key=str)]
    except ImportError:
        return _structural_check(cfg)


def validate(path: str) -> list[str]:
    return validate_dict(load_config(path))


def main(argv) -> int:
    if len(argv) < 2:
        print("Uso: python3 scripts/validate_config.py <ruta-config>")
        return 2
    errors = validate(argv[1])
    if errors:
        print(f"❌ Config inválida ({len(errors)} problema/s):")
        for e in errors:
            print(f"  · {e}")
        return 1
    engine = "jsonschema" if "jsonschema" in sys.modules else "structural (sin jsonschema)"
    print(f"✅ Config válida — {argv[1]}  [{engine}]")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
