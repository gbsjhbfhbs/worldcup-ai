"""比赛预测 Prompt 构造器 — 多维分析：实力、环境、爆冷"""
from typing import Tuple

from models.match import Match
from services.data_loader import DataLoader
from prompts.few_shot_examples import format_few_shot_for_system


# 球场环境数据（海拔/类型/六月气候）
VENUE_PROFILES = {
    "墨西哥城体育场": {"altitude": 2240, "type": "室外", "climate": "高原干燥, 紫外线强, 含氧量低, 球速偏快", "temp": "22-30°C"},
    "瓜达拉哈拉体育场": {"altitude": 1566, "type": "室外", "climate": "高原, 午后偶有雷雨, 湿度中等", "temp": "20-31°C"},
    "BBVA体育场": {"altitude": 537, "type": "室外", "climate": "半干旱, 高温, 对体能消耗大", "temp": "25-36°C"},
    "BMO球场": {"altitude": 76, "type": "室外", "climate": "温带, 可能有风, 六月温和", "temp": "18-26°C"},
    "BC广场": {"altitude": 0, "type": "室内(可开合)", "climate": "人工草皮, 温带海洋性, 阵雨频繁", "temp": "14-21°C"},
    "SoFi体育场": {"altitude": 30, "type": "室内", "climate": "恒温空调, 地中海气候, 干燥", "temp": "18-27°C"},
    "李维斯体育场": {"altitude": 2, "type": "室外", "climate": "湾区微气候, 傍晚海风大, 湿凉", "temp": "13-22°C"},
    "流明体育场": {"altitude": 52, "type": "室外", "climate": "温带海洋性, 常有小雨, 湿滑", "temp": "13-23°C"},
    "大都会体育场": {"altitude": 3, "type": "室外", "climate": "温带大陆性, 六月高温高湿", "temp": "20-33°C"},
    "林肯金融体育场": {"altitude": 12, "type": "室外", "climate": "温带, 湿度偏高, 可能有雷暴", "temp": "21-32°C"},
    "吉列体育场": {"altitude": 80, "type": "室外", "climate": "温带, 多变, 海风影响", "temp": "16-27°C"},
    "硬石体育场": {"altitude": 2, "type": "室外", "climate": "亚热带, 高温高湿, 午后雷雨常见", "temp": "25-34°C"},
    "奔驰体育场": {"altitude": 320, "type": "室内(可开合)", "climate": "亚热带, 空调恒温, 湿度可控", "temp": "24-32°C"},
    "AT&T体育场": {"altitude": 150, "type": "室内(可开合)", "climate": "亚热带, 空调, 不受外部天气影响", "temp": "26-36°C"},
    "NRG体育场": {"altitude": 13, "type": "室内(可开合)", "climate": "亚热带, 空调, 高温高湿外部", "temp": "24-34°C"},
    "儿童慈善公园": {"altitude": 270, "type": "室外", "climate": "大陆性, 六月高温, 湿度中等", "temp": "22-34°C"},
}

SYSTEM_PROMPT_TEMPLATE = """你是一位顶级足球分析师和博彩精算师，拥有 20 年经验。

你需要综合多维因素，预测一场比赛的：
1. 主胜/平局/客胜的概率（三个百分比整数，和为 100）
2. 最可能的比分（如"2-1"）
3. 置信度（高/中/低）
4. 详细推理（3-5 句话，涵盖实力、环境、爆冷风险）

## 分析框架（必须覆盖）

### 1. 实力对比
- FIFA 排名与 Elo 评分差距
- 近期状态走势（连续不败 vs 连败）
- 攻防效率（进球率与失球率对比）
- 历史交锋心理优势

### 2. 环境因素
- 海拔影响：高海拔球场（>1500m）对平原球队影响显著，含氧量低导致后程体能下降
- 高温高湿：亚热带球场（迈阿密/达拉斯/休斯顿）对欧洲球队消耗大
- 室内 vs 室外：封闭球场无风雨影响，技术流球队受益
- 时差/旅行：跨时区长途飞行后的状态影响

### 3. 爆冷风险评估
- 强队是否有慢热传统或关键球员伤停
- 弱队是否有爆冷基因（如 2022 沙特胜阿根廷）
- 小组赛首轮的不确定性更大
- 淘汰赛的保守心态可能导致加时/点球
- 裁判尺度、红黄牌、定位球防守等隐性因素

### 4. 特殊规则提醒
- 这是 48 队扩军后的首届世界杯，小组第三也有晋级机会
- 小组赛末轮需考虑"双方打平即可携手出线"的可能

## 输出格式（严格遵守，方便程序解析）
---PROBABILITIES---
HOME_WIN: <整数>
DRAW: <整数>
AWAY_WIN: <整数>
---SCORE---
<主队进球>-<客队进球>
---CONFIDENCE---
<高/中/低>
---REASONING---
<3-5句话综合推理，必须提及环境因素和爆冷风险>

{examples}"""


def _get_venue_profile(stadium: str) -> dict:
    """获取球场环境信息"""
    # 模糊匹配
    for key, profile in VENUE_PROFILES.items():
        if key[:4] in stadium or stadium[:4] in key:
            return profile
    return {"altitude": 0, "type": "室外", "climate": "暂无数据", "temp": "暂无数据"}


def _estimate_weather_impact(profile: dict, match_date_str: str) -> str:
    """根据气候和日期评估天气影响"""
    alt = profile["altitude"]
    climate = profile["climate"]
    venue_type = profile["type"]
    temp = profile["temp"]

    impacts = []

    # 高海拔影响
    if alt > 2000:
        impacts.append(f"极高海拔 ({alt}m)：含氧量约 78%，对平原球队影响巨大，后 30 分钟体能骤降。主队如有高原主场优势极大利好")
    elif alt > 1400:
        impacts.append(f"高海拔 ({alt}m)：含氧量约 85%，球速偏快，对不适应高原的球队有中等影响")
    elif alt > 500:
        impacts.append(f"中海拔 ({alt}m)：对体能有一定影响但不明显")

    # 温度
    if "34" in temp or "35" in temp or "36" in temp:
        impacts.append("极端高温 (>34°C)：需要大量补水暂停，欧洲球队不适风险高")
    elif "30" in temp or "31" in temp or "32" in temp or "33" in temp:
        impacts.append("高温 (30°C+)：午场比赛对体能要求高，不利于高位逼抢打法")

    # 湿度
    if "高湿" in climate or "湿度偏高" in climate:
        impacts.append("高湿度：体感温度更高，出汗量大，影响技术发挥")

    # 室内
    if "室内" in venue_type:
        impacts.append("室内/可开合顶棚：无风雨影响，草皮条件好，利于传控打法")

    # 风雨
    if "风" in climate or "海风" in climate:
        impacts.append("可能有风：影响长传和远射精度，对高空球打法不利")
    if "雨" in climate:
        impacts.append("可能有雨：场地湿滑，球速变快且不可预测，利好防守方")

    return "; ".join(impacts) if impacts else "无明显环境不利因素"


def build_match_prediction_prompt(
    match: Match,
    loader: DataLoader,
) -> Tuple[str, str]:
    """构造多维预测 prompt"""

    home = loader.get_team(match.home_team)
    away = loader.get_team(match.away_team)
    h2h = loader.get_head_to_head(match.home_team, match.away_team)

    examples_text = format_few_shot_for_system()
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(examples=examples_text)

    # 球场环境
    venue = _get_venue_profile(match.stadium)
    date_str = match.match_date.strftime("%Y-%m-%d %H:%M") if match.match_date else "待定"
    weather_impact = _estimate_weather_impact(venue, date_str)

    # 判断比赛阶段
    stage_hint = ""
    if match.stage.value == "小组赛":
        stage_hint = "这是小组赛，请注意：首轮双方会试探为主，末轮可能有默契球风险。"
    elif "决赛" in match.stage.value:
        stage_hint = "这是淘汰赛，请注意：双方会极为谨慎，加时和点球可能性增大，常规时间平局概率上升。"

    # 爆冷风险提示
    upset_hint = ""
    if home:
        if home.fifa_rank > 30 and (away and away.fifa_rank < 15):
            upset_hint += f"⚠️ 爆冷风险：主队{home.name}排名虽低但有主场之利，历史上世界杯东道主常有超常发挥。"
        if home.elo_rating - (away.elo_rating if away else 1500) > 300:
            upset_hint += f"\n⚠️ 大热倒灶风险：{home.name}实力明显占优，但世界杯历史上大热球队首轮翻车率约 15%。"
    if away and away.fifa_rank > 40 and home and home.fifa_rank < 10:
        upset_hint += f"\n💡 黑马潜力：{away.name}排名不高但可能有顽强防守+反击战术，强队久攻不下时需警惕。"

    def describe_team(t) -> str:
        if t is None:
            return "（数据缺失）"
        recent = ' '.join(t.recent_form) if t.recent_form else '暂无'
        players = ', '.join(t.key_players[:5]) if t.key_players else '暂无'
        return (
            f"FIFA 排名: {t.fifa_rank}\n"
            f"Elo 评分: {t.elo_rating:.0f}\n"
            f"所属足联: {t.confederation}\n"
            f"近期 5 场战绩: {recent}\n"
            f"场均进球: {t.avg_goals} / 场均失球: {t.avg_conceded}\n"
            f"世界杯冠军: {t.world_cup_titles} 次\n"
            f"主教练: {t.coach}\n"
            f"关键球员: {players}"
        )

    home_name = home.name if home else match.home_team
    away_name = away.name if away else match.away_team

    user_prompt = f"""请综合所有因素预测以下比赛：

【比赛信息】
赛事: 2026 FIFA 世界杯 {match.stage.value}
对阵: {home_name} (主) vs {away_name} (客)
日期: {date_str} 北京时间
场地: {match.stadium}, {match.city}

【场地环境】
海拔: {venue['altitude']}m
类型: {venue['type']}
气候: {venue['climate']}
气温范围: {venue['temp']}
环境影响评估: {weather_impact}

【{home_name} 数据】
{describe_team(home)}

【{away_name} 数据】
{describe_team(away)}

【历史交锋】
{h2h if h2h else '两队近年无直接交锋记录'}

【风险提示】
{stage_hint}{upset_hint}

请综合实力、环境、爆冷风险后进行预测。"""

    return system_prompt, user_prompt
