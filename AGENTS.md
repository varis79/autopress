# AGENTS.md — Autopress (punto de entrada del kit)

> **Eres un agente de código y alguien acaba de abrir el kit Autopress.** Tu
> trabajo: construir, junto a esta persona, **su propio medio editorial autónomo**
> sobre la temática que elija. Lee este archivo entero antes de tocar nada.

Autopress es un kit para montar un **medio de noticias curadas que se publica
solo**: ingiere fuentes RSS reales, las clasifica y selecciona (todo determinista,
gratis), redacta la edición con **una sola llamada a un LLM**, la publica como
sitio estático y envía una newsletter. Sin base de datos: el estado vive en Git.
Coste típico: **menos que un café al mes**. Agnóstico de temática.

---

## Orden de trabajo (síguelo)

1. **Lee este archivo.**
2. **Lee la arquitectura real (fuente de verdad):** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
   — corto y exacto (pipeline, config, máquina de estados, guardarraíles, comandos). El viejo
   `BLUEPRINT-MEDIO-AUTONOMO.md` es **material histórico, no ejecutable**: no lo sigas para
   implementar (solo como contexto).
3. **Haz el CUESTIONARIO DE ARRANQUE** (abajo). No asumas nada: **pregunta y espera
   respuesta.**
4. **Entra en `starter/`** — es el andamiaje ejecutable:
   - [starter/AGENTS.md](starter/AGENTS.md) — reglas de construcción (reglas de oro,
     perfiles de riesgo, SEO, verificación).
   - [starter/README.md](starter/README.md) — arquitectura y cómo correr en 30 s.
5. **Rellena los `<PLACEHOLDER>`** con las respuestas del cuestionario:
   - `starter/fixtures/config.json` (taxonomía, mercados, scoring, `compose.model`…)
     — validado por `starter/autopress.schema.json`.
   - `starter/prompts/master-prompt.md` (copia de `master-prompt.example.md` con el
     tono y las reglas del medio).
   - `starter/.env` (copia de `.env.example`; aquí va la clave de IA, **nunca** en el
     repo).
6. **Verifica contra `starter/fixtures/`** (test golden) **antes** de conectar el
   LLM: `cd starter && PYTHONPATH=. python3 -m unittest discover tests`.
7. **Construye por fases** siguiendo el blueprint; entrega el medio **funcionando
   end-to-end** con su propio README.

---

## Cuestionario de arranque (pregunta ESTO, una cosa a la vez)

No empieces a construir hasta tener respuestas a:

1. **Temática y ángulo** — ¿de qué va el medio y qué mirada aporta? **Debe tener flujo vivo
   de fuentes** (noticias nuevas con enlaces cada semana). Si es un tema estático o histórico
   (p. ej. "urbanismo del s. XVIII"), Autopress **no** es la herramienta: díselo con
   franqueza (ver `01-ANTES-DE-EMPEZAR.md`).
2. **Idioma(s)** de publicación.
3. **Mercados/geografías** — ¿cuáles son primarios y cuáles secundarios?
4. **Tono y voz** — sobrio/analítico, cercano, técnico…
5. **Perfil de riesgo** — `auto` / `review` (default) / `strict`. Temas sensibles
   (política, salud, geopolítica, personas nombradas) → `strict`. Detalle en
   [starter/AGENTS.md](starter/AGENTS.md) §3.
6. **¿Independiente o con patrocinador?**
7. **Nombre del medio** y si ya tiene **dominio**.
8. **¿Vas a monetizar?** (ads/afiliados/donaciones) **y ¿dónde quieres publicar?** El
   sitio es estático y va a cualquier host (ver `04-DESPLIEGUE.md`). Si monetiza, el plan
   gratis debe permitir uso comercial. **Verifica tú los términos vigentes del host que
   elija en el momento de construir** (cambian): busca "uso comercial / commercial use" en
   los ToS del host y avísale si su elección chocaría con monetizar. Recomendado por
   defecto: **Cloudflare Pages**.

---

## Reglas de oro (resumen — detalle en starter/AGENTS.md §2)

1. **Determinista en código; el LLM solo redacta** (una llamada por edición: cada
   llamada cuesta dinero).
2. **Nunca inventes cifras.** Sin dato con fuente → lenguaje cualitativo.
3. **Cada historia cita su(s) fuente(s)** con numeritos `[1][2]` al original.
4. **El HTML lo renderiza el código, no el LLM** (el LLM devuelve solo JSON).
5. **Secretos solo en variables de entorno** (`.env`), nunca en el repo ni en el
   cliente. El **modelo va en el YAML** (`compose.model`), no en el código.
6. **Solo enlaza páginas que existen en disco.**

---

## Configuración descubrible

El operador no tiene por qué saber qué se puede tocar. Si dice *"muéstrame los settings"*,
*"qué puedo configurar"* o quiere cambiar algo sin saber dónde vive (huso horario, modelo de
IA, perfil de riesgo, host, newsletter…), corre **`PYTHONPATH=. python3 -m scripts.settings
[tema]`** desde `starter/`: es el catálogo de TODO lo configurable, con su valor actual y
**dónde se toca** (config / .env / workflow / host). Enséñaselo y aplícalo tú.

## Qué automatizas tú (el agente) y qué es del operador

Automatiza **todo lo que no requiera crear cuentas ni iniciar sesión**:
- **Config, taxonomía, prompt maestro, `.env`** → `scripts/setup.py` los escribe.
- **Legales**: `scripts/setup.py` los **rellena solos** con las respuestas (nombre, email,
  país, dominio…). Si quedara algún `<PLACEHOLDER>`, complétalo tú desde el cuestionario. Deben
  quedar SIN placeholders (si no, producción se bloquea). Recuérdale que los revise (no son
  asesoría legal).
- **Generar el sitio, aprobar** (`scripts/pipeline`, `scripts/approve`), **commitear al repo**.
- **Deploy por CLI** (si el operador ya inició sesión en las CLIs): `gh secret set
  ANTHROPIC_API_KEY …`, `git push`, y el deploy del host (`wrangler pages deploy site`,
  `netlify deploy --prod --dir site`…). Ofrécete a correrlos.

**Del operador (una vez, no lo puedes hacer tú):** crear las cuentas (GitHub, host, Anthropic,
Resend), **iniciar sesión** en las CLIs (`gh auth login`, `wrangler login`…), sacar su **API
key** de la consola, el **DNS** del dominio, y la **decisión editorial** de aprobar en temas
sensibles. Guíale paso a paso en eso; el resto lo haces tú.

## Coste, licencia y atribución

- **Coste:** ~0,30–1,20 USD/mes (una edición semanal). Hosting estático gratis.
- **Licencia:** código (`starter/`) MIT; documentación CC BY 4.0. Ver [LICENSE](LICENSE).
- **Atribución:** añade en el footer un crédito **opcional y desmarcable** "Hecho
  con Autopress". Actívalo por defecto; si el operador lo quita, respétalo.

---

_Ahora: lee el blueprint, haz el cuestionario, y empieza por la primera fase.
Pregunta antes de asumir. Construye con criterio._
