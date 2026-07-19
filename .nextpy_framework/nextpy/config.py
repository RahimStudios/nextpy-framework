"""
NextPy Configuration Manager
Plain Python settings, no Pydantic
"""

import os
from dotenv import load_dotenv

# Load .env file (adjust path if your .env is two levels up)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "./.env"))

# Helper to parse booleans
def get_bool(key: str, default=False) -> bool:
    val = os.getenv(key, str(default))
    return val.lower() in ("1", "true", "yes", "on")



# Application settings
settings = {
    # App
    "app_name": os.getenv("APP_NAME", "NextPy App"),
    "debug": get_bool("DEBUG", True),
    "secret_key": os.getenv("SECRET_KEY", "change-me-in-production"),
    "domain": os.getenv("DOMAIN", "localhost:5000"),

    # Development
    "development": get_bool("DEVELOPMENT", True),
    "nextpy_debug": get_bool("NEXTPY_DEBUG", True),
    "host": os.getenv("HOST", "0.0.0.0"),
    "port": int(os.getenv("PORT", 5000)), 
    "nextpy_debug_icon": get_bool("NEXTPY_DEBUG_ICON", True),
    "nextpy_hot_reload": get_bool("NEXTPY_HOT_RELOAD", True),
    "nextpy_log_level": os.getenv("NEXTPY_LOG_LEVEL", "info"),

    # Database
    "database_url": os.getenv("DATABASE_URL", "sqlite:///./nextpy.db"),
    "db_echo": get_bool("DB_ECHO", False),

    # Auth
    "jwt_secret": os.getenv("JWT_SECRET", "change-me"),
    "jwt_algorithm": "HS256",
    "jwt_expiration_hours": int(os.getenv("JWT_EXPIRATION_HOURS", 24)),
    "session_secret": os.getenv("SESSION_SECRET", "change-me"),

    # Email
    "mail_server": os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    "mail_port": int(os.getenv("MAIL_PORT", 587)),
    "mail_username": os.getenv("MAIL_USERNAME", ""),
    "mail_password": os.getenv("MAIL_PASSWORD", ""),

    # API Keys
    "api_key": os.getenv("API_KEY"),
    "stripe_key": os.getenv("STRIPE_KEY"),
    "openai_api_key": os.getenv("OPENAI_API_KEY"),

    # URLs
    "frontend_url": os.getenv("FRONTEND_URL", "http://localhost:5000"),
    "backend_url": os.getenv("BACKEND_URL", "http://localhost:5000"),
}



# Optional helper functions
def get_setting(key, default=None):
    return settings.get(key, default)

def is_development():
    return settings.get("development", True)

def is_production():
    return not is_development()
