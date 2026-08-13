# CLAUDE.md — Autopress (repo mantenedor)

Este es el **repo fuente/mantenedor** de Autopress, un **kit** que un no-técnico usa
—con un agente de IA— para montar su propio medio de curación de noticias. Este
fichero es para quien **desarrolla el kit**. El fichero para el **operador** (quien
lo usa) es `starter/AGENTS.md`; no los confundas.

## Estructura
- `starter/` — ⭐ el kit ejecutable (`scripts/`, `tests/`, `functions/`, `legal/`,
  `autopress.schema.json`, `AGENTS.md`…). `pack.py` lo **aplana** a la raíz del
  template que descarga el operador.
- Raíz: guías (`EMPIEZA-AQUI.md`, `GUIA-COMPLETA.md`, `00`–`12`, `README.md`),
  `docs/ARCHITECTURE.md` (spec real, manda sobre el blueprint), `en/` (docs EN),
  `pack.py`, `VERSION`, `CHANGELOG.md`, `PROGRESO.md` (bitácora interna).

## Construir y verificar
- Tests (73): `cd starter && PYTHONPATH=. python3 -m unittest discover tests`.
- Empaquetar el template: `python3 pack.py <destino>` → crea `<destino>/` y su `.zip`.
  Verifica siempre: 0 `cd starter`, 0 enlaces rotos, tests en verde **dentro** del ZIP.

## Publicar una versión
1. Sube `VERSION` (SemVer) y añade entrada en `CHANGELOG.md`.
2. `git tag vX.Y.Z && git push origin vX.Y.Z`.
3. La Action `.github/workflows/release.yml` corre tests, empaqueta con `pack.py` y
   crea la Release con el ZIP versionado. Descarga estable: `/releases/latest`.

## Reglas del proyecto (respétalas)
- **Determinista en código; el LLM solo redacta** (1 llamada/edición). Sin cifras
  inventadas; citas por `ref_id`; review-first (nada indexa sin aprobación).
- **Alcance honesto**: es un *digest* que redacta desde resúmenes de RSS, no del
  artículo completo; parafrasea y cita, no "verifica hechos".
- **Independiente**: NADA atado a cuentas/servicios personales del autor; sin
  telemetría, sin CDNs externas. Mantenlo genérico.
- **Secretos solo en `.env`/secrets**, jamás en el repo ni en el cliente.
- **NO marcar el repo como "template repository"**: contiene `starter/` + docs de
  desarrollo; "Use this template" daría eso, no el kit aplanado. La distribución es
  el **ZIP de la Release**.
- `pack.py` **excluye** los docs solo-mantenedor (PROGRESO, REVISION-EXTERNA, KIT-v2)
  del template. Si añades uno, decide si va en `GUIDES` o se excluye.

## Auto-actualización (v0.6+)
`scripts/update.py` baja la última Release y sobrescribe **solo el motor** (allowlist)
con backup; nunca toca `config.json`/`.env`/`data/`/`site/`/`prompts/`/`legal/`.
`scripts/lib/models.py` + `doctor` avisan si `compose.model` es un ID heredado.
