# 12 · TROUBLESHOOTING — cuando algo no va

> Problemas comunes y su arreglo. Casi todo se resuelve pasándole el mensaje de error a tu
> agente; aquí están los más frecuentes.

## Entorno

- **`python3: command not found`** → en Windows suele ser `python`. Instala Python 3.11+.
- **`ModuleNotFoundError` (feedparser/anthropic)** → activa el entorno y
  `python3 -m pip install -r requirements.txt`.
- **`PYTHONPATH` en Windows PowerShell** → `$env:PYTHONPATH="."` en una línea y luego el comando.

## Ejecutar y ver

- **Los enlaces del sitio no funcionan al abrir el `.html`** → son absolutos; usa el servidor:
  `PYTHONPATH=. python3 -m scripts.serve` y abre `http://localhost:8000`.
- **Sale `stub` / `"gated": ["stub"]`** → no hay clave de IA: es lo esperado (preview). Añade
  `ANTHROPIC_API_KEY` en `.env` para redacción real.

## Publicación bloqueada (¡suele ser correcto!)

- **`"published": false` en `--production`** → el gate hizo su trabajo. Mira `gate_reasons`:
  - `stub` → falta clave. `mode-pause` → muy pocas noticias esta semana.
  - `qa-blocked` → mira `qa`: `numbers_supported:false` (cifra sin fuente) o
    `independent_sources:false` (en `strict`, faltan 2 fuentes independientes).

## Fuentes (feeds)

- **`source: feeds` pero `raw_count: 0`** → mira `feeds` en el estado: `status: error` (fuente
  caída/URL mala) vs `empty` (sin noticias en la ventana). Revisa las URLs o amplía
  `ingest.lookback_days`.

## Despliegue / correo

- **El host no actualiza** → revisa que la carpeta publicada sea `site` y que el CI hizo push.
- **La newsletter cae en spam** → faltan SPF/DKIM/DMARC (ver `02-CUENTAS-Y-DOMINIO.md`).
- **CI falla** → mira el log del step; lo común es `ANTHROPIC_API_KEY` no puesto en *Secrets*.

## No sé qué puedo cambiar

- Di *"muéstrame los settings"* o corre `PYTHONPATH=. python3 -m scripts.settings [tema]`.
