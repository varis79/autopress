"""i18n — textos del 'chrome' del medio por idioma.

El CONTENIDO de la edición lo redacta la IA en `site.language` (vía master-prompt). Aquí
van solo los textos fijos que pinta el código (nav, footer, caja de newsletter, archivo),
para que un medio en inglés se vea entero en inglés. Añadir un idioma = añadir su bloque.
"""
from __future__ import annotations

STRINGS = {
    "es": {
        "nav_latest": "Última", "nav_archive": "Archivo",
        "footer_ai": "Contenido redactado con asistencia de IA",
        "footer_made": "Hecho con",
        "nl_eyebrow": "Boletín semanal · gratis",
        "nl_title": "Recíbelo cada lunes en tu correo",
        "nl_placeholder": "tu@correo.com",
        "nl_button": "Suscribirme",
        "nl_note": "Sin spam · sin ventas · cancela cuando quieras",
        "cover_kicker": "En portada",
        "archive_heading": "Archivo",
        "archive_intro": "Todas las ediciones publicadas.",
        "archive_desc": "Todas las ediciones.",
    },
    "en": {
        "nav_latest": "Latest", "nav_archive": "Archive",
        "footer_ai": "Content written with AI assistance",
        "footer_made": "Made with",
        "nl_eyebrow": "Weekly newsletter · free",
        "nl_title": "Get it in your inbox every Monday",
        "nl_placeholder": "you@email.com",
        "nl_button": "Subscribe",
        "nl_note": "No spam · no selling · unsubscribe anytime",
        "cover_kicker": "On the cover",
        "archive_heading": "Archive",
        "archive_intro": "All published editions.",
        "archive_desc": "All editions.",
    },
}


def base_lang(lang: str) -> str:
    """Normaliza a idioma base BCP-47: 'en-US'/'English'→'en', 'es_ES'→'es'."""
    return (lang or "en").replace("_", "-").split("-")[0].lower()[:2]


def t(lang: str, key: str) -> str:
    """Texto de `key` en `lang`. Idioma desconocido → inglés (default internacional);
    clave ausente → se intenta en inglés, y si no, la propia clave."""
    base = STRINGS.get(base_lang(lang)) or STRINGS["en"]
    return base.get(key) or STRINGS["en"].get(key, key)
