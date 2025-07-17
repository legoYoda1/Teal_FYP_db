import os
from flask import Flask
from flask_socketio import SocketIO
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()

socketio = SocketIO(cors_allowed_origins='*')

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    #################For debugging##################
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    ################################################
    app.config['DB_PATH'] = os.getenv("MYSQL_DB_URI", "sqlite:///data/warehouse.db")
    app.config['QUERY_DB_PATH'] = os.getenv("MYSQL_QUERY_DB_URI", "sqlite:///data/query.db")

    app.db_engine = create_engine(app.config['DB_PATH'])
    app.query_db_engine = create_engine(app.config['QUERY_DB_PATH'])
    #app.config['DB_PATH'] = os.path.join('data', 'warehouse.db') # sqlite database paths
    #app.config['QUERY_DB_PATH'] = os.path.join('data', 'query.db') # sqlite database paths
    app.config["SECRET_KEY"] = os.getenv("FLASK_SESSIONS_SECRET_KEY")

    from app.routes.dashboard_routes import bp as dashboard_routes
    app.register_blueprint(dashboard_routes)
    
    socketio.init_app(app) 

    return app