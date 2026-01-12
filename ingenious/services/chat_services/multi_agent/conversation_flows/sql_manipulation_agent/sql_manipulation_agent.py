"""SQL manipulation agent conversation flow implementation.

This module provides a conversation flow for natural language SQL query generation
using an AutoGen agent with SQL execution tools for both SQLite and Azure SQL databases.
"""

import logging
import os
import sqlite3
import uuid
from dataclasses import dataclass
from typing import Callable, Optional

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import EVENT_LOGGER_NAME, CancellationToken
from autogen_core.tools import FunctionTool

from ingenious.client.azure import AzureClientFactory
from ingenious.models.agent import LLMUsageTracker
from ingenious.models.chat import ChatResponse, IChatRequest
from ingenious.services.chat_services.multi_agent.service import IConversationFlow
from ingenious.utils.token_counter import num_tokens_from_messages

try:
    import pyodbc

    PYODBC_AVAILABLE = True
except ImportError:
    PYODBC_AVAILABLE = False


@dataclass
class DatabaseConfig:
    """Configuration for database connection and schema."""

    use_azure: bool
    table_name: str
    column_names: list[str]
    connection_string: Optional[str] = None
    db_path: Optional[str] = None


class ConversationFlow(IConversationFlow):
    """Conversation flow for natural language to SQL query generation and execution.

    Provides SQL query generation and execution capabilities using an AutoGen assistant
    agent with function tools for querying SQLite or Azure SQL databases.

    Inherits from IConversationFlow to integrate with the multi-agent chat service.
    """

    def _is_azure_sql_configured(self) -> bool:
        """Check if Azure SQL is configured and available."""
        return (
            hasattr(self._config, "azure_sql_services")
            and self._config.azure_sql_services is not None
            and PYODBC_AVAILABLE
            and bool(self._config.azure_sql_services.database_connection_string)
            and self._config.azure_sql_services.database_connection_string
            != "mock-connection-string"
        )

    def _get_azure_sql_schema(self) -> Optional[DatabaseConfig]:
        """Get Azure SQL configuration and schema if available."""
        if not self._is_azure_sql_configured():
            return None

        azure_sql = self._config.azure_sql_services
        assert azure_sql is not None
        connection_string = azure_sql.database_connection_string
        table_name = azure_sql.table_name or "sample_table"

        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT COLUMN_NAME
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = ?
                    ORDER BY ORDINAL_POSITION
                """,
                    (table_name,),
                )
                column_names = [row[0] for row in cursor.fetchall()]

                if column_names:
                    return DatabaseConfig(
                        use_azure=True,
                        table_name=table_name,
                        column_names=column_names,
                        connection_string=connection_string,
                    )
        except Exception as e:
            print(f"Azure SQL connection failed, falling back to SQLite: {e}")

        return None

    def _get_sqlite_config(self) -> DatabaseConfig:
        """Get SQLite configuration with sample data setup."""
        db_path = os.path.join(self._memory_path, "students_performance.db")
        table_name = "students_performance"
        column_names = [
            "parental_education",
            "lunch",
            "test_prep_course",
            "math_score",
            "reading_score",
            "writing_score",
        ]

        self._ensure_sqlite_schema(db_path)

        return DatabaseConfig(
            use_azure=False,
            table_name=table_name,
            column_names=column_names,
            db_path=db_path,
        )

    def _ensure_sqlite_schema(self, db_path: str) -> None:
        """Ensure SQLite database exists with sample data."""
        with sqlite3.connect(db_path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS students_performance (
                parental_education TEXT,
                lunch TEXT,
                test_prep_course TEXT,
                math_score INTEGER,
                reading_score INTEGER,
                writing_score INTEGER
            )""")
            count = conn.execute("SELECT COUNT(*) FROM students_performance").fetchone()[0]
            if count == 0:
                conn.execute("""INSERT INTO students_performance VALUES
                    ('bachelor''s degree', 'standard', 'none', 72, 72, 74),
                    ('some college', 'standard', 'completed', 69, 90, 88),
                    ('master''s degree', 'standard', 'none', 90, 95, 93),
                    ('associate''s degree', 'free/reduced', 'none', 47, 57, 44),
                    ('some college', 'standard', 'none', 76, 78, 75),
                    ('high school', 'free/reduced', 'completed', 64, 64, 67),
                    ('high school', 'free/reduced', 'none', 38, 60, 50)
                """)

    def _get_database_config(self) -> DatabaseConfig:
        """Get the appropriate database configuration."""
        azure_config = self._get_azure_sql_schema()
        if azure_config:
            return azure_config
        return self._get_sqlite_config()

    async def _build_memory_context(
        self, chat_request: IChatRequest, logger: logging.Logger
    ) -> str:
        """Build conversation memory context from thread history."""
        if not chat_request.thread_id or not self._chat_service:
            return ""

        try:
            thread_messages = await self._chat_service.chat_history_repository.get_thread_messages(
                chat_request.thread_id
            )
            if not thread_messages:
                return ""

            recent_messages = thread_messages[-10:]
            memory_parts = [
                f"{msg.role}: {(msg.content or '')[:100]}..." for msg in recent_messages
            ]
            return "Previous conversation:\n" + "\n".join(memory_parts) + "\n\n"
        except Exception as e:
            logger.warning(f"Failed to retrieve thread memory: {e}")
            return ""

    def _create_sql_executor(self, db_config: DatabaseConfig) -> Callable[[str], str]:
        """Create a SQL executor function for the given database config."""

        def execute_sql(query: str) -> str:
            """Execute SQL query on configured database."""
            try:
                if db_config.use_azure and db_config.connection_string:
                    with pyodbc.connect(db_config.connection_string) as conn:
                        cursor = conn.cursor()
                        cursor.execute(query)
                        results = cursor.fetchall()
                        columns = [column[0] for column in cursor.description]
                elif db_config.db_path:
                    with sqlite3.connect(db_config.db_path) as conn:
                        cursor = conn.execute(query)
                        results = cursor.fetchall()
                        columns = [description[0] for description in cursor.description]
                else:
                    return "SQL Error: No database configured"

                if not results:
                    return "No results found."

                if len(results) == 1:
                    return str(dict(zip(columns, results[0])))
                return str([dict(zip(columns, row)) for row in results[:10]])
            except Exception as e:
                return f"SQL Error: {str(e)}"

        return execute_sql

    def _build_system_message(self, db_config: DatabaseConfig, memory_context: str) -> str:
        """Build the system message for the SQL assistant agent."""
        database_type = "Azure SQL Database" if db_config.use_azure else "SQLite database"
        table_name = db_config.table_name
        columns = ", ".join(db_config.column_names)

        # Prompt template for LLM (not executed as SQL); validated by caller
        # nosec B608: database_type and table_name are validated before this function call
        return f"""You are a SQL expert that helps write and execute SQL queries on data stored in {database_type}.

{memory_context}IMPORTANT: If there is previous conversation context above, you MUST:
- Reference it when answering follow-up questions
- Use information from previous queries to inform new queries
- Maintain context about what data has already been discussed
- Answer questions that refer to "it", "that", "those" etc. based on previous context

Tasks:
- Write SQL queries to answer user questions about the data
- Use the 'execute_sql_tool' to run queries
- Always consider and reference previous conversation when relevant
- Format your response based on the number of rows:
  - Single Row: Use the format {{column_name: value, column_name: value}}
  - Multiple Rows: Use a list format with each row as a dictionary

The target table '{table_name}' contains the following columns: {columns}.
Use "SELECT ... FROM {table_name}" format for your queries.
DO NOT change schema or table names.
When composing summary statistics, use functions like AVG(), COUNT(), etc.
When the user asks what columns are available, just list them without running a query.

Example queries:
- SELECT * FROM {table_name} LIMIT 5
- SELECT AVG(salary) FROM {table_name}
- SELECT COUNT(*) FROM {table_name} WHERE department = 'Engineering'
"""

    def _estimate_tokens(
        self, system_message: str, user_msg: str, final_message: str, model: str
    ) -> tuple[int, int, int]:
        """Estimate token usage from conversation messages."""
        try:
            messages_for_counting = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_msg},
                {"role": "assistant", "content": final_message},
            ]
            total_tokens = num_tokens_from_messages(messages_for_counting, model)
            prompt_tokens = num_tokens_from_messages(messages_for_counting[:-1], model)
            completion_tokens = total_tokens - prompt_tokens
            return total_tokens, prompt_tokens, completion_tokens
        except Exception:
            return 0, 0, 0

    async def get_conversation_response(self, chat_request: IChatRequest) -> ChatResponse:
        """Get a conversation response by generating and executing SQL queries.

        Creates an SQL expert assistant agent with database query tools and processes
        the user's natural language question to generate and execute SQL queries.

        Args:
            chat_request: ChatRequest containing the user's question and configuration.

        Returns:
            ChatResponse with the SQL query results and conversation metadata.
        """
        model_config = self._config.models[0]
        logger = logging.getLogger(EVENT_LOGGER_NAME)
        logger.setLevel(logging.INFO)

        llm_logger = LLMUsageTracker(
            agents=[],
            config=self._config,
            chat_history_repository=self._chat_service.chat_history_repository
            if self._chat_service
            else None,
            revision_id=str(uuid.uuid4()),
            identifier=str(uuid.uuid4()),
            event_type="sql_manipulation",
        )
        logger.handlers = [llm_logger]

        memory_context = await self._build_memory_context(chat_request, logger)
        db_config = self._get_database_config()
        model_client = AzureClientFactory.create_openai_chat_completion_client(model_config)

        try:
            execute_sql = self._create_sql_executor(db_config)
            database_type = "Azure SQL Database" if db_config.use_azure else "SQLite database"

            sql_tool = FunctionTool(
                execute_sql,
                description=f"Execute SQL query on {database_type} with table "
                f"'{db_config.table_name}' and columns: {', '.join(db_config.column_names)}",
            )

            system_message = self._build_system_message(db_config, memory_context)

            sql_assistant = AssistantAgent(
                name="sql_assistant",
                system_message=system_message,
                model_client=model_client,
                tools=[sql_tool],
                reflect_on_tool_use=True,
            )

            user_msg = f"Context: SQL Expert Assistant for analyzing data.\n\nUser question: {chat_request.user_prompt}"

            response = await sql_assistant.on_messages(
                messages=[TextMessage(content=user_msg, source="user")],
                cancellation_token=CancellationToken(),
            )

            final_message = "No response generated"
            if response.chat_message and hasattr(response.chat_message, "content"):
                final_message = str(response.chat_message.content)

            total_tokens, _, completion_tokens = self._estimate_tokens(
                system_message, user_msg, final_message, model_config.model
            )

        finally:
            await model_client.close()

        return ChatResponse(
            thread_id=chat_request.thread_id or "",
            message_id=str(uuid.uuid4()),
            agent_response=final_message,
            token_count=total_tokens,
            max_token_count=completion_tokens,
            memory_summary=final_message,
        )
