# from flask import Flask
# from flask_smorest import Api

# from config import Config
# from app.web import web_bp
# from app.api import api_bp


# def create_app():
#     app = Flask(__name__)

#     app.config.from_object(Config)

#     api = Api(app)

#     # Register normal web blueprint (Jinja)
#     app.register_blueprint(web_bp)

#     # Register API blueprint (Smorest)
#     api.register_blueprint(api_bp)

#     return app
from flask import Flask,session
from dotenv import load_dotenv
from flask_login import LoginManager, current_user

# Import models
from app.models import (
    User,
    Project,
    Task,
    Comment,
    Attachment
)

load_dotenv()

from app.extensions import (
    db,
    jwt,
    migrate,
    cors,
    api as smorest_api,
    mail,
    login_manager
)
from app.extensions import limiter
from app.celery_worker import make_celery
from config import Config



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    cors.init_app(
        app,
        origins=app.config.get(
            "CORS_ORIGINS",
            ["http://localhost:5000"]
        )
    )

    smorest_api.init_app(app)

    limiter.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Στο create_app() μετά το login_manager.init_app(app):
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    # Celery
    celery = make_celery(app)
    app.extensions['celery'] = celery  # για πρόσβαση αλλού

    # Import tasks to register them
    from app import tasks



    # Import blueprints
    from app.api import api_bp
    from app.web import web_bp

    # Register blueprints
    app.register_blueprint(web_bp)
    smorest_api.register_blueprint(api_bp)

    @app.route("/health")
    def health():
        return {
            "status": "ok",
            "service": "TaskFlow"
        }, 200



    return app
