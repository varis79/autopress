# newsletter/ — double opt-in and safe unsubscribe

The site is static, so the newsletter needs **3 endpoints** (a serverless
function) that your host runs. The **security logic** (signed tokens) is already in
[`scripts/newsletter.py`](../scripts/newsletter.py) and **is tested**
([`tests/test_newsletter.py`](../tests/test_newsletter.py)); here's how to wire it up.

## The flow (double opt-in + signed unsubscribe)

```
[Form del sitio] --POST /api/subscribe { email }-->  genera token(confirm,email,+48h)
                                                     y envía email con enlace de confirmación
[Usuario clica] --GET /api/confirm?token=...------>  verifica token → alta en Resend
[Cada correo]   pie con --GET /api/unsubscribe?token=...-> verifica token → baja en Resend
```

- **No one can subscribe/unsubscribe third parties:** each link carries an **HMAC token** that
  contains the email + an expiry, signed with `NEWSLETTER_SECRET`. Without the key it can't
  be forged (this prevents *subscription bombing* and the classic tamperable `?email=`).
- **Double opt-in:** a subscription doesn't count until the user confirms from their inbox.

## Environment variables

| Variable | What for |
|---|---|
| `RESEND_API_KEY` | Send emails and manage the audience |
| `RESEND_AUDIENCE_ID` | The list where people subscribe/unsubscribe |
| `NEWSLETTER_SECRET` | Sign/verify the tokens (long and random; `openssl rand -hex 32`) |

## Reference handler (Python; port the SAME scheme if your host uses JS)

```python
import time, urllib.request, json, os
from scripts.newsletter import make_token, verify_token, CONFIRM, UNSUBSCRIBE, DEFAULT_TTL

SITE = os.environ["SITE_URL"]  # p. ej. https://tumedio.com

def on_subscribe(email):
    token = make_token(CONFIRM, email, int(time.time()) + DEFAULT_TTL)
    link = f"{SITE}/api/confirm?token={token}"
    _resend_email(email, "Confirma tu suscripción", f"Confirma aquí: {link}")
    return "Revisa tu correo para confirmar."

def on_confirm(token):
    email = verify_token(token, CONFIRM, int(time.time()))
    if not email: return 400, "Enlace inválido o caducado"
    _resend_contact_add(email)                 # alta en la audiencia
    return 200, "¡Suscripción confirmada!"

def on_unsubscribe(token):
    email = verify_token(token, UNSUBSCRIBE, int(time.time()))
    if not email: return 400, "Enlace inválido"
    _resend_contact_remove(email)
    return 200, "Te has dado de baja."
```

Every email you send must include the unsubscribe link in its footer with
`make_token(UNSUBSCRIBE, email, exp_lejano)`.

## Deploying the endpoint (depending on your host)

- **Cloudflare** → a *Worker* or *Pages Function* at `/api/*`.
- **Netlify** → a *Netlify Function*.
- **Vercel** → a *Serverless Function* at `/api/*` (remember: Hobby is non-commercial).

Set `RESEND_API_KEY`, `RESEND_AUDIENCE_ID` and `NEWSLETTER_SECRET` in the host's
*secrets/env*. **If your function is JS**, replicate the HMAC-SHA256 token with the same format
(`base64url(payload) + "." + base64url(hmac(secret, payload))`, `payload =
"action:email:exp"`) so it's compatible with `scripts/newsletter.py`.

> Legal framework (privacy, double opt-in depending on jurisdiction): see
> [`legal/privacidad.md`](../legal/privacidad.md) and
> [`../02-CUENTAS-Y-DOMINIO.md`](../../02-CUENTAS-Y-DOMINIO.md).
