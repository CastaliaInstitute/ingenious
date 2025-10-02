"""FastAPI dependency injection without dependency-injector library.

This module provides FastAPI dependency injection functions for all major
application services including configuration, database, chat services, and
authentication.
"""

from functools import lru_cache
from typing import Any

from fastapi import Depends, Request

from ingenious.common.enums import AuthenticationMethod
from ingenious.config.main_settings import IngeniousSettings
from ingenious.core.structured_logging import get_logger
from ingenious.db.chat_history_repository import ChatHistoryRepository
from ingenious.external_services.openai_service import OpenAIService
from ingenious.files.files_repository import FileStorage
from ingenious.models.database_client import DatabaseClientType
from ingenious.services.chat_service import ChatService
from ingenious.services.message_feedback_service import MessageFeedbackService

logger = get_logger(__name__)


# Cache the config to avoid reloading
@lru_cache
def get_config() -> IngeniousSettings:
    """Get the application configuration.

    Lazily loads configuration to avoid heavy imports at module load time.
    Configuration is cached after first access.

    Returns:
        Application settings instance.
    """
    from ingenious.config.config import get_config as _get_config

    return _get_config()


def get_openai_service(
    config: IngeniousSettings = Depends(get_config),
) -> OpenAIService:
    """Get OpenAI service instance.

    Args:
        config: Application settings containing OpenAI configuration.

    Returns:
        Configured OpenAI service instance.
    """
    return OpenAIService(
        azure_endpoint=str(config.models[0].base_url),
        api_key=str(config.models[0].api_key),
        api_version=str(config.models[0].api_version),
        open_ai_model=str(config.models[0].model),
        deployment=str(config.models[0].deployment),
        authentication_method=AuthenticationMethod(config.models[0].authentication_method),
        client_id=str(config.models[0].client_id),
        client_secret=str(config.models[0].client_secret),
        tenant_id=str(config.models[0].tenant_id),
    )


def get_database_type(
    config: IngeniousSettings = Depends(get_config),
) -> DatabaseClientType:
    """Get database type from configuration.

    Args:
        config: Application settings containing database configuration.

    Returns:
        Database client type, defaults to SQLite if invalid type specified.
    """
    db_type_val = config.chat_history.database_type.lower()
    try:
        return DatabaseClientType(db_type_val)
    except ValueError:
        return DatabaseClientType.SQLITE  # Default to SQLite


def get_chat_history_repository(
    config: IngeniousSettings = Depends(get_config),
    db_type: DatabaseClientType = Depends(get_database_type),
) -> ChatHistoryRepository:
    """Get chat history repository instance.

    Args:
        config: Application settings containing database configuration.
        db_type: Database client type to use.

    Returns:
        Configured chat history repository instance.
    """
    return ChatHistoryRepository(db_type=db_type, config=config)


def get_chat_service(
    config: IngeniousSettings = Depends(get_config),
    chat_history_repository: ChatHistoryRepository = Depends(get_chat_history_repository),
    openai_service: OpenAIService = Depends(get_openai_service),
) -> ChatService:
    """Get chat service instance.

    Args:
        config: Application settings containing chat service configuration.
        chat_history_repository: Repository for storing chat history.
        openai_service: OpenAI service instance for AI operations.

    Returns:
        Configured chat service instance.
    """
    cs_type = config.chat_service.type

    # Create a wrapper that includes the openai_service
    class ConfigWrapper:
        """Wrapper to inject OpenAI service into configuration.

        Attributes:
            openai_service_instance: The OpenAI service instance.
        """

        def __init__(self, config: IngeniousSettings, openai_service: OpenAIService):
            """Initialize config wrapper.

            Args:
                config: Application settings instance.
                openai_service: OpenAI service instance to inject.
            """
            self._config = config
            self.openai_service_instance = openai_service

        def __getattr__(self, name: str) -> Any:
            """Delegate attribute access to wrapped config.

            Args:
                name: Attribute name to access.

            Returns:
                Attribute value from wrapped configuration.
            """
            return getattr(self._config, name)

    wrapped_config = ConfigWrapper(config, openai_service)

    return ChatService(
        chat_service_type=cs_type,
        chat_history_repository=chat_history_repository,
        conversation_flow="",  # Will be set per request
        config=wrapped_config,  # type: ignore
    )


def get_message_feedback_service(
    chat_history_repository: ChatHistoryRepository = Depends(get_chat_history_repository),
) -> MessageFeedbackService:
    """Get message feedback service instance.

    Args:
        chat_history_repository: Repository for accessing message data.

    Returns:
        Configured message feedback service instance.
    """
    return MessageFeedbackService(chat_history_repository=chat_history_repository)


def get_file_storage_data(
    config: IngeniousSettings = Depends(get_config),
) -> FileStorage:
    """Get file storage instance for data category.

    Args:
        config: Application settings containing storage configuration.

    Returns:
        Configured file storage instance for data files.
    """
    return FileStorage(config=config, Category="data")


def get_file_storage_revisions(
    config: IngeniousSettings = Depends(get_config),
) -> FileStorage:
    """Get file storage instance for revisions category.

    Args:
        config: Application settings containing storage configuration.

    Returns:
        Configured file storage instance for revision files.
    """
    return FileStorage(config=config, Category="revisions")


def get_conditional_security(
    request: Request, config: IngeniousSettings = Depends(get_config)
) -> str:
    """Get authenticated user from request.

    Returns 'anonymous' when authentication is disabled in configuration.

    Args:
        request: FastAPI request object containing authorization headers.
        config: Application settings instance.

    Returns:
        Username of authenticated user, or 'anonymous' if auth is disabled.

    Raises:
        HTTPException: If authentication fails or no valid credentials are provided.
    """
    # Import here to avoid circular dependency
    from ingenious.services.auth_dependencies import get_auth_user

    return get_auth_user(request, config)
