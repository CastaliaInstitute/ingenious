"""Retry decorators with exponential backoff."""

from __future__ import annotations

import asyncio
import functools
import random
import time
from typing import Any, Callable, Type, TypeVar

from ingenious.core.structured_logging import get_logger
from ingenious.errors.base import IngeniousError

logger = get_logger(__name__)

# Type variables for generic decorators
F = TypeVar("F", bound=Callable[..., Any])


def retry_on_error(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    exceptions: tuple[Type[Exception], ...] = (IngeniousError,),
    only_recoverable: bool = True,
) -> Callable[[F], F]:
    """Decorator for retrying operations on error.

    Parameters
    ----------
    max_retries : int
        Maximum number of retry attempts
    base_delay : float
        Initial delay between retries
    max_delay : float
        Maximum delay between retries
    exponential_base : float
        Base for exponential backoff
    jitter : bool
        Whether to add random jitter to delays
    exceptions : tuple
        Exception types that should trigger retries
    only_recoverable : bool
        Only retry recoverable IngeniousError instances

    Examples:
    --------
    >>> @retry_on_error(max_retries=3, base_delay=1.0)
    >>> def fetch_external_data():
    ...     # This will retry up to 3 times on IngeniousError
    ...     return api_client.get_data()
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except exceptions as exc:
                    last_exception = exc

                    # Check if we should retry this exception
                    should_retry = True
                    if isinstance(exc, IngeniousError) and only_recoverable:
                        should_retry = exc.recoverable

                    # Don't retry on the last attempt or non-recoverable errors
                    if attempt >= max_retries or not should_retry:
                        if isinstance(exc, IngeniousError):
                            exc.with_context(
                                retry_count=attempt,
                                max_retries=max_retries,
                                final_attempt=True,
                            )
                        raise exc

                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (exponential_base**attempt), max_delay)

                    # Add jitter to prevent thundering herd
                    if jitter:
                        delay *= 0.5 + random.random() * 0.5  # nosec B311

                    # Log retry attempt
                    logger.warning(
                        f"Retrying {func.__name__} after error",
                        function_name=func.__name__,
                        attempt=attempt + 1,
                        max_retries=max_retries,
                        delay_seconds=delay,
                        exception_type=exc.__class__.__name__,
                        error_message=str(exc),
                    )

                    # Update context with retry information
                    if isinstance(exc, IngeniousError):
                        exc.with_context(
                            retry_count=attempt + 1,
                            max_retries=max_retries,
                            next_delay_seconds=delay,
                        )

                    time.sleep(delay)

            # This should never be reached, but just in case
            if last_exception:
                raise last_exception
            else:
                raise IngeniousError("Retry loop completed without success or exception")

        return wrapper  # type: ignore

    return decorator


def async_retry_on_error(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    exceptions: tuple[Type[Exception], ...] = (IngeniousError,),
    only_recoverable: bool = True,
) -> Callable[[F], F]:
    """Async version of retry_on_error decorator."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)

                except exceptions as exc:
                    last_exception = exc

                    should_retry = True
                    if isinstance(exc, IngeniousError) and only_recoverable:
                        should_retry = exc.recoverable

                    if attempt >= max_retries or not should_retry:
                        if isinstance(exc, IngeniousError):
                            exc.with_context(
                                retry_count=attempt,
                                max_retries=max_retries,
                                final_attempt=True,
                            )
                        raise exc

                    delay = min(base_delay * (exponential_base**attempt), max_delay)

                    if jitter:
                        delay *= 0.5 + random.random() * 0.5  # nosec B311

                    logger.warning(
                        f"Retrying async {func.__name__} after error",
                        function_name=func.__name__,
                        attempt=attempt + 1,
                        max_retries=max_retries,
                        delay_seconds=delay,
                        exception_type=exc.__class__.__name__,
                        error_message=str(exc),
                    )

                    if isinstance(exc, IngeniousError):
                        exc.with_context(
                            retry_count=attempt + 1,
                            max_retries=max_retries,
                            next_delay_seconds=delay,
                        )

                    await asyncio.sleep(delay)

            if last_exception:
                raise last_exception
            else:
                raise IngeniousError("Async retry loop completed without success or exception")

        return wrapper  # type: ignore

    return decorator
