"""AI 预测世界杯 2026 — Flask 应用入口"""
import sys
from pathlib import Path

# 确保项目根目录在 sys.path 中
sys.path.insert(0, str(Path(__file__).resolve().parent))

from flask import Flask, render_template
from config import Config
from utils.db import init_db


def create_app() -> Flask:
    """Flask 应用工厂"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'worldcup-ai-2026-dev'

    # 确保 instance 目录存在
    instance_dir = Path(__file__).resolve().parent / "instance"
    instance_dir.mkdir(parents=True, exist_ok=True)

    # 初始化数据库
    init_db()

    # 注册蓝图
    from routes.main import main_bp
    from routes.matches import matches_bp
    from routes.predictions import predictions_bp
    from routes.teams import teams_bp
    from routes.bracket import bracket_bp
    from routes.analysis import analysis_bp
    from routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(matches_bp)
    app.register_blueprint(predictions_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(bracket_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(api_bp)

    # 全局模板变量 — 小组中文标签
    @app.context_processor
    def inject_group_labels():
        from services.data_loader import DataLoader
        loader = DataLoader()
        loader.load_all()
        return {'group_labels': loader.get_all_group_labels()}

    # 全局错误处理
    @app.errorhandler(404)
    def not_found(e):
        return render_template('error.html',
                              message='页面不存在，请检查链接是否正确。'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('error.html',
                              message='服务器内部错误，请稍后重试。'), 500

    return app


# 模块级 app 实例（Gunicorn 生产环境用）
app = create_app()


# 开发模式直接运行
if __name__ == '__main__':
    print("=" * 50)
    print("[AI 预测世界杯 2026]")
    print("=" * 50)
    print()

    # 检查 API Key
    if not Config.ANTHROPIC_API_KEY:
        print("[!] 未检测到 ANTHROPIC_API_KEY 环境变量")
        print("    AI 预测功能将不可用，但可以浏览比赛数据和球队信息。")
        print("    设置方法: set ANTHROPIC_API_KEY=sk-ant-xxx")
        print()

    app = create_app()

    # 获取本机局域网 IP
    import socket
    local_ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass

    print("[*] 启动服务器:")
    print(f"    本机访问: http://127.0.0.1:5000")
    if local_ip != "127.0.0.1":
        print(f"    局域网访问: http://{local_ip}:5000")
    print("    按 Ctrl+C 停止")
    print()

    # 生产环境使用 host='0.0.0.0' 允许外部访问
    # 注意：关闭 debug=True 前务必设置 SECRET_KEY
    app.run(host='0.0.0.0', port=5000, debug=True)
