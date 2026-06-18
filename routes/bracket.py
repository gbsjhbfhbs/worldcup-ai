"""淘汰赛对阵图 & 冠军预测路由"""
from flask import Blueprint, render_template, request, jsonify

from services.data_loader import DataLoader
from services.simulator import Simulator
from services.ai_client import AIClientError

bracket_bp = Blueprint('bracket', __name__, url_prefix='/bracket')


@bracket_bp.route('/')
def bracket_page():
    """淘汰赛对阵图页面"""
    loader = DataLoader()
    loader.load_all()
    return render_template('bracket.html')


@bracket_bp.route('/champion')
def champion_page():
    """冠军预测页面"""
    return render_template('champion.html')


@bracket_bp.route('/api/simulate', methods=['POST'])
def api_simulate():
    """API: 运行冠军模拟"""
    iterations = 1000
    if request.is_json:
        iterations = min(request.json.get('iterations', 1000), 5000)

    try:
        sim = Simulator()
        odds = sim.run_simulation(iterations=iterations)
        return jsonify({
            "iterations": iterations,
            "odds": [
                {
                    "team_code": o.team_code,
                    "team_name": o.team_name,
                    "probability": round(o.probability, 4),
                    "win_count": o.win_count,
                    "elo_rating": o.elo_rating,
                }
                for o in odds[:10]  # 只返回前 10 名
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
