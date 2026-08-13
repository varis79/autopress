# Ejemplo trabajado — "Radar Movilidad" (México + España)

Un medio **completo y relleno** para que veas cómo encaja todo. Regla de oro del onboarding:
**nada es obligatorio; avanzas por niveles.**

## Míralo ya (nivel 0, sin cuentas ni claves)

Corre el pipeline apuntando a este config (usa los fixtures como datos de demo):

```bash
cd starter && PYTHONPATH=. python3 -m scripts.pipeline --config examples/movilidad-mx-es/config.json
```

Verás una edición de "Radar Movilidad" en `site/` (preview `noindex`). Sírvela con
`PYTHONPATH=. python3 -m scripts.serve` y ábrela en `http://localhost:8000`.

## Sube de nivel cuando quieras (sin rehacer nada)

| Nivel | Qué añades | Cómo |
|---|---|---|
| 1 | **Publicar online** | Conecta el repo a un host (ver `../../04-DESPLIEGUE.md`). Sin dominio usas su subdominio gratis. |
| 2 | **Dominio propio** | Rellena `site.domain` en el config y apúntalo en el host. |
| 3 | **Feeds reales + IA** | Añade `sources` (abajo) y `ANTHROPIC_API_KEY` en `.env`. |
| 4 | **Automático** | Activa el workflow `.github/workflows/publish.yml`. |
| 5 | **Newsletter** | Ver `../../newsletter/README.md` (doble opt-in + baja firmada). |

### Bloque `sources` para el nivel 3 (reemplaza por feeds reales de tu tema)

```json
"sources": [
  {"name": "Fuente 1", "url": "https://EJEMPLO-medio-movilidad.com/rss", "geo_hint": "mx"},
  {"name": "Fuente 2", "url": "https://EJEMPLO-regulador.es/feed", "geo_hint": "es"}
]
```

Añádelo a `config.json` y el pipeline **ingiere de la red** en vez de los fixtures. Busca los
feeds RSS reales de la prensa/reguladores de tu tema y sustitúyelos.

## Empieza el tuyo

En vez de editar a mano, usa el asistente: `PYTHONPATH=. python3 -m scripts.setup`.
Este ejemplo es solo una referencia de cómo se ve todo relleno y coherente.
