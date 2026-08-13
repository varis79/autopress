# 05 · QUESTIONNAIRE — define your outlet

> The questions that define your outlet. You can answer them here (to get ready) or let
> the **assistant** ask them for you: `cd starter && PYTHONPATH=. python3 -m scripts.setup`.
> Remember: **nothing is required all at once** — skip what you don't have and add it later.

## 1. Identity
- **Name** of the outlet and **tagline** (a one-line description of what it is).
- **Language** of publication.
- **Reference timezone** (affects the publishing schedule).

## 2. Topic (the most important part)
- **What is it about and what angle does it bring?** Be specific (not "technology," but "regulation of
  electric mobility in Mexico and Spain").
- **Does it have a live flow of sources?** New stories with links should appear every week. If it's
  a static/historical topic, Autopress is **not** the right tool (see `01-ANTES-DE-EMPEZAR.md`).
- **Key topics/subtopics** and their keywords.
- **Markets/geographies**: which are primary and which are secondary.
- **Players** to follow (companies, regulators).

## 3. Voice
- **Tone**: analytical/sober, approachable, technical… Prioritize the outside reader.

## 4. Governance (how much review)
- **Risk profile**: `auto` (publishes on its own), `review` (opens a PR, the default), `strict`
  (sensitive topics: corroboration across ≥2 sources + review). See `07-GUARDARRAILES.md`.
- **Independent or with a sponsor?** See `08-MODO-INDEPENDIENTE.md`.

## 5. Publishing (optional, added later)
- **Where do you publish?** and **do you monetize?** (affects the host — see `04-DESPLIEGUE.md`).
- **Your own domain?** If not, you use the host's free subdomain.

## 6. Integrations (optional)
- **AI key** (without it, stub mode). **Newsletter** (Resend) if you want a bulletin.

> Not sure what can be configured? Say *"show me the settings"* or run
> `PYTHONPATH=. python3 -m scripts.settings` — the full catalog with where each thing lives.
