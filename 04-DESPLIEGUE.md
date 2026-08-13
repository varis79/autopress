# 04 · DESPLIEGUE — publica tu sitio donde quieras

> **Idea clave:** lo que genera Autopress es un **sitio estático** (HTML + CSS + `rss.xml`
> + `sitemap.xml`, en la carpeta `site/`). Eso se sube **tal cual a cualquier host
> estático** — no hay nada atado a un proveedor. Aquí tienes un **recomendado** para
> empezar y **cuatro opciones** con guía, para que elijas tú.

_Datos de planes/ToS verificados en 2026-08 (fuentes al final). **Los términos cambian:**
tu agente te pregunta host y monetización en el cuestionario de arranque y **comprueba los
términos vigentes** del host que elijas — esta guía es una referencia con fecha, no la
verdad eterna._

---

## Lo único que de verdad importa al elegir: ¿vas a monetizar?

Algunos planes gratuitos **prohíben el uso comercial** (ads, afiliados, vender, incluso
pedir donaciones según el caso). Es la única trampa real. Regla rápida:

- **Vas a monetizar** (ads / afiliados / donaciones / cobrar) → **Cloudflare Pages** o
  **Netlify** (sus planes gratis sí permiten uso comercial).
- **No monetizas** (proyecto personal, informativo) → **cualquiera** de los cuatro sirve.

---

## Comparativa (gratis, 2026-08)

| Host | ¿Free permite monetizar? | Límites del plan gratis | Dominio propio | Facilidad |
|---|---|---|---|---|
| **⭐ Cloudflare Pages** (recomendado) | ✅ **Sí** | Bandwidth **ilimitado** | Gratis | Fácil (conecta el repo) |
| **Netlify** | ✅ **Sí** (no puedes *revender* el hosting) | 100 GB/mes · 300 min build/mes | Gratis | **Muy fácil** (Git o arrastrar carpeta) |
| **GitHub Pages** | ⚠️ **No** para negocio/e-commerce/SaaS | 100 GB/mes (soft) · sitio ≤1 GB · 10 builds/h | Gratis | Fácil (desde el mismo repo) |
| **Vercel** | ⚠️ **No** en Hobby (solo personal) · Pro $20/mes | 100 GB/mes | Gratis | Muy fácil |

**Por qué Cloudflare Pages es el recomendado por defecto:** permite uso comercial en
gratis, no te limita el bandwidth, da dominio propio gratis y se conecta al repo en un par
de clics. Pero es una **recomendación, no una obligación**: tu sitio es portable.

---

## Mini-guías (elige una)

En los tres primeros, el patrón es el mismo: **conectas tu repo de GitHub** y el host
**reconstruye y publica solo** cada vez que cambie. Le indicas que la carpeta a publicar es
la de salida del sitio (`site/`).

### ⭐ Cloudflare Pages (recomendado)
1. Cuenta gratis en Cloudflare → **Workers & Pages → Create → Pages → Connect to Git**.
2. Elige tu repo. Build command: *(ninguno, es estático)*. Output directory: **`site`**.
3. Deploy. Te da `tumedio.pages.dev`. Añade tu dominio en **Custom domains**.

### Netlify (la más fácil para no técnicos)
1. Cuenta gratis en Netlify → **Add new site → Import an existing project** (o arrastra la
   carpeta `site/` en *Deploys* para una prueba rápida).
2. Publish directory: **`site`**. Deploy.
3. Dominio propio en **Domain settings**.

### GitHub Pages (solo si NO monetizas)
1. En tu repo → **Settings → Pages**.
2. Publica desde una rama/carpeta con el sitio, o con una GitHub Action que suba `site/`.
3. Dominio propio en el mismo panel. ⚠️ Recuerda: su ToS **no permite** usarlo para negocio.

### Vercel (con aviso)
1. Importa el repo en Vercel. Output: **`site`**. Deploy.
2. ⚠️ El plan **Hobby (gratis) es solo uso personal no comercial**. Si monetizas necesitas
   **Pro (~$20/mes)**. Para un medio con ads/afiliados, mejor Cloudflare o Netlify.

---

## Automatización: se publica solo (GitHub Actions)

El kit trae el workflow **`.github/workflows/publish.yml`** que hace que tu medio se
publique **solo cada semana**. La clave: el **compose con IA corre una sola vez ahí** (con
tu clave en *Secrets*), y el host solo **sirve el `site/` ya renderizado** — no re-ejecuta
la IA ni necesita saber Python.

**Puesta en marcha (una vez):**
1. En GitHub → **Settings → Secrets and variables → Actions** → añade `ANTHROPIC_API_KEY`.
2. Crea tu **`config.json`** de producción en la raíz del repo (con tu bloque `sources`).
3. Conecta tu host al repo con **carpeta a publicar = `site`** y **sin build command** (el
   sitio ya viene renderizado en el repo).

**Qué hace cada semana** (lunes por defecto; también hay botón manual):
- Corre el pipeline en modo producción y, según tu **`risk_profile`**:
  - `auto` → **commitea y publica solo** (el host redepliega al detectar el push).
  - `review` / `strict` → **abre un Pull Request** para que lo revises y hagas merge (no se
    publica hasta que tú quieras — fiel a "revisión humana").
  - stub / pausa / QA bloqueada → **el job falla** y no publica nada.

> `site/` y `data/editions/` **se versionan** (el CI los actualiza). El host sirve `site/`;
> `data/editions/` es tu histórico ("Git como base de datos"). Cambiar de host no toca tu
> pipeline: reconectas el repo en otro sitio y ya.

---

## Fuentes (verificado 2026-08)

- Cloudflare Pages — [pricing](https://developers.cloudflare.com/pages/functions/pricing/) ·
  [plan gratis](https://www.cloudflare.com/plans/free/)
- Netlify — [uso comercial (foro oficial)](https://answers.netlify.com/t/can-we-use-netlify-free-plan-for-commercial-purposes/41545) ·
  [pricing](https://www.netlify.com/pricing/)
- GitHub Pages — [límites y uso permitido](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- Vercel — [plan Hobby](https://vercel.com/docs/plans/hobby)

_Anterior: [03-COSTES.md](03-COSTES.md) · Cuentas y DNS: [02-CUENTAS-Y-DOMINIO.md](02-CUENTAS-Y-DOMINIO.md)_
