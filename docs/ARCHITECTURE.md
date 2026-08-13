# ARCHITECTURE — cómo está construido Autopress (fuente de verdad)

> 🌐 **English:** [en/ARCHITECTURE.md](../en/ARCHITECTURE.md)

> Descripción **corta y exacta de lo que existe hoy** en `starter/`. Esto manda sobre el
> `BLUEPRINT-MEDIO-AUTONOMO.md` (que es material histórico, no ejecutable). Si algo del
> blueprint contradice esto o a las decisiones D1-D4, **gana esto**.

## Qué es

Un pipeline en Python (stdlib + `feedparser` + `anthropic`) que convierte feeds RSS en una
edición semanal, la controla y la publica como **sitio estático**. Sin base de datos: el
estado vive en Git (`data/editions/`).

> **Alcance honesto (impórtalo al construir):** la IA redacta a partir del **título y el
> resumen del RSS**, NO del artículo completo — es un *digest* que parafrasea y cita, no un
> sistema que "lee" y verifica el sentido de cada afirmación. Por eso la **indexación
> automática está DESACTIVADA por defecto** (`publishing.allow_auto_index=false`): todo pasa
> por **revisión humana** (`review` → `approve.py`) hasta que exista un gate de originalidad
> real. No prometas al operador "verificación de hechos"; promete "curación con cita y
> guardarraíles".

## Pipeline (etapa → fichero)

```
ingest → classify → dedupe → select → compose → qa → editorial_gate → publish
```
- `scripts/ingest.py` — descarga feeds (timeout/UA/reintentos), anti-SSRF (sin ficheros
  locales ni hosts privados), diagnóstico por fuente.
- `scripts/classify.py`, `dedupe.py`, `select_stories.py`, `pipeline_core.py` — núcleo
  determinista (clasificación, dedupe con memoria, selección con scoring/cuotas/modo).
- `scripts/compose.py` — redacción con LLM (procedencia por `ref_id`, anti-inyección);
  `compose_stub.py` es el fallback sin clave.
- `scripts/qa.py` — QA por niveles (blocking/review_required/warning); en `strict`, exige
  fuentes independientes.
- `scripts/editorial_gate.py` — quality-gate D1: qué edición puede indexarse.
- `scripts/publish.py` — renderiza el sitio desde `data/editions/` (Git como BD).
- `scripts/pipeline.py` — orquesta todo; valida el config; imprime estado JSON.

## Config

- `config.json` (el del operador) validado contra `autopress.schema.json`
  (`additionalProperties:false`). **Config inválida = no se ejecuta** (exit 2).
- `fixtures/config.json` es SOLO para tests/demo. La taxonomía de producción la genera el
  operador (asistente `scripts/setup.py`); una config con `meta.needs_taxonomy` no publica.

## Máquina de estados (publicación e indexación)

Cada edición persistida lleva `status`:
- `needs_review` → **noindex**, fuera del sitemap (borrador).
- `approved` → indexable en producción.

Reglas:
- `risk_profile=auto` + quality-gate OK + no-stub → `approved`.
- `review`/`strict` → `needs_review`; un humano lo pasa a `approved` con `scripts/approve.py`.
- **stub nunca se publica en producción** (invariante). El **sitemap solo lista approved**.

## Guardarraíles (impuestos por código)

Cifras no respaldadas → bloqueo; procedencia por `ref_id` (no inventa fuentes); URLs solo
http/https; anti-inyección (escape de `<`/`>`); `noindex` por defecto. Detalle en
`../07-GUARDARRAILES.md`.

## Deploy

Salida estática en `site/`; el host la sirve (ver `../04-DESPLIEGUE.md`). CI semanal en
`.github/workflows/publish.yml` (auto→publica, review/strict→PR).

## Para el agente: qué editar y qué no

- **Edita**: `config.json`, `prompts/master-prompt.md`, `.env`, y las fuentes (`sources`).
- **No reescribas** la arquitectura del pipeline ni el esquema sin motivo. Extiende, no
  reinventes.
- **Comandos**: `python -m scripts.doctor` · `scripts.setup` · `scripts.serve` ·
  `scripts.pipeline [--config … --production]` · `scripts.approve <slug>` · `scripts.settings`.
- **Criterio de terminado**: `python -m unittest discover tests` en verde y `doctor` OK.
