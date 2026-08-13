// GET /api/unsubscribe?token=…  → verifica y marca la baja en Resend (suppression, no borra).
// El enlace con token va en el pie de cada envío (lo genera quien manda el boletín).
import { verifyToken } from "../_token.js";

export async function onRequestGet({ request, env }) {
  const token = new URL(request.url).searchParams.get("token") || "";
  const email = await verifyToken(token, "unsubscribe", Math.floor(Date.now() / 1000), env.NEWSLETTER_SECRET);
  if (!email) return new Response("Enlace inválido.", { status: 400 });

  const r = await fetch(
    `https://api.resend.com/audiences/${env.RESEND_AUDIENCE_ID}/contacts/${encodeURIComponent(email)}`,
    {
      method: "PATCH",
      headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({ unsubscribed: true }),
    }
  );
  if (!r.ok) return new Response("No se pudo procesar la baja. Escríbenos y lo hacemos.", { status: 502 });
  return new Response("Te has dado de baja. Ya no recibirás el boletín.", {
    status: 200, headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
}
