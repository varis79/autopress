// POST /api/subscribe  { email, cf-turnstile-response? }  → envía email de confirmación (doble opt-in).
// Variables de entorno (Cloudflare Pages → Settings → Environment variables):
//   NEWSLETTER_SECRET, RESEND_API_KEY, NEWSLETTER_FROM, SITE_URL
//   TURNSTILE_SECRET_KEY  (opcional pero MUY recomendado: anti-bot real; ver 04-DESPLIEGUE)
//   SUBS_KV               (opcional: binding KV para rate-limit por IP)
import { makeToken } from "../_token.js";
import { t } from "../_i18n.js";

// Verifica el token de Cloudflare Turnstile server-side. Sin esto, un tercero podría
// automatizar POSTs y hacer que tu dominio envíe correos de confirmación no solicitados
// (email-bombing), quemando tu cuota de Resend y tu reputación de envío.
async function verifyTurnstile(token, secret, ip) {
  const body = new URLSearchParams({ secret, response: token || "" });
  if (ip) body.set("remoteip", ip);
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST", body,
  });
  const data = await r.json().catch(() => ({ success: false }));
  return !!data.success;
}

// Rate-limit por IP usando KV (si está enlazado). Degrada a "sin límite" si no hay KV.
async function rateLimited(kv, ip, max = 5, windowSec = 3600) {
  if (!kv || !ip) return false;
  const key = `sub:${ip}`;
  const n = parseInt((await kv.get(key)) || "0", 10) + 1;
  await kv.put(key, String(n), { expirationTtl: windowSec });
  return n > max;
}

export async function onRequestPost({ request, env }) {
  const L = t(env);
  const ip = request.headers.get("CF-Connecting-IP") || "";

  // Capa 1 — gate de origen: un POST legítimo del formulario trae Origin = tu sitio. Rechaza
  // los que traen un Origin distinto (bots cross-site). Solo cuando SITE_URL y Origin existen,
  // para no romper clientes que no envían la cabecera.
  if (env.SITE_URL) {
    const origin = request.headers.get("Origin") || "";
    let allowed = "";
    try { allowed = new URL(env.SITE_URL).origin; } catch (e) { allowed = ""; }
    if (allowed && origin && origin !== allowed) {
      return new Response(L.botFailed, { status: 403 });
    }
  }

  const form = await request.formData().catch(() => null);

  // Capa 2 — honeypot: campo oculto que un humano nunca rellena. Si viene con valor es un bot:
  // fingimos éxito (no enviamos nada) para no darle pistas.
  if ((form?.get("website") || "").toString().trim()) {
    return new Response(L.checkInbox, { status: 200 });
  }

  const email = (form?.get("email") || "").toString().trim().toLowerCase();
  if (!email || !email.includes("@")) {
    return new Response(L.invalidEmail, { status: 400 });
  }

  // Capa 3 — rate-limit por IP (si hay KV): frena el bombardeo aunque no haya Turnstile.
  if (await rateLimited(env.SUBS_KV, ip)) {
    return new Response(L.tooMany, { status: 429 });
  }

  // Capa 4 — anti-bot: si configuraste Turnstile, EXÍGELO (cierra el email-bombing a terceros).
  if (env.TURNSTILE_SECRET_KEY) {
    const tsToken = (form?.get("cf-turnstile-response") || "").toString();
    if (!(await verifyTurnstile(tsToken, env.TURNSTILE_SECRET_KEY, ip))) {
      return new Response(L.botFailed, { status: 403 });
    }
  }

  const exp = Math.floor(Date.now() / 1000) + 60 * 60 * 48; // 48 h para confirmar
  const token = await makeToken("confirm", email, exp, env.NEWSLETTER_SECRET);
  const link = `${env.SITE_URL}/api/confirm?token=${encodeURIComponent(token)}`;

  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: env.NEWSLETTER_FROM,
      to: [email],
      subject: L.subject,
      html: L.emailHtml(link),
    }),
  });
  if (!r.ok) return new Response(L.sendFailed, { status: 502 });
  return new Response(L.checkInbox, { status: 200 });
}
