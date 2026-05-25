from app.api import api_bp
from app.api import auth  # Αυτό φορτώνει τα auth endpoints


@api_bp.route("/test")
def test():
    return {
        "message": "API works"
    }

