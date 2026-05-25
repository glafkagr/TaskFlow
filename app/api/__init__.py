from flask_smorest import Blueprint

api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api/v1",
    description="TaskFlow API v1",
)

# Import auth and register its blueprint INSIDE api_bp
from app.api.auth import auth_blp
api_bp.register_blueprint(auth_blp)

from app.api.projects import projects_blp
api_bp.register_blueprint(projects_blp)

from app.api.tasks import tasks_blp
api_bp.register_blueprint(tasks_blp)

from app.api.comments import comments_blp
api_bp.register_blueprint(comments_blp)

from app.api.attachments import attachments_blp
api_bp.register_blueprint(attachments_blp)

from app.api.reminders import reminders_blp
api_bp.register_blueprint(reminders_blp)

from app.api import routes
