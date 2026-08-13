# Autopress — Progreso de construcción

> Registro vivo de **qué se ha construido, qué decisiones se tomaron y qué falta**.
> Complementa a `KIT-v2-DECISIONES-Y-PLAN.md` (el plan) con el estado real de la obra.
> **Última actualización: 2026-08-11.**

## 🗺️ Mapa del proyecto (dónde estamos) — 2026-08-11

**Motor y credibilidad: COMPLETOS. Todos los críticos/altos de las 2 reviews externas
(ChatGPT + Gemini): cerrados.** Quedan piezas de *completitud* y *empaquetado*.

**✅ Hecho y verificado (29/29 tests):**
- Pipeline: ingest (feeds reales + fixtures) → clasificar → deduplicar → seleccionar →
  compose (LLM/stub) → QA → publicar. `--config`/`--fixtures`/`--production`.
- Credibilidad: procedencia por historia, **cifras bloqueadas si no están en la fuente**,
  anti-inyección (escape `<`/`>`), URLs seguras, citas `[1][2]`.
- Gobernanza: `risk_profile` real (auto/review/strict), fuentes **independientes**, gate de
  publicación, `noindex` por defecto.
- Persistencia: `data/editions/` (Git como BD), archivo/RSS/sitemap acumulan histórico.
- CI: workflow semanal (auto→publica, review/strict→PR, bloqueado→falla).
- SEO: JSON-LD, Open Graph, `lastmod`.
- Newsletter: tokens firmados HMAC (doble opt-in + baja) testeados; flujo documentado.
- **Bilingüe ES+EN**: el medio se renderiza entero en el idioma configurado (i18n del chrome);
  las guías 00-12 + README traducidas al inglés en `en/`.
- Empaquetado base: `AGENTS.md` + cuestionario, `README`, `requirements`, `LICENSE`, schema.
- Docs no-técnicas: `00`-`04` (quickstart, alcance, cuentas, costes, despliegue).
- Legal: `starter/legal/` (privacidad, IA/AI Act, derechos-fuentes, términos).

**✅ Track A COMPLETO** (C-01, A-01, A-02, C-03, M-01, M-05, C-02, A-03, A-06, A-07, **A-04**).
El template compartible se genera con `pack.py` (starter/ en la raíz, guías a nivel raíz, docs de
mantenedor fuera): **51 tests pasan dentro del template, 0 enlaces rotos, workflow en la raíz.**

**✅ Camino "Integridad primero" COMPLETO (Lotes 1–6 + reframe) — 64 tests.**
- **1 · Estado**: auto no auto-indexa (opt-in), gate por renderizado, approve revalida, RSS solo
  aprobadas, fixtures fuera de prod, bucle review/strict (promote).
- **2 · Seguridad**: SSRF con DNS+redirecciones (IP decimal), XSS (whitelist `style`/`palette`,
  `safe_url` en enlaces legales), `getpass` para la clave, Dependabot (Actions/pip).
- **3 · Riesgo**: léxico de acusaciones ampliado (robo/delitos, ES+EN).
- **4 · Robustez**: memoria entre semanas (`seen.json`), escrituras atómicas + limpieza de
  huérfanos, `retract.py`, fechas inválidas → recencia ~0.
- **5 · Legal**: campos de derechos por fuente (schema), enlaces legales `.md`→`.html` seguros.
- **6 · Otros**: `site.domain` obligatorio en prod, `--help`/flags desconocidos, `serve` respeta
  exit, preview≠published, normalización de idioma (BCP-47).
- **Reframe**: reposicionado como "digest RSS asistido, review-first"; coste real = atención;
  promesa "verificación de hechos" → "curación con cita"; quitada la de cooling.

**✅ Llave en mano (2026-08-12):** legal auto-rellenado por `setup`; **newsletter real**
(`functions/api/subscribe|confirm|unsubscribe.js` para Cloudflare Pages + token HMAC compatible);
**`GUIA-COMPLETA.md`** paso a paso "para tontos" (dónde dar de alta cada cuenta, API key, calidad
de contenido, deploy). El agente automatiza todo salvo crear cuentas/login (instruido en AGENTS.md).

**⏳ Pendiente:**
- **Path B (fase propia)**: leer el artículo real + evidencia por afirmación (C-04), reputación
  por fuente + anti-envenenamiento, gate de originalidad.
- Verificar en vivo el circuito de IA (necesita una clave) y traducir `GUIA-COMPLETA` a EN.
- Residuos menores: fijar Actions por SHA completo (Dependabot ya avisa); QA de idioma del
  contenido (heurístico); token de newsletter con email en la URL (opaco necesita storage).

_Track B hecho: **A-05 riesgo por artículo** (acusación sin atribución+corroboración → bloqueo en
cualquier perfil) + **enriquecimiento de evidencia** (duplicados aportan su resumen)._

**Onboarding web:** `EMPIEZA-AQUI.md` (+ `en/START-HERE.md`) con el **prompt de inicio** y el aviso
de que hace falta un **agente de código** (Claude Code/Cursor/ChatGPT-agente), no un chat normal.
Incluidos en el template (`pack.py`), enlazados desde el README.

**Revisión #4 (6/10) + Camino "Integridad primero":** ver Changelog. Hallazgo de fondo: **falsa
confianza** — el kit parecía un medio que verifica, siendo un digest de teasers RSS. Decisión del
usuario: reencuadrar honesto + endurecer (no "leer artículos reales" ahora). **Lote 1 hecho (59
tests).** Regresión de empaquetado (`cd starter` en el template) detectada por el review y **corregida**.

**2026-08-11 · Camino "Integridad primero" (Lotes 1–6) ejecutado en autónomo.** Tras el review #4
(6/10) que destapó la "falsa confianza", se reencuadró el producto (digest RSS review-first) y se
endurecieron gobernanza, seguridad, riesgo, robustez y legal (ver la lista de arriba). Nuevos
scripts: `promote.py`, `retract.py`, `seen.py`; nuevos gates (`no-domain`, `fixtures-in-production`,
auto-index opt-in, gate por historias renderizadas); `approve.py` revalida todo; SSRF con
resolución DNS y revalidación de redirecciones; whitelist de temas (XSS); `getpass`; workflow
`approve-release.yml` + `dependabot.yml`. Reframe honesto en README (ES+EN) y `ARCHITECTURE`.
**64 tests; template regenerado (0 `cd starter`, 0 enlaces rotos, tests verdes dentro).**

**Bilingüe COMPLETO (un solo zip):** el medio (chrome i18n es/en), las **guías** (`en/`), el **spec
de la IA** (`en/AGENTS.md`, `en/ARCHITECTURE.md`, `en/HOWTO.md`), las **plantillas legales**
(`legal/en/*.md`, renderizadas según `site.language`, con etiquetas de footer localizadas) y los
READMEs internos (`newsletter/README.en.md`, `examples/…/README.en.md`). Selectores de idioma en los
docs ES. Verificado: 55 tests, 0 enlaces rotos en el template. Decisión: **un zip** (código idéntico,
solo cambian docs → dos zips sería duplicar el proyecto).

_Detalle cronológico en el Changelog (abajo)._

## Estado en una frase

El motor del `starter/` (opción **C**: implementación de referencia genérica y ejecutable)
corre **end-to-end en local, sin cuentas ni claves**:
`fixtures → clasificar → deduplicar → seleccionar → compose (LLM o stub) → QA por niveles →
publicar sitio navegable`. La **redacción con IA** ya está cableada (`compose.py`, con
anti-inyección + procedencia + fallback a stub); la clave va en `.env` (`.env.example`).
Sistema de themes de **30 combinaciones** (6 estilos × 5 paletas) con galería. Tests *golden*,
*ingest* y *compose* en verde (8/8). Arquitectura documentada en `starter/README.md`.

## Hecho (verificado / verde)

| Área | Ficheros | Estado |
|---|---|---|
| Núcleo determinista | `scripts/lib/text.py`, `classify.py`, `dedupe.py`, `select_stories.py`, `pipeline_core.py` | ✅ corre |
| Test golden (contrato) | `fixtures/{raw.jsonl,config.json,expected/selection.json}`, `tests/test_pipeline_golden.py` | ✅ 3 tests OK |
| Contrato de config | `autopress.schema.json`, `scripts/validate_config.py` | ✅ valida |
| Diagnóstico operador | `scripts/doctor.py` | ✅ "LISTO para local" |
| Compose sin LLM | `scripts/compose_stub.py` (con procedencia: fuente del ítem crudo, no inventada) | ✅ |
| Render | `scripts/lib/templating.py`, `scripts/lib/site.py` | ✅ |
| Publicar sitio | `scripts/publish.py`, `scripts/pipeline.py` → `site/` (home, permalink, archivo, sitemap, rss) | ✅ navegable |
| QA por niveles | `scripts/qa.py` (blocking / review_required / warning) | ✅ alineado con `sources` |
| **Compose con LLM** | `scripts/compose.py` (SDK Anthropic, anti-inyección, procedencia validada, fallback stub) | ✅ cableado + test |
| **Superficie de tokens** | `.env.example`, `.gitignore`, carga `_load_dotenv` en pipeline, `compose.model` en config/schema | ✅ |
| **Prompt maestro** | `prompts/master-prompt.example.md` (constitución editorial + regla anti-inyección) | ✅ plantilla |
| **Doc de arquitectura** | `starter/README.md` (cómo corre, pipeline, config, tokens, límites) | ✅ para revisión externa |
| **Empaquetado (B)** | `AGENTS.md` raíz (entry + cuestionario), `starter/requirements.txt` (pinneado), `LICENSE` (MIT + CC BY 4.0), `starter/LICENSE` | ✅ |
| **AGENTS.md reconciliado** | `starter/AGENTS.md` apunta a ficheros reales (blueprint raíz, `.env`, citas numeradas, mapa de `scripts/`) | ✅ sin refs rotas |
| **Onboarding no-técnico (C)** | `00-QUICKSTART` (checkpoints), `01-ANTES-DE-EMPEZAR` (alcance/honestidad), `02-CUENTAS-Y-DOMINIO` (SPF/DKIM/DMARC), `03-COSTES` (tabla verificada) | ✅ |
| **Guardarraíles credibilidad (Cluster 1)** | `compose.py` (source_refs por historia + saneo `<`/`>`), `qa.py` (check **bloqueante** de cifras sin fuente), `pipeline.py` (gate de producción + exit≠0), `lib/text.py` (`safe_url`/`number_tokens`), `noindex` por defecto en `site.py` | ✅ 15/15 tests |
| **Tests adversariales** | `tests/test_guardrails.py`: fuentes cruzadas, cifras inventadas, `javascript:`, ruptura de delimitador, noindex | ✅ |
| **Reconciliación alcance (Cluster 4)** | banner D4 en el blueprint, `starter/AGENTS.md` (blueprint deja de ser "fuente de verdad" sobre D4), quickstart multiplataforma (venv+deps, Windows, servidor local, honestidad fixtures), matiz legal opt-in + HMAC | ✅ |
| **Pipeline real (Cluster 2a)** | `ingest` cableado al `pipeline` (feeds reales con `sources` en config; fixtures si no), `_fetch` robusto (timeout/UA/reintentos/límite), diagnóstico por fuente (ok/empty/error), `as_of` en runtime, `--config`/`--fixtures` | ✅ 17/17 tests |
| **Gobernanza real (Cluster 2b/3)** | `registrable_domain` (cuenta fuentes INDEPENDIENTES; mismo cable ≠ 2), QA `independent_sources` bloqueante **solo en `strict`**, `risk_profile` en el gate (`auto` indexa; `review`/`strict` → preview `pending_review`) | ✅ 21/21 tests |
| **Plantillas legales (Cluster 5a)** | `starter/legal/`: `privacidad`, `divulgacion-ia` (AI Act), `derechos-fuentes` (parafraseo + takedown), `terminos` + `README` con checklist; placeholders + aviso "no es asesoría legal" | ✅ |
| **Guía de despliegue (Cluster 5b·i)** | `04-DESPLIEGUE.md` host-agnóstico: recomendado Cloudflare + Netlify/GitHub Pages/Vercel con aviso comercial; ToS verificados 2026-08; host+monetización en cuestionario; agente verifica ToS al construir | ✅ |
| **Persistencia de ediciones (Cluster 5b·ii)** | `publish.py` reconstruye el sitio desde `data/editions/*.json` (Git como BD); archivo/RSS/sitemap **acumulan histórico**; persiste solo en publicación real; preview no toca el almacén | ✅ 23/23 tests |
| **CI semanal (Cluster 5b·iii)** | `.github/workflows/publish.yml`: cron + manual, `permissions` mínimos; `auto`→publica, `review`/`strict`→**abre PR**, bloqueado→falla; compose IA una vez, host sirve `site/` versionado | ✅ YAML válido |
| **SEO básico (Cluster 5b·iv)** | JSON-LD `NewsArticle` (con autoría), Open Graph, `<lastmod>` en sitemap; `<` escapado en el JSON-LD | ✅ 24/24 tests |
| **Newsletter (Cluster 5b·v)** | `scripts/newsletter.py` tokens HMAC (doble opt-in + baja firmada, anti-bombing), form cableado a `/api/subscribe`, `newsletter/README.md` con handler de referencia + deploy por host | ✅ 29/29 tests |
| **Asistente + preview (admin)** | `scripts/setup.py` (wizard incremental → escribe config/.env/prompt), `scripts/serve.py` (build + sirve preview), `validate_dict`; onboarding **por niveles** (nada bloquea) | ✅ 33/33 tests |
| **Ejemplo trabajado (B)** | `examples/movilidad-mx-es/` (config + master-prompt rellenos + README con niveles); corre con fixtures → "Radar Movilidad" | ✅ |
| **Catálogo de settings descubrible** | `scripts/settings.py` (fuente única: qué se configura, valor actual y *dónde* — config/.env/workflow/host); comando `settings [tema]`; gancho en `AGENTS.md` ("muéstrame los settings"); `site.timezone` añadido | ✅ 37/37 tests |
| **Docs de guía (D)** | `05-CUESTIONARIO`, `06-ADAPTACION-TEMATICA`, `07-GUARDARRAILES`, `08-MODO-INDEPENDIENTE`, `10-SEO`, `12-TROUBLESHOOTING` | ✅ |
| **Costes precisos (6)** | `03-COSTES` con **fórmula reproducible** (tokens in/out), aviso precio intro Sonnet, escalón Resend (~1.000 contactos) | ✅ |
| **i18n del medio (capa 1 bilingüe)** | `lib/i18n.py` (es/en) + `templating`/`site` localizados: nav, footer, newsletter, archivo, kicker; medio en EN sale entero en EN; idioma desconocido→EN | ✅ 41/41 tests |
| **Docs en inglés (capa 2 bilingüe)** | `en/`: README + guías `00`-`12` traducidas (fielmente, código/enlaces preservados); selector de idioma ES↔EN en ambos README | ✅ 0 enlaces rotos |
| Themes | `theme/theme.css` (6 estilos × 5 paletas, light+dark) | ✅ |
| Galería navegable | `scripts/render_demo.py` → `sample-output/gallery.html` | ✅ 30 combinaciones |

**Cómo correr (local, sin cuentas):**
```bash
cd starter
PYTHONPATH=. python3 -m unittest tests.test_pipeline_golden   # contrato determinista
python3 scripts/doctor.py                                     # diagnóstico
PYTHONPATH=. python3 -m scripts.pipeline                      # publica site/ navegable
PYTHONPATH=. python3 -m scripts.render_demo                   # galería de themes
```

## Decisiones bloqueadas

- **D1** SEO técnico siempre; generación masiva OFF por defecto; calidad-gate de indexación.
- **D2** Caso base exigente pero **genérico** (sin temática fija); perfiles `auto`/`review`/`strict`.
- **D3** Hosting por defecto **Cloudflare Pages** (Vercel con aviso: Hobby prohíbe uso comercial).
  **Evolución (2026-08-11):** el output es un **sitio estático portable** → **host-agnóstico**.
  No se ata a Cloudflare; se **recomienda** (no se obliga) y se dan 4 opciones con guía
  (`04-DESPLIEGUE.md`). Aviso de uso comercial cubre **Vercel Hobby Y GitHub Pages** (ambos lo
  prohíben; Cloudflare y Netlify sí permiten). Host + monetización van en el **cuestionario**, y
  **el agente verifica los ToS vigentes al construir** (los términos caducan).
- **D4 (2026-08-10)** **Alcance = solo curación de noticias.** El kit sirve para temas con
  **flujo vivo de fuentes** (flotas, geopolítica de actualidad, energía…), donde la IA
  *resume* hechos reales y los cita. **NO** cubre temas estáticos/históricos ni revistas de
  ensayo *generado* (otro producto: más caro, menos procedencia, más riesgo de alucinación).
  Decidido por el usuario. Documentado en `01-ANTES-DE-EMPEZAR.md`; encuadre corregido en
  `README.md` y `AGENTS.md`.
- **Starter = opción C** (referencia genérica ejecutable, no "solo instrucciones").
- **Procedencia estilo ChatGPT**: el LLM devuelve `ref_id`, el renderer copia la fuente; se
  rechazan IDs desconocidos. (Pendiente de formalizar del todo.)
- **Themes 6×5**, system fonts self-hosted, galería para la web personal.
- **NUEVO (2026-08-10):** **citas numeradas multi-fuente por historia** (estilo Perplexity):
  `story.source_refs = [ref_id, …]` → `[1][2]` enlazando al original. Habilita el guardarraíl
  de ≥2 fuentes independientes en `strict`.

## Revisión externa (4 IAs) — consolidado

**Ya abordado (total o parcial):** starter ejecutable · fuente por historia · QA por niveles
(inicial) · `select.py`→`select_stories.py` · schema con gobernanza (`risk_profile`,
`editorial.mode`, `block_stub_in_production`, `ai_disclosure`) · aviso de uso comercial de Vercel.

**Pendiente (prioridad alta):**
1. Procedencia formal `ref_id` + **citas numeradas multi-fuente**.
2. QA completo + **delimitadores anti-inyección de prompt** vía RSS + fixtures adversariales.
3. Ingest real (feedparser) + `sources` en config.
4. Doble opt-in + baja con token firmado.
5. Adaptadores de deploy (**Cloudflare primero**) + workflow CI con `permissions`.
6. Guías no-técnicas: `00-QUICKSTART` (checkpoints), `02b-SPF/DKIM/DMARC`, tabla "tú vs el agente".
7. `requirements` con versiones fijas + `CHANGELOG` + fecha de verificación.
8. Docs `00`–`12` y plantillas legales (`11-LEGAL/`).

## Próximos pasos (orden propuesto)

1. ~~Citas numeradas + procedencia `ref_id`~~ ✅ (Fase A)
2. ~~Ingest real (feedparser)~~ ✅ (Fase A)
3. ~~LLM compose real + `.env.example` (superficie de tokens)~~ ✅ (Fase A2)
4. ~~Empaquetado (B): `AGENTS.md` raíz, `requirements.txt` pinneado, `LICENSE`~~ ✅ (Fase B)
5. ~~Onboarding no-técnico (C): `00-QUICKSTART`, `01`, `02` (SPF/DKIM/DMARC), `03-COSTES`~~ ✅ (Fase C)
6. ~~Revisión externa (ChatGPT + Gemini)~~ ✅ consolidada → plan por clusters.
7. ~~Cluster 1 (credibilidad) + Cluster 4 (alcance/docs)~~ ✅
8. ~~Cluster 2a (pipeline real: ingest cableado + HTTP robusto)~~ ✅
9. ~~Cluster 2b + 3 (gobernanza real: fuentes independientes + risk_profile)~~ ✅
10. **Cluster 5 — Legal + vertical operativo**:
    - ~~5a · plantillas legales `starter/legal/` (privacidad, divulgación IA/AI Act, derechos RSS, términos)~~ ✅
    - **5b · vertical operativo**: CI (GitHub Actions + `permissions`) + adaptador Cloudflare +
      **persistir ediciones** (archivo/RSS/sitemap desde todas) + newsletter doble opt-in con token HMAC. ← siguiente
11. **Cluster 6 — Costes**: fórmula/tokens, caducidad precio Sonnet, escalón de Resend.
12. **Residuales**: precisión del dedupe (eventos distintos), cooling-window horaria de `strict`.
13. **Publicación (F)**: GitHub template + ZIP público + galería en la web.

## Changelog

- **2026-08-10** — Arranque del `starter/` (C): núcleo determinista + test golden; contrato de
  config (`schema` + `validate_config` + `doctor`); sistema de themes 6×5 + galería navegable;
  edición completa navegable (`pipeline` + `publish` → home/permalink/archivo/sitemap/rss);
  QA por niveles (inicial). Todo offline y en verde.
- **2026-08-10 · Fase A** — Ingest RSS real (`feedparser`) + test offline; **dedup con memoria
  de procedencia** (los duplicados pasan a ser fuentes adicionales); **citas numeradas
  multi-fuente `[1][2]`** (estilo Perplexity, con rechazo de IDs desconocidos); pulido de
  diseño (titulares/kickers en color de acento, degradados, **caja de suscripción**, hovers).
- **2026-08-10 · Fase A2** — **Redacción con IA cableada** (`scripts/compose.py`, SDK Anthropic):
  lee `ANTHROPIC_API_KEY` del entorno; contenido RSS en `<untrusted_sources>` (**anti-inyección**);
  `assemble()` valida procedencia (descarta historias/fuentes con `ref_id` desconocido — la IA no
  puede inventar); **fallback automático a stub** si no hay clave o algo falla (el kit nunca se
  rompe, nunca gasta sin querer). **Superficie de tokens**: `.env.example` + `.gitignore` + carga
  de `.env` en el pipeline; **modelo en el YAML** (`compose.model`, default económico
  `claude-sonnet-5`) nunca en código. `qa.py` alineado con el modelo `sources`. Nuevo
  `prompts/master-prompt.example.md` (constitución editorial). **`starter/README.md`** documenta
  toda la arquitectura para revisión externa. Tests: 8/8 en verde (golden + ingest + compose).
- **2026-08-10 · Fase B (empaquetado)** — **`AGENTS.md` raíz**: punto de entrada del kit con el
  **cuestionario de arranque** completo (temática, idioma, mercados, tono, riesgo, host…) y el
  orden de trabajo; autosuficiente aunque los docs `00`–`12` aún no existan. **`starter/requirements.txt`**
  pinneado (`feedparser==6.0.11`, `anthropic==0.96.0`; núcleo solo stdlib; verificado con Python
  3.13.1). **Licencia doble**: `LICENSE` raíz (MIT para código + CC BY 4.0 para docs) y
  `starter/LICENSE` (MIT autocontenido). **Reconciliación de `starter/AGENTS.md`**: eliminadas las
  referencias a ficheros inexistentes (`04-BLUEPRINT.md`, `05-CUESTIONARIO.md`,
  `07-GUARDARRAILES.md`, `pipeline-config.example.yml`) → ahora apunta al blueprint de la raíz, al
  cuestionario del `AGENTS.md` raíz, a `.env`, a las citas numeradas y al mapa real de `scripts/`.
  Verificado: 0 refs rotas, requirements satisfechos, 8/8 tests verdes.
- **2026-08-10 · Fase C (onboarding no-técnico) + Decisión D4** — Cuatro docs de arranque para
  no técnicos, guiados por **checkpoints** ("✅ deberías ver…" / "🔧 si falla"): `00-QUICKSTART.md`
  (de cero a primera edición, stub → clave real), `01-ANTES-DE-EMPEZAR.md` (para quién SÍ/NO,
  qué es autónomo), `02-CUENTAS-Y-DOMINIO.md` (GitHub, Cloudflare Pages, dominio, y **SPF/DKIM/
  DMARC** con DMARC progresivo `none→quarantine→reject`), `03-COSTES.md` (tabla verificada
  2026-06: Haiku ~$0.30, Sonnet ~$0.73, Opus ~$1.20/mes; free tiers; aviso Vercel; 3 escenarios).
  **Decisión D4**: alcance del kit = **solo curación de noticias** (temas con flujo vivo de
  fuentes), no temas estáticos/históricos ni ensayo generado; encuadre corregido en `README.md`
  y `AGENTS.md`. Surgió de la pregunta del usuario (flotas MX/ES vs. "urbanismo del s. XVIII").
- **2026-08-10 · Revisión externa #1 (ChatGPT)** — auditoría fuerte y en su mayoría correcta
  (verificada en código). **Críticos confirmados:** (1) procedencia valida que la URL existe pero
  NO que respalde el texto → una historia puede citar la fuente de otra y colar cifras inventadas
  (`compose.py` `assemble` usa el set global de ids; `qa.py` no compara cifras); (2) el pipeline
  operativo **nunca llama a `ingest()`** (siempre `fixtures/raw.jsonl`); (3) `publish()` corre
  siempre, aunque `mode=pause`/QA=`blocked`/stub, y todo sale `index,follow` (`site.py:43`);
  `block_stub_in_production` nunca se lee; (4) no se acumula histórico de ediciones. **Altos:**
  `risk_profile`/`cooling_window`/`min_independent_sources` solo en schema, sin código → `strict`
  es protección ficticia; anti-inyección sin escapar el delimitador; **`javascript:` en `href`**
  (templating.py:43); ingest sin timeout/reintentos/bozo, excepciones silenciadas; fechas frágiles;
  dedupe cuenta el mismo cable como 2 fuentes "independientes"; legal (derechos RSS, newsletter
  `onsubmit=return false`, disclosure de patrocinio); SEO sin quality-gate real; quickstart no
  multiplataforma; **blueprint contradice D4** (promete patrocinado/evergreen/Vercel). Consolidación
  → plan por clusters (ver `REVISION-EXTERNA.md` / siguiente entrada). Pendiente: 1-2 reviews más.
  (10 dimensiones, formato de salida fijo, decisiones D1–D4 marcadas como no re-litigables),
  orden de lectura de ficheros por tiers, y comando de snapshot. Generado `autopress-review.zip`
  (111 KB, verificado sin `.env` real / `site/` / `__pycache__`) para subir a las otras IAs.
- **2026-08-10 · Revisión externa #2 (Gemini)** — **converge fuertemente con ChatGPT** (triangulación).
  Mismos 2 críticos: (1) romper el delimitador `</untrusted_sources>` desde un feed, (2) QA
  informativo + auto-merge publica alucinaciones → check determinista de cifras. Coincide también
  en legal (doble opt-in + baja HMAC, plantillas `11-LEGAL/`), Windows en el quickstart, y aviso
  D4 en §11 del blueprint. Aporta: escapar `<`/`>` (no solo la etiqueta) y firmar la baja con HMAC.
- **2026-08-10 · Cluster 1 (credibilidad) + Cluster 4 (alcance) IMPLEMENTADOS.** Confirmados en
  código los hallazgos y arreglados con tests. **Cluster 1:** (a) `source_refs` restringido a las
  fuentes **de esa historia** (`assemble` usa `_story_allowed_ids`; adiós fuentes cruzadas);
  (b) **check bloqueante `numbers_supported`** en `qa.py` — toda cifra ≥2 dígitos de la redacción
  debe aparecer en la fuente (`number_tokens`); las historias llevan `_evidence`; (c) **gate de
  publicación** en `pipeline.py`: en `--production`, `stub`/`pause`/`qa-blocked` **no publican** y
  salen con código 1; en local se genera **preview `noindex`**; (d) **`safe_url`** (solo http/https)
  mata `javascript:`/`data:` en ingest, en el resolver de fuentes y en las citas; (e) **saneo del
  delimitador** escapando `<`/`>` en el contenido RSS antes de enviarlo al LLM. `tests/test_guardrails.py`
  fija los 5 con los payloads de los reviewers. **Cluster 4:** banner de alcance D4 al inicio del
  blueprint + precedencia D4/starter sobre el blueprint en `starter/AGENTS.md`; quickstart
  multiplataforma (venv+`pip install` al inicio, nota PowerShell, **servidor local** en vez de abrir
  el `.html`, honestidad "esto redacta la demo, no tus feeds aún"); matiz legal del opt-in +
  baja HMAC en `02`. **Tests: 15/15 verdes** (8 previos + 7 guardarraíles).
- **2026-08-10 · Cluster 2a (pipeline real).** Cierra el crítico "el pipeline nunca llama a
  `ingest()`". Ahora, si el config trae `sources`, el pipeline **ingiere de feeds reales**
  (`ingest` con `_fetch`: timeout, User-Agent identificable, reintentos con backoff, límite de
  tamaño) y devuelve **diagnóstico por fuente** (`ok`/`empty`/`error` — una fuente caída ya no
  se confunde con vacía); si no hay `sources`, usa los fixtures (demo/tests reproducibles). El
  `as_of` se calcula en runtime salvo que el operador lo fije. Nuevos flags `--config <ruta>`
  (config de producción propia) y `--fixtures`. `sources`/`ingest` añadidos al schema. El estado
  del pipeline reporta `source`, `raw_count` y `feeds`. Verificado offline: feed local → `source:
  feeds`, `raw_count: 2`, diagnóstico `ok`. **Tests: 17/17** (+diagnóstico de feeds, +gate del
  pipeline). Pendiente **2b**: dedupe con independencia de fuente (mismo cable ≠ 2 fuentes), junto
  al Cluster 3 (risk_profile real).
- **2026-08-10 · Cluster 2b + 3 (gobernanza real).** `risk_profile` deja de ser promesa: (a)
  **fuentes independientes** — `registrable_domain` (eTLD+1 aproximado) cuenta editores distintos;
  dos URLs del mismo dominio ya NO cuentan como corroboración; (b) QA añade el check **bloqueante
  `independent_sources` solo en `strict`** (≥`min_independent_sources`, default 2); (c) el **gate por
  perfil**: solo `auto` auto-indexa en producción, `review`/`strict` generan preview `noindex` con
  `pending_review=true` (fiel a "abre PR y para"). Verificado: `risk_profile=strict` sobre la demo
  (fuentes de un solo dominio) → `independent_sources:false` → `blocked`. **Tests 21/21** (+4:
  dominio registrable, strict bloquea/pasa, review sin check). Residuales anotados: precisión del
  dedupe (fusionar eventos distintos con títulos parecidos) y cooling-window horaria de `strict`
  (requiere timestamps con hora, no solo día) — mejoras futuras.
- **2026-08-10 · Cluster 5a (plantillas legales).** `starter/legal/` con 4 plantillas +
  `README`: `privacidad.md` (RGPD: responsable, base legal=consentimiento, encargados, derechos,
  sin cookies de seguimiento), `divulgacion-ia.md` (transparencia AI Act: contenido redactado por
  IA desde fuentes reales, supervisión humana por perfil de riesgo, correcciones), `derechos-fuentes.md`
  (parafraseo de hechos + cita/enlace + extracto breve + **proceso de retirada/takedown**),
  `terminos.md`. Todas con `<PLACEHOLDER>` y aviso destacado **"no es asesoría legal, adapta a tu
  jurisdicción"**. Enlazadas desde `starter/AGENTS.md` y el README raíz. Cubre el hueco legal que
  ChatGPT y Gemini pusieron en su top-5. Sin cambios de código → tests siguen 21/21.
- **2026-08-11 · Despliegue host-agnóstico + persistencia de ediciones.** (a) `04-DESPLIEGUE.md`:
  el output es estático y portable; recomendado Cloudflare, con Netlify/GitHub Pages/Vercel y el
  aviso de uso comercial (que —corrección tras verificar— afecta a **Vercel Hobby Y GitHub Pages**,
  no solo Vercel). Host+monetización van al cuestionario y el agente verifica ToS al construir.
  (b) **Persistencia**: `publish.py` guarda cada edición publicada en `data/editions/<slug>.json`
  (versionado, "Git como BD") y reconstruye el sitio entero desde ahí → archivo/RSS/sitemap
  **acumulan** el histórico (cierra el crítico "no se acumula" de ChatGPT). Persiste solo en
  `--production` no bloqueado; el preview no toca el almacén. **Tests 23/23** (+2 de persistencia).
- **2026-08-11 · CI + SEO.** (a) **`.github/workflows/publish.yml`**: publicación automática
  semanal (+ botón manual), `permissions` mínimos, `concurrency`. El compose con IA corre **una
  vez** en el CI (clave en Secrets); el host sirve el `site/` renderizado. Lógica por `risk_profile`:
  `auto`→commit/publica, `review`/`strict`→**abre PR** (peter-evans/create-pull-request), bloqueado→
  el job falla. Decisión de infra: `site/` y `data/editions/` **se versionan** (quitado `/site/` del
  `.gitignore`) para no re-ejecutar la IA en el host. (b) **SEO**: `lib/site.py` añade JSON-LD
  `NewsArticle` (autoría declarada), Open Graph y `<lastmod>` por URL en el sitemap; `<` escapado
  en el JSON-LD (anti-ruptura de `<script>`). **Tests 24/24.** Cierra los hallazgos SEO de ambas
  reviews (faltaban JSON-LD/OG/lastmod).
- **2026-08-11 · Newsletter (doble opt-in + baja HMAC).** `scripts/newsletter.py`: tokens
  firmados (HMAC-SHA256, `payload="action:email:exp"`, base64url) con `make_token`/`verify_token`
  — email en el token (no `?email=` manipulable), acción tipada (confirm≠unsubscribe), caducidad,
  comparación en tiempo constante. Cierra el alto de ambas reviews (baja firmada, anti
  *subscription bombing*). Form del sitio cableado a `POST /api/subscribe` (antes `onsubmit=
  return false`). `newsletter/README.md` documenta el flujo de 3 endpoints, las env
  (`RESEND_API_KEY`/`RESEND_AUDIENCE_ID`/`NEWSLETTER_SECRET`), un handler de referencia y el
  deploy por host. **Tests 29/29** (+5). Pendiente: el envío real por Resend (capa de host).
- **2026-08-11 · Asistente CLI + preview + onboarding incremental + ejemplo.** Decisión de
  producto: el "admin" es un **asistente ligero**, no un panel web (mantiene barato/portable).
  (a) `scripts/setup.py`: wizard interactivo que escribe `config.json`/`.env`/`master-prompt.md`
  (con `NEWSLETTER_SECRET` autogenerado); lógica pura (`build_config`/`render_master_prompt`)
  testeada; `validate_config` ahora expone `validate_dict`. (b) `scripts/serve.py`: construye el
  preview y lo sirve en local (un comando). (c) **Onboarding por niveles** (0→6): nada bloquea —
  sin dominio/feeds/clave se avanza igual (subdominio/fixtures/stub); plasmado en `00-QUICKSTART`
  y en `starter/AGENTS.md` (instrucción explícita al agente de no bloquear). (d) **Ejemplo
  trabajado** `examples/movilidad-mx-es/` (config + master-prompt rellenos), corre con fixtures →
  "Radar Movilidad". **Tests 33/33** (+4). Cierra el punto B del roadmap.
- **2026-08-11 · Catálogo de settings descubrible.** Idea del usuario: poder decir "muéstrame
  los settings" y que la IA sepa enseñar TODO lo configurable. `scripts/settings.py` = fuente única
  de verdad (~30 opciones) con categoría, `scope` (**dónde se toca**: config/.env/workflow/host),
  nivel, tipo, default/opciones y descripción; el comando `settings [tema]` filtra y muestra el
  **valor actual** si hay `config.json`. Gancho explícito en `AGENTS.md` (raíz y starter) para que
  el agente lo use ante "qué puedo configurar / cambia el huso horario / el modelo…". Añadido
  `site.timezone` al schema. **Tests 37/37** (+4).
- **2026-08-11 · Docs de guía completos + costes precisos.** Escritos los 6 docs que faltaban:
  `05-CUESTIONARIO` (preguntas + remite a `setup`/`settings`), `06-ADAPTACION-TEMATICA` (playbooks
  por tipo de tema + cómo encontrar feeds), `07-GUARDARRAILES` (lo impuesto por código vs política
  editorial + perfiles), `08-MODO-INDEPENDIENTE` (monetización honesta + landmine de host),
  `10-SEO` (lo que el kit ya hace + mass-gen OFF + buenas prácticas), `12-TROUBLESHOOTING`
  (problemas comunes, con foco en "bloqueo = correcto"). `03-COSTES` gana la **fórmula
  reproducible** (tokens×precio), el aviso del precio introductorio de Sonnet y el escalón de
  Resend. 0 enlaces rotos. **Residuales** (dedupe fino, cooling-window horaria) documentados como
  baja prioridad (knob ya existe / requiere timestamps con hora) — no se mete código arriesgado.
- **2026-08-11 · Bilingüe ES + EN (dos capas).** **Capa 1 (medio):** `scripts/lib/i18n.py` con
  textos del "chrome" (nav, footer, caja de newsletter, archivo, kicker) en `es`/`en`; `templating`
  y `site` tiran de `t(lang, key)` según `site.language` — un medio en inglés se ve **entero** en
  inglés; idioma desconocido → inglés (default internacional). El español sigue idéntico.
  `tests/test_i18n.py` lo fija. **Capa 2 (docs):** carpeta `en/` con **README + guías 00-12
  traducidas** al inglés (vía 12 subagentes en paralelo, con glosario y reglas de enlaces
  compartidas); código, comandos, placeholders y enlaces preservados (los internos a `starter/`
  con `../`). Selector de idioma ES↔EN en ambos README. **Verificado: 0 enlaces rotos en todo el
  repo, spot-checks OK. Tests 41/41.**
- **2026-08-11 · Revisión externa #3 (ChatGPT) — dura y en gran parte correcta.** Revela una capa
  nueva (operabilidad + máquina de estados de publicación). Confirmados en código: C-01 (no había
  transición aprobado→indexable; D1 sin implementar), C-02 (setup conserva taxonomía de fixtures),
  C-03 (formulario de newsletter a un endpoint inexistente), C-04 (procedencia posicional, no
  semántica), A-01 (SSRF: lectura de fichero local desde `sources`), A-02 (config no validado en
  runtime), M-01 (enums de tema falsos), M-05 (doctor 3.8 / `VERCEL_DEPLOY_HOOK`). Decisión del
  usuario: **Track A (honesto y seguro)**. Nota: M-04 (bilingüe) ya estaba resuelto en el turno
  anterior, posterior a ese ZIP.
- **2026-08-11 · Track A · Lote 1 (estado + seguridad + gobernanza).** (a) **Máquina de estados de
  publicación** (C-01): `scripts/editorial_gate.py` (quality-gate D1: no-stub + QA ok + suficientes
  historias + todas con fuente); cada edición lleva `status` (needs_review/approved) y
  `quality_report`; solo `auto` + gate OK → `approved`; `publish` indexa **por edición según su
  status**; **sitemap solo con approved**; `scripts/approve.py` (paso humano review/strict → approved
  → reconstruye indexable); **stub como INVARIANTE** (siempre bloquea producción, ya no configurable).
  (b) **Seguridad SSRF** (A-01): `ingest` ya no lee ficheros locales desde `sources` (solo con
  `allow_local`, fixtures) y bloquea hosts privados/loopback. (c) **Gobernanza de config** (A-02): el
  pipeline **valida el config en runtime** (`validate_dict`, exit 2 si inválido), `jsonschema`
  pinneado, `additionalProperties:false` en la raíz, bloques `newsletter`/`meta` en el schema.
  (d) **Newsletter condicional** (C-03): el formulario solo se renderiza con `newsletter.enabled`
  (adiós form roto a 404). (e) **Quick-wins**: enums de tema derivados del CSS real (M-01), `doctor`
  a Python 3.11 + `DEPLOY_HOOK` (M-05). **Tests 46/46** (+ gate, needs_review noindex/sitemap, etc.).
- **2026-08-11 · Track A · Lote 2 (C-02 + A-03 + A-06).** (a) **C-02 taxonomía real**: `setup`
  ya NO copia los fixtures — `build_config` usa defaults neutros y construye la taxonomía desde
  las respuestas (temas/mercados/actores); marca `meta.origin` y `meta.needs_taxonomy`; el
  pipeline **bloquea producción** si la taxonomía es placeholder (`taxonomy-placeholder`).
  Verificado: un medio "quantum/Japan" NO conserva regulación/México. Fix colateral: `as_of` se
  fija siempre (antes crasheaba con config sin `as_of`). (b) **A-03 spec coherente**: nuevo
  `docs/ARCHITECTURE.md` (corto, exacto, la fuente de verdad); el `BLUEPRINT` marcado como
  **histórico/no ejecutable**; `AGENTS.md` (raíz y starter) apuntan a ARCHITECTURE, no al blueprint.
  (c) **A-06 operabilidad**: `compose` registra la **causa** del fallback (`_compose_error`, no lo
  oculta); el pipeline escribe `data/operations/latest.json` (+ histórico en producción) con estado,
  quality, gate_reasons y feeds. **Tests 47/47**, 0 enlaces rotos.
- **2026-08-11 · Track A · A-07 (legal real).** `scripts/legal.py`: convierte las plantillas
  `legal/*.md` (rellenadas) a `site/legal/*.html` con el theme; `pending()` detecta placeholders
  sin rellenar. El **footer** ahora respeta `editorial.ai_disclosure` (declara o no la IA) y
  **enlaza** las páginas legales. El pipeline **bloquea producción** si quedan placeholders legales
  (`legal-placeholders`) — un medio público no sale sin su legal. **Tests 51/51.**
- **2026-08-11 · Track A · A-04 (repo-root) → TRACK A COMPLETO.** `pack.py` genera el **template
  compartible** con el contenido de `starter/` en la **raíz** (el workflow queda en
  `.github/workflows/` de la raíz, que es donde GitHub lo reconoce); las guías `00`-`12` +
  `ARCHITECTURE`/`HOWTO`/`README` a nivel raíz; `en/` incluido; y **fuera** los docs de mantenedor
  (`PROGRESO`, `REVISION-EXTERNA`, `KIT-v2`) y lo generado (`site/`, logs). Reescribe los enlaces
  según la profundidad y neutraliza los que apuntaban a docs excluidos. **Workflow endurecido**:
  `timeout-minutes`, tests+validación **antes** de gastar en el modelo, subida del reporte como
  artefacto, y avisos (permiso de PR del `GITHUB_TOKEN`, cron se desactiva a los 60 días).
  **Verificado en el build: 51/51 tests dentro del template, 0 enlaces rotos, workflow en la raíz.**
- **2026-08-11 · Track B · A-05 (riesgo por artículo) + evidencia.** `scripts/risk.py`: etiqueta
  cada historia (allegation/health/financial/politics/violence/minor/rumor, ES+EN, determinista).
  QA añade el check **bloqueante `sensitive_support`** (en TODOS los perfiles): una **acusación**
  no se publica sin **atribución** ("según…") **y ≥2 fuentes independientes** — así un medio en
  `review`/`auto` tampoco cuela una acusación sin respaldo (el caso exacto de la review #3).
  **Evidencia enriquecida**: los duplicados fusionados ahora guardan su `summary`, que entra en la
  evidencia que valida QA. **Tests 55/55.** Residuo honesto: la verificación *semántica* completa
  (afirmación↔evidencia) queda como fase dedicada (C-04).
