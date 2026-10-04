#!/usr/bin/env python3
"""Generate the seven worked diagrams in the beginner's Transformer guide.

Requires Python, Matplotlib and Noto Sans CJK. Run from any working directory:
    MPLCONFIGDIR=/tmp/transformer-mpl python3 /path/to/scripts/generate-learning-diagrams.py
Add --preview-dir /tmp/transformer-learning-previews to inspect PNG previews.
The default font is checked on disk; --font-path can select another Noto CJK file.
SVG text becomes paths, so readers do not need the font. Fixed SVG IDs, omitted
date metadata and trimmed line endings keep reruns stable in the same environment.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
WIDTH = 720
INK = "#172b46"
MUTED = "#51627a"
LINE = "#d7e0eb"
PALE = "#f4f7fb"
BLUE = "#245cc7"
ORANGE = "#b45309"
GREEN = "#087e68"
TINTS = ("#edf3ff", "#fff5e9", "#eaf7f3")
FONT = None


def text(ax, x, y, value, size=13, color=INK, ha="left", va="center", **kwargs):
    return ax.text(x, y, value, fontsize=size, fontproperties=FONT, color=color,
                   ha=ha, va=va, linespacing=1.55, **kwargs)


def box(ax, x, y, w, h, fill=PALE, edge=LINE, radius=9, linewidth=1):
    patch = FancyBboxPatch((x, y), w, h,
                          boxstyle=f"round,pad=0,rounding_size={radius}",
                          linewidth=linewidth, edgecolor=edge, facecolor=fill)
    ax.add_patch(patch)
    return patch


def rect(ax, x, y, w, h, fill, edge="none", linewidth=1, **kwargs):
    patch = Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge,
                      linewidth=linewidth, **kwargs)
    ax.add_patch(patch)
    return patch


def arrow(ax, start, end, color=MUTED, **kwargs):
    patch = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=12,
                            linewidth=1.5, color=color, shrinkA=0, shrinkB=0,
                            **kwargs)
    ax.add_patch(patch)
    return patch


def line(ax, xs, ys, color=LINE, **kwargs):
    ax.plot(xs, ys, color=color, linewidth=1, **kwargs)


def section(ax, y, number, title, detail=None):
    box(ax, 30, y - 12, 25, 25, BLUE, BLUE, radius=7)
    text(ax, 42.5, y, str(number), size=12, color="white", ha="center")
    text(ax, 67, y, title, size=15)
    if detail:
        text(ax, 67, y + 25, detail, size=11.5, color=MUTED)


def canvas(height, title, subtitle):
    fig = plt.figure(figsize=(WIDTH / 72, height / 72), dpi=144, facecolor="white")
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set(xlim=(0, WIDTH), ylim=(height, 0))
    ax.axis("off")
    rect(ax, 30, 27, 5, 27, BLUE)
    text(ax, 47, 40, title, size=22)
    text(ax, 30, 77, subtitle, size=12, color=MUTED)
    line(ax, [30, 690], [99, 99])
    return fig, ax


def note(ax, y, lines, height=None):
    height = height or (len(lines) * 23 + 20)
    box(ax, 30, y, 660, height)
    for index, value in enumerate(lines):
        text(ax, 45, y + 20 + index * 23, value, size=11, color=MUTED)


def embedding():
    fig, ax = canvas(680, "文字先查表，再带上位置信息", "先跟编号找到记录，再看同一份基础向量怎样用于两个位置。")
    section(ax, 128, 1, "按编号查 embedding 表（存放基础向量的表）")
    box(ax, 30, 165, 135, 124, TINTS[0], BLUE)
    text(ax, 97.5, 195, "片段：书", size=18, ha="center")
    text(ax, 97.5, 237, "编号 17", size=17, color=BLUE, ha="center")
    arrow(ax, (172, 225), (242, 225), BLUE)
    text(ax, 207, 206, "查表", size=11, color=BLUE, ha="center")
    box(ax, 250, 162, 440, 134, fill="white")
    rect(ax, 251, 198, 438, 48, TINTS[0])
    for x, label in ((285, "编号"), (365, "片段"), (548, "基础向量")):
        text(ax, x, 180, label, size=12, color=MUTED, ha="center")
    for y, number, token, vector in ((222, "17", "书", "[0.2, −0.4]"),
                                     (271, "42", "伞", "[−0.1, 0.7]")):
        for x, value in ((285, number), (365, token), (548, vector)):
            text(ax, x, y, value, size=15, ha="center", color=BLUE if number == "17" else INK)
    text(ax, 360, 322, "取出同一份 [0.2, −0.4]，分别交给两个位置", size=13, ha="center")
    section(ax, 365, 2, "逐项相加：第一格加第一格，第二格加第二格")
    for y, label, position, output, color, tint in (
        (398, "位置 A", "[0.1, 0.2]", "[0.3, −0.2]", BLUE, TINTS[0]),
        (482, "位置 B", "[0.3, 0.4]", "[0.5, 0.0]", GREEN, TINTS[2]),
    ):
        box(ax, 30, y, 660, 71, tint, color)
        text(ax, 48, y + 35, label, size=14, color=color)
        text(ax, 174, y + 16, "基础向量", size=10.5, color=MUTED, ha="center")
        text(ax, 357, y + 16, "位置向量", size=10.5, color=MUTED, ha="center")
        text(ax, 568, y + 16, "后续计算用的新表示", size=10.5, color=MUTED, ha="center")
        for x, value in ((174, "[0.2, −0.4]"), (267, "+"), (357, position), (458, "="), (568, output)):
            text(ax, x, y + 43, value, size=16, ha="center", color=color if x == 568 else INK)
    note(ax, 576, [
        "编号只负责查表，不表示语义远近；相加后，编号和表中原记录都不变。",
        "A、B 与所有数字都是教学设定；不能把两格固定解释成“词义”和“页码”。",
        "这里只画加法式位置方法，不代表所有模型都这样加入位置信息。",
    ])
    return fig


def qkv():
    fig, ax = canvas(940, "Q、K、V：先分清用途，再看数字", "上半部分用书本类比用途，下半部分回到同一份数字的三路计算。")
    section(ax, 129, 1, "需求、目录、正文：分别对应三种用途")
    box(ax, 30, 159, 660, 48, TINTS[0], BLUE)
    text(ax, 48, 183, "当前需求类比 Q", size=13, color=BLUE)
    text(ax, 302, 183, "“我想学做番茄炒蛋。”", size=17)
    text(ax, 130, 236, "书", size=12, color=MUTED, ha="center")
    text(ax, 328, 232, "目录说明类比 K", size=12, color=ORANGE, ha="center")
    text(ax, 549, 232, "实际内容类比 V", size=12, color=GREEN, ha="center")
    text(ax, 328, 251, "用于判断相关性", size=10.5, color=MUTED, ha="center")
    text(ax, 549, 251, "用于提供参考内容", size=10.5, color=MUTED, ha="center")
    rows = [
        ("《家常菜做法》", "番茄炒蛋", "炒蛋盛出，炒番茄，\n再合炒"),
        ("《厨房食材处理》", "切菜、打蛋", "怎样切番茄、\n怎样打散鸡蛋"),
        ("《汽车维修》", "轮胎、引擎", "检查轮胎、\n更换维修部件"),
    ]
    for index, (book, key, value) in enumerate(rows):
        y = 270 + 68 * index
        box(ax, 30, y, 660, 59, fill=PALE if index % 2 == 0 else "white")
        text(ax, 130, y + 29, book, size=12.5, ha="center")
        text(ax, 328, y + 29, key, size=13, color=ORANGE, ha="center")
        text(ax, 549, y + 29, value, size=12, color=GREEN, ha="center")
        line(ax, [231, 231], [y + 10, y + 49])
        line(ax, [429, 429], [y + 10, y + 49])
    text(ax, 360, 487, "同一行是一套来源：一本书的目录 K 与它的正文 V 必须配套。", size=12, ha="center")
    section(ax, 535, 2, "真实计算：完整的 [2, 3] 分别进入三套参数")
    box(ax, 228, 568, 264, 45, fill=PALE)
    text(ax, 360, 590, "同一位置的完整表示 [2, 3]", size=14, ha="center")
    for cx, color in ((134, BLUE), (360, ORANGE), (586, GREEN)):
        arrow(ax, (360, 613), (cx, 644), color)
    data = [
        (30, BLUE, TINTS[0], "Q", "2×1 + 3×2 = 8", "2×0 + 3×1 = 3", "[8, 3]", "当前位置去比较"),
        (256, ORANGE, TINTS[1], "K", "2×1 + 3×1 = 5", "2×(−1) + 3×1 = 1", "[5, 1]", "供各位置比较"),
        (482, GREEN, TINTS[2], "V", "2×1 + 3×0 = 2", "2×0 + 3×2 = 6", "[2, 6]", "供内容组合使用"),
    ]
    for x, color, tint, role, first, second, result, usage in data:
        box(ax, x, 650, 208, 169, tint, color)
        text(ax, x + 104, 671, f"{role} 的参数计算", size=13, color=color, ha="center")
        text(ax, x + 104, 704, first, size=12.5, ha="center")
        text(ax, x + 104, 730, second, size=12.5, ha="center")
        text(ax, x + 104, 764, result, size=20, color=color, ha="center")
        text(ax, x + 104, 797, usage, size=12, color=color, ha="center")
    note(ax, 840, [
        "三路都使用完整 [2, 3]；既不是把句子切三段，也不是把各格数字分给三路。",
        "书本只是用途比喻，真实模型不在翻书；8 不表示“番茄炒蛋”。",
        "这里人为设定参数；真实参数由训练得到，当前 Q、K、V 则是本次计算结果。",
    ])
    return fig


def softmax(values):
    highest = max(values)
    terms = [math.exp(value - highest) for value in values]
    total = sum(terms)
    return [term / total for term in terms]


def score_gap():
    fig, ax = canvas(530, "分数差距变大，比例会有多偏？", "两条比例条同样长，都代表 100%；蓝色是位置 1，橙色是位置 2。")
    for y, values, labels in ((148, [1, 0], ("73.11%", "26.89%")),
                              (295, [10, 0], ("99.995%", "0.005%"))):
        weights = softmax(values)
        text(ax, 30, y, f"分数 [{values[0]}, 0]", size=16)
        arrow(ax, (171, y), (231, y), BLUE)
        text(ax, 253, y, "softmax", size=14, color=BLUE)
        text(ax, 690, y, "总和 100%", size=12, color=MUTED, ha="right")
        left, width, top, height = 30, 660, y + 27, 39
        rect(ax, left, top, width * weights[0], height, BLUE)
        # The tiny second segment uses its exact probability, without a minimum
        # width or an outline that would visually enlarge its contribution.
        rect(ax, left + width * weights[0], top, width * weights[1], height, ORANGE)
        if values[0] == 1:
            text(ax, left + width * weights[0] / 2, top + height / 2,
                 f"位置 1：{labels[0]}", size=14, color="white", ha="center")
            text(ax, left + width * (weights[0] + weights[1] / 2), top + height / 2,
                 f"位置 2：{labels[1]}", size=12, color="white", ha="center")
            text(ax, 30, y + 91, "分数相差 1：两个位置都分到明显份额。", size=12, color=MUTED)
        else:
            text(ax, 360, top + height / 2, f"位置 1：约 {labels[0]}", size=14, color="white", ha="center")
            text(ax, 30, y + 91, "位置 2：约 0.005%，仍大于零", size=12, color=ORANGE)
            text(ax, 690, y + 91, "末段按真实比例绘制，几乎不可见", size=11, color=MUTED, ha="right")
    note(ax, 420, [
        "排名没变，改变的是分数差距；这里没有把向量维度从 1 改成 10。",
        "d_k 是 Q/K 的维度，√ 是平方根。除以 √d_k 是为了控制常见条件下，",
        "维度增加带来的点积分数尺度变化；它不保证分配比例总接近平均。",
    ])
    return fig


def weighted_values():
    fig, ax = canvas(970, "从参考比例，到新的两个数字", "接着第 6 章的同一组算例：当前位置“它”的 Q = [1, 0]。")
    section(ax, 129, 1, "按列向下追踪：用 K 算比例，再乘同一来源的 V")
    centers = (300, 458, 616)
    starts = (225, 383, 541)
    colors = (BLUE, ORANGE, GREEN)
    tints = TINTS
    weights = softmax([1 / math.sqrt(2), 0, 1 / math.sqrt(2)])
    sources = ("书", "图书馆", "读完")
    keys = ("[1, 0]", "[0, 1]", "[1, 1]")
    values = ((10, 0), (0, 10), (6, 6))
    for x, tint, color in zip(starts, tints, colors):
        box(ax, x, 167, 149, 270, tint, edge=color)
    row_positions = (189, 233, 276, 320, 366, 414)
    row_labels = ("信息来源", "K", "Q 与 K 的点积", "除以 √2", "softmax 参考比例", "同一来源的 V")
    for y, label in zip(row_positions, row_labels):
        text(ax, 30, y, label, size=12.5, color=MUTED)
    for index, (cx, source, key, value, color, weight) in enumerate(zip(centers, sources, keys, values, colors, weights)):
        vals = (source, key, "1" if index != 1 else "0", "约 0.7071" if index != 1 else "0",
                f"约 {weight * 100:.2f}%", f"[{value[0]}, {value[1]}]")
        for y, label in zip(row_positions, vals):
            text(ax, cx, y, label, size=14 if y != 366 else 13.5, color=color, ha="center")
        arrow(ax, (cx, 380), (cx, 394), color)
    text(ax, 360, 460, "每份 V 的两格都乘自己的比例；V 不参与前面的 Q/K 打分。", size=12, ha="center")
    section(ax, 501, 2, "按行相加：每一格各自收集三个来源的数值贡献")
    contributions = [[weight * vector[component] for weight, vector in zip(weights, values)]
                     for component in range(2)]
    totals = [sum(parts) for parts in contributions]
    # Both bars share one numerical scale; length measures contribution, not
    # semantic proportion. Zero contributions have labels but no artificial width.
    scale = 500 / 7
    for component, y in enumerate((545, 660)):
        parts = contributions[component]
        text(ax, 30, y + 18, f"第{('一', '二')[component]}格", size=15)
        cursor = 128
        for part, color, source in zip(parts, colors, sources):
            width = part * scale
            if part:
                rect(ax, cursor, y, width, 39, color)
                text(ax, cursor + width / 2, y + 19.5, f"{source} 约 {part:.4f}", size=12, color="white", ha="center")
            cursor += width
        text(ax, cursor + 9, y + 19.5, f"≈ {totals[component]:.2f}", size=16)
        zero_source = "图书馆" if component == 0 else "书"
        text(ax, 128, y + 60, f"{zero_source}贡献 = 0（这一格 V 为 0）", size=11.5, color=MUTED)
        text(ax, 128, y + 84, f"未舍入数字求和：约 {totals[component]:.10f}", size=12)
    box(ax, 30, 770, 660, 49, TINTS[0], BLUE)
    text(ax, 360, 794, "新向量 ≈ [6.42, 4.38]    →    交给后续计算", size=18, color=BLUE, ha="center")
    note(ax, 837, [
        "总和用未舍入数字计算；第二格约 4.3844，保留两位小数为 4.38。",
        "各段标签分别舍入，直接相加可能出现末位差异；两条贡献条共用同一尺度。",
        "本例 V 非负，才这样用条长展示；真实 V 可以有负数，贡献不是“词义占比”。",
        "权重不能解释最终回答的全部原因；这一步得到新向量，还没有输出“书”。",
    ])
    return fig


def multihead():
    fig, ax = canvas(830, "多头怎样把结果拼在一起？", "本章另设数字 [1, 2]、[3, 4]；不是第 6 章注意力算例的后续结果。")
    section(ax, 129, 1, "同一段内容，进入两套注意力计算")
    box(ax, 171, 161, 378, 45)
    text(ax, 360, 183, "同一段内容的表示（允许看到的位置）", size=14, ha="center")
    for cx, color in ((188, BLUE), (532, GREEN)):
        arrow(ax, (360, 206), (cx, 240), color)
    for x, color, tint, head, output in ((30, BLUE, TINTS[0], "头 1", "[1, 2]"),
                                        (374, GREEN, TINTS[2], "头 2", "[3, 4]")):
        box(ax, x, 245, 316, 130, tint, color)
        text(ax, x + 158, 267, f"{head}：自己的 Q/K/V 参数", size=14, color=color, ha="center")
        text(ax, x + 158, 302, "比较 → 分配比例 → 组合 V", size=13, ha="center")
        text(ax, x + 158, 346, f"同一个位置的输出 {output}", size=15, color=color, ha="center")
    section(ax, 420, 2, "拼接：按顺序排列，没有求平均")
    for index, (value, color, tint) in enumerate((("1", BLUE, TINTS[0]), ("2", BLUE, TINTS[0]),
                                                  ("3", GREEN, TINTS[2]), ("4", GREEN, TINTS[2]))):
        x = 217 + index * 72
        box(ax, x, 453, 68, 43, tint, color, radius=5)
        text(ax, x + 34, 474, value, size=22, color=color, ha="center")
    # Route connectors around the step heading instead of through its text.
    line(ax, [333, 333, 251], [375, 438, 438], color=BLUE)
    arrow(ax, (251, 438), (251, 452), BLUE)
    line(ax, [532, 532, 467], [375, 438, 438], color=GREEN)
    arrow(ax, (467, 438), (467, 452), GREEN)
    text(ax, 360, 520, "头 1 的两格接上头 2 的两格 → [1, 2, 3, 4]", size=13, ha="center")
    section(ax, 564, 3, "输出变换：用示例参数做乘加")
    box(ax, 30, 596, 660, 98)
    text(ax, 48, 622, "第一格：1×1 + 2×0 + 3×1 + 4×0 = 4", size=15)
    text(ax, 48, 660, "第二格：1×0 + 2×1 + 3×0 + 4×1 = 6", size=15)
    box(ax, 549, 610, 120, 71, TINTS[0], BLUE)
    text(ax, 609, 632, "输出", size=12, color=BLUE, ha="center")
    text(ax, 609, 659, "[4, 6]", size=21, color=BLUE, ha="center")
    note(ax, 720, [
        "两个头都处理允许看到的位置，不是分别接收前半句和后半句。",
        "各头有各自的参数，不预先规定哪个头专门找人名、哪个头专门找物品。",
        "真实输出参数由训练得到，后面的变换不总是示例里的简单相加。",
    ])
    return fig


def causal_mask():
    fig, ax = canvas(820, "哪一格可以看，哪一格必须挡住？", "小明｜借了｜一本｜书：逐行看当前位置允许参考哪些信息。")
    section(ax, 132, 1, "四个位置的可见范围")
    text(ax, 435, 132, "列：提供信息的位置", size=14, color=BLUE, ha="center")
    arrow(ax, (225, 153), (669, 153), BLUE)
    text(ax, 30, 199, "行：", size=12, color=MUTED)
    text(ax, 30, 222, "当前处理", size=12, color=MUTED)
    text(ax, 30, 245, "的位置", size=12, color=MUTED)
    arrow(ax, (108, 222), (108, 448), MUTED)
    labels = ("小明", "借了", "一本", "书")
    left, top, cw, ch = 211, 214, 116, 62
    for col, label in enumerate(labels):
        text(ax, left + (col + 0.5) * cw, 187, label, size=15, ha="center")
    for row, label in enumerate(labels):
        text(ax, 161, top + (row + 0.5) * ch, label, size=15, ha="center", color=BLUE if row == 2 else INK)
        for col in range(4):
            x, y = left + col * cw, top + row * ch
            allowed = col <= row
            rect(ax, x, y, cw - 5, ch - 5, TINTS[0] if allowed else "#f4f4f4",
                 edge=BLUE if allowed else "#c8ced8", hatch=None if allowed else "///", linewidth=0.8)
            text(ax, x + (cw - 5) / 2, y + (ch - 5) / 2, "可看" if allowed else "禁看",
                 size=15, color=BLUE if allowed else MUTED, ha="center",
                 bbox=dict(facecolor=TINTS[0] if allowed else "#f4f4f4", edgecolor="none", pad=2))
    box(ax, 30, 482, 660, 62, TINTS[0], BLUE)
    text(ax, 46, 502, "“一本”可以看自己，并用“小明、借了、一本”预测下一个片段“书”。", size=12)
    text(ax, 46, 525, "“可看”只表示允许参与计算，不表示各格权重一定相同。", size=11.5, color=MUTED)
    section(ax, 582, 2, "独立的三来源例子（不是上方四列中的某一整行）")
    box(ax, 30, 614, 260, 57)
    text(ax, 160, 642, "[0, 0, −∞]", size=21, ha="center")
    arrow(ax, (307, 642), (417, 642), BLUE)
    text(ax, 362, 624, "softmax", size=12, color=BLUE, ha="center")
    box(ax, 438, 614, 252, 57, TINTS[0], BLUE)
    text(ax, 564, 642, "[0.5, 0.5, 0]", size=21, color=BLUE, ha="center")
    note(ax, 695, [
        "−∞ 表示负无穷；在 softmax 中，被挡住的第三项贡献为 0，最终比例为 0。",
        "普通分数 0 不能替代遮罩：exp(0) = 1，仍会参加比例分配。",
        "训练程序虽然拿到了完整材料，当前位置仍需要挡住后面的内容。",
    ])
    return fig


def training():
    height = 925
    fig, ax = canvas(height, "哪一步改参数，哪一步只是使用？", "单参数教学模型：输出 = w × 输入。先训练一次，再固定参数做两次推理。")
    section(ax, 129, 1, "训练：输入固定为 2，目标固定为 4")
    text(ax, 30, 158, "损失 = (2w − 4)²；曲线高度表示损失，横轴表示参数 w。", size=12, color=MUTED)
    chart = fig.add_axes((77 / WIDTH, (height - 414) / height, 342 / WIDTH, 220 / height))
    ws = [0.6 + (2.2 - 0.6) * index / 100 for index in range(101)]
    chart.plot(ws, [(2 * w - 4) ** 2 for w in ws], color=BLUE, linewidth=2.5)
    chart.set_xlim(0.6, 2.2)
    chart.set_ylim(-0.2, 8.5)
    chart.set_xticks([1, 1.8, 2], ["1", "1.8", "2"])
    chart.set_yticks([0, 4, 8])
    chart.tick_params(axis="both", colors=MUTED, labelsize=11)
    chart.grid(axis="y", color=LINE, linewidth=0.8)
    chart.spines[["top", "right"]].set_visible(False)
    chart.spines[["left", "bottom"]].set_color(LINE)
    chart.set_xlabel("参数 w", fontsize=12, color=MUTED, fontproperties=FONT)
    chart.set_ylabel("损失", fontsize=12, color=MUTED, fontproperties=FONT)
    chart.scatter([1], [4], color=ORANGE, s=56, zorder=5)
    chart.scatter([1.8], [0.16], color=GREEN, s=56, zorder=5)
    chart.annotate("更新前", (1, 4), xytext=(1.16, 5.1), fontsize=12, color=ORANGE,
                   fontproperties=FONT, arrowprops=dict(arrowstyle="-", color=ORANGE))
    chart.annotate("更新后", (1.8, 0.16), xytext=(1.85, 1.7), fontsize=12, color=GREEN,
                   fontproperties=FONT, arrowprops=dict(arrowstyle="-", color=GREEN), ha="center")
    chart.annotate("", (1.78, 0.27), xytext=(1.03, 3.87),
                   arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.5, connectionstyle="arc3,rad=0.16"))
    for y, tint, color, stage, parameter, output, loss in (
        (188, TINTS[1], ORANGE, "更新前", "1", "2", "4"),
        (315, TINTS[2], GREEN, "更新后", "1.8", "3.6", "0.16"),
    ):
        box(ax, 462, y, 228, 112, tint, color)
        text(ax, 481, y + 23, f"{stage}：w = {parameter}", size=15, color=color)
        text(ax, 481, y + 57, f"输出 = {output}", size=14)
        text(ax, 481, y + 87, f"损失 = {loss}", size=14)
    box(ax, 30, 469, 660, 96)
    text(ax, 47, 492, "反向传播算梯度：−8", size=14, color=BLUE)
    text(ax, 365, 492, "优化器按学习率 0.1 更新参数", size=13, color=GREEN)
    text(ax, 360, 535, "新 w = 1 − 0.1 × (−8) = 1.8", size=21, ha="center")
    section(ax, 607, 2, "推理：固定同一个参数 w = 1.8")
    for y, input_value, output in ((645, "2", "3.6"), (716, "3", "5.4")):
        box(ax, 30, y, 158, 47, fill="white")
        text(ax, 109, y + 23.5, f"输入 {input_value}", size=17, ha="center")
        arrow(ax, (199, y + 23.5), (260, y + 23.5), GREEN)
        box(ax, 275, y, 177, 47, TINTS[2], GREEN)
        text(ax, 363.5, y + 23.5, "乘同一个 1.8", size=16, color=GREEN, ha="center")
        arrow(ax, (465, y + 23.5), (526, y + 23.5), GREEN)
        box(ax, 539, y, 151, 47, fill="white")
        text(ax, 614.5, y + 23.5, f"输出 {output}", size=17, ha="center")
    note(ax, 790, [
        "输入不同，输出可以不同，但参数仍是 1.8；输入 3 是另一次推理对照。",
        "反向传播负责计算梯度，优化器才实际修改参数；普通推理只使用参数。",
        "一条单参数曲线只是教学简化，不代表完整语言模型，也不保证每次更新",
        "都改善所有样本。下方推理对照没有修改上方固定输入为 2 的训练任务。",
    ])
    return fig


DIAGRAMS = (
    ("embedding-position", embedding),
    ("qkv-books-and-vectors", qkv),
    ("softmax-score-gap", score_gap),
    ("attention-weighted-values", weighted_values),
    ("multihead-concatenation", multihead),
    ("causal-mask-grid", causal_mask),
    ("training-and-inference", training),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-dir", type=Path, help="Also write PNG previews to this directory.")
    parser.add_argument("--font-path", type=Path, default=Path(
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        help="Path to an installed Noto Sans CJK font (TTC/OTF/TTF).")
    args = parser.parse_args()
    if not args.font_path.is_file():
        parser.error(f"CJK font not found: {args.font_path}; install Noto Sans CJK or use --font-path.")
    global FONT
    FONT = font_manager.FontProperties(fname=str(args.font_path))
    font_manager.fontManager.addfont(str(args.font_path))
    matplotlib.rcParams.update({
        "font.family": FONT.get_name(),
        "svg.fonttype": "path",
        "svg.hashsalt": "transformer-learning-diagrams-v1",
        "axes.unicode_minus": True,
        "savefig.facecolor": "white",
    })
    target = ROOT / "docs" / "images"
    target.mkdir(parents=True, exist_ok=True)
    if args.preview_dir:
        args.preview_dir.mkdir(parents=True, exist_ok=True)
    for name, draw in DIAGRAMS:
        fig = draw()
        svg_path = target / f"{name}.svg"
        fig.savefig(svg_path, format="svg", metadata={"Date": None})
        svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines()) + "\n",
                            encoding="utf-8")
        if args.preview_dir:
            fig.savefig(args.preview_dir / f"{name}.png", dpi=144)
        plt.close(fig)
        print(svg_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
