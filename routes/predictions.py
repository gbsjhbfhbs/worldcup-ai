"""预测相关页面路由"""
from flask import Blueprint, render_template, request, jsonify

from services.data_loader import DataLoader
from services.predictor import Predictor, PredictorError
from services.ai_client import AIClient, AIClientError

predictions_bp = Blueprint('predictions', __name__, url_prefix='/predictions')


@predictions_bp.route('/')
def prediction_home():
    """预测首页"""
    loader = DataLoader()
    loader.load_all()
    upcoming = loader.get_upcoming_matches(limit=20)
    return render_template('prediction_home.html', upcoming=upcoming)


@predictions_bp.route('/<match_id>')
def predict_page(match_id):
    """单场预测页"""
    loader = DataLoader()
    loader.load_all()

    match = loader.get_match(match_id)
    if match is None:
        return render_template('error.html', message=f"比赛不存在: {match_id}"), 404

    home = loader.get_team(match.home_team)
    away = loader.get_team(match.away_team)

    # 尝试从缓存获取预测
    from utils.cache import get_cached_prediction
    cached = get_cached_prediction(match_id)

    return render_template(
        'prediction.html',
        match=match,
        home=home,
        away=away,
        cached=cached,
    )
