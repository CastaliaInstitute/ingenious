"""Helper functions and utilities for validation command.

This module contains reusable validation helpers extracted from ValidateCommand
for better organization and testability.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, List, Tuple

from ingenious.common.enums import AuthenticationMethod


@dataclass
class AuthValidationResult:
    """Result of authentication validation."""

    passed: bool = True
    message: str = ""
    missing_fields: List[str] = field(default_factory=list)


def validate_auth_credentials(model: Any) -> AuthValidationResult:
    """Validate model credentials based on authentication method.

    Args:
        model: Model configuration object with authentication settings

    Returns:
        AuthValidationResult containing validation status and details
    """
    result = AuthValidationResult()
    auth_method = model.authentication_method

    if auth_method == AuthenticationMethod.DEFAULT_CREDENTIAL:
        result.message = "default_credential authentication (no additional credentials required)"
    elif auth_method == AuthenticationMethod.MSI:
        if not model.client_id:
            result.passed = False
            result.missing_fields.append("client_id (required for MSI authentication)")
        else:
            result.message = "MSI authentication with client_id"
    elif auth_method == AuthenticationMethod.TOKEN:
        if not model.api_key:
            result.passed = False
            result.missing_fields.append("api_key (required for TOKEN authentication)")
        else:
            result.message = "token authentication with API key"
    elif auth_method == AuthenticationMethod.CLIENT_ID_AND_SECRET:
        if not model.client_id:
            result.missing_fields.append(
                "client_id (required for CLIENT_ID_AND_SECRET authentication)"
            )
        if not model.client_secret:
            result.missing_fields.append(
                "client_secret (required for CLIENT_ID_AND_SECRET authentication)"
            )
        if not model.tenant_id and not os.getenv("AZURE_TENANT_ID"):
            result.missing_fields.append(
                "tenant_id (required for CLIENT_ID_AND_SECRET authentication, can use AZURE_TENANT_ID env var)"
            )
        if result.missing_fields:
            result.passed = False
        else:
            result.message = "client_id_and_secret authentication"

    return result


def get_base_model_missing_fields(model: Any) -> List[str]:
    """Get list of missing base model fields.

    Args:
        model: Model configuration object

    Returns:
        List of missing field names
    """
    missing = []
    if not model.base_url:
        missing.append("base_url")
    if not model.model:
        missing.append("model")
    return missing


def validate_model_config(model: Any) -> Tuple[bool, str, List[str]]:
    """Validate model configuration completely.

    Args:
        model: Model configuration object

    Returns:
        Tuple of (passed, auth_message, missing_fields)
    """
    base_missing = get_base_model_missing_fields(model)
    auth_result = validate_auth_credentials(model)

    all_missing = base_missing + auth_result.missing_fields
    passed = not all_missing and auth_result.passed

    return passed, auth_result.message, all_missing


# Dependency definitions for validation
CORE_DEPENDENCIES = [
    ("pandas", "Required for sql-manipulation-agent"),
    ("fastapi", "Core web framework"),
    ("openai", "Azure OpenAI connectivity"),
    ("typer", "CLI framework"),
]

OPTIONAL_DEPENDENCIES = [
    ("chromadb", "Required for knowledge-base-agent"),
    ("azure.storage.blob", "Required for Azure Blob Storage"),
    ("pyodbc", "Required for SQL database connectivity"),
]

# Environment fix command templates
ENV_FIX_COMMANDS = {
    "models": [
        "export INGENIOUS_MODELS__0__BASE_URL=https://your-resource.openai.azure.com/",
        "export INGENIOUS_MODELS__0__API_KEY=your-api-key",
        "export INGENIOUS_MODELS__0__MODEL=gpt-4o-mini",
        "export INGENIOUS_MODELS__0__API_VERSION=2024-12-01-preview",
        "export INGENIOUS_MODELS__0__DEPLOYMENT=your-deployment-name",
    ],
    "auth_token": [
        "export INGENIOUS_MODELS__0__AUTHENTICATION_METHOD=token",
        "export INGENIOUS_MODELS__0__API_KEY=your-api-key",
    ],
    "auth_msi": [
        "export INGENIOUS_MODELS__0__AUTHENTICATION_METHOD=msi",
        "export INGENIOUS_MODELS__0__CLIENT_ID=your-managed-identity-client-id",
    ],
    "auth_client_secret": [
        "export INGENIOUS_MODELS__0__AUTHENTICATION_METHOD=client_id_and_secret",
        "export INGENIOUS_MODELS__0__CLIENT_ID=your-app-client-id",
        "export INGENIOUS_MODELS__0__CLIENT_SECRET=your-client-secret",
        "export INGENIOUS_MODELS__0__TENANT_ID=your-tenant-id",
    ],
}
