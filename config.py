"""全局配置"""
import os
from pathlib import Path


class Config:
    """应用配置（不可变常量）"""
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    DATABASE = BASE_DIR / "instance" / "worldcup.db"
    FLAGS_DIR = BASE_DIR / "static" / "img" / "flags"

    # Anthropic API — 从多个可能的环境变量读取
    ANTHROPIC_API_KEY = (
        os.environ.get("ANTHROPIC_API_KEY", "")
        or os.environ.get("ANTHROPIC_AUTH_TOKEN", "")
    )
    ANTHROPIC_BASE_URL = os.environ.get("ANTHROPIC_BASE_URL", "")

    # 模型选择（适配 DeepSeek 代理等兼容 API）
    PREDICTION_MODEL = os.environ.get("WC_PREDICTION_MODEL",
        os.environ.get("ANTHROPIC_DEFAULT_HAIKU_MODEL_NAME", "claude-haiku-4-5-20251001"))
    ANALYSIS_MODEL = os.environ.get("WC_ANALYSIS_MODEL",
        os.environ.get("ANTHROPIC_DEFAULT_SONNET_MODEL_NAME", "claude-sonnet-4-6"))

    # 生产环境
    SECRET_KEY = os.environ.get("SECRET_KEY", "worldcup-ai-2026-dev")
    PORT = int(os.environ.get("PORT", 5000))

    # 缓存与重试
    CACHE_TTL_HOURS = 24
    MAX_RETRIES = 3
    REQUEST_TIMEOUT = 60

    # 蒙特卡洛模拟
    DEFAULT_SIMULATIONS = 1000  # 默认模拟次数
    MAX_SIMULATIONS = 5000      # 单次模拟上限
