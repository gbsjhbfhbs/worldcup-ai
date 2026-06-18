"""SQLite 数据库初始化和连接管理"""
import sqlite3
from pathlib import Path
from config import Config


def get_db_path() -> Path:
    """获取数据库文件路径，确保目录存在"""
    db_path = Config.DATABASE
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def get_connection() -> sqlite3.Connection:
    """获取数据库连接"""
    conn = sqlite3.connect(str(get_db_path()))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """初始化数据库表结构"""
    conn = get_connection()
    try:
        conn.executescript("""
        -- AI 预测缓存
        CREATE TABLE IF NOT EXISTS prediction_cache (
            match_id TEXT PRIMARY KEY,
            home_win_prob REAL NOT NULL,
            draw_prob REAL NOT NULL,
            away_win_prob REAL NOT NULL,
            predicted_home_score INTEGER NOT NULL,
            predicted_away_score INTEGER NOT NULL,
            confidence TEXT NOT NULL,
            reasoning TEXT NOT NULL,
            model_used TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );

        -- AI 分析缓存
        CREATE TABLE IF NOT EXISTS analysis_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id TEXT NOT NULL,
            analysis_type TEXT NOT NULL,   -- 'pre_match' | 'post_match'
            content TEXT NOT NULL,
            model_used TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            UNIQUE(match_id, analysis_type)
        );

        -- 模拟记录
        CREATE TABLE IF NOT EXISTS simulation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            team_code TEXT NOT NULL,
            win_count INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );

        -- 历史预测准确率
        CREATE TABLE IF NOT EXISTS prediction_accuracy (
            match_id TEXT PRIMARY KEY,
            predicted_home_score INTEGER NOT NULL,
            predicted_away_score INTEGER NOT NULL,
            actual_home_score INTEGER NOT NULL,
            actual_away_score INTEGER NOT NULL,
            correct_outcome INTEGER NOT NULL DEFAULT 0,  -- 1=正确
            exact_score INTEGER NOT NULL DEFAULT 0       -- 1=完全匹配
        );
        """)
        conn.commit()
    finally:
        conn.close()
