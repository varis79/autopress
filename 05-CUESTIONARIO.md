# 05 · CUESTIONARIO — define tu medio

> Las preguntas que definen tu medio. Puedes contestarlas aquí (para prepararte) o dejar
> que el **asistente** las haga por ti: `cd starter && PYTHONPATH=. python3 -m scripts.setup`.
> Recuerda: **nada es obligatorio de golpe** — salta lo que no tengas y añádelo luego.

## 1. Identidad
- **Nombre** del medio y **lema** (una frase de qué es).
- **Idioma** de publicación.
- **Huso horario** de referencia (afecta a la agenda de publicación).

## 2. Temática (lo más importante)
- **¿De qué va y qué mirada aporta?** Sé específico (no "tecnología", sino "regulación de
  movilidad eléctrica en México y España").
- **¿Tiene flujo vivo de fuentes?** Debe salir noticia nueva con enlaces cada semana. Si es
  un tema estático/histórico, Autopress **no** es la herramienta (ver `01-ANTES-DE-EMPEZAR.md`).
- **Temas/subtemas** clave y sus palabras clave.
- **Mercados/geografías**: cuáles son primarios y cuáles secundarios.
- **Actores** a seguir (empresas, reguladores).

## 3. Voz
- **Tono**: analítico/sobrio, cercano, técnico… Prioridad al lector externo.

## 4. Gobernanza (cuánta revisión)
- **Perfil de riesgo**: `auto` (publica solo), `review` (abre PR, por defecto), `strict`
  (temas sensibles: corroboración ≥2 fuentes + revisión). Ver `07-GUARDARRAILES.md`.
- **¿Independiente o con patrocinador?** Ver `08-MODO-INDEPENDIENTE.md`.

## 5. Publicación (opcional, se añade luego)
- **¿Dónde publicas?** y **¿monetizas?** (afecta al host — ver `04-DESPLIEGUE.md`).
- **¿Dominio propio?** Si no, usas el subdominio gratis del host.

## 6. Integraciones (opcional)
- **Clave de IA** (sin ella, modo stub). **Newsletter** (Resend) si quieres boletín.

> ¿No sabes qué se puede configurar? Di *"muéstrame los settings"* o corre
> `PYTHONPATH=. python3 -m scripts.settings` — el catálogo completo con dónde vive cada cosa.
