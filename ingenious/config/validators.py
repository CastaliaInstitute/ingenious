"""Configuration validation logic.

This module contains validation functions and methods
for ensuring configuration integrity.
"""

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Tuple

from ingenious.common.enums import AuthenticationMethod

from .models import ModelSettings

if TYPE_CHECKING:
    from .main_settings import IngeniousSettings


@dataclass
class LegacyEnvConfig:
    """Container for legacy environment variable values."""

    api_key: str
    base_url: str
    model: str
    deployment: str

    @classmethod
    def from_environment(cls) -> "LegacyEnvConfig":
        """Load legacy configuration from environment variables."""
        return cls(
            api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            base_url=os.getenv("AZURE_OPENAI_BASE_URL", ""),
            model=os.getenv("AZURE_OPENAI_MODEL", "gpt-4.1-nano"),
            deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-nano"),
        )


def _get_credentials_from_env(legacy: LegacyEnvConfig) -> Tuple[str, str]:
    """Get API key and base URL from environment, with legacy fallback."""
    api_key = os.getenv("INGENIOUS_MODELS__0__API_KEY", "") or legacy.api_key
    base_url = os.getenv("INGENIOUS_MODELS__0__BASE_URL", "") or legacy.base_url
    return api_key, base_url


def _determine_auth_method(api_key: str, base_url: str) -> str:
    """Determine authentication method from environment or credentials."""
    auth_method = os.getenv("INGENIOUS_MODELS__0__AUTHENTICATION_METHOD", "").lower()
    if auth_method:
        return auth_method
    if api_key:
        return "token"
    if base_url:
        return "default_credential"
    return ""


def _validate_credentials_for_auth(auth_method: str, api_key: str, base_url: str) -> None:
    """Validate credentials are sufficient for the authentication method."""
    error_msg = (
        "At least one model must be configured. "
        "Set INGENIOUS_MODELS__0__API_KEY and "
        "INGENIOUS_MODELS__0__BASE_URL environment variables "
        "or AZURE_OPENAI_API_KEY and AZURE_OPENAI_BASE_URL, "
        "or provide model configurations."
    )

    if auth_method == "token" and (not api_key or not base_url):
        raise ValueError(error_msg)
    if auth_method != "token" and not base_url:
        raise ValueError(
            "At least one model must be configured. "
            "Set INGENIOUS_MODELS__0__BASE_URL environment variable "
            "or AZURE_OPENAI_BASE_URL, "
            "or provide model configurations."
        )


def _create_default_model(
    api_key: str,
    base_url: str,
    auth_method: str,
    legacy: LegacyEnvConfig,
) -> ModelSettings:
    """Create a default ModelSettings from environment configuration."""
    try:
        auth_method_enum = AuthenticationMethod(auth_method.upper())
    except ValueError:
        auth_method_enum = AuthenticationMethod.DEFAULT_CREDENTIAL

    model_kwargs = {
        "model": legacy.model,
        "api_type": "rest",
        "api_version": "2023-03-15-preview",
        "base_url": base_url,
        "deployment": legacy.deployment,
        "authentication_method": auth_method_enum,
    }

    if api_key and auth_method_enum == AuthenticationMethod.TOKEN:
        model_kwargs["api_key"] = api_key

    return ModelSettings(**model_kwargs)


def _validate_model_credentials(
    model: ModelSettings,
    index: int,
    legacy: LegacyEnvConfig,
) -> Tuple[List[str], str, str]:
    """Validate a single model's credentials and return errors."""
    errors: List[str] = []
    model_api_key = model.api_key or legacy.api_key
    model_base_url = model.base_url or legacy.base_url
    requires_api_key = model.authentication_method == AuthenticationMethod.TOKEN

    if requires_api_key:
        if not model_api_key:
            errors.append(
                f"Model {index + 1} has no API key (required for TOKEN "
                "authentication). Set INGENIOUS_MODELS__0__API_KEY "
                "or AZURE_OPENAI_API_KEY."
            )
        elif "placeholder" in model_api_key.lower():
            errors.append(
                "API key is required for TOKEN authentication. "
                "Set the appropriate environment variable "
                "(e.g., AZURE_OPENAI_API_KEY) or provide a valid key."
            )

    if not model_base_url:
        base_url_msg = "Set INGENIOUS_MODELS__0__BASE_URL or AZURE_OPENAI_BASE_URL."
        if requires_api_key and not model_api_key:
            errors[-1] = (
                f"Model {index + 1} has no API key or base URL. "
                "Set INGENIOUS_MODELS__0__API_KEY or "
                "AZURE_OPENAI_API_KEY, and " + base_url_msg
            )
        else:
            errors.append(f"Model {index + 1} has no base URL. " + base_url_msg)
    elif "placeholder" in model_base_url.lower():
        errors.append(
            "Base URL is required. Set the appropriate environment "
            "variable (e.g., AZURE_OPENAI_BASE_URL) or provide a "
            "valid URL."
        )

    return errors, model_api_key, model_base_url


def _apply_legacy_fallbacks(model: ModelSettings, legacy: LegacyEnvConfig) -> None:
    """Update model with legacy environment variables if fields are missing."""
    if not model.api_key and legacy.api_key:
        model.api_key = legacy.api_key
    if not model.base_url and legacy.base_url:
        model.base_url = legacy.base_url
    if not model.model and legacy.model:
        model.model = legacy.model


def _create_model_from_environment(legacy: LegacyEnvConfig) -> List[ModelSettings]:
    """Create a model configuration from environment variables."""
    api_key, base_url = _get_credentials_from_env(legacy)

    if not api_key and not base_url:
        raise ValueError(
            "At least one model must be configured. "
            "Set INGENIOUS_MODELS__0__API_KEY and "
            "INGENIOUS_MODELS__0__BASE_URL environment variables "
            "or AZURE_OPENAI_API_KEY and AZURE_OPENAI_BASE_URL, "
            "or provide model configurations."
        )

    auth_method = _determine_auth_method(api_key, base_url)
    _validate_credentials_for_auth(auth_method, api_key, base_url)
    return [_create_default_model(api_key, base_url, auth_method, legacy)]


def validate_models_not_empty(
    models: List[ModelSettings],
) -> List[ModelSettings]:
    """Ensure at least one model is configured."""
    legacy = LegacyEnvConfig.from_environment()

    if not models:
        return _create_model_from_environment(legacy)

    errors: List[str] = []
    for i, model in enumerate(models):
        model_errors, _, _ = _validate_model_credentials(model, i, legacy)
        errors.extend(model_errors)
        _apply_legacy_fallbacks(model, legacy)

    if errors:
        error_msg = "At least one model must be configured. " + " ".join(errors)
        raise ValueError(error_msg)

    return models


def validate_configuration(settings: "IngeniousSettings") -> None:
    """Validate the complete configuration and provide helpful feedback."""
    errors = []

    if not settings.models:
        errors.append(
            "No models configured. Set INGENIOUS_MODELS__0__API_KEY and "
            "INGENIOUS_MODELS__0__BASE_URL."
        )

    for i, model in enumerate(settings.models):
        # Check if API key is required based on authentication method
        requires_api_key = model.authentication_method == AuthenticationMethod.TOKEN

        if requires_api_key:
            # Check for missing or None API key
            if not model.api_key:
                errors.append(
                    f"Model {i + 1} has no API key (required for TOKEN "
                    "authentication). Set INGENIOUS_MODELS__{i}__API_KEY "
                    "or AZURE_OPENAI_API_KEY."
                )
            elif "placeholder" in model.api_key.lower():
                errors.append(
                    f"Model {i + 1} has placeholder API key. "
                    "Set a valid API key in environment variables."
                )

        # Check for missing or empty base URL (always required)
        if not model.base_url:
            errors.append(
                f"Model {i + 1} has no base URL. "
                "Set INGENIOUS_MODELS__{i}__BASE_URL or "
                "AZURE_OPENAI_BASE_URL."
            )
        elif "placeholder" in model.base_url.lower():
            errors.append(
                f"Model {i + 1} has placeholder base URL. "
                "Set a valid base URL in environment variables."
            )

    if (
        settings.web_configuration.authentication.enable
        and not settings.web_configuration.authentication.password
    ):
        errors.append(
            "Web authentication is enabled but no password is set. "
            "Set WEB_AUTH_PASSWORD environment variable."
        )

    if errors:
        error_msg = "Configuration validation failed:\n" + "\n".join(
            f"- {error}" for error in errors
        )
        error_msg += "\n\nSee documentation for configuration examples."
        raise ValueError(error_msg)
