"""Render the coordinate figures for section 3.2 (requires Matplotlib).

Run from the repository root:
    python3 scripts/generate-vector-diagrams.py

Pass --preview-dir /tmp/vector-previews to also export PNG previews.
SVG text is converted to paths so Chinese labels render without external fonts.
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import MultipleLocator


ROOT = Path(__file__).resolve().parents[1]
BLUE = "#245cc7"
ORANGE = "#b45309"
INK = "#1e293b"
MUTED = "#475569"


def configure():
    font = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
    if font.exists():
        font_manager.fontManager.addfont(str(font))
        family = font_manager.FontProperties(fname=str(font)).get_name()
    else:
        family = "sans-serif"  # Supply a CJK font on other systems if needed.
    plt.rcParams.update({
        "font.family": family,
        "font.size": 12,
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.unicode_minus": False,
        "svg.fonttype": "path",
        "svg.hashsalt": "transformer-vector-diagrams-v1",
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    })


def canvas(title, subtitle, xlim, ylim, ticks_x, ticks_y, grid_step, xlabel, ylabel):
    fig = plt.figure(figsize=(10, 7.2))
    fig.text(0.08, 0.935, title, fontsize=22)
    fig.text(0.08, 0.885, subtitle, fontsize=12, color=MUTED)
    ax = fig.add_axes((0.10, 0.16, 0.55, 0.63))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks(ticks_x)
    ax.set_yticks(ticks_y)
    ax.set_xticklabels([f"{n:g}" if n else "" for n in ticks_x], fontsize=10)
    ax.set_yticklabels([f"{n:g}" if n else "" for n in ticks_y], fontsize=10)
    ax.xaxis.set_minor_locator(MultipleLocator(grid_step))
    ax.yaxis.set_minor_locator(MultipleLocator(grid_step))
    ax.grid(which="both", color="#e2e8f0", linewidth=0.7, zorder=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("bottom", "left"):
        ax.spines[side].set_position("zero")
        ax.spines[side].set_color("#64748b")
        ax.spines[side].set_linewidth(1.4)
    ax.tick_params(which="minor", length=0)
    ax.tick_params(which="major", length=3, pad=5)
    ax.plot(0, 0, "o", color=INK, markersize=5, zorder=6)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.xaxis.set_label_coords(0.5, -0.13)
    fig.text(0.10, 0.815, ylabel, fontsize=12)
    return fig, ax


def vector(ax, point, label, color, offset):
    x, y = point
    ax.plot((x, x, 0), (0, y, y), linestyle=(0, (4, 3)),
            linewidth=1.4, color=color, alpha=0.7, zorder=2)
    ax.annotate("", xy=point, xytext=(0, 0),
                arrowprops={"arrowstyle": "-|>", "color": color,
                            "lw": 2.4, "mutation_scale": 21,
                            "shrinkA": 0, "shrinkB": 0}, zorder=4)
    ax.scatter([x], [y], s=32, color=color, zorder=5)
    ax.annotate(label, xy=point, xytext=offset, textcoords="offset points",
                color=color, fontsize=13,
                bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9, "pad": 2})


def note(fig, y, title, lines, color):
    fig.text(0.70, y, title, color=color, fontsize=16)
    fig.text(0.70, y - 0.052, "\n".join(lines), color=INK,
             fontsize=13, va="top", linespacing=1.75)


def drink_figure():
    fig, ax = canvas(
        "两个数字，怎样画成一个位置？",
        "饮料例子：[甜度, 酸度]，两个评分都由人规定",
        (-0.6, 10.5), (-0.6, 10.5), range(11), range(11), 1,
        "横轴：第一个数字（甜度）", "纵轴：第二个数字（酸度）",
    )
    vector(ax, (8, 2), "甲 [8, 2]", BLUE, (-28, 15))
    vector(ax, (3, 7), "乙 [3, 7]", ORANGE, (12, 4))
    ax.annotate("原点 [0, 0]", xy=(0, 0), xytext=(8, -24),
                textcoords="offset points", fontsize=10)
    note(fig, 0.71, "甲：甜度 8，酸度 2", ("从原点先向右 8 格", "再向上 2 格，找到蓝点"), BLUE)
    note(fig, 0.49, "乙：甜度 3，酸度 7", ("从原点先向右 3 格", "再向上 7 格，找到橙点"), ORANGE)
    fig.text(0.70, 0.235, "虚线：帮你对齐刻度\n箭头：从原点指向这组数的位置",
             fontsize=11, color=MUTED, linespacing=1.8)
    fig.text(0.08, 0.035, "两个数字对应两个方向，所以叫二维；图里有几个点，不决定向量有几维。",
             fontsize=11, color=MUTED)
    return fig


def token_figure():
    fig, ax = canvas(
        "“书”和“伞”的示例向量，怎样读？",
        "仍然按顺序读：[第一个数字, 第二个数字]",
        (-0.6, 0.6), (-0.6, 0.9), (-0.4, -0.1, 0, 0.2, 0.5),
        (-0.4, -0.2, 0, 0.2, 0.4, 0.7), 0.1,
        "横轴：第一个数字", "纵轴：第二个数字",
    )
    # Keep scale labels clear of the arrow just to the left of the vertical axis.
    ax.tick_params(axis="y", labelleft=False)
    for value in (-0.4, -0.2, 0.2, 0.4, 0.7):
        ax.annotate(f"{value:g}", xy=(0, value),
                    xytext=(8 if value > 0 else -8, -4),
                    textcoords="offset points", fontsize=10, color=MUTED,
                    ha="left" if value > 0 else "right")
    vector(ax, (0.2, -0.4), "书 [0.2, -0.4]", BLUE, (12, 3))
    vector(ax, (-0.1, 0.7), "伞 [-0.1, 0.7]", ORANGE, (-105, 14))
    ax.annotate("原点 [0, 0]", xy=(0, 0), xytext=(10, 12),
                textcoords="offset points", fontsize=10)
    note(fig, 0.71, "书：[0.2, -0.4]", ("第一个数为正：向右 0.2", "第二个数为负：向下 0.4"), BLUE)
    note(fig, 0.49, "伞：[-0.1, 0.7]", ("第一个数为负：向左 0.1", "第二个数为正：向上 0.7"), ORANGE)
    fig.text(0.70, 0.235, "这两条轴没有被规定为\n“知识”“纸张”等中文属性。",
             fontsize=11, color=MUTED, linespacing=1.8)
    fig.text(0.08, 0.035, "数值只是教学假设。这些坐标也不是词语在句子中的先后位置。",
             fontsize=11, color=MUTED)
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-dir", type=Path)
    args = parser.parse_args()
    configure()
    output = ROOT / "docs" / "images"
    output.mkdir(parents=True, exist_ok=True)
    if args.preview_dir:
        args.preview_dir.mkdir(parents=True, exist_ok=True)
    for name, render in (("vector-drink-coordinates", drink_figure),
                         ("vector-token-coordinates", token_figure)):
        fig = render()
        svg_path = output / f"{name}.svg"
        fig.savefig(svg_path, metadata={"Date": None})
        svg_path.write_text("\n".join(line.rstrip() for line in
                                      svg_path.read_text(encoding="utf-8").splitlines()) + "\n",
                            encoding="utf-8")
        if args.preview_dir:
            fig.savefig(args.preview_dir / f"{name}.png", dpi=160)
        plt.close(fig)
        print(f"Wrote docs/images/{name}.svg")


if __name__ == "__main__":
    main()
