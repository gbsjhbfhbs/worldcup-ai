"""比赛数据模型 — 不可变 dataclass"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Tuple


class MatchStage(Enum):
    """比赛阶段"""
    GROUP = "小组赛"
    ROUND_OF_32 = "1/16 决赛"
    ROUND_OF_16 = "1/8 决赛"
    QUARTER_FINAL = "1/4 决赛"
    SEMI_FINAL = "半决赛"
    THIRD_PLACE = "三四名决赛"
    FINAL = "决赛"


@dataclass(frozen=True)
class Match:
    """一场比赛的核心数据（不可变）"""
    match_id: str                       # 如 "G-A-1" 或 "KO-R16-3"
    home_team: str                      # FIFA 三字母代码，如 "FRA"
    away_team: str
    stage: MatchStage
    group: Optional[str] = None         # 小组赛有值，如 "A"
    match_date: Optional[datetime] = None
    stadium: str = ""
    city: str = ""
    home_score: Optional[int] = None    # None = 未进行
    away_score: Optional[int] = None

    def is_played(self) -> bool:
        return self.home_score is not None

    def score_display(self) -> str:
        if not self.is_played():
            return "vs"
        return f"{self.home_score} - {self.away_score}"


@dataclass(frozen=True)
class PredictionResult:
    """AI 预测结果（不可变）"""
    match_id: str
    home_win_prob: float                # 0.0 ~ 1.0
    draw_prob: float
    away_win_prob: float
    predicted_home_score: int
    predicted_away_score: int
    confidence: str                     # "高" / "中" / "低"
    reasoning: str                      # AI 推理过程
    model_used: str
    created_at: str = ""

    def __post_init__(self):
        # 校验概率和 ≈ 1.0
        total = self.home_win_prob + self.draw_prob + self.away_win_prob
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"概率和必须为 1.0，当前为 {total}")

    def score_display(self) -> str:
        return f"{self.predicted_home_score} - {self.predicted_away_score}"

    def prob_home_pct(self) -> str:
        return f"{self.home_win_prob * 100:.0f}%"

    def prob_draw_pct(self) -> str:
        return f"{self.draw_prob * 100:.0f}%"

    def prob_away_pct(self) -> str:
        return f"{self.away_win_prob * 100:.0f}%"
