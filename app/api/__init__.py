from flask_smorest import Blueprint

api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api/v1",
    description="TaskFlow API v1",
)

from app.api import routes
