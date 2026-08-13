# 07 · GUARDRAILS — editorial standards

> What makes your outlet **credible**. Part is **enforced by code** (it doesn't depend on
> the AI "behaving well"); part is your own editorial policy. Here it all is in one place.

## Enforced by code (non-negotiable)

| Rule | How it's guaranteed |
|---|---|
| **No made-up figures** | QA blocks the edition if a number in the copy doesn't appear in its source (`numbers_supported`). |
| **Real provenance** | The AI only returns a `ref_id`; the code copies the URL. A third-party or made-up citation → discarded. |
| **Anti-injection** | RSS content is delimited and with `<`/`>` escaped: a source can't issue commands. |
| **No active schemes** | Only http/https URLs in links (no `javascript:`). |
| **Stub never in production** | The gate prevents publishing drafts. |

## Risk profiles (you choose)

| Profile | When | What it does |
|---|---|---|
| `auto` | Harmless niches | Publishes on its own. |
| `review` (**default**) | Most cases | Generates the edition and **opens a PR**: you review it and merge. |
| `strict` | Sensitive topics (health, politics, people) | + **≥2 independent sources** per story (QA blocks if not) + mandatory review. |

## Editorial policy (recommended)

- **Attribute, don't assert** anything contentious: "according to X…", never as your own fact.
- **Neutrality**: inform, don't campaign. Distinguish fact from analysis.
- **Corrections**: have a contact email and correct quickly; flag the correction.
- **AI transparency**: state that the content is written by an AI (`editorial.ai_disclosure`,
  footer, and `../starter/legal/divulgacion-ia.md`).
- **Conflicts of interest**: if there's a sponsor, disclose it (see `08-MODO-INDEPENDIENTE.md`).

## What it looks like in practice

Run in `strict` and watch the status: if a story doesn't have 2 independent sources, QA
marks it `blocked` and it isn't published. That's the guardrail working, not an error.
