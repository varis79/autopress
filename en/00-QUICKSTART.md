# 00 · QUICKSTART — from zero to your first edition

> **Who it's for:** anyone, even if you can't code. You decide and supervise;
> **the AI agent does the technical work**. Time: ~60–90 min the first time.
> By the end you'll have **a sample edition published on your computer** (with
> nothing paid connected yet).

This document goes by **checkpoints**. After each step there's a "✅ you should
see…". If you don't see it, right there is the "🔧 if it fails".

---

## What you need before you start

1. **A computer** (Mac, Windows or Linux).
2. **A coding agent with access to terminal and files** — Claude Code, Cursor,
   or similar. It's the one that builds your outlet; you talk to it in plain language.
3. **Python 3.11 or higher** installed (the agent can check and install it).
4. **Nothing paid yet.** The AI key and the accounts (host, newsletter) come
   later. This quickstart is 100% free and local.

> You don't need to know what a terminal is or read code. You're going to **copy
> and paste commands** (the ▶ buttons in this guide) or ask the agent to run them.

---

## Onboarding by levels (nothing is required upfront)

It's not all-or-nothing. **You advance by levels and each one works on its own**; you add what's missing
whenever you want, without redoing anything:

| Level | You have | What you're missing and it's FINE |
|---|---|---|
| **0** | Your outlet runs locally (demo) | — |
| **1** | Published online | *no domain* → you use the host's free subdomain |
| **2** | Your own domain | you add it in `site.domain` when you have it |
| **3** | Real feeds + AI | *no key* → stub mode (you see the outlet without spending) |
| **4** | Publishes itself (CI) | optional; until then you launch it yourself |
| **5** | Newsletter | optional |
| **6** | You monetize | optional |

> **Shortcut:** instead of editing files by hand, use the **wizard**:
> `cd starter && PYTHONPATH=. python3 -m scripts.setup` — it asks you the questions and writes
> `config.json`, `.env` and the prompt for you. It skips whatever you don't have.

## Step 0 · Get the kit and open it with your agent

Download the kit (ZIP from `/releases/latest`) and open it with your
AI agent. The first thing the agent will do is read **`AGENTS.md`**, the entry
file.

Check that you have Python:

```bash
python3 --version
```

**✅ You should see** something like `Python 3.11.x` or higher.
**🔧 If it fails** (`command not found`): ask the agent "install Python 3.11+ for me" or
download it from python.org. On Windows it's usually `python` instead of `python3`.

Set up an isolated environment and install the dependencies (once):

```bash
cd starter && python3 -m venv .venv && . .venv/bin/activate && python3 -m pip install -r requirements.txt
```

**✅ You should see** `feedparser` and `anthropic` install without errors.

> **🪟 Windows note (PowerShell).** The commands in this guide use
> Mac/Linux syntax. In PowerShell, two changes: activate the environment with `.venv\Scripts\Activate.ps1`,
> and where you see `PYTHONPATH=. python3 -m scripts.X`, write it on **two lines**:
> `$env:PYTHONPATH="."` and then `python -m scripts.X`. Your agent can give you the
> exact command for your system if you ask.

---

## Step 1 · The startup questionnaire

Tell your agent: **"Let's get started, run the startup questionnaire for me."** It will
ask you (and it **must wait for your answers**, not make them up):

- Theme and angle of the outlet
- Language(s)
- Markets/geographies (which are primary)
- Tone and voice
- **Risk profile**: `auto`, `review` (recommended) or `strict` (for sensitive
  topics: politics, health, geopolitics, people)
- Independent or with a sponsor?
- Name of the outlet and whether you have a domain

**✅ You should see** the agent **ask you** instead of assuming. Take your time
with the answers: they're the editorial line of your outlet.

---

## Step 2 · The agent configures your outlet

With your answers, the agent fills in:

- `starter/fixtures/config.json` — taxonomy, markets, scoring, AI model.
- `starter/prompts/master-prompt.md` — the "editorial constitution" (tone + rules).

You don't have to touch these files by hand; the agent edits them. You can ask it
to explain to you in plain language what it put there.

**✅ You should see** two files created/edited with your decisions inside.

---

## Step 3 · Environment check (doctor)

```bash
cd starter && PYTHONPATH=. python3 -m scripts.doctor
```

**✅ You should see** at the end: **`READY for local mode (fixtures, no accounts).`**
**🔧 If it fails:** the doctor tells you exactly what's missing (e.g. a dependency).
Pass the message to the agent and have it resolve it.

---

## Step 4 · Generate the site in test mode (stub)

Still **without spending anything**. "Stub mode" writes with placeholder text so you
see the structure, the design and the quality control working.

```bash
cd starter && PYTHONPATH=. python3 -m scripts.pipeline
```

**✅ You should see** a status JSON with `"published": true` and **`"indexable": false`**
(it's a **preview**: `noindex` is set on purpose so drafts aren't indexed) and a
new `starter/site/` folder.

View it in the browser with **a single command** (it builds and serves; opening the `.html` directly
breaks the internal links, which are absolute):

```bash
cd starter && PYTHONPATH=. python3 -m scripts.serve
```

Open `http://localhost:8000`. It's your outlet, browsable. The `stub` notice is **correct and
expected**: it's a test draft, it isn't published to production. It's removed when you connect
the AI (step 6).

**🔧 If it fails:** copy the error to the agent. The most common thing is a missing dependency
(activate the environment from Step 0 and `python3 -m pip install -r requirements.txt`).

---

## Step 5 · (Optional) Choose your design

```bash
cd starter && PYTHONPATH=. python3 -m scripts.render_demo
```

Open `starter/sample-output/gallery.html`: you'll see **6 styles × 5 palettes** (light and
dark). Choose the one you like and tell the agent "use style X with palette Y";
it'll put it in your config.

**✅ You should see** a gallery with 30 look-and-feel combinations.

---

## Step 6 · Connect the AI (first real edition)

Now the real writing. You need **an AI key** (from your model
provider). Cost: **cents per edition** (see [03-COSTES.md](03-COSTES.md)).

1. Copy the secrets template:
   ```bash
   cd starter && cp .env.example .env
   ```
2. Open `.env` and paste your key into `ANTHROPIC_API_KEY=...`. **This file is never
   uploaded to the internet** (it's protected in `.gitignore`).
3. Generate again:
   ```bash
   cd starter && PYTHONPATH=. python3 -m scripts.pipeline
   ```

**✅ You should see** a genuinely written edition: in the status, `"gate_reasons"` **no
longer includes `"stub"`**, and each story carries its **numbered sources `[1][2]`** linking
to the original.
**🔧 If something fails with the AI** (invalid key, no balance, no network): the system
**falls back to stub mode on its own** — it doesn't break. Check the key and the balance.

> **From the demo to YOUR real news.** As is, the pipeline writes the **demo**
> selection (the fixtures) so you can test the circuit. For real news on your topic,
> add your **RSS feeds** to the config (the `sources` block, see `../starter/autopress.schema.json`)
> and point the pipeline to your own config:
> ```bash
> PYTHONPATH=. python3 -m scripts.pipeline --config config.json
> ```
> With `sources`, the pipeline **ingests from the network** (with timeout, retries and per-source
> diagnostics) instead of the fixtures. And for the **indexable** version (not preview) you run it
> in production, which **doesn't publish** if the edition is stub, is paused or QA blocks it
> (it exits with a code ≠ 0):
> ```bash
> PYTHONPATH=. python3 -m scripts.pipeline --config config.json --production
> ```

---

## You now have your outlet working (locally). What now?

- **Publish it on the internet** (free) → next: [02-CUENTAS-Y-DOMINIO.md](02-CUENTAS-Y-DOMINIO.md).
- **Understand the real cost** and the free tiers → [03-COSTES.md](03-COSTES.md).
- **Not sure if it's for you?** → [01-ANTES-DE-EMPEZAR.md](01-ANTES-DE-EMPEZAR.md).
- **How it works under the hood** (for you or for your agent) → [../starter/README.md](../starter/README.md).

> Golden rule: **the agent builds, you supervise.** When the topic is sensitive,
> review before publishing (`strict` profile). It's your outlet and your judgment.
