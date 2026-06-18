"""比赛列表和详情路由"""
from flask import Blueprint, render_template, abort

from services.data_loader import DataLoader

matches_bp = Blueprint('matches', __name__, url_prefix='/matches')


@matches_bp.route('/')
def match_list():
    """全部比赛列表"""
    loader = DataLoader()
    loader.load_all()

    all_matches = loader.get_all_matches()
    groups = sorted(set(
        m.group for m in all_matches if m.group
    ))
    group_labels = loader.get_all_group_labels()

    return render_template(
        'matches.html',
        matches=all_matches,
        groups=groups,
        group_labels=group_labels,
    )


@matches_bp.route('/<match_id>')
def match_detail(match_id):
    """比赛详情页（含预测入口）"""
    loader = DataLoader()
    loader.load_all()

    match = loader.get_match(match_id)
    if match is None:
        abort(404)

    home = loader.get_team(match.home_team)
    away = loader.get_team(match.away_team)

    # 检查是否有缓存的 AI 预测
    from utils.cache import get_cached_prediction, get_cached_analysis
    cached_pred = get_cached_prediction(match_id)
    cached_post = get_cached_analysis(match_id, "post_match")

    return render_template(
        'match_detail.html',
        match=match,
        home=home,
        away=away,
        cached_pred=cached_pred,
        cached_post=cached_post,
    )
