// GET /api/confirm?token=…  → verifica y da de alta en la audiencia de Resend.
import { verifyToken } from "../_token.js";

export async function onRequestGet({ request, env }) {
  const token = new URL(request.url).searchParams.get("token") || "";
  const email = await verifyToken(token, "confirm", Math.floor(Date.now() / 1000), env.NEWSLETTER_SECRET);
  if (!email) return new Response("Enlace inválido o caducado.", { status: 400 });

  const r = await fetch(`https://api.resend.com/audiences/${env.RESEND_AUDIENCE_ID}/contacts`, {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ email, unsubscribed: false }),
  });
  // 200/201 = creado; 409 = ya existía → también es "confirmado".
  if (!r.ok && r.status !== 409) {
    return new Response("No se pudo completar el alta. Inténtalo más tarde.", { status: 502 });
  }
  return new Response("¡Suscripción confirmada! Gracias por unirte.", {
    status: 200, headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
}
