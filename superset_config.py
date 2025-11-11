import os
from dotenv import load_dotenv
load_dotenv()

# Security
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-change-in-prod")

# Database
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

# Timeouts
ENABLE_EXAMPLES = False
SQLLAB_TIMEOUT = 300
SUPERSET_WEBSERVER_TIMEOUT = 300
SQLLAB_ASYNC_TIME_LIMIT_SEC = 300

# Embedded Dashboards
FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
}

# Guest Tokens
GUEST_ROLE_NAME = "Public"
GUEST_TOKEN_JWT_SECRET = os.environ.get("GUEST_TOKEN_JWT_SECRET", "change-me-in-prod")

# CORS
CORS_OPTIONS = {
    "supports_credentials": True,
    "origins": ["*"],  # Change to your domain in production
}
