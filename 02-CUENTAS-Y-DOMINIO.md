# 02 · CUENTAS Y DOMINIO — poner tu medio online

> **Cuándo necesitas esto:** solo cuando quieras **publicar en internet** y/o
> **enviar newsletter**. Para probar en local (el [00-QUICKSTART](00-QUICKSTART.md))
> no hace falta ninguna cuenta.
>
> Es la parte más "de fontanería" del proyecto. Ve despacio, por checkpoints, y deja
> que el agente ejecute los pasos técnicos. Costes: ver [03-COSTES.md](03-COSTES.md).

---

## Checklist de cuentas (en orden)

| # | Cuenta | Para qué | ¿Obligatoria? |
|---|---|---|---|
| 1 | **GitHub** | Guardar el código y **automatizar** la edición semanal | Sí, para publicar |
| 2 | **Cloudflare Pages** | Servir tu web (host **por defecto**, gratis, permite monetizar) | Sí, para publicar |
| 3 | **Clave de IA** | Redactar la edición (ya en el quickstart) | Sí, para redacción real |
| 4 | **Resend** | Enviar la newsletter | Opcional |
| 5 | **Dominio** | Tener `tumedio.com` propio | Opcional (~10–15 USD/año) |

> **Recuerda el aviso de hosting:** el plan gratis de **Vercel prohíbe uso comercial**
> (afiliados, AdSense, donaciones). Por eso el default es **Cloudflare Pages**. Ver
> [03-COSTES.md](03-COSTES.md).

---

## Paso 1 · GitHub (código + automatización)

1. Crea una cuenta en github.com (gratis).
2. Sube tu proyecto (el agente lo hace con `git`). 
3. **Decisión — repo público o privado:**
   - **Público:** automatización (GitHub Actions) **gratis e ilimitada**, pero
     **cualquiera ve tu config, tus fuentes y tus decisiones editoriales**.
   - **Privado:** protege tu "receta", pero los minutos de Actions gratis son
     limitados (2.000/mes).
   Elige según cuánto te importe la privacidad. Puedes cambiar después.

**✅ Checkpoint:** tu proyecto aparece en tu GitHub.

---

## Paso 2 · Elige host y publica

Tu sitio es **estático y portable** (`site/`): se sube a cualquier host. Tienes la
comparativa y las mini-guías (Cloudflare, Netlify, GitHub Pages, Vercel) en
**[04-DESPLIEGUE.md](04-DESPLIEGUE.md)**. Recomendado para empezar: **Cloudflare Pages**
(gratis, permite monetizar, dominio propio gratis).

En casi todos, el patrón es: **conectas tu repo** y el host publica solo la carpeta de
salida (`site/`).

**✅ Checkpoint:** el host te da una URL con tu sitio (p. ej. `tumedio.pages.dev`).
**🔧 Si no aparece:** revisa que la carpeta de salida publicada sea la del sitio generado.

---

## Paso 3 · Dominio propio (opcional)

1. Compra el dominio en cualquier registrador (son intercambiables). Coste típico
   **~10–15 USD/año**.
2. Apúntalo a Cloudflare Pages (en Pages → Custom domains → añades tu dominio;
   Cloudflare te indica los registros DNS a crear).

**✅ Checkpoint:** `https://tumedio.com` carga tu sitio (puede tardar minutos en
propagar el DNS).

---

## Paso 4 · Newsletter y correo que NO cae en spam (SPF · DKIM · DMARC)

Si envías boletín, tu dominio tiene que **demostrar** que ese correo es legítimo. Sin
esto, tus emails caen en spam o los rechazan. Son **tres registros DNS** que añades una
vez. Resend (u otro proveedor) te da los valores exactos; tú los pegas en tu DNS
(Cloudflare). El agente te guía.

| Registro | Qué dice | Cómo se pone |
|---|---|---|
| **SPF** | "Estos servidores pueden enviar correo en mi nombre" | Un registro TXT que autoriza a tu proveedor (Resend) |
| **DKIM** | "Este correo va firmado y no se ha manipulado" | Registros (CNAME/TXT) con la clave que te da el proveedor |
| **DMARC** | "Si un correo no pasa SPF/DKIM, haz esto" | Un TXT en `_dmarc.tudominio.com` |

**Recomendación para DMARC:** empieza en modo observación y endurece después:
1. `p=none` (solo monitoriza, no bloquea) las primeras semanas.
2. Cuando veas que tu correo legítimo pasa, sube a `p=quarantine` y luego `p=reject`.

**✅ Checkpoint:** en el panel de Resend tu dominio figura como **"verified"** y un
**envío de prueba** te llega a la bandeja de entrada (no a spam).
**🔧 Si cae en spam:** casi siempre falta uno de los tres registros o hay una errata al
copiarlo. Revísalos con el agente.

> **Doble opt-in y baja (matiz legal, importante):** "por ley" sería demasiado absoluto —
> en la UE (RGPD/ePrivacy) el marketing exige **consentimiento previo** (con matices), y en
> EE. UU. CAN-SPAM funciona sobre todo con **opt-out**. Como default prudente que cumple en
> la práctica casi en todas partes, el kit usa **doble opt-in** (email de confirmación) y
> **baja de un clic con token firmado (HMAC del email + clave secreta)** en el enlace — así
> nadie puede dar de baja a terceros ni inundarte de altas falsas (*subscription bombing*).
> Se monta en la fase de newsletter (D); aquí solo dejamos el correo bien autenticado.

---

## Regla de seguridad (para todas las cuentas)

- **Los secretos (claves API, tokens) NUNCA van en el repo.** Van en `.env` (local,
  ignorado por git) y en los **"secrets" de GitHub Actions** / variables de entorno del
  host (producción).
- Si una clave se te cuela en el repo, **revócala y genera otra**. Considérala quemada.

---

_Siguiente: entender el gasto en [03-COSTES.md](03-COSTES.md), o cómo funciona por
dentro en [starter/README.md](starter/README.md). Anterior:
[00-QUICKSTART.md](00-QUICKSTART.md)._
