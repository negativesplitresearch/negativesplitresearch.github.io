"""Generate the default 1200x630 OpenGraph image (public/og-default.png)."""
import matplotlib

matplotlib.use("Agg")
import logging  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

fig = plt.figure(figsize=(12, 6.3), dpi=100, facecolor="#fbfaf7")
fig.patches.append(plt.Rectangle((0, 0), 0.018, 1, transform=fig.transFigure, color="#c2410c"))
serif = ["Source Serif 4", "Georgia", "DejaVu Serif"]
fig.text(0.08, 0.72, "NEGATIVE SPLIT RESEARCH", fontsize=20, color="#c2410c", fontweight="bold", family=["Helvetica Neue", "Arial", "DejaVu Sans"])
fig.text(0.08, 0.40, "The business behind\nthe finish line.", fontsize=64, color="#16140f", family=serif, fontweight="semibold", linespacing=1.05)
fig.text(0.08, 0.16, "Running · Triathlon · Cycling · Swimming", fontsize=22, color="#5f5a52", family=["Helvetica Neue", "Arial", "DejaVu Sans"])
fig.savefig("public/og-default.png", facecolor=fig.get_facecolor())
