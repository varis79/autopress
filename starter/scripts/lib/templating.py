"""Render determinista de la edición y de la galería de themes (solo stdlib).

El HTML lo produce el código, no el LLM. El theme se aplica por atributos
`data-style` / `data-palette` / `data-theme` en el elemento raíz + variables CSS.
"""
from __future__ import annotations
import html

from scripts.lib.text import safe_url
from scripts.lib.i18n import t


def _esc(s) -> str:
    return html.escape(s if s is not None else "")


# Página de inicio del proyecto (para el crédito del footer). Configurable por si el
# proyecto usa otro dominio; siempre OPCIONAL (editorial.attribution).
_AUTOPRESS_URL = "https://evaristobabe.com/resources/autopress"


def _footer_html(lang: str = "es", config: dict = None) -> str:
    config = config or {}
    ed = config.get("editorial", {})
    ai = ed.get("ai_disclosure", True)              # declara la IA (default sí)
    attribution = ed.get("attribution", True)       # crédito "Hecho con Autopress" (desmarcable)
    links = config.get("_legal_links", [])          # inyectado por publish/legal
    parts = []
    if ai:
        parts.append(_esc(t(lang, "footer_ai")))
    if attribution:
        url = safe_url(ed.get("attribution_url") or _AUTOPRESS_URL) or _AUTOPRESS_URL
        parts.append(f'{_esc(t(lang, "footer_made"))} '
                     f'<a href="{_esc(url)}" rel="noopener">Autopress</a>')
    legal = ""
    if links:
        items = " · ".join(f'<a href="{_esc(h)}">{_esc(l)}</a>' for l, h in links)
        legal = f'\n    <nav class="legal">{items}</nav>'
    return (
        '  <footer class="site">\n'
        f'    {" · ".join(parts)}{legal}\n'
        "  </footer>"
    )


def _newsletter_box(lang: str = "es") -> str:
    return (
        '  <aside class="nl">\n'
        f'    <p class="nl-eyebrow">{_esc(t(lang, "nl_eyebrow"))}</p>\n'
        f'    <h3 class="nl-title">{_esc(t(lang, "nl_title"))}</h3>\n'
        '    <form class="nl-form" method="post" action="/api/subscribe">\n'
        '      <input class="nl-input" type="email" name="email" required '
        f'placeholder="{_esc(t(lang, "nl_placeholder"))}" aria-label="email">\n'
        f'      <button class="nl-btn" type="submit">{_esc(t(lang, "nl_button"))}</button>\n'
        "    </form>\n"
        f'    <p class="nl-note">{_esc(t(lang, "nl_note"))}</p>\n'
        "  </aside>"
    )


def _cite_one(s) -> str:
    url = safe_url(s.get("url"))            # solo http/https; nunca javascript:/data:
    if not url:
        return f'<span class="cite">[{s.get("n")}]</span>'   # sin enlace si no es seguro
    return (f'<a href="{_esc(url)}" title="{_esc(s.get("name"))}" '
            f'rel="noopener nofollow" target="_blank">[{s.get("n")}]</a>')


def _cites(sources) -> str:
    """Citas numeradas [1][2]… enlazando a cada fuente original (solo esquemas seguros)."""
    if not sources:
        return ""
    return f'<sup class="cites">{"".join(_cite_one(s) for s in sources)}</sup>'


def edition_inner(ed: dict, lang: str = "es", newsletter: bool = False) -> str:
    """Masthead + portada + historias (con citas numeradas) + suscripción (si activa)."""
    stub = '<span class="stub">stub</span>' if ed.get("stub") else ""
    cov = ed.get("cover", {})
    cover_kicker = cov.get("kicker") or t(lang, "cover_kicker")
    stories = ed.get("stories", [])
    cards = []
    for s in stories[1:]:  # la portada es stories[0]; las tarjetas son el resto
        kicker = f'<p class="kicker">{_esc(s.get("topic"))}</p>\n  ' if s.get("topic") else ""
        market = f'<span class="tag">{_esc(s.get("market"))}</span>' if s.get("market") else ""
        cards.append(
            '<article class="card">\n  '
            + kicker
            + f'<h3>{_esc(s.get("headline"))}</h3>\n'
            f'  <p>{_esc(s.get("summary"))} {_cites(s.get("sources", []))}</p>\n'
            f'  <div class="meta">{market}</div>\n'
            "</article>"
        )
    return (
        '  <header class="masthead">\n'
        f'    <h1>{_esc(ed.get("title"))}</h1>\n'
        f'    <span class="date">{_esc(ed.get("date"))} {stub}</span>\n'
        "  </header>\n"
        '  <section class="cover">\n'
        f'    <p class="kicker">{_esc(cover_kicker)}</p>\n'
        f'    <h2>{_esc(cov.get("headline"))}</h2>\n'
        f'    <p class="deck">{_esc(cov.get("deck"))} {_cites(cov.get("sources", []))}</p>\n'
        "  </section>\n"
        '  <div class="stories">\n    ' + "\n    ".join(cards) + "\n  </div>\n"
        + (_newsletter_box(lang) if newsletter else "")   # el form solo si la newsletter está activa
    )


def render_edition(ed: dict, lang: str = "es") -> str:
    """Edición envuelta para la galería (con .wrap y footer). La galería muestra el
    diseño completo, incluida la caja de newsletter."""
    return ('<div class="wrap">\n' + edition_inner(ed, lang, newsletter=True) + "\n"
            + _footer_html(lang) + "\n</div>")


# ===== Galería de themes =====

_GALLERY_CHROME = """
.gal{position:sticky;top:0;z-index:20;background:#0e0e11;color:#fff;border-bottom:1px solid #222;
  font:14px/1.4 system-ui,-apple-system,'Segoe UI',sans-serif;padding:.7rem 1rem}
.gal-row{display:flex;gap:.55rem;align-items:center;flex-wrap:wrap;max-width:1120px;margin:0 auto}
.gal-row + .gal-row{margin-top:.55rem}
.gal-brand{font-weight:800;letter-spacing:.02em;margin-right:.3rem}
.gal-lab{font-size:.68rem;text-transform:uppercase;letter-spacing:.09em;opacity:.5;width:3rem}
.pill{font:inherit;font-size:.84rem;padding:.32rem .72rem;border-radius:999px;border:1px solid #333;
  background:#191920;color:#cfcfd6;cursor:pointer;transition:.12s}
.pill:hover{border-color:#666;color:#fff}
.pill.on{background:#fff;color:#111;border-color:#fff;font-weight:600}
.sw{display:inline-flex;align-items:center;gap:.42rem;font:inherit;font-size:.84rem;
  padding:.26rem .66rem .26rem .34rem;border-radius:999px;border:1px solid #333;background:#191920;
  color:#cfcfd6;cursor:pointer;transition:.12s}
.sw:hover{border-color:#666;color:#fff}
.sw.on{border-color:#fff;color:#fff;font-weight:600;box-shadow:0 0 0 1px #fff inset}
.sw .chip{width:1.05rem;height:1.05rem;border-radius:50%;box-shadow:inset 0 0 0 1px rgba(255,255,255,.22)}
.gal-spacer{margin-left:auto;display:flex;gap:.7rem;align-items:center}
.gal-count{font-size:.7rem;opacity:.5}
.gal-toggle{font:inherit;font-size:.82rem;padding:.32rem .72rem;border-radius:8px;border:1px solid #333;
  background:#191920;color:#fff;cursor:pointer}
.gal-toggle:hover{border-color:#666}
"""

_GALLERY_SCRIPT = """
<script>
  var r = document.documentElement;
  document.querySelectorAll('[data-kind]').forEach(function (b) {
    b.addEventListener('click', function () {
      var k = b.dataset.kind, v = b.dataset.value;
      r.dataset[k] = v;
      document.querySelectorAll('[data-kind="' + k + '"]').forEach(function (x) {
        x.classList.toggle('on', x === b);
      });
    });
  });
  var tb = document.getElementById('gal-toggle');
  tb.onclick = function () {
    var dark = r.dataset.theme === 'dark';
    r.dataset.theme = dark ? 'light' : 'dark';
    tb.textContent = dark ? '🌙 Oscuro' : '☀️ Claro';
  };
</script>
"""


def render_gallery(ed, css, styles, palettes, default_style, default_palette) -> str:
    """styles: [(key,label)]  ·  palettes: [(key,label,accent_hex,bg_hex)]."""
    style_pills = "".join(
        f'<button class="pill{" on" if k == default_style else ""}" '
        f'data-kind="style" data-value="{k}">{v}</button>'
        for k, v in styles
    )
    pal_sw = "".join(
        f'<button class="sw{" on" if k == default_palette else ""}" data-kind="palette" '
        f'data-value="{k}" title="{v}">'
        f'<span class="chip" style="background:linear-gradient(135deg,{bg} 50%,{ac} 50%)"></span>{v}</button>'
        for k, v, ac, bg in palettes
    )
    head = (
        '<!doctype html>\n'
        f'<html lang="es" data-style="{default_style}" data-palette="{default_palette}" data-theme="light">\n'
        '<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>Autopress · galería de estilos</title>\n<style>\n'
        + _GALLERY_CHROME + css + "\n</style>\n</head>\n<body>\n"
    )
    panel = (
        '<div class="gal">\n'
        '  <div class="gal-row">\n'
        '    <span class="gal-brand">Autopress</span>\n'
        '    <span class="gal-lab">Estilo</span>\n'
        f'    {style_pills}\n'
        '    <span class="gal-spacer"><button class="gal-toggle" id="gal-toggle">🌙 Oscuro</button></span>\n'
        '  </div>\n'
        '  <div class="gal-row">\n'
        '    <span class="gal-lab">Paleta</span>\n'
        f'    {pal_sw}\n'
        f'    <span class="gal-spacer"><span class="gal-count">{len(styles)}×{len(palettes)} = {len(styles) * len(palettes)} combinaciones</span></span>\n'
        '  </div>\n'
        '</div>\n'
    )
    return head + panel + render_edition(ed) + "\n" + _GALLERY_SCRIPT + "\n</body>\n</html>\n"
