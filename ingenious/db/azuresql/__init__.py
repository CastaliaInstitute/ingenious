"""Azure SQL database adapter for Ingenious chat history.

Provides repository implementation for storing chat history, threads,
messages, and metadata in Azure SQL Database using pyodbc.
"""

import json
from typing import Any, Dict, List, Optional

import pyodbc

from ingenious.config import IngeniousSettings

# Future import placeholders for advanced error handling
# from ingenious.core.error_handling import (
#     database_operation,
#     operation_context,
#     with_correlation_id,
# )
from ingenious.core.structured_logging import get_logger
from ingenious.db.base_sql import BaseSQLRepository
from ingenious.db.chat_history_models import StepDict, ThreadDict, User
from ingenious.db.query_builder import AzureSQLDialect, QueryBuilder
from ingenious.errors import (
    DatabaseQueryError,
)

logger = get_logger(__name__)


class azuresql_ChatHistoryRepository(BaseSQLRepository):
    """Azure SQL implementation of chat history repository.

    Stores chat history, threads, messages, and metadata in Azure SQL Database
    using pyodbc with MERGE operations for upsert functionality.
    """

    def __init__(self, config: IngeniousSettings) -> None:
        """Initialize Azure SQL chat history repository with connection configuration.

        Args:
            config: Ingenious settings containing Azure SQL connection configuration.

        Raises:
            ValueError: If neither azure_sql_services nor chat_history connection string is configured.
        """
        # Try to get connection string from azure_sql_services first, then fallback to chat_history
        self.connection_string = None
        if config.azure_sql_services and config.azure_sql_services.database_connection_string:
            self.connection_string = config.azure_sql_services.database_connection_string
        elif config.chat_history.database_connection_string:
            self.connection_string = config.chat_history.database_connection_string

        if not self.connection_string:
            raise ValueError(
                "Azure SQL connection string is required for azuresql chat history repository. "
                "Please set either INGENIOUS_AZURE_SQL_SERVICES__CONNECTION_STRING or "
                "INGENIOUS_CHAT_HISTORY__DATABASE_CONNECTION_STRING"
            )

        # Initialize query builder with Azure SQL dialect
        query_builder = QueryBuilder(AzureSQLDialect())

        # Call parent constructor which will call _init_connection and _create_tables
        super().__init__(config, query_builder)

    def _init_connection(self) -> None:
        """Initialize Azure SQL connection with retry logic."""
        import time

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                logger.info(
                    f"Attempting Azure SQL connection (attempt {attempt + 1}/{max_retries})"
                )
                self.connection = pyodbc.connect(self.connection_string)
                self.connection.autocommit = True
                logger.info("Azure SQL connection established successfully")
                return
            except Exception as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    logger.error("All connection attempts failed")
                    raise

    def _execute_sql(
        self, sql: str, params: list[Any] | None = None, expect_results: bool = True
    ) -> Any:
        """Execute SQL with Azure SQL connection handling."""
        if params is None:
            params = []
        cursor = None
        try:
            cursor = self.connection.cursor()

            if expect_results:
                cursor.execute(sql, params)
                rows = cursor.fetchall()
                # Convert to list of dictionaries
                columns = [column[0] for column in cursor.description]
                result = [dict(zip(columns, row)) for row in rows]
                return result
            else:
                cursor.execute(sql, params)
                self.connection.commit()

        except Exception as e:
            logger.error(
                "SQL execution failed",
                error=str(e),
                sql_query=sql[:100] + "..." if len(sql) > 100 else sql,
                param_count=len(params) if params else 0,
                operation="sql_execute",
            )
            raise DatabaseQueryError(
                "SQL query execution failed",
                context={
                    "query_preview": sql[:100] + "..." if len(sql) > 100 else sql,
                    "param_count": len(params) if params else 0,
                    "expect_results": expect_results,
                },
                cause=e,
            ) from e

        finally:
            if cursor:
                cursor.close()

    def execute_sql(
        self, sql: str, params: list[Any] | None = None, expect_results: bool = True
    ) -> Any:
        """Legacy method for backward compatibility."""
        if params is None:
            params = []
        return self._execute_sql(sql, params, expect_results)

    # Removed empty _create_tables override - using base class implementation

    async def _get_user_by_id(self, user_id: str) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT id, identifier, metadata, createdAt FROM users WHERE id = ?""",
            (user_id,),
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            return User(id=row[0], identifier=row[1], metadata=row[2], createdAt=row[3])
        return None

    async def get_threads_for_user(
        self, identifier: str, thread_id: Optional[str]
    ) -> Optional[List[ThreadDict]]:
        """Retrieve threads associated with a user identifier.

        Args:
            identifier: User identifier to query threads for.
            thread_id: Optional thread ID to filter results.

        Returns:
            List of thread dictionaries for the user, or empty list. Returns None if user not found.
        """
        # Query threads for user
        if thread_id is None:
            user_threads_query = """
                SELECT TOP 100
                    [id] AS thread_id,
                    [createdAt] AS thread_createdat,
                    [name] AS thread_name,
                    [userId] AS user_id,
                    [userIdentifier] AS user_identifier,
                    [tags] AS thread_tags,
                    [metadata] AS thread_metadata
                FROM threads
                WHERE [userIdentifier] = ?
                ORDER BY [createdAt] DESC
            """
            user_threads = self.execute_sql(user_threads_query, [identifier])
        else:
            user_threads_query = """
                SELECT TOP 100
                    [id] AS thread_id,
                    [createdAt] AS thread_createdat,
                    [name] AS thread_name,
                    [userId] AS user_id,
                    [userIdentifier] AS user_identifier,
                    [tags] AS thread_tags,
                    [metadata] AS thread_metadata
                FROM threads
                WHERE [userIdentifier] = ? AND [id] = ?
                ORDER BY [createdAt] DESC
            """
            user_threads = self.execute_sql(user_threads_query, [identifier, thread_id])

        if not isinstance(user_threads, list):
            return None
        if not user_threads:
            return []

        # Get thread IDs for subsequent queries
        thread_ids_list = [str(thread["thread_id"]) for thread in user_threads]
        thread_ids_placeholders = ",".join("?" * len(thread_ids_list))

        # Query steps and feedbacks
        steps_feedbacks_query = f"""
            SELECT
                s.[id] AS step_id,
                s.[name] AS step_name,
                s.[type] AS step_type,
                s.[threadId] AS step_threadid,
                s.[parentId] AS step_parentid,
                s.[streaming] AS step_streaming,
                s.[waitForAnswer] AS step_waitforanswer,
                s.[isError] AS step_iserror,
                s.[metadata] AS step_metadata,
                s.[tags] AS step_tags,
                s.[input] AS step_input,
                s.[output] AS step_output,
                s.[createdAt] AS step_createdat,
                s.[start] AS step_start,
                s.[end] AS step_end,
                s.[generation] AS step_generation,
                s.[showInput] AS step_showinput,
                s.[language] AS step_language,
                s.[indent] AS step_indent,
                f.[value] AS feedback_value,
                f.[comment] AS feedback_comment,
                f.[id] AS feedback_id
            FROM steps s LEFT JOIN feedbacks f ON s.[id] = f.[forId]
            WHERE s.[threadId] IN ({thread_ids_placeholders})
            ORDER BY s.[createdAt] ASC
        """
        try:
            steps_feedbacks = self.execute_sql(steps_feedbacks_query, thread_ids_list)
        except Exception as e:
            logger.warning(f"Failed to fetch steps/feedbacks: {e}")
            steps_feedbacks = []

        # Query elements
        elements_query = f"""
            SELECT
                e.[id] AS element_id,
                e.[threadId] as element_threadid,
                e.[type] AS element_type,
                e.[chainlitKey] AS element_chainlitkey,
                e.[url] AS element_url,
                e.[objectKey] as element_objectkey,
                e.[name] AS element_name,
                e.[display] AS element_display,
                e.[size] AS element_size,
                e.[language] AS element_language,
                e.[page] AS element_page,
                e.[forId] AS element_forid,
                e.[mime] AS element_mime
            FROM elements e
            WHERE e.[threadId] IN ({thread_ids_placeholders})
        """
        try:
            elements = self.execute_sql(elements_query, thread_ids_list)
        except Exception as e:
            logger.warning(f"Failed to fetch elements: {e}")
            elements = []

        # Build thread dictionaries
        thread_dicts: Dict[str, ThreadDict] = {}
        for thread in user_threads:
            tid = thread["thread_id"]
            if tid is not None:
                # Parse metadata if it's a string
                metadata = thread.get("thread_metadata")
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except (json.JSONDecodeError, TypeError):
                        metadata = {}

                thread_dicts[tid] = ThreadDict(
                    id=tid,
                    createdAt=thread["thread_createdat"],
                    name=thread["thread_name"],
                    userId=thread["user_id"],
                    userIdentifier=thread["user_identifier"],
                    tags=thread["thread_tags"],
                    metadata=metadata,
                    steps=[],
                    elements=[],
                )

        # Process steps and feedbacks
        if isinstance(steps_feedbacks, list):
            from ingenious.db.chat_history_models import FeedbackDict
            from ingenious.db.chat_history_models import StepDict as StepDictModel

            for step_feedback in steps_feedbacks:
                tid = step_feedback.get("step_threadid")
                if tid is not None and tid in thread_dicts:
                    feedback = None
                    if step_feedback.get("feedback_value") is not None:
                        feedback = FeedbackDict(
                            forId=step_feedback["step_id"],
                            id=step_feedback.get("feedback_id"),
                            value=step_feedback["feedback_value"],
                            comment=step_feedback.get("feedback_comment"),
                        )

                    # Parse metadata and generation if they're strings
                    step_metadata = step_feedback.get("step_metadata")
                    if isinstance(step_metadata, str):
                        try:
                            step_metadata = json.loads(step_metadata)
                        except (json.JSONDecodeError, TypeError):
                            step_metadata = {}

                    step_generation = step_feedback.get("step_generation")
                    if isinstance(step_generation, str):
                        try:
                            step_generation = json.loads(step_generation)
                        except (json.JSONDecodeError, TypeError):
                            step_generation = {}

                    step_dict = StepDictModel(
                        id=step_feedback["step_id"],
                        name=step_feedback["step_name"],
                        type=step_feedback["step_type"],
                        threadId=tid,
                        parentId=step_feedback.get("step_parentid"),
                        streaming=step_feedback.get("step_streaming", False),
                        waitForAnswer=step_feedback.get("step_waitforanswer"),
                        isError=step_feedback.get("step_iserror"),
                        metadata=step_metadata,
                        tags=step_feedback.get("step_tags"),
                        input=step_feedback.get("step_input"),
                        output=step_feedback.get("step_output"),
                        createdAt=step_feedback.get("step_createdat"),
                        start=step_feedback.get("step_start"),
                        end=step_feedback.get("step_end"),
                        generation=step_generation,
                        showInput=step_feedback.get("step_showinput"),
                        language=step_feedback.get("step_language"),
                        indent=step_feedback.get("step_indent"),
                        feedback=feedback,
                    )
                    thread_dicts[tid]["steps"].append(step_dict)

        # Process elements
        if isinstance(elements, list):
            from ingenious.db.chat_history_models import ElementDict

            for element in elements:
                tid = element.get("element_threadid")
                if tid is not None and tid in thread_dicts:
                    element_dict: ElementDict = {
                        "id": element["element_id"],
                        "threadId": tid,
                        "type": element.get("element_type"),
                        "chainlitKey": element.get("element_chainlitkey"),
                        "url": element.get("element_url"),
                        "objectKey": element.get("element_objectkey"),
                        "name": element.get("element_name"),
                        "display": element.get("element_display"),
                        "size": element.get("element_size"),
                        "language": element.get("element_language"),
                        "page": element.get("element_page"),
                        "forId": element.get("element_forid"),
                        "mime": element.get("element_mime"),
                        "autoPlay": element.get("element_autoplay"),
                        "playerConfig": element.get("element_playerconfig"),
                    }
                    elements_list = thread_dicts[tid].get("elements")
                    if elements_list is not None:
                        elements_list.append(element_dict)

        return list(thread_dicts.values())

    async def add_step(self, step_dict: StepDict) -> None:
        """Add a step record to the Azure SQL steps table.

        Args:
            step_dict: Dictionary containing step data including id, type, threadId, metadata, and generation fields.
        """
        logger.info(
            "Creating step in database",
            step_id=step_dict.get("id"),
            step_type=step_dict.get("type"),
            thread_id=step_dict.get("threadId"),
            operation="create_step",
        )

        # If disableFeedback is not provided, default to False
        step_dict["disableFeedback"] = step_dict.get("disableFeedback", False)

        step_dict["showInput"] = (
            str(step_dict.get("showInput", "")).lower() if "showInput" in step_dict else None
        )
        parameters = {
            key: value
            for key, value in step_dict.items()
            if value is not None and not (isinstance(value, dict) and not value)
        }
        parameters["metadata"] = json.dumps(step_dict.get("metadata", {}))
        parameters["generation"] = json.dumps(step_dict.get("generation", {}))

        columns = ", ".join(f"[{key}]" for key in parameters.keys())
        values = ", ".join("?" for key in parameters.keys())
        # nosec B608: table name 'steps' is hardcoded constant, parameters use ? placeholders
        query = f"""
            INSERT INTO steps ({columns})
            VALUES ({values});
        """
        self.execute_sql(sql=query, params=list(parameters.values()), expect_results=False)

    async def update_thread(
        self,
        thread_id: str,
        name: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, object]] = None,
        tags: Optional[List[str]] = None,
    ) -> str:
        """Update an existing thread or create a new one using MERGE (upsert) operation.

        Args:
            thread_id: Unique identifier for the thread.
            name: Optional name for the thread.
            user_id: Optional user ID to associate with the thread.
            metadata: Optional metadata dictionary to store with the thread.
            tags: Optional list of tags to categorize the thread.

        Returns:
            Empty string on successful update or insert.
        """
        logger.info(
            "Updating thread",
            thread_id=thread_id,
            user_id=user_id,
            has_name=name is not None,
            has_metadata=metadata is not None,
            operation="update_thread",
        )
        user_identifier = None
        if user_id:
            logger.debug(
                "Retrieving user identifier",
                user_id=user_id,
                operation="get_user_identifier",
            )
            user = await self._get_user_by_id(user_id)
            if user:
                user_identifier = user.identifier

        data = {
            "id": thread_id,
            "createdAt": (self.get_now() if metadata is None else None),
            "name": (
                name
                if name is not None
                else (metadata.get("name") if metadata and "name" in metadata else None)
            ),
            "userId": user_id,
            "userIdentifier": user_identifier,
            "tags": json.dumps(tags) if tags else None,
            "metadata": json.dumps(metadata) if metadata else None,
        }

        parameters = {key: value for key, value in data.items() if value is not None}

        columns = ", ".join(f"[{key}]" for key in parameters.keys())
        values = ", ".join("?" for key in parameters.keys())
        updates = ", ".join(f"[{key}] = ?" for key in parameters.keys() if key != "id")

        # Use MERGE for upsert in SQL Server
        # nosec B608: table name 'threads' is hardcoded constant, parameters use ? placeholders
        query = f"""
            MERGE threads AS target
            USING (SELECT ? as id) AS source ON target.id = source.id
            WHEN MATCHED THEN
                UPDATE SET {updates}
            WHEN NOT MATCHED THEN
                INSERT ({columns})
                VALUES ({values});
        """

        # Prepare parameters for MERGE statement
        merge_params = [thread_id] + list(parameters.values())[1:] + list(parameters.values())

        self.execute_sql(sql=query, params=merge_params, expect_results=False)

        return ""

    async def update_memory(self) -> None:
        """Update the chat history summary table to retain only the latest record per thread.

        Uses a temporary table to identify the most recent record for each thread by timestamp,
        then clears and repopulates the chat_history_summary table with only these latest records.
        """
        cursor = self.connection.cursor()

        # Create a temporary table for the latest records
        cursor.execute("""
            SELECT user_id, thread_id, message_id, positive_feedback, timestamp, role, content,
                   content_filter_results, tool_calls, tool_call_id, tool_call_function
            INTO #latest_chat_history
            FROM (
                SELECT user_id, thread_id, message_id, positive_feedback, timestamp, role, content,
                       content_filter_results, tool_calls, tool_call_id, tool_call_function,
                       ROW_NUMBER() OVER (PARTITION BY thread_id ORDER BY timestamp DESC) AS row_num
                FROM chat_history_summary
            ) AS LatestRecords
            WHERE row_num = 1
        """)

        # Clear the original table
        cursor.execute("DELETE FROM chat_history_summary")

        # Insert the latest records back into the original table
        cursor.execute("""
            INSERT INTO chat_history_summary (user_id, thread_id, message_id, positive_feedback, timestamp, role, content,
                                              content_filter_results, tool_calls, tool_call_id, tool_call_function)
            SELECT user_id, thread_id, message_id, positive_feedback, timestamp, role, content,
                   content_filter_results, tool_calls, tool_call_id, tool_call_function
            FROM #latest_chat_history
        """)

        # Drop the temporary table
        cursor.execute("DROP TABLE #latest_chat_history")
        cursor.close()
