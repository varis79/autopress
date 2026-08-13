# 04 · DEPLOYMENT — publish your site wherever you want

> **Key idea:** what Autopress generates is a **static site** (HTML + CSS + `rss.xml`
> + `sitemap.xml`, in the `site/` folder). That gets uploaded **as-is to any static
> host** — nothing is tied to a single provider. Here's a **recommended** option to
> get started plus **four options** with guidance, so you can choose for yourself.

_Plan/ToS data verified in 2026-08 (sources at the end). **Terms change:**
your agent asks you about host and monetization in the startup questionnaire and **checks the
current terms** of the host you pick — this guide is a dated reference, not the
eternal truth._

---

## The only thing that truly matters when choosing: are you going to monetize?

Some free plans **forbid commercial use** (ads, affiliates, selling, even
soliciting donations depending on the case). That's the only real trap. Quick rule:

- **You're going to monetize** (ads / affiliates / donations / charging) → **Cloudflare Pages** or
  **Netlify** (their free plans do allow commercial use).
- **You don't monetize** (personal, informational project) → **any** of the four works.

---

## Comparison (free tier, 2026-08)

| Host | Does free allow monetizing? | Free plan limits | Custom domain | Ease |
|---|---|---|---|---|
| **⭐ Cloudflare Pages** (recommended) | ✅ **Yes** | **Unlimited** bandwidth | Free | Easy (connect the repo) |
| **Netlify** | ✅ **Yes** (you can't *resell* the hosting) | 100 GB/month · 300 min build/month | Free | **Very easy** (Git or drag the folder) |
| **GitHub Pages** | ⚠️ **No** for business/e-commerce/SaaS | 100 GB/month (soft) · site ≤1 GB · 10 builds/h | Free | Easy (from the same repo) |
| **Vercel** | ⚠️ **No** on Hobby (personal only) · Pro $20/month | 100 GB/month | Free | Very easy |

**Why Cloudflare Pages is the default recommendation:** it allows commercial use on
the free tier, doesn't cap your bandwidth, gives you a free custom domain and connects to the repo in a couple
of clicks. But it's a **recommendation, not an obligation**: your site is portable.

---

## Mini-guides (pick one)

For the first three, the pattern is the same: **you connect your GitHub repo** and the host
**rebuilds and publishes itself** every time something changes. You tell it that the folder to publish is
the site's output folder (`site/`).

### ⭐ Cloudflare Pages (recommended)
1. Free account on Cloudflare → **Workers & Pages → Create → Pages → Connect to Git**.
2. Choose your repo. Build command: *(none, it's static)*. Output directory: **`site`**.
3. Deploy. It gives you `tumedio.pages.dev`. Add your domain under **Custom domains**.

### Netlify (the easiest for non-technical folks)
1. Free account on Netlify → **Add new site → Import an existing project** (or drag the
   `site/` folder into *Deploys* for a quick test).
2. Publish directory: **`site`**. Deploy.
3. Custom domain under **Domain settings**.

### GitHub Pages (only if you do NOT monetize)
1. In your repo → **Settings → Pages**.
2. Publish from a branch/folder containing the site, or with a GitHub Action that uploads `site/`.
3. Custom domain in the same panel. ⚠️ Remember: its ToS **does not allow** using it for business.

### Vercel (with a caveat)
1. Import the repo into Vercel. Output: **`site`**. Deploy.
2. ⚠️ The **Hobby (free) plan is for personal, non-commercial use only**. If you monetize you need
   **Pro (~$20/month)**. For an outlet with ads/affiliates, Cloudflare or Netlify is better.

---

## Automation: it publishes itself (GitHub Actions)

The kit ships the **`.github/workflows/publish.yml`** workflow that makes your outlet
**publish itself every week**. The key: the **AI compose runs only once there** (with
your key in *Secrets*), and the host only **serves the already-rendered `site/`** — it doesn't re-run
the AI or need to know Python.

**Setup (once):**
1. On GitHub → **Settings → Secrets and variables → Actions** → add `ANTHROPIC_API_KEY`.
2. Create your production **`config.json`** at the repo root (with your `sources` block).
3. Connect your host to the repo with **publish folder = `site`** and **no build command** (the
   site already comes rendered in the repo).

**What it does each week** (Monday by default; there's also a manual button):
- Runs the pipeline in production mode and, depending on your **`risk_profile`**:
  - `auto` → **commits and publishes itself** (the host redeploys when it detects the push).
  - `review` / `strict` → **opens a Pull Request** for you to review and merge (nothing is
    published until you want it to be — faithful to "human review").
  - stub / paused / QA blocked → **the job fails** and nothing gets published.

> `site/` and `data/editions/` **are versioned** (CI updates them). The host serves `site/`;
> `data/editions/` is your history ("Git as a database"). Switching hosts doesn't touch your
> pipeline: you reconnect the repo somewhere else and you're done.

---

## Sources (verified 2026-08)

- Cloudflare Pages — [pricing](https://developers.cloudflare.com/pages/functions/pricing/) ·
  [free plan](https://www.cloudflare.com/plans/free/)
- Netlify — [commercial use (official forum)](https://answers.netlify.com/t/can-we-use-netlify-free-plan-for-commercial-purposes/41545) ·
  [pricing](https://www.netlify.com/pricing/)
- GitHub Pages — [limits and permitted use](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- Vercel — [Hobby plan](https://vercel.com/docs/plans/hobby)

_Previous: [03-COSTES.md](03-COSTES.md) · Accounts and DNS: [02-CUENTAS-Y-DOMINIO.md](02-CUENTAS-Y-DOMINIO.md)_
