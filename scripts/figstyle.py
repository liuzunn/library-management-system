"""Publication-style matplotlib helpers (house style).

Implements the API conventions from the scientific-figure-making skill:
PALETTE / DEFAULT_COLORS / FigureStyle / apply_publication_style /
create_subplots / finalize_figure / make_grouped_bar / annotate_bars /
make_trend / make_heatmap / make_scatter.

Chinese-labelled figures additionally register a CJK-capable font stack.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE",
    "green_2": "#AADCA9",
    "green_3": "#8BCF8B",
    "red_1": "#F6CFCB",
    "red_2": "#E9A6A1",
    "red_strong": "#B64342",
    "neutral": "#CFCECE",
    "highlight": "#FFD700",
    "teal": "#42949E",
    "violet": "#9A4D8E",
}

DEFAULT_COLORS = [
    PALETTE["blue_main"],
    PALETTE["green_3"],
    PALETTE["red_strong"],
    PALETTE["teal"],
    PALETTE["violet"],
    PALETTE["neutral"],
]

# CJK-capable stack first, then the skill's Latin default.
CJK_FONTS = (
    "Microsoft YaHei",
    "SimHei",
    "Noto Sans SC",
    "SimSun",
    "DejaVu Sans",
    "Helvetica",
    "Arial",
)


@dataclass(frozen=True)
class FigureStyle:
    """Base typography / spine settings for a figure."""

    font_size: int = 16
    axes_linewidth: float = 2.5
    use_tex: bool = False
    font_family: tuple = CJK_FONTS


# --------------------------------------------------------------------------
# Style / layout
# --------------------------------------------------------------------------


def apply_publication_style(style=None):
    """Configure matplotlib rcParams for the house publication look."""
    style = style or FigureStyle()
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": list(style.font_family),
            "font.size": style.font_size,
            "axes.labelsize": style.font_size,
            "axes.titlesize": style.font_size + 2,
            "xtick.labelsize": style.font_size - 2,
            "ytick.labelsize": style.font_size - 2,
            "legend.fontsize": style.font_size - 3,
            "axes.linewidth": style.axes_linewidth,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "legend.frameon": False,
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "axes.unicode_minus": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "text.usetex": style.use_tex,
        }
    )
    return style


def create_subplots(nrows=1, ncols=1, figsize=None, **kwargs):
    """Return (fig, axes) where axes is a flattened 1-D array."""
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, **kwargs)
    axes = np.atleast_1d(axes).ravel()
    return fig, axes


def finalize_figure(fig, out_path, formats=None, dpi=300, close=True, pad=0.05, **kwargs):
    """Save fig to one or more formats; returns the written paths."""
    out_path = Path(out_path)
    if formats is None:
        formats = [out_path.suffix.lstrip(".") or "pdf"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    saved = []
    for fmt in formats:
        target = out_path.with_suffix("." + fmt)
        fig.savefig(target, dpi=dpi, bbox_inches="tight", pad_inches=pad, **kwargs)
        saved.append(target)
    if close:
        plt.close(fig)
    return saved


# --------------------------------------------------------------------------
# Plot helpers
# --------------------------------------------------------------------------


def _as_1d(values, name):
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1:
        raise ValueError(name + " must be 1-D, got shape " + str(arr.shape))
    return arr


def make_grouped_bar(ax, categories, series, labels, ylabel="Value", colors=None,
                     annotate=False, fmt="{:.0f}", width=0.8):
    """Grouped bar chart. series is a list of per-group value arrays."""
    categories = list(categories)
    series = [np.asarray(s, dtype=float) for s in series]
    for s in series:
        if len(s) != len(categories):
            raise ValueError("each series must match len(categories)")
    colors = colors or DEFAULT_COLORS
    n = len(series)
    x = np.arange(len(categories), dtype=float)
    bar_w = width / n
    containers = []
    for i, (vals, lab) in enumerate(zip(series, labels)):
        offset = -width / 2 + bar_w * (i + 0.5)
        containers.append(ax.bar(x + offset, vals, bar_w, label=lab,
                                 color=colors[i % len(colors)],
                                 edgecolor="black", linewidth=1.0))
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel(ylabel)
    if annotate:
        for c in containers:
            annotate_bars(ax, c, fmt=fmt)
    return containers[-1]


def annotate_bars(ax, bars, fmt="{:.2f}", fontsize=10, padding=3):
    """Write value labels above each bar of a BarContainer."""
    for rect in bars:
        h = rect.get_height()
        ax.annotate(fmt.format(h), xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, padding), textcoords="offset points",
                    ha="center", va="bottom", fontsize=fontsize)


def make_trend(ax, x, y_series, labels, colors=None, ylabel=None, xlabel=None,
               show_shadow=True, marker="o"):
    """Line chart for one or more series, with an optional +/-1 sd band."""
    x = _as_1d(x, "x")
    colors = colors or DEFAULT_COLORS
    for i, (ys, lab) in enumerate(zip(y_series, labels)):
        if isinstance(ys, (tuple, list)) and len(ys) == 2 and np.ndim(ys[0]) == 1:
            mean = _as_1d(ys[0], "mean")
            sd = _as_1d(ys[1], "sd")
        else:
            mean = _as_1d(ys, "y")
            sd = None
        if len(mean) != len(x):
            raise ValueError("each series must match len(x)")
        c = colors[i % len(colors)]
        ax.plot(x, mean, marker=marker, markersize=5, linewidth=2.2, color=c,
                label=lab, markeredgecolor="white", markeredgewidth=1.0)
        if show_shadow and sd is not None:
            ax.fill_between(x, mean - sd, mean + sd, color=c, alpha=0.18, linewidth=0)
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    return ax


def make_heatmap(ax, matrix, x_labels=None, y_labels=None, cmap="magma",
                 cbar_label=None, annotate=False, fmt="{:.0f}", vmin=None, vmax=None):
    """Render a 2-D matrix as a heatmap."""
    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2:
        raise ValueError("matrix must be 2-D")
    im = ax.imshow(matrix, cmap=cmap, aspect="auto", vmin=vmin, vmax=vmax)
    if x_labels is not None:
        ax.set_xticks(np.arange(matrix.shape[1]))
        ax.set_xticklabels(x_labels)
    if y_labels is not None:
        ax.set_yticks(np.arange(matrix.shape[0]))
        ax.set_yticklabels(y_labels)
    if annotate:
        mid = (matrix.min() + matrix.max()) / 2
        for r in range(matrix.shape[0]):
            for c in range(matrix.shape[1]):
                ax.text(c, r, fmt.format(matrix[r, c]), ha="center", va="center",
                        fontsize=10, color="white" if matrix[r, c] < mid else "black")
    if cbar_label:
        cb = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
        cb.set_label(cbar_label)
        cb.outline.set_linewidth(1.0)
    return im


def make_scatter(ax, x, y, label=None, color=None, size=50, alpha=0.7):
    """Single-series scatter plot."""
    x = _as_1d(x, "x")
    y = _as_1d(y, "y")
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    return ax.scatter(x, y, s=size, alpha=alpha, label=label,
                      color=color or PALETTE["blue_main"],
                      edgecolor="white", linewidth=0.8, zorder=3)


# --------------------------------------------------------------------------
# Diagram primitives (E-R / DFD)
# --------------------------------------------------------------------------


def draw_entity(ax, x, y, text, w=1.9, h=0.75, fontsize=15,
                facecolor="#EAF1FA", edgecolor=None, lw=2.0):
    """Chen-notation entity: rectangle."""
    edgecolor = edgecolor or PALETTE["blue_main"]
    ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, facecolor=facecolor,
                               edgecolor=edgecolor, linewidth=lw, zorder=4))
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize, zorder=5,
            fontweight="bold", color="#0B2E5C")
    return (x, y, w, h)


def draw_diamond(ax, x, y, text, w=2.0, h=1.15, fontsize=15,
                 facecolor="#FDF3D8", edgecolor=None, lw=2.0):
    """Chen-notation relationship: diamond."""
    edgecolor = edgecolor or "#B8860B"
    pts = [(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=facecolor,
                         edgecolor=edgecolor, linewidth=lw, zorder=4))
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize, zorder=5,
            fontweight="bold", color="#7A5B00")
    return (x, y, w, h)


def draw_attribute(ax, x, y, text, w=1.5, h=0.62, fontsize=13,
                   facecolor="#EAF6EC", edgecolor=None, lw=1.6, key=False):
    """Chen-notation attribute: ellipse. key=True underlines the label."""
    edgecolor = edgecolor or "#2E7D32"
    ax.add_patch(Ellipse((x, y), w, h, facecolor=facecolor, edgecolor=edgecolor,
                         linewidth=lw, zorder=4))
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize, zorder=5,
            color="#1B4D20")
    if key:
        half = 0.155 * len(text)
        ax.plot([x - half, x + half], [y - 0.13, y - 0.13], color="#1B4D20",
                linewidth=1.6, zorder=5, solid_capstyle="butt")
    return (x, y, w, h)


def _edge_point(cx, cy, w, h, tx, ty):
    """Point on the boundary of a centred box (w x h) facing target (tx, ty)."""
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    sx = (w / 2) / abs(dx) if dx else float("inf")
    sy = (h / 2) / abs(dy) if dy else float("inf")
    s = min(sx, sy)
    return cx + dx * s, cy + dy * s


def connect(ax, a, b, lw=1.6, color="#4A4A4A", style="-"):
    """Line from the boundary of box a to the boundary of box b."""
    ax1, ay1, aw, ah = a
    bx1, by1, bw, bh = b
    x0, y0 = _edge_point(ax1, ay1, aw, ah, bx1, by1)
    x1, y1 = _edge_point(bx1, by1, bw, bh, ax1, ay1)
    ax.plot([x0, x1], [y0, y1], color=color, linewidth=lw, zorder=2,
            linestyle=style, solid_capstyle="round")


def draw_process(ax, x, y, text, w=2.9, h=0.95, fontsize=12.5, number=None):
    """DFD process: rounded rectangle with a numbered strip on top."""
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor="#EAF1FA", edgecolor=PALETTE["blue_main"],
                                linewidth=1.8, zorder=4))
    ax.plot([x - w / 2 + 0.10, x + w / 2 - 0.10], [y + h / 2 - 0.30] * 2,
            color=PALETTE["blue_main"], linewidth=1.2, zorder=5)
    ax.text(x, y + h / 2 - 0.155, number or "", ha="center", va="center",
            fontsize=10.5, color=PALETTE["blue_main"], zorder=5)
    ax.text(x, y - 0.17, text, ha="center", va="center", fontsize=fontsize,
            zorder=5, color="#0B2E5C")
    return (x, y, w, h)


def draw_external(ax, x, y, text, w=2.0, h=0.9, fontsize=12.5):
    """DFD external entity: rectangle with a heavy left edge."""
    ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, facecolor="#F3F3F3",
                               edgecolor="#5A5A5A", linewidth=1.8, zorder=4))
    ax.plot([x - w / 2] * 2, [y - h / 2, y + h / 2], color=PALETTE["blue_main"],
            linewidth=4.0, zorder=5)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize, zorder=5,
            color="#333333")
    return (x, y, w, h)


def draw_store(ax, x, y, text, w=2.6, h=0.72, fontsize=12.5, sid=None):
    """DFD data store: open-ended rectangle with an id box on the left."""
    ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, facecolor="#FFFFFF",
                               edgecolor="#6A6A6A", linewidth=1.6, zorder=4))
    ax.plot([x - w / 2 + 0.42] * 2, [y - h / 2, y + h / 2], color="#6A6A6A",
            linewidth=1.6, zorder=5)
    ax.text(x - w / 2 + 0.21, y, sid or "", ha="center", va="center", fontsize=11,
            zorder=7, color="#333333")
    ax.text(x + 0.21, y, text, ha="center", va="center", fontsize=fontsize,
            zorder=7, color="#333333")
    return (x, y, w, h)


def draw_arrow(ax, a, b, label=None, lw=1.6, color="#4A4A4A",
               label_offset=(0, 0.22), fontsize=11, rad=0.0, both=False):
    """Directed arrow between two box tuples, with an optional edge label."""
    ax1, ay1, aw, ah = a
    bx1, by1, bw, bh = b
    x0, y0 = _edge_point(ax1, ay1, aw, ah, bx1, by1)
    x1, y1 = _edge_point(bx1, by1, bw, bh, ax1, ay1)
    st = "<->" if both else "->"
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=st, color=color, linewidth=lw,
                                shrinkA=0, shrinkB=0,
                                connectionstyle="arc3,rad=" + str(rad)),
                zorder=3)
    if label:
        mx = (x0 + x1) / 2 + label_offset[0]
        my = (y0 + y1) / 2 + label_offset[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=fontsize,
                color="#1A1A1A", zorder=6,
                bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                          edgecolor="none", alpha=0.92))


def blank_axes(ax, xlim, ylim):
    """Turn an axes into a clean canvas for schematic diagrams."""
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return ax
