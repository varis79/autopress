# Paquete de revisión externa — Autopress

> Para pasar el proyecto a **otras IAs** (o revisores humanos) y recibir una crítica
> útil, comparable y accionable. Contiene: (1) cómo usarlo, (2) el **prompt de
> revisión** listo para copiar, (3) los **ficheros a dar** en orden de lectura, (4) las
> **decisiones ya tomadas** que no hay que re-litigar. **Fecha: 2026-08-10.**

---

## 1. Cómo hacer la revisión

- Usa **2–3 IAs distintas** (p. ej. una de cada familia) para triangular. Sus sesgos se
  cancelan; lo que las tres marcan, es real.
- **Dales los ficheros** (§3). Si la herramienta acepta subir carpetas/zip, mejor. Si no,
  pega en el **orden de lectura** indicado. Prioriza el Tier 1–3; el Tier 4 es referencia.
- Pega el **prompt de §2** al final, después de los ficheros.
- Pídeles la salida en el **formato** que el prompt exige, para poder comparar respuestas.
- Trae aquí sus respuestas y las consolidamos (como hicimos con las 4 primeras).

**Snapshot compartible** (zip limpio, sin secretos ni generados):
```bash
cd "/Users/varis/Desktop/Air/Claude" && zip -r autopress-review.zip autopress \
  -x '*/__pycache__/*' -x '*/site/*' -x '*/.env' -x '*/.DS_Store'
```

---

## 2. EL PROMPT (copia desde aquí)

```
ROL: Eres un revisor senior de producto y de ingeniería, escéptico y constructivo.
Vas a auditar "Autopress", un kit open-source para que una persona NO técnica
construya, con ayuda de un agente de IA, un "medio de curación de noticias que se
publica solo": ingiere feeds RSS reales, clasifica/deduplica/selecciona (todo
determinista, en código), redacta la edición con UNA llamada a un LLM, la publica como
sitio estático y envía newsletter. Sin base de datos (el estado vive en Git).

TU OBJETIVO: encontrar los fallos, riesgos y huecos que impedirían que esto sea
(a) creíble, (b) barato y robusto, (c) usable por alguien no técnico, (d) seguro con
los secretos, (e) legal. No adules. Prioriza por severidad y sé concreto.

PRINCIPIOS DE DISEÑO (entiéndelos; solo cuestiónalos con argumento fuerte):
- Determinista en código (gratis, auditable); el LLM SOLO redacta (1 llamada/edición).
- Procedencia: el LLM devuelve solo `ref_id`; el CÓDIGO copia la URL desde un registro
  validado y RECHAZA ids desconocidos → la IA no puede inventar fuentes. Citas [1][2].
- Anti-inyección: el contenido RSS (no confiable) va dentro de <untrusted_sources>.
- Sin secretos en el repo: claves solo en variables de entorno (.env / secrets).

DECISIONES YA CERRADAS (no las re-litigues salvo que tengas un argumento de peso):
- D1: SEO técnico siempre, pero generación masiva de páginas OFF por defecto (quality-gate).
- D2: caso base exigente pero genérico (sin temática fija).
- D3: host por defecto Cloudflare Pages (el free de Vercel prohíbe uso comercial).
- D4: ALCANCE = solo curación de NOTICIAS (temas con flujo vivo de fuentes). NO cubre
  temas estáticos/históricos ni revistas de ensayo generado. Verifica que producto y
  docs sean coherentes con esto; marca donde prometan de más.

AUDITA ESTAS DIMENSIONES. Para cada hallazgo: severidad (crítico/alto/medio/bajo),
dimensión, descripción, ubicación (fichero:línea si aplica) y recomendación concreta.
1. CREDIBILIDAD / PROCEDENCIA: ¿puede colarse una fuente o un HECHO/cifra inventada pese
   a las validaciones de compose.py (assemble) y qa.py? ¿Existe un check que falle el
   build ante cifras sin fuente, o falta? ¿Huecos?
2. ANTI-INYECCIÓN: ¿bastan los delimitadores? Diseña 2–3 payloads de una fuente RSS
   maliciosa que intenten secuestrar la redacción y di si el diseño los frena.
3. SECRETOS: ¿alguna vía por la que una API key acabe en el repo, en el HTML de cliente,
   en logs, o en el sitio publicado?
4. ROBUSTEZ: fallos de red, feed malformado, 0 noticias, dedupe demasiado agresivo,
   encodings raros, fechas. ¿Degrada con gracia (p. ej. cae a stub) o rompe?
5. COSTE: ¿las cifras de 03-COSTES.md son realistas? ¿Multiplicadores ocultos?
6. USABILIDAD NO-TÉCNICA: ¿00-QUICKSTART.md es seguible de verdad sin saber programar?
   ¿Dónde se atasca la gente? ¿Qué checkpoint falta?
7. ALCANCE (D4): coherencia producto/docs con "solo curación de noticias".
8. LEGAL: derechos sobre contenido RSS (resumir vs copiar), divulgación de IA, privacidad
   de la newsletter (doble opt-in, baja). ¿Qué falta antes de publicar?
9. SEO: ¿el quality-gate de indexación está bien planteado? ¿Riesgos de penalización?
10. HUECOS vs. PROMESA: ¿qué describe el blueprint que NO está implementado y debería
    estar para un MVP realmente compartible?

FORMATO DE SALIDA (respétalo):
A) Resumen ejecutivo (5–8 líneas): ¿está listo para compartir? ¿riesgo mayor?
B) Tabla de hallazgos: Severidad | Dimensión | Hallazgo | Fichero:línea | Recomendación.
C) Top 5 acciones antes de publicar, ordenadas por impacto.
D) Qué está BIEN (para no romperlo al iterar).
Si algo no puedes verificar con los ficheros dados, dilo explícitamente en vez de asumir.
```

---

## 3. Ficheros a dar (orden de lectura)

⭐ = crítico para la revisión de credibilidad/seguridad.

**Tier 1 — Producto, estado y decisiones**
- `README.md` — qué es, para quién, licencias.
- `PROGRESO.md` — estado real, decisiones **D1–D4**, changelog. (Da el contexto vivo.)
- `01-ANTES-DE-EMPEZAR.md` — el alcance (D4) explicado.

**Tier 2 — Cómo se usa (revisión de usabilidad)**
- `AGENTS.md` — punto de entrada + cuestionario de arranque.
- `00-QUICKSTART.md` — el recorrido no-técnico con checkpoints.
- `02-CUENTAS-Y-DOMINIO.md` — cuentas, DNS, SPF/DKIM/DMARC.
- `03-COSTES.md` — tabla de costes verificada + escenarios.

**Tier 3 — Arquitectura y código (revisión técnica)**
- `starter/README.md` — arquitectura y mapa etapa×fichero.
- `starter/AGENTS.md` — reglas de oro (no negociables).
- `starter/autopress.schema.json` — contrato de configuración.
- ⭐ `starter/scripts/compose.py` — redacción LLM, **procedencia + anti-inyección**.
- `starter/scripts/compose_stub.py` — redacción de marcador (fallback).
- `starter/scripts/pipeline_core.py`, `starter/scripts/pipeline.py` — orquestación.
- `starter/scripts/ingest.py`, `classify.py`, `dedupe.py`, `select_stories.py` — núcleo determinista.
- ⭐ `starter/scripts/qa.py` — control de calidad por niveles.
- `starter/scripts/publish.py`, `starter/scripts/lib/{site,templating,text}.py` — render/publicación.
- `starter/tests/{test_pipeline_golden,test_ingest,test_compose}.py` — contrato y cobertura.
- `starter/fixtures/{config.json,raw.jsonl,expected/selection.json}` — datos y golden.

**Tier 4 — Especificación y referencia (para verificar huecos)**
- `BLUEPRINT-MEDIO-AUTONOMO.md` — la spec completa (larga; úsala para el punto 10).
- `KIT-v2-DECISIONES-Y-PLAN.md` — decisiones y hechos verificados (afiliados, costes, ToS).
- `starter/.env.example`, `starter/requirements.txt`, `starter/prompts/master-prompt.example.md`,
  `starter/theme/theme.css`.

---

## 4. Qué NO pedirles (ya decidido o fuera de alcance)

- Rediseñar el principio "determinista + 1 llamada LLM" (es el núcleo del valor).
- Proponer base de datos (es "Git como base de datos" a propósito).
- Ampliar a temas históricos/ensayo (descartado en **D4**).
- Elegir otro host por defecto (D3 ya sopesó Vercel vs Cloudflare).
- Detalles de diseño visual fino (se itera aparte); pueden comentar, no es prioridad.

> Pueden **cuestionar** cualquiera de estas con un argumento fuerte — pero que sepan que
> ya se debatieron, para que no gasten el review en re-abrir lo cerrado.

---

_Cuando tengas 2–3 respuestas, tráelas y las consolidamos en un plan de acción priorizado
(como el consolidado de las 4 primeras revisiones que ya hicimos)._
