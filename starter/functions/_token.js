// Token firmado (HMAC-SHA256) — MISMO formato que scripts/newsletter.py, para doble opt-in
// y baja segura. payload = "accion:email:exp".  token = base64url(payload) + "." + base64url(firma)
const enc = new TextEncoder();

function b64url(bytes) {
  let s = btoa(String.fromCharCode(...new Uint8Array(bytes)));
  return s.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
function unb64url(s) {
  s = s.replace(/-/g, "+").replace(/_/g, "/");
  s += "=".repeat((4 - (s.length % 4)) % 4);
  const bin = atob(s);
  return Uint8Array.from(bin, (c) => c.charCodeAt(0));
}
async function _key(secret) {
  return crypto.subtle.importKey("raw", enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign", "verify"]);
}

export async function makeToken(action, email, exp, secret) {
  const payload = `${action}:${email.trim().toLowerCase()}:${exp}`;
  const sig = await crypto.subtle.sign("HMAC", await _key(secret), enc.encode(payload));
  return b64url(enc.encode(payload)) + "." + b64url(sig);
}

export async function verifyToken(token, expectedAction, now, secret) {
  try {
    const [p, s] = token.split(".");
    const payloadBytes = unb64url(p);
    const ok = await crypto.subtle.verify("HMAC", await _key(secret), unb64url(s), payloadBytes);
    if (!ok) return null;
    const [action, email, exp] = new TextDecoder().decode(payloadBytes).split(":");
    if (action !== expectedAction || Number(exp) < now) return null;
    return email;
  } catch (e) {
    return null;
  }
}
