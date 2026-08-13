# Kit "Medio Autónomo" v2 — Decisiones y plan de construcción

> Documento de trabajo. Consolida las decisiones tomadas, la capa factual **verificada**
> (afiliados, coste, hosting) y el plan de estructura, para construir el kit público
> gratuito derivado de `BLUEPRINT-MEDIO-AUTONOMO.md`. Sirve de base única para la
> construcción y para que revisores externos partan de hechos, no de suposiciones.
>
> **Fecha de verificación de datos:** 2026-08 (afiliados, precios de modelo, ToS de host
> cambian — re-verificar antes de publicar).

---

## 0. Qué es el kit y para quién

Un **kit descargable y gratuito** ("hazte tu propio medio autónomo") que se publica en la
web personal del autor, en **español e inglés**. Estrella polar: **una persona sin
conocimientos técnicos, con ayuda de un agente de IA, monta su propio medio de noticias
curadas de su temática, gastando poco o nada.**

Se entrega como **repo plantilla de GitHub ("Use this template") + ZIP** con estructura ya
montada y un `AGENTS.md` que orienta al agente. El que lo recibe lo abre con su agente y
arranca.

---

## 1. Decisiones tomadas (bloqueadas)

### D1 — SEO: reglas correctas siempre; no inundar Google; calidad-gate por defecto

- El kit **siempre** enseña SEO técnico correcto (schema, sitemap, interlinking, frescura,
  metadatos). Eso es núcleo.
- **La generación masiva de páginas pilar con LLM es OPT-IN y está OFF por defecto.** No es
  obligatoria ni el camino principal.
- **Por defecto, a Google solo se liberan (index) las páginas que superan un umbral de
  calidad y valor real.** Todo lo demás nace `noindex` y solo se libera si cumple.
- El operador **elige** si quiere escalar en volumen, pero el kit lo desaconseja como
  primer paso y advierte del riesgo (contenido a escala = política antispam de Google;
  medios basura; el nombre del autor encima del manual).
- **Umbral de calidad (definir como checklist verificable):** contenido único ≥30%, sin
  cifras inventadas de empresas privadas (hook que falla el build), ≥3 enlaces internos
  entrantes / ≥5 salientes, intro redactable con criterio, aporta algo que no está en otra
  página, no *thin*. Solo al pasar TODO → entra al sitemap/index.
- **Núcleo del kit = "publica una revista/newsletter semanal decente".** Eso ya es un
  producto completo sin tocar SEO masivo.

### D2 — Caso base: el exigente, pero genérico (sin temática fija)

- El kit se escribe asumiendo por defecto **el caso difícil**: temas que pueden ser
  sensibles, **sin patrocinador**, con **opción de revisión humana**. Los guardarraíles
  quedan en el **núcleo**, no en un anexo (si van como anexo, se ignoran).
- **Pero NO se centra en ninguna temática concreta** (ni geopolítica ni flotas). Todo es
  parametrizable vía el cuestionario de arranque. La temática del autor (geopolítica) va
  como **ejemplo trabajado aparte**, no como el eje del kit.
- El **caso fácil** (B2B con patrocinador y producto) se **deriva** relajando reglas
  (activar sección de marca, CTA, blacklist de competidores), no al revés.

### D3 — Hosting: default a host comercial-friendly

- **Default recomendado: Cloudflare Pages** (u otro cuyo free tier permita uso comercial).
- **Vercel** se menciona como opción válida **con el aviso**: su plan gratuito (Hobby)
  **prohíbe uso comercial** — y su definición incluye afiliados como propósito principal,
  AdSense y pedir donaciones. Al monetizar, hay que pasar a **Vercel Pro (~$20/mes)**.
- El kit sigue siendo **100% gratis** para quien aún no monetiza, en cualquier host.

---

## 2. Capa factual verificada (no re-derivar)

### 2.1 Afiliados — recomendación: casi no ponerlos, y decirlo

| Servicio | ¿Afiliado real? | Paga | Uso en el kit |
|---|---|---|---|
| **Anthropic (API)** | Referral enterprise (B2B) + guest passes de Claude Code (crédito, no cash) | Crédito | No sirve para lectores; el de crédito solo abarata al autor, marginal |
| **Vercel** | Aparentemente sí (existe `/legal/affiliate-marketing-terms`; trackers citan 20% recurrente, cookie 90d) | Cash | ⚠️ chocaría con su prohibición de uso comercial en Hobby — no promover |
| **Resend** | **No** | — | — |
| **Beehiiv** | Sí — ~50% durante 12 meses, recurrente, cookie 60d | Cash | Único con sentido: recomendar como alternativa *mejor* para no-técnicos |
| **Kit/ConvertKit** | Sí — 50% 12 meses + 10-20% recurrente después | Cash | Ídem, alternativa |
| **Namecheap (dominio)** | Sí — 25-38% en dominios (~$1-3/venta) | Cash | El más limpio: gasto inevitable, registradores intercambiables |

**Regla del kit:** el núcleo del stack es gratis y no paga afiliación; donde pagan bien
(herramientas SEO de $99/mes) es donde el consejo se corrompe. Únicos afiliados éticos:
**dominio (Namecheap)** y **plataforma de newsletter alternativa (Beehiiv/Kit)** — pero con
el default gratis (Resend/Cloudflare) recomendado *antes* de mirar quién paga, siempre
declarado, y con un enlace sin afiliación al lado. Expectativa de ingreso: cercana a cero.
El retorno del kit es **reputacional**.

### 2.2 Coste real por edición (precios verificados 2026-06)

Una edición ≈ 1 llamada al LLM (~12k tokens entrada / ~7k salida):

| Modelo | $/1M in · out | Coste/edición | Coste/mes (semanal + teaser) |
|---|---|---|---|
| Haiku 4.5 | $1 / $5 | ~$0.05 | **~$0.30** |
| Sonnet 5 | $3 / $15 | ~$0.14 | **~$0.73** |
| Opus 5 | $5 / $25 | ~$0.24 | **~$1.20** |

**Un medio semanal cuesta menos que un café al mes.** Los multiplicadores de coste son:
(a) **búsqueda web en compose** si se añade, y **(b) generación masiva de páginas SEO**
(cientos de páginas escritas por LLM) — razón independiente para dejar el SEO masivo
opt-in (D1). El kit debe traer una **sección de costes** con estos números, los free tiers,
y los puntos de ruptura.

### 2.3 Landmine de hosting (crítico)

**Vercel Hobby (free) prohíbe uso comercial**, definición incluida: afiliados como
propósito principal, AdSense, donaciones, ser pagado por construir. → resuelto por D3
(default Cloudflare Pages). **Verificar la ToS vigente de Vercel y de Cloudflare Pages antes
de publicar el kit.**

### 2.4 Otros hechos a documentar

- **Actions gratis con minutos generosos, pero repos privados solo 2.000 min/mes**; los
  repos **públicos** son gratis ilimitados **pero exponen tu config, fuentes y decisiones
  editoriales**. El kit debe advertirlo y dejar elegir.
- **SPF/DKIM/DMARC** no es trivial para un no-técnico: merece su propia guía paso a paso.
- Los **IDs de modelo y las APIs caducan**: el kit necesita fecha de "última verificación"
  y un `CHANGELOG`.

---

## 3. Huecos del blueprint actual que estas decisiones obligan a cerrar

Del análisis de revisión (consolidado), lo que toca por las decisiones D1-D3:

| # | Hueco | Acción por las decisiones |
|---|---|---|
| G-fuente | `stories[]` **no tiene `source_name`/`source_url`** | **Crítico.** Añadir campos de fuente al esquema y a las reglas de oro. Un medio que no enlaza al original es un scraper con buena tipografía. |
| G-derechos | Nada sobre derechos del material RSS (cuánto tomar, atribución, feeds no-comerciales, Google News) | Sección legal obligatoria en el kit |
| G-IA | No se declara que el contenido lo escribe una IA | Añadir a legal + `author` del schema + footer (transparencia UE) |
| G-correcciones | No hay política/mecanismo de correcciones | Barato con Git; incluir plantilla y política |
| G-doble-optin | Alta directa `unsubscribed:false` | Ofrecer doble opt-in confirmado como default prudente (UE); baja con token firmado, no email en URL |
| G-inyección | Texto de RSS (no confiable) entra al LLM sin mitigación | Delimitadores + instrucción + sanitización + check de QA |
| G-fetch | El LLM redacta sobre el resumen del RSS, no el texto completo | Ofrecer fetch del texto de los N seleccionados (respetando robots.txt) como mejora |
| G-QA-editorial | QA valida estructura, no correspondencia con fuentes | Check determinista: entidades/cifras del output deben aparecer en el input |
| G-neutralidad | Cero gestión de sesgo/fuentes/verificación | **Núcleo** (D2): niveles de fuente, corroboración ≥2 fuentes en temas contestados, ventana de enfriamiento, atribución de acusaciones, cifras con rango+fuente |
| G-sin-patrocinador | `<MARCA>`/`<BLACKLIST>`/cuotas mueren sin patrocinador | Modo independiente por defecto (D2): qué se apaga, qué se sustituye, monetización |
| G-perfil-riesgo | Auto-merge sin revisión como único modo | **Tres perfiles**: `auto` (nichos inocuos), `review` (default del kit), `strict` (sensibles: revisión + doble fuente + enfriamiento). QA configurable por perfil |

---

## 4. Estructura de entrega propuesta (ZIP / repo plantilla)

Romper el MD único en un kit navegable. Estructura base (ajustada a D1-D3):

```
autopress/  (medio-autonomo-kit)
├── README.md                    Qué es, para quién NO es, expectativas honestas, licencia
├── 00-QUICKSTART.md             ~90 min: edición en local (modo stub) + primer deploy
├── 01-ANTES-DE-EMPEZAR.md       ¿Es para ti? Alternativas honestas (Ghost/Substack/Beehiiv)
├── 02-CUENTAS-Y-DOMINIO.md      Checklist: GitHub, host (Cloudflare Pages default), Resend,
│                                Cloudflare, DNS, SPF/DKIM/DMARC, facturación API
├── 03-COSTES.md                 Tabla real (§2.2) + free tiers + puntos de ruptura + 3 escenarios
├── 04-BLUEPRINT.md              El blueprint actual, depurado, genérico (destino: el agente)
├── 05-CUESTIONARIO.md           Intake ampliado: + perfil de riesgo, + modo patrocinio/independiente,
│                                + idioma, + política de fuentes
├── 06-ADAPTACION-TEMATICA.md    Playbooks genéricos: B2B nicho · ciencia · local · sensibles
├── 07-GUARDARRAILES.md          Estándares editoriales (NÚCLEO): niveles de fuente,
│                                corroboración, correcciones, declaración de IA, difamación,
│                                inyección de prompt, verificación determinista
├── 08-MODO-INDEPENDIENTE.md     Sin patrocinador: qué se apaga/sustituye + monetización
│                                (afiliados §2.1 · AdSense/donaciones + landmine host D3)
├── 09-OPERACION.md              Runbook semanal, fallos frecuentes, primeros 90 días, cuándo abandonar
├── 10-SEO.md                    SEO correcto SIEMPRE; masivo OPT-IN/OFF; calidad-gate de indexación (D1)
├── 11-LEGAL/                    Plantillas: privacidad, términos, política editorial,
│                                declaración de IA, declaración de afiliados, derechos RSS
├── 12-TROUBLESHOOTING.md        Síntoma → causa → solución
├── GLOSARIO.md · LICENCIA.md · CHANGELOG.md · FAQ.md
├── starter/                     ⭐ REPO PLANTILLA FUNCIONAL (el mayor multiplicador)
│   ├── AGENTS.md                Orientación para el agente de código (punto de entrada)
│   ├── fixtures/                Feeds de ejemplo + salida "golden" para verificar el pipeline
│   └── theme/                   CSS y tipografía por defecto (para no partir de un folio en blanco)
├── prompts/                     Maestro genérico · independiente · sensible (+ el fácil derivado)
└── ejemplos/                    Un caso trabajado completo, genérico (el de geopolítica del autor
                                 va aquí como ejemplo, no como eje del kit)
```

Notas:
- **`starter/` es lo que convierte esto de "documento" en "kit".** Sin él, dos personas con
  el mismo texto obtienen sistemas distintos.
- **`01-ANTES-DE-EMPEZAR` con alternativas honestas** (cuándo NO usar el kit) genera más
  confianza que cualquier feature.
- **`07-GUARDARRAILES` es transversal y va en el núcleo** (decisión D2).
- **Licencia:** CC BY 4.0 para la documentación + MIT para el código del `starter/`,
  separadas y explícitas.
- **Atribución / bucle de crecimiento:** cada medio generado enlaza en el footer a la web
  del autor ("Hecho con Autopress · <web>/resources/autopress"), activado por defecto
  pero **desmarcable**. Cada medio creado = un backlink.

### 4.1 Gestión ES/EN
- **Español = fuente de verdad; inglés = derivado.** Un repo, dos árboles espejo (`/es/`,
  `/en/`) con nombres de fichero idénticos.
- **El código nunca se traduce** (identificadores, claves YAML, rutas del starter en inglés);
  el idioma de *salida* del medio es configuración (`site.language`), no propiedad del código.
- `glossary.yml` (términos que no se traducen) + `translate.py` (LLM + glosario + estado con
  hash del fuente → solo retraduce lo cambiado).
- **Lo legal se reescribe, no se traduce** (RGPD ≠ CAN-SPAM). Revisión humana obligatoria en
  `00`, `01`, `03`, `07` y todo `11-LEGAL/`.

---

## 5. Próximos pasos

1. **Construir el `starter/`** (repo plantilla funcional + `AGENTS.md` + `fixtures/` +
   `theme/`) — es el mayor multiplicador.
2. **Escribir los docs `00`–`12`** en el orden de valor (Quickstart y Guardarraíles primero).
3. **Sección de costes y legal** con los datos de §2.
4. **Verificar antes de publicar:** ToS de Vercel/Cloudflare, IDs de modelo y precios
   vigentes, términos de afiliados.
5. **Pasar el candidato a otras IAs** para revisión adversaria (prompt ya preparado), y
   contrastar.

---

_Este documento fija las decisiones D1-D3 y la capa factual verificada. Cualquier cambio de
rumbo en esas decisiones invalida partes de la estructura de §4._
