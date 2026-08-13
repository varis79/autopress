# Autopress · starter (reference implementation)

Engine for an **autonomous editorial media outlet**: it ingests feeds, classifies,
deduplicates, selects, **writes with AI**, runs quality control, and **publishes a
browsable static site** — with no database (Git is the database), the
**deterministic core in code** (free, reproducible) and **AI only for judgment**
(writing). It runs entirely **offline and keyless** in demo mode.

> This `starter/` is the generic reference implementation. It ships with no
> theme; the theme is defined by the `config.json` + `prompts/master-prompt.md`
> that the agent fills in during onboarding.

---

## 1. Up and running in 30 seconds (no keys, no accounts)

```bash
cd starter
PYTHONPATH=. python3 -m scripts.doctor        # checks environment and files
PYTHONPATH=. python3 -m scripts.pipeline       # generates the site in starter/site/
PYTHONPATH=. python3 -m unittest discover tests -v   # tests (all should be green)
```

Open `starter/site/index.html`. You'll see a sample edition (**stub** mode:
placeholder content, flagged as "do not publish in production"). For real
writing, add your AI key (§4).

---

## 2. How it works (the pipeline)

A linear flow; each stage is a pure, testable function.

```
feeds RSS ─▶ ingest ─▶ classify ─▶ dedupe ─▶ select ─▶ compose ─▶ qa ─▶ publish ─▶ site/
             (network) (deterministic, in code, free)   (AI)   (control)  (static HTML)
```

| Stage | File | What it does | AI? |
|---|---|---|---|
| Ingest | [scripts/ingest.py](../scripts/ingest.py) | Downloads/parses feeds, cleans HTML, stable id by canonical URL | No |
| Classification | [scripts/classify.py](../scripts/classify.py) | topic (most matches), market (title×2+summary), players | No |
| Deduplication | [scripts/dedupe.py](../scripts/dedupe.py) | Canonical URL + title similarity; duplicates are **merged** as extra sources | No |
| Selection | [scripts/select_stories.py](../scripts/select_stories.py) | blacklist → scoring → geo/topic quotas → mode (normal/short/pause) | No |
| **Writing** | [scripts/compose.py](../scripts/compose.py) | Calls the LLM; validates provenance; **falls back to stub** | **Yes** |
| — stub | [scripts/compose_stub.py](../scripts/compose_stub.py) | Placeholder writing (no spend), for demo/tests | No |
| QA | [scripts/qa.py](../scripts/qa.py) | Checks by level: blocking / review_required / warning | No |
| Publishing | [scripts/publish.py](../scripts/publish.py) | Writes index, edition, archive, sitemap.xml, rss.xml | No |
| Orchestrator | [scripts/pipeline.py](../scripts/pipeline.py) | Ties it all together, loads `.env`, prints JSON status | No |
| Core | [scripts/pipeline_core.py](../scripts/pipeline_core.py) | `run()` (golden contract) and `run_full()` (with dedupe) | No |

Shared libraries in [scripts/lib/](../scripts/lib/): `text.py` (Unicode
word-based matching, canonical URL), `templating.py` (edition + citation render),
`site.py` (pages, sitemap, RSS).

---

## 3. Provenance and citations (Perplexity style, with validation)

Each story carries its numbered sources `[1][2]`. The design prevents the AI from
**inventing** sources or stories:

1. The AI receives the items inside `<untrusted_sources>` and can only return
   `ref_id`s that exist in that input.
2. `assemble()` in [compose.py](../scripts/compose.py) **validates**: it discards
   any story `ref_id` that isn't in the selection and any `source_ref` with an
   unknown id. The URL of each source is copied by the **code** from the validated
   registry, not by the AI.
3. Duplicates detected in dedupe are kept as **additional sources** of the same
   story (which is why a news item can have `[1][2]`).

Verifiable in the tests: `tests/test_compose.py` checks that an invented source
(`sFAKE00000`) is discarded and that a story with an unknown `ref_id` doesn't pass.

---

## 4. Where the AI tokens go (the key)

**Never** in the code or in `config.json`. Only in the environment:

```bash
cp .env.example .env      # and fill in ANTHROPIC_API_KEY=...
```

- `.env` is in `.gitignore` (never committed). In production, the key goes in the
  GitHub Actions *secrets* / host environment variables.
- `scripts/pipeline.py` loads `.env` automatically (`_load_dotenv`, no
  dependencies).
- **The model** is chosen in `config.json` → `compose.model` (currently
  `"claude-sonnet-5"`, inexpensive; configurable). The model id goes in the YAML,
  not in the code.
- **Without a key**, `compose()` falls back to stub: the kit **never breaks** and
  spends nothing.

Full config contract in [autopress.schema.json](../autopress.schema.json). A
config that doesn't validate against the schema **must not run**
(`validate_config.py`).

---

## 5. Design: styles × palettes (30 combinations)

The style (structure+typography) and the palette (color) are **decoupled** via CSS
variables and `data-style` / `data-palette` / `data-theme` attributes in
[theme/theme.css](../theme/theme.css): **6 styles × 5 palettes × light/dark**.

```bash
PYTHONPATH=. python3 -m scripts.render_demo    # generates sample-output/gallery.html
```

The gallery is what gets uploaded to the web to pick a look without touching code.

---

## 6. Governance: risk profiles and QA

- **risk_profile** (`config.json`): `auto` (auto-publishes) · `review` (default:
  opens a PR and stops) · `strict` (human review + double source + cooldown).
- **Leveled QA** ([qa.py](../scripts/qa.py)): `blocking` (e.g. missing cover → does
  not publish) · `review_required` (e.g. story with no source) · `warning` (e.g.
  stub). The resulting status (`ok` / `ok-qa-warn` / `blocked`) is consumed by the
  workflow according to the profile.
- A **stub never reaches production** (`publishing.block_stub_in_production`).

---

## 7. Folder structure

```
starter/
├─ AGENTS.md               # entry point for the agent (project rules)
├─ README.md               # this document (architecture + how to run)
├─ autopress.schema.json   # configuration contract (validated)
├─ .env.example            # where keys go (copy to .env)
├─ .gitignore              # .env, __pycache__, /site/
├─ prompts/
│  └─ master-prompt.example.md   # editorial constitution (rename to master-prompt.md)
├─ scripts/                # the pipeline (see §2)
│  └─ lib/                 # text, templating, site
├─ theme/theme.css         # 6 styles × 5 palettes × light/dark
├─ fixtures/               # sample data + golden (config, raw.jsonl, expected/)
├─ tests/                  # golden, ingest, compose (all offline)
├─ sample-output/          # generated design gallery
└─ site/                   # pipeline output (generated; in .gitignore)
```

---

## 8. Tests (all offline, no API spend)

```bash
cd starter && PYTHONPATH=. python3 -m unittest discover tests -v
```

- `test_pipeline_golden.py` — **reproducibility contract**: two agents with the
  same input produce the same selection (`fixtures/expected/selection.json`). It
  also verifies dedupe and competitor filtering.
- `test_ingest.py` — feed parsing/normalization and recency window.
- `test_compose.py` — provenance (rejection of invented sources/stories) and
  fallback to stub without a key.

---

## 9. Status and limits (for review)

**Done and verified:** full offline pipeline; golden test green; numbered
multi-source citations with provenance validation; LLM compose with
anti-injection and fallback; token surface (`.env`); 30 design combinations;
leveled QA aligned with the source model.

**Pending (roadmap):** root packaging (pinned requirements, LICENSE); step-by-step
onboarding for non-technical users (SPF/DKIM/DMARC, costs); deploy adapter
(Cloudflare Pages) + CI + double opt-in newsletter; adversarial injection
fixtures; legal document (AI disclosure). Changes recorded in
[../PROGRESO.md](PROGRESO.md).

**Estimated cost** of running a media outlet like this: ~0.30–1.20 USD/month (free
static hosting + one AI call per weekly edition).
