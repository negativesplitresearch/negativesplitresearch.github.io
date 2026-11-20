"""
Negative Split Research chart style.

Every chart is rendered twice (light + dark) so it matches the site theme:
    public/charts/<slug>/<name>.svg       (light)
    public/charts/<slug>/<name>-dark.svg  (dark)
Embed in an issue with:  <Chart src="/charts/<slug>/<name>.svg" alt="..." caption="..." source="..." />

Usage:
    import sys; sys.path.insert(0, "scripts")
    from charts import render

    def plot(ax, t):
        ax.bar(years, revenue, color=t["series"][0], edgecolor=t["surface"], linewidth=2)

    render("garmin", "revenue", plot, title="Revenue, $bn", subtitle="FY2020-FY2024")

Rules (validated palette; see README):
  - series[0] (race-bib orange) is ALWAYS the company the issue is about.
  - series[1], series[2] are peers, in that fixed order. More than 3 -> use t["context"] grey.
  - One y-axis only. Never dual-axis. Two measures -> two charts.
  - >= 2 series needs a legend; label the last point / key bars directly, not every point.
"""
from __future__ import annotations

import os
from typing import Callable

import matplotlib

matplotlib.use("Agg")
import logging  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

THEMES = {
    "light": {
        "surface": "#fbfaf7",
        "ink": "#16140f",
        "muted": "#5f5a52",
        "grid": "#e6e2d9",
        "context": "#a8a39a",
        "series": ["#c2410c", "#2563a8", "#0f8a6e"],
    },
    "dark": {
        "surface": "#111110",
        "ink": "#ece9e2",
        "muted": "#a39e94",
        "grid": "#2c2a26",
        "context": "#5f5a52",
        "series": ["#e2652a", "#4f8fdb", "#22a886"],
    },
}

SANS = ["Inter", "Inter Variable", "Helvetica Neue", "Arial", "DejaVu Sans"]
SERIF = ["Source Serif 4", "Georgia", "Times New Roman", "DejaVu Serif"]


def _style(t: dict) -> dict:
    return {
        "font.family": "sans-serif",
        "font.sans-serif": SANS,
        "font.size": 15,
        "svg.fonttype": "path",
        "figure.facecolor": t["surface"],
        "axes.facecolor": t["surface"],
        "savefig.facecolor": t["surface"],
        "axes.edgecolor": t["grid"],
        "axes.labelcolor": t["muted"],
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "grid.color": t["grid"],
        "grid.linewidth": 1,
        "xtick.color": t["muted"],
        "ytick.color": t["muted"],
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "ytick.major.pad": 8,
        "lines.linewidth": 2.5,
        "lines.markersize": 8,
        "legend.frameon": False,
        "legend.labelcolor": t["ink"],
        "text.color": t["ink"],
    }


def render(
    slug: str,
    name: str,
    plot: Callable[[plt.Axes, dict], None],
    title: str = "",
    subtitle: str = "",
    source: str = "",
    size: tuple[float, float] = (12, 6.75),
    out_root: str = "public/charts",
) -> list[str]:
    """Render `plot(ax, theme)` in light and dark. Returns the written paths."""
    out_dir = os.path.join(out_root, slug)
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for mode, t in THEMES.items():
        with plt.rc_context(_style(t)):
            fig, ax = plt.subplots(figsize=size, dpi=100)
            plot(ax, t)
            top = 0.86 if title else 0.95
            if title:
                fig.text(0.06, 0.94, title, fontsize=24, fontweight="semibold", family=SERIF, color=t["ink"], va="top")
            if subtitle:
                fig.text(0.06, 0.875, subtitle, fontsize=15, color=t["muted"], va="top")
                top = 0.80
            if source:
                fig.text(0.06, 0.03, f"Source: {source}", fontsize=12, color=t["muted"])
            fig.text(0.94, 0.03, "Negative Split Research", fontsize=12, color=t["muted"], ha="right")
            fig.subplots_adjust(left=0.06, right=0.94, top=top, bottom=0.14 if source else 0.10)
            # Shift the plot right so tick labels never clip at the left edge;
            # they then align with the title at x = 0.06.
            fig.canvas.draw()
            x0 = ax.get_tightbbox(fig.canvas.get_renderer()).x0 / fig.bbox.width
            if x0 < 0.06:
                fig.subplots_adjust(left=0.06 + (0.06 - x0))
            suffix = "" if mode == "light" else "-dark"
            path = os.path.join(out_dir, f"{name}{suffix}.svg")
            fig.savefig(path, format="svg")
            if os.environ.get("NSR_PREVIEW"):
                fig.savefig(os.path.join(os.environ["NSR_PREVIEW"], f"{slug}-{name}{suffix}.png"))
            plt.close(fig)
            paths.append(path)
    return paths
