"""赛前/赛后分析 Prompt 构造器"""
from typing import Tuple


def build_pre_match_analysis_prompt(
    match_id: str, home_data: dict, away_data: dict
) -> Tuple[str, str]:
    """构造赛前深度分析 prompt"""
    system_prompt = """\
你是一位资深足球评论员和战术分析师。请对即将进行的比赛提供深度分析。

分析要求：
1. 两队近期状态对比
2. 关键对位分析（进攻端 vs 防守端）
3. 战术打法预测
4. 胜负走势判断
5. 值得关注的球员

输出格式：使用 Markdown，分为以下章节：
## 状态分析
## 关键对位
## 战术预测
## 胜负走势
## 焦点球员"""

    user_prompt = f"""\
请分析以下即将进行的 2026 世界杯比赛：

主队：{home_data.get('name', '?')}
客队：{away_data.get('name', '?')}

主队详细信息：{home_data}
客队详细信息：{away_data}
比赛编号：{match_id}"""

    return system_prompt, user_prompt


def build_post_match_analysis_prompt(
    match_id: str, home: dict, away: dict,
    home_score: int, away_score: int,
    pre_prediction: str = "",
) -> Tuple[str, str]:
    """构造赛后总结 prompt"""
    system_prompt = """\
你是一位资深足球评论员。请对刚结束的比赛撰写赛后总结。

分析要求：
1. 比赛过程简述
2. 关键转折点
3. 双方表现评分
4. 对晋级形势的影响

输出格式：使用 Markdown"""

    user_prompt = f"""\
2026 世界杯比赛已结束：

{home.get('name', '?')} {home_score} - {away_score} {away.get('name', '?')}

赛前 AI 预测：{pre_prediction if pre_prediction else '无'}

请撰写赛后总结。"""

    return system_prompt, user_prompt
