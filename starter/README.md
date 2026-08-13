# Autopress · starter (implementación de referencia)

> 🌐 **English:** [en/HOWTO.md](../en/HOWTO.md)

Motor de un **medio editorial autónomo**: ingiere feeds, clasifica, deduplica,
selecciona, **redacta con IA**, pasa control de calidad y **publica un sitio
estático navegable** — sin base de datos (Git es la base de datos) y con el
**núcleo determinista en código** (gratis, reproducible) y **la IA solo para el
juicio** (redactar). Corre entero **offline y sin claves** en modo demostración.

> Este `starter/` es la implementación de referencia genérica. No trae ninguna
> temática; el tema lo define el `config.json` + `prompts/master-prompt.md` que
> rellena el agente durante el onboarding.

---

## 1. Arranque en 30 segundos (sin claves, sin cuentas)

```bash
cd starter
PYTHONPATH=. python3 -m scripts.doctor        # comprueba entorno y ficheros
PYTHONPATH=. python3 -m scripts.pipeline       # genera el sitio en starter/site/
PYTHONPATH=. python3 -m unittest discover tests -v   # tests (deben ir todos verde)
```

Abre `starter/site/index.html`. Verás una edición de ejemplo (modo **stub**:
contenido de marcador, marcado como "no publicar en producción"). Para redacción
real, añade tu clave de IA (§4).

---

## 2. Cómo funciona (el pipeline)

Un flujo lineal; cada etapa es una función pura y testeable.

```
feeds RSS ─▶ ingest ─▶ classify ─▶ dedupe ─▶ select ─▶ compose ─▶ qa ─▶ publish ─▶ site/
             (red)     (determinista, en código, gratis)   (IA)   (control)  (HTML estático)
```

| Etapa | Fichero | Qué hace | ¿IA? |
|---|---|---|---|
| Ingesta | [scripts/ingest.py](scripts/ingest.py) | Descarga/parsea feeds, limpia HTML, id estable por URL canónica | No |
| Clasificación | [scripts/classify.py](scripts/classify.py) | topic (más coincidencias), market (título×2+resumen), players | No |
| Deduplicación | [scripts/dedupe.py](scripts/dedupe.py) | URL canónica + similitud de título; los duplicados se **fusionan** como fuentes extra | No |
| Selección | [scripts/select_stories.py](scripts/select_stories.py) | blacklist → scoring → cuotas geo/tema → modo (normal/short/pause) | No |
| **Redacción** | [scripts/compose.py](scripts/compose.py) | Llama al LLM; valida procedencia; **fallback a stub** | **Sí** |
| — stub | [scripts/compose_stub.py](scripts/compose_stub.py) | Redacción de marcador (sin gastar), para demo/tests | No |
| QA | [scripts/qa.py](scripts/qa.py) | Chequeos por nivel: blocking / review_required / warning | No |
| Publicación | [scripts/publish.py](scripts/publish.py) | Escribe index, edición, archivo, sitemap.xml, rss.xml | No |
| Orquestador | [scripts/pipeline.py](scripts/pipeline.py) | Une todo, carga `.env`, imprime estado JSON | No |
| Núcleo | [scripts/pipeline_core.py](scripts/pipeline_core.py) | `run()` (contrato golden) y `run_full()` (con dedupe) | No |

Librerías compartidas en [scripts/lib/](scripts/lib/): `text.py` (matching por
palabra Unicode, URL canónica), `templating.py` (render de edición + citas),
`site.py` (páginas, sitemap, RSS).

---

## 3. Procedencia y citas (estilo Perplexity, con validación)

Cada historia lleva sus fuentes numeradas `[1][2]`. El diseño impide que la IA
**invente** fuentes o historias:

1. La IA recibe los ítems dentro de `<untrusted_sources>` y solo puede devolver
   `ref_id` que existan en ese input.
2. `assemble()` en [compose.py](scripts/compose.py) **valida**: descarta cualquier
   `ref_id` de historia que no esté en la selección y cualquier `source_ref` con
   id desconocido. La URL de cada fuente la copia el **código** desde el registro
   validado, no la IA.
3. Los duplicados detectados en dedupe se conservan como **fuentes adicionales**
   de la misma historia (por eso una noticia puede tener `[1][2]`).

Verificable en los tests: `tests/test_compose.py` prueba que una fuente inventada
(`sFAKE00000`) se descarta y que una historia con `ref_id` desconocido no pasa.

---

## 4. Dónde van los tokens de IA (la clave)

**Nunca** en el código ni en el `config.json`. Solo en el entorno:

```bash
cp .env.example .env      # y rellena ANTHROPIC_API_KEY=...
```

- `.env` está en `.gitignore` (jamás se sube). En producción, la clave va en los
  *secrets* de GitHub Actions / variables de entorno del host.
- `scripts/pipeline.py` carga `.env` automáticamente (`_load_dotenv`, sin
  dependencias).
- **El modelo** se elige en `config.json` → `compose.model` (ahora
  `"claude-sonnet-5"`, económico; configurable). El id del modelo va en el YAML,
  no en el código.
- **Sin clave**, `compose()` cae a stub: el kit **nunca se rompe** y no gasta.

Contrato completo de config en [autopress.schema.json](autopress.schema.json).
Un config que no valide contra el esquema **no debe ejecutarse** (`validate_config.py`).

---

## 5. Diseño: estilos × paletas (30 combinaciones)

El estilo (estructura+tipografía) y la paleta (color) están **desacoplados** vía
variables CSS y atributos `data-style` / `data-palette` / `data-theme` en
[theme/theme.css](theme/theme.css): **6 estilos × 5 paletas × claro/oscuro**.

```bash
PYTHONPATH=. python3 -m scripts.render_demo    # genera sample-output/gallery.html
```

La galería es lo que se sube a la web para elegir look sin tocar código.

---

## 6. Gobernanza: perfiles de riesgo y QA

- **risk_profile** (`config.json`): `auto` (auto-publica) · `review` (default: abre
  PR y para) · `strict` (revisión humana + doble fuente + enfriamiento).
- **QA por niveles** ([qa.py](scripts/qa.py)): `blocking` (p.ej. falta portada →
  no publica) · `review_required` (p.ej. historia sin fuente) · `warning` (p.ej.
  stub). El status resultante (`ok` / `ok-qa-warn` / `blocked`) lo consume el
  workflow según el perfil.
- Un **stub jamás llega a producción** (`publishing.block_stub_in_production`).

---

## 7. Estructura de carpetas

```
starter/
├─ AGENTS.md               # punto de entrada para el agente (reglas del proyecto)
├─ README.md               # este documento (arquitectura + cómo correr)
├─ autopress.schema.json   # contrato de configuración (validado)
├─ .env.example            # dónde van las claves (copiar a .env)
├─ .gitignore              # .env, __pycache__, /site/
├─ prompts/
│  └─ master-prompt.example.md   # constitución editorial (renombrar a master-prompt.md)
├─ scripts/                # el pipeline (ver §2)
│  └─ lib/                 # text, templating, site
├─ theme/theme.css         # 6 estilos × 5 paletas × claro/oscuro
├─ fixtures/               # datos de ejemplo + golden (config, raw.jsonl, expected/)
├─ tests/                  # golden, ingest, compose (todos offline)
├─ sample-output/          # galería de diseños generada
└─ site/                   # salida del pipeline (generada; en .gitignore)
```

---

## 8. Tests (todo offline, no gasta API)

```bash
cd starter && PYTHONPATH=. python3 -m unittest discover tests -v
```

- `test_pipeline_golden.py` — **contrato de reproducibilidad**: dos agentes con el
  mismo input producen la misma selección (`fixtures/expected/selection.json`).
  También verifica dedupe y filtro de competidor.
- `test_ingest.py` — parseo/normalización de feeds y ventana de recencia.
- `test_compose.py` — procedencia (rechazo de fuentes/historias inventadas) y
  fallback a stub sin clave.

---

## 9. Estado y límites (para revisión)

**Hecho y verificado:** pipeline completo offline; golden test verde; citas
numeradas multi-fuente con validación de procedencia; compose LLM con
anti-inyección y fallback; superficie de tokens (`.env`); 30 combinaciones de
diseño; QA por niveles alineado con el modelo de fuentes.

**Pendiente (roadmap):** empaquetado raíz (requirements pinneados, LICENSE);
onboarding paso a paso para no técnicos (SPF/DKIM/DMARC, costes); adaptador de
deploy (Cloudflare Pages) + CI + newsletter doble opt-in; fixtures adversarias de
inyección; documento legal (divulgación IA). Cambios registrados en
[../PROGRESO.md](../PROGRESO.md).

**Coste estimado** de operar un medio así: ~0,30–1,20 USD/mes (hosting estático
gratis + una llamada de IA por edición semanal).
