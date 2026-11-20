"""
Pre-publish gate for an issue. Used by /publish.

    python3 scripts/publish_check.py <slug>

Exits 0 if the issue is ready to publish, 1 otherwise (with reasons).
Checks:
  1. src/content/issues/<slug>.mdx exists.
  2. The verdict placeholder is gone and the <Verdict> block has real text.
  3. The disclosure placeholder has been replaced.
  4. research/<slug>/check.md exists.
  5. No unticked "- [ ]" items under "## Wrong" or "## Advice-language flags" in check.md.
Warns (does not fail) on remaining "Unsourced" items.
"""
import re
import sys
from pathlib import Path


def section(md: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", md, re.M | re.S)
    return m.group(1) if m else ""


def main(slug: str) -> int:
    problems, warnings = [], []
    issue = Path(f"src/content/issues/{slug}.mdx")
    check = Path(f"research/{slug}/check.md")

    if not issue.exists():
        print(f"FAIL: {issue} not found.")
        return 1
    src = issue.read_text()

    if "[VERDICT: TO BE WRITTEN BY EDITOR]" in src:
        problems.append("Verdict placeholder is still in the issue. Write the verdict inside <Verdict>…</Verdict>.")
    blocks = re.findall(r"<Verdict>(.*?)</Verdict>", src, re.S)
    if not blocks:
        problems.append("No <Verdict>…</Verdict> block found in the issue.")
    elif not any(len(re.sub(r"\s+", " ", b).strip()) >= 20 for b in blocks):
        problems.append("The <Verdict> block is empty or too short (< 20 characters).")

    if "TO BE CONFIRMED BY EDITOR" in src:
        problems.append("Disclosure placeholder is still in the frontmatter. Set `disclosure:` to your actual position.")

    if not check.exists():
        problems.append(f"{check} not found. Run the fact-checker (/new-issue) first.")
    else:
        md = check.read_text()
        for heading in ("Wrong", "Advice-language flags"):
            body = section(md, heading)
            if not body and heading == "Wrong":
                problems.append("check.md has no '## Wrong' section; can't confirm it is clean.")
            open_items = [l.strip() for l in body.splitlines() if l.strip().startswith("- [ ]")]
            for item in open_items:
                problems.append(f"Unresolved in check.md › {heading}: {item[6:][:160]}")
        unsourced = [l for l in section(md, "Unsourced").splitlines() if l.strip().startswith("- ") and "None." not in l]
        if unsourced:
            warnings.append(f"{len(unsourced)} unsourced claim(s) in check.md. Make sure you've cut, softened or sourced them.")

    for w in warnings:
        print(f"WARN: {w}")
    if problems:
        for p in problems:
            print(f"FAIL: {p}")
        return 1
    print(f"OK: {slug} is ready to publish.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 scripts/publish_check.py <slug>")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
