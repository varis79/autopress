"""Renderiza la edición demo y la galería navegable de themes (6 estilos × 5 paletas).

Sin cuentas, sin claves, sin LLM (modo stub). Uso:
    cd starter && PYTHONPATH=. python3 -m scripts.render_demo
Genera: sample-output/gallery.html  (autocontenida, para incrustar en una web).
"""
from __future__ import annotations
import json
import os

from scripts.pipeline_core import run_full
from scripts.compose_stub import compose_stub
from scripts.lib.templating import render_gallery

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # starter/

# 6 estilos × 5 paletas = 30 combinaciones. Cada paleta lleva (accent, bg) para el swatch.
STYLES = [
    ("editorial", "Editorial"),
    ("modern", "Modern"),
    ("technical", "Technical"),
    ("magazine", "Magazine"),
    ("minimal", "Minimal"),
    ("newsprint", "Newsprint"),
]
PALETTES = [
    ("ink", "Ink", "#c0271e", "#ffffff"),
    ("warm", "Warm", "#b4532a", "#f5f1e8"),
    ("cool", "Cool", "#2563b8", "#f4f6f9"),
    ("forest", "Forest", "#2f6b3f", "#f1f4ee"),
    ("signal", "Signal", "#e5004c", "#faf9fb"),
]


def _load_jsonl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def main():
    raw = _load_jsonl(os.path.join(ROOT, "fixtures", "raw.jsonl"))
    with open(os.path.join(ROOT, "fixtures", "config.json"), encoding="utf-8") as f:
        config = json.load(f)

    selection, deduped = run_full(raw, config)
    by_id = {it["id"]: it for it in deduped}
    edition = compose_stub(selection, by_id,
                           {"title": "El Radar Semanal", "date": config.get("as_of", "")})

    with open(os.path.join(ROOT, "theme", "theme.css"), encoding="utf-8") as f:
        css = f.read()

    out_dir = os.path.join(ROOT, "sample-output")
    os.makedirs(out_dir, exist_ok=True)
    html = render_gallery(edition, css, STYLES, PALETTES,
                          default_style="editorial", default_palette="warm")
    out = os.path.join(out_dir, "gallery.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ {out} ({len(html)} bytes) · {len(STYLES)}×{len(PALETTES)}="
          f"{len(STYLES) * len(PALETTES)} combinaciones · edición {selection['mode']} de {selection['count']} historias")


if __name__ == "__main__":
    main()
