# -*- coding: utf-8 -*-
"""实验二 插图：功能结构图、分层体系结构图、程序流程图。

沿用 scientific-figure-making 技能规定的版面风格（figstyle.py）。
绘制完成后用渲染器计算每个文本对象的外接矩形，自动检查是否有重叠。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle

import figstyle as fs

OUT = Path(r"C:\Users\LZ\Desktop\软工\figures")
fs.apply_publication_style(fs.FigureStyle(font_size=12, axes_linewidth=1.6))

BOXES = []


def R(x, y, w, h):
    r = (x - w / 2, y - h / 2, w, h)
    BOXES.append(r)
    return r


def rect(ax, x, y, text, w=2.6, h=0.66, fc="#EAF1FA", ec=None, fs_=12,
         bold=False, color="#0B2E5C", radius=0.06):
    ec = ec or fs.PALETTE["blue_main"]
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.01,rounding_size=%.2f" % radius,
                                facecolor=fc, edgecolor=ec, linewidth=1.5, zorder=4))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs_, zorder=5,
            color=color, fontweight="bold" if bold else "normal")
    return R(x, y, w, h)


def terminator(ax, x, y, text, w=2.2, h=0.7, fs_=12):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.01,rounding_size=%.34",
                                facecolor="#E8F5E9", edgecolor="#2E7D32",
                                linewidth=1.6, zorder=4))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs_, zorder=5,
            color="#1B5E20", fontweight="bold")
    return R(x, y, w, h)


def decision(ax, x, y, text, w=4.4, h=1.5, fs_=11):
    pts = [(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)]
    ax.add_patch(Polygon(pts, closed=True, facecolor="#FDF3D8", edgecolor="#B8860B",
                         linewidth=1.6, zorder=4))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs_, zorder=5, color="#7A5B00")
    return R(x, y, w, h)


def arrow(ax, p0, p1, label=None, lw=1.5, color="#4A4A4A", rad=0.0, lpos=None,
          fs_=10.5, dashes=False):
    ax.annotate("", xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle="-|>", color=color, linewidth=lw,
                                shrinkA=0, shrinkB=0,
                                linestyle="--" if dashes else "-",
                                connectionstyle="arc3,rad=%.2f" % rad), zorder=3)
    if label:
        mx, my = lpos if lpos else ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs_, color="#1A1A1A",
                zorder=6, bbox=dict(boxstyle="round,pad=0.16", facecolor="white",
                                    edgecolor="none", alpha=0.94))


def canvas(figsize, xlim, ylim):
    fig, ax = plt.subplots(figsize=figsize)
    fs.blank_axes(ax, xlim, ylim)
    return fig, ax


def check_overlaps(fig, ax, title):
    """用渲染器计算文本外接矩形，报告相互重叠的文本对。"""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    items = [(t.get_text(), t.get_window_extent(renderer)) for t in ax.texts if t.get_text()]
    bad = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i][1], items[j][1]
            if a.overlaps(b):
                ox = min(a.x1, b.x1) - max(a.x0, b.x0)
                oy = min(a.y1, b.y1) - max(a.y0, b.y0)
                if ox > 2 and oy > 2:
                    print("   [重叠] %r <-> %r  (%.0f x %.0f px)" % (items[i][0], items[j][0], ox, oy))
                    bad += 1
    print("%s : %d 个文本对象, %d 处重叠" % (title, len(items), bad))
    return bad


# =====================================================================
# 图1  系统功能结构图
# =====================================================================
BOXES.clear()
fig, ax = canvas((12.6, 7.2), (-0.2, 17.0), (6.3, 11.9))

rect(ax, 8.5, 11.20, "图书管理系统", w=4.6, h=0.86, fc="#0F4D92",
     ec="#0B2E5C", fs_=15, bold=True, color="white")

MODULES = [
    (2.30, "图书信息管理", ["录入图书", "修改图书", "删除图书", "查询图书"]),
    (6.35, "读者信息管理", ["录入读者", "修改读者", "删除读者", "查询读者"]),
    (10.40, "借阅管理", ["办理借书", "办理还书", "借阅明细", "未还清单"]),
    (14.45, "统计查询", ["借阅排行", "读者统计", "出版社统计", "月度趋势"]),
]

BUS = 10.18
ax.plot([MODULES[0][0], MODULES[-1][0]], [BUS, BUS], color="#4A4A4A", linewidth=1.5, zorder=2)
arrow(ax, (8.5, 10.77), (8.5, BUS), lw=1.5)

for cx, name, subs in MODULES:
    arrow(ax, (cx, BUS), (cx, 9.66), lw=1.5)
    top = 9.22
    h = 0.66 + len(subs) * 0.50
    ax.add_patch(FancyBboxPatch((cx - 1.78, top - h), 3.56, h,
                                boxstyle="round,pad=0.01,rounding_size=0.08",
                                facecolor="#FFFFFF", edgecolor="#9AA5B1",
                                linewidth=1.4, zorder=3))
    ax.add_patch(Rectangle((cx - 1.78, top - 0.66), 3.56, 0.66,
                           facecolor=fs.PALETTE["blue_main"], edgecolor="none", zorder=4))
    ax.text(cx, top - 0.33, name, ha="center", va="center", fontsize=12.5,
            color="white", fontweight="bold", zorder=5)
    for k, s in enumerate(subs):
        y = top - 0.66 - (k + 0.5) * 0.50
        ax.plot([cx - 1.72, cx - 1.52], [y, y], color="#8BCF8B", linewidth=3, zorder=5)
        ax.text(cx - 1.38, y, s, ha="left", va="center", fontsize=11.5,
                color="#333333", zorder=5)

check_overlaps(fig, ax, "图1 功能结构图")
for p in fs.finalize_figure(fig, OUT / "figA1_function_structure", formats=["png", "pdf"], dpi=300):
    print("saved", p)

# =====================================================================
# 图2  程序分层体系结构图
# =====================================================================
BOXES.clear()
fig, ax = canvas((12.6, 8.4), (-0.2, 16.4), (0.4, 10.4))


def layer(y, h, title, items, fc, ec, tc, item_fc="#FFFFFF"):
    ax.add_patch(FancyBboxPatch((0.6, y - h / 2), 15.0, h,
                                boxstyle="round,pad=0.01,rounding_size=0.10",
                                facecolor=fc, edgecolor=ec, linewidth=1.8, zorder=3))
    ax.text(1.85, y, title, ha="center", va="center", fontsize=13, color=tc,
            fontweight="bold", zorder=5)
    n = len(items)
    x0, x1 = 3.9, 15.1
    slot = (x1 - x0) / n
    for i, it in enumerate(items):
        cx = x0 + slot * (i + 0.5)
        w = min(slot - 0.22, 2.8)
        ax.add_patch(FancyBboxPatch((cx - w / 2, y - 0.42), w, 0.84,
                                    boxstyle="round,pad=0.01,rounding_size=0.07",
                                    facecolor=item_fc, edgecolor=ec, linewidth=1.2, zorder=4))
        ax.text(cx, y, it, ha="center", va="center", fontsize=10.5, color="#0B2E5C", zorder=5)


layer(9.30, 1.44, "表\n示\n层",
      ["MainFrame", "BookPanel", "ReaderPanel", "BorrowPanel", "StatPanel"],
      "#EAF1FA", fs.PALETTE["blue_main"], "#0B2E5C")
layer(7.05, 1.06, "业务\n逻辑层", ["LibraryService（业务校验 / 异常转换）"],
      "#EAF6EC", "#2E7D32", "#1B5E20")
layer(4.80, 1.06, "数据\n访问层", ["BookDao", "ReaderDao", "BorrowDao", "StatDao"],
      "#FDF3D8", "#B8860B", "#7A5B00")
layer(2.05, 1.90, "数\n据\n库\n层",
      ["基本表\nbook / reader / borrow", "视图\nv_borrow_detail 等",
       "触发器\ntrg_borrow_before_insert", "存储过程\nsp_book_insert 等"],
      "#F3F3F3", "#5A5A5A", "#333333")

arrow(ax, (14.35, 8.58), (14.35, 7.58), rad=0.0)
ax.text(15.25, 8.08, "调用\n返回", ha="center", va="center", fontsize=10, color="#333333", zorder=6)
arrow(ax, (14.35, 6.52), (14.35, 5.33))
ax.text(15.25, 5.93, "业务方法", ha="center", va="center", fontsize=10, color="#333333", zorder=6)
arrow(ax, (14.35, 4.27), (14.35, 3.00))
ax.text(15.15, 3.63, "JDBC\nSQL", ha="center", va="center", fontsize=10, color="#B64342", zorder=6)

check_overlaps(fig, ax, "图2 分层体系结构图")
for p in fs.finalize_figure(fig, OUT / "figA2_architecture", formats=["png", "pdf"], dpi=300):
    print("saved", p)
