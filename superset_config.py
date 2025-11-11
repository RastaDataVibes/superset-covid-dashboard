import os
from dotenv import load_dotenv
load_dotenv()

# === SECURITY ===
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-change-in-prod")

# === DATABASE ===
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

# === TIMEOUTS ===
ENABLE_EXAMPLES = False
SQLLAB_TIMEOUT = 300
SUPERSET_WEBSERVER_TIMEOUT = 300
SQLLAB_ASYNC_TIME_LIMIT_SEC = 300

# === EMBEDDED DASHBOARDS (CRITICAL FOR YOUR BUTTON) ===
FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
}

# === GUEST TOKEN SUPPORT ===
GUEST_ROLE_NAME = "Public"  # You must create this role in Superset UI
GUEST_TOKEN_JWT_SECRET = os.environ.get("GUEST_TOKEN_JWT_SECRET", "change-me-in-prod")

# === CORS (Allow your frontend) ===
CORS_OPTIONS = {
    "supports_credentials": True,
    "origins": ["*"],  # Change to your domain in prod
}

# === GEVENT MONKEY PATCH (ADDED BY DOCKERFILE - DO NOT REMOVE) ===
# import gevent.monkey; gevent.monkey.patch_all()
