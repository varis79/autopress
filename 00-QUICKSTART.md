# 00 · QUICKSTART — de cero a tu primera edición

> **Para quién:** cualquiera, aunque no sepas programar. Tú decides y supervisas;
> **el agente de IA hace el trabajo técnico**. Tiempo: ~60–90 min la primera vez.
> Al final tendrás **una edición de ejemplo publicada en tu ordenador** (todavía
> sin conectar nada de pago).

Este documento va por **checkpoints**. Después de cada paso hay un "✅ deberías
ver…". Si no lo ves, ahí mismo está el "🔧 si falla".

---

## Qué necesitas antes de empezar

1. **Un ordenador** (Mac, Windows o Linux).
2. **Un agente de código con acceso a terminal y ficheros** — Claude Code, Cursor,
   o similar. Es quien construye tu medio; tú le hablas en lenguaje normal.
3. **Python 3.11 o superior** instalado (el agente puede comprobarlo e instalarlo).
4. **Nada de pago todavía.** La clave de IA y las cuentas (host, newsletter) llegan
   más tarde. Este quickstart es 100% gratis y local.

> No necesitas saber qué es una terminal ni leer código. Vas a **copiar y pegar
> comandos** (los botones ▶ de esta guía) o pedirle al agente que los ejecute.

---

## Onboarding por niveles (nada es obligatorio)

No es todo-o-nada. **Avanzas por niveles y cada uno funciona solo**; añades lo que falta
cuando quieras, sin rehacer nada:

| Nivel | Tienes | Te falta y NO pasa nada |
|---|---|---|
| **0** | Tu medio corre en local (demo) | — |
| **1** | Publicado online | *sin dominio* → usas el subdominio gratis del host |
| **2** | Dominio propio | lo añades en `site.domain` cuando lo tengas |
| **3** | Feeds reales + IA | *sin clave* → modo stub (ves el medio sin gastar) |
| **4** | Se publica solo (CI) | opcional; hasta entonces lo lanzas tú |
| **5** | Newsletter | opcional |
| **6** | Monetizas | opcional |

> **Atajo:** en vez de editar ficheros a mano, usa el **asistente**:
> `cd starter && PYTHONPATH=. python3 -m scripts.setup` — te hace las preguntas y te escribe
> `config.json`, `.env` y el prompt. Salta lo que no tengas.

## Paso 0 · Consigue el kit y ábrelo con tu agente

Descarga el kit (ZIP desde `/releases/latest`) y ábrelo con tu
agente de IA. Lo primero que hará el agente es leer **`AGENTS.md`**, el archivo de
entrada.

Comprueba que tienes Python:

```bash
python3 --version
```

**✅ Deberías ver** algo como `Python 3.11.x` o superior.
**🔧 Si falla** (`command not found`): pídele al agente "instálame Python 3.11+" o
descárgalo de python.org. En Windows suele ser `python` en vez de `python3`.

Prepara un entorno aislado e instala las dependencias (una vez):

```bash
cd starter && python3 -m venv .venv && . .venv/bin/activate && python3 -m pip install -r requirements.txt
```

**✅ Deberías ver** que se instalan `feedparser` y `anthropic` sin errores.

> **🪟 Nota Windows (PowerShell).** Los comandos de esta guía usan sintaxis de
> Mac/Linux. En PowerShell, dos cambios: activa el entorno con `.venv\Scripts\Activate.ps1`,
> y donde veas `PYTHONPATH=. python3 -m scripts.X`, escríbelo en **dos líneas**:
> `$env:PYTHONPATH="."` y luego `python -m scripts.X`. Tu agente puede darte el
> comando exacto para tu sistema si se lo pides.

---

## Paso 1 · El cuestionario de arranque

Dile a tu agente: **"Vamos a empezar, hazme el cuestionario de arranque."** Te
preguntará (y **debe esperar tus respuestas**, no inventarlas):

- Temática y ángulo del medio
- Idioma(s)
- Mercados/geografías (cuáles son primarios)
- Tono y voz
- **Perfil de riesgo**: `auto`, `review` (recomendado) o `strict` (para temas
  sensibles: política, salud, geopolítica, personas)
- ¿Independiente o con patrocinador?
- Nombre del medio y si tienes dominio

**✅ Deberías ver** que el agente **te pregunta** en vez de asumir. Tómate tu tiempo
en las respuestas: son la línea editorial de tu medio.

---

## Paso 2 · El agente configura tu medio

Con tus respuestas, el agente rellena:

- `starter/fixtures/config.json` — taxonomía, mercados, scoring, modelo de IA.
- `starter/prompts/master-prompt.md` — la "constitución editorial" (tono + reglas).

No tienes que tocar estos ficheros a mano; el agente los edita. Puedes pedirle que
te explique en lenguaje normal qué puso.

**✅ Deberías ver** dos ficheros creados/editados con tus decisiones dentro.

---

## Paso 3 · Comprobación del entorno (doctor)

```bash
cd starter && PYTHONPATH=. python3 -m scripts.doctor
```

**✅ Deberías ver** al final: **`LISTO para modo local (fixtures, sin cuentas).`**
**🔧 Si falla:** el doctor te dice exactamente qué falta (p. ej. una dependencia).
Pásale el mensaje al agente y que lo resuelva.

---

## Paso 4 · Genera el sitio en modo de prueba (stub)

Todavía **sin gastar nada**. El "modo stub" redacta con texto de marcador para que
veas la estructura, el diseño y el control de calidad funcionando.

```bash
cd starter && PYTHONPATH=. python3 -m scripts.pipeline
```

**✅ Deberías ver** un JSON de estado con `"published": true` e **`"indexable": false`**
(es un **preview**: se marca `noindex` a propósito para no indexar borradores) y una
carpeta nueva `starter/site/`.

Míralo en el navegador con **un solo comando** (construye y sirve; abrir el `.html` directo
rompe los enlaces internos, que son absolutos):

```bash
cd starter && PYTHONPATH=. python3 -m scripts.serve
```

Abre `http://localhost:8000`. Es tu medio, navegable. El aviso `stub` es **correcto y
esperado**: es un borrador de prueba, no se publica en producción. Se quita al conectar
la IA (paso 6).

**🔧 Si falla:** copia el error al agente. Lo más común es que falte una dependencia
(activa el entorno del Paso 0 y `python3 -m pip install -r requirements.txt`).

---

## Paso 5 · (Opcional) Elige tu diseño

```bash
cd starter && PYTHONPATH=. python3 -m scripts.render_demo
```

Abre `starter/sample-output/gallery.html`: verás **6 estilos × 5 paletas** (claro y
oscuro). Elige el que te guste y dile al agente "usa el estilo X con la paleta Y";
lo pondrá en tu config.

**✅ Deberías ver** una galería con 30 combinaciones de aspecto.

---

## Paso 6 · Conecta la IA (primera edición de verdad)

Ahora sí, la redacción real. Necesitas **una clave de IA** (de tu proveedor de
modelo). Coste: **céntimos por edición** (ver [03-COSTES.md](03-COSTES.md)).

1. Copia la plantilla de secretos:
   ```bash
   cd starter && cp .env.example .env
   ```
2. Abre `.env` y pega tu clave en `ANTHROPIC_API_KEY=...`. **Este fichero nunca se
   sube a internet** (está protegido en `.gitignore`).
3. Vuelve a generar:
   ```bash
   cd starter && PYTHONPATH=. python3 -m scripts.pipeline
   ```

**✅ Deberías ver** una edición redactada de verdad: en el estado, `"gate_reasons"` **ya
no incluye `"stub"`**, y cada historia lleva sus **fuentes numeradas `[1][2]`** enlazando
al original.
**🔧 Si algo falla con la IA** (clave inválida, sin saldo, sin red): el sistema
**vuelve solo al modo stub** — no se rompe. Revisa la clave y el saldo.
> **Terminal nueva = reactiva el entorno.** Si abres otra terminal, vuelve a activar el
> venv (`. .venv/bin/activate`) antes de correr el pipeline: sin él falta el paquete
> `anthropic` y la edición **cae a stub aunque tu clave sea válida**. Comprueba en vivo con
> `PYTHONPATH=. python3 -m scripts.doctor --smoke` (hace 1 llamada real y avisa si algo falla).

> **De la demo a TUS noticias reales.** Sin más, el pipeline redacta la selección de
> **demo** (los fixtures) para que compruebes el circuito. Para noticias reales de tu tema,
> añade tus **feeds RSS** al config (bloque `sources`, ver `starter/autopress.schema.json`)
> y apunta el pipeline a tu propia config:
> ```bash
> PYTHONPATH=. python3 -m scripts.pipeline --config config.json
> ```
> Con `sources`, el pipeline **ingiere de la red** (con timeout, reintentos y diagnóstico
> por fuente) en vez de los fixtures. Y para la versión **indexable** (no preview) se corre
> en producción, que **no publica** si la edición es stub, está en pausa o QA la bloquea
> (sale con código ≠ 0):
> ```bash
> PYTHONPATH=. python3 -m scripts.pipeline --config config.json --production
> ```

---

## Ya tienes tu medio funcionando (en local). ¿Y ahora?

- **Publicarlo en internet** (gratis) → siguiente: [02-CUENTAS-Y-DOMINIO.md](02-CUENTAS-Y-DOMINIO.md).
- **Entender el coste real** y los free tiers → [03-COSTES.md](03-COSTES.md).
- **¿Dudas de si es para ti?** → [01-ANTES-DE-EMPEZAR.md](01-ANTES-DE-EMPEZAR.md).
- **Cómo funciona por dentro** (para ti o para tu agente) → [starter/README.md](starter/README.md).

> Regla de oro: **el agente construye, tú supervisas.** Cuando el tema sea sensible,
> revisa antes de publicar (perfil `strict`). Es tu medio y tu criterio.
