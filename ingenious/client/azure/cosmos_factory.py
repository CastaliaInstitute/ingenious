"""Cosmos DB client factory for creating Azure Cosmos DB clients.

This module provides factory methods for creating Azure Cosmos DB clients
with appropriate authentication methods based on configuration.
"""

from typing import Any

from ingenious.config.models import CosmosSettings

# Optional imports with fallbacks
try:
    from azure.cosmos import CosmosClient

    HAS_COSMOS = True
except ImportError:
    CosmosClient = None
    HAS_COSMOS = False

# Export HAS_COSMOS for backward compatibility
__all__ = ["CosmosDBClientFactory", "HAS_COSMOS"]

try:
    from .builder.cosmos_client import CosmosClientBuilder
except ImportError:
    CosmosClientBuilder = None  # type: ignore


class CosmosDBClientFactory:
    """Factory class for creating Azure Cosmos DB clients."""

    @staticmethod
    def create_client(
        cosmos_config: CosmosSettings,
    ) -> Any:
        """Create an Azure Cosmos DB client.

        Args:
            cosmos_config: Cosmos DB configuration settings

        Returns:
            CosmosClient: Configured Azure Cosmos DB client

        Raises:
            ImportError: If azure-cosmos package is not installed
        """
        if not HAS_COSMOS:
            raise ImportError(
                "azure-cosmos is required for Cosmos DB functionality. "
                "Install with: pip install azure-cosmos"
            )

        if CosmosClientBuilder is None:
            raise ImportError(
                "CosmosClientBuilder is not available. azure-cosmos package is required."
            )

        builder = CosmosClientBuilder(cosmos_config)
        return builder.build()
