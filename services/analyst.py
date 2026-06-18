"""AI 赛事分析 — 赛前深度分析和赛后总结"""
from config import Config
from services.ai_client import AIClient, AIClientError
from services.data_loader import DataLoader
from models.match import Match
from models.team import Team
from utils.cache import cache_analysis, get_cached_analysis


class AnalystError(Exception):
    """分析服务错误"""
    pass


class Analyst:
    """AI 赛事分析师"""

    def __init__(self, ai_client: AIClient = None, loader: DataLoader = None):
        self.ai = ai_client or AIClient()
        self.loader = loader or DataLoader()
        self.loader.load_all()

    def pre_match_analysis(self, match_id: str, force_refresh: bool = False) -> str:
        """赛前深度分析"""
        if not force_refresh:
            cached = get_cached_analysis(match_id, "pre_match")
            if cached:
                return cached

        match = self.loader.get_match(match_id)
        if match is None:
            raise AnalystError(f"比赛不存在: {match_id}")

        home = self.loader.get_team(match.home_team)
        away = self.loader.get_team(match.away_team)

        system_prompt = """你是一位资深足球评论员和战术分析师，拥有 20 年经验。
请对即将进行的 2026 世界杯比赛提供深度赛前分析。

分析要求（用 Markdown 格式）：
## 近期状态对比
- 两队最近 5 场比赛表现分析
- 攻防两端数据解读

## 关键对位
- 3 组关键球员对位分析
- 哪个位置将决定比赛走向

## 战术预测
- 双方可能使用的阵型和打法
- 比赛节奏预判（快攻/控球/防反）

## 胜负走势
- 三种可能的结果分别需要什么条件
- 你的最终判断

## 看点提示
- 本场比赛最值得关注的 3 个看点"""

        home_text = self._describe_team(home)
        away_text = self._describe_team(away)
        date_str = match.match_date.strftime("%Y-%m-%d %H:%M") if match.match_date else "待定"

        user_prompt = f"""2026 世界杯 {match.stage.value}
对阵: {home_text['name']} (主) vs {away_text['name']} (客)
日期: {date_str} (北京时间)
场地: {match.stadium}, {match.city}

主队数据:
{home_text['detail']}

客队数据:
{away_text['detail']}

请输出赛前分析。"""

        try:
            result = self.ai.call(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=Config.ANALYSIS_MODEL,
                max_tokens=3000,
            )
            cache_analysis(match_id, "pre_match", result, Config.ANALYSIS_MODEL)
            return result
        except AIClientError as e:
            raise AnalystError(f"AI 服务不可用: {e}")

    def post_match_analysis(self, match_id: str, force_refresh: bool = False) -> str:
        """赛后总结"""
        if not force_refresh:
            cached = get_cached_analysis(match_id, "post_match")
            if cached:
                return cached

        match = self.loader.get_match(match_id)
        if match is None:
            raise AnalystError(f"比赛不存在: {match_id}")
        if not match.is_played():
            raise AnalystError(f"比赛尚未进行，无法生成赛后分析")

        home = self.loader.get_team(match.home_team)
        away = self.loader.get_team(match.away_team)

        system_prompt = """你是一位资深足球评论员。请对刚结束的 2026 世界杯比赛撰写赛后总结。

分析要求（用 Markdown 格式）：
## 比赛回顾
- 比分和关键进球描述
- 比赛过程简述

## 关键转折点
- 改变比赛走势的关键时刻
- 教练的战术调整

## 球员评分
- 双方最佳球员 (MVP)
- 表现不佳的球员

## 晋级形势
- 这个结果对小组出线的影响
- 下一轮的关键战"""

        home_name = home.name if home else match.home_team
        away_name = away.name if away else match.away_team

        user_prompt = f"""2026 世界杯比赛已结束：
{home_name} {match.home_score} - {match.away_score} {away_name}
赛事: {match.stage.value}
日期: {match.match_date.strftime('%Y-%m-%d %H:%M') if match.match_date else '未知'}
场地: {match.stadium}

请撰写赛后总结。"""

        try:
            result = self.ai.call(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=Config.ANALYSIS_MODEL,
                max_tokens=3000,
            )
            cache_analysis(match_id, "post_match", result, Config.ANALYSIS_MODEL)
            return result
        except AIClientError as e:
            raise AnalystError(f"AI 服务不可用: {e}")

    def _describe_team(self, team: Team) -> dict:
        """描述球队数据"""
        if team is None:
            return {"name": "未知", "detail": "数据缺失"}
        recent = ' '.join(team.recent_form)
        players = ', '.join(team.key_players[:5])
        detail = (
            f"FIFA 排名: {team.fifa_rank}\n"
            f"Elo 评分: {team.elo_rating:.0f}\n"
            f"近期 5 场: {recent}\n"
            f"场均进球: {team.avg_goals} / 场均失球: {team.avg_conceded}\n"
            f"关键球员: {players}\n"
            f"世界杯冠军: {team.world_cup_titles} 次\n"
            f"主教练: {team.coach}"
        )
        return {"name": team.name, "detail": detail}
