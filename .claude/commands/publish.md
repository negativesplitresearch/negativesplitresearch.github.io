---
description: Gate-check an issue, mark it approved, generate social copy, build, commit and push to main.
argument-hint: <slug>
---

Publish the issue with slug: **$ARGUMENTS**

If no slug was given, list the drafts (files in `src/content/issues/` with `draft: true`) and ask which one. Stop at the first failure in any step below, tell me exactly why, and do not continue.

## 1. Gate checks
Run:
```
python3 scripts/publish_check.py $ARGUMENTS
```
It confirms the verdict block is filled in (placeholder gone, real text inside `<Verdict>`), the disclosure placeholder is replaced, and research/$ARGUMENTS/check.md has no unticked items under **Wrong** or **Advice-language flags**.
- If it prints any `FAIL`, stop and show me every FAIL line. Change nothing.
- Show me any `WARN` lines, but they don't block.

## 2. Approve
In `src/content/issues/$ARGUMENTS.mdx`, change `draft: true` to `draft: false`. Change nothing else in the file.

## 3. Social copy
Run the **distributor** agent with the Agent tool: "Slug: $ARGUMENTS. The issue is approved (draft: false). Write social/$ARGUMENTS/." Confirm that `social/$ARGUMENTS/linkedin.md`, `instagram-carousel.md` and `x-thread.md` exist.

## 4. Build
```
export PATH="$HOME/.local/node/bin:$PATH"; npm run build
```
If the build fails, set `draft: true` back, stop, and show me the error. Then confirm `dist/issues/$ARGUMENTS/index.html` exists.

## 5. Commit and push
- `git status` to check what changed. Stage only this issue's files: `src/content/issues/$ARGUMENTS.mdx`, `public/charts/$ARGUMENTS/`, `research/$ARGUMENTS/`, `social/$ARGUMENTS/`. If other files are modified, list them and don't stage them.
- Commit with: `Publish issue: <title>`
- `git push origin main`. If the push fails, show me the error; don't force-push.

## 6. Report
- Live URL: https://negativesplitresearch.github.io/issues/$ARGUMENTS/ (live 1–2 minutes after the GitHub Actions deploy finishes)
- Paths of the three social files, and the LinkedIn hook line
- Reminder: send the newsletter from Beehiiv (it isn't sent automatically) and post the social copy.
