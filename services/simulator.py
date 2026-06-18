"""蒙特卡洛淘汰赛模拟 — 多次迭代预测冠军概率"""
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from config import Config
from services.ai_client import AIClient, AIClientError
from services.data_loader import DataLoader
from models.team import Team


@dataclass
class SimResult:
    """一次模拟的淘汰赛结果"""
    champion: str                           # 冠军代码
    runner_up: str                          # 亚军
    semifinalists: Tuple[str, str]          # 四强
    round_results: List[dict] = field(default_factory=list)  # 每轮结果


@dataclass
class ChampionOdds:
    """夺冠概率"""
    team_code: str
    team_name: str
    win_count: int
    probability: float                     # 0.0 ~ 1.0
    elo_rating: float


class Simulator:
    """蒙特卡洛淘汰赛模拟器"""

    def __init__(self, ai_client: AIClient = None, loader: DataLoader = None):
        self.ai = ai_client or AIClient()
        self.loader = loader or DataLoader()
        self.loader.load_all()

    def run_simulation(self, iterations: int = None) -> List[ChampionOdds]:
        """运行蒙特卡洛模拟，返回夺冠概率列表（降序）"""
        iterations = iterations or Config.DEFAULT_SIMULATIONS
        iterations = min(iterations, Config.MAX_SIMULATIONS)

        teams = self.loader.get_all_teams()
        team_list = list(teams.keys())
        win_counts = {t: 0 for t in team_list}

        print(f"[Simulator] 开始 {iterations} 次模拟...")
        start_time = time.time()

        for i in range(iterations):
            champion = self._simulate_knockout(team_list)
            win_counts[champion] += 1

            if (i + 1) % 100 == 0:
                elapsed = time.time() - start_time
                print(f"  已完成 {i + 1}/{iterations} ({elapsed:.0f}s)")

        # 转换为概率
        odds = []
        for code, team in teams.items():
            if win_counts[code] > 0:
                odds.append(ChampionOdds(
                    team_code=code,
                    team_name=team.name,
                    win_count=win_counts[code],
                    probability=win_counts[code] / iterations,
                    elo_rating=team.elo_rating,
                ))

        odds.sort(key=lambda x: x.probability, reverse=True)
        elapsed = time.time() - start_time
        print(f"[Simulator] 完成 {iterations} 次模拟 ({elapsed:.0f}s)")

        return odds

    def _simulate_knockout(self, team_list: List[str]) -> str:
        """模拟一次淘汰赛（基于 Elo 评分的随机晋级）"""
        remaining = list(team_list)
        random.shuffle(remaining)

        # 淘汰赛轮次：32 -> 16 -> 8 -> 4 -> 2 -> 1
        while len(remaining) > 1:
            next_round = []
            for i in range(0, len(remaining), 2):
                if i + 1 >= len(remaining):
                    next_round.append(remaining[i])
                    continue
                t1, t2 = remaining[i], remaining[i + 1]
                winner = self._match_winner(t1, t2)
                next_round.append(winner)
            remaining = next_round

        return remaining[0]

    def _match_winner(self, team1: str, team2: str) -> str:
        """基于 Elo 评分 + 随机扰动计算胜者"""
        t1 = self.loader.get_team(team1)
        t2 = self.loader.get_team(team2)

        elo1 = t1.elo_rating if t1 else 1500
        elo2 = t2.elo_rating if t2 else 1500

        # Elo 胜率公式
        expected1 = 1.0 / (1.0 + 10.0 ** ((elo2 - elo1) / 400.0))
        # 加随机扰动（模拟淘汰赛不确定性）
        roll = random.random()
        # 淘汰赛有加时/点球可能，弱队爆冷概率略高
        adjusted = expected1 * 0.85 + 0.075  # 收紧强队优势，增加随机性

        return team1 if roll < adjusted else team2

    def predict_single_match(self, team1_code: str, team2_code: str) -> Tuple[float, float]:
        """预测单场淘汰赛胜负概率（Elo-based）"""
        t1 = self.loader.get_team(team1_code)
        t2 = self.loader.get_team(team2_code)
        elo1 = t1.elo_rating if t1 else 1500
        elo2 = t2.elo_rating if t2 else 1500
        p1 = 1.0 / (1.0 + 10.0 ** ((elo2 - elo1) / 400.0))
        return (p1, 1.0 - p1)
