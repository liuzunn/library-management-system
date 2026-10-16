# -*- coding: utf-8 -*-
"""图4 图书管理系统数据库表结构（逻辑结构 / 外键联系）图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

import figstyle as fs

OUT = Path(r"C:\Users\LZ\Desktop\软工\figures")
fs.apply_publication_style(fs.FigureStyle(font_size=12, axes_linewidth=1.6))

ROW_H, HEAD_H = 0.60, 0.74


def draw_table(ax, x_left, y_top, w, title, cn, cols):
    """绘制一张表：表头 + 字段行。cols 元素为 (字段名, 类型, 键标记)。"""
    n = len(cols)
    h = HEAD_H + n * ROW_H
    y_bot = y_top - h

    ax.add_patch(FancyBboxPatch((x_left, y_bot), w, h,
                                boxstyle="round,pad=0.0,rounding_size=0.12",
                                facecolor="#FFFFFF", edgecolor="#9AA5B1",
                                linewidth=1.5, zorder=3))
    ax.add_patch(plt.Rectangle((x_left, y_top - HEAD_H), w, HEAD_H,
                               facecolor=fs.PALETTE["blue_main"], edgecolor="none",
                               zorder=4))
    ax.text(x_left + 0.24, y_top - HEAD_H / 2, title, ha="left", va="center",
            fontsize=13, color="white", fontweight="bold", zorder=5)
    ax.text(x_left + w - 0.24, y_top - HEAD_H / 2, cn, ha="right", va="center",
            fontsize=11, color="#D8E4F5", zorder=5)

    centers = {}
    for i, (name, dtype, key) in enumerate(cols):
        y_c = y_top - HEAD_H - (i + 0.5) * ROW_H
        centers[name] = y_c
        if i % 2 == 1:
            ax.add_patch(plt.Rectangle((x_left, y_c - ROW_H / 2), w, ROW_H,
                                       facecolor="#F4F7FB", edgecolor="none", zorder=3.5))
        ax.plot([x_left + 0.06, x_left + w - 0.06], [y_c - ROW_H / 2] * 2,
                color="#E3E8EF", linewidth=0.8, zorder=4)
        ax.text(x_left + 0.26, y_c, name, ha="left", va="center", fontsize=11.5,
                color="#0B2E5C" if key else "#333333",
                fontweight="bold" if key else "normal", zorder=5)
        if key:
            ax.text(x_left + 1.62, y_c, key, ha="left", va="center", fontsize=9.5,
                    color="#B8860B", fontweight="bold", zorder=5)
        ax.text(x_left + w - 0.24, y_c, dtype, ha="right", va="center", fontsize=10,
                color="#7A8699", zorder=5)
    ax.plot([x_left + 0.06, x_left + w - 0.06], [y_top - HEAD_H] * 2,
            color="#9AA5B1", linewidth=1.2, zorder=5)
    return dict(x_left=x_left, x_right=x_left + w, y_top=y_top, y_bot=y_bot,
                w=w, h=h, centers=centers)


def rel(ax, pts, label_from, label_to, fontsize=11.5):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs[:-1], ys[:-1], color="#B64342", linewidth=1.6, zorder=2,
            solid_capstyle="round", solid_joinstyle="round")
    ax.annotate("", xy=pts[-1], xytext=pts[-2],
                arrowprops=dict(arrowstyle="->", color="#B64342", linewidth=1.6,
                                shrinkA=0, shrinkB=0), zorder=2)
    ax.text(pts[0][0] + 0.30, pts[0][1] + 0.26, label_from, fontsize=fontsize,
            color="#B64342", fontweight="bold", ha="center", va="center", zorder=6,
            bbox=dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="none"))
    ax.text(pts[-1][0] - 0.34, pts[-1][1] + 0.26, label_to, fontsize=fontsize,
            color="#B64342", fontweight="bold", ha="center", va="center", zorder=6,
            bbox=dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="none"))


fig, ax = plt.subplots(figsize=(12.4, 8.6))
fs.blank_axes(ax, (0.2, 17.8), (0.9, 12.4))

book = draw_table(ax, 1.30, 11.60, 5.00, "book", "图书表", [
    ("书号", "VARCHAR(20)", "PK"),
    ("书名", "VARCHAR(120)", ""),
    ("作者", "VARCHAR(60)", ""),
    ("价格", "DECIMAL(8,2)", ""),
    ("出版社", "VARCHAR(80)", ""),
    ("摘要", "VARCHAR(500)", ""),
])

reader = draw_table(ax, 1.30, 5.90, 5.00, "reader", "读者表", [
    ("卡号", "VARCHAR(20)", "PK"),
    ("姓名", "VARCHAR(30)", ""),
    ("性别", "ENUM('男','女')", ""),
    ("单位", "VARCHAR(80)", ""),
    ("类型", "VARCHAR(20)", ""),
    ("级别", "VARCHAR(20)", ""),
])

borrow = draw_table(ax, 11.20, 8.80, 5.70, "borrow", "借阅表", [
    ("书号", "VARCHAR(20)", "PK,FK"),
    ("卡号", "VARCHAR(20)", "PK,FK"),
    ("借书时间", "DATE", "PK"),
    ("还书时间", "DATE", ""),
])

# book(1) —— borrow(N)
rel(ax, [(book["x_right"], book["centers"]["书号"]), (8.85, book["centers"]["书号"]),
         (8.85, borrow["centers"]["书号"]), (borrow["x_left"], borrow["centers"]["书号"])],
    "1", "N")
# reader(1) —— borrow(N)
rel(ax, [(reader["x_right"], reader["centers"]["卡号"]), (9.90, reader["centers"]["卡号"]),
         (9.90, borrow["centers"]["卡号"]), (borrow["x_left"], borrow["centers"]["卡号"])],
    "1", "N")

ax.text(8.42, 9.05, "外码约束  fk_borrow_book", fontsize=10.5, color="#B64342",
        ha="center", va="center", rotation=90)
ax.text(10.38, 3.60, "外码约束  fk_borrow_reader", fontsize=10.5, color="#B64342",
        ha="center", va="center", rotation=90)

handles = [
    Line2D([], [], marker="s", linestyle="none", markersize=12,
           markerfacecolor=fs.PALETTE["blue_main"], markeredgecolor="none", label="表名 / 中文名"),
    Line2D([], [], marker="s", linestyle="none", markersize=12,
           markerfacecolor="white", markeredgecolor="#9AA5B1", label="字段行"),
    Line2D([], [], color="#B64342", linewidth=2.0, label="外键联系（1:N）"),
]
leg = ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.02),
                fontsize=11, ncol=3, handletextpad=0.8, columnspacing=2.4)
leg.get_frame().set_linewidth(0.9)
leg.get_frame().set_edgecolor("#BBBBBB")

for p in fs.finalize_figure(fig, OUT / "fig4_schema", formats=["png", "pdf"], dpi=300):
    print("saved", p)
