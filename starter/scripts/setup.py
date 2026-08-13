"""setup — asistente de configuración (incremental: NADA es obligatorio).

Hace las preguntas del cuestionario y te escribe `config.json`, `prompts/master-prompt.md`
y `.env`. Puedes saltarte lo que no tengas (dominio, feeds, clave de IA…) y añadirlo luego:
el kit funciona en cada nivel.

    cd starter && PYTHONPATH=. python3 -m scripts.setup

La lógica de construcción (`build_config`, `render_master_prompt`) es pura y testeable;
`main()` solo recoge respuestas y escribe ficheros.
"""
from __future__ import annotations
import copy
import datetime as dt
import getpass
import json
import os
import re
import secrets

from scripts.lib.i18n import base_lang

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # starter/


# Defaults NEUTROS de producción (NO los fixtures: la taxonomía sale de las respuestas).
_DEFAULTS = {
    "dedupe": {"title_similarity_threshold": 0.82},
    "selection": {
        "competitor_blacklist": [],
        "scoring": {"topic_match": 1.0, "topic_priority_boost": 0.5, "market_primary": 1.2,
                    "market_secondary": 0.4, "market_tertiary": 0.3, "market_other": 0.15,
                    "players_base": 0.5, "players_extra": 0.1, "players_max_extra": 3,
                    "recency_max_bonus": 2.0, "recency_decay_per_day": 0.2},
        "geo_quotas": {"primary": [0, 5], "secondary": [0, 2], "other": [0, 2]},
        "topic_quotas": {},
    },
    "modes": {"target_normal": 5, "min_normal": 4, "min_short": 2},
    "compose": {"model": "claude-sonnet-5", "max_tokens": 8000},
}


def _taxonomy(answers: dict):
    """Taxonomía a partir de las respuestas del operador. Si no hay temas/mercados, deja un
    placeholder y marca `needs_taxonomy` (el pipeline NO publica en producción con placeholder)."""
    topics = {t.strip().lower(): [t.strip().lower()] for t in answers.get("topics", []) if t.strip()}
    markets = {m.strip().lower(): {"tier": "primary", "keywords": [m.strip().lower()]}
               for m in answers.get("markets", []) if m.strip()}
    players = {p.strip(): [p.strip().lower()] for p in answers.get("players", []) if p.strip()}
    needs = not topics or not markets
    tax = {
        "topics": topics or {"general": ["general"]},
        "priority_topics": [],
        "markets": markets or {"global": {"tier": "primary", "keywords": ["global"]}},
        "players": players,
    }
    return tax, needs


def build_config(answers: dict) -> dict:
    """Config de producción desde defaults neutros + respuestas. La taxonomía viene del
    operador (nunca de los fixtures). Marca `meta.origin` y `meta.needs_taxonomy`."""
    cfg = copy.deepcopy(_DEFAULTS)
    tax, needs = _taxonomy(answers)
    cfg["taxonomy"] = tax
    cfg["risk_profile"] = answers.get("risk_profile") or "review"
    cfg["site"] = {
        "name": answers.get("name") or "Mi medio",
        "tagline": answers.get("tagline") or "",
        "domain": answers.get("domain") or "",   # vacío = usa el subdominio gratis del host
        "language": answers.get("language") or "es",
        "theme": {"style": answers.get("style") or "editorial",
                  "palette": answers.get("palette") or "warm"},
    }
    if answers.get("sources"):                   # sin feeds → el pipeline usa fixtures
        cfg["sources"] = answers["sources"]
    cfg["meta"] = {"origin": "setup", "needs_taxonomy": needs}
    return cfg


def fill_legal(answers: dict, root: str) -> list:
    """Rellena las plantillas legales (del idioma del medio) con las respuestas → deja las
    páginas legales listas (sin placeholders), así producción no queda bloqueada. Siguen
    trayendo el aviso 'no es asesoría legal': el operador debería revisarlas."""
    name = answers.get("name") or "Mi medio"
    topic = answers.get("topic") or name
    publisher = answers.get("publisher") or name
    email = answers.get("email") or "contacto@ejemplo.com"
    country = answers.get("country") or "—"
    domain = answers.get("domain") or ""
    host = answers.get("host") or "Cloudflare Pages"
    today = dt.date.today().isoformat()
    vals = {
        "NOMBRE_MEDIO": name, "MEDIA_NAME": name, "TEMA": topic, "TOPIC": topic,
        "IDIOMA": answers.get("language") or "es",
        "RESPONSABLE": publisher, "PUBLISHER": publisher, "CONTROLLER": publisher,
        "EDITOR_IN_CHARGE": publisher,
        "EMAIL_CONTACTO": email, "CONTACT_EMAIL": email,
        "FECHA": today, "DATE": today,
        "DOMICILIO_O_PAIS": country, "ADDRESS_OR_COUNTRY": country,
        "DOMINIO": domain, "DOMAIN": domain,
        "PROVEEDOR_NEWSLETTER": "Resend", "NEWSLETTER_PROVIDER": "Resend",
        "PROVEEDOR_HOSTING": host, "HOSTING_PROVIDER": host,
        "PLAZO": "72 h", "TIMEFRAME": "72h",
        "LICENCIA_CONTENIDO": "CC BY 4.0", "CONTENT_LICENSE": "CC BY 4.0",
    }
    lang = base_lang(answers.get("language") or "es")
    ldir = os.path.join(root, "legal", lang)
    if not os.path.isdir(ldir):
        ldir = os.path.join(root, "legal")
    written = []
    for fn in ("privacidad.md", "divulgacion-ia.md", "derechos-fuentes.md", "terminos.md"):
        path = os.path.join(ldir, fn)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for key, val in vals.items():
            text = re.sub(r"<" + key + r"[^>]*>", val, text)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        written.append(os.path.relpath(path, root))
    return written


def render_master_prompt(answers: dict, template: str) -> str:
    repl = {
        "<NOMBRE_MEDIO>": answers.get("name") or "Mi medio",
        "<IDIOMA>": answers.get("language") or "es",
        "<TEMA>": answers.get("topic") or "<TEMA>",
        "<TONO>": answers.get("tone") or "sobrio, analítico y sin hype",
        "<MERCADOS>": answers.get("markets_str") or "<MERCADOS>",
    }
    out = template
    for k, v in repl.items():
        out = out.replace(k, v)
    return out


def unlocked_level(answers: dict) -> str:
    """Nivel alcanzado con lo que hay (mensaje motivador, incremental)."""
    if answers.get("domain") and answers.get("api_key"):
        return "3+ · feeds/IA listos y dominio propio"
    if answers.get("api_key") or answers.get("sources"):
        return "3 · feeds reales / IA (redacción de verdad)"
    if answers.get("name"):
        return "0-1 · tu medio corre en local y puede subirse online (subdominio gratis)"
    return "0 · demo local"


# ---------- interactivo ----------

def _ask(prompt: str, default: str = "") -> str:
    hint = f" [{default}]" if default else " (opcional, Enter para saltar)"
    try:
        val = input(f"· {prompt}{hint}: ").strip()
    except EOFError:
        val = ""
    return val or default


def _write(path: str, content: str, label: str):
    if os.path.exists(path):
        if _ask(f"{label} ya existe. ¿Sobrescribir? (s/N)", "N").lower() not in ("s", "si", "sí", "y"):
            print(f"  ↳ conservado {label}")
            return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ escrito {label}")


def main():
    print("\n=== Autopress · asistente de configuración ===")
    print("Nada es obligatorio: salta lo que no tengas (Enter) y añádelo luego.\n")

    with open(os.path.join(ROOT, "prompts", "master-prompt.example.md"), encoding="utf-8") as f:
        template = f.read()

    def _csv(s):
        return [x.strip() for x in (s or "").split(",") if x.strip()]

    a = {}
    a["name"] = _ask("Nombre del medio", "Mi medio")
    a["tagline"] = _ask("Lema / tagline")
    a["topic"] = _ask("Temática (de qué va)")
    a["language"] = _ask("Idioma", "es")
    a["tone"] = _ask("Tono/voz")
    a["topics"] = _csv(_ask("Temas/keywords principales, separados por coma (p. ej. regulación, baterías)"))
    a["markets_str"] = _ask("Mercados/geografías (p. ej. México, España)")
    a["markets"] = _csv(a["markets_str"])
    a["players"] = _csv(_ask("Actores/empresas a seguir, separados por coma (opcional)"))
    a["risk_profile"] = _ask("Perfil de riesgo (auto/review/strict)", "review")
    a["domain"] = _ask("Dominio propio (si ya lo tienes)")
    # Datos para rellenar los legales automáticamente (siguen siendo revisables):
    a["email"] = _ask("Email de contacto (privacidad y retiradas)")
    a["publisher"] = _ask("Responsable/editor (nombre)", a.get("name") or "Mi medio")
    a["country"] = _ask("País/jurisdicción")
    a["host"] = _ask("Host previsto", "Cloudflare Pages")
    feeds = _ask("URLs de feeds RSS separadas por coma (si ya las tienes)")
    if feeds:
        a["sources"] = [{"name": u.split("//")[-1].split("/")[0], "url": u.strip()}
                        for u in feeds.split(",") if u.strip()]
    # La clave NO se muestra por pantalla (getpass). Mejor aún: ponla directamente en los
    # secrets de GitHub/host y déjala vacía aquí. Nunca la pegues en el chat de tu agente.
    try:
        a["api_key"] = getpass.getpass("· Clave de IA ANTHROPIC_API_KEY (oculta, Enter para saltar): ").strip()
    except (EOFError, KeyboardInterrupt):
        a["api_key"] = ""

    # Escribir ficheros
    print("\nEscribiendo configuración…")
    cfg = build_config(a)
    _write(os.path.join(ROOT, "config.json"),
           json.dumps(cfg, ensure_ascii=False, indent=2), "config.json")
    if cfg["meta"]["needs_taxonomy"]:
        print("  ⚠️  Sin temas o mercados: se dejó una taxonomía placeholder. NO se publicará en "
              "producción hasta que la definas (o pídele a tu agente que la genere para tu tema).")
    # Rellenar los legales automáticamente (quedan listos; revísalos igualmente).
    filled = fill_legal(a, ROOT)
    if filled:
        print(f"  ✓ legales rellenados: {', '.join(filled)}  (revísalos: no son asesoría legal)")
    _write(os.path.join(ROOT, "prompts", "master-prompt.md"),
           render_master_prompt(a, template), "prompts/master-prompt.md")

    # .env a partir del ejemplo, rellenando lo que haya (+ NEWSLETTER_SECRET generado)
    with open(os.path.join(ROOT, ".env.example"), encoding="utf-8") as f:
        env_lines = f.read().splitlines()
    filled = []
    for line in env_lines:
        if line.startswith("ANTHROPIC_API_KEY=") and a.get("api_key"):
            filled.append("ANTHROPIC_API_KEY=" + a["api_key"])
        elif line.startswith("NEWSLETTER_SECRET="):
            filled.append("NEWSLETTER_SECRET=" + secrets.token_hex(32))
        else:
            filled.append(line)
    _write(os.path.join(ROOT, ".env"), "\n".join(filled) + "\n", ".env")

    print(f"\n🎉 Nivel desbloqueado: {unlocked_level(a)}")
    print("Siguiente: previsualiza con  →  PYTHONPATH=. python3 -m scripts.serve")
    print("(Refina la taxonomía/keywords del config.json con tu agente cuando quieras.)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
