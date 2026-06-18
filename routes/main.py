"""首页和基础路由"""
from flask import Blueprint, render_template

from services.data_loader import DataLoader

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """首页：今日比赛 + 即将进行"""
    loader = DataLoader()
    loader.load_all()

    from datetime import datetime
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_matches = loader.get_matches_by_date(today_str)
    today_ids = {m.match_id for m in today_matches}
    # 排除今日比赛
    upcoming = [m for m in loader.get_upcoming_matches(limit=10)
                if m.match_id not in today_ids]
    played = loader.get_played_matches()

    return render_template(
        'index.html',
        today_matches=today_matches,
        upcoming=upcoming,
        played=played,
    )


@main_bp.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')
