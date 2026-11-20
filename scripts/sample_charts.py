"""Charts for the SAMPLE issue. Figures are fictional and illustrative only."""
import sys

sys.path.insert(0, "scripts")
from charts import render  # noqa: E402

years = ["FY21", "FY22", "FY23", "FY24", "FY25"]
revenue = [410, 468, 541, 602, 655]  # fictional, $m


def revenue_plot(ax, t):
    bars = ax.bar(years, revenue, width=0.6, color=t["series"][0], edgecolor=t["surface"], linewidth=2)
    ax.bar_label(bars, labels=[f"${v}m" for v in revenue], padding=6, color=t["ink"], fontsize=14)
    ax.set_ylim(0, 760)
    ax.yaxis.set_major_formatter(lambda v, _: f"${v:.0f}m")


render("sample", "revenue", revenue_plot, title="Revenue keeps compounding", subtitle="Tempo Gear Co., revenue by fiscal year ($m)", source="Fictional data for layout preview")

peers = ["Tempo Gear\n(SAMPLE)", "Peer A", "Peer B", "Peer C"]
margins = [47.0, 55.5, 44.2, 39.8]  # fictional, %


def margin_plot(ax, t):
    colors = [t["series"][0]] + [t["context"]] * 3
    bars = ax.barh(peers[::-1], margins[::-1], height=0.55, color=colors[::-1], edgecolor=t["surface"], linewidth=2)
    ax.bar_label(bars, labels=[f"{m:.1f}%" for m in margins[::-1]], padding=6, color=t["ink"], fontsize=14)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    ax.set_xlim(0, 65)
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.tick_params(axis="y", labelcolor=t["ink"])


render("sample", "gross-margin", margin_plot, title="Gross margin vs peers", subtitle="Latest fiscal year, %", source="Fictional data for layout preview")
