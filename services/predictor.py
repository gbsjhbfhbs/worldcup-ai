"""比赛预测服务 — 协调 prompt 构建、API 调用、响应解析、缓存"""
import re
from typing import Optional

from config import Config
from models.match import PredictionResult, Match
from services.ai_client import AIClient, AIClientError
from services.data_loader import DataLoader
from prompts.match_prediction import build_match_prediction_prompt
from utils.validators import validate_probabilities, parse_score
from utils.cache import cache_prediction, get_cached_prediction


class PredictorError(Exception):
    """预测服务错误"""
    pass


class Predictor:
    """比赛预测器"""

    def __init__(self, ai_client: AIClient = None, loader: DataLoader = None):
        self.ai = ai_client or AIClient()
        self.loader = loader or DataLoader()

    def predict(self, match_id: str, force_refresh: bool = False) -> PredictionResult:
        """预测单场比赛（优先返回缓存）"""
        # 1. 检查缓存
        if not force_refresh:
            cached = get_cached_prediction(match_id)
            if cached:
                return cached

        # 2. 加载比赛数据
        match = self._ensure_loaded().get_match(match_id)
        if match is None:
            raise PredictorError(f"比赛不存在: {match_id}")
        if match.is_played():
            raise PredictorError(f"比赛已结束: {match_id} ({match.score_display()})")

        # 3. 构造 prompt
        system_prompt, user_prompt = build_match_prediction_prompt(match, self.loader)

        # 4. 调用 AI
        try:
            raw_response = self.ai.call(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=Config.PREDICTION_MODEL,
                max_tokens=1000,
            )
        except AIClientError as e:
            raise PredictorError(f"AI 服务不可用: {e}")

        # 5. 解析响应
        result = self._parse_response(match_id, raw_response)

        # 6. 缓存
        cache_prediction(result)

        return result

    def _parse_response(self, match_id: str, raw: str) -> PredictionResult:
        """解析 AI 结构化输出"""
        # 提取概率
        home_win = self._extract_int(raw, r'HOME_WIN:\s*(\d+)', default=33)
        draw = self._extract_int(raw, r'DRAW:\s*(\d+)', default=34)
        away_win = self._extract_int(raw, r'AWAY_WIN:\s*(\d+)', default=33)

        # 如果解析出来的概率不合理，使用默认值
        if not validate_probabilities(home_win, draw, away_win):
            print(f"[Predictor] 解析概率失败: {home_win}/{draw}/{away_win}，使用默认值")
            home_win, draw, away_win = 34, 33, 33

        # 提取比分
        score_match = re.search(r'---SCORE---\s*\n?\s*(\d{1,2})\s*-\s*(\d{1,2})', raw)
        if score_match:
            home_score = int(score_match.group(1))
            away_score = int(score_match.group(2))
        else:
            # fallback：搜索任意比分格式
            parsed = parse_score(raw)
            if parsed:
                home_score, away_score = parsed
            else:
                home_score, away_score = 1, 1  # 兜底

        # 提取置信度
        conf_match = re.search(r'---CONFIDENCE---\s*\n?\s*(高|中|低)', raw)
        confidence = conf_match.group(1) if conf_match else "中"

        # 提取推理
        reasoning_match = re.search(r'---REASONING---\s*\n?\s*(.+?)$', raw, re.DOTALL)
        reasoning = reasoning_match.group(1).strip() if reasoning_match else "（AI 未提供推理）"

        return PredictionResult(
            match_id=match_id,
            home_win_prob=home_win / 100.0,
            draw_prob=draw / 100.0,
            away_win_prob=away_win / 100.0,
            predicted_home_score=home_score,
            predicted_away_score=away_score,
            confidence=confidence,
            reasoning=reasoning,
            model_used=Config.PREDICTION_MODEL,
        )

    def _extract_int(self, text: str, pattern: str, default: int = 0) -> int:
        """从文本中提取整数"""
        match = re.search(pattern, text)
        if match:
            val = int(match.group(1))
            if 0 <= val <= 100:
                return val
        return default

    def _ensure_loaded(self) -> DataLoader:
        """确保数据已加载"""
        self.loader.load_all()
        return self.loader
