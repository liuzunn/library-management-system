# -*- coding: utf-8 -*-
"""图1 图书管理系统 E-R 图（实体-联系图, Chen 记法）

依据实验指导书《附录二 图书管理系统的实体-联系图》绘制。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse, Polygon, Rectangle

import figstyle as fs

OUT = Path(r"C:\Users\LZ\Desktop\软工\figures")

fs.apply_publication_style(fs.FigureStyle(font_size=15, axes_linewidth=2.0))

fig, ax = plt.subplots(figsize=(10.2, 12.4))
fs.blank_axes(ax, (0.0, 11.2), (1.9, 13.9))

# ---------------- 实体 ----------------
book = fs.draw_entity(ax, 5.5, 10.2, "图书", w=2.05, h=0.82, fontsize=17)
reader = fs.draw_entity(ax, 5.5, 6.2, "读者", w=2.05, h=0.82, fontsize=17)

# ---------------- 联系 ----------------
borrow = fs.draw_diamond(ax, 5.5, 8.4, "借阅", w=2.15, h=1.20, fontsize=17)

# ---------------- 图书的属性 ----------------
book_attrs = [
    ("书号", 1.55, 11.30, True),
    ("书名", 3.20, 12.60, False),
    ("作者", 5.10, 12.92, False),
    ("价格", 7.00, 12.60, False),
    ("出版社", 8.72, 11.90, False),
    ("摘要", 9.75, 11.05, False),
]
for name, ax_, ay_, is_key in book_attrs:
    node = fs.draw_attribute(ax, ax_, ay_, name, w=1.42, h=0.64, fontsize=13.5, key=is_key)
    fs.connect(ax, book, node, lw=1.5)

# ---------------- 联系自身的属性 ----------------
for name, ax_, ay_ in [("借书时间", 2.55, 8.40), ("还书时间", 8.45, 8.40)]:
    node = fs.draw_attribute(ax, ax_, ay_, name, w=1.78, h=0.64, fontsize=13.5, key=True)
    fs.connect(ax, borrow, node, lw=1.5)

# ---------------- 读者的属性 ----------------
reader_attrs = [
    ("卡号", 1.45, 4.62, True),
    ("姓名", 3.30, 3.62, False),
    ("性别", 5.05, 3.42, False),
    ("单位", 6.78, 3.62, False),
    ("类型", 8.42, 4.02, False),
    ("级别", 9.85, 4.90, False),
]
for name, ax_, ay_, is_key in reader_attrs:
    node = fs.draw_attribute(ax, ax_, ay_, name, w=1.42, h=0.64, fontsize=13.5, key=is_key)
    fs.connect(ax, reader, node, lw=1.5)

# ---------------- 基数 ----------------
fs.connect(ax, book, borrow, lw=1.8)
fs.connect(ax, borrow, reader, lw=1.8)
ax.text(6.02, 9.44, "N", fontsize=18, color="#B64342", fontweight="bold",
        ha="center", va="center", zorder=6)
ax.text(6.02, 7.36, "1", fontsize=18, color="#B64342", fontweight="bold",
        ha="center", va="center", zorder=6)

# ---------------- 图例 ----------------
handles = [
    Line2D([], [], marker="s", linestyle="none", markersize=13,
           markerfacecolor="#EAF1FA", markeredgecolor=fs.PALETTE["blue_main"],
           label="实体"),
    Line2D([], [], marker="D", linestyle="none", markersize=11,
           markerfacecolor="#FDF3D8", markeredgecolor="#B8860B", label="联系"),
    Line2D([], [], marker="o", linestyle="none", markersize=13,
           markerfacecolor="#EAF6EC", markeredgecolor="#2E7D32", label="属性"),
    Line2D([], [], marker="o", linestyle="none", markersize=13,
           markerfacecolor="#EAF6EC", markeredgecolor="#2E7D32", label="主键（下划线）"),
]
leg = ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.005, 0.005),
                fontsize=13, ncol=2, handletextpad=0.6, columnspacing=1.4,
                borderpad=0.8)
leg.get_frame().set_linewidth(0.9)
leg.get_frame().set_edgecolor("#BBBBBB")
leg.get_frame().set_facecolor("#FCFCFC")
leg.get_frame().set_alpha(0.95)

saved = fs.finalize_figure(fig, OUT / "fig1_er_diagram", formats=["png", "pdf"], dpi=300)
for p in saved:
    print("saved", p)
