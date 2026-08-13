# newsletter/ — doble opt-in y baja (LLAVE EN MANO)

Las funciones ya están escritas en **`functions/api/`** (Cloudflare Pages Functions):
`subscribe.js` (alta con confirmación), `confirm.js` (alta en Resend) y `unsubscribe.js`
(baja). Usan tokens firmados HMAC (mismo formato que `scripts/newsletter.py`, ya testeado).
**Tú solo activas la newsletter y pegas tus claves.** El formulario del sitio ya apunta a
`/api/subscribe`.

## Puesta en marcha (para no técnicos)

1. **Activa la newsletter** en tu config: `"newsletter": { "enabled": true }`.
2. **Crea una cuenta en Resend** → https://resend.com (gratis para empezar).
   - **Verifica tu dominio** (Domains → Add domain; añade los registros DNS que te da).
   - Crea una **Audience** (Audiences) → copia su **ID**.
   - Saca una **API key** (API Keys → Create).
3. **Pon las variables** en Cloudflare Pages (tu proyecto → Settings → Environment variables):
   | Variable | Qué es | De dónde |
   |---|---|---|
   | `RESEND_API_KEY` | Clave de Resend | Resend → API Keys |
   | `RESEND_AUDIENCE_ID` | Tu lista | Resend → Audiences |
   | `NEWSLETTER_SECRET` | Firma los enlaces (larga y aleatoria) | genera una: `openssl rand -hex 32` |
   | `NEWSLETTER_FROM` | Remitente, p. ej. `Boletín <hola@tudominio.com>` | tu dominio verificado |
   | `SITE_URL` | La URL de tu sitio, p. ej. `https://tudominio.com` | tu dominio |
4. **Redespliega**. Listo: el formulario ya funciona (alta → email de confirmación → clic →
   suscrito).

## Enviar el boletín cada semana
Dos opciones:
- **Fácil**: usa **Resend → Broadcasts** (interfaz) para enviar la edición a tu Audience; Resend
  gestiona la baja.
- **Con tu enlace de baja**: al enviar, incluye en el pie un enlace
  `/api/unsubscribe?token=…` generado con `scripts/newsletter.py` (`make_token("unsubscribe", email, exp)`).

> **Otros hosts**: si usas Netlify/Vercel en vez de Cloudflare, la lógica es idéntica; copia
> las 3 funciones a `netlify/functions/` o `api/` y ajusta la firma del handler. El token
> (`functions/_token.js`) es Web Crypto estándar y funciona igual.

Marco legal (privacidad, consentimiento): ver [`../legal/`](../legal/) y
[`../../02-CUENTAS-Y-DOMINIO.md`](../../02-CUENTAS-Y-DOMINIO.md).
