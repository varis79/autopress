# 08 · INDEPENDENT MODE AND MONETIZATION (honest)

> The base case is **independent**. Monetization is optional, and here it comes without hype: the
> revenue expectation is **near zero** at the start. Build it because you care about the
> topic, not as a get-rich-quick scheme.

## Independent (default)

- `editorial.mode = independent`. No sponsor, no conflicts. Maximum credibility.
- This is what we recommend to start with and for sensitive topics.

## With a sponsor (optional)

- `editorial.mode = sponsored` + `sponsorship`. If you accept sponsorship, **always disclose it**
  visibly (no "disguised advertorial"): Google News and editorial ethics require it.
  Identify the sponsor and the selection criteria.

## Monetization channels (and their fine print)

| Channel | Reality |
|---|---|
| **Affiliates** | The kit does **not** push you toward affiliates for expensive tools (that's where advice gets corrupted). The only clean one: the **domain**. Always disclose affiliate links. |
| **AdSense / display** | Possible once you have real traffic. Watch the **host**: monetizing requires a commercial free tier (Cloudflare/Netlify yes; Vercel Hobby and GitHub Pages **no**). |
| **Donations** | Ko-fi / GitHub Sponsors. This also counts as "commercial use" on some hosts. |
| **Subscription/premium** | Later on; requires more infrastructure. |

## The host landmine (repeated because it matters)

If you're going to monetize, review `04-DESPLIEGUE.md`: **Vercel Hobby and GitHub Pages prohibit
commercial use** on their free plan. Cloudflare Pages and Netlify allow it. The agent verifies the
current ToS at build time.

## Golden rule

Credibility is the asset. Before monetizing, have a media outlet people actually want to read. The
monetization that sacrifices trust isn't worth it.
