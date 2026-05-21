from app.api import api_bp


@api_bp.route("/test")
def test():
    return {
        "message": "API works"
    }
