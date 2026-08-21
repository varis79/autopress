# Changelog

Todas las versiones publicables de Autopress. Formato basado en
[Keep a Changelog](https://keepachangelog.com/es/1.1.0/) y versionado
[SemVer](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

- **MAJOR** — cambios que rompen configs/flujos existentes.
- **MINOR** — funcionalidad nueva compatible hacia atrás.
- **PATCH** — arreglos y retoques sin cambio de contrato.

> **English:** this changelog is maintained in Spanish; entries are short and
> technical. The kit itself is fully bilingual (ES/EN).

## [Unreleased]
Objetivo **0.7.0** — Núcleo LLM fiable, endpoint público seguro y medio más
descubrible. Release combinada (hardening + SEO/E-E-A-T). Sin cambios que rompan
configs de v0.6; los operadores actualizan con `scripts/update.py`. Alcance en
`docs/ROADMAP-v0.7.md`; decisión de Path B en `docs/adr/0001-path-b-aplazado.md`.

### Añadido
- **`doctor --smoke`** (opt-in, requiere `ANTHROPIC_API_KEY`): ejecuta UNA llamada
  real de `compose` sobre un fixture de 1 historia y verifica `stub=False`, JSON
  parseado y `stop_reason`; primera verificación reproducible del camino LLM en vivo.
- **Páginas E-E-A-T** generadas del `config`: `/acerca`, `/metodologia`, `/fuentes`,
  con **byline** en el masthead. Formalizan el alcance honesto como señal de confianza.
- **`robots.txt`** generado por `publish` (producción con `Sitemap:`; preview `Disallow: /`).
- **`<title>` con el titular** de portada y `<meta description>` por página (antes: nombre·fecha).
- **"La semana en N puntos"** (lead escaneable) y badge **"N fuentes lo cubren"**,
  ambos deterministas (0 llamadas LLM extra).
- **Anti-bot del boletín en 4 capas** (`/api/subscribe`): gate de origen, honeypot,
  rate-limit por IP (KV) y verificación server-side de Turnstile.
- **`doctor --feeds`**: expone el diagnóstico de fuentes vivas/muertas que ya calculaba `ingest`.
- **Descubribilidad (Lote G, backport determinista)**: navegación **prev/next**
  entre ediciones; **twitter cards** + **`og:image` estática** que aporta el operador
  (`site.og_image`); **`og:locale`** derivado del idioma; **JSON-LD enriquecido**
  (inLanguage, publisher/logo, author, `sameAs` opt-in, BreadcrumbList). Todo
  determinista, opt-in y sin dependencias nuevas. Detalle en `docs/ROADMAP-v0.7.md`.
- **Aviso de modelo RETIRADO** (`scripts/lib/models.py`): el aviso distingue ahora
  *retirado* (el ID ya no existe → 404 → edición en stub) de *heredado* (funciona,
  pero hay algo más nuevo). El nivel no se escribe a mano: se deduce comparando la
  fecha de retirada anunciada con la de hoy, así un modelo con fecha futura pasa solo
  a "retirado" el día que toca aunque el operador lleve meses sin actualizar. Lista
  ampliada con la familia Claude 4 (incluido `claude-opus-4-1-20250805`, retirado el
  2026-08-05) y con las fechas de los Claude 3 ya retirados.

### Cambiado
- **`compose`**: presupuesto de `thinking` explícito y separado del de salida; una
  respuesta truncada (`stop_reason=max_tokens`) se registra como causa `truncated`
  en vez de degradar a stub sin diagnóstico. Default de `compose.max_tokens`
  unificado a **8000** en settings/setup/schema/costes, con aviso de que en Sonnet 5
  ese tope incluye el razonamiento. Un **404** del proveedor (modelo inexistente o
  retirado) se registra como causa **`model-not-found`** en vez del críptico
  `NotFoundError`, y `doctor --smoke` explica que el arreglo es editar `compose.model`,
  no reintentar. Al no depender de ninguna lista, cubre también los modelos que se
  retiren después de esta versión del kit.
- **Guardarraíles**: el check anti-cifras cubre también números de un dígito; la
  atribución de acusaciones exige nombrar una fuente distinta de la propia acusación.
- **i18n del correo** del boletín (confirmación/baja) por idioma del medio.
- **Docs**: `07-GUARDARRAILES` aclara que `auto` no auto-indexa sin
  `allow_auto_index`; se retira "Use this template"; se explicita que el envío del
  boletín es manual hoy; el aviso de privacidad documenta el email en el token.

### Arreglado
- **`pack.py`** reescribe también los `.py` (no solo `.md`): 0 `cd starter` en el
  template (aserción añadida al CI de release).
- **`doctor`** valida el `config.json` del operador (antes solo `fixtures/`).
- **`update.py`** valida las rutas del ZIP antes de extraer (anti zip-slip).
- **`assemble()`** descarta historias con titular/resumen vacíos y recae a stub si
  no queda contenido útil.
- **Re-suscripción del boletín**: `confirm.js` hace `PATCH` en un `409` de Resend
  (POST no actualiza un contacto existente), así quien se dio de baja y vuelve queda
  `unsubscribed:false` de verdad. (Detectado al cruzar la auditoría del medio hermano.)
- Ejemplos y happy-path coherentes (`config.json`, `serve`/`--config`), aviso si
  falta `anthropic` con clave presente, y varias correcciones de coherencia de docs.

## [0.6.0] — 2026-08-12
Autoservicio y auto-actualización. Onboarding pensado para que baste con enviar
la URL del repo.

### Añadido
- **Auto-actualización** `scripts/update.py`: descarga la última Release y
  **sobrescribe solo el motor** (scripts, tests, esquema, functions, AGENTS) con
  **copia de seguridad** previa; **nunca toca** `config.json`, `.env`, `data/`,
  `site/`, `prompts/`, `legal/` ni `examples/`. Flags `--check`, `--docs`,
  `--yes`. Solo stdlib. Upstream configurable con `AUTOPRESS_UPSTREAM`.
- **Aviso de modelo heredado** en `doctor` (no bloqueante): `scripts/lib/models.py`
  mapea IDs superados → reemplazo sugerido; se actualiza con el kit.
- **`VERSION` incluido en el paquete** para que `update` sepa qué versión hay.

### Cambiado
- **README (ES/EN) — hero "Empieza en 3 pasos"**: Paso 0 lidera con la opción
  **sin terminal** (app de doble clic), descarga correcta desde Releases (aviso de
  no usar "Code → Download ZIP") y prompt de inicio en caja copiable.

## [0.5.0] — 2026-08-12
Primera versión pública **beta**. El motor y los guardarraíles están maduros;
falta la fase "medio de verdad" (leer el artículo completo + evidencia por
afirmación) y el endpoint real de newsletter. Apta para pruebas de operadores.

### Añadido
- **Kit completo bilingüe (ES/EN)** en un solo paquete: medio generado, docs,
  legales y guía. Onboarding con un prompt mínimo de 3 líneas → el agente lee
  `AGENTS.md` y lleva al operador de la mano (empezando por una bienvenida).
- **Pipeline determinista** (stdlib + `feedparser` + `anthropic`): ingest →
  clasificar → deduplicar → seleccionar → redactar (1 llamada LLM/edición) →
  QA → puerta editorial → publicar. "Git como base de datos"; sitio estático.
- **Publicación review-first**: por defecto nada se indexa sin aprobación
  humana; `auto` **no** auto-indexa salvo opt-in explícito.
- **Guardarraíles en código**: no inventar cifras, citas por `ref_id` (no puede
  inventar fuentes), acusaciones atribuidas + doble fuente en `strict`,
  anti-inyección, `safe_url`, `noindex` por defecto, hardening SSRF.
- **Newsletter llave en mano** (opcional): funciones serverless (Cloudflare
  Pages) con doble opt-in y baja firmados por HMAC.
- **CI**: tests + validación de esquema antes de tocar el modelo; workflow de
  release que empaqueta el ZIP al taggear.
- **Legales autorellenables**, `setup` interactivo, `settings`/`doctor`,
  atribución de footer desmarcable.

### Notas
- Se redacta desde los **resúmenes de RSS**, no del artículo completo: es un
  *digest* con criterio que parafrasea y cita; no verifica el sentido de cada
  dato. El operador sigue siendo editor y responsable legal.
- El coste en API es de céntimos por edición (una sola llamada de redacción).

[Unreleased]: https://github.com/varis79/autopress/compare/v0.6.0...HEAD
[0.6.0]: https://github.com/varis79/autopress/releases/tag/v0.6.0
[0.5.0]: https://github.com/varis79/autopress/releases/tag/v0.5.0
