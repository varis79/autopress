"""Conocimiento de modelos LLM, mantenido a mano y actualizable con el kit.

`doctor` lo usa para avisar si el `compose.model` del config es un modelo
**heredado** (una generación antigua que conviene actualizar). No requiere red ni
clave: es una lista determinista.

Mantenimiento (maintainers): cuando Anthropic saca una generación nueva o depreca
un ID, añádelo aquí con su reemplazo sugerido. El operador lo recibe al correr
`python3 -m scripts.update` (llega con la siguiente versión del kit).
"""
from __future__ import annotations

# ID heredado/superado  →  reemplazo vigente sugerido.
# (No afirmamos fecha exacta de retirada; solo "hay algo más nuevo y recomendado".)
SUPERSEDED = {
    "claude-3-opus-20240229": "claude-opus-5",
    "claude-3-sonnet-20240229": "claude-sonnet-5",
    "claude-3-haiku-20240307": "claude-haiku-4-5",
    "claude-3-5-sonnet-20240620": "claude-sonnet-5",
    "claude-3-5-sonnet-20241022": "claude-sonnet-5",
    "claude-3-5-haiku-20241022": "claude-haiku-4-5",
    "claude-3-7-sonnet-20250219": "claude-sonnet-5",
}

# Reemplazo por defecto si no se reconoce el modelo pero se quiere sugerir uno.
SUGGESTED_DEFAULT = "claude-sonnet-5"


def superseded(model: str) -> str | None:
    """Reemplazo sugerido si `model` es heredado; None si no hay aviso.

    Un modelo desconocido NO se marca (evita falsos positivos con IDs nuevos):
    solo avisamos de los que sabemos que están superados.
    """
    if not model:
        return None
    return SUPERSEDED.get(model)
