"""Blob storage client factory for creating Azure Blob clients.

This module provides factory methods for creating Azure Blob Storage clients
with appropriate authentication methods based on configuration.
"""

from typing import Optional

from azure.storage.blob import BlobClient, BlobServiceClient

from ingenious.common.enums import AuthenticationMethod
from ingenious.config.models import FileStorageContainerSettings

from .builder.blob_client import BlobClientBuilder, BlobServiceClientBuilder


class BlobClientFactory:
    """Factory class for creating Azure Blob Storage clients."""

    @staticmethod
    def create_service_client(
        file_storage_config: FileStorageContainerSettings,
    ) -> BlobServiceClient:
        """Create an Azure Blob Service client from file storage configuration.

        Args:
            file_storage_config: File storage configuration containing authentication details

        Returns:
            BlobServiceClient: Configured Azure Blob Service client
        """
        builder = BlobServiceClientBuilder(file_storage_config)
        return builder.build()

    @staticmethod
    def create_service_client_from_params(
        account_url: str,
        authentication_method: AuthenticationMethod = AuthenticationMethod.DEFAULT_CREDENTIAL,
        token: Optional[str] = None,
        client_id: Optional[str] = None,
    ) -> BlobServiceClient:
        """Create an Azure Blob Service client with direct parameters.

        Args:
            account_url: Storage account URL
            authentication_method: Authentication method
            token: API key/SAS token/connection string for TOKEN authentication
            client_id: Client ID for MSI authentication

        Returns:
            BlobServiceClient: Configured Azure Blob Service client
        """
        file_storage_settings = FileStorageContainerSettings(
            enable=True,
            storage_type="azure",
            container_name="",  # Not required for service client
            path="./",
            add_sub_folders=True,
            url=account_url,
            client_id=client_id or "",
            token=token or "",
            authentication_method=authentication_method,
        )
        builder = BlobServiceClientBuilder(file_storage_settings)
        return builder.build()

    @staticmethod
    def create_blob_client(
        file_storage_config: FileStorageContainerSettings,
        container_name: str,
        blob_name: str,
    ) -> BlobClient:
        """Create an Azure Blob client from file storage configuration.

        Args:
            file_storage_config: File storage configuration containing authentication details
            container_name: Name of the container
            blob_name: Name of the blob

        Returns:
            BlobClient: Configured Azure Blob client
        """
        builder = BlobClientBuilder(file_storage_config, container_name, blob_name)
        return builder.build()

    @staticmethod
    def create_blob_client_from_params(
        account_url: str,
        blob_name: str,
        container_name: str,
        authentication_method: AuthenticationMethod = AuthenticationMethod.DEFAULT_CREDENTIAL,
        token: Optional[str] = None,
        client_id: Optional[str] = None,
    ) -> BlobClient:
        """Create an Azure Blob client with direct parameters.

        Args:
            account_url: Storage account URL
            blob_name: Name of the blob
            container_name: Name of the container
            authentication_method: Authentication method
            token: API key/SAS token/connection string for TOKEN authentication
            client_id: Client ID for MSI authentication

        Returns:
            BlobClient: Configured Azure Blob client
        """
        file_storage_settings = FileStorageContainerSettings(
            enable=True,
            storage_type="azure",
            container_name=container_name,
            path="./",
            add_sub_folders=True,
            url=account_url,
            client_id=client_id or "",
            token=token or "",
            authentication_method=authentication_method,
        )
        builder = BlobClientBuilder(file_storage_settings, container_name, blob_name)
        return builder.build()
