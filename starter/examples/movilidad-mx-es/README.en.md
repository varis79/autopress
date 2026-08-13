# Worked example — "Radar Movilidad" (Mexico + Spain)

A **complete, fully populated** media outlet so you can see how everything fits together. The golden rule of onboarding:
**nothing is required; you progress by levels.**

## See it right now (level 0, no accounts or keys)

Run the pipeline pointing at this config (it uses the fixtures as demo data):

```bash
cd starter && PYTHONPATH=. python3 -m scripts.pipeline --config examples/movilidad-mx-es/config.json
```

You'll get an edition of "Radar Movilidad" in `site/` (preview with `noindex`). Serve it with
`PYTHONPATH=. python3 -m scripts.serve` and open it at `http://localhost:8000`.

## Level up whenever you want (without redoing anything)

| Level | What you add | How |
|---|---|---|
| 1 | **Publish online** | Connect the repo to a host (see `../../04-DESPLIEGUE.md`). Without a domain you use its free subdomain. |
| 2 | **Your own domain** | Fill in `site.domain` in the config and point it at the host. |
| 3 | **Real feeds + AI** | Add `sources` (below) and `ANTHROPIC_API_KEY` in `.env`. |
| 4 | **Automatic** | Enable the `.github/workflows/publish.yml` workflow. |
| 5 | **Newsletter** | See `../../newsletter/README.md` (double opt-in + signed unsubscribe). |

### `sources` block for level 3 (replace with real feeds for your topic)

```json
"sources": [
  {"name": "Fuente 1", "url": "https://EJEMPLO-medio-movilidad.com/rss", "geo_hint": "mx"},
  {"name": "Fuente 2", "url": "https://EJEMPLO-regulador.es/feed", "geo_hint": "es"}
]
```

Add it to `config.json` and the pipeline **ingests from the network** instead of the fixtures. Look up the real
RSS feeds of the press/regulators for your topic and substitute them.

## Start your own

Instead of editing by hand, use the wizard: `PYTHONPATH=. python3 -m scripts.setup`.
This example is just a reference for what everything looks like when it's fully populated and coherent.
