# 12 · TROUBLESHOOTING — when something goes wrong

> Common problems and their fixes. Almost everything gets solved by passing the error message to your
> agent; here are the most frequent ones.

## Environment

- **`python3: command not found`** → on Windows it's usually `python`. Install Python 3.11+.
- **`ModuleNotFoundError` (feedparser/anthropic)** → activate the environment and run
  `python3 -m pip install -r requirements.txt`.
- **`PYTHONPATH` on Windows PowerShell** → `$env:PYTHONPATH="."` on one line, then the command.

## Run and view

- **The site's links don't work when you open the `.html`** → they're absolute; use the server:
  `PYTHONPATH=. python3 -m scripts.serve` and open `http://localhost:8000`.
- **You get `stub` / `"gated": ["stub"]`** → there's no AI key: this is expected (preview). Add
  `ANTHROPIC_API_KEY` to `.env` for real writing.

## Publishing blocked (this is usually correct!)

- **`"published": false` on `--production`** → the gate did its job. Look at `gate_reasons`:
  - `stub` → key missing. `mode-pause` → too few stories this week.
  - `qa-blocked` → look at `qa`: `numbers_supported:false` (a figure with no source) or
    `independent_sources:false` (in `strict`, the 2 independent sources are missing).

## Sources (feeds)

- **`source: feeds` but `raw_count: 0`** → look at `feeds` in the status: `status: error` (source
  down/bad URL) vs `empty` (no stories in the window). Check the URLs or widen
  `ingest.lookback_days`.

## Deployment / email

- **The host doesn't update** → check that the published folder is `site` and that CI did the push.
- **The newsletter lands in spam** → SPF/DKIM/DMARC are missing (see `02-CUENTAS-Y-DOMINIO.md`).
- **CI fails** → look at the step's log; the common cause is `ANTHROPIC_API_KEY` not set in *Secrets*.

## I don't know what I can change

- Say *"show me the settings"* or run `PYTHONPATH=. python3 -m scripts.settings [topic]`.
