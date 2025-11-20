"""Database-agnostic SQL query builder with dialect support.

This module provides SQL query generation for multiple database backends
through a dialect pattern, supporting SQLite and Azure SQL.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Dialect(ABC):
    """Abstract base class for database-specific SQL dialects.

    Subclasses implement database-specific SQL syntax for common operations
    including table creation, UPSERT, LIMIT clauses, and data types.
    """

    @abstractmethod
    def get_create_table_if_not_exists_prefix(self) -> str:
        """Get the CREATE TABLE IF NOT EXISTS prefix for this database.

        Returns:
            Database-specific SQL prefix for conditional table creation.
        """
        pass

    @abstractmethod
    def get_limit_clause(self, limit: int) -> str:
        """Get the LIMIT clause syntax for this database.

        Args:
            limit: Maximum number of rows to return.

        Returns:
            Database-specific LIMIT clause.
        """
        pass

    @abstractmethod
    def get_upsert_query(self, table: str, columns: List[str], conflict_column: str) -> str:
        """Generate database-specific UPSERT query.

        Args:
            table: Table name for the UPSERT operation.
            columns: List of column names to insert/update.
            conflict_column: Column name to check for conflicts.

        Returns:
            Database-specific UPSERT SQL query.
        """
        pass

    @abstractmethod
    def get_temp_table_syntax(self, table_name: str, select_query: str) -> str:
        """Get temporary table creation syntax for this database.

        Args:
            table_name: Name for the temporary table.
            select_query: SELECT query to populate the temp table.

        Returns:
            Database-specific temporary table creation SQL.
        """
        pass

    @abstractmethod
    def get_drop_temp_table_syntax(self, table_name: str) -> str:
        """Get temporary table drop syntax for this database.

        Args:
            table_name: Name of the temporary table to drop.

        Returns:
            Database-specific temporary table drop SQL.
        """
        pass

    @abstractmethod
    def get_data_types(self) -> Dict[str, str]:
        """Get mapping of generic to database-specific data types.

        Returns:
            Dictionary mapping generic type names to database-specific types.
        """
        pass


class SQLiteDialect(Dialect):
    """SQLite-specific SQL dialect implementation.

    Implements SQLite syntax for table creation, UPSERT with ON CONFLICT,
    temporary tables, and data type mappings.
    """

    def get_create_table_if_not_exists_prefix(self) -> str:
        """Get SQLite's CREATE TABLE IF NOT EXISTS prefix.

        Returns:
            The string 'CREATE TABLE IF NOT EXISTS'.
        """
        return "CREATE TABLE IF NOT EXISTS"

    def get_limit_clause(self, limit: int) -> str:
        """Get SQLite's LIMIT clause.

        Args:
            limit: Maximum number of rows to return.

        Returns:
            LIMIT clause in SQLite format.
        """
        return f"LIMIT {limit}"

    def get_upsert_query(self, table: str, columns: List[str], conflict_column: str) -> str:
        """Generate SQLite UPSERT query using ON CONFLICT.

        Args:
            table: Table name for the UPSERT operation.
            columns: List of column names to insert/update.
            conflict_column: Column name to check for conflicts.

        Returns:
            SQLite UPSERT query using ON CONFLICT DO UPDATE syntax.
        """
        columns_str = ", ".join(f'"{col}"' for col in columns)
        values_str = ", ".join("?" for _ in columns)
        updates_str = ", ".join(
            f'"{col}" = EXCLUDED."{col}"' for col in columns if col != conflict_column
        )

        # nosec B608: table name validated by caller, parameters use ? placeholders
        return f"""
            INSERT INTO {table} ({columns_str})
            VALUES ({values_str})
            ON CONFLICT ("{conflict_column}") DO UPDATE
            SET {updates_str}
        """

    def get_temp_table_syntax(self, table_name: str, select_query: str) -> str:
        """Generate SQLite temporary table creation syntax.

        Args:
            table_name: Name for the temporary table.
            select_query: SELECT query to populate the temp table.

        Returns:
            SQLite CREATE TEMP TABLE AS query.
        """
        # nosec B608: table_name validated by caller, select_query constructed internally
        return f"""
            CREATE TEMP TABLE {table_name} AS
            {select_query}
        """

    def get_drop_temp_table_syntax(self, table_name: str) -> str:
        """Generate SQLite temporary table drop syntax.

        Args:
            table_name: Name of the temporary table to drop.

        Returns:
            SQLite DROP TABLE query.
        """
        # nosec B608: table_name validated by caller
        return f"DROP TABLE {table_name}"

    def get_data_types(self) -> Dict[str, str]:
        """Get SQLite data type mappings.

        Returns:
            Dictionary mapping generic types to SQLite types.
        """
        return {
            "uuid": "UUID",
            "varchar": "TEXT",
            "text": "TEXT",
            "boolean": "BOOLEAN",
            "datetime": "TEXT",
            "int": "INT",
            "json": "JSONB",
            "array": "TEXT[]",
        }


class AzureSQLDialect(Dialect):
    """Azure SQL (SQL Server) specific dialect implementation.

    Implements SQL Server syntax including MERGE for UPSERT, TOP for LIMIT,
    conditional table creation with sysobjects, and T-SQL data types.
    """

    def get_create_table_if_not_exists_prefix(self) -> str:
        """Get Azure SQL's conditional table creation prefix.

        Returns:
            SQL Server IF NOT EXISTS check using sysobjects with placeholder for table_name.
        """
        return "IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U')\nCREATE TABLE"

    def get_limit_clause(self, limit: int) -> str:
        """Get Azure SQL's TOP clause for limiting results.

        Args:
            limit: Maximum number of rows to return.

        Returns:
            TOP clause in SQL Server format.
        """
        return f"TOP {limit}"

    def get_upsert_query(self, table: str, columns: List[str], conflict_column: str) -> str:
        """Generate Azure SQL MERGE statement for UPSERT.

        Args:
            table: Table name for the UPSERT operation.
            columns: List of column names to insert/update.
            conflict_column: Column name to check for conflicts.

        Returns:
            SQL Server MERGE statement for UPSERT operation.
        """
        columns_str = ", ".join(f"[{col}]" for col in columns)
        values_str = ", ".join("?" for _ in columns)
        updates_str = ", ".join(f"[{col}] = ?" for col in columns if col != conflict_column)

        # nosec B608: table name validated by caller, parameters use ? placeholders
        return f"""
            MERGE {table} AS target
            USING (SELECT ? as {conflict_column}) AS source ON target.[{conflict_column}] = source.{conflict_column}
            WHEN MATCHED THEN
                UPDATE SET {updates_str}
            WHEN NOT MATCHED THEN
                INSERT ({columns_str})
                VALUES ({values_str})
        """

    def get_temp_table_syntax(self, table_name: str, select_query: str) -> str:
        """Generate Azure SQL temporary table creation syntax.

        Args:
            table_name: Name for the temporary table (without # prefix).
            select_query: SELECT query to populate the temp table.

        Returns:
            SQL Server SELECT INTO #temp_table syntax.
        """
        # nosec B608: table name validated by caller, select_query is constructed internally
        return f"""
            {select_query}
            INTO #{table_name}
        """

    def get_drop_temp_table_syntax(self, table_name: str) -> str:
        """Generate Azure SQL temporary table drop syntax.

        Args:
            table_name: Name of the temporary table to drop (without # prefix).

        Returns:
            SQL Server DROP TABLE #temp_table query.
        """
        # nosec B608: table_name validated by caller
        return f"DROP TABLE #{table_name}"

    def get_data_types(self) -> Dict[str, str]:
        """Get Azure SQL data type mappings.

        Returns:
            Dictionary mapping generic types to SQL Server types.
        """
        return {
            "uuid": "UNIQUEIDENTIFIER",
            "varchar": "NVARCHAR(255)",
            "text": "NVARCHAR(MAX)",
            "boolean": "BIT",
            "datetime": "DATETIME2",
            "int": "INT",
            "json": "NVARCHAR(MAX)",
            "array": "NVARCHAR(MAX)",
        }


class QueryBuilder:
    """Centralized query builder that generates database-specific SQL queries.

    Uses a dialect pattern to generate SQL queries that are compatible with
    different database backends. Supports table creation, message operations,
    user and thread management, and memory operations.

    Attributes:
        dialect: Database dialect for generating database-specific SQL.
    """

    def __init__(self, dialect: Dialect) -> None:
        """Initialize the query builder with a database dialect.

        Args:
            dialect: Database dialect to use for SQL generation.
        """
        self.dialect = dialect
        self._data_types = dialect.get_data_types()

    def _get_data_type(self, generic_type: str) -> str:
        """Get database-specific data type for a generic type.

        Args:
            generic_type: Generic data type name (e.g., 'uuid', 'varchar').

        Returns:
            Database-specific data type string.
        """
        return self._data_types.get(generic_type, generic_type)

    def create_chat_history_table(self) -> str:
        """Generate CREATE TABLE query for chat_history table.

        Returns:
            Database-specific SQL to create the chat_history table with columns
            for user_id, thread_id, message_id, feedback, timestamps, roles, and tool calls.
        """
        table_name = "chat_history"
        prefix = self.dialect.get_create_table_if_not_exists_prefix()
        if "{table_name}" in prefix:
            prefix = prefix.format(table_name=table_name)

        # nosec B608: table name 'chat_history' is hardcoded constant, parameters use ? placeholders
        return f"""
            {prefix} {table_name} (
                user_id {self._get_data_type("varchar")},
                thread_id {self._get_data_type("varchar")},
                message_id {self._get_data_type("varchar")},
                positive_feedback {self._get_data_type("boolean")},
                timestamp {self._get_data_type("datetime")},
                role {self._get_data_type("varchar")},
                content {self._get_data_type("text")},
                content_filter_results {self._get_data_type("text")},
                tool_calls {self._get_data_type("text")},
                tool_call_id {self._get_data_type("varchar")},
                tool_call_function {self._get_data_type("varchar")}
            );
        """

    def create_chat_history_summary_table(self) -> str:
        """Generate CREATE TABLE query for chat_history_summary table.

        Returns:
            Database-specific SQL to create the chat_history_summary table with
            the same schema as chat_history for storing summarized memory.
        """
        table_name = "chat_history_summary"
        prefix = self.dialect.get_create_table_if_not_exists_prefix()
        if "{table_name}" in prefix:
            prefix = prefix.format(table_name=table_name)

        # nosec B608: table name 'chat_history_summary' is hardcoded constant, parameters use ? placeholders
        return f"""
            {prefix} {table_name} (
                user_id {self._get_data_type("varchar")},
                thread_id {self._get_data_type("varchar")},
                message_id {self._get_data_type("varchar")},
                positive_feedback {self._get_data_type("boolean")},
                timestamp {self._get_data_type("datetime")},
                role {self._get_data_type("varchar")},
                content {self._get_data_type("text")},
                content_filter_results {self._get_data_type("text")},
                tool_calls {self._get_data_type("text")},
                tool_call_id {self._get_data_type("varchar")},
                tool_call_function {self._get_data_type("varchar")}
            );
        """

    def create_users_table(self) -> str:
        """Generate CREATE TABLE query for users table.

        Returns:
            Database-specific SQL to create the users table with columns for
            id (UUID), identifier, metadata (JSON), and createdAt timestamp.
        """
        table_name = "users"
        prefix = self.dialect.get_create_table_if_not_exists_prefix()
        if "{table_name}" in prefix:
            prefix = prefix.format(table_name=table_name)

        # nosec B608: table name 'users' is hardcoded constant, parameters use ? placeholders
        return f"""
            {prefix} {table_name} (
                id {self._get_data_type("uuid")} PRIMARY KEY,
                identifier {self._get_data_type("varchar")} NOT NULL UNIQUE,
                metadata {self._get_data_type("json")} NOT NULL,
                createdAt {self._get_data_type("datetime")}
            );
        """

    def create_threads_table(self) -> str:
        """Generate CREATE TABLE query for threads table.

        Returns:
            Database-specific SQL to create the threads table with foreign key
            to users table and columns for thread metadata, tags, and timestamps.
        """
        table_name = "threads"
        prefix = self.dialect.get_create_table_if_not_exists_prefix()
        if "{table_name}" in prefix:
            prefix = prefix.format(table_name=table_name)

        foreign_key = ""
        if isinstance(self.dialect, AzureSQLDialect):
            foreign_key = "FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE"
        else:
            foreign_key = 'FOREIGN KEY ("userId") REFERENCES users("id") ON DELETE CASCADE'

        # nosec B608: table name 'threads' is hardcoded constant, parameters use ? placeholders
        return f"""
            {prefix} {table_name} (
                id {self._get_data_type("uuid")} PRIMARY KEY,
                createdAt {self._get_data_type("datetime")},
                name {self._get_data_type("varchar")},
                userId {self._get_data_type("uuid")},
                userIdentifier {self._get_data_type("varchar")},
                tags {self._get_data_type("array")},
                metadata {self._get_data_type("json")},
                {foreign_key}
            );
        """

    def create_steps_table(self) -> str:
        """Generate CREATE TABLE query for steps table.

        Returns:
            Database-specific SQL to create the steps table for storing conversation
            steps with input, output, generation metadata, and timing information.
        """
        table_name = "steps"
        prefix = self.dialect.get_create_table_if_not_exists_prefix()
        if "{table_name}" in prefix:
            prefix = prefix.format(table_name=table_name)

        # Handle 'end' column name conflict in SQL Server
        end_column = "[end]" if isinstance(self.dialect, AzureSQLDialect) else "end"

        # nosec B608: table name 'steps' is hardcoded constant, parameters use ? placeholders
        return f"""
            {prefix} {table_name} (
                id {self._get_data_type("uuid")} PRIMARY KEY,
                name {self._get_data_type("varchar")} NOT NULL,
                type {self._get_data_type("varchar")} NOT NULL,
                threadId {self._get_data_type("uuid")} NOT NULL,
                parentId {self._get_data_type("uuid")},
                disableFeedback {self._get_data_type("boolean")} NOT NULL,
                streaming {self._get_data_type("boolean")} NOT NULL,
                waitForAnswer {self._get_data_type("boolean")},
                isError {self._get_data_type("boolean")},
                metadata {self._get_data_type("json")},
                tags {self._get_data_type("array")},
                input {self._get_data_type("text")},
                output {self._get_data_type("text")},
                createdAt {self._get_data_type("datetime")},
                start {self._get_data_type("datetime")},
                {end_column} {self._get_data_type("datetime")},
                generation {self._get_data_type("json")},
                showInput {self._get_data_type("varchar")},
                language {self._get_data_type("varchar")},
                indent {self._get_data_type("int")}
            );
        """

    def create_elements_table(self) -> str:
        """Generate CREATE TABLE query for elements table.

        Returns:
            Database-specific SQL to create the elements table for storing
            file attachments, images, and other elements associated with threads.
        """
        table_name = "elements"
        prefix = self.dialect.get_create_table_if_not_exists_prefix()
        if "{table_name}" in prefix:
            prefix = prefix.format(table_name=table_name)

        # nosec B608: table name 'elements' is hardcoded constant, parameters use ? placeholders
        return f"""
            {prefix} {table_name} (
                id {self._get_data_type("uuid")} PRIMARY KEY,
                threadId {self._get_data_type("uuid")},
                type {self._get_data_type("varchar")},
                url {self._get_data_type("text")},
                chainlitKey {self._get_data_type("varchar")},
                name {self._get_data_type("varchar")} NOT NULL,
                display {self._get_data_type("varchar")},
                objectKey {self._get_data_type("varchar")},
                size {self._get_data_type("varchar")},
                page {self._get_data_type("int")},
                language {self._get_data_type("varchar")},
                forId {self._get_data_type("uuid")},
                mime {self._get_data_type("varchar")}
            );
        """

    def create_feedbacks_table(self) -> str:
        """Generate CREATE TABLE query for feedbacks table.

        Returns:
            Database-specific SQL to create the feedbacks table for storing
            user feedback (value and comment) associated with steps.
        """
        table_name = "feedbacks"
        prefix = self.dialect.get_create_table_if_not_exists_prefix()
        if "{table_name}" in prefix:
            prefix = prefix.format(table_name=table_name)

        # nosec B608: table name 'feedbacks' is hardcoded constant, parameters use ? placeholders
        return f"""
            {prefix} {table_name} (
                id {self._get_data_type("uuid")} PRIMARY KEY,
                forId {self._get_data_type("uuid")} NOT NULL,
                threadId {self._get_data_type("uuid")} NOT NULL,
                value {self._get_data_type("int")} NOT NULL,
                comment {self._get_data_type("text")}
            );
        """

    def insert_message(self) -> str:
        """Generate INSERT query for adding a message to chat history.

        Returns:
            Parameterized INSERT query with 11 placeholders for message data.
        """
        return """
            INSERT INTO chat_history (
                user_id, thread_id, message_id, positive_feedback, timestamp,
                role, content, content_filter_results, tool_calls,
                tool_call_id, tool_call_function)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

    def insert_memory(self) -> str:
        """Generate INSERT query for adding a memory to chat history summary.

        Returns:
            Parameterized INSERT query with 11 placeholders for memory data.
        """
        return """
            INSERT INTO chat_history_summary (
                user_id, thread_id, message_id, positive_feedback, timestamp,
                role, content, content_filter_results, tool_calls,
                tool_call_id, tool_call_function)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

    def select_message(self) -> str:
        """Generate SELECT query for retrieving a specific message.

        Returns:
            Parameterized SELECT query with placeholders for message_id and thread_id.
        """
        return """
            SELECT user_id, thread_id, message_id, positive_feedback, timestamp, role, content,
                   content_filter_results, tool_calls, tool_call_id, tool_call_function
            FROM chat_history
            WHERE message_id = ? AND thread_id = ?
        """

    def select_latest_memory(self) -> str:
        """Generate SELECT query for retrieving the latest memory for a thread.

        Returns:
            Database-specific query to select the most recent memory by timestamp.
        """
        limit_clause = self.dialect.get_limit_clause(1)

        if isinstance(self.dialect, AzureSQLDialect):
            # nosec B608: table name 'chat_history_summary' is hardcoded constant, parameters use ? placeholders
            return f"""
                SELECT {limit_clause} user_id, thread_id, message_id, positive_feedback, timestamp, role, content,
                       content_filter_results, tool_calls, tool_call_id, tool_call_function
                FROM chat_history_summary
                WHERE thread_id = ?
                ORDER BY timestamp DESC
            """
        else:
            # nosec B608: table name 'chat_history_summary' is hardcoded constant, parameters use ? placeholders
            return f"""
                SELECT user_id, thread_id, message_id, positive_feedback, timestamp, role, content,
                       content_filter_results, tool_calls, tool_call_id, tool_call_function
                FROM chat_history_summary
                WHERE thread_id = ?
                ORDER BY timestamp DESC
                {limit_clause}
            """

    def update_message_feedback(self) -> str:
        """Generate UPDATE query for updating message feedback.

        Returns:
            Parameterized UPDATE query with placeholders for feedback, message_id, and thread_id.
        """
        return """
            UPDATE chat_history
            SET positive_feedback = ?
            WHERE message_id = ? AND thread_id = ?
        """

    def update_memory_feedback(self) -> str:
        """Generate UPDATE query for updating memory feedback.

        Returns:
            Parameterized UPDATE query with placeholders for feedback, message_id, and thread_id.
        """
        return """
            UPDATE chat_history_summary
            SET positive_feedback = ?
            WHERE message_id = ? AND thread_id = ?
        """

    def update_message_content_filter(self) -> str:
        """Generate UPDATE query for updating message content filter results.

        Returns:
            Parameterized UPDATE query with placeholders for filter results, message_id, and thread_id.
        """
        return """
            UPDATE chat_history
            SET content_filter_results = ?
            WHERE message_id = ? AND thread_id = ?
        """

    def update_memory_content_filter(self) -> str:
        """Generate UPDATE query for updating memory content filter results.

        Returns:
            Parameterized UPDATE query with placeholders for filter results, message_id, and thread_id.
        """
        return """
            UPDATE chat_history_summary
            SET content_filter_results = ?
            WHERE message_id = ? AND thread_id = ?
        """

    def insert_user(self) -> str:
        """Generate INSERT query for creating a new user.

        Returns:
            Parameterized INSERT query with placeholders for id, identifier, metadata, and createdAt.
        """
        return """
            INSERT INTO users (id, identifier, metadata, createdAt)
            VALUES (?, ?, ?, ?)
        """

    def select_user(self) -> str:
        """Generate SELECT query for retrieving a user by identifier.

        Returns:
            Parameterized SELECT query with placeholder for identifier.
        """
        return """
            SELECT id, identifier, metadata, createdAt
            FROM users
            WHERE identifier = ?
        """

    def select_thread_messages(self, limit: int = 5) -> str:
        """Generate SELECT query for retrieving recent thread messages.

        Args:
            limit: Maximum number of messages to retrieve. Defaults to 5.

        Returns:
            Database-specific query to select the most recent messages for a thread,
            ordered by timestamp ascending (oldest to newest).
        """
        if isinstance(self.dialect, AzureSQLDialect):
            # nosec B608: table name 'chat_history' is hardcoded constant, parameters use ? placeholders
            return f"""
                SELECT TOP {limit} user_id, thread_id, message_id, positive_feedback, timestamp, role, content,
                       content_filter_results, tool_calls, tool_call_id, tool_call_function
                FROM (
                    SELECT user_id, thread_id, message_id, positive_feedback, timestamp, role, content,
                           content_filter_results, tool_calls, tool_call_id, tool_call_function,
                           ROW_NUMBER() OVER (ORDER BY timestamp DESC) as rn
                    FROM chat_history
                    WHERE thread_id = ?
                ) AS ranked
                WHERE rn <= {limit}
                ORDER BY timestamp ASC
            """
        else:
            # nosec B608: table name 'chat_history' is hardcoded constant, parameters use ? placeholders
            return f"""
                SELECT *
                FROM (
                    SELECT user_id, thread_id, message_id, positive_feedback, timestamp, role, content,
                           content_filter_results, tool_calls, tool_call_id, tool_call_function
                    FROM chat_history
                    WHERE thread_id = ?
                    ORDER BY timestamp DESC
                    LIMIT {limit}
                ) AS last_five
                ORDER BY timestamp ASC
            """

    def select_thread_memory(self) -> str:
        """Generate SELECT query for retrieving thread memory.

        Returns:
            Database-specific query to select the most recent memory entry for a thread.
        """
        limit_clause = self.dialect.get_limit_clause(1)

        if isinstance(self.dialect, AzureSQLDialect):
            # nosec B608: table name 'chat_history_summary' is hardcoded constant, parameters use ? placeholders
            return f"""
                SELECT {limit_clause} user_id, thread_id, message_id, positive_feedback, timestamp, role, content,
                       content_filter_results, tool_calls, tool_call_id, tool_call_function
                FROM chat_history_summary
                WHERE thread_id = ?
                ORDER BY timestamp DESC
            """
        else:
            # nosec B608: table name 'chat_history_summary' is hardcoded constant, parameters use ? placeholders
            return f"""
                SELECT user_id, thread_id, message_id, positive_feedback, timestamp, role, content,
                       content_filter_results, tool_calls, tool_call_id, tool_call_function
                FROM chat_history_summary
                WHERE thread_id = ?
                ORDER BY timestamp DESC
                {limit_clause}
            """

    def delete_thread(self) -> str:
        """Generate DELETE query for removing all messages in a thread.

        Returns:
            Parameterized DELETE query with placeholder for thread_id.
        """
        return """
            DELETE FROM chat_history
            WHERE thread_id = ?
        """

    def delete_thread_memory(self) -> str:
        """Generate DELETE query for removing thread memory.

        Returns:
            Parameterized DELETE query with placeholder for thread_id.
        """
        return """
            DELETE FROM chat_history_summary
            WHERE thread_id = ?
        """

    def delete_user_memory(self) -> str:
        """Generate DELETE query for removing all memory for a user.

        Returns:
            Parameterized DELETE query with placeholder for user_id.
        """
        return """
            DELETE FROM chat_history_summary
            WHERE user_id = ?
        """

    def get_query(self, query_type: str, **kwargs: Any) -> str:
        """Get a query by type name with optional parameters.

        Dynamically invokes a query method by name, allowing runtime
        query selection with optional parameters.

        Args:
            query_type: Name of the query method to invoke (e.g., 'insert_message').
            **kwargs: Optional parameters to pass to the query method.

        Returns:
            The SQL query string from the matching method, or empty string if not found.
        """
        method_name = query_type
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            if callable(method):
                result = method(**kwargs)
                return str(result) if result is not None else ""
        return ""
