"""Conocimiento de modelos LLM, mantenido a mano y actualizable con el kit.

`doctor` lo usa para avisar si el `compose.model` del config conviene cambiarlo.
No requiere red ni clave: es una lista determinista.

Dos niveles de aviso, y la diferencia le importa al operador:

  · **retirado** — el ID ya no existe. La API responde 404 y la edición cae a
    STUB: está roto AHORA y hay que editar el config.
  · **heredado** — sigue funcionando, pero hay una generación más nueva y
    recomendada (y, si Anthropic anunció fecha, dejará de funcionar ese día).

El nivel NO se escribe a mano: se deduce comparando la fecha de retirada
anunciada con la de hoy. Así un modelo con fecha futura pasa solo de "heredado"
a "retirado" el día que toca, aunque el operador lleve meses sin actualizar el
kit. Esta lista es la red de seguridad *preventiva*; la red que atrapa lo que no
esté aquí (un ID mal escrito, un modelo retirado después de esta versión) es el
404 que `compose` traduce a la causa `model-not-found`.

Mantenimiento (maintainers): cuando Anthropic depreca un ID o anuncia su
retirada, añádelo aquí con su reemplazo y la fecha (o None si aún no hay fecha).
Fuente: la página de deprecations de Anthropic. El operador lo recibe al correr
`python3 -m scripts.update` (llega con la siguiente versión del kit).
"""
from __future__ import annotations
import datetime as _dt

# ID heredado → (reemplazo vigente sugerido, fecha de retirada anunciada | None).
# Fechas en ISO (YYYY-MM-DD) según los anuncios de Anthropic. Se comparan como
# texto: en ISO el orden alfabético es el cronológico.
KNOWN: dict[str, tuple[str, str | None]] = {
    # --- Con fecha de retirada anunciada (ya pasada = retirado) ---
    "claude-2.0": ("claude-sonnet-5", "2025-07-21"),
    "claude-2.1": ("claude-sonnet-5", "2025-07-21"),
    "claude-3-sonnet-20240229": ("claude-sonnet-5", "2025-07-21"),
    "claude-3-5-sonnet-20240620": ("claude-sonnet-5", "2025-10-28"),
    "claude-3-5-sonnet-20241022": ("claude-sonnet-5", "2025-10-28"),
    "claude-3-opus-20240229": ("claude-opus-5", "2026-01-05"),
    "claude-3-5-haiku-20241022": ("claude-haiku-4-5", "2026-02-19"),
    "claude-3-7-sonnet-20250219": ("claude-sonnet-5", "2026-02-19"),
    "claude-3-haiku-20240307": ("claude-haiku-4-5", "2026-04-19"),
    "claude-opus-4-1": ("claude-opus-5", "2026-08-05"),
    "claude-opus-4-1-20250805": ("claude-opus-5", "2026-08-05"),
    # --- Deprecados sin fecha anunciada: funcionan, pero conviene moverse ---
    "claude-opus-4-0": ("claude-opus-5", None),
    "claude-opus-4-20250514": ("claude-opus-5", None),
    "claude-sonnet-4-0": ("claude-sonnet-5", None),
    "claude-sonnet-4-20250514": ("claude-sonnet-5", None),
}

# Reemplazo por defecto si no se reconoce el modelo pero se quiere sugerir uno.
SUGGESTED_DEFAULT = "claude-sonnet-5"

RETIRED = "retired"    # el ID ya no existe: 404
LEGACY = "legacy"      # funciona, pero hay algo más nuevo


def advisory(model: str, today: str | None = None) -> dict | None:
    """Aviso sobre `model`, o None si no hay nada que decir.

    Devuelve `{"model", "status", "replacement", "retires"}` con `status`
    RETIRED (la fecha anunciada ya pasó) o LEGACY. `today` (ISO) se puede
    inyectar en tests para no depender del calendario.

    Un modelo desconocido NO se marca (evita falsos positivos con IDs nuevos):
    solo avisamos de los que conocemos.
    """
    if not model:
        return None
    entry = KNOWN.get(model)
    if entry is None:
        return None
    replacement, retires = entry
    day = today or _dt.date.today().isoformat()
    status = RETIRED if (retires and retires <= day) else LEGACY
    return {"model": model, "status": status,
            "replacement": replacement, "retires": retires}


def superseded(model: str) -> str | None:
    """Reemplazo sugerido si hay aviso sobre `model`; None si no lo hay.

    Se mantiene por compatibilidad y para llamadas que solo quieren el "¿a qué
    lo cambio?". Para saber si está retirado o solo heredado, usa `advisory()`.
    """
    adv = advisory(model)
    return adv["replacement"] if adv else None


def describe(model: str, today: str | None = None) -> str | None:
    """Frase lista para enseñarle al operador, o None si no hay aviso."""
    adv = advisory(model, today)
    if adv is None:
        return None
    fix = f"cámbialo a '{adv['replacement']}' en config.json (compose.model)"
    if adv["status"] == RETIRED:
        # OJO: str.capitalize() minusculiza el resto de la frase (se comería un ID
        # con mayúsculas). Subimos solo la primera letra.
        return (f"'{model}' está RETIRADO (Anthropic lo retiró el {adv['retires']}): "
                f"la API responde 404 y tu edición saldría en STUB. "
                f"{fix[0].upper()}{fix[1:]}.")
    if adv["retires"]:
        return (f"'{model}' es un modelo heredado y dejará de funcionar el "
                f"{adv['retires']}: {fix} antes de esa fecha.")
    return (f"'{model}' es un modelo heredado (hay una generación más nueva y "
            f"recomendada): {fix}.")
