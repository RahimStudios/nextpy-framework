"""
NextPy Configuration Manager
Plain Python settings, no Pydantic
"""

import os
from dotenv import load_dotenv

# Load the project's .env first, then fall back to a framework-local .env.
_project_env = os.path.join(os.getcwd(), ".env")
if os.path.exists(_project_env):
    load_dotenv(dotenv_path=_project_env)
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
def reload_settings(project_dir=None) -> dict:
    """Reload the project ``.env`` and refresh ``settings`` in place.

    The CLI calls this before commands that touch the database so values added
    after import (or in a different working directory) are picked up.
    """
    env_path = os.path.join(project_dir or os.getcwd(), ".env")
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path, override=True)

    settings.update(
        {
            "app_name": os.getenv("APP_NAME", settings.get("app_name", "NextPy App")),
            "debug": get_bool("DEBUG", settings.get("debug", True)),
            "secret_key": os.getenv("SECRET_KEY", settings.get("secret_key", "change-me-in-production")),
            "domain": os.getenv("DOMAIN", settings.get("domain", "localhost:5000")),
            "development": get_bool("DEVELOPMENT", settings.get("development", True)),
            "nextpy_debug": get_bool("NEXTPY_DEBUG", settings.get("nextpy_debug", True)),
            "host": os.getenv("HOST", settings.get("host", "0.0.0.0")),
            "port": int(os.getenv("PORT", str(settings.get("port", 5000)))),
            "nextpy_debug_icon": get_bool("NEXTPY_DEBUG_ICON", settings.get("nextpy_debug_icon", True)),
            "nextpy_hot_reload": get_bool("NEXTPY_HOT_RELOAD", settings.get("nextpy_hot_reload", True)),
            "nextpy_log_level": os.getenv("NEXTPY_LOG_LEVEL", settings.get("nextpy_log_level", "info")),
            "database_url": os.getenv("DATABASE_URL", settings.get("database_url", "sqlite:///./nextpy.db")),
            "db_echo": get_bool("DB_ECHO", settings.get("db_echo", False)),
            "jwt_secret": os.getenv("JWT_SECRET", settings.get("jwt_secret", "change-me")),
            "jwt_expiration_hours": int(os.getenv("JWT_EXPIRATION_HOURS", str(settings.get("jwt_expiration_hours", 24)))),
            "session_secret": os.getenv("SESSION_SECRET", settings.get("session_secret", "change-me")),
            "mail_server": os.getenv("MAIL_SERVER", settings.get("mail_server", "smtp.gmail.com")),
            "mail_port": int(os.getenv("MAIL_PORT", str(settings.get("mail_port", 587)))),
            "mail_username": os.getenv("MAIL_USERNAME", settings.get("mail_username", "")),
            "mail_password": os.getenv("MAIL_PASSWORD", settings.get("mail_password", "")),
            "api_key": os.getenv("API_KEY", settings.get("api_key")),
            "stripe_key": os.getenv("STRIPE_KEY", settings.get("stripe_key")),
            "openai_api_key": os.getenv("OPENAI_API_KEY", settings.get("openai_api_key")),
            "frontend_url": os.getenv("FRONTEND_URL", settings.get("frontend_url", "http://localhost:5000")),
            "backend_url": os.getenv("BACKEND_URL", settings.get("backend_url", "http://localhost:5000")),
        }
    )
    return settings


def get_setting(key, default=None):
    return settings.get(key, default)

def is_development():
    return settings.get("development", True)

def is_production():
    return not is_development()
