# Copy web — /resources/autopress (ES + EN)

> Contenido listo para maquetar. Cada sección trae **ES** y **EN**. La página es
> bilingüe (sigue el sistema i18n del sitio). URL canónica exacta:
> `https://evaristobabe.com/resources/autopress`
> Enlaces fijos: repo `https://github.com/varis79/autopress` · descarga
> `https://github.com/varis79/autopress/releases/latest` · changelog
> `https://github.com/varis79/autopress/blob/main/CHANGELOG.md`

---

## SEO / meta

**ES**
- Title: `Autopress — monta tu propio medio de noticias con IA`
- Description: `Kit gratuito y abierto para montar, con ayuda de una IA, tu propio medio de noticias curadas que se publica solo, con revisión humana. El coste en API es de céntimos.`

**EN**
- Title: `Autopress — build your own AI-powered news outlet`
- Description: `A free, open kit to build, with the help of an AI, your own curated news outlet that publishes itself, human-reviewed by default. API cost is cents.`

OG: og:title = title, og:description = description, og:image = screenshot de una
edición o de la galería de estilos. og:type = website.

---

## 1. Hero

**ES**
- Eyebrow: `Recurso · Kit gratuito y abierto`
- H1: `Autopress`
- Subtítulo: `Monta tu propio medio de noticias con IA: ingiere fuentes, cura, redacta una edición y la publica como web — casi solo, y con tu revisión antes de nada.`
- CTA primario: `Descargar` → releases/latest
- CTA secundario: `Ver en GitHub` → repo
- Nota bajo botones: `Gratis y abierto · Necesitas un agente de IA y tu propia API key`

**EN**
- Eyebrow: `Resource · Free & open kit`
- H1: `Autopress`
- Subtitle: `Build your own AI-powered news outlet: it ingests sources, curates, writes an edition and publishes it as a website — almost on its own, and with your review first.`
- Primary CTA: `Download` → releases/latest
- Secondary CTA: `View on GitHub` → repo
- Note under buttons: `Free & open · You need an AI agent and your own API key`

---

## 2. Qué es / What it is

**ES**
Autopress es un kit que, con la ayuda de un agente de IA (Claude Code, Cursor,
Codex…), monta tu propio **medio de noticias curadas** sobre el tema que elijas.
Reúne feeds RSS, descarta duplicados, selecciona lo relevante, redacta una edición
periódica y la publica como sitio web estático. Tú fijas la línea; la IA hace el
trabajo repetitivo.

> **Con honestidad:** redacta a partir de los **resúmenes** de las fuentes, no del
> artículo completo — es un *digest* con criterio que **parafrasea y cita**, no un
> periódico que "verifica" cada dato. Y la autonomía es de la **generación**, no del
> criterio: por defecto **nada se indexa sin tu aprobación**. Tú sigues siendo el
> editor y el responsable.

**EN**
Autopress is a kit that, with the help of an AI agent (Claude Code, Cursor, Codex…),
builds your own **curated news outlet** on the topic you choose. It gathers RSS
feeds, drops duplicates, picks what matters, writes a recurring edition and
publishes it as a static website. You set the editorial line; the AI does the
repetitive work.

> **Honestly:** it writes from the **summaries** of the sources, not the full
> article — it's a thoughtful *digest* that **paraphrases and cites**, not a
> newspaper that "verifies" every figure. And the autonomy is in the **generation**,
> not the judgment: by default **nothing is indexed without your approval**. You
> remain the editor and the responsible party.

---

## 3. Empieza en 3 pasos / Get started in 3 steps

**ES**
**Paso 0 — un asistente de IA (una app, sin terminal).** Hace todo el trabajo
técnico por ti; tú solo hablas con él. Si no tienes ninguno: Cursor, la app de
Claude Code, o ChatGPT en modo Codex.
1. **Descarga el kit** desde *Releases* y descomprímelo. *(No uses el botón verde
   "Code → Download ZIP": eso es el código fuente, no el kit.)*
2. **Abre esa carpeta con tu asistente.**
3. **Pega este prompt** y sigue lo que te diga:

> Te doy el kit Autopress (estos ficheros). Ayúdame a montar mi propio medio de
> noticias con IA. Soy una persona SIN conocimientos técnicos. Lee AGENTS.md y
> síguelo: llévame paso a paso, ejecutando tú los comandos y esperando mis
> respuestas. No publiques nada sin mi visto bueno.

Te da la bienvenida, te hace unas preguntas y construye tu medio contigo.

**EN**
**Step 0 — an AI assistant (an app, no terminal).** It does all the technical work
for you; you just talk to it. If you don't have one: Cursor, the Claude Code app, or
ChatGPT in Codex mode.
1. **Download the kit** from *Releases* and unzip it. *(Don't use the green
   "Code → Download ZIP" button: that's the source code, not the kit.)*
2. **Open that folder with your assistant.**
3. **Paste this prompt** and follow along:

> Here's the Autopress kit (these files). Help me set up my own AI-powered news
> outlet. I'm NON-technical. Read AGENTS.md and follow it: walk me through it step by
> step, running the commands yourself and waiting for my answers. Don't publish
> anything without my go-ahead.

It welcomes you, asks a few questions and builds your outlet with you.

---

## 4. Cuánto cuesta / What it costs

**ES**
`Céntimos en API por edición` — una sola llamada al modelo por número. El stack
(hosting, repositorio) puede ser gratuito. **El coste real es tu atención:** revisar
cada edición, cuidar los derechos de las fuentes y corregir. Ni el kit ni tú
dependéis de nadie: usas tu propia cuenta y tu propia clave.

**EN**
`Cents in API per edition` — a single model call per issue. The stack (hosting,
repo) can be free. **The real cost is your attention:** reviewing each edition,
minding source rights, and correcting. Neither the kit nor you depend on anyone:
you use your own account and your own key.

---

## 5. Cómo funciona / How it works

**ES** (pasos de un diagrama simple)
`Fuentes RSS → Cura y deduplica → Selecciona → Redacta (IA, 1 llamada) → Tú revisas → Publica (web estática)`
Determinista en código (gratis) en casi todo; la IA solo redacta lo ya
seleccionado. Por eso puedes tener **muchísimas fuentes** sin encarecer nada.

**EN**
`RSS sources → Curate & dedupe → Select → Write (AI, 1 call) → You review → Publish (static site)`
Deterministic in code (free) for almost everything; the AI only writes what's
already been selected. That's why you can have **lots of sources** without raising
the cost.

---

## 6. Para quién / Who it's for

**ES**
- **Sí, si** quieres un medio propio, curado, con SEO, que controlas tú, sobre un
  tema con flujo vivo de noticias.
- **No, si** solo quieres una newsletter simple: usa Substack, Ghost o Beehiiv —
  más fácil y sin montar nada.

**EN**
- **Yes, if** you want your own curated outlet, with SEO, that you control, on a
  topic with a live flow of news.
- **No, if** you just want a simple newsletter: use Substack, Ghost or Beehiiv —
  easier and nothing to set up.

---

## 7. Se mantiene solo / It keeps itself current

**ES**
Versión actual: **v0.6.0 (beta)**. El kit **se auto-actualiza**: un comando trae el
último motor sin tocar tu configuración ni tu contenido. Historial en el CHANGELOG.

**EN**
Current version: **v0.6.0 (beta)**. The kit **self-updates**: one command pulls the
latest engine without touching your config or your content. History in the CHANGELOG.

---

## 8. Feedback / Feedback

**ES**
¿Lo pruebas? Cuéntame cómo te fue: abre un *issue* de feedback en GitHub. Todo lo que
encuentres ayuda a mejorarlo.

**EN**
Trying it out? Tell me how it went: open a feedback *issue* on GitHub. Anything you
find helps make it better.

(CTA → https://github.com/varis79/autopress/issues/new/choose)

---

## 9. Licencia y stack / License & stack

**ES**
Código bajo **MIT**, documentación bajo **CC BY 4.0**. Hecho sobre el **SDK de
Anthropic**; necesitas tu propia **API key** (dato factual; sin vínculo ni aval de
Anthropic).

**EN**
Code under **MIT**, docs under **CC BY 4.0**. Built on the **Anthropic SDK**; you
need your own **API key** (factual; no affiliation with or endorsement by Anthropic).

---

## 10. FAQ

**ES**
- **¿Necesito saber programar?** No. El asistente ejecuta todo; tú decides.
- **¿Es gratis?** El kit sí. La API la pagas tú (céntimos por edición). El hosting
  puede ser gratis.
- **¿Es legal?** Tú eres el editor responsable. El kit cita las fuentes y por
  defecto no indexa sin tu revisión; los derechos de las fuentes los vigilas tú.
- **¿En qué idiomas?** El kit y el medio que genera son bilingües (ES + EN).

**EN**
- **Do I need to code?** No. The assistant runs everything; you decide.
- **Is it free?** The kit is. You pay the API (cents per edition). Hosting can be free.
- **Is it legal?** You're the responsible editor. The kit cites sources and by
  default doesn't index without your review; you mind the source rights.
- **What languages?** The kit and the outlet it generates are bilingual (ES + EN).

---

## Brief para Codex (montaje en evaristobabe.com)

> La web NO se construye en este repo; la monta Codex en el repo de evaristobabe.com.
> Este brief + el copy de arriba son la fuente de la verdad del mensaje.

```
Trabaja en el repo de evaristobabe.com. Voy a crear una sección de RECURSOS y su
primera página, Autopress. El sitio ES BILINGÜE (ES+EN): usa su sistema i18n
existente y publica ambas versiones. Inspecciona primero el framework y el sistema
de diseño y REPLICA el estilo del sitio — no inventes uno nuevo.

1) /resources — índice DATA-DRIVEN de proyectos (una colección/array). Cada item:
   slug, título, tagline, estado, tags, repoUrl, fecha, destacado. Tarjetas
   bilingües. Diséñalo para que añadir un proyecto futuro sea 1 item + 1 página.
   Autopress es el primero.
2) /resources/autopress — plantilla de "página de proyecto" reutilizable.
   URL canónica EXACTA (no la cambies): https://evaristobabe.com/resources/autopress

CONTENIDO: usa TAL CUAL el copy ES+EN de este documento (hero, qué es + aviso
honesto, empieza en 3 pasos con el prompt en caja copiable, coste, cómo funciona,
para quién, versión/auto-update, feedback, licencia, FAQ, metadatos SEO/OG). No
reescribas el mensaje; solo maqueta.

ENLACES: repo https://github.com/varis79/autopress · descarga
https://github.com/varis79/autopress/releases/latest · changelog
https://github.com/varis79/autopress/blob/main/CHANGELOG.md · feedback
https://github.com/varis79/autopress/issues/new/choose

TÉCNICO
- Si es viable en build, consulta https://api.github.com/repos/varis79/autopress/releases/latest
  para mostrar la versión actual y enlazar el ZIP más reciente; si no, /releases/latest.
- SEO por idioma: title, meta description, canonical, hreflang ES/EN, y Open Graph.
  Imagen OG: screenshot de una edición o de la galería de estilos del kit.
- NADA de formularios que recojan datos ni newsletter en esta página: los CTAs van a
  GitHub. Tono honesto, "para tontos", sin hype.
- No hagas deploy ni publiques: déjalo en una rama/preview para revisar.
```
