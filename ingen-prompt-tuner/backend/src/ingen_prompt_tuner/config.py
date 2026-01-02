"""Configuration settings for Prompt Tuner.

This module configures both the Prompt Tuner application settings and
the Ingenious framework configuration for AI agent orchestration.

Ingenious Configuration:
    The Ingenious framework uses INGENIOUS_* environment variables:
    - INGENIOUS_MODELS__0__API_KEY: Azure OpenAI API key
    - INGENIOUS_MODELS__0__BASE_URL: Azure OpenAI endpoint (Cognitive Services format)
    - INGENIOUS_MODELS__0__MODEL: Model name (e.g., gpt-4o-mini)
    - INGENIOUS_MODELS__0__DEPLOYMENT: Azure deployment name
    - INGENIOUS_MODELS__0__API_VERSION: API version
    - INGENIOUS_MODELS__0__API_TYPE: API type (rest)
    - INGENIOUS_MODELS__0__ROLE: Model role (chat)
"""

import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings for Prompt Tuner."""

    # Server
    host: str = "0.0.0.0"
    port: int = 8002

    # Authentication
    auth_enabled: bool = True
    jwt_secret: str = "prompt-tuner-dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440  # 24 hours

    # Admin user
    admin_email: str = "admin@prompttuner.local"
    admin_password: str = "admin"

    model_config = {"env_prefix": "PT_"}


def configure_ingenious_from_env() -> None:
    """Configure Ingenious framework from environment variables.

    Maps PT_* environment variables to INGENIOUS_* if Ingenious vars are not set.
    This provides backward compatibility while migrating to the Ingenious framework.
    """
    # Map PT_* variables to INGENIOUS_* format if not already set
    mappings = {
        "PT_AZURE_OPENAI_ENDPOINT": "INGENIOUS_MODELS__0__BASE_URL",
        "PT_AZURE_OPENAI_KEY": "INGENIOUS_MODELS__0__API_KEY",
        "PT_AZURE_OPENAI_DEPLOYMENT": "INGENIOUS_MODELS__0__DEPLOYMENT",
        "PT_AZURE_OPENAI_API_VERSION": "INGENIOUS_MODELS__0__API_VERSION",
    }

    for pt_var, ingen_var in mappings.items():
        if pt_var in os.environ and ingen_var not in os.environ:
            os.environ[ingen_var] = os.environ[pt_var]

    # Set defaults for Ingenious framework if not configured
    defaults = {
        "INGENIOUS_MODELS__0__MODEL": os.environ.get("PT_AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
        "INGENIOUS_MODELS__0__API_TYPE": "rest",
        "INGENIOUS_MODELS__0__ROLE": "chat",
    }

    for var, default in defaults.items():
        if var not in os.environ:
            os.environ[var] = default


# Configure Ingenious framework on module load
configure_ingenious_from_env()

settings = Settings()
