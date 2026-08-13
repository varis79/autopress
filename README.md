# Autopress

> 🌐 **English:** [README in English](en/README.md) · guides in [`en/`](en/README.md)

**Hazte tu propio digest de noticias asistido por IA.** Autopress es un kit gratuito y abierto
para montar, con la ayuda de un agente de IA, un **boletín de noticias curadas que se genera
solo, con revisión humana por defecto**: ingiere **feeds RSS** (titulares y resúmenes), los
cura, redacta una edición semanal y la publica como sitio web estático — sobre la temática que
tú elijas. Newsletter opcional (montas tú el endpoint).

> **Sé consciente de dos cosas (honestidad primero):** (1) redacta a partir de los **resúmenes
> de RSS**, no del artículo completo — es un *digest* con criterio, no un periódico que "lee" la
> noticia; **parafrasea y cita**, no verifica el sentido de cada cifra. (2) **Autonomía = la
> generación**, no el criterio: por defecto **nada se indexa sin tu aprobación** (`review`), y
> tú sigues siendo el editor y el responsable legal. El coste en API es de céntimos; el coste
> real es **tu atención** (revisar, derechos de fuentes, correcciones).

> **Estado:** motor y guardarraíles maduros (pipeline, gobernanza review-first, CI, SEO, legal,
> asistente, bilingüe); 4 revisiones externas. Pendiente: fase "medio de verdad" (leer el
> artículo real + evidencia por afirmación) y el endpoint real de newsletter. Detalle en
> `PROGRESO.md`.

---

## Qué es

- Un **blueprint** genérico y sin secretos + un **starter** (andamiaje que un agente de IA
  usa para construir tu medio) + guías para no-técnicos.
- Para **medios de curación de noticias**: cualquier tema con **flujo vivo de fuentes**
  (ciberseguridad, agricultura, geopolítica de actualidad, energía, flotas…). La temática la
  eliges tú en un cuestionario de arranque. **No** es para temas estáticos/históricos ni para
  revistas de ensayo generado por IA — ver `01-ANTES-DE-EMPEZAR.md`.
- **Barato en dinero** (una edición semanal: **~$0,30–$1,20/mes** en API + stack gratis), pero
  **no gratis en tiempo:** el coste dominante es **tu atención** como editor/responsable
  (revisar cada edición, derechos de las fuentes, correcciones, vigilar fallos).

## Para quién NO es (honestidad primero)

- Si solo quieres una newsletter simple, **usa Ghost, Substack o Beehiiv** — más fácil, sin
  montar nada. Autopress tiene sentido cuando quieres **un medio propio, curado y con SEO**,
  que controlas tú.
- **No es magia sin manos:** necesitas un **agente de código con acceso a terminal y repo**
  (Claude Code, Cursor…) para construirlo, y crear unas cuentas gratuitas (GitHub, un host,
  Resend). El agente hace el trabajo técnico; tú decides y supervisas.
- **La autonomía es de la edición semanal, no del criterio editorial.** Tú fijas las reglas,
  las fuentes y la línea; revisas cuando el tema es sensible.

## Qué contiene

```
README.md              · Esto
AGENTS.md              · Punto de entrada del kit + cuestionario (para tu agente)
00-QUICKSTART.md       · De cero a tu primera edición (por niveles, nada bloquea)
01-ANTES-DE-EMPEZAR.md · ¿Es para ti? Alternativas honestas
02-CUENTAS-Y-DOMINIO   · Cuentas, DNS, SPF/DKIM/DMARC
03-COSTES.md           · Coste real + fórmula + puntos de ruptura
04-DESPLIEGUE.md       · Publica donde quieras (comparativa de hosts + CI)
05-CUESTIONARIO.md     · El intake que define tu medio
06-ADAPTACION-TEMATICA · Playbooks por tipo de tema
07-GUARDARRAILES.md    · Estándares editoriales (lo impuesto por código + política)
08-MODO-INDEPENDIENTE  · Independiente + monetización honesta
10-SEO.md · 12-TROUBLESHOOTING.md
BLUEPRINT-MEDIO-AUTONOMO.md · El plano técnico completo
starter/               · ⭐ El proyecto ejecutable (AGENTS.md, scripts/, tests/…)
  scripts/setup.py     · asistente · serve.py · preview · settings.py · catálogo
  legal/ · newsletter/ · examples/movilidad-mx-es/ (caso trabajado)
```

## Empezar

> 🚀 **Guía de arranque + prompt de inicio:** [EMPIEZA-AQUI.md](EMPIEZA-AQUI.md).

1. Descarga el kit (o usa "Use this template" en GitHub).
2. Ábrelo con tu agente de IA (Claude Code / Cursor). Lee **`starter/AGENTS.md`**, te hace el
   cuestionario y construye tu medio.
3. ¿Prefieres a mano? `cd starter && PYTHONPATH=. python3 -m scripts.setup` (asistente) y
   `python3 -m scripts.serve` (previsualiza). O di *"muéstrame los settings"*.

**Nada es obligatorio de golpe:** avanzas por niveles (local → online → dominio → feeds/IA →
automático → newsletter → monetizas) y cada uno funciona solo. Sin dominio usas el subdominio
del host; sin clave de IA ves el medio en modo demo.

## Decisiones clave del kit

- **SEO correcto siempre; nunca inundar Google.** La generación masiva de páginas está
  **desactivada por defecto**; solo se indexan páginas que superan un umbral de calidad.
- **Rigor por defecto:** fuentes citadas, revisión humana disponible, sin cifras inventadas.
  Genérico — no atado a ninguna temática.
- **Sitio estático portable**: despliega en cualquier host. Recomendado **Cloudflare Pages**
  (gratis y permite monetizar); **GitHub Pages** y **Vercel Hobby** prohíben uso comercial en
  gratis. El agente verifica los ToS vigentes al construir. Ver `04-DESPLIEGUE.md`.

## Licencia

- **Documentación:** CC BY 4.0.
- **Código del `starter/`:** MIT.

Cada medio construido con Autopress enlaza (de forma opcional y desmarcable) a la web del
autor del kit — un pequeño crédito que ayuda a que otros lo encuentren.

---

_Proyecto derivado de un medio editorial autónomo real, sanitizado y generalizado para que
cualquiera pueda montar el suyo._
