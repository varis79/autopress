# Guía completa — de cero a tu medio publicado (paso a paso, para todos)

Esta guía te lleva de la mano. **Tu agente de IA (Claude Code / Cursor) hace lo técnico**;
tú creas unas cuentas y decides. Tiempo: una o dos tardes la primera vez. Nada es obligatorio
de golpe: avanzas por niveles.

> Si prefieres el resumen rápido, ve a [00-QUICKSTART.md](00-QUICKSTART.md). Aquí está TODO,
> con enlaces de alta y qué copiar en cada sitio.

---

## Paso 1 · Las cuentas (crea solo las que vayas necesitando)

| Servicio | Para qué | Dónde darte de alta | Qué copiar |
|---|---|---|---|
| **GitHub** | Guardar el proyecto y automatizar | https://github.com/signup | (nada aún) |
| **Anthropic** | La IA que redacta | https://console.anthropic.com | tu **API key** |
| **Cloudflare** | Publicar el sitio (gratis, permite monetizar) | https://dash.cloudflare.com/sign-up | (nada aún) |
| **Resend** *(opcional)* | La newsletter | https://resend.com/signup | **API key** + **Audience ID** |
| **Dominio** *(opcional)* | `tumedio.com` | cualquier registrador (Namecheap, Cloudflare…) | (~10–15 $/año) |

> **Sin dominio, sin newsletter y sin monetizar** puedes tener tu medio online igualmente.
> Añádelos cuando quieras.

### Cómo sacar tu API key de Anthropic (la que más se usa)
1. Entra en **https://console.anthropic.com** y regístrate.
2. **Billing** → añade un método de pago y algo de saldo (el uso real son **céntimos al mes**).
3. **API Keys** → **Create Key** → cópiala (empieza por `sk-ant-…`). **Guárdala**, no se vuelve
   a mostrar. Esa es tu `ANTHROPIC_API_KEY`.

> **Regla de oro de seguridad:** nunca pegues una clave en el chat con tu agente. Mejor pon la
> clave directamente en el `.env` (con el asistente) o en los *secrets* del host/GitHub.

---

## Paso 2 · Configura tu medio (el agente lo hace contigo)

Abre el proyecto con tu agente y dile: **"hazme el asistente"**. O tú mismo:
```bash
PYTHONPATH=. python3 -m scripts.setup
```
Te preguntará, y con tus respuestas escribe todo (config, prompt, `.env`) **y rellena los
textos legales solo**. Ejemplo de respuestas para un medio de movilidad:
- Nombre: `Radar Movilidad` · Idioma: `es` · Tono: `sobrio y analítico`
- Temas: `regulación, baterías, cargadores` · Mercados: `México, España`
- Perfil de riesgo: `review` (recomendado para empezar)
- Email de contacto, país, dominio (si lo tienes)

> ¿No sabes qué se puede tocar? Di **"muéstrame los settings"**.

---

## Paso 3 · Que el CONTENIDO salga bien (lo más importante)

El motor es bueno, pero la calidad la marcan **tus fuentes** y **tu prompt**:

1. **Elige 3–8 feeds RSS buenos** de tu tema (prensa sectorial, reguladores, blogs de
   referencia). Para encontrarlos: busca "`tu tema` RSS", o prueba a añadir `/feed` o `/rss` a
   la web de la fuente. Añádelos en `config.json` → `sources`.
   - Anota licencia/derechos de cada fuente (campos `license`, `rights_status`); excluye las
     que no permitan resumir. Ver [`starter/legal/derechos-fuentes.md`](starter/legal/derechos-fuentes.md).
2. **Ajusta el prompt maestro** (`prompts/master-prompt.md`): tono, a quién te diriges, qué
   evitar. Es la "línea editorial".
3. **Empieza en `review`**: genera la edición y **revísala tú** antes de publicar. Mira si los
   resúmenes son fieles y si las fuentes están bien citadas. Ajusta keywords/scoring si la
   selección no es la que quieres.
4. **Recuerda el alcance honesto**: la IA redacta desde los **resúmenes del RSS**, no del
   artículo entero. Parafrasea y cita; **no inventa cifras** (el sistema bloquea las que no
   estén en la fuente) y **no publica acusaciones** sin atribución y ≥2 fuentes.

---

## Paso 4 · Míralo en tu ordenador (gratis, sin publicar)
```bash
PYTHONPATH=. python3 -m scripts.serve
```
Abre `http://localhost:8000`. Sin clave de IA sale en modo demo (`stub`); con tu
`ANTHROPIC_API_KEY` en `.env`, redacta de verdad. **Haz esta prueba antes de publicar.**

---

## Paso 5 · Publícalo (Cloudflare Pages)

1. Sube el proyecto a un repo de **GitHub** (tu agente lo hace con `git`).
2. En **Cloudflare** → **Workers & Pages → Create → Pages → Connect to Git** → elige tu repo.
   - Build command: *(ninguno)*. Output directory: **`site`**.
3. Te da una URL `tumedio.pages.dev`. Para dominio propio: **Custom domains**.
4. Para publicar de verdad (indexable) y automatizar, ver [04-DESPLIEGUE.md](04-DESPLIEGUE.md).
   El agente puede hacer el deploy por CLI si inicias sesión (`wrangler login`).

> Comparativa de hosts y el aviso de uso comercial: [04-DESPLIEGUE.md](04-DESPLIEGUE.md).

---

## Paso 6 · Newsletter (opcional, llave en mano)
Las funciones ya están hechas. Sigue [`starter/newsletter/README.md`](starter/newsletter/README.md):
crea Resend, verifica tu dominio, y pega 5 variables en Cloudflare. El formulario ya funciona.

---

## Paso 7 · Cada semana (se publica solo)
Activa el workflow `.github/workflows/publish.yml` (pon tu `ANTHROPIC_API_KEY` en GitHub →
Settings → Secrets). Según tu perfil: `auto` publica solo (si lo activas), `review`/`strict`
**abren un PR** para que revises y hagas merge. Detalle en [04-DESPLIEGUE.md](04-DESPLIEGUE.md).

---

## Si algo falla
Mira [12-TROUBLESHOOTING.md](12-TROUBLESHOOTING.md). Recuerda: un "bloqueo" en producción suele
ser el guardarraíl funcionando (falta legal, dominio, o la edición necesita tu aprobación).
