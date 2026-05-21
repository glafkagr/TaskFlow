from flask import Flask
from flask_smorest import Api

from config import Config
from app.web import web_bp
from app.api import api_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    api = Api(app)

    # Register normal web blueprint (Jinja)
    app.register_blueprint(web_bp)

    # Register API blueprint (Smorest)
    api.register_blueprint(api_bp)

    return app
