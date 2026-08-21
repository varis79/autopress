# 03 · COSTS — what it really costs

> **Summary:** a weekly outlet costs **less than a coffee a month**. The
> unavoidable expense is the **AI** (cents per edition) and, if you want your own
> domain, **~10–15 USD/year**. The rest of the stack has free tiers that are good
> enough to get started.
>
> **Data verified in 2026-06** (model prices) and **2026-08** (free tiers and
> host terms). **Check the current ones before deciding** — they change.

---

## 1. The only variable cost: the AI

The outlet makes **a single model call per edition** (everything else — ingestion,
classification, selection — is free code). That's why it's so cheap.

| Model | Price ($/1M tokens in · out) | Cost/edition | Cost/month (4-5 editions) |
|---|---|---|---|
| Haiku 4.5 | $1 / $5 | ~$0.05 | **~$0.30** |
| Sonnet 5 | $3 / $15 | ~$0.14 | **~$0.73** |
| Opus 5 | $5 / $25 | ~$0.24 | **~$1.20** |

The model is chosen in your config (`compose.model`). Start with an **affordable**
one (Sonnet or Haiku) and only move up if you feel the writing calls for it.

**What multiplies the cost** (and how to avoid it):
- Publishing daily instead of weekly (×7).
- Mass generation of SEO pages with AI → **disabled by default** on purpose
  (Google penalizes content at scale, and it sends the cost soaring).
- Unnecessary rewrites/retries. One call per edition is enough.

---

### The formula (so the numbers add up for you)

`cost/edition ≈ (input_tokens × price_in + output_tokens × price_out) / 1,000,000`

- **Input**: the selection (about 5-8 summarized news items) + the master prompt ≈ **1-3k tokens**.
- **Output**: the written edition, capped at `compose.max_tokens` (default **8,000**).
  On models with adaptive reasoning that cap is shared with *thinking*; compose **disables it
  by default** (`compose.thinking=disabled`) so the whole budget goes to the writing.
- With Sonnet 5 (~$3/$15 per 1M) that gives **~$0.05-0.14 per edition**. Multiply by 4-5
  editions/month. Today it's **1 LLM call per edition** (no extra calls).

> **Watch two things that change:** Sonnet 5 has an **introductory price ($2/$10 until
> 2026-08-31)**, then it goes up; and **model IDs/prices expire** — check the current one.

## 2. The rest of the stack (getting started is free)

| Piece | What for | Free tier | When you'd pay |
|---|---|---|---|
| **Hosting** (Cloudflare Pages) | Serve your static site | Free, **allows commercial use** | Practically never for a static site |
| **GitHub** | Store the code and automate | Public repos: unlimited free Actions | Private repo: 2,000 min/month free, then you pay |
| **Newsletter** (Resend) | Send the newsletter | Free to start (contact/send limits) | Once you pass the free tier (~1,000 contacts) you jump to a paid plan (check the current one) |
| **Domain** | Your own `youroutlet.com` | — | **~10–15 USD/year** (real, optional cost) |

> ⚠️ **Hosting warning if you monetize:** some free plans **prohibit commercial use**
> (affiliates, AdSense, donations): **Vercel Hobby** and **GitHub Pages** prohibit it; on
> Vercel, monetizing requires **Pro (~$20/month)**. **Cloudflare Pages** and **Netlify** do allow
> commercial use on the free tier (that's why Cloudflare is the recommended one). Comparison and guide in
> **[04-DESPLIEGUE.md](04-DESPLIEGUE.md)**; check the current ToS before choosing.

> **Public vs private repo:** the public one gives you unlimited free Actions, but
> **exposes your config, your sources and your editorial decisions** to anyone. The
> private one protects them but limits the free automation minutes. Decide based on
> how much the privacy of your "recipe" matters to you.

---

## 3. Three real-world scenarios

**A · Hobby, not monetizing (the most common way to start)**
- Affordable weekly AI + Cloudflare Pages + public GitHub + no custom domain.
- **Cost: ~$0.30–0.75/month.** Everything else, free.

**B · Serious, with domain and newsletter**
- AI (Sonnet) + Cloudflare Pages + custom domain + Resend.
- **Cost: ~$0.75/month + ~$12/year for the domain** (≈ **$1.75/month** amortized).

**C · Monetizing (affiliates/AdSense/donations)**
- Same as B, but **if you're on Vercel** you have to move to Pro (~$20/month). On
  **Cloudflare Pages monetizing is still free**.
- **Cost: ~$1.75/month** on Cloudflare, or **~$21.75/month** if you insist on Vercel.

---

## 4. On making money (an honest expectation)

- **Expected revenue is close to zero** at the start. Set this up because you're
  interested in the topic and want an outlet of your own, not as a get-rich-quick scheme.
- The kit **doesn't push you toward affiliates for expensive tools** (that's where advice
  gets corrupted). See honest monetization in `08-MODO-INDEPENDIENTE.md` (under construction).
- The **only unavoidable expense** is the AI (cents) and, if you want it, the domain.

---

_Next: [02-CUENTAS-Y-DOMINIO.md](02-CUENTAS-Y-DOMINIO.md) to get your outlet
online. Previous: [00-QUICKSTART.md](00-QUICKSTART.md)._
