"""Azure Search client factory for creating Azure AI Search clients.

This module provides factory methods for creating Azure AI Search clients
with appropriate authentication methods based on configuration.
"""

from typing import Any, Optional

from azure.core.credentials import AzureKeyCredential

from ingenious.common.enums import AuthenticationMethod
from ingenious.config.models import AzureSearchSettings

# Optional imports with fallbacks
try:
    from azure.search.documents import SearchClient as _SearchClient
    from azure.search.documents.aio import SearchClient as _AsyncSearchClient

    HAS_SEARCH = True
    SearchClient: Optional[type[Any]] = _SearchClient
    AsyncSearchClient: Optional[type[Any]] = _AsyncSearchClient
except ImportError:
    HAS_SEARCH = False
    SearchClient = None
    AsyncSearchClient = None

# Export HAS_SEARCH for backward compatibility
__all__ = ["SearchClientFactory", "HAS_SEARCH"]

try:
    from .builder.search_client import AzureSearchClientBuilder
except ImportError:
    AzureSearchClientBuilder = None  # type: ignore


class SearchClientFactory:
    """Factory class for creating Azure AI Search clients."""

    @staticmethod
    def create_client(search_config: AzureSearchSettings, index_name: str) -> Any:
        """Create an Azure Search client from search configuration.

        Args:
            search_config: Search configuration containing authentication details
            index_name: Name of the search index

        Returns:
            SearchClient: Configured Azure Search client

        Raises:
            ImportError: If azure-search-documents package is not installed
        """
        if not HAS_SEARCH:
            raise ImportError(
                "azure-search-documents is required for Azure Search functionality. "
                "Install with: pip install azure-search-documents"
            )

        if AzureSearchClientBuilder is None:
            raise ImportError(
                "AzureSearchClientBuilder is not available. "
                "azure-search-documents package is required."
            )

        builder = AzureSearchClientBuilder(search_config, index_name)
        return builder.build()

    @staticmethod
    def create_async_client(index_name: str, config: dict[str, Any], **client_options: Any) -> Any:
        """Create an async Azure Search client with direct parameters.

        Args:
            index_name: Name of the search index
            config: Dictionary containing 'endpoint' and 'search_key'
            **client_options: Additional client options (e.g., retry settings)

        Returns:
            SearchClient: Configured async Azure Search client from azure.search.documents.aio

        Raises:
            ImportError: If azure-search-documents package is not installed
            ValueError: If required config parameters are missing
        """
        if not HAS_SEARCH:
            raise ImportError(
                "azure-search-documents is required for Azure Search functionality. "
                "Install with: pip install azure-search-documents"
            )

        from azure.search.documents.aio import SearchClient

        endpoint = config.get("endpoint")
        search_key = config.get("search_key")

        if not endpoint or not search_key:
            raise ValueError("Both 'endpoint' and 'search_key' must be provided in config")

        credential = AzureKeyCredential(search_key)
        return SearchClient(
            endpoint=endpoint, index_name=index_name, credential=credential, **client_options
        )

    @staticmethod
    def create_client_from_params(
        endpoint: str,
        index_name: str,
        api_key: str,
        service: Optional[str] = None,
        authentication_method: AuthenticationMethod = AuthenticationMethod.DEFAULT_CREDENTIAL,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ) -> Any:
        """Create an Azure Search client with direct parameters.

        Args:
            endpoint: Azure Search service endpoint URL
            index_name: Name of the search index
            api_key: Azure Search service API key
            service: Azure Search service name (optional)
            authentication_method: Authentication method to use
            client_id: Client ID for authentication
            client_secret: Client secret for authentication
            tenant_id: Tenant ID for authentication

        Returns:
            SearchClient: Configured Azure Search client

        Raises:
            ImportError: If azure-search-documents package is not installed
        """
        if not HAS_SEARCH:
            raise ImportError(
                "azure-search-documents is required for Azure Search functionality. "
                "Install with: pip install azure-search-documents"
            )

        if AzureSearchClientBuilder is None:
            raise ImportError(
                "AzureSearchClientBuilder is not available. "
                "azure-search-documents package is required."
            )

        search_settings = AzureSearchSettings(
            service=service or "",
            endpoint=endpoint,
            key=api_key,
            client_id=client_id or "",
            client_secret=client_secret or "",
            tenant_id=tenant_id or "",
            authentication_method=authentication_method,
        )
        builder = AzureSearchClientBuilder(search_settings, index_name)
        return builder.build()
