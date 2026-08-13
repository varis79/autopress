# 06 · ADAPTACIÓN TEMÁTICA — playbooks por tipo de tema

> Cómo ajustar `config.json` (taxonomía, mercados, scoring) y el `master-prompt.md` según
> tu tema. La estructura es la misma; cambian las palabras clave, las fuentes y el tono.

## Los 4 ajustes que definen un tema

1. **Fuentes** (`sources`) — los feeds RSS. Es lo que más define el medio. Busca la prensa
   sectorial, reguladores, boletines y blogs de referencia de tu tema.
2. **Temas y keywords** (`taxonomy.topics`) — 3-6 temas con sus palabras clave (en el idioma
   de las fuentes). Ejemplo: `regulation: [regulation, law, compliance]`.
3. **Mercados** (`taxonomy.markets`) — geografías con `tier` (primary/secondary) y keywords.
4. **Tono** (`master-prompt.md`) — la voz para ese público.

## Playbooks

**Nicho B2B / sectorial** (logística, fintech, energía…)
- Fuentes: prensa del sector + reguladores. Tono técnico, para profesionales.
- Riesgo `review` o `auto` si es inocuo y con patrocinador.

**Regulatorio / política pública**
- Prioriza `regulation` en `priority_topics`. Atribuye siempre; nada de opinar como hecho.
- Riesgo `strict` si hay actores nombrados o es contencioso.

**Tecnología / producto**
- Keywords de producto y empresas (`players`). Cuidado con el hype: reglas de oro (§ cifras).

**Local / regional**
- Un solo mercado `primary`; keywords de ciudades/instituciones locales.

**Temas sensibles** (salud, política, personas)
- **`strict` obligatorio**: corroboración ≥2 fuentes independientes, revisión humana,
  acusaciones siempre atribuidas. Ver `07-GUARDARRAILES.md`.

## Cómo encontrar feeds RSS

- Busca "`<tu tema>` RSS" o añade `/feed`, `/rss` a la web de la fuente.
- Reguladores y prensa suelen tener feed. Verifica que actualiza y que sus términos permiten
  resumir/citar (ver `starter/legal/derechos-fuentes.md`).
- Empieza con 3-5 fuentes buenas; el pipeline deduplica y selecciona.

> El agente puede proponerte taxonomía y fuentes iniciales para tu tema; revísalas y ajusta.
