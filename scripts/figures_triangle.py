# -*- coding: utf-8 -*-
"""实验三 图B1：三角形判定程序流程图。

绘图风格复用 scripts/figstyle.py 与 scripts/figures_app_flow.py：
椭圆=起止、平行四边形=输入/输出、菱形=判断（本程序无独立的多步计算，
故不出现矩形处理符号）。判断顺序与 TriangleClassifier.classify() 逐句对应：
先范围、再三角形不等式、再“三边全等”→等边、“恰有两边相等”→等腰、否则一般。

输出：figures/figB1_triangle_flow.png（300 dpi）+ figures/figB1_triangle_flow.pdf

运行（在项目根目录）：
    D:/anaconda3/python.exe scripts/figures_triangle.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon

import figstyle as fs

OUT = Path(__file__).resolve().parent.parent / "figures"

fs.apply_publication_style(fs.FigureStyle(font_size=10.5, axes_linewidth=1.2))

# 图为约 4.8 英寸宽（300 dpi），10 pt 标签在 Word 中与正文可比
FS_MAIN = 10.0
LW = 1.7
EDGE = "#4A4A4A"

# (patch, text) 配对，供布局自检使用
NODES = []


def ellipse(ax, x, y, text, w=2.2, h=0.64):
    """起止：椭圆。"""
    patch = Ellipse((x, y), w, h, facecolor="#E8F5E9", edgecolor="#2E7D32",
                    linewidth=LW, zorder=4)
    ax.add_patch(patch)
    artist = ax.text(x, y, text, ha="center", va="center", fontsize=FS_MAIN, zorder=5,
                     color="#1B5E20", fontweight="bold")
    NODES.append((patch, artist))


def para(ax, x, y, text, w=3.3, h=0.66, skew=0.30):
    """输入/输出：平行四边形。"""
    pts = [(x - w / 2 + skew, y - h / 2), (x + w / 2, y - h / 2),
           (x + w / 2 - skew, y + h / 2), (x - w / 2, y + h / 2)]
    patch = Polygon(pts, closed=True, facecolor="#EAF1FA", edgecolor=fs.PALETTE["blue_main"],
                    linewidth=LW, zorder=4)
    ax.add_patch(patch)
    artist = ax.text(x, y, text, ha="center", va="center", fontsize=FS_MAIN, zorder=5,
                     color="#0B2E5C")
    NODES.append((patch, artist))


def dec(ax, x, y, text, w=4.6, h=1.6):
    """判断：菱形。"""
    pts = [(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)]
    patch = Polygon(pts, closed=True, facecolor="#FDF3D8", edgecolor="#B8860B",
                    linewidth=LW, zorder=4)
    ax.add_patch(patch)
    artist = ax.text(x, y, text, ha="center", va="center", fontsize=FS_MAIN, zorder=5,
                     color="#7A5B00", linespacing=1.25)
    NODES.append((patch, artist))


def arrow(ax, p0, p1, label=None, lpos=None, fs_=FS_MAIN):
    """带箭头连线；label 为“是/否”，lpos 为文字中心。"""
    ax.annotate("", xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle="-|>", color=EDGE, linewidth=1.55,
                                shrinkA=0, shrinkB=0), zorder=3)
    if label:
        mx, my = lpos if lpos else ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs_, color="#B64342",
                zorder=6, bbox=dict(boxstyle="round,pad=0.10", facecolor="white",
                                    edgecolor="none", alpha=0.95))


def seg(ax, pts):
    """折线（无箭头）。"""
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=EDGE, linewidth=1.55,
            zorder=3, solid_capstyle="round", solid_joinstyle="round")


def check(fig, ax, title):
    """布局自检：文本两两不重叠、图形两两不重叠、节点文字不越出所在图形。"""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bad = 0

    texts = [(t.get_text(), t.get_window_extent(renderer)) for t in ax.texts if t.get_text()]
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            a, b = texts[i][1], texts[j][1]
            if a.overlaps(b):
                ox = min(a.x1, b.x1) - max(a.x0, b.x0)
                oy = min(a.y1, b.y1) - max(a.y0, b.y0)
                if ox > 1.5 and oy > 1.5:
                    print("   [文本重叠] %r <-> %r (%.1f x %.1f px)" % (texts[i][0], texts[j][0], ox, oy))
                    bad += 1

    patches = list(ax.patches)
    for i in range(len(patches)):
        for j in range(i + 1, len(patches)):
            a = patches[i].get_window_extent(renderer)
            b = patches[j].get_window_extent(renderer)
            if a.overlaps(b):
                ox = min(a.x1, b.x1) - max(a.x0, b.x0)
                oy = min(a.y1, b.y1) - max(a.y0, b.y0)
                if ox > 1.0 and oy > 1.0:
                    print("   [图形重叠] patch#%d <-> patch#%d (%.1f x %.1f px)" % (i, j, ox, oy))
                    bad += 1

    # 节点文字必须完整落在所属图形内部（四角判定）
    for patch, artist in NODES:
        ext = artist.get_window_extent(renderer)
        path = patch.get_path().transformed(patch.get_patch_transform() + ax.transData)
        corners = [(ext.x0, ext.y0), (ext.x0, ext.y1), (ext.x1, ext.y0), (ext.x1, ext.y1)]
        if not all(path.contains_points(corners)):
            print("   [文字越界] %r 超出所在图形" % artist.get_text())
            bad += 1

    print("%s : %d 个文本, %d 个图形, %d 处问题" % (title, len(texts), len(patches), bad))
    return bad


# =====================================================================
# 图B1  三角形判定程序流程图
# =====================================================================
fig, ax = plt.subplots(figsize=(6.1, 8.58))
fs.blank_axes(ax, (2.0, 12.95), (1.0, 16.3))

X = 4.5          # 主流程列
RX = 10.05       # 右侧输出列
BUS = 12.6       # 输出汇流总线

# ---- 主流程 ----
ellipse(ax, X, 15.75, "开始")
para(ax, X, 14.68, "输入三个整数 a、b、c", w=4.5, h=0.70)
dec(ax, X, 13.055, "输入是否为\n3 个整数？", w=4.6, h=1.55)
dec(ax, X, 10.98, "三边是否均在\n1~100 范围内？", w=4.8, h=1.60)
dec(ax, X, 8.755, "任意两边之和\n是否大于第三边？", w=4.9, h=1.85)
dec(ax, X, 6.355, "三边是否\n全等？", w=4.2, h=1.45)
dec(ax, X, 4.355, "是否恰有\n两边相等？", w=4.2, h=1.45)
para(ax, X, 2.75, "输出：一般三角形", w=3.6, h=0.66)
ellipse(ax, X, 1.55, "结束")

# ---- 右侧输出分支 ----
para(ax, RX, 13.055, "输出：输入格式错误", w=4.0, h=0.80)
para(ax, RX, 10.98, "输出：输入越界", w=3.5, h=0.66)
para(ax, RX, 8.755, "输出：不构成三角形", w=4.0, h=0.66)
para(ax, RX, 6.355, "输出：等边三角形", w=3.7, h=0.66)
para(ax, RX, 4.355, "输出：等腰三角形", w=3.7, h=0.66)

# ---- 主流程连线 ----
arrow(ax, (X, 15.43), (X, 15.03))                        # 开始 -> 输入
arrow(ax, (X, 14.33), (X, 13.83))                        # 输入 -> 格式判断
arrow(ax, (X, 12.28), (X, 11.78), "是", (4.93, 12.03))    # D0 是 -> D1
arrow(ax, (X, 10.18), (X, 9.68), "是", (4.93, 9.93))      # D1 是 -> D2
arrow(ax, (X, 7.83), (X, 7.08), "是", (4.93, 7.455))      # D2 是 -> D3
arrow(ax, (X, 5.63), (X, 5.08), "否", (4.93, 5.355))      # D3 否 -> D4
arrow(ax, (X, 3.63), (X, 3.08), "否", (4.93, 3.355))      # D4 否 -> 一般输出
arrow(ax, (X, 2.42), (X, 1.87))                          # 一般输出 -> 结束

# ---- 判定分支：向右到输出平行四边形 ----
arrow(ax, (6.80, 13.055), (8.20, 13.055), "否", (7.50, 13.385))    # D0 否 -> 格式错误
arrow(ax, (6.90, 10.98), (8.45, 10.98), "否", (7.675, 11.31))      # D1 否 -> 越界
arrow(ax, (6.95, 8.755), (8.20, 8.755), "否", (7.575, 9.085))      # D2 否 -> 不构成
arrow(ax, (6.60, 6.355), (8.35, 6.355), "是", (7.475, 6.685))      # D3 是 -> 等边
arrow(ax, (6.60, 4.355), (8.35, 4.355), "是", (7.475, 4.685))      # D4 是 -> 等腰

# ---- 各输出汇流到“结束”：右侧总线 + 底部横线 ----
# 每项的 right 为平行四边形在水平中线处的最右边界（x + w/2 - skew/2）
for y, right in ((13.055, 11.90), (10.98, 11.65), (8.755, 11.90),
                 (6.355, 11.75), (4.355, 11.75)):
    ax.annotate("", xy=(BUS, y), xytext=(right, y),
                arrowprops=dict(arrowstyle="-|>", color=EDGE, linewidth=1.45,
                                shrinkA=0, shrinkB=0), zorder=3)
seg(ax, [(BUS, 13.055), (BUS, 1.55)])
arrow(ax, (BUS, 1.55), (5.60, 1.55))

bad = check(fig, ax, "图B1 三角形判定程序流程图")
saved = fs.finalize_figure(fig, OUT / "figB1_triangle_flow", formats=["png", "pdf"], dpi=300)
for p in saved:
    print("saved", p)
if bad:
    sys.exit(1)
