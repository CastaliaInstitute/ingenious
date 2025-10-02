"""Azure Cosmos DB client builder with multiple authentication methods.

This module provides a builder class for creating Azure Cosmos DB clients
with support for API key authentication and Azure AD token-based authentication.
"""

from typing import Union

from azure.cosmos import CosmosClient

from ingenious.client.azure.builder.base import AzureClientBuilder
from ingenious.common.enums import AuthenticationMethod
from ingenious.config.auth_config import AzureAuthConfig
from ingenious.config.models import CosmosSettings
from ingenious.models.config import CosmosConfig


class CosmosClientBuilder(AzureClientBuilder):
    """Builder for Azure Cosmos DB clients with multiple authentication methods.

    Attributes:
        uri: Cosmos DB account URI endpoint.
    """

    def __init__(self, cosmos_config: Union[CosmosConfig, CosmosSettings]):
        """Initialize the Cosmos DB client builder.

        Args:
            cosmos_config: Cosmos DB configuration containing URI and authentication parameters.
        """
        auth_config = self._create_auth_config_from_chat_history_config(cosmos_config)
        super().__init__(auth_config=auth_config)
        self.uri = cosmos_config.uri

    def _create_auth_config_from_chat_history_config(self, cosmos_config):
        """Create AzureAuthConfig from chat history configuration.

        Args:
            cosmos_config: Cosmos DB configuration object.

        Returns:
            AzureAuthConfig instance extracted from the Cosmos configuration.
        """
        return AzureAuthConfig.from_config(cosmos_config)

    def build(self) -> CosmosClient:
        """Build Azure Cosmos DB client based on configuration.

        Returns:
            Configured Azure Cosmos DB client.

        Raises:
            ValueError: If the credential type is invalid for the selected authentication method.
        """
        # Configure client based on credential type
        if self.auth_config.authentication_method == AuthenticationMethod.TOKEN:
            # Cosmos DB expects raw string for API key, not AzureKeyCredential
            return CosmosClient(
                url=self.uri,
                credential=self.api_key,  # Use raw string property
            )
        else:
            # Use Azure AD authentication - credential will be TokenCredential
            from azure.core.credentials import TokenCredential

            if not isinstance(self.credential, TokenCredential):
                raise ValueError(
                    f"Expected TokenCredential for Azure AD auth, got {type(self.credential)}"
                )

            return CosmosClient(url=self.uri, credential=self.credential)
