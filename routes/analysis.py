"""AI 分析路由 — 赛前/赛后分析"""
from flask import Blueprint, render_template, request, jsonify

from services.data_loader import DataLoader
from services.analyst import Analyst, AnalystError
from services.ai_client import AIClientError

analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')


@analysis_bp.route('/pre/<match_id>')
def pre_match_page(match_id):
    """赛前分析页面"""
    loader = DataLoader()
    loader.load_all()
    match = loader.get_match(match_id)
    if match is None:
        return render_template('error.html', message=f"比赛不存在: {match_id}"), 404
    home = loader.get_team(match.home_team)
    away = loader.get_team(match.away_team)

    from utils.cache import get_cached_analysis
    cached = get_cached_analysis(match_id, "pre_match")

    return render_template('analysis.html',
                           match=match, home=home, away=away,
                           analysis_type="pre_match", cached=cached)


@analysis_bp.route('/post/<match_id>')
def post_match_page(match_id):
    """赛后总结页面"""
    loader = DataLoader()
    loader.load_all()
    match = loader.get_match(match_id)
    if match is None:
        return render_template('error.html', message=f"比赛不存在: {match_id}"), 404
    if not match.is_played():
        return render_template('error.html', message="该比赛尚未进行"), 400
    home = loader.get_team(match.home_team)
    away = loader.get_team(match.away_team)

    from utils.cache import get_cached_analysis
    cached = get_cached_analysis(match_id, "post_match")

    return render_template('analysis.html',
                           match=match, home=home, away=away,
                           analysis_type="post_match", cached=cached)


@analysis_bp.route('/api/pre/<match_id>', methods=['POST'])
def api_pre_match(match_id):
    """API: 生成赛前分析"""
    try:
        analyst = Analyst()
        result = analyst.pre_match_analysis(match_id, force_refresh=True)
        return jsonify({"match_id": match_id, "analysis": result, "type": "pre_match"})
    except AnalystError as e:
        return jsonify({"error": str(e)}), 400
    except AIClientError as e:
        return jsonify({"error": f"AI 服务不可用: {e}"}), 503


@analysis_bp.route('/api/post/<match_id>', methods=['POST'])
def api_post_match(match_id):
    """API: 生成赛后总结"""
    try:
        analyst = Analyst()
        result = analyst.post_match_analysis(match_id, force_refresh=True)
        return jsonify({"match_id": match_id, "analysis": result, "type": "post_match"})
    except AnalystError as e:
        return jsonify({"error": str(e)}), 400
    except AIClientError as e:
        return jsonify({"error": f"AI 服务不可用: {e}"}), 503
