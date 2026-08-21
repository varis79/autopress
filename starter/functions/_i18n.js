// Textos del boletín por idioma. Idioma vía env NEWSLETTER_LANG ("es" | "en"; por defecto "es")
// para que un medio anglófono no envíe correos en español. Usado por functions/api/*.js.
const STRINGS = {
  es: {
    invalidEmail: "Introduce un email válido.",
    tooMany: "Demasiados intentos. Prueba más tarde.",
    botFailed: "Verificación anti-bot fallida. Recarga e inténtalo de nuevo.",
    sendFailed: "No se pudo enviar el correo. Inténtalo más tarde.",
    checkInbox: "Revisa tu correo para confirmar la suscripción.",
    subject: "Confirma tu suscripción",
    emailHtml: (link) =>
      `<p>Gracias por suscribirte. <strong>Confirma</strong> tu suscripción:</p>
       <p><a href="${link}">Confirmar suscripción</a></p>
       <p>Si no fuiste tú, ignora este correo.</p>`,
    linkInvalid: "Enlace inválido o caducado.",
    confirmFailed: "No se pudo completar el alta. Inténtalo más tarde.",
    confirmed: "¡Suscripción confirmada! Gracias por unirte.",
    unsubFailed: "No se pudo procesar la baja. Escríbenos y lo hacemos.",
    unsubbed: "Te has dado de baja. Ya no recibirás el boletín.",
  },
  en: {
    invalidEmail: "Enter a valid email.",
    tooMany: "Too many attempts. Try again later.",
    botFailed: "Anti-bot check failed. Reload and try again.",
    sendFailed: "Couldn't send the email. Try again later.",
    checkInbox: "Check your inbox to confirm your subscription.",
    subject: "Confirm your subscription",
    emailHtml: (link) =>
      `<p>Thanks for subscribing. <strong>Confirm</strong> your subscription:</p>
       <p><a href="${link}">Confirm subscription</a></p>
       <p>If this wasn't you, ignore this email.</p>`,
    linkInvalid: "Invalid or expired link.",
    confirmFailed: "Couldn't complete the signup. Try again later.",
    confirmed: "Subscription confirmed! Thanks for joining.",
    unsubFailed: "Couldn't process the unsubscribe. Email us and we'll do it.",
    unsubbed: "You've unsubscribed. You won't receive the newsletter anymore.",
  },
};

export function t(env) {
  const lang = ((env && env.NEWSLETTER_LANG) || "es").toString().toLowerCase().slice(0, 2);
  return STRINGS[lang] || STRINGS.es;
}
