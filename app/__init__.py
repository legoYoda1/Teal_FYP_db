import os
from flask import Flask
from flask_socketio import SocketIO
from sqlalchemy import create_engine
from dotenv import load_dotenv
from cachetools import TTLCache
load_dotenv()

socketio = SocketIO(cors_allowed_origins='*')

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    #################For debugging##################
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    ################################################
    app.config['DB_PATH'] = os.getenv("MYSQL_DB_URI")
    app.config['QUERY_DB_PATH'] = os.getenv("MYSQL_QUERY_DB_URI")

    app.db_engine = create_engine(app.config['DB_PATH'])
    app.query_db_engine = create_engine(app.config['QUERY_DB_PATH'])

    app.config["SECRET_KEY"] = os.getenv("FLASK_SESSIONS_SECRET_KEY")

    # Dropbox OAuth Configuration
    app.dropbox_app_key = os.getenv("DROPBOX_APP_KEY")
    app.dropbox_app_secret = os.getenv("DROPBOX_APP_SECRET")
    app.dropbox_refresh_token = os.getenv("DROPBOX_REFRESH_TOKEN")
    app.dropbox_token_cache = TTLCache(maxsize=1, ttl=14400)  # 4 hours

    # Set TTL to 30 days (in seconds) = 30 * 24 * 60 * 60 = 2,592,000 seconds
    app.saved_query_button_cache = TTLCache(maxsize=1000, ttl=2592000)
    app.overview_stats_cache = TTLCache(maxsize=1000, ttl=2592000)

    from app.routes.dashboard_routes import bp as dashboard_routes
    app.register_blueprint(dashboard_routes)
    
    socketio.init_app(app) 

    return app