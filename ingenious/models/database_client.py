"""Database client interfaces and types."""

import enum
from typing import Any, List, Optional, Protocol


class DatabaseClientType(enum.Enum):
    """Enumeration of supported database client types.

    Attributes:
        SQLITE: SQLite database client.
        AZURESQL: Azure SQL database client.
        COSMOS: Azure Cosmos DB client.
    """

    SQLITE = "sqlite"
    AZURESQL = "azuresql"
    COSMOS = "cosmos"


class DatabaseClient(Protocol):
    """Protocol for database client implementations."""

    def connect(self) -> None:
        """Establish connection to the database."""
        ...

    def execute_query(self, query: str, params: Optional[List[Any]] = None) -> None:
        """Execute a query without expecting results.

        Args:
            query: The SQL query to execute.
            params: Optional query parameters.
        """
        ...

    def fetch_all(self, query: str, params: Optional[List[Any]] = None) -> List[Any]:
        """Execute a query and fetch all results.

        Args:
            query: The SQL query to execute.
            params: Optional query parameters.

        Returns:
            List of all result rows.
        """
        ...

    def fetch_one(self, query: str, params: Optional[List[Any]] = None) -> Optional[Any]:
        """Execute a query and fetch one result.

        Args:
            query: The SQL query to execute.
            params: Optional query parameters.

        Returns:
            Single result row or None if no results.
        """
        ...
