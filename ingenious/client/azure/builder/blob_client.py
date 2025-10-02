"""Azure Blob Storage client builders with multiple authentication methods.

This module provides builder classes for creating Azure Blob Storage service and blob clients
with support for connection strings, SAS tokens, and Azure AD token-based authentication.
"""

from typing import Optional, Union

from azure.storage.blob import BlobClient, BlobServiceClient

from ingenious.client.azure.builder.base import AzureClientBuilder
from ingenious.common.enums import AuthenticationMethod
from ingenious.config.auth_config import AzureAuthConfig
from ingenious.config.models import FileStorageContainerSettings
from ingenious.models.config import FileStorageContainer


class BlobServiceClientBuilder(AzureClientBuilder):
    """Builder for Azure Blob Storage service clients with multiple authentication methods.

    Attributes:
        file_storage_config: File storage configuration containing account and authentication info.
    """

    def __init__(
        self,
        file_storage_config: Union[FileStorageContainer, FileStorageContainerSettings],
    ):
        """Initialize the Blob Service client builder.

        Args:
            file_storage_config: File storage configuration object.
        """
        # Extract authentication parameters from config
        auth_config = self._create_auth_config_from_storage_config(file_storage_config)
        super().__init__(auth_config=auth_config)
        self.file_storage_config = file_storage_config

    def _create_auth_config_from_storage_config(self, file_storage_config):
        """Create AzureAuthConfig from file storage configuration.

        Args:
            file_storage_config: File storage configuration object.

        Returns:
            AzureAuthConfig instance extracted from the storage configuration.
        """
        return AzureAuthConfig.from_config(file_storage_config)

    def build(self) -> BlobServiceClient:
        """Build Azure Blob Service client based on file storage configuration.

        Returns:
            Configured Azure Blob Service client.

        Raises:
            ValueError: If account URL is required but not provided.
        """
        # Get credential based on authentication method
        if self.auth_config.authentication_method == AuthenticationMethod.TOKEN:
            # Use SAS token or connection string - need raw string value
            credential_str = self.api_key

            # Check if it's a connection string or SAS token
            if "AccountName=" in credential_str:
                # Connection string
                return BlobServiceClient.from_connection_string(credential_str)
            else:
                # SAS token
                account_url = getattr(self.file_storage_config, "url", None) or getattr(
                    self.file_storage_config, "account_url", None
                )
                if not account_url:
                    raise ValueError("Account URL is required for blob storage authentication")
                return BlobServiceClient(account_url=account_url, credential=credential_str)
        else:
            # Use Azure AD authentication - use token_credential property
            account_url = getattr(self.file_storage_config, "url", None) or getattr(
                self.file_storage_config, "account_url", None
            )
            if not account_url:
                raise ValueError("Account URL is required for blob storage authentication")
            return BlobServiceClient(account_url=account_url, credential=self.token_credential)


class BlobClientBuilder(AzureClientBuilder):
    """Builder for Azure Blob File clients.

    Attributes:
        file_storage_config: File storage configuration object.
        container_name: Name of the blob container.
        blob_name: Name of the specific blob.
    """

    def __init__(
        self,
        file_storage_config: Union[FileStorageContainer, FileStorageContainerSettings],
        container_name: Optional[str] = None,
        blob_name: Optional[str] = None,
    ):
        """Initialize the Blob client builder.

        Args:
            file_storage_config: File storage configuration object.
            container_name: Optional container name, falls back to config value.
            blob_name: Optional blob name.
        """
        # Extract authentication parameters from config
        auth_config = self._create_auth_config_from_storage_config(file_storage_config)
        super().__init__(auth_config=auth_config)
        self.file_storage_config = file_storage_config
        self.container_name = container_name or getattr(file_storage_config, "container_name", None)
        self.blob_name = blob_name

    def _create_auth_config_from_storage_config(self, file_storage_config):
        """Create AzureAuthConfig from file storage configuration.

        Args:
            file_storage_config: File storage configuration object.

        Returns:
            AzureAuthConfig instance extracted from the storage configuration.
        """
        return AzureAuthConfig.from_config(file_storage_config)

    def build(self) -> BlobClient:
        """Build Azure Blob client for specific blob.

        Returns:
            Configured Azure Blob client.

        Raises:
            ValueError: If container_name or blob_name is not provided.
        """
        # Build the service client first
        service_builder = BlobServiceClientBuilder(self.file_storage_config)
        blob_service_client = service_builder.build()

        if not self.container_name:
            raise ValueError("Container name is required for BlobClient")
        if not self.blob_name:
            raise ValueError("Blob name is required for BlobClient")

        return blob_service_client.get_blob_client(
            container=self.container_name, blob=self.blob_name
        )
