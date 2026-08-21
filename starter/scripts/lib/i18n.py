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
        "tldr_heading": "La semana en breve",
        "sources_label": "fuentes",
        "nav_prev": "‹ Anterior", "nav_next": "Siguiente ›",
        "nav_method": "Metodología", "nav_about": "Acerca", "nav_sources": "Fuentes",
        "byline_curated": "Curado por", "byline_method": "cómo lo hacemos",
        "about_heading": "Acerca de este medio",
        "method_heading": "Cómo hacemos esto",
        "sources_heading": "Nuestras fuentes",
        "method_scope": "Este medio es un digest de curación: la IA redacta a partir del título y el resumen de cada fuente RSS —parafrasea y cita, no reproduce ni verifica el artículo completo.",
        "method_ai": "El contenido se redacta con asistencia de IA bajo supervisión humana.",
        "method_corrections": "¿Ves un error? Escríbenos y lo corregimos, señalando la corrección.",
        "method_cadence": "Cadencia", "method_risk": "Perfil de control",
        "method_sources_intro": "Curamos a partir de estas fuentes:",
        "risk_auto": "publicación automática en nichos inocuos",
        "risk_review": "cada edición pasa por revisión humana antes de indexarse",
        "risk_strict": "revisión humana + doble fuente independiente en temas sensibles",
        "cadence_weekly": "semanal",
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
        "tldr_heading": "The week in brief",
        "sources_label": "sources",
        "nav_prev": "‹ Previous", "nav_next": "Next ›",
        "nav_method": "Methodology", "nav_about": "About", "nav_sources": "Sources",
        "byline_curated": "Curated by", "byline_method": "how we do this",
        "about_heading": "About this outlet",
        "method_heading": "How we do this",
        "sources_heading": "Our sources",
        "method_scope": "This outlet is a curation digest: the AI writes from each RSS source's title and summary — it paraphrases and cites, it does not reproduce or verify the full article.",
        "method_ai": "Content is written with AI assistance under human oversight.",
        "method_corrections": "See an error? Email us and we'll fix it, flagging the correction.",
        "method_cadence": "Cadence", "method_risk": "Control profile",
        "method_sources_intro": "We curate from these sources:",
        "risk_auto": "automatic publishing in harmless niches",
        "risk_review": "every edition goes through human review before being indexed",
        "risk_strict": "human review + two independent sources on sensitive topics",
        "cadence_weekly": "weekly",
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
