---
description: Research, analyse, draft and fact-check a new issue (researcher → analyst → writer → fact-checker), then stop for the editor.
argument-hint: <company or topic>
---

Create a new Negative Split Research issue about: **$ARGUMENTS**

If no company/topic was given, stop and ask for one.

## 0. Slug
Derive a short kebab-case slug from the company/topic (e.g. "On Holding" → `on-holding`, "Garmin" → `garmin`). If `src/content/issues/<slug>.mdx` or `research/<slug>/` already exists, stop and ask whether to overwrite or use a different slug.

## 1–4. Run the agents strictly in order
Run each with the Agent tool, one at a time. Wait for each to finish and confirm its output file exists before starting the next. If any step fails or its output is missing, stop and report what happened. Do not do their work yourself.

1. **researcher**: "Company/topic: $ARGUMENTS. Slug: <slug>. Write research/<slug>/facts.md."
2. **analyst**: "Slug: <slug>. Read research/<slug>/facts.md. Write research/<slug>/analysis.md and 1–2 charts in public/charts/<slug>/."
3. **writer**: "Slug: <slug>. Read research/<slug>/facts.md and analysis.md. Write src/content/issues/<slug>.mdx with draft: true."
4. **fact-checker**: "Slug: <slug>. Verify src/content/issues/<slug>.mdx against the original sources. Write research/<slug>/check.md."

After step 3, confirm the draft has `draft: true` and contains `[VERDICT: TO BE WRITTEN BY EDITOR]`. If not, fix only those two things.

Then run `export PATH="$HOME/.local/node/bin:$PATH"; npm run build` to make sure the draft's MDX compiles. Drafts are excluded from production output, so this only checks syntax. Report any error.

## 5. Stop and report to the editor
Do not publish, commit or push. Give me:

**The issue**
- Title, summary, word count, file path
- The 3–5 numbers that matter (from analysis.md)
- Charts created
- Preview: `npm run dev`, then http://localhost:4321/issues/<slug>/ (drafts show in dev only)

**Fact check** (from research/<slug>/check.md)
- Summary line (verified / wrong / unsourced / advice flags)
- Every **Wrong** item in full
- Every **Advice-language flag** in full
- Unsourced items (brief)
- Data gaps (MISSING items from facts.md)

**Your to-do list**
1. Fix each Wrong item in the draft, then tick it `- [x]` in check.md.
2. Rewrite or remove each advice-language flag, then tick it.
3. Cut, soften or source the unsourced claims.
4. Write your verdict inside the `<Verdict>` block (replace the placeholder). Optionally add a one-line `verdict:` to the frontmatter.
5. Set `disclosure:` in the frontmatter to your actual position (e.g. "The author holds no position in GRMN.").
6. Read it once end to end, then run `/publish <slug>`.
