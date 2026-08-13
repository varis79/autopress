"""Utilidades de texto deterministas (solo stdlib).

Coincidencia de keywords con *word-boundary* Unicode (evita falsos positivos
como 'ley' dentro de 'ballena') y normalización canónica de URLs.
"""
from __future__ import annotations
import re
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode


def kw_in(text: str, keyword: str) -> bool:
    """True si `keyword` aparece como término completo en `text` (case-insensitive)."""
    if not keyword:
        return False
    pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"
    return re.search(pattern, text or "", re.IGNORECASE | re.UNICODE) is not None


def count_kw(text: str, keywords) -> int:
    """Número de keywords de la lista que aparecen en el texto."""
    return sum(1 for k in keywords if kw_in(text, k))


def canonical_url(url: str) -> str:
    """URL canónica: host en minúsculas, sin barra final, sin parámetros utm_*."""
    try:
        p = urlsplit(url)
        q = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
             if not k.lower().startswith("utm_")]
        return urlunsplit((p.scheme.lower(), p.netloc.lower(),
                           p.path.rstrip("/"), urlencode(q), ""))
    except Exception:
        return url or ""


_SECOND_LEVEL = {"co", "com", "org", "gov", "net", "ac", "edu"}


def registrable_domain(url: str) -> str:
    """Dominio registrable aproximado (eTLD+1) del host, p. ej. `ex.com`, `bbc.co.uk`.
    Sirve para contar fuentes INDEPENDIENTES: dos URLs del mismo dominio son el mismo
    editor (no corroboran de forma independiente). Heurística sin lista de sufijos
    públicos; suficiente para el guardarraíl de `strict`."""
    try:
        host = urlsplit(url).netloc.lower().split(":")[0]
    except Exception:
        return ""
    if host.startswith("www."):
        host = host[4:]
    labels = [x for x in host.split(".") if x]
    if not labels:
        return ""
    if len(labels) >= 3 and labels[-2] in _SECOND_LEVEL and len(labels[-1]) == 2:
        return ".".join(labels[-3:])          # bbc.co.uk, empresa.com.mx …
    return ".".join(labels[-2:]) if len(labels) >= 2 else labels[-1]


def safe_url(url: str) -> str:
    """Devuelve la URL solo si su esquema es http/https; si no, cadena vacía.
    Neutraliza `javascript:`, `data:`, `file:` etc. en href y en citas (una fuente
    RSS no confiable no debe poder inyectar un esquema activo)."""
    try:
        return url if urlsplit(url).scheme.lower() in ("http", "https") else ""
    except Exception:
        return ""


_SEP_BEFORE_DIGIT = re.compile(r"[\s., ](?=\d)")
_DIGIT_RUN = re.compile(r"\d+")


def number_tokens(text: str, min_len: int = 2) -> set:
    """Secuencias de dígitos (>= min_len) tras unir separadores de miles/decimales
    (`1.000`→`1000`, `3,5`→`35`, `87%`→`87`). Se usa para verificar que una cifra de
    la redacción aparece en la fuente (check anti-invención). Se ignoran dígitos
    sueltos para no bloquear por falsos positivos."""
    cleaned = _SEP_BEFORE_DIGIT.sub("", text or "")
    return {m.group(0) for m in _DIGIT_RUN.finditer(cleaned) if len(m.group(0)) >= min_len}
