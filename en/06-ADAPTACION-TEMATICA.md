# 06 · TOPIC ADAPTATION — playbooks by type of topic

> How to adjust `config.json` (taxonomy, markets, scoring) and `master-prompt.md` to fit
> your topic. The structure stays the same; what changes are the keywords, the sources and the tone.

## The 4 settings that define a topic

1. **Sources** (`sources`) — the RSS feeds. This is what defines the outlet the most. Look for the
   trade press, regulators, newsletters and reference blogs for your topic.
2. **Topics and keywords** (`taxonomy.topics`) — 3-6 topics with their keywords (in the language
   of the sources). Example: `regulation: [regulation, law, compliance]`.
3. **Markets** (`taxonomy.markets`) — geographies with `tier` (primary/secondary) and keywords.
4. **Tone** (`master-prompt.md`) — the voice for that audience.

## Playbooks

**B2B niche / sector-specific** (logistics, fintech, energy…)
- Sources: the sector's press + regulators. Technical tone, for professionals.
- `review` risk, or `auto` if it's harmless and has a sponsor.

**Regulatory / public policy**
- Prioritize `regulation` in `priority_topics`. Always attribute; never state opinion as fact.
- `strict` risk if there are named players or it's contentious.

**Technology / product**
- Product and company keywords (`players`). Watch out for hype: golden rules (§ figures).

**Local / regional**
- A single `primary` market; keywords for local cities/institutions.

**Sensitive topics** (health, politics, individuals)
- **`strict` mandatory**: corroboration from ≥2 independent sources, human review,
  accusations always attributed. See `07-GUARDARRAILES.md`.

## How to find RSS feeds

- Search for "`<your topic>` RSS" or add `/feed`, `/rss` to the source's website.
- Regulators and the press usually have a feed. Check that it updates and that their terms allow
  summarizing/quoting (see `../starter/legal/derechos-fuentes.md`).
- Start with 3-5 good sources; the pipeline deduplicates and selects.

> The agent can propose an initial taxonomy and sources for your topic; review them and adjust.
