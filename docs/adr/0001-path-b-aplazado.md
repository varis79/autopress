# ADR 0001 — Path B se aplaza a v0.8; v0.7 endurece el núcleo

- Estado: **Propuesto** (borrador para revisión)
- Fecha: 2026-08-13
- Contexto: definición de alcance de la v0.7

## Contexto
Autopress es hoy un **digest honesto**: la IA redacta desde el **título + resumen
del RSS**, no del artículo completo (`docs/ARCHITECTURE.md:15-21`,
`ingest.py:139` trunca el resumen a 320c). Por eso la indexación automática está
**desactivada por defecto** (`allow_auto_index=false`) y todo pasa por revisión.

"Path B" es el gap conocido: **leer el artículo real + evidencia por afirmación**,
para acercarse a algo parecido a verificación y poder relajar el auto-index con más
garantías. La auditoría lo evaluó como dimensión propia.

## Decisión
**Path B no entra en v0.7.** v0.7 se centra en fiabilidad del `compose`, seguridad
del endpoint de boletín, credibilidad de los guardarraíles y coherencia docs↔código,
más una capa de E-E-A-T/SEO on-page (determinista). Path B se diseña e implementa en
**v0.8+**, por fases y detrás de flag OFF.

## Motivos
1. **Riesgo de vender media feature.** El verificador adversarial **refutó** la
   preocupación legal (hoy no se descarga ningún cuerpo de artículo: 0 coincidencias
   de `fetch_article`/`readability` en `scripts/`) y **degradó a low/overstated** el
   resto de hallazgos de Path B: describen algo que no existe.
2. **Rompería principios si se hace a medias.** Ampliar la `_evidence` con el cuerpo
   del artículo SIN un check por-afirmación **debilita** la garantía anti-cifras
   (`qa.py` + `lib/text.py:number_tokens` comprueban pertenencia de tokens numéricos;
   con un corpus grande crece la probabilidad de falso "soportado"). Presentarlo como
   "más garantías" para relajar `allow_auto_index` viola el principio 1 (alcance
   honesto) y el 4 (review-first).
3. **La costura ya está limpia; no hay coste por esperar.** Las piezas reutilizables
   existen y no se tiran: procedencia por `ref_id` (`compose.assemble()`), `_evidence`
   (`compose_stub.py:22`), etiquetas de riesgo (`risk.py`), fuentes independientes
   (`registrable_domain`), y **la capa anti-SSRF de fetch** (`ingest.py:42-107`) —
   la pieza más difícil de un futuro Path B ya está hecha y probada.

## Precondiciones para abrir Path B (v0.8)
1. `doctor --smoke` probado en vivo (entra en v0.7): confianza reproducible en el
   camino LLM antes de añadirle superficie.
2. **Verificación numérica a nivel afirmación/entidad** diseñada y testeada (p. ej.
   ventana de N tokens donde co-ocurran cifra + entidad), no solo pertenencia de token.
3. **Extractor HTML→cuerpo determinista y ligero** evaluado (stdlib; sin dependencias
   pesadas ni CDNs).

## Consecuencias
- v0.7 puede publicarse rápido y subir de verdad la barra de fiabilidad/seguridad.
- La relajación de `allow_auto_index` se pospone hasta que exista el gate de
  originalidad/evidencia real — coherente con "no prometas verificación de hechos".
- El marketing sigue diciendo "curación con cita y guardarraíles", no "verificación".

## Alternativas descartadas
- **Path B fase 1 en v0.7 (solo fetch+extract, sin check por-afirmación):** descartada
  por (2) — introduce el riesgo justo antes de tener la mitigación.
- **No hacer Path B nunca:** descartada — es la palanca de credibilidad a medio plazo;
  solo se secuencia después del endurecimiento.
