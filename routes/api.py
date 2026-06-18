"""REST API 路由 — 供前端 JS 异步调用"""
from flask import Blueprint, request, jsonify

from services.data_loader import DataLoader
from services.predictor import Predictor, PredictorError
from services.ai_client import AIClientError
from utils.validators import validate_match_id
from utils.cache import get_cached_prediction

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/predict/<match_id>', methods=['POST'])
def predict_match(match_id):
    """触发单场比赛预测（同步返回）"""
    if not validate_match_id(match_id):
        return jsonify({"error": "match_id 格式无效"}), 400

    force = request.json.get('force_refresh', False) if request.is_json else False

    try:
        predictor = Predictor()
        result = predictor.predict(match_id, force_refresh=force)
        return jsonify({
            "match_id": result.match_id,
            "home_win_prob": round(result.home_win_prob, 3),
            "draw_prob": round(result.draw_prob, 3),
            "away_win_prob": round(result.away_win_prob, 3),
            "predicted_score": result.score_display(),
            "confidence": result.confidence,
            "reasoning": result.reasoning,
            "model_used": result.model_used,
        })
    except PredictorError as e:
        return jsonify({"error": str(e)}), 400
    except AIClientError as e:
        return jsonify({"error": f"AI 服务暂时不可用: {e}"}), 503
    except Exception as e:
        return jsonify({"error": f"服务器内部错误: {e}"}), 500


@api_bp.route('/prediction/<match_id>', methods=['GET'])
def get_prediction(match_id):
    """获取已有预测（只读缓存，不触发新预测）"""
    if not validate_match_id(match_id):
        return jsonify({"error": "match_id 格式无效"}), 400

    cached = get_cached_prediction(match_id)
    if cached:
        return jsonify({
            "match_id": cached.match_id,
            "home_win_prob": round(cached.home_win_prob, 3),
            "draw_prob": round(cached.draw_prob, 3),
            "away_win_prob": round(cached.away_win_prob, 3),
            "predicted_score": cached.score_display(),
            "confidence": cached.confidence,
            "reasoning": cached.reasoning,
        })
    return jsonify({"cached": False, "message": "暂无预测结果"}), 404


@api_bp.route('/teams', methods=['GET'])
def list_teams():
    """获取所有球队"""
    loader = DataLoader()
    loader.load_all()
    teams = loader.get_all_teams()
    result = {}
    for code, team in teams.items():
        result[code] = {
            "name": team.name,
            "name_en": team.name_en,
            "fifa_rank": team.fifa_rank,
            "elo_rating": team.elo_rating,
            "confederation": team.confederation,
            "group": team.group,
            "world_cup_titles": team.world_cup_titles,
        }
    return jsonify(result)


@api_bp.route('/matches', methods=['GET'])
def list_matches():
    """获取所有比赛"""
    loader = DataLoader()
    loader.load_all()
    matches = loader.get_all_matches()
    result = []
    for m in matches:
        result.append({
            "match_id": m.match_id,
            "home_team": m.home_team,
            "away_team": m.away_team,
            "stage": m.stage.value,
            "group": m.group,
            "match_date": m.match_date.isoformat() if m.match_date else None,
            "stadium": m.stadium,
            "city": m.city,
            "home_score": m.home_score,
            "away_score": m.away_score,
            "is_played": m.is_played(),
        })
    return jsonify(result)
