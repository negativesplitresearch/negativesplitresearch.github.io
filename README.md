# Negative Split Research

*The business behind the finish line.*

An independent newsletter and website on the business of endurance sports. Live at **https://negativesplitresearch.github.io**.

Built with Astro + MDX + Tailwind CSS, output as a static site, and deployed to GitHub Pages by GitHub Actions on every push to `main`.

---

## Run it locally

You need Node.js 22 or newer and Python 3 with matplotlib (for charts only).

```bash
npm install
npm run dev        # http://localhost:4321 (drafts ARE visible here, marked DRAFT)
npm run build      # type-check + production build into dist/ (drafts excluded)
npm run preview    # serve dist/ at http://localhost:4321
```

> **Node location on this Mac:** Node was installed to `~/.local/node` (no Homebrew). Either run `export PATH="$HOME/.local/node/bin:$PATH"` in each terminal, or add that line to `~/.zshrc`.

> **iCloud warning:** this repo lives in `~/Documents`, which is synced to iCloud Drive. When the disk is nearly full, iCloud evicts local files and builds hang. `node_modules`, `dist` and `.astro` are excluded from iCloud with `xattr -w 'com.apple.fileprovider.ignore#P' 1 <folder>`. If you delete and reinstall `node_modules`, run that command on it again. The robust fix is to move the repo out of `~/Documents` (e.g. to `~/code/`).

## Project layout

```
src/
  config.ts                 site name, tagline, nav, BEEHIIV_EMBED
  content.config.ts         issue frontmatter schema
  content/issues/*.mdx      one file per issue
  components/               Signup, Chart, Verdict, IssueCard, ThemeToggle
  layouts/Base.astro        <head>, OpenGraph tags, header, footer (disclaimer line)
  pages/                    home, /issues, /issues/[slug], /about, /disclaimer, rss.xml, 404
public/charts/<slug>/       chart SVGs (light + -dark variants)
scripts/charts.py           house chart style (matplotlib)
scripts/publish_check.py    pre-publish gate used by /publish
research/<slug>/            facts.md, analysis.md, check.md (agent working files)
social/<slug>/              LinkedIn, Instagram, X copy
.claude/agents/             researcher, analyst, writer, fact-checker, distributor
.claude/commands/           /new-issue, /publish
```

## Add an issue

### The automated way (Claude Code)

```
/new-issue Garmin
```

This runs researcher → analyst → writer → fact-checker, then stops with a summary and your to-do list. You then:

1. Fix every item under **Wrong** in `research/<slug>/check.md` and tick it (`- [x]`).
2. Rewrite every **Advice-language flag** and tick it.
3. Deal with the unsourced claims.
4. Write the verdict inside `<Verdict>…</Verdict>` (replacing `[VERDICT: TO BE WRITTEN BY EDITOR]`).
5. Set `disclosure:` in the frontmatter.
6. Preview with `npm run dev`, then run:

```
/publish <slug>
```

`/publish` refuses to run if the verdict or disclosure placeholder is still there or `check.md` has unticked Wrong/Advice items. If everything passes, it sets `draft: false`, writes the social copy, builds, commits and pushes.

### By hand

Create `src/content/issues/<slug>.mdx`. The filename becomes the URL: `/issues/<slug>/`.

```mdx
---
title: "Garmin's quiet subscription machine"
date: 2026-12-01
company: "Garmin"
ticker: "GRMN"              # optional
sector: "Wearables"         # used for archive filtering
summary: "One or two sentences for cards, RSS and social previews."
verdict: "Optional one-liner." # optional
cover: "/charts/garmin/cover.png"  # optional, also used as the OG image
disclosure: "The author holds no position in GRMN."
draft: true                 # true = never on the live site
---

Body in Markdown. Components are available without importing:

<Chart src="/charts/garmin/revenue.svg" alt="Describe the chart" caption="Takeaway" source="Garmin 10-K" />

<Verdict>
Your verdict.
</Verdict>
```

**Drafts:** `draft: true` issues appear only in `npm run dev`. They are filtered out of every production page, the RSS feed and the sitemap.

### Charts

Use the house style so charts match the site and work in dark mode:

```python
import sys; sys.path.insert(0, "scripts")
from charts import render

def plot(ax, t):  # t = theme colours for light/dark
    ax.bar(["FY23", "FY24"], [5.2, 6.3], color=t["series"][0], edgecolor=t["surface"], linewidth=2)

render("garmin", "revenue", plot, title="Revenue", subtitle="$bn", source="Garmin 10-K")
```

This writes `public/charts/garmin/revenue.svg` and `revenue-dark.svg`; `<Chart>` swaps them automatically. Orange (`series[0]`) is always the company the issue covers. Peers are blue then green, with grey for context. The palette has been checked for colour-blind separation in both themes. `scripts/sample_charts.py` is a worked example.

## Deploy

Push to `main`. `.github/workflows/deploy.yml` installs, builds and publishes `dist/` to GitHub Pages; it takes about 1–2 minutes. Watch progress in the repo's **Actions** tab. (Pages source must be set to *GitHub Actions* under Settings → Pages; it already is.)

## Add a custom domain later

Say you buy `negativesplit.com`.

1. **CNAME file:** create `public/CNAME` containing just the domain:
   ```
   negativesplit.com
   ```
   (Astro copies `public/` into the build, so Pages sees it on every deploy.)
2. **Update the site URL:** set `site` in `astro.config.mjs` and `url` in `src/config.ts` to `https://negativesplit.com`. Update the `Sitemap:` line in `public/robots.txt` and the link in `.claude/agents/distributor.md` and `.claude/commands/publish.md`.
3. **DNS at your registrar:**
   - Apex domain (`negativesplit.com`): four **A** records pointing to
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
     and optionally four **AAAA** records:
     `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
   - `www` subdomain: a **CNAME** record pointing to `negativesplitresearch.github.io`
4. **GitHub:** Settings → Pages → Custom domain → enter the domain → Save. Once the DNS check passes (minutes to 24h), tick **Enforce HTTPS**.
5. **Recommended:** verify the domain under your GitHub account/org settings → Pages → *Add a verified domain*, which stops anyone else claiming it.
6. Update the Beehiiv publication's website URL if you set it there.

## Before launch

- Delete the sample issue: `src/content/issues/sample-issue.mdx` and `public/charts/sample/`.
- Replace `public/og-default.png` if you want a custom social card (`python3 scripts/make_og.py` regenerates it).

---

Not investment advice. For information and education only.
