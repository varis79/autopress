# ROADMAP v0.8 — "Núcleo descubrible: hubs, newsletter y acabado SEO"

> Deriva del backport de 7 capacidades (generalización genérica y config-driven del
> medio de referencia; nada de ningún vertical) sobre la base endurecida de v0.7.
> Path B sigue fuera (ver `docs/adr/0001-path-b-aplazado.md`). SemVer: **MINOR
> (0.8.0)**, no rompe `config.json` de v0.7 (todo lo nuevo es opt-in con defaults
> inertes). Se distribuye vía `scripts/update.py`.

## Tema
Ampliar superficie de descubrimiento y distribución **sin romper los principios**:
determinista en código (el LLM solo redacta, **0 llamadas nuevas**), review-first,
noindex-por-defecto, gate anti-thin duro, sin CDNs, salida estática a `site/`.

## Entra (por lotes)

### Lote H — Hubs / pillar pages con gate anti-thin (FARO) — backport #1
- **H0** Refactor `_load_store` (duplicado en `publish.py:37`/`retract.py`) a
  `scripts/lib/store.py`. Prerequisito de hubs (y de un futuro radar). *(S)*
- **H1** Nuevo bloque config **`hubs` OPT-IN** (`enabled=false` default, coherente
  con `10-SEO.md` "generación masiva OFF"). Registrar en `autopress.schema.json`
  (la raíz es `additionalProperties:false`). *(S)*
- **H2** `scripts/lib/hubs.py` `collect_hubs(all_eds, taxonomy, cfg)`: agrupa SOLO
  ediciones que pasarían `_indexable` por eje (empezar por `topics`), uniendo cada
  story a su slug/título de edición. `_slug_axis()` determinista ascii en `text.py`. *(M)*
- **H3** `render_hub_page` en `site.py` reusa `render_page` (shell/robots/canonical)
  y el patrón de tarjetas de `render_archive_page`. `_hub_indexable(group, min_stories)`
  = production AND ≥ `hubs.min_stories` historias DISTINTAS approved. *(M)*
- **H4** `publish.py`: emitir `hubs/<axis>/<slug>.html` (limpiando el dir antes,
  como `magazines/`); meter en sitemap **SOLO** los hubs indexables; convertir el
  kicker topic/market en `<a>` al hub **solo si indexa** (evita red de doorways).
  Reutilizar el badge F5 "N fuentes" en las tarjetas. *(M)*
- **H5** Enlazado **historia→hub** (backport #2 Fase B) dentro de este PR, compartiendo
  el slugify de H2. Sin hub existente → texto plano (nunca ancla rota). *(S)*

Config: `hubs.enabled` (bool, false) · `hubs.axes` (subset de topics/markets/players,
default `[topics]`) · `hubs.min_stories` (int≥2, default 3) · `hubs.intros`
(valor-de-eje → párrafo estático, **sin LLM**). `players` como eje exige antes
persistirlos en `compose.assemble` (hoy se descartan).

### Lote I — Newsletter HTML determinista — backport #3
- **I1** `scripts/lib/email.py` `edition_email(ed, config, lang)` puro: tablas
  `role=presentation`, CSS inline, sin `<script>`/`<link>`/`@media`/imágenes
  remotas (el `theme.css` NO es email-safe: 55 usos de `var()/@media`); mismo DICT
  de la edición (**0 LLM**, mismo contenido que el sitio); citas vía `safe_url`. *(M)*
- **I2** `publish.py` paso gateado (`newsletter.compose` AND `status=='approved'`
  AND `not stub`): escribe `site/newsletter/<slug>.html` + `<slug>.json` (manifest)
  y los suma a `result['files']`. *(S)*
- **I3** Costura provider-agnóstica: placeholder `{{unsubscribe_url}}` documentado
  para que cualquier proveedor lo sustituya por destinatario. **NO se implementa el
  broadcast** (item hermano posterior). *(S — doc)*
- **I5** **Baja de un clic estándar (RFC 8058)**: cabecera `List-Unsubscribe` +
  `List-Unsubscribe-Post` en el envío, y endpoint de baja que acepte `POST` además del
  `GET` firmado (evita que los escáneres de email pre-carguen el enlace `GET` y den de
  baja sin querer). Va con el envío automatizado. *(S — heredado de la auditoría del medio hermano)*
- **I4** i18n del correo (`email_subject`/`preheader`/`view_online`/`unsub`/`cta`,
  es+en), compartiendo claves con E4 de v0.7. *(S)*

Config: `newsletter.compose` (bool, false) · `newsletter.provider` (string
informativo, default 'resend', **sin secretos**) · `newsletter.subject` (override).

### Lote J — Segunda ola SEO — backport #4 (@graph), #5 Fase B, #6 Capa 2
- **J1** `@graph` consolidado: un único `<script>` con `@id` cross-ref
  (Organization/WebSite/NewsArticle con `publisher`/`author` @id + `mainEntity`
  ItemList + BreadcrumbList; archive como CollectionPage). Enchufa el **author
  Person** del byline de F3 (v0.7) y el logo compartido. *(M)*
- **J2** **og:image PNG auto por edición** (Pillow **OPCIONAL**): `site.og_image.mode='auto'`
  genera tarjeta determinista en `assets/og/<slug>.png` (colores de `palettes.py`,
  **sin LLM**). DEGRADACIÓN: sin Pillow → cae a estática o sin-imagen, `doctor`
  avisa; **nunca** a SVG. Pillow declarado en un extra, no en el core. *(M)*
- **J3** **hreflang opt-in** (`site.alternates`): `<link rel=alternate hreflang>`
  SOLO en home/archivo indexables y con sitios hermanos declarados; **nunca** en
  permalinks de edición (no hay 1:1). x-default configurable. Suavizar de paso la
  copy sobrevendida de `web-page-copy.md:249`. *(S)*
- **J4** `news-sitemap` + feed RSS/JSON, reutilizando la lista de `_indexable` y el
  `image` de NewsArticle del @graph. 0 URLs noindex en feeds/sitemap. *(M)*

## No entra (y por qué)
- **Envío automático del boletín** a proveedor (broadcast) → item hermano de I,
  posterior. v0.8 solo deja la costura (HTML+manifest+placeholder).
- **Radar de temas emergentes (backport #7)** → v0.8+/explorar. Precondición dura:
  ~8-12 ediciones de historial (sin él, la señal es ruido) y `players` persistidos
  en `compose.assemble`. En v0.8 solo aterriza H0 (`lib/store.py`) que lo habilita.
- **Cifrado real del token de boletín** → según severidad; el HMAC ya basta hoy.

## Criterio de "terminado"
Suite verde dentro del ZIP de `pack.py` · `doctor` OK · `grep -c "cd starter"` == 0 ·
`hubs.enabled=false`/`newsletter.compose=false`/`og_image.mode=off` → template y
demo intactos (backward-compat) · 0 dependencias en el core (Pillow es extra opt-in) ·
0 llamadas LLM nuevas.

## Decisiones abiertas (a fijar al abrir v0.8)
- **Ejes iniciales de hubs** (solo `topics`, o también `markets`/`players`) y
  `hubs.min_stories` default (propuesto 3). `players` exige persistirlos antes.
- **`dateModified`**: mantenerlo == `datePublished` (honesto) o sellar
  `edition['updated']` en publish/approve para un valor real.
- **`newsletter.compose`** como flag separado de `newsletter.enabled` (recomendado,
  para no generar ficheros sorpresa).
- **Contrato `site.og_image`** (`mode: off|static|auto`, `path`) y si el logo del
  JSON-LD comparte asset con la og:image.
