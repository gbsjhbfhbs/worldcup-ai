"""球队数据中心路由"""
from flask import Blueprint, render_template, abort

from services.data_loader import DataLoader

teams_bp = Blueprint('teams', __name__, url_prefix='/teams')


@teams_bp.route('/')
def team_list():
    """球队列表"""
    loader = DataLoader()
    loader.load_all()
    teams = loader.get_all_teams()
    return render_template('teams.html', teams=teams)


@teams_bp.route('/<code>')
def team_detail(code):
    """球队详情"""
    loader = DataLoader()
    loader.load_all()
    team = loader.get_team(code.upper())
    if team is None:
        abort(404)
    return render_template('team_detail.html', team=team)
