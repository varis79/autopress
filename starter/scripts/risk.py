"""risk — riesgo POR ARTÍCULO (determinista, ES+EN).

El perfil global (`risk_profile`) no basta: un medio inocuo puede toparse con una noticia
sensible (una acusación, salud, consejo financiero…). Este módulo etiqueta cada historia y
permite escalar su tratamiento AUNQUE el perfil global sea `auto`/`review`.

Regla dura (la más importante): una **acusación** (fraude, corrupción, delito…) NO se publica
si no está **atribuida** ("según…") y **corroborada** por ≥2 fuentes independientes.
"""
from __future__ import annotations
import re

from scripts.lib.text import kw_in

_LABELS = {
    "allegation": ["fraud", "fraude", "corrupt", "corrupción", "corrupto", "scam", "estafa",
                   "laundering", "blanqueo", "bribe", "bribery", "soborno", "cohecho",
                   "accused", "accusation", "acusa", "acusación", "acusado", "alleged",
                   "allegation", "presunto", "presunta", "presuntamente", "denuncia",
                   "denunciado", "imputado", "imputada", "embezzle", "embezzlement",
                   "malversación", "malversó", "desfalco",
                   # robo / apropiación
                   "steal", "stole", "stolen", "theft", "robó", "robar", "roban", "robo",
                   "hurto", "apropiación", "apropió", "misappropriat",
                   # otros delitos frecuentes en acusaciones
                   "crime", "delito", "criminal", "illegal", "ilegal", "abuse", "abuso",
                   "assault", "agresión", "harass", "acoso"],
    "health": ["cancer", "cáncer", "vaccine", "vacuna", "covid", "disease", "enfermedad",
               "treatment", "tratamiento", "cure", "cura", "clinical", "clínico", "symptom",
               "síntoma", "drug", "fármaco", "diagnosis", "diagnóstico"],
    "financial_advice": ["price target", "precio objetivo", "buy", "comprar", "sell", "vender",
                         "forecast", "pronóstico", "predict", "predicción", "bull", "bear",
                         "rally", "invertir", "inversión rentable"],
    "politics": ["election", "elección", "elecciones", "president", "presidente", "minister",
                 "ministro", "gobierno", "government", "senate", "senado", "congreso",
                 "parliament", "parlamento", "vote", "voto", "party", "partido"],
    "violence": ["kill", "killed", "murder", "asesinato", "asesinado", "attack", "atentado",
                 "shooting", "tiroteo", "terror", "terrorismo", "war crime", "masacre"],
    "minor": ["child", "niño", "niña", "menor", "menores", "teenager", "adolescente", "minor"],
    "rumor": ["rumor", "rumour", "leak", "filtración", "unconfirmed", "sin confirmar",
              "reportedly", "al parecer", "sources say", "fuentes dicen", "supposedly"],
}

# Atribución = APUNTAR A UNA FUENTE, no adjetivar la propia acusación. Por eso NO valen aquí
# 'presunto/alleged' (hedge sin fuente) ni 'acusa/denuncia' (son los propios disparadores de la
# etiqueta `allegation`): usarlos como atribución hacía el guardarraíl circular ("El presunto
# fraude…" se auto-atribuía). Solo cuentan marcas que nombran o citan a alguien.
_ATTRIBUTION = ["según", "de acuerdo con", "according to", "reportedly", "al parecer",
                "sources say", "fuentes", "afirma", "afirmó", "asegura", "aseguró",
                "sostiene", "sostuvo", "informa", "informó", "claims", "said"]

# Etiquetas que, sin atribución + corroboración, NO deben publicarse.
BLOCKING_LABELS = {"allegation"}


def tags(text: str) -> set:
    """Etiquetas de riesgo presentes en el texto."""
    return {label for label, words in _LABELS.items() if any(kw_in(text, w) for w in words)}


def has_attribution(text: str) -> bool:
    low = (text or "").lower()
    return any(a in low for a in _ATTRIBUTION)
