"""AI 响应缓存 — 基于 SQLite，减少重复 API 调用"""
import sqlite3
from datetime import datetime, timedelta
from typing import Optional

from models.match import PredictionResult
from utils.db import get_connection
from config import Config


def cache_prediction(result: PredictionResult) -> None:
    """缓存预测结果"""
    conn = get_connection()
    try:
        conn.execute("""
            INSERT OR REPLACE INTO prediction_cache
            (match_id, home_win_prob, draw_prob, away_win_prob,
             predicted_home_score, predicted_away_score,
             confidence, reasoning, model_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result.match_id,
            result.home_win_prob,
            result.draw_prob,
            result.away_win_prob,
            result.predicted_home_score,
            result.predicted_away_score,
            result.confidence,
            result.reasoning,
            result.model_used,
        ))
        conn.commit()
    finally:
        conn.close()


def get_cached_prediction(match_id: str) -> Optional[PredictionResult]:
    """获取缓存的预测（检查 TTL）"""
    conn = get_connection()
    try:
        row = conn.execute("""
            SELECT * FROM prediction_cache
            WHERE match_id = ?
            AND datetime(created_at, 'localtime') > datetime('now', 'localtime', ?)
        """, (match_id, f'-{Config.CACHE_TTL_HOURS} hours')).fetchone()

        if row is None:
            return None

        return PredictionResult(
            match_id=row["match_id"],
            home_win_prob=row["home_win_prob"],
            draw_prob=row["draw_prob"],
            away_win_prob=row["away_win_prob"],
            predicted_home_score=row["predicted_home_score"],
            predicted_away_score=row["predicted_away_score"],
            confidence=row["confidence"],
            reasoning=row["reasoning"],
            model_used=row["model_used"],
            created_at=row["created_at"],
        )
    finally:
        conn.close()


def cache_analysis(match_id: str, analysis_type: str, content: str, model: str) -> None:
    """缓存 AI 分析（赛前/赛后）"""
    conn = get_connection()
    try:
        conn.execute("""
            INSERT OR REPLACE INTO analysis_cache
            (match_id, analysis_type, content, model_used)
            VALUES (?, ?, ?, ?)
        """, (match_id, analysis_type, content, model))
        conn.commit()
    finally:
        conn.close()


def get_cached_analysis(match_id: str, analysis_type: str) -> Optional[str]:
    """获取缓存的分析内容"""
    conn = get_connection()
    try:
        row = conn.execute("""
            SELECT content FROM analysis_cache
            WHERE match_id = ? AND analysis_type = ?
        """, (match_id, analysis_type)).fetchone()
        return row["content"] if row else None
    finally:
        conn.close()
