import os
from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins='*')

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    #################For debugging##################
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    ################################################
    app.config['DB_PATH'] = os.path.join('data', 'test.db')

    from app.routes.dashboard_routes import bp as dashboard_routes
    app.register_blueprint(dashboard_routes)

    from app.routes.report_upload_routes import bp as report_uploads_routes_bp
    app.register_blueprint(report_uploads_routes_bp)
    
    socketio.init_app(app) 

    return app