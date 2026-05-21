class Config:
    SECRET_KEY = "dev-secret-key"

    API_TITLE = "TaskFlow API"
    API_VERSION = "v1"

    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/api/docs"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
