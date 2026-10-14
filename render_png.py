"""Render etf_fee_bite_table.csv as a shaded PNG table (etf_fee_bite_table.png)."""
import csv

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# One-hue sequential blue ramp, light (near zero) -> dark (largest bite).
RAMP = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
        "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
CMAP = LinearSegmentedColormap.from_list("bite", RAMP)
INK, MUTED, SURFACE, GRID = "#1f1f1d", "#5f5e5a", "#ffffff", "#d9d8d4"

with open("etf_fee_bite_table.csv", newline="") as f:
    rows = list(csv.reader(f))
header, body = rows[0], rows[1:]
values = [[float(c.rstrip("%")) for c in r[1:]] for r in body]
vmax = max(max(r) for r in values)

n_rows, n_cols = len(body), len(header)
cell_w, label_w, cell_h = 1.0, 1.15, 0.32
fig_w = label_w + (n_cols - 1) * cell_w
fig_h = (n_rows + 1) * cell_h
top_pad, bottom_pad = 1.3, 0.55

fig = plt.figure(figsize=(fig_w + 0.6, fig_h + top_pad + bottom_pad), dpi=150,
                 facecolor=SURFACE)
ax = fig.add_axes([0.3 / (fig_w + 0.6), bottom_pad / (fig_h + top_pad + bottom_pad),
                   fig_w / (fig_w + 0.6), fig_h / (fig_h + top_pad + bottom_pad)])
ax.set_xlim(0, fig_w)
ax.set_ylim(fig_h, 0)
ax.axis("off")

fig.text(0.3 / (fig_w + 0.6), 1 - 0.45 / (fig_h + top_pad + bottom_pad),
         "Cumulative ETF Value Lost to Expense Ratios", fontsize=20,
         fontweight="bold", color=INK, va="center")
fig.text(0.3 / (fig_w + 0.6), 1 - 0.9 / (fig_h + top_pad + bottom_pad),
         "Each cell = 1 − (1 − expense ratio)^years: the share of value lost "
         "versus an identical no-fee ETF. No return or starting-balance assumption.",
         fontsize=11, color=MUTED, va="center")


def col_x(j):
    return 0 if j == 0 else label_w + (j - 1) * cell_w


# Header row
for j, h in enumerate(header):
    w = label_w if j == 0 else cell_w
    text = "Expense ratio" if j == 0 else h.replace(" years", " yr")
    ax.text(col_x(j) + w / 2, cell_h / 2, text, ha="center", va="center",
            fontsize=9.5, fontweight="bold", color=INK)
ax.plot([0, fig_w], [cell_h, cell_h], color=INK, lw=1)

# Body rows
for i, (r, vals) in enumerate(zip(body, values)):
    y = (i + 1) * cell_h
    ax.text(label_w / 2, y + cell_h / 2, r[0], ha="center", va="center",
            fontsize=9, fontweight="bold", color=INK)
    for j, v in enumerate(vals, start=1):
        t = v / vmax
        ax.add_patch(plt.Rectangle((col_x(j) + 0.02, y + 0.02), cell_w - 0.04,
                                   cell_h - 0.04, facecolor=CMAP(t), lw=0))
        ax.text(col_x(j) + cell_w / 2, y + cell_h / 2, r[j], ha="center",
                va="center", fontsize=8.5, color="#ffffff" if t > 0.5 else INK)
    if (i + 1) % 10 == 0 and i + 1 < n_rows:
        ax.plot([0, fig_w], [y + cell_h, y + cell_h], color=GRID, lw=0.8)

fig.text(0.3 / (fig_w + 0.6), 0.25 / (fig_h + top_pad + bottom_pad),
         "Expense ratio applied annually and compounded. Darker = more value lost.",
         fontsize=9, color=MUTED, va="center")

fig.savefig("etf_fee_bite_table.png", facecolor=SURFACE)
