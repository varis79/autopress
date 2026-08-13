# 08 · MODO INDEPENDIENTE Y MONETIZACIÓN (honesto)

> El caso base es **independiente**. La monetización es opcional y aquí va sin humo: la
> expectativa de ingreso es **cercana a cero** al principio. Móntalo porque te importa el
> tema, no como negocio rápido.

## Independiente (por defecto)

- `editorial.mode = independent`. Sin patrocinador, sin conflictos. Máxima credibilidad.
- Es lo recomendado para empezar y para temas sensibles.

## Con patrocinador (opcional)

- `editorial.mode = sponsored` + `sponsorship`. Si aceptas patrocinio, **decláralo siempre**
  de forma visible (no "publirreportaje disfrazado"): Google News y la ética editorial lo
  exigen. Identifica patrocinador y criterio de selección.

## Vías de monetización (y su letra pequeña)

| Vía | Realidad |
|---|---|
| **Afiliados** | El kit **no** te empuja a afiliados de herramientas caras (ahí el consejo se corrompe). Único limpio: el **dominio**. Declara siempre los enlaces afiliados. |
| **AdSense / display** | Posible cuando tengas tráfico real. Ojo al **host**: monetizar exige free tier comercial (Cloudflare/Netlify sí; Vercel Hobby y GitHub Pages **no**). |
| **Donaciones** | Ko-fi / GitHub Sponsors. También cuenta como "uso comercial" en algunos hosts. |
| **Suscripción/premium** | Más adelante; requiere más infraestructura. |

## El landmine del host (repetido porque importa)

Si vas a monetizar, revisa `04-DESPLIEGUE.md`: **Vercel Hobby y GitHub Pages prohíben uso
comercial** en su plan gratis. Cloudflare Pages y Netlify lo permiten. El agente verifica los
ToS vigentes al construir.

## Regla de oro

La credibilidad es el activo. Antes de monetizar, ten un medio que la gente quiera leer. La
monetización que sacrifica la confianza no vale la pena.
