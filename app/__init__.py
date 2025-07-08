import os
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
load_dotenv()

socketio = SocketIO(cors_allowed_origins='*')

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    #################For debugging##################
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    ################################################
    app.config['DB_PATH'] = os.path.join('data', 'test.db')
    app.config['QUERY_DB_PATH'] = os.path.join('data', 'saved_queries.db')
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    from app.routes.dashboard_routes import bp as dashboard_routes
    app.register_blueprint(dashboard_routes)
    
    socketio.init_app(app) 

    return app