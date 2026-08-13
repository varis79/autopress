# Autopress

> 🌐 **Español:** [README en español](../README.md) · guías en [`../`](../README.md)

**Build your own AI-assisted news digest.** Autopress is a free, open kit to set up, with the
help of an AI agent, a **curated news bulletin that generates itself, human-reviewed by
default**: it ingests **RSS feeds** (headlines and summaries), curates them, writes a weekly
edition and publishes it as a static website — on whatever topic you choose. Optional
newsletter (you set up the endpoint).

> **Two honest caveats:** (1) it writes from **RSS summaries**, not the full article — it's a
> thoughtful *digest*, not a newspaper that "reads" the news; it **paraphrases and cites**, it
> does not semantically verify every figure. (2) **Autonomy = the generation**, not the
> judgment: by default **nothing is indexed without your approval** (`review`), and you remain
> the editor and the legally responsible party. API cost is cents; the real cost is **your
> attention** (reviewing, source rights, corrections).

> **Status:** engine and credibility **complete** (pipeline, guardrails, governance, CI, SEO,
> newsletter, assistant); guide docs complete; verified by 2 external reviews. Pending:
> final packaging (GitHub template + download) and actual newsletter sending (host layer).
> Live details in `../PROGRESO.md`.

---

## What it is

- A generic, secret-free **blueprint** + a **starter** (scaffolding an AI agent
  uses to build your outlet) + guides for non-technical users.
- For **news-curation outlets**: any topic with a **live flow of sources**
  (cybersecurity, agriculture, current geopolitics, energy, fleets…). You choose the topic
  in a startup questionnaire. It is **not** for static/historical topics nor for
  AI-generated essay magazines — see `01-ANTES-DE-EMPEZAR.md`.
- **Genuinely cheap:** the core (one weekly edition) costs **~$0.30–$1.20 a month** in
  model API; the rest of the stack has free plans. Less than a coffee.

## Who it is NOT for (honesty first)

- If you only want a simple newsletter, **use Ghost, Substack or Beehiiv** — easier, with
  nothing to set up. Autopress makes sense when you want **your own curated outlet with SEO**,
  one you control.
- **It is not hands-free magic:** you need a **coding agent with terminal and repo access**
  (Claude Code, Cursor…) to build it, and to create a few free accounts (GitHub, a host,
  Resend). The agent does the technical work; you decide and supervise.
- **The autonomy is in the weekly edition, not in the editorial judgment.** You set the rules,
  the sources and the editorial line; you review when the topic is sensitive.

## What it contains

```
README.md              · This
AGENTS.md              · Kit entry point + questionnaire (for your agent)
00-QUICKSTART.md       · From zero to your first edition (by levels, nothing blocks you)
01-ANTES-DE-EMPEZAR.md · Is it for you? Honest alternatives
02-CUENTAS-Y-DOMINIO   · Accounts, DNS, SPF/DKIM/DMARC
03-COSTES.md           · Real cost + formula + break-even points
04-DESPLIEGUE.md       · Publish wherever you want (host comparison + CI)
05-CUESTIONARIO.md     · The intake that defines your outlet
06-ADAPTACION-TEMATICA · Playbooks by topic type
07-GUARDARRAILES.md    · Editorial standards (what's enforced by code + policy)
08-MODO-INDEPENDIENTE  · Going independent + honest monetization
10-SEO.md · 12-TROUBLESHOOTING.md
BLUEPRINT-MEDIO-AUTONOMO.md · The full technical blueprint
starter/               · ⭐ The runnable project (AGENTS.md, scripts/, tests/…)
  scripts/setup.py     · assistant · serve.py · preview · settings.py · catalog
  legal/ · newsletter/ · examples/movilidad-mx-es/ (worked case)
```

## Getting started

1. Download the kit (or use "Use this template" on GitHub).
2. Open it with your AI agent (Claude Code / Cursor). Read **`../starter/AGENTS.md`**; it runs the
   questionnaire and builds your outlet.
3. Prefer to do it by hand? `cd starter && PYTHONPATH=. python3 -m scripts.setup` (assistant) and
   `python3 -m scripts.serve` (preview). Or say *"show me the settings"*.

**Nothing is required upfront:** you progress by levels (local → online → domain → feeds/AI →
automatic → newsletter → monetization) and each one works on its own. Without a domain you use the host's
subdomain; without an AI key you see the outlet in demo mode.

## Key decisions of the kit

- **Correct SEO always; never flood Google.** Mass page generation is
  **disabled by default**; only pages that pass a quality threshold get indexed.
- **Rigor by default:** cited sources, human review available, no invented figures.
  Generic — not tied to any topic.
- **Portable static site**: deploy on any host. Recommended **Cloudflare Pages**
  (free and allows monetization); **GitHub Pages** and **Vercel Hobby** prohibit commercial use on
  free plans. The agent checks the current ToS when building. See `04-DESPLIEGUE.md`.

## License

- **Documentation:** CC BY 4.0.
- **`starter/` code:** MIT.

Every outlet built with Autopress links (optionally and removably) to the website of
the kit's author — a small credit that helps others find it.

---

_A project derived from a real autonomous editorial outlet, sanitized and generalized so that
anyone can build their own._
