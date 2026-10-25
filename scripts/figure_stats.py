# -*- coding: utf-8 -*-
"""图5 图书借阅数据统计分析（四联图）。

数据直接来自 MySQL 数据库 library_db 的统计查询结果 (_work/stats.json)。
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np

import figstyle as fs

ROOT = Path(r"C:\Users\LZ\Desktop\软工")
OUT = ROOT / "figures"
data = json.loads((ROOT / "_work" / "stats.json").read_text(encoding="utf-8"))

fs.apply_publication_style(fs.FigureStyle(font_size=13, axes_linewidth=1.8))
P = fs.PALETTE

fig, axes = fs.create_subplots(2, 2, figsize=(14.4, 10.4))
ax_a, ax_b, ax_c, ax_d = axes

# ---------------------------------------------------------------- (a) 出版社
rows = [(r["k"], int(r["v"])) for r in data["publisher"]]
top = rows[:6]
rest = sum(v for _, v in rows[6:])
labels_a = [k for k, _ in top] + ["其他 %d 家出版社" % (len(rows) - 6)]
vals_a = [v for _, v in top] + [rest]

y = np.arange(len(labels_a))
bars = ax_a.barh(y, vals_a, height=0.68, color=[P["blue_main"]] * 6 + [P["neutral"]],
                 edgecolor="black", linewidth=0.9, zorder=3)
ax_a.set_yticks(y)
ax_a.set_yticklabels(labels_a, fontsize=11)
ax_a.invert_yaxis()
ax_a.set_xlabel("借阅次数")
ax_a.set_title("(a) 各出版社图书借阅次数", fontsize=13.5)
ax_a.set_xlim(0, max(vals_a) * 1.22)
for rect, v in zip(bars, vals_a):
    ax_a.text(rect.get_width() + max(vals_a) * 0.015,
              rect.get_y() + rect.get_height() / 2, str(v),
              va="center", ha="left", fontsize=11)
ax_a.grid(axis="x", linestyle=":", alpha=0.35, zorder=0)
ax_a.set_axisbelow(True)

# ---------------------------------------------------------------- (b) 月度趋势
months = [r["k"][-2:] + "月" for r in data["monthly"]]
mv = [int(r["v"]) for r in data["monthly"]]
fs.make_trend(ax_b, np.arange(len(months)), [mv], ["月度借阅量"],
              colors=[P["blue_main"]], ylabel="借阅次数", xlabel="月份",
              show_shadow=False)
for xi, v in zip(np.arange(len(months)), mv):
    ax_b.annotate(str(v), (xi, v), textcoords="offset points", xytext=(0, 8),
                  ha="center", fontsize=10.5)
ax_b.set_xticks(np.arange(len(months)))
ax_b.set_xticklabels(months, fontsize=11)
ax_b.set_ylim(0, max(mv) * 1.28)
ax_b.set_title("(b) 2026 年 3—9 月借阅量变化趋势", fontsize=13.5)
ax_b.grid(axis="y", linestyle=":", alpha=0.35, zorder=0)
ax_b.set_axisbelow(True)

# ---------------------------------------------------------------- (c) 读者类型
rt = data["reader_type"]
order = ["学生", "教师", "职工"]
by = {r["k"]: r for r in rt}
cats = [t for t in order if t in by]
loans = [int(by[t]["v"]) for t in cats]
openl = {r["k"]: int(r["v"]) for r in data["open_by_type"]}
opens = [openl.get(t, 0) for t in cats]
fs.make_grouped_bar(ax_c, cats, [loans, opens], ["借阅总次数", "其中尚未归还"],
                    ylabel="次数", annotate=True,
                    colors=[P["blue_main"], P["red_2"]], width=0.62)
ax_c.set_ylim(0, max(loans) * 1.24)
ax_c.set_title("(c) 不同类型读者的借阅情况", fontsize=13.5)
ax_c.legend(loc="upper right", fontsize=11)
ax_c.grid(axis="y", linestyle=":", alpha=0.35, zorder=0)
ax_c.set_axisbelow(True)

# ---------------------------------------------------------------- (d) 热力图
tm = data["type_month"]
mcols = sorted({r["m"] for r in tm})
d = {(r["t"], r["m"]): int(r["n"]) for r in tm}
mat = np.array([[d.get((t, m), 0) for m in mcols] for t in cats], dtype=float)
fs.make_heatmap(ax_d, mat, x_labels=[m[-2:] + "月" for m in mcols], y_labels=cats,
                cmap="magma", cbar_label="借阅次数", annotate=True, fmt="{:.0f}")
ax_d.set_title("(d) 读者类型 × 月份借阅量分布", fontsize=13.5)

for p in fs.finalize_figure(fig, OUT / "fig5_stats", formats=["png", "pdf"], dpi=300,
                            pad=0.08):
    print("saved", p)
