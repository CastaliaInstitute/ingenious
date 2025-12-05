"""OpenAI client factory for creating Azure OpenAI clients.

This module provides factory methods for creating Azure OpenAI clients
with appropriate authentication methods based on configuration.
"""

from typing import Any, Optional

from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from openai import AzureOpenAI

from ingenious.common.enums import AuthenticationMethod
from ingenious.config.models import ModelSettings

from .builder.openai_chat_completions_client import (
    AzureOpenAIChatCompletionClientBuilder,
)
from .builder.openai_client import AzureOpenAIClientBuilder
from .builder.openai_client_async import AsyncAzureOpenAIClientBuilder


class OpenAIClientFactory:
    """Factory class for creating Azure OpenAI clients."""

    @staticmethod
    def create_client(
        model_config: ModelSettings,
    ) -> AzureOpenAI:
        """Create an Azure OpenAI client from model configuration.

        Args:
            model_config: Model configuration containing authentication details

        Returns:
            AzureOpenAI: Configured Azure OpenAI client
        """
        builder = AzureOpenAIClientBuilder(model_config)
        return builder.build()

    @staticmethod
    def create_client_from_params(
        model: str,
        base_url: str,
        api_version: str,
        deployment: Optional[str] = None,
        api_key: Optional[str] = None,
        authentication_method: AuthenticationMethod = AuthenticationMethod.DEFAULT_CREDENTIAL,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ) -> AzureOpenAI:
        """Create an Azure OpenAI client with direct parameters.

        Args:
            model: Model name (e.g., "gpt-4", "gpt-3.5-turbo")
            base_url: Azure OpenAI endpoint URL
            api_version: Azure OpenAI API version
            deployment: Azure deployment name. If None, uses model name
            api_key: API key for authentication. Required if not using default credential
            authentication_method: Authentication method
            client_id: Client ID for MSI or CLIENT_ID_AND_SECRET authentication
            client_secret: Client secret for CLIENT_ID_AND_SECRET authentication
            tenant_id: Tenant ID for CLIENT_ID_AND_SECRET authentication

        Returns:
            AzureOpenAI: Configured Azure OpenAI client
        """
        model_settings = ModelSettings(
            model=model,
            api_type="rest",
            base_url=base_url,
            api_version=api_version,
            deployment=deployment or model,
            api_key=api_key or "",
            authentication_method=authentication_method,
            client_id=client_id or "",
            client_secret=client_secret or "",
            tenant_id=tenant_id or "",
        )
        builder = AzureOpenAIClientBuilder(model_settings)
        return builder.build()

    @staticmethod
    def create_chat_completion_client(
        model_config: ModelSettings,
    ) -> AzureOpenAIChatCompletionClient:
        """Create an Azure OpenAI Chat Completion client from model configuration.

        Args:
            model_config: Model configuration containing authentication details

        Returns:
            AzureOpenAIChatCompletionClient: Configured Azure OpenAI Chat Completion client
        """
        builder = AzureOpenAIChatCompletionClientBuilder(model_config)
        return builder.build()

    @staticmethod
    def create_chat_completion_client_from_params(
        model: str,
        base_url: str,
        api_version: str,
        deployment: Optional[str] = None,
        api_key: Optional[str] = None,
        authentication_method: AuthenticationMethod = AuthenticationMethod.DEFAULT_CREDENTIAL,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ) -> AzureOpenAIChatCompletionClient:
        """Create an Azure OpenAI Chat Completion client with direct parameters.

        Args:
            model: Model name (e.g., "gpt-4", "gpt-3.5-turbo")
            base_url: Azure OpenAI endpoint URL
            api_version: Azure OpenAI API version
            deployment: Azure deployment name. If None, uses model name
            api_key: API key for authentication. Required if not using default credential
            authentication_method: Authentication method
            client_id: Client ID for MSI or CLIENT_ID_AND_SECRET authentication
            client_secret: Client secret for CLIENT_ID_AND_SECRET authentication
            tenant_id: Tenant ID for CLIENT_ID_AND_SECRET authentication

        Returns:
            AzureOpenAIChatCompletionClient: Configured Azure OpenAI Chat Completion client
        """
        model_settings = ModelSettings(
            model=model,
            api_type="rest",
            base_url=base_url,
            api_version=api_version,
            deployment=deployment or model,
            api_key=api_key or "",
            authentication_method=authentication_method,
            client_id=client_id or "",
            client_secret=client_secret or "",
            tenant_id=tenant_id or "",
        )
        builder = AzureOpenAIChatCompletionClientBuilder(model_settings)
        return builder.build()

    @staticmethod
    def create_async_client(
        config: dict[str, Any],
        api_version: Optional[str] = None,
        **client_options: Any,
    ) -> Any:
        """Create an async Azure OpenAI client with direct parameters.

        This method is used by the Azure Search service for embedding and generation.

        Args:
            config: Dictionary containing 'openai_endpoint' and 'openai_key'
            api_version: Azure OpenAI API version
            **client_options: Additional client options (e.g., max_retries)

        Returns:
            AsyncAzureOpenAI: Configured async Azure OpenAI client
        """
        builder = AsyncAzureOpenAIClientBuilder.from_config(
            config=config,
            api_version=api_version,
            client_options=client_options,
        )
        return builder.build()
