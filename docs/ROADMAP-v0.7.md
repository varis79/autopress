# ROADMAP v0.7 — "Núcleo fiable, endpoint seguro, medio descubrible"

> Alcance de la v0.7 (release **combinada**: hardening + SEO/E-E-A-T). Deriva de la
> auditoría por dimensiones (8 finders + verificación adversarial) y de la ideación
> de producto. Decisión de Path B en `docs/adr/0001-path-b-aplazado.md`.

## Tema
Cerrar los huecos de **fiabilidad del núcleo LLM** (`compose`) y de **seguridad
del endpoint público** (newsletter), sanear la **coherencia docs↔código**, y dar
al medio del operador **superficie E-E-A-T + higiene SEO on-page**. **Path B se
aplaza entero a v0.8.**

SemVer: **MINOR (0.7.0)**. No rompe `config.json` de v0.6. `doctor --smoke` es
opt-in; el default de `max_tokens` se unifica a 8000 (los configs que ya fijan un
valor no cambian). Los operadores en v0.6 reciben v0.7 vía `scripts/update.py`.

## Entra (por lotes)

### Lote A — Fiabilidad del compose (el hueco nº1)
- **A1** `compose.py:164,177` — Fijar `thinking` explícito (o desactivarlo)
  separando su presupuesto del de salida; detectar `resp.stop_reason=="max_tokens"`
  y registrar causa `"truncated"` en `_compose_error` en vez de un `JSONDecodeError`
  genérico. *(rank 1, high, S/M)*
- **A2** `settings.py:56`, `setup.py`, `autopress.schema.json:166`, `03-COSTES.md:40`
  (ES+EN) — Unificar default `max_tokens=8000` y documentar que en Sonnet 5 ese tope
  **incluye el thinking**; advertir de no bajarlo. *(rank 5, S)*
- **A3** `doctor.py` — `python3 -m scripts.doctor --smoke` opt-in (requiere clave):
  1 llamada real sobre un fixture de 1 historia; asserta `stub==False` + JSON parseado;
  muestra `stop_reason` + `usage`. Aislado; no toca el pipeline determinista.
  Cubre de paso la validez del `model id`. *(rank 7, M)*
- **A4** `compose.py:124` — Descartar en `assemble()` historias con `headline`/`summary`
  vacíos; recaer a stub si tras el filtrado no queda contenido. *(rank 24, S)*

### Lote B — Seguridad del endpoint público
- **B1** `functions/api/subscribe.js:6` — Verificar Turnstile server-side (POST a
  `challenges.cloudflare.com/turnstile/v0/siteverify`) antes de enviar + rate-limit
  por IP (KV de Cloudflare). Corregir el claim "anti subscription bombing" de
  `newsletter.py:6`. *(rank 2, high, M)*
- **B2** `update.py:201` — Validar cada `ZipInfo.filename` (rechazar rutas absolutas
  y `..`) antes de `extractall` (anti zip-slip en la feature estrella de v0.6). *(rank 15, S)*
- **B3** DOC — Documentar en `legal/privacidad.md` (ES+EN) que el token del boletín
  lleva el email en base64 firmado (no cifrado) → puede quedar en logs del host.
  El cifrado real del payload se aplaza a v0.8. *(rank 14, S — solo documentar)*

### Lote C — Credibilidad / guardarraíles
- **C1** `lib/text.py:72` / `qa.py` — Bajar `min_len` a 1 (o comprobar dígitos
  sueltos) en `numbers_supported`; alinear `07-GUARDARRAILES.md:10` con la garantía
  real. Cierra la fuga de cifras de un dígito ("2→9 muertos"). *(rank 3, S)*
- **C2** `risk.py:44` — Romper la atribución circular: exigir que la atribución
  nombre una fuente (`según/according to/fuentes`+entidad) distinta de las palabras
  de la propia acusación. *(rank 9, S)*
- **C3** `07-GUARDARRAILES.md:20` — Corregir "auto = publica solo" →
  "auto = publica solo SOLO si activas `publishing.allow_auto_index`; por defecto
  pasa por revisión". *(rank 6, S)*

### Lote D — Empaquetado / tooling del mantenedor
- **D1** `pack.py:102` — Extender `_rewrite_commands` a `.py` (docstrings/comentarios)
  y añadir aserción CI `grep -c "cd starter" == 0` sobre el template. *(rank 4, S)*
- **D2** `doctor.py:42` — `check_config`/`check_golden` validan el `config.json` del
  operador si existe (no solo `fixtures/`). Unificar docstring a
  `PYTHONPATH=. python3 -m scripts.doctor`. *(ranks 8, 17, S)*
- **D3** `release.yml:30` — Nombre del step sin literal "65+" → "Tests del starter". *(rank 19, S)*

### Lote E — UX del no-técnico (fricciones del cold test)
- **E1** Ejemplos con `config.json` (no `mi-config.json`); happy-path con
  `scripts.serve` o `--config config.json` explícito. *(rank 11, S)*
- **E2** Recordar reactivar el venv por sesión, o que `pipeline`/`doctor` avisen si
  falta `anthropic` cuando hay clave (hoy cae a stub en silencio). *(rank 12, S)*
- **E3** Eliminar "Use this template" de `EMPIEZA-AQUI.md:19` y `00-QUICKSTART.md:48`. *(rank 13, S)*
- **E4** i18n del correo de confirmación y respuestas `confirm/unsubscribe` por idioma. *(rank 10, S)*
- **E5** Doc-pulido honesto: alinear promesa "sin terminal" README↔QUICKSTART (rank 26),
  quitar el "teaser" inexistente de `03-COSTES` (rank 18), separador decimal ES (rank 21),
  dejar EXPLÍCITO que el envío del boletín es **manual** hoy (rank 22-parcial). *(S)*
- **E6** "Feed doctor": exponer los `diagnostics` de fuentes vivas/muertas que
  `ingest.py` YA calcula (subcomando `doctor --feeds`). *(vision NOW, S)*

### Lote F — SEO on-page + señales de curación (producto)
- **F1** `site.py:85,164` — `<title>` = `{cover.headline} · {site.name}` (~60c) y
  `<meta description>` por página desde el deck (~155c), distintos para home/archivo/edición. *(vision, S, score 90)*
- **F2** `site.py` — `render_robots()` + escritura en `publish.py`: producción con
  `Sitemap:`; preview con `Disallow: /`. *(vision, S, score 84)*
- **F3 (FARO)** Páginas **E-E-A-T deterministas** desde `config`: `/acerca`,
  `/metodologia`, `/fuentes` + **byline visible** en el masthead que enlaza a
  `/metodologia`. Formaliza el "alcance honesto" como señal pública de confianza.
  Subsume "cómo hacemos esto" y "ficha de fuentes". *(vision FLAGSHIP, M, score 86)*
- **F4** `templating.py` — "La semana en N puntos": `<ul class="tldr">` construido
  deterministamente desde los headlines ya compuestos (0 llamadas extra). *(vision, S, score 80)*
- **F5** `templating.py` — Badge "N fuentes lo cubren" leyendo `merged`/`sources`
  (0 API): hace visible el dedupe como señal de corroboración. *(vision, S, score 74)*

### Lote G — Backport de descubribilidad (quick wins deterministas, 0-riesgo)
> Generalización genérica y config-driven de capacidades del medio de referencia
> (reimplementadas desde cero; nada de ningún vertical). Todo determinista, **0
> llamadas LLM**, 0 dependencias nuevas. Se pliega sobre la misma pasada de `<head>`
> que F1/F2/F3 (se edita `site.py` `_og()`/head UNA sola vez).
- **G1** `publish.py`, `site.py`, `i18n.py` — **Nav prev/next entre ediciones**
  (backport #2 Fase A). Vecinos por fecha desde el store ya ordenado; `render_edition_page`
  gana `prev_ed`/`next_ed`, pinta `<nav>` con `rel=prev/next` + `<link rel=prev/next>`
  en head. URLs relativas `/magazines/<slug>.html`. Claves i18n es/en. **No depende
  de hubs.** *(M)*
- **G2** `site.py:27` + nuevo `scripts/lib/palettes.py` — **twitter:card + og:image
  estática** (backport #5 Fase A). `twitter:card/title/description` SIEMPRE (mejora el
  preview solo-texto). `site.og_image.path` raster del operador → `og:image` con URL
  absoluta saneada por `safe_url`. **Rechazar `.svg`** como og:image (los sociales lo
  ignoran; sería una promesa falsa). `palettes.py` = fuente única de color (mata la
  duplicación `theme.css`/`render_demo`). La tarjeta PNG auto-por-edición → v0.8. *(M)*
- **G3** `site.py:27`, `i18n.py` — **og:locale** (backport #6 Capa 1). `_og_locale(site)`:
  override `site.locale` o derivación honesta de `site.language` (`es-ES`→`es_ES`; `es`→`es`,
  sin inventar región). **Fusiona con F1** (misma línea de head). *(S)*
- **G4** `site.py:32-48` — **JSON-LD aditivo** (backport #4 parte barata). Enriquecer
  `_jsonld_edition`: `inLanguage`, `publisher.url`+`logo` (si `site.logo` http/https),
  `author.url`, `sameAs` **opt-in** solo si `config.site.same_as` valida http/https;
  `_jsonld_breadcrumb` como 2º `<script>`. **No cambiar los separators de `json.dumps`**.
  El `@graph` consolidado → v0.8. *(S)*

### Config nuevo del Lote G (opt-in, backward-compat)
- `site.og_image = {mode: off|static, path}` (default `off`).
- `site.locale` (xx_YY, opcional; si falta se deriva de `site.language`).
- `site.same_as` (array de URIs propias verificadas; solo si validan http/https).
- `site.logo` (URI/ruta opcional; comparte asset con og:image, sin Pillow).

## No entra (y por qué)
> El resto del backport (hubs, newsletter determinista, 2ª ola SEO) se detalla en
> `docs/ROADMAP-v0.8.md` (Lotes H/I/J).
- **Path B completo** (fetch del cuerpo + evidencia por afirmación + reputación de
  fuente + gate de originalidad + relajar `allow_auto_index`) → **v0.8+**. No existe
  hoy; el verificador refutó/degradó todos sus hallazgos. Meter el fetch del cuerpo
  SIN el check por-afirmación **debilita** la garantía anti-cifras justo cuando se
  usaría para justificar auto-index → rompe los principios 1 (alcance honesto) y 4
  (review-first). Ver ADR 0001.
- **Cifrado real del token de boletín** (AES-GCM / id opaco) → v0.8. En v0.7 solo se
  documenta la fuga (B3). El HMAC ya impide altas/bajas de terceros; severidad low.
- **Envío automático de la edición** a Resend Broadcasts → v0.8 (L, superficie nueva).
  En v0.7 se aclara en la doc que el envío es manual.
- **Hubs por tema persistentes** (programmatic SEO) → v0.8, en UNA implementación con
  gate anti-thin. Rozar la prohibición de "contenido a escala" con prisa junto a la
  auditoría es arriesgado; merece su propia release.
- **Recetas por vertical, descubridor de feeds, panel de revisión local, controles
  editoriales, "por qué importa", newsletter HTML determinista** → v0.8 (alto valor,
  pero superficie nueva; v0.7 sube la barra antes de ampliar).
- **Ingesta paralela, SSRF pinning anti-rebinding, Windows, `_extract_json` con llaves
  balanceadas, `env:` para `GITHUB_REF_NAME`** → pasada de seguridad/escala v0.8
  (OVERSTATED/PLAUSIBLE, condiciones acotadas).

## Criterio de "terminado" (cada lote)
`cd starter && PYTHONPATH=. python3 -m unittest discover tests` en verde ·
`python3 -m scripts.doctor` OK · `python3 pack.py <tmp>` sin enlaces rotos y con
`grep -c "cd starter"` == 0 dentro del ZIP · tests nuevos por cada fix con lógica.

## Fortalezas que NO se tocan
Procedencia blindada en `assemble()` · invariante "stub nunca en producción"
(4 guardas) · review-first por defecto · doble opt-in HMAC (paridad JS↔Python) ·
higiene XSS centralizada · capa anti-SSRF reutilizable · input al LLM acotado por
diseño (no crece con nº de fuentes).

## Origen
Auditoría multiagente 2026-08-12/13 (18 agentes, verificación adversarial). El
detalle de los 32 hallazgos y su verificación vive en la bitácora `PROGRESO.md`.
