"""settings — catálogo descubrible de TODO lo configurable.

Fuente única de verdad de "qué puedo configurar y dónde vive". La IA lo usa cuando el
operador dice "muéstrame los settings" / "qué puedo cambiar" / "ajusta el huso horario…".

    cd starter && PYTHONPATH=. python3 -m scripts.settings            # todo
    cd starter && PYTHONPATH=. python3 -m scripts.settings newsletter  # filtra

`scope` = dónde se toca cada cosa:
  config    → config.json            env      → .env (secretos)
  prompt    → prompts/master-prompt   workflow → .github/workflows/publish.yml
  host      → panel del host (decisión, no fichero)
"""
from __future__ import annotations
import json
import os

from scripts.render_demo import STYLES as _STYLES, PALETTES as _PALETTES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # starter/

# Opciones reales de tema (fuente única: las que implementa theme.css / render_demo).
_STYLE_KEYS = [k for k, _ in _STYLES]
_PALETTE_KEYS = [k for k, *_ in _PALETTES]

# key, categoría, scope, nivel, tipo, default, opciones (o None), descripción
SETTINGS = [
    # --- Identidad (nivel 0-2) ---
    ("site.name", "Identidad", "config", 0, "texto", "Mi medio", None, "Nombre del medio."),
    ("site.tagline", "Identidad", "config", 0, "texto", "", None, "Lema/subtítulo."),
    ("site.language", "Identidad", "config", 0, "texto", "es", None, "Idioma de publicación."),
    ("site.timezone", "Identidad", "config", 0, "texto", "UTC", None,
     "Huso horario de referencia del medio (p. ej. America/Mexico_City, Europe/Madrid)."),
    ("site.domain", "Identidad", "config", 2, "texto", "", None,
     "Dominio propio. Vacío = usas el subdominio gratis del host (no bloquea)."),
    # --- Diseño (nivel 0) ---
    ("site.theme.style", "Diseño", "config", 0, "opción", "editorial",
     _STYLE_KEYS, "Estilo visual (estructura+tipografía)."),
    ("site.theme.palette", "Diseño", "config", 0, "opción", "warm",
     _PALETTE_KEYS, "Paleta de color."),
    # --- Temática / contenido (nivel 3) ---
    ("taxonomy.topics", "Temática", "config", 3, "objeto", "{}", None,
     "Temas y sus palabras clave (clasificación)."),
    ("taxonomy.priority_topics", "Temática", "config", 3, "lista", "[]", None, "Temas que puntúan más."),
    ("taxonomy.markets", "Temática", "config", 3, "objeto", "{}", None,
     "Geografías (primary/secondary/…) con sus keywords."),
    ("taxonomy.players", "Temática", "config", 3, "objeto", "{}", None, "Actores/empresas a seguir."),
    # --- Fuentes (nivel 3) ---
    ("sources", "Fuentes", "config", 3, "lista", "(fixtures si vacío)", None,
     "Feeds RSS del medio. Sin esto, el pipeline usa los fixtures de demo."),
    ("ingest.lookback_days", "Fuentes", "config", 3, "entero", "8", None, "Ventana de recencia (días)."),
    ("ingest.max_per_source", "Fuentes", "config", 3, "entero", "20", None, "Tope de ítems por fuente."),
    # --- IA (nivel 3) ---
    ("compose.model", "IA", "config", 3, "texto", "claude-sonnet-5", None,
     "Modelo de IA que redacta (verifica el ID vigente)."),
    ("compose.max_tokens", "IA", "config", 3, "entero", "8000", None,
     "Tope de tokens de salida. En modelos con razonamiento adaptativo (p. ej. Sonnet 5) este tope se comparte con el 'thinking'; no lo bajes o la edición puede truncarse."),
    ("compose.thinking", "IA", "config", 3, "texto", "disabled", None,
     "Razonamiento del modelo: 'disabled' (por defecto, da todo max_tokens a la redacción) o 'adaptive'."),
    ("ANTHROPIC_API_KEY", "IA", "env", 3, "secreto", "", None,
     "Clave del modelo. Sin ella → modo stub (no gasta)."),
    # --- Riesgo / gobernanza (nivel 3) ---
    ("risk_profile", "Gobernanza", "config", 3, "opción", "review", ["auto", "review", "strict"],
     "Cuánta revisión: auto publica solo, review abre PR, strict exige corroboración."),
    ("publishing.min_independent_sources", "Gobernanza", "config", 3, "entero", "2", None,
     "En strict: fuentes de dominios independientes mínimas por historia."),
    ("publishing.block_stub_in_production", "Gobernanza", "config", 3, "bool", "true", None,
     "Un stub nunca llega a producción."),
    ("editorial.ai_disclosure", "Gobernanza", "config", 3, "bool", "true", None,
     "Declara públicamente que el contenido lo redacta una IA."),
    # --- Selección (avanzado) ---
    ("selection.competitor_blacklist", "Avanzado", "config", 3, "lista", "[]", None,
     "Términos que descartan una noticia (competidores)."),
    ("modes.target_normal", "Avanzado", "config", 3, "entero", "5", None, "Nº de historias objetivo por edición."),
    # --- Newsletter (nivel 5) ---
    ("RESEND_API_KEY", "Newsletter", "env", 5, "secreto", "", None, "Clave de Resend (envío)."),
    ("RESEND_AUDIENCE_ID", "Newsletter", "env", 5, "texto", "", None, "Lista de suscriptores."),
    ("NEWSLETTER_SECRET", "Newsletter", "env", 5, "secreto", "(autogenerado)", None,
     "Firma los enlaces de confirmación/baja (HMAC)."),
    ("TURNSTILE_SECRET_KEY", "Newsletter", "env", 5, "secreto", "", None, "Anti-bot del formulario (opcional)."),
    # --- Despliegue (nivel 1/4) ---
    ("host", "Despliegue", "host", 1, "decisión", "Cloudflare Pages", None,
     "Dónde publicas. Ver 04-DESPLIEGUE.md (recuerda el aviso de uso comercial)."),
    ("cron (agenda)", "Despliegue", "workflow", 4, "texto", "0 6 * * 1 (lun 06:00 UTC)", None,
     "Cuándo se publica sola. Se edita en .github/workflows/publish.yml."),
]

_REQUIRED_FIELDS = 8


def _current(config: dict, dotted: str):
    node = config
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def render(query: str = None, config: dict = None) -> str:
    q = (query or "").strip().lower()
    config = config or {}
    rows = [s for s in SETTINGS
            if not q or q in s[0].lower() or q in s[1].lower() or q in s[7].lower() or q == s[2]]
    if not rows:
        return f'No hay settings que coincidan con "{query}".'
    out = ["Settings de Autopress — 'scope' indica dónde se toca cada cosa.",
           "(config=config.json · env=.env · workflow=.github/… · host=panel del host)\n"]
    cat = None
    for key, category, scope, level, typ, default, options, desc in rows:
        if category != cat:
            cat = category
            out.append(f"▸ {category}")
        cur = _current(config, key) if scope == "config" else None
        val = f"actual={json.dumps(cur, ensure_ascii=False)}" if cur is not None else f"default={default}"
        opts = f" opciones={options}" if options else ""
        out.append(f"  · {key}  [{scope}·nivel {level}·{typ}]  {val}{opts}\n      {desc}")
    return "\n".join(out)


def main(argv):
    cfg = {}
    path = os.path.join(ROOT, "config.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            cfg = json.load(f)
    print(render(" ".join(argv[1:]) if len(argv) > 1 else None, cfg))
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv))
