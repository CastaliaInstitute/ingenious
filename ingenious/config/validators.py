"""
Configuration validation logic.

This module contains validation functions and methods
for ensuring configuration integrity.
"""

import os
from typing import TYPE_CHECKING, List

from ingenious.common.enums import AuthenticationMethod

from .models import ModelSettings

if TYPE_CHECKING:
    from .main_settings import IngeniousSettings


def validate_models_not_empty(
    models: List[ModelSettings],
) -> List[ModelSettings]:
    """Ensure at least one model is configured."""
    # Get legacy environment variables for backward compatibility
    legacy_api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
    legacy_base_url = os.getenv("AZURE_OPENAI_BASE_URL", "")
    legacy_model = os.getenv("AZURE_OPENAI_MODEL", "gpt-4.1-nano")

    if not models:
        # Check for environment variables with INGENIOUS_ prefix
        api_key = os.getenv("INGENIOUS_MODELS__0__API_KEY", "")
        base_url = os.getenv("INGENIOUS_MODELS__0__BASE_URL", "")

        # Also check legacy environment variables for backward compatibility
        if not api_key:
            api_key = legacy_api_key
        if not base_url:
            base_url = legacy_base_url

        # If we have no credentials at all, raise an error immediately
        if not api_key and not base_url:
            raise ValueError(
                "At least one model must be configured. "
                "Set INGENIOUS_MODELS__0__API_KEY and "
                "INGENIOUS_MODELS__0__BASE_URL environment variables "
                "or AZURE_OPENAI_API_KEY and AZURE_OPENAI_BASE_URL, "
                "or provide model configurations."
            )

        # Get authentication method from environment
        auth_method = os.getenv(
            "INGENIOUS_MODELS__0__AUTHENTICATION_METHOD", ""
        ).lower()

        # If no authentication method specified, check if we have credentials
        if not auth_method:
            if api_key:
                auth_method = "token"
            elif base_url:
                auth_method = "default_credential"

        # Validate that we have the required configuration
        if auth_method == "token":
            if not api_key or not base_url:
                raise ValueError(
                    "At least one model must be configured. "
                    "Set INGENIOUS_MODELS__0__API_KEY and "
                    "INGENIOUS_MODELS__0__BASE_URL environment variables "
                    "or AZURE_OPENAI_API_KEY and AZURE_OPENAI_BASE_URL, "
                    "or provide model configurations."
                )
        else:  # default_credential, msi, client_id_and_secret
            if not base_url:
                raise ValueError(
                    "At least one model must be configured. "
                    "Set INGENIOUS_MODELS__0__BASE_URL environment variable "
                    "or AZURE_OPENAI_BASE_URL, "
                    "or provide model configurations."
                )

        # Create default model with appropriate authentication method
        try:
            auth_method_enum = AuthenticationMethod(auth_method.upper())
        except ValueError:
            auth_method_enum = AuthenticationMethod.DEFAULT_CREDENTIAL

        # Prepare model settings kwargs
        model_kwargs = {
            "model": legacy_model,
            "api_type": "rest",
            "api_version": "2023-03-15-preview",
            "base_url": base_url,
            "deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-nano"),
            "authentication_method": auth_method_enum,
        }

        # Only include API key if we have one and it's needed
        if api_key and auth_method_enum == AuthenticationMethod.TOKEN:
            model_kwargs["api_key"] = api_key

        model_settings = ModelSettings(**model_kwargs)
        return [model_settings]

    # If models exist, validate them based on authentication method
    errors = []
    for i, model in enumerate(models):
        model_api_key = model.api_key or legacy_api_key
        model_base_url = model.base_url or legacy_base_url

        missing_fields = []

        # Check if API key is required based on authentication method
        requires_api_key = model.authentication_method == AuthenticationMethod.TOKEN

        if requires_api_key:
            if not model_api_key:
                missing_fields.append("API key")
            elif "placeholder" in model_api_key.lower():
                errors.append(
                    "API key is required for TOKEN authentication. "
                    "Set the appropriate environment variable "
                    "(e.g., AZURE_OPENAI_API_KEY) or provide a valid key."
                )

        if not model_base_url:
            missing_fields.append("base URL")
        elif "placeholder" in model_base_url.lower():
            errors.append(
                "Base URL is required. Set the appropriate environment "
                "variable (e.g., AZURE_OPENAI_BASE_URL) or provide a "
                "valid URL."
            )

        if missing_fields:
            if len(missing_fields) == 1:
                if missing_fields[0] == "API key":
                    errors.append(
                        f"Model {i + 1} has no API key (required for TOKEN "
                        "authentication). Set INGENIOUS_MODELS__0__API_KEY "
                        "or AZURE_OPENAI_API_KEY."
                    )
                else:
                    errors.append(
                        f"Model {i + 1} has no base URL. "
                        "Set INGENIOUS_MODELS__0__BASE_URL or "
                        "AZURE_OPENAI_BASE_URL."
                    )
            else:
                base_url_msg = (
                    "Set INGENIOUS_MODELS__0__BASE_URL or AZURE_OPENAI_BASE_URL."
                )
                if requires_api_key:
                    errors.append(
                        f"Model {i + 1} has no API key or base URL. "
                        "Set INGENIOUS_MODELS__0__API_KEY or "
                        "AZURE_OPENAI_API_KEY, and " + base_url_msg
                    )
                else:
                    errors.append(f"Model {i + 1} has no base URL. " + base_url_msg)

        # Update the model with legacy env vars if they were missing
        if not model.api_key and legacy_api_key:
            model.api_key = legacy_api_key
        if not model.base_url and legacy_base_url:
            model.base_url = legacy_base_url
        if not model.model and legacy_model:
            model.model = legacy_model

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
