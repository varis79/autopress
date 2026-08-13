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

[Unreleased]: https://github.com/varis79/autopress/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/varis79/autopress/releases/tag/v0.5.0
