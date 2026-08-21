"""newsletter — tokens firmados (HMAC) para doble opt-in y baja.

El envío de correo (Resend) y el endpoint HTTP son específicos del host; lo que vive
aquí es la LÓGICA DE SEGURIDAD, reproducible y testeable: firmar y verificar tokens para
que **nadie pueda dar de alta/baja a terceros** en la LISTA ni falsificar una confirmación.

Alcance honesto: el token EVITA meter/sacar a terceros de la audiencia, pero por sí solo
NO frena el *email-bombing* (mandar confirmaciones a direcciones ajenas): eso lo cierran el
rate-limit + Turnstile del endpoint (`functions/api/subscribe.js`). Además el `<email>` va
firmado pero en **base64 (no cifrado)** dentro del token, así que puede quedar en logs del
host o en cabeceras Referer (ver `legal/privacidad.md`).

Token = base64url(payload) + "." + base64url(hmac_sha256(secret, payload))
payload = "<action>:<email>:<exp_epoch>"

La clave sale de `NEWSLETTER_SECRET` (entorno). `exp`/`now` se pasan explícitos para que
los tests sean deterministas; en producción el handler usa `time.time()`.
"""
from __future__ import annotations
import base64
import hashlib
import hmac
import os

CONFIRM = "confirm"
UNSUBSCRIBE = "unsubscribe"
DEFAULT_TTL = 60 * 60 * 48   # 48 h para confirmar el alta


def _secret(secret: str = None) -> bytes:
    s = secret or os.environ.get("NEWSLETTER_SECRET", "")
    if not s:
        raise RuntimeError("Falta NEWSLETTER_SECRET en el entorno")
    return s.encode("utf-8")


def _b64(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _unb64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def _norm(email: str) -> str:
    return (email or "").strip().lower()


def make_token(action: str, email: str, exp: int, secret: str = None) -> str:
    """Firma un token para `action` (confirm|unsubscribe) sobre `email`, válido hasta `exp`."""
    payload = f"{action}:{_norm(email)}:{int(exp)}".encode("utf-8")
    sig = hmac.new(_secret(secret), payload, hashlib.sha256).digest()
    return _b64(payload) + "." + _b64(sig)


def verify_token(token: str, expected_action: str, now: int, secret: str = None):
    """Devuelve el email si el token es válido (firma correcta, acción esperada, no
    expirado); si no, None. Comparación en tiempo constante."""
    try:
        p_b64, s_b64 = token.split(".", 1)
        payload, sig = _unb64(p_b64), _unb64(s_b64)
    except Exception:
        return None
    expected = hmac.new(_secret(secret), payload, hashlib.sha256).digest()
    if not hmac.compare_digest(sig, expected):
        return None
    try:
        action, email, exp = payload.decode("utf-8").split(":")
    except Exception:
        return None
    if action != expected_action or int(exp) < int(now):
        return None
    return email
