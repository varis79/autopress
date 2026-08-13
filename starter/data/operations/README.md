# data/operations/ — reporte de cada ejecución (operabilidad)

Cada run del pipeline deja aquí su estado:

- **`latest.json`** — el último run (siempre se sobrescribe).
- **`<timestamp>.json`** — historial (solo en `--production`).

Incluye: origen (fixtures/feeds), recuento, modo, `edition_status`, `quality`, `gate_reasons`,
`compose_error` (por qué se cayó a stub, si aplica) y el diagnóstico por feed. Es lo que miras
para saber **qué pasó y por qué** cuando algo no se publicó.

> Los `.json` están en `.gitignore` (se regeneran). En CI conviene subir `latest.json` como
> artefacto del job.
