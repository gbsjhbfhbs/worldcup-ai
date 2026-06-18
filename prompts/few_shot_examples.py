"""Few-shot 示例 — 基于 2022 世界杯真实比赛构造"""
from typing import List, Tuple

# 每个示例: (user_prompt 简化版, expected_output 结构化片段)
FEW_SHOT_EXAMPLES: List[Tuple[str, str]] = [
    # 示例 1: 强弱分明的比赛
    (
        "【比赛信息】2022 世界杯小组赛\n对阵: 法国 vs 澳大利亚\n"
        "法国 FIFA排名:4, Elo:2080, 近5场:[W,W,W,D,W], 场均进2.4/失0.9\n"
        "澳大利亚 FIFA排名:38, Elo:1750, 近5场:[W,D,L,W,L], 场均进1.3/失1.2\n"
        "历史交锋: 近3次交手：法国2胜1平0负",
        "---PROBABILITIES---\nHOME_WIN: 65\nDRAW: 22\nAWAY_WIN: 13\n"
        "---SCORE---\n2-0\n"
        "---CONFIDENCE---\n高\n"
        "---REASONING---\n"
        "法国队整体实力明显占优，FIFA排名和Elo评分均大幅领先。"
        "澳大利亚近期状态不稳定，面对强队防线容易失误。"
        "预计法国控制中场，姆巴佩的速度将是突破口。"
    ),
    # 示例 2: 实力接近的比赛
    (
        "【比赛信息】2022 世界杯1/4决赛\n对阵: 荷兰 vs 阿根廷\n"
        "荷兰 FIFA排名:8, Elo:1980, 近5场:[W,W,D,W,W], 场均进2.0/失0.6\n"
        "阿根廷 FIFA排名:3, Elo:2060, 近5场:[W,W,W,W,D], 场均进2.2/失0.5\n"
        "历史交锋: 近5次交手：荷兰2胜1平2负",
        "---PROBABILITIES---\nHOME_WIN: 30\nDRAW: 35\nAWAY_WIN: 35\n"
        "---SCORE---\n1-1\n"
        "---CONFIDENCE---\n低\n"
        "---REASONING---\n"
        "两队实力非常接近，都有稳固的防线和出色的进攻组织。"
        "淘汰赛阶段双方将更加谨慎，常规时间平局可能性大。"
        "梅西的个人能力是阿根廷的变数，但荷兰整体战术执行力更强。"
    ),
    # 示例 3: 黑马 vs 传统强队
    (
        "【比赛信息】2022 世界杯小组赛\n对阵: 沙特阿拉伯 vs 墨西哥\n"
        "沙特 FIFA排名:51, Elo:1670, 近5场:[L,W,L,D,W], 场均进1.0/失1.5\n"
        "墨西哥 FIFA排名:13, Elo:1880, 近5场:[W,D,W,W,L], 场均进1.8/失0.9\n"
        "历史交锋: 两队近年无直接交锋记录",
        "---PROBABILITIES---\nHOME_WIN: 18\nDRAW: 27\nAWAY_WIN: 55\n"
        "---SCORE---\n0-2\n"
        "---CONFIDENCE---\n中\n"
        "---REASONING---\n"
        "墨西哥整体实力和大赛经验明显优于沙特。"
        "沙特缺乏在面对强队时的进球能力，防线压力会很大。"
        "但考虑到沙特曾有爆冷先例，保留一定冷门概率。"
    ),
]


def format_few_shot_for_system() -> str:
    """将 few-shot 示例格式化为 system prompt 的一部分"""
    lines = ["以下是一些预测示例供参考：", ""]
    for i, (user_part, output) in enumerate(FEW_SHOT_EXAMPLES, 1):
        lines.append(f"【示例 {i}】")
        lines.append(f"输入: {user_part.strip()}")
        lines.append(f"输出: {output.strip()}")
        lines.append("")
    return "\n".join(lines)
