# -*- coding: utf-8 -*-
"""图2 图书管理系统数据流图（顶层图）与 图3 第1层展开图。

符号约定（软件工程教材通用记法）：
  矩形(左边框加粗) = 外部实体； 圆角矩形 = 加工；
  开口矩形 = 数据存储；        带箭头线段 = 数据流。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse

import figstyle as fs

OUT = Path(r"C:\Users\LZ\Desktop\软工\figures")
fs.apply_publication_style(fs.FigureStyle(font_size=13, axes_linewidth=1.8))


def poly_arrow(ax, pts, label=None, lw=1.6, color="#4A4A4A", fontsize=10.5,
               label_pos=None):
    """折线数据流箭头：中间各段为直线，最后一段带箭头。"""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    if len(pts) > 2:
        ax.plot(xs[:-1], ys[:-1], color=color, linewidth=lw, zorder=3,
                solid_capstyle="round", solid_joinstyle="round")
    ax.annotate("", xy=pts[-1], xytext=pts[-2],
                arrowprops=dict(arrowstyle="->", color=color, linewidth=lw,
                                shrinkA=0, shrinkB=0), zorder=3)
    if label:
        mx, my = label_pos
        ax.text(mx, my, label, ha="center", va="center", fontsize=fontsize,
                color="#1A1A1A", zorder=6,
                bbox=dict(boxstyle="round,pad=0.16", facecolor="white",
                          edgecolor="none", alpha=0.95))


def flow(ax, a, b, label=None, rad=0.0, both=False, offset=(0, 0.28),
         fontsize=10.5, lw=1.5):
    fs.draw_arrow(ax, a, b, label=label, rad=rad, both=both, lw=lw,
                  label_offset=offset, fontsize=fontsize)


# =========================================================================
# 图2  顶层数据流图
# =========================================================================
fig, ax = plt.subplots(figsize=(11.6, 5.4))
fs.blank_axes(ax, (-0.4, 16.4), (0.6, 7.6))

fs.draw_external(ax, 2.4, 4.1, "图书管理员", w=2.9, h=1.15, fontsize=13.5)
fs.draw_external(ax, 13.6, 4.1, "读者", w=2.9, h=1.15, fontsize=13.5)

ax.add_patch(Ellipse((8.0, 4.1), 4.4, 3.0, facecolor="#EAF1FA",
                     edgecolor=fs.PALETTE["blue_main"], linewidth=2.2, zorder=4))
ax.text(8.0, 4.62, "0", ha="center", va="center", fontsize=12,
        color=fs.PALETTE["blue_main"], zorder=5)
ax.text(8.0, 4.05, "图书管理系统", ha="center", va="center", fontsize=13.5,
        color="#0B2E5C", zorder=5, fontweight="bold")

poly_arrow(ax, [(3.85, 4.85), (5.85, 4.85)], label="图书信息 / 读者信息 / 借还书办理",
           label_pos=(4.85, 5.38))
poly_arrow(ax, [(5.85, 3.35), (3.85, 3.35)], label="处理结果 / 统计报表",
           label_pos=(4.85, 2.82))
poly_arrow(ax, [(12.15, 4.85), (10.15, 4.85)], label="借书申请 / 还书申请 / 查询请求",
           label_pos=(11.15, 5.38))
poly_arrow(ax, [(10.15, 3.35), (12.15, 3.35)], label="借阅结果 / 查询结果",
           label_pos=(11.15, 2.82))

handles = [
    Line2D([], [], marker="s", linestyle="none", markersize=12,
           markerfacecolor="#F3F3F3", markeredgecolor="#5A5A5A", label="外部实体"),
    Line2D([], [], marker="o", linestyle="none", markersize=13,
           markerfacecolor="#EAF1FA", markeredgecolor=fs.PALETTE["blue_main"], label="加工（系统）"),
]
leg = ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.02),
                fontsize=11, ncol=2, handletextpad=0.6, columnspacing=2.0)
leg.get_frame().set_linewidth(0.9)
leg.get_frame().set_edgecolor("#BBBBBB")

for p in fs.finalize_figure(fig, OUT / "fig2_dfd_top", formats=["png", "pdf"], dpi=300):
    print("saved", p)

# =========================================================================
# 图3  第1层数据流图（展开图）
# =========================================================================
fig, ax = plt.subplots(figsize=(13.4, 8.8))
fs.blank_axes(ax, (-0.1, 17.7), (0.2, 11.6))

admin = fs.draw_external(ax, 2.30, 8.60, "图书管理员", w=2.50, h=1.10, fontsize=12.5)
reader = fs.draw_external(ax, 2.30, 3.20, "读者", w=2.50, h=1.10, fontsize=12.5)

p1 = fs.draw_process(ax, 6.60, 10.20, "图书信息管理", w=3.00, h=1.10, number="1", fontsize=12)
p2 = fs.draw_process(ax, 6.60, 7.50, "读者信息管理", w=3.00, h=1.10, number="2", fontsize=12)
p3 = fs.draw_process(ax, 6.60, 4.80, "借阅管理", w=3.00, h=1.10, number="3", fontsize=12)
p4 = fs.draw_process(ax, 6.60, 1.60, "查询与统计", w=3.00, h=1.60, number="4", fontsize=12)

d1 = fs.draw_store(ax, 12.20, 10.20, "图书表", w=3.20, h=0.90, sid="D1", fontsize=12)
d2 = fs.draw_store(ax, 12.20, 7.50, "读者表", w=3.20, h=0.90, sid="D2", fontsize=12)
d3 = fs.draw_store(ax, 12.20, 4.80, "借阅表", w=3.20, h=0.90, sid="D3", fontsize=12)

# --- 外部实体 <-> 加工 ---
flow(ax, admin, p1, "图书信息", offset=(0, 0.30))
flow(ax, admin, p2, "读者信息", offset=(0, 0.30))
flow(ax, admin, p3, "借还书办理", offset=(0.55, -0.30))
flow(ax, reader, p3, "借书 / 还书申请", offset=(0.30, 0.32))
flow(ax, reader, p4, "查询请求", rad=0.16, offset=(-0.10, -0.55))
flow(ax, p4, reader, "查询结果", rad=0.16, offset=(-0.10, 0.62))

# --- 加工 <-> 数据存储（读写） ---
flow(ax, p1, d1, "图书数据", both=True, offset=(0, 0.30))
flow(ax, p2, d2, "读者数据", both=True, offset=(0, 0.30))
flow(ax, p3, d3, "借阅记录", both=True, offset=(0, 0.30))

# --- 加工3 读取存储做校验：标签落在加工列与存储列之间的空档 ---
flow(ax, d1, p3, "图书信息校验", rad=-0.30, offset=(0.05, 0.32))
flow(ax, d2, p3, "读者资格校验", rad=-0.20, offset=(0.12, -0.30))

# --- 数据存储 -> 加工4：嵌套 L 形走线，外层通道下探最深，互不交叉 ---
poly_arrow(ax, [(13.80, 10.20), (17.00, 10.20), (17.00, 0.90), (8.10, 0.90)],
           label="读取图书数据", label_pos=(12.05, 1.20))
poly_arrow(ax, [(13.80, 7.50), (16.10, 7.50), (16.10, 1.50), (8.10, 1.50)],
           label="读取读者数据", label_pos=(11.00, 1.80))
poly_arrow(ax, [(13.80, 4.80), (15.20, 4.80), (15.20, 2.10), (8.10, 2.10)],
           label="读取借阅数据", label_pos=(9.95, 2.40))

# --- 加工4 -> 图书管理员：统计报表（沿最左侧通道绕行） ---
poly_arrow(ax, [(5.10, 1.15), (0.65, 1.15), (0.65, 9.15), (1.05, 9.15)],
           label="统计报表", label_pos=(1.45, 5.60))

handles = [
    Line2D([], [], marker="s", linestyle="none", markersize=12,
           markerfacecolor="#F3F3F3", markeredgecolor="#5A5A5A", label="外部实体"),
    Line2D([], [], marker="s", linestyle="none", markersize=12,
           markerfacecolor="#EAF1FA", markeredgecolor=fs.PALETTE["blue_main"], label="加工"),
    Line2D([], [], marker="s", linestyle="none", markersize=12,
           markerfacecolor="#FFFFFF", markeredgecolor="#6A6A6A", label="数据存储"),
]
leg = ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.03),
                fontsize=11, ncol=3, handletextpad=0.6, columnspacing=2.2)
leg.get_frame().set_linewidth(0.9)
leg.get_frame().set_edgecolor("#BBBBBB")

for p in fs.finalize_figure(fig, OUT / "fig3_dfd_level1", formats=["png", "pdf"], dpi=300):
    print("saved", p)
