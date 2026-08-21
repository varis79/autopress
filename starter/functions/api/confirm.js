// GET /api/confirm?token=…  → verifica y da de alta en la audiencia de Resend.
import { verifyToken } from "../_token.js";
import { t } from "../_i18n.js";

export async function onRequestGet({ request, env }) {
  const L = t(env);
  const token = new URL(request.url).searchParams.get("token") || "";
  const email = await verifyToken(token, "confirm", Math.floor(Date.now() / 1000), env.NEWSLETTER_SECRET);
  if (!email) return new Response(L.linkInvalid, { status: 400 });

  const audience = `https://api.resend.com/audiences/${env.RESEND_AUDIENCE_ID}/contacts`;
  const auth = { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" };
  let r = await fetch(audience, {
    method: "POST", headers: auth,
    body: JSON.stringify({ email, unsubscribed: false }),
  });
  // En Resend, POST /contacts NO actualiza un contacto que ya existe (devuelve 409). Quien se
  // dio de baja y vuelve seguiría con unsubscribed:true y NO recibiría correos pese a confirmar.
  // Por eso, en 409, hacemos PATCH para re-suscribirlo de verdad (unsubscribed:false).
  if (r.status === 409) {
    r = await fetch(`${audience}/${encodeURIComponent(email)}`, {
      method: "PATCH", headers: auth,
      body: JSON.stringify({ unsubscribed: false }),
    });
  }
  if (!r.ok) {
    return new Response(L.confirmFailed, { status: 502 });
  }
  return new Response(L.confirmed, {
    status: 200, headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
}
