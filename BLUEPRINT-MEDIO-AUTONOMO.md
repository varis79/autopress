# Blueprint — Cómo construir un medio editorial autónomo

> ⛔ **DOCUMENTO HISTÓRICO — NO es la especificación ejecutable.** El diseño real y
> actualizado está en **`docs/ARCHITECTURE.md`** + `starter/`. Este blueprint es la visión
> original (larga, con partes superadas: usa YAML donde el starter usa JSON, es Vercel-first
> donde el default es Cloudflare, propone generación masiva SEO y modo patrocinado que están
> **fuera del alcance base**, y describe QA "informativo" cuando el código tiene bloqueantes).
> **NO lo sigas para implementar.** Úsalo solo como contexto/ideas. Ante cualquier conflicto,
> mandan `docs/ARCHITECTURE.md`, `starter/` y las decisiones D1-D4. Alcance (D4): solo
> **curación de noticias** (temas con flujo vivo de fuentes).

> **Qué es este documento.** Es una plantilla completa y reutilizable para construir,
> desde cero, un **medio editorial semanal que se publica solo**: un pipeline que
> ingiere noticias reales, las cura, redacta una revista con una IA, la publica como
> sitio web estático y envía una newsletter — sin intervención humana en el flujo
> principal.
>
> Está escrito para que **se lo entregues a una IA** (por ejemplo Claude Code, Cursor,
> o cualquier asistente con acceso a ficheros y terminal). La IA debe **leerlo entero,
> hacerte un breve cuestionario para conocer tu temática, y luego construir el
> proyecto** siguiendo el plan de la sección 18.
>
> El patrón es **agnóstico de temática**: sirve igual para flotas, agricultura,
> ciberseguridad, restauración, energía, real estate, moda o lo que quieras. Solo
> cambian los parámetros del cuestionario (sección 2).

> ⚠️ **Este documento no contiene ninguna clave, secreto, dominio ni marca real.**
> Todo lo sensible aparece como `<PLACEHOLDER>` o como *nombre* de variable de entorno
> (nunca su valor). Antes de compartirlo, no hay nada que borrar.

---

## Índice

0. [Instrucciones para la IA (léelo primero)](#0-instrucciones-para-la-ia-léelo-primero)
1. [Qué vas a construir (el patrón)](#1-qué-vas-a-construir-el-patrón)
2. [Cuestionario de arranque (parámetros)](#2-cuestionario-de-arranque-parámetros)
3. [Arquitectura general](#3-arquitectura-general)
4. [Estructura del repositorio](#4-estructura-del-repositorio)
5. [Subsistemas](#5-subsistemas)
6. [El pipeline paso a paso](#6-el-pipeline-paso-a-paso)
7. [Configuración (`pipeline-config.yml`)](#7-configuración-pipeline-configyml)
8. [El prompt maestro editorial (plantilla)](#8-el-prompt-maestro-editorial-plantilla)
9. [Modelo de datos (Git como base de datos)](#9-modelo-de-datos-git-como-base-de-datos)
10. [Lógica de negocio](#10-lógica-de-negocio)
11. [Sistema SEO](#11-sistema-seo)
12. [Newsletter](#12-newsletter)
13. [Tecnologías y dependencias](#13-tecnologías-y-dependencias)
14. [Despliegue (Vercel + GitHub Actions)](#14-despliegue-vercel--github-actions)
15. [Variables de entorno y secretos](#15-variables-de-entorno-y-secretos)
16. [Seguridad y anti-spam](#16-seguridad-y-anti-spam)
17. [Reglas editoriales de oro](#17-reglas-editoriales-de-oro)
18. [Plan de construcción para la IA](#18-plan-de-construcción-para-la-ia)
19. [Checklist de lanzamiento](#19-checklist-de-lanzamiento)
20. [Glosario](#20-glosario)
- [Apéndice A · Decisiones de diseño (y por qué)](#apéndice-a--decisiones-de-diseño-y-por-qué)
- [Apéndice B · Gotchas y lecciones aprendidas](#apéndice-b--gotchas-y-lecciones-aprendidas)

---

## 0. Instrucciones para la IA (léelo primero)

Si eres una IA y alguien te ha entregado este documento, tu trabajo es **construir un
medio editorial autónomo** siguiendo este blueprint. Procede así:

1. **Lee el documento completo** antes de escribir una sola línea de código.
2. **Haz el cuestionario de la sección 2** al operador. No asumas la temática ni el
   idioma: pregúntalos. Espera sus respuestas.
3. Con las respuestas, **rellena todos los `<PLACEHOLDER>`** de este blueprint y
   genera el proyecto siguiendo el **plan de construcción de la sección 18**.
4. Aplica el principio rector: **lo determinista, en código (gratis); la IA, solo
   para lo que exige juicio o redacción** (sección 3.3). Cada llamada al modelo cuesta
   dinero: minimízalas.
5. **Nunca inventes cifras** ni atribuyas datos falsos a empresas (sección 17).
6. **No incrustes secretos en el código.** Usa variables de entorno (sección 15).
7. Entrega el proyecto **funcionando end-to-end** y con un README propio.

> Este blueprint describe *qué* construir y *por qué*. Tú decides los detalles de
> implementación concretos, pero respeta las reglas de negocio y las decisiones de
> diseño, que son las que hacen que el sistema sea barato, robusto y creíble.

---

## 1. Qué vas a construir (el patrón)

Un **medio editorial de marca (owned media)**: una publicación periódica, pública y
de aspecto premium, sobre un tema concreto, editada por una empresa (el *patrocinador*)
que la usa como **activo de captación** — tráfico orgánico B2B/B2C, SEO, citación por
LLMs y leads — **sin que parezca un anuncio**.

**Las tres ideas que lo hacen viable:**

1. **Se publica solo.** Un pipeline en CI (GitHub Actions) corre en un cron semanal:
   ingiere noticias reales, las clasifica y selecciona, redacta la revista con **una
   sola llamada a un LLM**, valida la calidad, publica el HTML y envía la newsletter.
2. **Cero base de datos.** Todo el estado vive versionado en Git (JSONL, Markdown,
   JSON, HTML). Los suscriptores viven en un servicio de email (Resend). No hay backend
   con estado propio salvo dos funciones serverless para alta/baja.
3. **Determinista donde se pueda, IA solo donde aporta juicio.** Ingesta,
   clasificación, deduplicación y selección son código puro (gratis, auditable,
   reproducible). El LLM **solo redacta**. Coste típico por edición: **muy bajo**
   (una llamada al modelo).

**Resultado:** un sitio estático de decenas o cientos de páginas (la revista semanal +
una red de páginas evergreen de SEO), una newsletter, y un motor que lo mantiene vivo
semana a semana casi gratis.

**Público objetivo del medio:** lo defines tú en el cuestionario. El patrón funciona
mejor para **nichos B2B con poca cobertura de calidad en el idioma objetivo**, donde
un resumen curado y con autoridad genera confianza.

---

## 2. Cuestionario de arranque (parámetros)

**IA: haz estas preguntas al operador antes de construir.** Cada respuesta rellena un
`<PLACEHOLDER>` que se propaga por todo el sistema.

| # | Pregunta | Placeholder | Ejemplo (no lo uses; es solo ilustrativo) |
|---|---|---|---|
| Q1 | ¿Cuál es la **temática** del medio? | `<TEMA>` | "ciberseguridad para pymes" |
| Q2 | ¿Cómo se **llama** el medio? ¿Y el eslogan? | `<NOMBRE_MEDIO>` / `<ESLOGAN>` | inventa uno del nicho |
| Q3 | ¿Qué **empresa lo patrocina** y qué producto vende? | `<MARCA>` / `<PRODUCTO>` | una empresa SaaS de seguridad |
| Q4 | ¿En qué **idioma** se publica? ¿Habrá más idiomas después? | `<IDIOMA>` | español (EN más adelante) |
| Q5 | ¿Qué **mercados/geografías** priorizas y en qué orden? | `<MERCADOS>` | primario: MX, ES · secundario: USA |
| Q6 | ¿Con qué **cadencia**? ¿Qué día y hora? | `<CADENCIA>` | lunes 07:00 (Europa/Madrid) |
| Q7 | ¿Qué **subtemas / secciones** cubre? (5-12) | `<TOPICS>` | amenazas, cumplimiento, IA, casos… |
| Q8 | ¿Qué **competidores directos** NO quieres promocionar? | `<BLACKLIST>` | marcas rivales del patrocinador |
| Q9 | ¿Qué **fuentes RSS / medios** son relevantes? (o que la IA las proponga) | `<FUENTES>` | medios del sector + Google News |
| Q10 | ¿Cuál será el **dominio** de producción? | `<DOMINIO>` | `tudominio.com` |
| Q11 | ¿Qué **tono editorial**? (sobrio, técnico, cercano…) | `<TONO>` | autoridad sobria, sin hype |
| Q12 | ¿Email de **respuesta** y remitente de la newsletter? | `<EMAIL_REPLY>` / `<EMAIL_FROM>` | `hola@tudominio.com` |

Reglas de propagación:
- **`<TEMA>`, `<TOPICS>`, `<MERCADOS>`** → taxonomía, clasificación, cuotas y el prompt
  maestro.
- **`<MARCA>`, `<PRODUCTO>`** → firma, CTA suave y la sección "Desde `<MARCA>`" (opcional).
- **`<BLACKLIST>`** → filtro de selección e interlinking (no regalar SEO al rival).
- **`<DOMINIO>`, `<EMAIL_*>`** → deploy, canonical, sitemap, RSS, newsletter.

---

## 3. Arquitectura general

### 3.1 Modelo mental en 30 segundos

Un **generador de sitio estático dirigido por un pipeline de Python**, con **una única
llamada a un LLM por edición**, y **sin base de datos**. Todo el conocimiento y todos
los artefactos viven versionados en Git. **GitHub Actions es el "runtime"** (los crons
son el reloj). **Vercel** sirve el HTML estático y dos funciones Edge. **Resend** guarda
los suscriptores y envía el email.

### 3.2 Componentes principales

| Componente | Tecnología sugerida | Responsabilidad |
|---|---|---|
| Pipeline editorial | Python 3.11 (`scripts/`) | Ingesta, clasificación, dedupe, selección, composición (LLM), QA, publicación |
| Motor de composición | LLM (Claude u otro modelo capaz) | Redactar la revista a partir de la selección; devuelve **JSON estructurado** |
| Sistema de plantillas | `string.Template` (stdlib) | Renderiza el HTML (lo hace el **código**, no el LLM) |
| Corpus SEO | HTML estático + matriz YAML/CSV | Hubs y páginas pilar; interlinking; Schema.org |
| Newsletter | Resend + LLM + funciones Edge | Suscripción anti-spam, teaser, envío broadcast |
| Orquestación CI/CD | GitHub Actions (cron) | Edición semanal, freshness, canary, generación de páginas |
| Hosting / CDN | Vercel (static + Edge) | Servir el sitio y 2 APIs; deploy en cada push a `main` |
| Configuración | `pipeline-config.yml` | Único sitio con los parámetros del pipeline |
| Constitución editorial | `prompts/master-prompt.md` | System prompt que define voz, estructura y reglas |
| Almacén de estado | Git + Resend | Sin DB; todo versionado salvo suscriptores |

### 3.3 Principios arquitectónicos (no negociables)

1. **Determinista donde se pueda; LLM solo donde aporta juicio.** Ingesta,
   clasificación, dedupe y selección son código puro. El LLM solo redacta.
2. **Git como base de datos.** Cada ejecución deja rastro versionado y auditable.
3. **QA informativo, nunca bloqueante.** El sistema **siempre publica**, aun con
   avisos, y los registra. Nunca perder una semana por un falso positivo.
4. **Una sola hoja de estilo.** Identidad reconocible; la única variación semanal es
   un puñado de variables CSS de color.
5. **Configuración externa al código.** Cambiar fuentes, pesos o cuotas se hace en
   YAML, no tocando scripts.
6. **Idempotencia.** Los scripts de inyección (schema, links, facts, CTAs) se pueden
   re-ejecutar sin duplicar contenido.

### 3.4 Diagrama lógico

```
                 ┌──────────────── GitHub Actions (cron semanal) ───────────────┐
 Fuentes RSS ───▶│  weekly-edition:                                             │
 (medios + News) │    ingest → classify → dedupe → select → compose → qa →      │
                 │    publish → notify                                          │
                 │        │                 │                    │              │
                 │        │                 ▼                    ▼              │
                 │        │            LLM (1 llamada)     index/archive/         │
                 │        │            por edición         sitemap/rss/memoria    │
                 │        ▼                                                       │
                 │  content/raw/*.jsonl → magazines/YYYY-MM-DD-*.html            │
                 │  → git branch + PR + auto-merge (si ok) → deploy hook         │
                 │  → smoke test → send_newsletter (Resend)                     │
                 └───────────────────────────────────────────────────────────────┘
                                        │ push a main
                                        ▼
                 ┌──────────────────── Vercel ────────────────────┐
 Lector / bot ──▶│  Sitio estático (clean URLs)                   │
                 │  /api/subscribe   (Edge) ──▶ Resend            │
                 │  /api/unsubscribe (Edge) ──▶ Resend            │
                 └─────────────────────────────────────────────────┘

  weekly-freshness   (otro día): rota "Sabías qué" + fecha de modificación + sitemap
  weekly-canary      (otro día): verifica que el sitio responde 200; abre issue si no
  generate-pages     (manual):   genera páginas pilar de SEO con el LLM
```

---

## 4. Estructura del repositorio

Todos los ficheros del sitio van **en la raíz del repo**. Estructura sugerida:

```
/
├── index.html                  # Home = copia de la edición más reciente
├── archive.html                # Índice de todas las ediciones
├── sitemap.xml  rss.xml  robots.txt  404.html
├── vercel.json                 # clean URLs, headers de cache, redirects
├── requirements.txt
├── pipeline-config.yml         # TODOS los parámetros del pipeline
├── favicon.ico  og-default.png
├── assets/
│   ├── radar.css               # única hoja de estilo
│   └── sabias-que.json         # pool de "facts" para cajas dinámicas
├── api/
│   ├── subscribe.js            # función Edge: alta (con anti-spam)
│   └── unsubscribe.js          # función Edge: baja
├── magazines/                  # cada edición + su resumen .txt
│   ├── YYYY-MM-DD-<slug>.html
│   └── YYYY-MM-DD-<slug>-summary.txt
├── prompts/
│   ├── master-prompt.md        # la "constitución editorial"
│   ├── pillar-page-prompt.md
│   └── qa-checklist.md
├── content/
│   ├── taxonomy/               # topics, players, markets, fleet/segment types…
│   ├── raw/{week}-raw.jsonl            # traza de ingesta
│   ├── decisions/{week}-*.json         # selección, compose-info, newsletter
│   ├── qa/{week}-report.md             # informe de QA
│   ├── editorial-memory.md             # log append-only de qué se cubrió
│   ├── sabias-que-pool.md / .json      # pool de datos curados
│   └── pillar-matrix/                  # la "matriz viva" de páginas SEO
│       ├── matrix.csv  markets.yml  topics.yml  intents.yml …
│       └── pages/<slug>.md             # tracking por página
├── scripts/
│   ├── pipeline.py             # orquestador de las 8 etapas
│   ├── ingest.py classify.py dedupe.py select.py compose.py qa.py publish.py notify.py
│   ├── lib/                    # config, paths, templating, seo, forbidden…
│   ├── generate_pillar_page.py  discover_entities.py  detect_emerging_topics.py
│   ├── linkify_master.py  inject_*.py  rotate_facts.py  refresh_freshness.py
│   └── send_newsletter.py  generate_newsletter_copy.py  generate_email.py
├── <secciones SEO>/            # temas/  mercados/  players/  ciudades/  sectores/ …
├── about/  legal/              # quiénes somos, privacidad, términos
└── .github/workflows/          # weekly-edition, freshness, canary, generate-pages
```

Cada sección SEO es un directorio con `index.html` por página, servidos con URLs
limpias (`/temas/<slug>/`).

---

## 5. Subsistemas

Siete subsistemas. Para cada uno: objetivo, entradas, salidas y regla clave.

### 5.1 Pipeline editorial semanal
- **Objetivo:** producir una edición completa cada semana sin intervención humana.
- **Entradas:** fuentes RSS (config), taxonomía, memoria editorial, parámetros.
- **Salidas:** `magazines/YYYY-MM-DD-*.html` + `-summary.txt`; actualización de
  `index.html`, `archive.html`, `sitemap.xml`, `rss.xml`, `editorial-memory.md`;
  artefactos de traza en `content/raw|decisions|qa/`.
- **Interfaz:** `python -m scripts.pipeline [--date YYYY-MM-DD]`. Salida JSON a stdout
  que el workflow parsea para decidir etiqueta de PR y auto-merge.

### 5.2 Composición con LLM
- **Objetivo:** convertir la selección de historias en una revista con la voz correcta.
- **Entrada:** la selección (`{week}-selection.json`) + el master prompt.
- **Salida:** **JSON estructurado** (ver 9.4) → HTML vía plantillas + resumen + metadatos.
- **Regla clave:** el HTML lo renderiza el **código**, no el LLM. El LLM solo devuelve
  contenido. Esto garantiza consistencia estructural semana a semana.
- **Fallback sin API key:** genera un *stub* etiquetado que QA detecta; nunca crashea.

### 5.3 Corpus SEO (hubs + páginas pilar)
- **Objetivo:** captar tráfico long-tail y ser citado por LLMs con una red de páginas
  evergreen interconectadas.
- **Estructura:** hubs (índices por dimensión) + páginas pilar (`<topic> × <mercado> ×
  <intención>`). Fuente de verdad: la **matriz viva** (`content/pillar-matrix/`).
- **Regla anti-penalización:** las páginas de baja prioridad **arrancan en `noindex`**
  y entran al sitemap solo al superar un umbral de unicidad (contenido único ≥30%).

### 5.4 Interlinking automático
- **Objetivo:** tejer enlaces internos (por entidades) y externos (autoridad) sin
  trabajo manual, enlazando **solo páginas que existen en disco**.
- **Regla de negocio:** **no regalar SEO a los competidores** de `<BLACKLIST>`. Los
  términos genéricos del sector enlazan al pilar propio, nunca a la web del patrocinador.

### 5.5 Frescura + "Sabías qué"
- **Objetivo:** mantener las páginas "vivas" para Google de forma legítima (cambios de
  contenido reales, no solo la fecha).
- **Mecánica:** cada semana se rota **un** dato curado por página (caja "Sabías qué")
  y se actualiza la fecha de modificación de **una fracción** de páginas (nunca todas
  a la vez: los updates masivos sin cambio real penalizan).

### 5.6 Newsletter (suscripción + envío)
- **Objetivo:** captar emails y enviar un teaser semanal de la edición.
- **Almacén:** Resend (Audiences/Contacts). **No hay DB propia.** El estado de dedup
  de envío vive en `content/decisions/{week}-newsletter.json`.
- **Componentes:** funciones Edge de alta/baja + generación del teaser (LLM) + envío
  como broadcast de Resend + inyección de cajas de suscripción en todas las páginas.

### 5.7 Descubrimiento + matriz viva
- **Objetivo:** que el sitio crezca solo detectando qué cubre la redacción pero no
  tiene página, y proponiendo nuevas páginas/temas.
- **Mecánica:** un script escanea las ediciones recientes; si una entidad conocida se
  menciona varias veces sin página, crea un *stub* `noindex,follow`. Un paso con LLM
  agrupa titulares y detecta temas emergentes → propuesta → revisión humana → expansión
  de la matriz → generación de la página.

---

## 6. El pipeline paso a paso

| Etapa | Script | Qué hace | ¿Determinista? |
|---|---|---|---|
| 1. Ingest | `ingest.py` | Lee las fuentes RSS, ventana de ~8 días, máx N items/fuente, limpia `utm_*` | Sí |
| 2. Classify | `classify.py` | Etiqueta topic/market/segment/players por keyword (con *word-boundary* Unicode) | Sí |
| 3. Dedupe | `dedupe.py` | URL canónica + similitud difusa de títulos (`SequenceMatcher`, umbral ~0.82) | Sí |
| 4. Select | `select.py` | Filtra competidores + anti-repetición, puntúa, aplica cuotas, decide modo | Sí |
| 5. Compose | `compose.py` | **1 llamada al LLM** → JSON → render HTML vía plantillas | LLM |
| 6. QA | `qa.py` | ~9 checks + avisos; informe en `content/qa/`; **no bloquea** | Sí |
| 7. Publish | `publish.py` | Actualiza index/archive/sitemap/rss/memoria + hooks SEO | Sí |
| 8. Notify | `notify.py` | Postea a Slack si hay webhook; si no, salta | Sí |

**Flujo feliz (edición semanal):**
1. Cron dispara → checkout `main`, Python 3.11, `pip install`.
2. Calcula la fecha de edición, crea rama `edition-YYYY-MM-DD-<run_id>`.
3. Corre el pipeline → escribe la edición y sus artefactos.
4. El workflow parsea `status`, etiqueta el PR, y si `status ∈ {ok, ok-qa-warn}` hace
   **auto-merge** (squash).
5. Dispara el **deploy hook** de Vercel (redeploy explícito).
6. **Smoke test:** varios `curl` a la URL final; falla si nunca responde 200.
7. **Envía la newsletter** (si hay claves de Resend). No bloqueante.

**Modos según material disponible:**
- `normal` (~10-12 historias) · `short` (~7-9, umbrales de QA más laxos) · `pause`
  (< umbral mínimo → no toca el sitio, solo deja traza).

**Casos de error:** ingesta vacía → `fail`, no publica. Fuente RSS caída → se registra
y sigue con el resto. Timeout del LLM → reintento con un modelo de *fallback*. Sin API
key → *stub*. Deploy caído (detectado por el canary) → abre un issue.

---

## 7. Configuración (`pipeline-config.yml`)

Un único fichero YAML con **todos** los parámetros. Esqueleto genérico:

```yaml
site:
  name: "<NOMBRE_MEDIO>"
  tagline: "<ESLOGAN>"
  domain: "<DOMINIO>"
  language: "<IDIOMA>"
  publisher: "<MARCA>"

cadence:
  day: "monday"          # <CADENCIA>
  time_local: "07:00"
  timezone: "Europe/Madrid"

sources:                 # <FUENTES> — mezcla medios con RSS + queries de Google News
  - name: "Medio 1"
    url: "https://ejemplo.com/feed"
    geo_hint: "<mercado>"
    topic_hint: "<topic>"
  # … añade 10-25 fuentes …

ingest:
  lookback_days: 8
  max_items_per_source: 20
  timeout_seconds: 20
blocklist_domains: []   # dominios de baja calidad a excluir

classification:
  topics: [<TOPICS>]                 # lista de subtemas con sus keywords
  markets: [<MERCADOS>]              # con tier: primary/secondary/tertiary
  segment_types: []                  # segmentos de audiencia del nicho

dedupe:
  title_similarity_threshold: 0.82

selection:
  competitor_blacklist: [<BLACKLIST>]     # marcas que excluyen un item
  recent_weeks_check: 8                   # anti-repetición contra N ediciones
  repetition_threshold: 0.85
  scoring:                                # todos los pesos configurables
    topic_match: 1.0
    topic_priority_boost: 0.5
    market_primary: 1.2
    market_secondary: 0.4
    market_tertiary: 0.3
    market_other: 0.15
    players_base: 0.5
    recency_max_bonus: 2.0
    recency_decay_per_day: 0.2
  topic_quotas: {}                        # tope de historias por topic
  geo_quotas:                             # reparto geográfico objetivo
    primary: [7, 10]
    secondary: [1, 2]
    other: [0, 2]

compose:
  model_primary: "<MODELO_LLM_CAPAZ>"     # el modelo más capaz disponible
  model_fallback: "<MODELO_LLM_ECONOMICO>"
  max_tokens: 8000
  temperature: 0.4
  accent_palettes:                        # 6 paletas; se elige 1/semana determinista
    - {name: "…", primary: "#…", …}

qa:
  internal_link_check: true
  external_link_check: false              # no HEAD externo (ahorra runtime)
  max_em_dash_in_prose: 1
  min_words_edition_normal: 3000
  min_words_edition_short: 2200

modes:
  min_stories_normal: 10
  min_stories_short: 7
  min_stories_pause: 4
```

> **Regla:** cambiar comportamiento del medio = editar este YAML, **no** los scripts.

---

## 8. El prompt maestro editorial (plantilla)

`prompts/master-prompt.md` es la **constitución editorial**: el system prompt que el
LLM recibe en cada composición. Plantilla genérica a rellenar:

```markdown
# System prompt — <NOMBRE_MEDIO>

Eres el/la editor(a) jefe de "<NOMBRE_MEDIO>", una publicación semanal en <IDIOMA>
sobre <TEMA>, editada por <MARCA>. Tu trabajo: convertir la selección de noticias
reales de esta semana en una revista redactada con autoridad, sobria y útil.

## Voz y tono
- <TONO>. Nada de hype, nada de clichés de LinkedIn.
- Prioridad al lector externo. <MARCA> aparece con elegancia, nunca como protagonista.

## Estructura de la edición (devuélvela como JSON, ver esquema abajo)
- Portada: titular (máx 12 palabras, sustantivo+verbo, con dato), bajada, tags.
- Resumen ejecutivo.
- Bloque "Lo que importó esta semana" (tarjetas).
- Historias (10 en modo normal, 7 en short): cada una con headline, resumen,
  "por qué al operador", "por qué al negocio", país/mercado, tag.
- Bloque "Movimientos" (M&A, rondas, contrataciones del sector).
- Opinión / editorial breve.
- Sección "Desde <MARCA>": SOLO si hay material real; si no, se omite.
- CTA de cierre suave hacia <MARCA> (sin "¡compra ya!").

## Prioridad geográfica
- La geografía es la del HECHO, no la del lector. <MERCADOS> primarios siempre tienen
  su sección.

## Prohibiciones absolutas (capa pública)
- Nada de lenguaje interno/comercial: "competidor", "argumento comercial",
  "oportunidad", "<MARCA> debe/necesita".
- Rasgos de IA prohibidos: guiones largos en prosa (máx 1), "no es X, es Y",
  grandilocuencia, tríadas huecas.
- NO inventes cifras. Si no tienes el dato con fuente, no lo pongas.

## Precondiciones bloqueantes
- Si no hay noticias reales suficientes, o no puedes leer este prompt, NO generes:
  deja constancia y termina en modo "pause".

## Formato de salida
Devuelve EXCLUSIVAMENTE un JSON con las claves del esquema (sección 9.4 del blueprint).
El HTML lo renderiza el código, tú solo devuelves contenido.
```

---

## 9. Modelo de datos (Git como base de datos)

No hay base de datos relacional. El "modelo" son ficheros versionados con ciclo de vida
por semana ISO (`YYYY-Www`) o por fecha de edición (`YYYY-MM-DD`).

### 9.1 Entidades

| Entidad | Representación | Clave | Ciclo de vida |
|---|---|---|---|
| Item (noticia cruda) | línea JSONL en `content/raw/{week}-raw.jsonl` | hash / URL canónica | ingesta → clasificado → deduplicado → seleccionado o descartado |
| Edición | `magazines/YYYY-MM-DD-*.html` + `-summary.txt` | fecha + nº correlativo | compuesta → QA → publicada → archivada |
| Selección | `content/decisions/{week}-selection.json` | week | inmutable tras publicar |
| Página pilar | `<dir>/<slug>/index.html` + `pages/<slug>.md` | slug | planeada → generada (noindex) → liberada (index) → refrescada |
| Fact "Sabías qué" | bloque en `sabias-que-pool.md` → `.json` | id | curado → compilado → rotado |
| Suscriptor | contacto en Resend Audience | email | alta → baja |
| Memoria editorial | bloque append-only en `editorial-memory.md` | nº edición | se añade al publicar; nunca se edita retro |

### 9.2 Estados de un item

```
crudo → clasificado → deduplicado → candidato
                                       ├─ descartado_competidor  (blacklist)
                                       ├─ descartado_repeticion  (memoria editorial)
                                       ├─ descartado_cuota       (topic/geo)
                                       └─ elegido → historia en la edición
```

### 9.3 La matriz de páginas (`matrix.csv`)
Columnas sugeridas: `dimension, slug, label, market, topic_code, intent, tier,
review_days, schema_type, url_path`.
- `dimension` ∈ {topic, use-case, vertical, subgeo}.
- `tier` ∈ {1,2,3}; `review_days`: T1=30, T2=60, T3=90.
- `schema_type` ∈ {Article, HowTo, FAQPage} según la intención de búsqueda.

### 9.4 Esquema del JSON que devuelve el LLM (compose)
Claves top-level esperadas por `compose.py`:
`cover_headline`, `cover_deck`, `overline`, `cover_tags[]`, `meta_description`,
`executive_summary`, `editors_body`, `cta_headline`, `opinion_quote`, `opinion_body`,
`wm_cards[]` (`tone`/`headline`/`body`), `slack_summary`, `movimientos[]`
(`type`/`market`/`headline`/`detail`), `stories[]` (`ref_id`, `tag_class`, `tag_label`,
`market`, `date_label`, `headline`, `summary`, `why_operator`, `why_business`, `topic`,
`segment_type`, `players[]`, `micro_tags[]`).

> **Regla de credibilidad (crítica):** cada historia debe llevar además **`source_name`
> y `source_url`** que enlacen a la noticia original. Un medio que reescribe noticias
> ajenas y no enlaza a la fuente no es un medio: es un scraper con buena tipografía.

---

## 10. Lógica de negocio

### 10.1 Clasificación (determinista)
Keyword match con **word-boundary Unicode** (evita falsos positivos dentro de otras
palabras). Por item: topic, market, segment, players. *Market scoring:* match en título
×2, en resumen ×1; gana el más puntuado.

### 10.2 Deduplicación
URL canónica (sin `utm_*`) + similitud difusa de títulos (`SequenceMatcher`, umbral
~0.82) + limpieza de sufijos de fuente.

### 10.3 Selección editorial (reglas y prioridades)
1. **Filtro de competidores** (antes del scoring): cualquier item que mencione un
   término de `<BLACKLIST>` se excluye. No se da visibilidad gratis al rival.
2. **Anti-repetición:** compara contra las últimas ~8 ediciones (umbral 0.85).
3. **Scoring por item** (pesos configurables): topic match + boost si es prioritario;
   peso de mercado (primario ≫ secundario); players; recencia (bonus que decae por día).
4. **Cuotas por topic y geográficas:** objetivo típico, dominar en los mercados
   primarios y dejar 1-3 huecos para secundarios.
5. **Decisión de modo:** normal / short / pause según cantidad de material.

### 10.4 Composición (reglas duras)
Impuestas por el master prompt y verificadas por QA + una lista de expresiones
prohibidas (`lib/forbidden.py`): nada de lenguaje interno/comercial en la capa pública;
rasgos de IA prohibidos; titular de portada con dato; la marca solo con elegancia; la
geografía es la del hecho.

### 10.5 QA (informativo, no bloquea)

Genera `content/qa/{week}-report.md` y **publica igual** (`status=ok-qa-warn`). Nunca se
pierde una semana por un falso positivo. Checks:

| Check | Qué mira |
|---|---|
| C1 framing | Expresiones internas/comerciales prohibidas en la capa pública |
| C2 thin | Edición corta o historias por debajo del mínimo de palabras |
| C3 voice | Guiones largos en prosa (>1), estructuras "no es X, es Y" |
| C4 meta | `title`, `description`, `canonical`, `og:url`, `article:published_time` |
| C5 structure | `H1` único; portada / nota del editor / CTA / cierre presentes |
| C6 links | Enlaces internos rotos |
| C7 repetition | Titular de portada similar a ediciones recientes |
| C8 claims | Afirmaciones absolutas ("líder", "el mejor", "el más barato") |
| C9 stub | Marcador `[stub:` presente (compuso sin API key) |
| A1 geo mix | Ratio de mercados primarios bajo (**aviso**) |
| A2 topics | Pocos topics distintos (**aviso**) |

> **Decisión histórica:** el QA empezó siendo **bloqueante** y se cambió a **informativo**.
> Si quieres que algo bloquee de verdad, hazlo con intención explícita (como el hook de
> "no inventar cifras" en las pilares, que sí falla el build — ver 11.6).

---

## 11. Sistema SEO

**Objetivo:** captar tráfico long-tail en `<IDIOMA>` y ser citado como fuente por LLMs,
con una red de páginas evergreen interconectadas. Es lo que convierte una "revista
semanal" en un **activo de tráfico compuesto**.

### 11.1 Arquitectura del corpus

- **Hubs:** páginas índice por dimensión (`/temas/`, `/mercados/`, `/players/`,
  `/sectores/`, `/casos-uso/`, `/ciudades/`, `/corredores/`, `/evergreen/`) que **listan
  solo páginas que existen en disco**.
- **Páginas pilar:** `<topic> × <mercado> × <intención>`, evergreen (1.300–2.000
  palabras), generadas con el LLM (`generate_pillar_page.py`) a partir de la matriz.
  Variantes por intención con sufijo de slug: `-comparativa`, `-guia`, `-regulacion`.
- **Matriz viva** (`content/pillar-matrix/`): CSV + YAML que define las páginas planeadas
  y su ciclo de vida (dimensión, tier, cadencia de revisión, schema, noindex→index).
- **Stubs:** páginas mínimas `noindex,follow` (200–400 palabras) que acumulan *equity* de
  enlace hasta que superan el umbral para liberarse a `index` (`release_pillars.py`).

### 11.2 Checklist de `<head>` obligatorio por página

Toda página (salvo la 404 y la styleguide) debe llevar:

```html
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large"/>
<title>…</title>                     <!-- único, <70 chars, dato/palabra clave primero -->
<meta name="description" content="…"/> <!-- único, <155 chars, accionable -->
<meta name="author" content="<MARCA>"/>
<!-- Open Graph: og:title, og:description, og:type(article|website), og:url,
     og:site_name, og:image (1200×630) -->
<!-- Twitter: twitter:card=summary_large_image, title, description, image -->
<meta property="article:published_time" content="YYYY-MM-DD"/>
<meta property="article:modified_time"  content="YYYY-MM-DD"/>  <!-- lo mueve la frescura -->
<link rel="canonical" href="https://<DOMINIO>/<ruta>/"/>
<!-- hreflang si hay par entre mercados: es-MX / es-ES / x-default -->
<link rel="alternate" type="application/rss+xml" href="/rss.xml"/>
<link rel="stylesheet" href="/assets/radar.css"/>
```

La **home** duplica la última edición pero con `canonical` a la raíz + `alternate` al
permalink de la edición (evita contenido duplicado).

### 11.3 Schema.org JSON-LD por tipo de página

| Tipo | Schemas |
|---|---|
| Home | `NewsMediaOrganization` + `WebSite` + `ItemList` (últimas ediciones) |
| Edición (magazine) | `NewsArticle` + `BreadcrumbList` |
| Hub de mercado | `CollectionPage` + `BreadcrumbList` + `Organization` + `WebSite` |
| Pilar (tema) | `Article` + `FAQPage` + `BreadcrumbList` |
| Caso de uso | `Article` + `FAQPage` + `HowTo` (si aplica) + `BreadcrumbList` |
| Sector / Ciudad / Corredor | `Article` + `BreadcrumbList` |
| Evergreen (checklist) | `Article` + `HowTo` + `BreadcrumbList` |
| Legal | `WebPage` + `BreadcrumbList` |

Usa un `@id` estable para la Organization (`https://<DOMINIO>/#organization`) y el WebSite
(`…/#website`) y referéncialos desde el resto. Se inyecta de forma idempotente
(`inject_schema_static.py`).

### 11.4 Interlinking automático (reglas exactas)

`linkify_master.py` mantiene un **diccionario único de entidades** (ciudades, marcas,
organismos, corredores, topics, términos editoriales genéricos). Reglas:
- **1 mención enlazada por entidad y página** (no saturar).
- **Saltar** si el término ya está dentro de un `<a>`, `<script>` o `<head>`.
- **Diversificar el anchor** por hash (no siempre el mismo texto).
- **Clase CSS por tipo** de entidad.
- **Nunca autoenlazar a la web del patrocinador** (`<MARCA>`) desde el cuerpo; los términos
  genéricos del sector enlazan al **pilar propio**.
- **No regalar SEO a los competidores** de `<BLACKLIST>` (no se autoenlazan sus webs).
- Objetivo por página: **≥3 enlaces internos entrantes / ≥5 salientes**.
- Enlaces externos solo a **fuentes de autoridad** (organismos oficiales, no rivales).

Complementos: `inject_story_links.py` (bloque "relacionadas" + tags clicables en
ediciones), `inject_edition_backlinks.py` (pilar ← ediciones que lo cubren),
`inject_sources.py` (bloque "Fuentes y referencias"). **Regla de oro:** nunca enlazar a
una URL que no existe en disco (`purge_dead_links.py` limpia los rotos).

### 11.5 Frescura (cron semanal) — mecánica exacta

Google premia el contenido que cambia **de verdad**. Sin frescura, un sitio estático se
vuelve *stale* en ~90 días. El sistema (cron un día distinto al de la edición):
- **`build_facts_json.py`**: compila el pool humano `sabias-que-pool.md` → `.json`
  (fuente de verdad = el MD; el JSON es artefacto). Filtra facts con confianza
  `pending/conflict`.
- **`rotate_facts.py`**: inyecta **una** caja "Sabías qué" por página, elegida por
  *scoring*: `+3` si la categoría del fact coincide con la de la página, `+2` si el mercado
  coincide, `+1` si es `global`, `+1` si la confianza es alta/cross-validada, `+0.1 ×
  evergreen_score`. Rotación determinista: `(isoweek + sha1(url)) % nº_candidatos` → el
  mismo fact toda la semana en una página, distinto entre páginas, cambia cada semana.
- **`refresh_freshness.py`**: actualiza `article:modified_time`, el `<time>` visible y el
  `dateModified` del JSON-LD de **~30 páginas/semana** (ciclo de ~6 semanas por página).
  **Nunca todas a la vez** (los updates masivos sin cambio real penalizan).
- **`rebuild_sitemap.py`**: reconstruye el sitemap con `lastmod = mtime real`; prioridad
  por sección; **auto-excluye las páginas `noindex`**.

### 11.6 Cuatro reglas SEO editoriales críticas (no negociables)

1. **PROHIBIDO inventar cifras de empresas privadas.** (Una auditoría encontró 30+ páginas
   con datos fabricados tipo "la empresa X recortó costes 18%".) **Permitido:** cifras de
   instituciones/empresas **públicas con enlace**, cifras de mercado **agregadas con fuente
   nombrada**, datos propios verificables, o **lenguaje cualitativo** ("operadores de
   referencia como X, Y, Z"). **Enforcement:** `qa_pillars.py` cuenta y **falla el build**
   si una página tiene **≥5 porcentajes de empresa privada** o **≥6 cifras absolutas sin
   fuente**; corre en un **hook pre-commit** sobre los HTML en *staging*.
2. **Consistencia interna:** si una cifra aparece en varias páginas (mismo actor, mismo
   mercado) **debe coincidir**. Tres cifras distintas para la misma empresa = síntoma de
   invención → usar cualitativo.
3. **Voz periodística, no marketing:** datos antes que adjetivos, sobriedad, cero hype;
   la marca aparece solo en un bloque discreto al final. Lista negra de expresiones en el
   prompt de pilar.
4. **Regenerar una pilar pisa los fixes manuales.** Tras `generate_pillar_page.py` hay que
   re-correr **en orden**: linkify → `seo_polish.py` → `rebuild_sitemap.py` → `qa_pillars.py`.

### 11.7 `robots.txt` pro-LLM y convención de slugs

- **`robots.txt`** permite explícitamente a los bots de IA (para ser citado como fuente).
- **Slugs** (con año para poder rotar): `<topic>-<sufijo-nicho>-<mercado>-<año>`,
  variantes `-comparativa/-guia/-regulacion`, casos `<caso>-<mercado>-<año>`, sectores
  `<sector>-<mercado>-<año>`, ciudades `<topic>-<ciudad>-<año>`. El cambio de año se hace con
  301 desde el slug viejo.

---

## 12. Newsletter

Almacén de suscriptores: **Resend** (Audiences/Contacts). **No hay DB propia.** El estado
de dedup de envío vive en `content/decisions/{week}-newsletter.json` (versionado en Git).

### 12.1 Alta — `POST /api/subscribe` (función Edge)

Runtime Edge. Body JSON `{ email, hp, ts }` (`hp`=honeypot, `ts`=token Turnstile). El
handler ejecuta las comprobaciones **en este orden exacto** (importa: las capas baratas
van primero):

1. `OPTIONS` → responde `204` con headers CORS (preflight). Método distinto de `POST` → `405`.
2. **Capa 1 — Origin/Referer gate** (antes de parsear el body): lee `origin` y `referer`;
   si **ninguno** empieza por un valor de la allowlist `ALLOWED_ORIGINS` (tu dominio, con
   y sin `www`) → **`403`**. Un navegador real siempre manda uno; el bot con `curl` no.
3. Parsea el body; normaliza `email = body.email.trim().toLowerCase()`.
4. **Capa 2 — Honeypot:** si `hp` viene relleno → responde **`200 {ok:true}` falso** (no
   alerta al bot) pero **NO registra** el contacto.
5. Valida el email con regex `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` → `400` si no cuadra.
6. **Capa 3 — Turnstile:** solo se exige **si `TURNSTILE_SECRET_KEY` está en el entorno**
   (rollout progresivo: sin el secret, el sitio funciona con las capas 1 y 2; en cuanto lo
   pones, el reto se activa solo). Si está y falta `ts` → `403`. Verifica server-side con
   `POST https://challenges.cloudflare.com/turnstile/v0/siteverify` (body
   `secret + response + remoteip`, donde `remoteip` = primer IP de `x-forwarded-for`); si
   `success !== true` → `403`.
7. Comprueba `RESEND_API_KEY` + `RESEND_AUDIENCE_ID`; si faltan → `500`.
8. `POST https://api.resend.com/audiences/{AUDIENCE_ID}/contacts` con `Bearer` y body
   `{ email, unsubscribed:false }`. **`200`/`201` → ok; `409` (ya existe) → éxito
   silencioso `{ok:true}`; otro → `500`.**

Todas las respuestas llevan los headers CORS con el origin permitido.

> **Recomendación para el kit público:** para operadores en la UE, considera **doble
> opt-in confirmado** por defecto (email de confirmación antes de dar de alta), y una baja
> con **token firmado** en la URL en vez del email en claro.

### 12.2 Baja — `GET /api/unsubscribe?email=` (función Edge)

Valida el email (misma regex) y hace **upsert** `{ email, unsubscribed:true }` al mismo
endpoint de contactos de Resend. Trata `200`/`201`/`409` como éxito. **No tiene capas
anti-spam** (es un GET idempotente de baja). Una página estática `unsubscribe.html` lee
`?email=` y llama a esta API.

### 12.3 Cajas de suscripción en cliente (`inject_newsletter_ctas.py`)

Inyecta **dos widgets** en todas las páginas (idempotente; las páginas nuevas lo heredan
del template):
- **`nl-bar`**: barra fina bajo el header, *dismissable* (recuerda el cierre con
  `sessionStorage`).
- **`nl-mid`**: tarjeta editorial a mitad de contenido; su posición depende del tipo de
  página (magazine → tras el 3.er artículo; pillar → tras el primer `<h2>`; hub → antes del
  bloque newsletter o del footer).

Detalles anti-bot **en el cliente** (deben coincidir con el servidor):
- Cada formulario lleva un **honeypot oculto**: `<input class="nl-hp" name="hp"
  tabindex="-1" autocomplete="off" aria-hidden="true">` (fuera de pantalla). Solo un bot lo
  rellena.
- **Turnstile invisible**: el contenedor se renderiza con `execution:'execute'`, así el reto
  **solo corre al enviar** (no consume cuota por *pageview*). La `site key` es pública (va en
  el HTML). Los contenedores van **fuera** del `<form>` (posicionados off-screen) para no
  romper el layout. Una función `cfExec(key)` devuelve una promesa con el token; el handler
  del submit hace `await cfExec(...)` y manda `{email, hp, ts}` a `/api/subscribe`.
- El script de Turnstile se carga **una vez por página** (`onloadTurnstileCallback`,
  `render:'explicit'`).

> `<TURNSTILE_SITE_KEY>` (pública) va en el HTML; `TURNSTILE_SECRET_KEY` es secreto y vive
> solo en el entorno del servidor. **No los intercambies.**

### 12.4 Envío del teaser semanal (`send_newsletter.py`)

Flujo (usa `requests`, no urllib, por el SSL de macOS):
1. Carga el *compose-info* de la edición (por fecha o la más reciente). Si la semana fue
   `pause` → no envía.
2. **Dedup:** si existe `content/decisions/{week}-newsletter.json` → sale (`already-sent`),
   salvo `--force`.
3. Genera el copy del teaser con el LLM (`generate_newsletter_copy.py`), con *fallback*
   local si no hay API key o falla.
4. Renderiza el email con `generate_email.py` (HTML con tablas compatibles con Outlook +
   versión texto).
5. **Crea el broadcast:** `POST {RESEND_API}/broadcasts` con `{ name, audience_id, from,
   subject, html, text, reply_to }`. El `subject` sale del `subject_line` del LLM o de un
   *fallback* `"Nº {N} · {titular} · <NOMBRE_MEDIO>"`.
6. **Lo envía:** `POST {RESEND_API}/broadcasts/{id}/send`.
7. Guarda el registro de envío en `{week}-newsletter.json` (para el dedup futuro).
8. Imprime un JSON de resultado a stdout (lo consume el workflow). Flags: `--date`,
   `--dry-run`, `--no-claude`, `--force`.

En el workflow, este paso corre tras `publish` y **no es bloqueante** (si falla el email,
la edición ya se publicó).

### 12.5 Entregabilidad

Verifica el dominio en Resend con **SPF/DKIM/DMARC** en el DNS antes de usar tu `from`
propio (mientras no esté verificado, Resend obliga a usar su dirección de pruebas). Usa un
`reply_to` real (`<EMAIL_REPLY>`).

> **Cambiar de proveedor** (Beehiiv, ConvertKit, Mailchimp…) solo obliga a reescribir
> `api/subscribe.js`; el HTML del formulario no cambia.
>
> **Placeholders:** `<EMAIL_FROM>`, `<EMAIL_REPLY>`, `<TURNSTILE_SITE_KEY>`, y las variables
> de entorno de la sección 15. Nunca incrustes la API key ni el Audience ID en el código.

---

## 13. Tecnologías y dependencias

| Capa | Tecnología | Por qué |
|---|---|---|
| Lenguaje pipeline | Python 3.11 | Ecosistema RSS/HTML maduro |
| Parsing RSS | `feedparser` | Estándar de facto |
| HTML | `beautifulsoup4` | Manipulación robusta e idempotente |
| Config | `pyyaml` | Config legible externa al código |
| HTTP | `requests` | SSL correcto en macOS (mejor que urllib) |
| LLM | SDK del proveedor (p. ej. `anthropic`) | Redacción de la edición |
| Plantillas | `string.Template` (stdlib) | Sin dependencias, render determinista |
| Hosting | Vercel (static + Edge) | Deploy en push, clean URLs, funciones Edge |
| Email | Resend | Broadcasts + Audiences; free tier generoso |
| Anti-bot | Cloudflare Turnstile | CAPTCHA invisible, sin fricción |
| CI/CD | GitHub Actions | El cron y el "runtime" del pipeline |
| Front-end | HTML + CSS puro + JS inline mínimo | Sin framework, sin build, máxima velocidad |
| Tipografía | Una serif + una sans (p. ej. Fraunces + Inter) | Identidad editorial premium |

`requirements.txt` (versiones a fijar por la IA al construir):
```
feedparser
beautifulsoup4
pyyaml
requests
anthropic        # o el SDK del proveedor de LLM elegido
```

**Notas de dependencias (lecciones reales):**
- **`requests` en lugar de `urllib`**: `urllib` da fallos de SSL en macOS; `requests` los
  maneja bien. Todo el HTTP saliente (Resend, verificaciones) usa `requests`.
- **Fijar el SDK del LLM** a una versión conocida: versiones recientes de `httpx`
  rompieron el SDK de Anthropic con un `TypeError('proxies')`; conviene un *pin* mínimo del
  SDK que lo evite.
- **`string.Template` (stdlib)** para el render: sin dependencias, determinista. **El HTML
  lo hace el código, no el LLM.**

### 13.1 Servicios externos (el "stack de arriba")

| Servicio | Rol | Free tier / coste | Por qué se eligió |
|---|---|---|---|
| **GitHub + Actions** | Repo, crons, "runtime" del pipeline, PRs, Issues | Gratis en repos públicos / minutos incluidos | Es el reloj y el motor; cero infra propia |
| **Vercel** | Hosting estático + 2 funciones Edge + Analytics | Free tier generoso | Deploy en push, clean URLs, Edge, Speed Insights |
| **Anthropic Claude** (u otro LLM) | Composición editorial, teaser, generación de pilares, detección de temas | Pago por uso (≈ una llamada/edición) | Calidad de redacción con 1 sola llamada |
| **Resend** | Almacén de suscriptores (Audiences) + envío (Broadcasts) | ~3.000 emails/mes gratis | Dev-friendly, listas + transaccional |
| **Cloudflare Turnstile** | CAPTCHA invisible (3.ª capa anti-spam) | Gratis | Sin fricción, sin cookies |
| **Fuentes RSS/Atom** | Materia prima editorial | Gratis | Medios del sector + **queries de Google News** por tema/mercado |
| **Google Search Console** | Indexación, envío de sitemap, rendimiento | Gratis | Medir y forzar indexación |

**Analítica (sin cookies):** Vercel **Web Analytics** + **Speed Insights** vía
`<script defer src="/_vercel/insights/script.js">` en cada página. Sin trackers de terceros.

**Notificaciones opcionales:** un webhook de **Slack** para avisar de cada publicación y de
las alertas del *canary* (si no hay webhook, el paso se salta sin romper nada).

### 13.2 Lo que deliberadamente NO se usa

Base de datos, CMS/headless, framework JS (React/Vue), bundler (Webpack/Vite), `npm build`,
publicidad, comentarios/comunidad, trackers de terceros, servidor propio. **Cada "no" es
una decisión** para minimizar coste, superficie de ataque y mantenimiento.

**Sobre el modelo LLM:** usa el modelo más capaz disponible para la **composición** (la
calidad de la redacción manda) y uno más económico como *fallback* y para tareas menores
(teaser, detección de temas). Comprueba los **IDs de modelo vigentes** del proveedor al
construir — no los quemes en el código, ponlos en el YAML.

---

## 14. Despliegue (Vercel + GitHub Actions)

GitHub Actions es el **motor** (corre el pipeline y hace commit); Vercel es el **hosting**
(sirve lo que hay en `main`). Cuatro workflows cubren todo el ciclo de vida.

### 14.1 Vercel — `vercel.json` (config exacta)

```jsonc
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "cleanUrls": true,        // /temas/x/ en vez de /temas/x/index.html
  "trailingSlash": false,
  "headers": [
    { "source": "/(.*)\\.html",  "headers": [{ "key": "Cache-Control", "value": "public, max-age=0, must-revalidate" }] },
    { "source": "/rss.xml",      "headers": [{ "key": "Content-Type", "value": "application/rss+xml; charset=utf-8" }, { "key": "Cache-Control", "value": "public, max-age=1800" }] },
    { "source": "/sitemap.xml",  "headers": [{ "key": "Content-Type", "value": "application/xml; charset=utf-8" }, { "key": "Cache-Control", "value": "public, max-age=1800" }] },
    { "source": "/robots.txt",   "headers": [{ "key": "Cache-Control", "value": "public, max-age=86400" }] }
  ],
  "redirects": [
    { "source": "/last",    "destination": "/",            "permanent": false },
    { "source": "/archivo", "destination": "/archive.html","permanent": true  },
    { "source": "/feed",    "destination": "/rss.xml",     "permanent": true  }
  ]
}
```
- HTML **no-cache** (para que las ediciones/rotaciones se vean al instante); RSS/sitemap
  30 min; robots 1 día.
- Las funciones `/api/*` se resuelven por convención (Edge runtime), sin *rewrites*.
- Conecta el repo a Vercel: deploy automático en cada push a `main` + preview por PR.

> ⚠️ **Aviso de uso comercial:** el plan gratuito (Hobby) de Vercel prohíbe el uso
> comercial — su definición incluye enlaces de afiliado como propósito principal, AdSense y
> pedir donaciones. Si vas a monetizar el medio, usa un host cuyo free tier permita uso
> comercial (p. ej. Cloudflare Pages) o pasa a Vercel Pro. Verifica la ToS vigente.

### 14.2 `robots.txt` pro-LLM

Además de los buscadores (Googlebot, Bingbot…), **nombra explícitamente los bots de IA**
con `Allow: /` para permitir que te citen como fuente (muchos, si no se les nombra, aplican
un default conservador): `GPTBot`, `ChatGPT-User`, `OAI-SearchBot` (OpenAI), `ClaudeBot`,
`anthropic-ai`, `Claude-Web` (Anthropic), `Google-Extended` (Gemini), `PerplexityBot`,
`Perplexity-User`, `Cohere-AI`, `Meta-ExternalAgent`, `Applebot-Extended`, `Bytespider`,
`Diffbot`… Cierra con `User-agent: *` / `Allow: /` y la línea `Sitemap:
https://<DOMINIO>/sitemap.xml`.

### 14.3 Secretos por workflow (dónde va cada uno)

| Secret | `weekly-edition` | `freshness` | `canary` | `generate-pages` |
|---|:--:|:--:|:--:|:--:|
| `ANTHROPIC_API_KEY` | ✅ compose + newsletter | — | — | ✅ |
| `VERCEL_DEPLOY_HOOK` | ✅ redeploy | ✅ redeploy | — | — |
| `RESEND_API_KEY` / `RESEND_AUDIENCE_ID` | ✅ envío | — | — | — |
| `SLACK_WEBHOOK_URL` | ⚪ opcional | — | — | — |
| `SLACK_WEBHOOK_ALERTS_URL` | — | — | ⚪ opcional | — |
| `GITHUB_TOKEN` (automático) | ✅ PR/merge | ✅ push | ✅ issue | ✅ PR |

### 14.4 `weekly-edition.yml` — anatomía (el workflow central)

```yaml
on:
  schedule: [{ cron: '7 5 * * 1' }]        # Lunes 05:07 UTC
  workflow_dispatch:                        # + ejecución manual con inputs
    inputs: { edition_date: '', allow_stub: 'false' }
permissions: { contents: write, pull-requests: write, issues: write }
concurrency: { group: weekly-edition, cancel-in-progress: false }
```
Pasos, en orden:
1. **Checkout** (`fetch-depth: 0`) + **setup-python 3.11** + **cache pip** + `pip install -r requirements.txt`.
2. **Git identity** del bot.
3. **Calcular fecha** de edición (próximo día de publicación) y **crear rama**
   `edition-<fecha>-<run_id>`.
4. **Correr el pipeline** con `set +e`, capturando el JSON de stdout a fichero. Extrae
   `status` con un **parser robusto** (intenta `json.loads`; si hay ruido antes, busca el
   último bloque `{…}` válido). Guarda `status` en el output del step.
5. **¿Hay cambios?** (`git status --porcelain`).
6. **Commit + push** (`--force` sobre la rama efímera).
7. **Crear PR** con label según `status`:

   | `status` | Label | Título |
   |---|---|---|
   | `ok` | `ready-to-review` | Edición · QA OK |
   | `ok-qa-warn` | `ready-to-review` | publicado con avisos QA |
   | `pause` | `editorial-pause` | Pausa editorial |
   | `*` (fail/error) | `pipeline-error` | Pipeline error |

8. **Auto-merge** (`gh pr merge --squash --delete-branch`) **solo si** `status ∈ {ok,
   ok-qa-warn}`.
9. **Deploy hook** de Vercel (`curl -X POST`) — si el secret no está, `::warning::` y sigue.
10. **Smoke test**: bucle `for i in 1..8`, `curl -sIL` a la URL de la edición, `sleep 20`
    entre intentos; `exit 0` al primer `200`, o `::error:: + exit 1` tras 160 s.
11. **Send newsletter** (`python -m scripts.send_newsletter --date …`) — **no bloqueante**
    (si falla, `::warning::`; la edición ya está publicada).

> **Regla de oro CI:** la publicación no depende del email ni del deploy hook. El orden es
> *publicar primero, notificar después*.

### 14.5 `weekly-freshness.yml` (cron miércoles 06:00 UTC)

Sin PR: hace **push directo a `main`**. Pasos: `build_facts_json` → `rotate_facts` →
`inject_dynamic_dyk` → `refresh_freshness` → `rebuild_sitemap` → commit **solo si hay
cambios** (`git diff --cached --quiet`) → push → deploy hook.

> **Gotcha:** para que Actions pueda commitear ficheros dentro de `.github/workflows/`, el
> token necesita scope `workflow`. Si usas el `GITHUB_TOKEN` por defecto suele bastar; con
> un PAT, dáselo.

### 14.6 `weekly-deploy-canary.yml` (cron martes 08:00 UTC, ~26 h después de la edición)

Verificación diferida e independiente: `curl` a la home y a la URL de la edición de esta
semana. Decide `ok` / `site-down` (home ≠ 200) / `edition-missing` (edición ≠ 200). Si no
es `ok`: **crea el label `deploy-down`** y **abre un issue** con diagnóstico y pasos de
recuperación (+ Slack opcional). Existe porque el webhook de Vercel falló una vez y una
edición mergeada no llegó a producción sin que nadie lo notara.

### 14.7 `generate-pillar-pages.yml` (manual, `workflow_dispatch`)

Genera páginas pilar con el LLM. `timeout-minutes: 90`. Inputs: `mode` (`single`/`tier`/
`filter`), `slug`, `tier`, `dimension`, `market`, `limit`, `indexed`. Construye los args
del CLI según el modo, corre `generate_pillar_page`, y abre un **PR con checklist de
revisión** (voz editorial, cifras con fuente, slot de marca discreto, links a páginas
reales, JSON-LD válido). **No auto-mergea** — SEO se revisa a mano.

### 14.8 Hook pre-commit (`install_hooks.sh`)

`bash scripts/install_hooks.sh` escribe un `pre-commit` que, sobre los HTML de pilar en
*staging* (`temas|mercados|casos-uso|sectores|ciudades|evergreen/**/index.html`), corre
`qa_pillars.py` y **aborta el commit** si detecta cifras inventadas (ver 11.6). Se puede
saltar con `git commit --no-verify` (no recomendado).

### 14.9 Desarrollo local
```bash
python3 -m http.server 4173                  # servir el sitio estático
python -m scripts.pipeline --date YYYY-MM-DD # pipeline (sin API key = stub)
python -m scripts.send_newsletter --dry-run  # generar email sin enviar
python -m scripts.generate_pillar_page --slug <slug> --dry-run
```

---

## 15. Variables de entorno y secretos

**Nunca en el repo ni en los logs.** Se configuran en GitHub Actions (secrets) y en
Vercel (env). Aquí van solo los **nombres**; los valores los pone el operador.

| Variable | ¿Obligatoria? | Uso | Dónde |
|---|---|---|---|
| `ANTHROPIC_API_KEY` (o la del proveedor LLM) | Sí | Composición, pillars, teaser | GitHub Actions |
| `VERCEL_DEPLOY_HOOK` | Recomendada | Redeploy explícito post-merge | GitHub Actions |
| `RESEND_API_KEY` | Sí (newsletter) | Alta + envío | Vercel env + GitHub Actions |
| `RESEND_AUDIENCE_ID` | Sí (newsletter) | Audiencia de Resend | Vercel env + GitHub Actions |
| `RESEND_FROM_EMAIL` | Opcional | Remitente (`<EMAIL_FROM>`) | env script |
| `TURNSTILE_SECRET_KEY` | Opcional | Verificación anti-bot server-side | Vercel env |
| `SLACK_WEBHOOK_URL` | Opcional | Notificar publicación | GitHub Actions |
| `GITHUB_TOKEN` | Automático | `gh` PR/issue/label | GitHub Actions |

- El **site key** de Turnstile es público (va en el HTML); el **secret key** no.
- `.gitignore` debe excluir `.env`, `.vercel`, `__pycache__`.

---

## 16. Seguridad y anti-spam

### 16.1 Anti-spam de la suscripción — 3 capas defensivas

El flujo exacto y el orden están en la sección 12.1. Resumen del **porqué de cada capa**
(nacieron tras una oleada real de *subscription-bombing* —bots dando de alta emails ajenos
en masa—; la defensa se montó por capas, de la más barata a la más cara):

1. **Origin/Referer gate** (capa barata, va primero): corta a los bots que pegan a la API
   con `curl` sin cabecera de origen válida → `403`. Filtra el grueso del ruido sin gastar
   nada.
2. **Honeypot** (`hp`): campo oculto que solo un bot rellena; se responde `200` falso para
   no darle pistas, pero no se registra. Coste cero, atrapa formularios automáticos.
3. **Cloudflare Turnstile invisible** (capa cara, va al final): CAPTCHA sin fricción que
   solo corre en el submit. **Se activa solo si `TURNSTILE_SECRET_KEY` está en el entorno**
   → despliegue progresivo y seguro (el sitio nunca se rompe por activarlo). Verificación
   server-side con `siteverify` + `remoteip`.

Refuerzos: validación regex del email, CORS allowlist, y el tratamiento de `409` de Resend
como éxito silencioso (idempotencia). `/api/unsubscribe` es un GET de baja idempotente sin
estas capas.

> **Sin rate-limiting propio** más allá de las 3 capas (Turnstile mitiga el grueso). Si el
> volumen lo exige, añadir un límite por IP en la función Edge o un WAF por delante.

### 16.2 Seguridad del email (entregabilidad / anti-spoofing)

- Dominio verificado en Resend con **SPF/DKIM/DMARC** en el DNS.
- `reply_to` propio (`<EMAIL_REPLY>`).
- Honeypot inyectado también de forma retroactiva en formularios ya publicados
  (migración idempotente sobre todas las páginas).

### 16.3 Autenticación, autorización y datos

- **No hay usuarios ni login**: el sitio es público de solo lectura. Las funciones Edge no
  autentican al visitante (la protección es el anti-spam).
- La **autoridad de escritura** vive en GitHub Actions (auto-merge con `GITHUB_TOKEN`).
- **Único dato personal**: el email del suscriptor, almacenado solo en Resend. Sin PII de
  terceros. Fuentes de contenido: todas públicas (RSS/Atom). User-Agent identificable.
- Páginas legales obligatorias: `/legal/privacidad/`, `/legal/terminos/`.

### 16.4 Gestión de secretos (higiene)

- Todos los secretos viven en **GitHub Actions secrets** y **Vercel env** — **nunca** en el
  repo ni en los logs (los `console.error` no imprimen la API key).
- `.gitignore` excluye `.env`, `.vercel`, `__pycache__`.
- Distingue **público vs secreto**: la `site key` de Turnstile es pública (va en el HTML);
  la `secret key` no. La API key de Resend y el Audience ID nunca se incrustan en el JS de
  cliente — solo se usan en el servidor (función Edge) leyéndolos de `process.env`.
- Los IDs de modelo LLM van en el YAML, no quemados en el código.

---

## 17. Reglas editoriales de oro

Estas reglas son las que hacen que el medio sea **creíble** y no un panfleto:

1. **No es un memo interno, ni un digest, ni un folleto comercial.** Prioridad al
   lector externo. El patrocinador aparece con elegancia, no como protagonista.
2. **Si no hay novedades reales del patrocinador, la sección "Desde `<MARCA>`" se
   omite.** No se rellena por rellenar.
3. **Nunca inventar cifras.** Prohibido atribuir datos fabricados a empresas privadas
   (tipo "la empresa X recortó costes 18%"). Si no hay dato con fuente, no va. Conviene
   un check automático que **falle el build** si hay demasiados porcentajes/absolutos
   de empresa sin fuente.
4. **Cero rasgos de IA:** guiones largos en prosa (máx 1/edición), estructuras "no es X,
   es Y", grandilocuencia, tríadas huecas, clichés de LinkedIn.
5. **La geografía es la del hecho, no la del lector.** Los mercados primarios siempre
   tienen su sección.
6. **No regalar visibilidad ni SEO a los competidores** de `<BLACKLIST>`.
7. **Solo enlazar/listar páginas que existen en disco.** Nunca URLs muertas.
8. **Enlazar SIEMPRE la fuente original** de cada historia (`source_url`). Un medio que
   reescribe sin atribuir no es un medio.
9. **QA no bloquea, pero registra.** Si algo debe bloquear, hazlo con intención.

---

## 18. Plan de construcción para la IA

Construye en este orden. Verifica cada fase antes de pasar a la siguiente.

**Fase 0 — Intake.** Haz el cuestionario (sección 2). Fija todos los `<PLACEHOLDER>`.

**Fase 1 — Esqueleto.**
- Crea el repo, `requirements.txt`, `.gitignore`, `pipeline-config.yml` (sección 7),
  `assets/radar.css`, `index.html`/`404.html` base, `vercel.json`.
- Escribe `prompts/master-prompt.md` a partir de la plantilla (sección 8).
- Define la taxonomía inicial en `content/taxonomy/` (topics, markets, players).

**Fase 2 — Pipeline determinista.**
- Implementa `ingest → classify → dedupe → select` + `lib/` (config, paths, forbidden).
- Verifica con fuentes reales que produce una selección coherente (sin llamar al LLM).

**Fase 3 — Composición + render.**
- Implementa `compose.py` (1 llamada al LLM → JSON del esquema 9.4) + `lib/templating.py`
  (render HTML por código). Añade el *fallback* stub sin API key.
- Implementa `qa.py` (informativo) y `publish.py` (index/archive/sitemap/rss/memoria).
- Corre el pipeline entero en local y revisa la edición generada.

**Fase 4 — Automatización.**
- Escribe `.github/workflows/weekly-edition.yml` (cron + auto-merge + deploy hook +
  smoke test) y `weekly-canary.yml`.
- Conecta el host al repo. Configura los secrets (sección 15).

**Fase 5 — SEO.**
- Monta la matriz (`content/pillar-matrix/`), `generate_pillar_page.py`,
  `linkify_master.py`, `inject_schema_static.py`, hubs, `robots.txt`, `sitemap.xml`.
- Añade frescura: `sabias-que-pool.md` → `.json`, `rotate_facts.py`,
  `refresh_freshness.py`, `weekly-freshness.yml`.

**Fase 6 — Newsletter.**
- Implementa `api/subscribe.js` y `api/unsubscribe.js` (con las 3 capas anti-spam),
  `inject_newsletter_ctas.py`, `generate_newsletter_copy.py`, `generate_email.py`,
  `send_newsletter.py`. Verifica el dominio en Resend (SPF/DKIM/DMARC).

**Fase 7 — Lanzamiento.** Recorre el checklist de la sección 19.

---

## 19. Checklist de lanzamiento

- [ ] `pipeline-config.yml` completo (fuentes reales, cuotas, blacklist, mercados).
- [ ] `prompts/master-prompt.md` con la voz y las reglas del nicho.
- [ ] El pipeline corre en local y genera una edición creíble (revisada a mano).
- [ ] QA pasa como informativo; ningún check crítico se salta.
- [ ] `vercel.json` con clean URLs, cache y redirects. Sitio desplegado.
- [ ] Secrets configurados en GitHub Actions y el host (ninguno en el repo).
- [ ] Deploy hook + smoke test + canary funcionando.
- [ ] `robots.txt`, `sitemap.xml`, `rss.xml`, Schema.org por página.
- [ ] Cada historia enlaza su fuente original (`source_url`).
- [ ] Newsletter: dominio verificado en Resend, alta/baja probadas, teaser enviado a
      una lista de prueba.
- [ ] Anti-spam de la suscripción activo (origin gate + honeypot + Turnstile).
- [ ] Páginas legales (`/about/`, `/legal/privacidad/`, `/legal/terminos/`).
- [ ] `README.md` propio del proyecto.
- [ ] Cron de la edición semanal habilitado.

---

## 20. Glosario

| Término | Definición |
|---|---|
| **Edición / magazine** | La revista periódica (`magazines/YYYY-MM-DD-<slug>.html`). |
| **Hub** | Página índice de una dimensión que lista páginas existentes. |
| **Página pilar** | Página temática evergreen de SEO (topic × mercado × intención). |
| **Stub** | Página mínima `noindex,follow` que acumula equity hasta liberarse. |
| **Matriz viva** | Sistema YAML/CSV que define las páginas planeadas y su ciclo de vida. |
| **Tier** | Prioridad de una página (T1/T2/T3): fija cadencia de revisión y si arranca noindex. |
| **Intención** | Intención de búsqueda (informacional/comparativa/guía/regulación) → schema. |
| **Dimensión** | Tipo de página en la matriz: topic, use-case, vertical, subgeo. |
| **DYK / "Sabías qué"** | Caja con un dato curado, rotado por semana/página. |
| **Frescura** | Actualización controlada de la fecha de modificación (señal de "vivo" a Google). |
| **Modo (normal/short/pause)** | Decisión de selección según el material disponible. |
| **Master prompt** | La constitución editorial (system prompt del LLM). |
| **Memoria editorial** | Log append-only de qué se cubrió y cuándo (anti-repetición). |
| **Blacklist de competidores** | Marcas que excluyen un item de la selección. |
| **Deploy hook** | URL POST que fuerza un redeploy explícito en Vercel. |
| **Canary** | Verificación diferida de que el deploy responde 200. |
| **Honeypot** | Campo oculto anti-bot; si se rellena, se finge éxito sin registrar. |
| **Owned media** | Medio propiedad de una marca, usado como activo de captación. |

---

## Apéndice A · Decisiones de diseño (y por qué)

Estas son las decisiones que definen el sistema. Respétalas salvo que tengas una razón
fuerte para cambiarlas.

| # | Decisión | Motivo | Alternativa descartada | Consecuencia |
|---|---|---|---|---|
| D1 | **Sin base de datos; Git como store** | Auditabilidad, reproducibilidad, coste cero | Postgres/Supabase/KV | Estado versionado; no apto para escrituras concurrentes de usuario |
| D2 | **Clasificación determinista por keywords** | Gratis, auditable, sin latencia LLM | Clasificación por LLM/embeddings | Falsos +/− que se mantienen a mano |
| D3 | **1 sola llamada LLM por edición** | Coste mínimo, simplicidad | Multi-agente / varias pasadas | Contexto limitado al resumen del RSS |
| D4 | **El HTML lo renderiza el código, no el LLM** | Consistencia estructural garantizada | Que el LLM devuelva HTML | El LLM solo aporta contenido (JSON) |
| D5 | **QA informativo, no bloqueante** | Nunca perder una semana | QA bloqueante | Puede publicar con avisos; se registran |
| D6 | **Una sola hoja CSS + pocas vars semanales** | Identidad reconocible, sin rediseño | CSS ad-hoc por edición | Cambios de sistema van en PR aparte |
| D7 | **Blacklist de competidores en la selección** | No regalar visibilidad al rival | Mencionarlos como "señal" | Se pierde alguna noticia |
| D8 | **No autoenlazar a competidores** | Ídem, en el interlinking | Enlazar sus webs | Sus marcas no se autoenlazan |
| D9 | **Deploy hook explícito + smoke test + canary** | El webhook implícito de Vercel falló una vez | Confiar solo en el webhook | Redeploy garantizado y verificado |
| D10 | **Suscriptores en Resend, no en DB** | Delegar entregabilidad y almacenamiento | KV/DB propio | Dependencia de Resend; dedup de envío en Git |
| D11 | **Matriz "viva" en vez de N páginas fijas** | Escalar SEO gestionando ciclo de vida | Generar todo de una vez | Complejidad de tiers/noindex/threshold |
| D12 | **Prioridad geográfica por peso de mercado** | Es el mercado real del patrocinador | Reparto equitativo | Mercados secundarios entran por cuota, no por score |
| D13 | **Analítica sin cookies** | Privacidad + sin banner de consentimiento | GA4 con cookies | Menos granularidad, cero fricción legal |

---

## Apéndice B · Gotchas y lecciones aprendidas

Errores reales que costaron tiempo. Documentarlos evita repetirlos.

- **`select.py` sombrea el módulo `select` del stdlib.** Cualquier script en `scripts/`
  que importe `subprocess`/`os.popen` puede coger el fichero equivocado. *Workaround:* al
  inicio del script, si `sys.path[0]` acaba en `/scripts`, hacer `sys.path.pop(0)`.
- **BeautifulSoup re-serializa el HTML** al guardar: reordena atributos, autocierra tags,
  colapsa espacios. No es un bug, pero **ensucia los diffs**. Para regex sobre atributos,
  soporta ambos órdenes.
- **Regenerar una pilar pisa los fixes manuales** (cleanups, disclaimers). Siempre re-correr
  la cadena de linking + `seo_polish` + `rebuild_sitemap` + `qa_pillars` después.
- **El PAT de GitHub necesita scope `workflow`** para pushear ficheros en
  `.github/workflows/`. Sin ese scope, el cron de frescura no se puede commitear.
- **El webhook implícito de deploy de Vercel puede fallar.** Por eso el pipeline dispara un
  **deploy hook explícito** y hace **smoke test** (varios `curl` con reintentos) + un
  **canary** diferido que abre un issue si el sitio no responde 200.
- **Las páginas nuevas nacían `noindex` por defecto** por un flag del renderer de pilares.
  Decide conscientemente el default y usa un flag para forzar stub.
- **Numeración de ediciones por conteo de filas** en `archive.html`: frágil si cambia el
  markup. Si algo raro pasa con la numeración, mira ahí.
- **El `python3` del sistema puede no traer las libs** (p. ej. BeautifulSoup). Usa un
  intérprete que tenga las dependencias instaladas para correr los scripts en local.
- **Contexto del LLM limitado al resumen del RSS:** si el feed da poco texto, la redacción
  sufre (lo marca el check C2). No es un fallo, es una restricción de diseño (D3).
- **Mover ficheros entre carpetas desde un shell sandboxed puede perder el fichero** si el
  destino queda fuera del directorio de trabajo. Trabaja con las herramientas de archivo o
  dentro del propio repo; ten copia en Git antes de mover nada importante.

---

_Fin del blueprint. Este documento es agnóstico de temática y no contiene secretos:
rellena los `<PLACEHOLDER>` con el cuestionario de la sección 2 y sigue el plan de la
sección 18 para construir tu propio medio editorial autónomo._
