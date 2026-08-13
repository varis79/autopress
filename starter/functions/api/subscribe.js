// POST /api/subscribe  { email }  → envía email de confirmación (doble opt-in).
// Variables de entorno (Cloudflare Pages → Settings → Environment variables):
//   NEWSLETTER_SECRET, RESEND_API_KEY, NEWSLETTER_FROM, SITE_URL
import { makeToken } from "../_token.js";

export async function onRequestPost({ request, env }) {
  const form = await request.formData().catch(() => null);
  const email = (form?.get("email") || "").toString().trim().toLowerCase();
  if (!email || !email.includes("@")) {
    return new Response("Introduce un email válido.", { status: 400 });
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
      subject: "Confirma tu suscripción",
      html: `<p>Gracias por suscribirte. <strong>Confirma</strong> tu suscripción:</p>
             <p><a href="${link}">Confirmar suscripción</a></p>
             <p>Si no fuiste tú, ignora este correo.</p>`,
    }),
  });
  if (!r.ok) return new Response("No se pudo enviar el correo. Inténtalo más tarde.", { status: 502 });
  return new Response("Revisa tu correo para confirmar la suscripción.", { status: 200 });
}
