"""SQL client factory for creating Azure SQL Database clients.

This module provides factory methods for creating Azure SQL Database connections
with appropriate authentication methods based on configuration.
"""

from typing import Optional

import pyodbc

from ingenious.common.enums import AuthenticationMethod
from ingenious.config.models import AzureSqlSettings

from .builder.sql_client import AzureSqlClientBuilder, AzureSqlClientBuilderWithAuth


class SQLClientFactory:
    """Factory class for creating Azure SQL Database clients."""

    @staticmethod
    def create_client(
        sql_config: AzureSqlSettings,
    ) -> pyodbc.Connection:
        """Create an Azure SQL client from SQL configuration.

        Args:
            sql_config: SQL configuration containing connection details

        Returns:
            pyodbc.Connection: Configured Azure SQL connection
        """
        builder = AzureSqlClientBuilder(sql_config)
        return builder.build()

    @staticmethod
    def create_client_from_params(
        database_name: str,
        connection_string: str,
        table_name: Optional[str] = None,
    ) -> pyodbc.Connection:
        """Create an Azure SQL client with direct parameters.

        Args:
            database_name: Azure SQL database name
            connection_string: Azure SQL connection string
            table_name: Default table name for operations (optional)

        Returns:
            pyodbc.Connection: Configured Azure SQL connection
        """
        sql_settings = AzureSqlSettings(
            database_name=database_name,
            table_name=table_name or "",
            database_connection_string=connection_string,
        )
        builder = AzureSqlClientBuilder(sql_settings)
        return builder.build()

    @staticmethod
    def create_client_with_auth(
        server: str,
        database: str,
        authentication_method: AuthenticationMethod = AuthenticationMethod.DEFAULT_CREDENTIAL,
        username: Optional[str] = None,
        password: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ) -> pyodbc.Connection:
        """Create an Azure SQL client with explicit authentication configuration.

        Args:
            server: SQL Server name
            database: Database name
            authentication_method: Authentication method to use
            username: Username for SQL authentication
            password: Password for SQL authentication
            client_id: Client ID for MSI or CLIENT_ID_AND_SECRET authentication
            client_secret: Client secret for CLIENT_ID_AND_SECRET authentication
            tenant_id: Tenant ID for CLIENT_ID_AND_SECRET authentication

        Returns:
            pyodbc.Connection: Configured Azure SQL connection
        """
        builder = AzureSqlClientBuilderWithAuth(
            server=server,
            database=database,
            authentication_method=authentication_method,
            username=username,
            password=password,
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id,
        )
        return builder.build()

    @staticmethod
    def create_client_with_auth_from_params(
        server: str,
        database: str,
        authentication_method: AuthenticationMethod = AuthenticationMethod.DEFAULT_CREDENTIAL,
        username: Optional[str] = None,
        password: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ) -> pyodbc.Connection:
        """Create an Azure SQL client with explicit authentication configuration from direct parameters.

        This is an alias for create_client_with_auth since it already accepts direct parameters.

        Args:
            server: SQL Server name
            database: Database name
            authentication_method: Authentication method to use
            username: Username for SQL authentication
            password: Password for SQL authentication
            client_id: Client ID for MSI or CLIENT_ID_AND_SECRET authentication
            client_secret: Client secret for CLIENT_ID_AND_SECRET authentication
            tenant_id: Tenant ID for CLIENT_ID_AND_SECRET authentication

        Returns:
            pyodbc.Connection: Configured Azure SQL connection
        """
        return SQLClientFactory.create_client_with_auth(
            server=server,
            database=database,
            authentication_method=authentication_method,
            username=username,
            password=password,
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id,
        )
