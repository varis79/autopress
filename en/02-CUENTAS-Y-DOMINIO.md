# 02 · ACCOUNTS AND DOMAIN — putting your outlet online

> **When you need this:** only when you want to **publish on the internet** and/or
> **send a newsletter**. To test locally (the [00-QUICKSTART](00-QUICKSTART.md))
> you don't need any account.
>
> This is the most "plumbing" part of the project. Go slow, checkpoint by checkpoint, and let
> the agent run the technical steps. Costs: see [03-COSTES.md](03-COSTES.md).

---

## Accounts checklist (in order)

| # | Account | What for | Required? |
|---|---|---|---|
| 1 | **GitHub** | Store the code and **automate** the weekly edition | Yes, to publish |
| 2 | **Cloudflare Pages** | Serve your site (host **by default**, free, allows monetization) | Yes, to publish |
| 3 | **AI key** | Write the edition (already in the quickstart) | Yes, for real writing |
| 4 | **Resend** | Send the newsletter | Optional |
| 5 | **Domain** | Have your own `yourmedia.com` | Optional (~10–15 USD/year) |

> **Remember the hosting warning:** the free plan of **Vercel prohibits commercial use**
> (affiliates, AdSense, donations). That's why the default is **Cloudflare Pages**. See
> [03-COSTES.md](03-COSTES.md).

---

## Step 1 · GitHub (code + automation)

1. Create an account at github.com (free).
2. Upload your project (the agent does it with `git`). 
3. **Decision — public or private repo:**
   - **Public:** automation (GitHub Actions) **free and unlimited**, but
     **anyone can see your config, your sources and your editorial decisions**.
   - **Private:** protects your "recipe", but the free Actions minutes are
     limited (2,000/month).
   Choose based on how much privacy matters to you. You can change it later.

**✅ Checkpoint:** your project shows up in your GitHub.

---

## Step 2 · Choose a host and publish

Your site is **static and portable** (`site/`): it uploads to any host. You have the
comparison and the mini-guides (Cloudflare, Netlify, GitHub Pages, Vercel) in
**[04-DESPLIEGUE.md](04-DESPLIEGUE.md)**. Recommended to start: **Cloudflare Pages**
(free, allows monetization, free custom domain).

In almost all of them, the pattern is: **you connect your repo** and the host publishes only the output folder (`site/`).

**✅ Checkpoint:** the host gives you a URL with your site (e.g. `yourmedia.pages.dev`).
**🔧 If it doesn't show up:** check that the published output folder is the one for the generated site.

---

## Step 3 · Custom domain (optional)

1. Buy the domain from any registrar (they're interchangeable). Typical cost
   **~10–15 USD/year**.
2. Point it to Cloudflare Pages (in Pages → Custom domains → you add your domain;
   Cloudflare tells you the DNS records to create).

**✅ Checkpoint:** `https://yourmedia.com` loads your site (DNS may take a few minutes to
propagate).

---

## Step 4 · Newsletter and email that does NOT land in spam (SPF · DKIM · DMARC)

If you send a newsletter, your domain has to **prove** that the email is legitimate. Without
this, your emails land in spam or get rejected. They are **three DNS records** you add once.
Resend (or another provider) gives you the exact values; you paste them into your DNS
(Cloudflare). The agent guides you.

| Record | What it says | How you set it |
|---|---|---|
| **SPF** | "These servers can send email on my behalf" | A TXT record that authorizes your provider (Resend) |
| **DKIM** | "This email is signed and hasn't been tampered with" | Records (CNAME/TXT) with the key your provider gives you |
| **DMARC** | "If an email doesn't pass SPF/DKIM, do this" | A TXT at `_dmarc.yourdomain.com` |

**Recommendation for DMARC:** start in observation mode and tighten later:
1. `p=none` (only monitors, doesn't block) for the first few weeks.
2. When you see that your legitimate mail passes, move up to `p=quarantine` and then `p=reject`.

**✅ Checkpoint:** in the Resend panel your domain shows as **"verified"** and a
**test send** lands in your inbox (not in spam).
**🔧 If it lands in spam:** almost always one of the three records is missing or there's a typo when
copying it. Review them with the agent.

> **Double opt-in and unsubscribe (legal nuance, important):** "by law" would be too absolute —
> in the EU (GDPR/ePrivacy) marketing requires **prior consent** (with nuances), and in
> the US CAN-SPAM works mostly on an **opt-out** basis. As a prudent default that complies in
> practice almost everywhere, the kit uses **double opt-in** (confirmation email) and
> **one-click unsubscribe with a signed token (HMAC of the email + secret key)** in the link — so
> no one can unsubscribe third parties or flood you with fake sign-ups (*subscription bombing*).
> It gets set up in the newsletter phase (D); here we only leave the email properly authenticated.

---

## Security rule (for all accounts)

- **Secrets (API keys, tokens) NEVER go in the repo.** They go in `.env` (local,
  ignored by git) and in the **GitHub Actions "secrets"** / environment variables of the
  host (production).
- If a key slips into the repo, **revoke it and generate another**. Consider it burned.

---

_Next: understand the spending in [03-COSTES.md](03-COSTES.md), or how it works
under the hood in [starter/README.md](../starter/README.md). Previous:
[00-QUICKSTART.md](00-QUICKSTART.md)._
