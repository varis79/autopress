# 07 · GUARDARRAÍLES — estándares editoriales

> Lo que hace a tu medio **creíble**. Parte está **impuesta por el código** (no depende de
> que la IA "se porte bien"); parte es política editorial tuya. Aquí está todo junto.

## Impuesto por el código (no negociable)

| Regla | Cómo se garantiza |
|---|---|
| **No inventar cifras** | QA bloquea la edición si un número de la redacción (incluidos los de un dígito: muertos, %, conteos) no aparece en su fuente (`numbers_supported`). |
| **Procedencia real** | La IA solo devuelve `ref_id`; el código copia la URL. Cita ajena o inventada → descartada. |
| **Anti-inyección** | El contenido RSS va delimitado y con `<`/`>` escapados: una fuente no puede dar órdenes. |
| **Sin esquemas activos** | Solo URLs http/https en enlaces (nada de `javascript:`). |
| **Stub nunca en producción** | El gate impide publicar borradores. |

## Perfiles de riesgo (tú eliges)

| Perfil | Cuándo | Qué hace |
|---|---|---|
| `auto` | Nichos inocuos | Publica solo **SOLO si activas `publishing.allow_auto_index`** (opt-in explícito). Por defecto (`false`) la edición pasa igual por **revisión humana** antes de indexarse. |
| `review` (**default**) | La mayoría | Genera la edición y **abre PR**: la revisas y haces merge. |
| `strict` | Sensibles (salud, política, personas) | + **≥2 fuentes independientes** por historia (QA bloquea si no) + revisión obligatoria. |

> **Review-first por defecto:** ni siquiera `auto` indexa sin `publishing.allow_auto_index=true`.
> Es a propósito: nada llega a Google sin tu visto bueno mientras no lo actives.

## Política editorial (recomendada)

- **Atribuye, no afirmes** lo contencioso: "según X…", nunca como hecho propio.
- **Neutralidad**: informa, no milites. Distingue hecho de análisis.
- **Correcciones**: ten un email de contacto y corrige rápido; señala la corrección.
- **Transparencia de IA**: declara que el contenido lo redacta una IA (`editorial.ai_disclosure`,
  footer, y `starter/legal/divulgacion-ia.md`).
- **Conflictos de interés**: si hay patrocinador, decláralo (ver `08-MODO-INDEPENDIENTE.md`).

## Cómo se ve en la práctica

Corre en `strict` y mira el estado: si una historia no tiene 2 fuentes independientes, QA
la marca `blocked` y no se publica. Eso es el guardarraíl funcionando, no un error.
