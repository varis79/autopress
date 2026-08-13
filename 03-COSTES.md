# 03 · COSTES — cuánto cuesta de verdad

> **Resumen:** un medio semanal cuesta **menos que un café al mes**. El gasto
> inevitable es la **IA** (céntimos por edición) y, si quieres dominio propio,
> **~10–15 USD/año**. El resto del stack tiene planes gratuitos que sirven para
> empezar.
>
> **Datos verificados en 2026-06** (precios de modelo) y **2026-08** (free tiers y
> términos de host). **Verifica los vigentes antes de decidir** — cambian.

---

## 1. El único coste variable: la IA

El medio hace **una sola llamada al modelo por edición** (el resto —ingesta,
clasificación, selección— es código gratis). Por eso es tan barato.

| Modelo | Precio ($/1M tokens in · out) | Coste/edición | Coste/mes (semanal + teaser) |
|---|---|---|---|
| Haiku 4.5 | $1 / $5 | ~$0.05 | **~$0.30** |
| Sonnet 5 | $3 / $15 | ~$0.14 | **~$0.73** |
| Opus 5 | $5 / $25 | ~$0.24 | **~$1.20** |

El modelo se elige en tu config (`compose.model`). Empieza por uno **económico**
(Sonnet o Haiku) y sube solo si notas que la redacción lo pide.

**Qué multiplica el coste** (y cómo evitarlo):
- Publicar a diario en vez de semanal (×7).
- Generación masiva de páginas SEO con IA → **desactivada por defecto** a propósito
  (Google penaliza el contenido a escala, y dispara el gasto).
- Reescrituras/reintentos innecesarios. Una llamada por edición basta.

---

### La fórmula (para que te salgan las cuentas)

`coste/edición ≈ (tokens_entrada × precio_in + tokens_salida × precio_out) / 1.000.000`

- **Entrada**: la selección (unas 5-8 noticias resumidas) + el prompt maestro ≈ **1-3k tokens**.
- **Salida**: la edición redactada, tope `compose.max_tokens` (por defecto **4.000**).
- Con Sonnet 5 (~$3/$15 por 1M) eso da **~$0,05-0,14 por edición**. Multiplica por 4-5
  ediciones/mes. Si añades un *teaser* para la newsletter, es **una llamada más** por envío.

> **Ojo a dos cosas que cambian:** Sonnet 5 tiene **precio introductorio ($2/$10 hasta
> 2026-08-31)**, luego sube; y los **IDs/precenios de modelo caducan** — verifica el vigente.

## 2. El resto del stack (empezar es gratis)

| Pieza | Para qué | Free tier | Cuándo pagarías |
|---|---|---|---|
| **Hosting** (Cloudflare Pages) | Servir tu web estática | Gratis, **permite uso comercial** | Prácticamente nunca para un sitio estático |
| **GitHub** | Guardar el código y automatizar | Repos públicos: Actions gratis ilimitado | Repo privado: 2.000 min/mes gratis, luego se paga |
| **Newsletter** (Resend) | Enviar el boletín | Free para empezar (límite de contactos/envíos) | Al pasar el free (~1.000 contactos) saltas a plan de pago (verifica el vigente) |
| **Dominio** | `tumedio.com` propio | — | **~10–15 USD/año** (gasto real, opcional) |

> ⚠️ **Aviso de hosting si monetizas:** algunos planes gratis **prohíben el uso comercial**
> (afiliados, AdSense, donaciones): **Vercel Hobby** y **GitHub Pages** lo prohíben; en
> Vercel monetizar exige **Pro (~$20/mes)**. **Cloudflare Pages** y **Netlify** sí permiten
> uso comercial en gratis (por eso Cloudflare es el recomendado). Comparativa y guía en
> **[04-DESPLIEGUE.md](04-DESPLIEGUE.md)**; verifica los ToS vigentes antes de elegir.

> **Repo público vs privado:** el público te da Actions gratis ilimitado, pero
> **expone tu config, tus fuentes y tus decisiones editoriales** a cualquiera. El
> privado las protege pero limita los minutos gratis de automatización. Decide según
> cuánto te importe la privacidad de tu "receta".

---

## 3. Tres escenarios reales

**A · Hobby, sin monetizar (lo más común al empezar)**
- IA económica semanal + Cloudflare Pages + GitHub público + sin dominio propio.
- **Coste: ~$0.30–0.75/mes.** Todo lo demás, gratis.

**B · Serio, con dominio y newsletter**
- IA (Sonnet) + Cloudflare Pages + dominio propio + Resend.
- **Coste: ~$0.75/mes + ~$12/año de dominio** (≈ **$1.75/mes** amortizado).

**C · Monetizando (afiliados/AdSense/donaciones)**
- Igual que B, pero **si estás en Vercel** debes pasar a Pro (~$20/mes). En
  **Cloudflare Pages sigue siendo gratis** monetizar.
- **Coste: ~$1.75/mes** en Cloudflare, o **~$21.75/mes** si te empeñas en Vercel.

---

## 4. Sobre ganar dinero (expectativa honesta)

- **La expectativa de ingreso es cercana a cero** al principio. Monta esto porque te
  interesa el tema y quieres un medio propio, no como negocio rápido.
- El kit **no te empuja a afiliados de herramientas caras** (ahí es donde el consejo
  se corrompe). Ver monetización honesta en `08-MODO-INDEPENDIENTE.md` (en construcción).
- El **único gasto inevitable** es la IA (céntimos) y, si lo quieres, el dominio.

---

_Siguiente: [02-CUENTAS-Y-DOMINIO.md](02-CUENTAS-Y-DOMINIO.md) para poner tu medio
online. Anterior: [00-QUICKSTART.md](00-QUICKSTART.md)._
