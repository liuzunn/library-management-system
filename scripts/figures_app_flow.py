# -*- coding: utf-8 -*-
"""实验二 插图：图书信息录入流程图、借书业务流程图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

import figstyle as fs

OUT = Path(r"C:\Users\LZ\Desktop\软工\figures")
fs.apply_publication_style(fs.FigureStyle(font_size=12, axes_linewidth=1.6))


def rect(ax, x, y, text, w=2.6, h=0.66, fc="#EAF1FA", ec=None, fs_=11.5,
         bold=False, color="#0B2E5C"):
    ec = ec or fs.PALETTE["blue_main"]
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.01,rounding_size=0.07",
                                facecolor=fc, edgecolor=ec, linewidth=1.5, zorder=4))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs_, zorder=5,
            color=color, fontweight="bold" if bold else "normal")


def term(ax, x, y, text, w=2.3, h=0.68, fs_=12):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.01,rounding_size=0.33",
                                facecolor="#E8F5E9", edgecolor="#2E7D32",
                                linewidth=1.6, zorder=4))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs_, zorder=5,
            color="#1B5E20", fontweight="bold")


def dec(ax, x, y, text, w=4.6, h=1.7, fs_=11):
    pts = [(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)]
    ax.add_patch(Polygon(pts, closed=True, facecolor="#FDF3D8", edgecolor="#B8860B",
                         linewidth=1.6, zorder=4))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs_, zorder=5, color="#7A5B00")


def arrow(ax, p0, p1, label=None, lpos=None, lw=1.5, color="#4A4A4A", fs_=10.5):
    ax.annotate("", xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle="-|>", color=color, linewidth=lw,
                                shrinkA=0, shrinkB=0), zorder=3)
    if label:
        mx, my = lpos if lpos else ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs_, color="#B64342",
                zorder=6, bbox=dict(boxstyle="round,pad=0.14", facecolor="white",
                                    edgecolor="none", alpha=0.95))


def seg(ax, pts, lw=1.5, color="#4A4A4A"):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=color, linewidth=lw, zorder=3, solid_capstyle="round",
            solid_joinstyle="round")


def check(fig, ax, title):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    items = [(t.get_text(), t.get_window_extent(r)) for t in ax.texts if t.get_text()]
    bad = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i][1], items[j][1]
            if a.overlaps(b):
                ox = min(a.x1, b.x1) - max(a.x0, b.x0)
                oy = min(a.y1, b.y1) - max(a.y0, b.y0)
                if ox > 2 and oy > 2:
                    print("   [重叠] %r <-> %r (%.0f x %.0f)" % (items[i][0], items[j][0], ox, oy))
                    bad += 1
    print("%s : %d 个文本, %d 处重叠" % (title, len(items), bad))
    return bad


# =====================================================================
# 图3  图书信息录入流程图
# =====================================================================
fig, ax = plt.subplots(figsize=(9.4, 11.6))
fs.blank_axes(ax, (-0.4, 11.7), (4.6, 16.2))

term(ax, 3.2, 15.35, "开始")
rect(ax, 3.2, 14.00, "输入图书信息：书号、书名、作者、价格、出版社、摘要", w=4.7, h=0.72)
dec(ax, 3.2, 12.20, "必填项是否完整、价格是否为合法数字？", w=4.7, h=1.70)
rect(ax, 3.2, 10.20, "组装 Book 对象，调用 LibraryService.addBook()\n（内部调用存储过程 sp_book_insert）",
     w=4.7, h=0.88)
dec(ax, 3.2, 8.30, "数据库是否接受？\n（主键是否重复、取值是否合法）", w=4.7, h=1.80)
rect(ax, 3.2, 6.50, "提示“图书录入成功”，清空表单并刷新图书列表", w=4.7, h=0.72)
term(ax, 3.2, 5.40, "结束")

arrow(ax, (3.2, 15.01), (3.2, 14.36))
arrow(ax, (3.2, 13.64), (3.2, 13.05))
arrow(ax, (3.2, 11.35), (3.2, 10.64), "是", lpos=(3.62, 11.00))
arrow(ax, (3.2, 9.76), (3.2, 9.20))
arrow(ax, (3.2, 7.40), (3.2, 6.86), "是", lpos=(3.62, 7.13))
arrow(ax, (3.2, 6.14), (3.2, 5.74))

rect(ax, 7.95, 12.20, "提示：输入不合法，请重新填写", w=3.5, h=0.70, fc="#FDECEA", ec="#B64342")
arrow(ax, (5.55, 12.20), (6.20, 12.20), "否", lpos=(5.85, 12.55))
seg(ax, [(9.70, 12.20), (9.95, 12.20), (9.95, 14.18), (5.55, 14.18)])
arrow(ax, (9.95, 14.18), (5.62, 14.18))

rect(ax, 7.95, 8.30, "提示：录入失败，显示数据库返回的错误信息", w=3.9, h=0.70, fc="#FDECEA", ec="#B64342")
arrow(ax, (5.55, 8.30), (6.00, 8.30), "否", lpos=(5.80, 8.66))
seg(ax, [(9.90, 8.30), (10.75, 8.30), (10.75, 13.82), (5.55, 13.82)])
arrow(ax, (10.75, 13.82), (5.62, 13.82))

check(fig, ax, "图3 图书信息录入流程图")
for p in fs.finalize_figure(fig, OUT / "figA3_flow_book_insert", formats=["png", "pdf"], dpi=300):
    print("saved", p)

# =====================================================================
# 图4  借书业务流程图
# =====================================================================
fig, ax = plt.subplots(figsize=(9.8, 11.0))
fs.blank_axes(ax, (-0.4, 11.9), (4.7, 16.1))

term(ax, 3.0, 15.30, "开始")
rect(ax, 3.0, 14.15, "输入书号、卡号、借书日期", w=4.6, h=0.70)
rect(ax, 3.0, 12.95, "调用存储过程 sp_borrow_book(书号, 卡号, 借书日期)", w=4.8, h=0.70)
dec(ax, 3.0, 11.15, "触发器校验是否通过？\n（还书时间不早于借书时间，\n且该图书当前未借出）",
    w=4.8, h=2.10)
dec(ax, 3.0, 8.60, "外键校验是否通过？\n（书号、卡号必须已存在）", w=4.8, h=1.80)
rect(ax, 3.0, 6.55, "写入 borrow 表；提示“借书成功”；\n刷新借阅明细与未归还清单", w=4.8, h=0.92)
term(ax, 3.0, 5.35, "结束")

arrow(ax, (3.0, 14.96), (3.0, 14.50))
arrow(ax, (3.0, 13.80), (3.0, 13.30))
arrow(ax, (3.0, 12.60), (3.0, 12.20))
arrow(ax, (3.0, 10.10), (3.0, 9.50), "是", lpos=(3.42, 9.80))
arrow(ax, (3.0, 7.70), (3.0, 7.01), "是", lpos=(3.42, 7.35))
arrow(ax, (3.0, 6.09), (3.0, 5.69))

rect(ax, 8.90, 11.15, "Java 端捕获 SQLException\n弹出错误提示对话框", w=3.8, h=0.92,
     fc="#FDECEA", ec="#B64342")
term(ax, 8.90, 9.60, "结束（借书失败）", w=3.2, h=0.72)
arrow(ax, (5.40, 11.15), (7.00, 11.15), "否", lpos=(6.20, 11.52))
arrow(ax, (8.90, 10.69), (8.90, 9.96))
seg(ax, [(5.40, 8.60), (11.40, 8.60), (11.40, 11.15)])
arrow(ax, (11.40, 11.15), (10.80, 11.15), "否", lpos=(6.25, 8.96))

check(fig, ax, "图4 借书业务流程图")
for p in fs.finalize_figure(fig, OUT / "figA4_flow_borrow", formats=["png", "pdf"], dpi=300):
    print("saved", p)
