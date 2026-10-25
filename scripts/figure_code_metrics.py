# -*- coding: utf-8 -*-
"""实验三 插图：各包代码行构成（数据来自 _work/exp3_code_metrics.json）。"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
import numpy as np

import figstyle as fs

ROOT = Path(r"C:/Users/LZ/Desktop/软工")
METRICS = json.loads((ROOT / "_work" / "exp3_code_metrics.json").read_text(encoding="utf-8"))

PKG_LABEL = {
    "com.library.library": "根包（App）",
    "com.library.library.util": "util",
    "com.library.library.entity": "entity",
    "com.library.library.dao": "dao",
    "com.library.library.service": "service",
    "com.library.library.ui": "ui",
}

agg = {}
for f in METRICS["files"]:
    p = f["path"].replace("\\", "/")
    key = p.split("/src/main/java/")[1].rsplit("/", 1)[0].replace("/", ".")
    a = agg.setdefault(key, {"code": 0, "comment": 0, "blank": 0, "files": 0})
    a["code"] += f["code"]
    a["comment"] += f["comment"]
    a["blank"] += f["blank"]
    a["files"] += 1

order = sorted(PKG_LABEL, key=lambda k: agg[k]["code"], reverse=True)
labels = [PKG_LABEL[k] + "\n(%d 个文件)" % agg[k]["files"] for k in order]
code = np.array([agg[k]["code"] for k in order])
comment = np.array([agg[k]["comment"] for k in order])
blank = np.array([agg[k]["blank"] for k in order])

fs.apply_publication_style(fs.FigureStyle(font_size=12, axes_linewidth=1.4))
fig, ax = plt.subplots(figsize=(8.6, 4.7))
y = np.arange(len(order))
h = 0.60
ax.barh(y, code, h, label="代码行", color=fs.PALETTE["blue_main"], edgecolor="black", linewidth=0.6)
ax.barh(y, comment, h, left=code, label="注释行", color=fs.PALETTE["green_3"], edgecolor="black", linewidth=0.6)
ax.barh(y, blank, h, left=code + comment, label="空行", color="#D9D9D9", edgecolor="black", linewidth=0.6)
for i in range(len(order)):
    total = code[i] + comment[i] + blank[i]
    ax.text(total + 4, i, "共 %d 行" % total, va="center", fontsize=9.5, color="#333333")
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlabel("行数")
ax.set_xlim(0, max(code + comment + blank) * 1.18)
ax.legend(loc="lower right", frameon=False, fontsize=9.5)
ax.spines["left"].set_visible(True)
ax.spines["bottom"].set_visible(True)
ax.tick_params(axis="y", length=0)
ax.set_title("图书管理系统各包代码量构成", fontsize=13, pad=10)
fig.tight_layout()

for p in fs.finalize_figure(fig, ROOT / "figures" / "figB2_code_metrics",
                            formats=["png", "pdf"], dpi=300):
    print("saved", p)
