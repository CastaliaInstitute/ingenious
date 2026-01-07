"""Comprehensive tests for error handling framework.

Tests cover retry decorators, recovery strategies, circuit breaker pattern,
and error context management with full mocking of external dependencies.
"""

import asyncio
import time

import pytest

from ingenious.core.error_handling import (
    CircuitBreakerRecoveryStrategy,
    FallbackRecoveryStrategy,
    RecoveryStrategy,
    async_retry_on_error,
    retry_on_error,
)
from ingenious.core.error_handling.decorators import _RetryHandler
from ingenious.errors.base import IngeniousError


class TestRetryHandler:
    """Test the shared retry handler logic."""

    def test_should_retry_returns_true_for_recoverable_error(self):
        """Test should_retry returns True for recoverable errors."""
        handler = _RetryHandler(
            max_retries=3,
            base_delay=1.0,
            max_delay=60.0,
            exponential_base=2.0,
            jitter=False,
            exceptions=(IngeniousError,),
            only_recoverable=True,
            func_name="test_func",
        )

        error = IngeniousError("Test error", recoverable=True)
        assert handler.should_retry(error, attempt=0) is True
        assert handler.should_retry(error, attempt=1) is True
        assert handler.should_retry(error, attempt=2) is True

    def test_should_retry_returns_false_for_non_recoverable_error(self):
        """Test should_retry returns False for non-recoverable errors."""
        handler = _RetryHandler(
            max_retries=3,
            base_delay=1.0,
            max_delay=60.0,
            exponential_base=2.0,
            jitter=False,
            exceptions=(IngeniousError,),
            only_recoverable=True,
            func_name="test_func",
        )

        error = IngeniousError("Test error", recoverable=False)
        assert handler.should_retry(error, attempt=0) is False

    def test_should_retry_returns_false_on_last_attempt(self):
        """Test should_retry returns False on last attempt."""
        handler = _RetryHandler(
            max_retries=3,
            base_delay=1.0,
            max_delay=60.0,
            exponential_base=2.0,
            jitter=False,
            exceptions=(IngeniousError,),
            only_recoverable=True,
            func_name="test_func",
        )

        error = IngeniousError("Test error", recoverable=True)
        assert handler.should_retry(error, attempt=3) is False

    def test_calculate_delay_with_exponential_backoff(self):
        """Test delay calculation with exponential backoff."""
        handler = _RetryHandler(
            max_retries=5,
            base_delay=1.0,
            max_delay=60.0,
            exponential_base=2.0,
            jitter=False,
            exceptions=(IngeniousError,),
            only_recoverable=True,
            func_name="test_func",
        )

        assert handler.calculate_delay(0) == 1.0  # 1.0 * 2^0
        assert handler.calculate_delay(1) == 2.0  # 1.0 * 2^1
        assert handler.calculate_delay(2) == 4.0  # 1.0 * 2^2
        assert handler.calculate_delay(3) == 8.0  # 1.0 * 2^3

    def test_calculate_delay_respects_max_delay(self):
        """Test delay calculation respects max_delay limit."""
        handler = _RetryHandler(
            max_retries=10,
            base_delay=1.0,
            max_delay=10.0,
            exponential_base=2.0,
            jitter=False,
            exceptions=(IngeniousError,),
            only_recoverable=True,
            func_name="test_func",
        )

        # 1.0 * 2^5 = 32, but max is 10
        assert handler.calculate_delay(5) == 10.0

    def test_calculate_delay_with_jitter(self):
        """Test delay calculation includes jitter when enabled."""
        handler = _RetryHandler(
            max_retries=3,
            base_delay=1.0,
            max_delay=60.0,
            exponential_base=2.0,
            jitter=True,
            exceptions=(IngeniousError,),
            only_recoverable=True,
            func_name="test_func",
        )

        delays = [handler.calculate_delay(1) for _ in range(10)]
        # With jitter, delays should vary between 1.0 and 2.0 (0.5 to 1.0 of base*2)
        assert any(d != delays[0] for d in delays), "Jitter should cause variation"

    def test_handle_final_failure_updates_context(self):
        """Test handle_final_failure updates error context."""
        handler = _RetryHandler(
            max_retries=3,
            base_delay=1.0,
            max_delay=60.0,
            exponential_base=2.0,
            jitter=False,
            exceptions=(IngeniousError,),
            only_recoverable=True,
            func_name="test_func",
        )

        error = IngeniousError("Test error")
        handler.handle_final_failure(error, attempt=3)

        assert error.context.metadata.get("retry_count") == 3
        assert error.context.metadata.get("max_retries") == 3
        assert error.context.metadata.get("final_attempt") is True


class TestRetryOnErrorDecorator:
    """Test the synchronous retry decorator."""

    def test_successful_call_no_retry(self):
        """Test that successful calls don't trigger retries."""
        call_count = 0

        @retry_on_error(max_retries=3, exceptions=(ValueError,))
        def successful_func():
            nonlocal call_count
            call_count += 1
            return "success"

        result = successful_func()

        assert result == "success"
        assert call_count == 1

    def test_retries_on_recoverable_error(self):
        """Test that retries occur on recoverable errors."""
        call_count = 0

        @retry_on_error(max_retries=3, base_delay=0.01, exceptions=(IngeniousError,))
        def failing_then_success():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise IngeniousError("Temporary error", recoverable=True)
            return "success"

        result = failing_then_success()

        assert result == "success"
        assert call_count == 3

    def test_raises_after_max_retries(self):
        """Test that error is raised after max retries exhausted."""
        call_count = 0

        @retry_on_error(max_retries=2, base_delay=0.01, exceptions=(IngeniousError,))
        def always_fails():
            nonlocal call_count
            call_count += 1
            raise IngeniousError("Always fails", recoverable=True)

        with pytest.raises(IngeniousError, match="Always fails"):
            always_fails()

        assert call_count == 3  # Initial + 2 retries

    def test_no_retry_for_non_recoverable_error(self):
        """Test that non-recoverable errors don't trigger retries."""
        call_count = 0

        @retry_on_error(
            max_retries=3,
            base_delay=0.01,
            exceptions=(IngeniousError,),
            only_recoverable=True,
        )
        def non_recoverable_error():
            nonlocal call_count
            call_count += 1
            raise IngeniousError("Non-recoverable", recoverable=False)

        with pytest.raises(IngeniousError, match="Non-recoverable"):
            non_recoverable_error()

        assert call_count == 1  # No retries

    def test_only_catches_specified_exceptions(self):
        """Test that only specified exceptions trigger retries."""
        call_count = 0

        @retry_on_error(max_retries=3, base_delay=0.01, exceptions=(ValueError,))
        def raises_type_error():
            nonlocal call_count
            call_count += 1
            raise TypeError("Wrong type")

        with pytest.raises(TypeError, match="Wrong type"):
            raises_type_error()

        assert call_count == 1  # No retries for TypeError


class TestAsyncRetryOnErrorDecorator:
    """Test the asynchronous retry decorator."""

    @pytest.mark.asyncio
    async def test_successful_async_call_no_retry(self):
        """Test that successful async calls don't trigger retries."""
        call_count = 0

        @async_retry_on_error(max_retries=3, exceptions=(ValueError,))
        async def successful_func():
            nonlocal call_count
            call_count += 1
            return "success"

        result = await successful_func()

        assert result == "success"
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_async_retries_on_recoverable_error(self):
        """Test that async retries occur on recoverable errors."""
        call_count = 0

        @async_retry_on_error(max_retries=3, base_delay=0.01, exceptions=(IngeniousError,))
        async def failing_then_success():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise IngeniousError("Temporary error", recoverable=True)
            return "success"

        result = await failing_then_success()

        assert result == "success"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_async_raises_after_max_retries(self):
        """Test that async error is raised after max retries exhausted."""
        call_count = 0

        @async_retry_on_error(max_retries=2, base_delay=0.01, exceptions=(IngeniousError,))
        async def always_fails():
            nonlocal call_count
            call_count += 1
            raise IngeniousError("Always fails", recoverable=True)

        with pytest.raises(IngeniousError, match="Always fails"):
            await always_fails()

        assert call_count == 3  # Initial + 2 retries

    @pytest.mark.asyncio
    async def test_async_no_retry_for_non_recoverable(self):
        """Test that non-recoverable errors don't trigger async retries."""
        call_count = 0

        @async_retry_on_error(
            max_retries=3,
            base_delay=0.01,
            exceptions=(IngeniousError,),
            only_recoverable=True,
        )
        async def non_recoverable_error():
            nonlocal call_count
            call_count += 1
            raise IngeniousError("Non-recoverable", recoverable=False)

        with pytest.raises(IngeniousError, match="Non-recoverable"):
            await non_recoverable_error()

        assert call_count == 1  # No retries


class TestRecoveryStrategy:
    """Test the base RecoveryStrategy class."""

    def test_base_class_raises_not_implemented(self):
        """Test that base class methods raise NotImplementedError."""
        strategy = RecoveryStrategy()
        error = IngeniousError("Test")

        with pytest.raises(NotImplementedError):
            strategy.can_recover(error)

        with pytest.raises(NotImplementedError):
            strategy.recover(error)


class TestFallbackRecoveryStrategy:
    """Test the FallbackRecoveryStrategy class."""

    def test_can_recover_with_fallbacks(self):
        """Test can_recover returns True when fallbacks exist and error is recoverable."""

        def fallback1():
            return "fallback1"

        strategy = FallbackRecoveryStrategy([fallback1])
        error = IngeniousError("Test", recoverable=True)

        assert strategy.can_recover(error) is True

    def test_can_recover_without_fallbacks(self):
        """Test can_recover returns False when no fallbacks exist."""
        strategy = FallbackRecoveryStrategy([])
        error = IngeniousError("Test", recoverable=True)

        assert strategy.can_recover(error) is False

    def test_can_recover_non_recoverable_error(self):
        """Test can_recover returns False for non-recoverable errors."""

        def fallback1():
            return "fallback1"

        strategy = FallbackRecoveryStrategy([fallback1])
        error = IngeniousError("Test", recoverable=False)

        assert strategy.can_recover(error) is False

    def test_recover_uses_first_successful_fallback(self):
        """Test recover uses the first successful fallback."""

        def fallback1():
            return "fallback1_result"

        def fallback2():
            return "fallback2_result"

        strategy = FallbackRecoveryStrategy([fallback1, fallback2])
        error = IngeniousError("Test", recoverable=True)

        result = strategy.recover(error)

        assert result == "fallback1_result"

    def test_recover_tries_next_fallback_on_failure(self):
        """Test recover tries next fallback when first fails."""

        def fallback1():
            raise RuntimeError("Fallback 1 failed")

        def fallback2():
            return "fallback2_result"

        strategy = FallbackRecoveryStrategy([fallback1, fallback2])
        error = IngeniousError("Test", recoverable=True)

        result = strategy.recover(error)

        assert result == "fallback2_result"

    def test_recover_raises_original_error_when_all_fallbacks_fail(self):
        """Test recover raises original error when all fallbacks fail."""

        def fallback1():
            raise RuntimeError("Fallback 1 failed")

        def fallback2():
            raise RuntimeError("Fallback 2 failed")

        strategy = FallbackRecoveryStrategy([fallback1, fallback2])
        error = IngeniousError("Original error", recoverable=True)

        with pytest.raises(IngeniousError, match="Original error"):
            strategy.recover(error)

    def test_recover_passes_args_to_fallback(self):
        """Test recover passes arguments to fallback functions."""
        received_args = []

        def fallback1(*args, **kwargs):
            received_args.extend(args)
            received_args.append(kwargs)
            return "success"

        strategy = FallbackRecoveryStrategy([fallback1])
        error = IngeniousError("Test", recoverable=True)

        strategy.recover(error, "arg1", "arg2", key="value")

        assert received_args == ["arg1", "arg2", {"key": "value"}]


class TestCircuitBreakerRecoveryStrategy:
    """Test the CircuitBreakerRecoveryStrategy class."""

    def test_initial_state_is_closed(self):
        """Test circuit breaker starts in closed state."""
        strategy = CircuitBreakerRecoveryStrategy()
        assert strategy.state == "closed"
        assert strategy.failure_count == 0

    def test_can_recover_for_expected_exception(self):
        """Test can_recover returns True for expected exception type."""
        strategy = CircuitBreakerRecoveryStrategy(expected_exception=IngeniousError)
        error = IngeniousError("Test")

        assert strategy.can_recover(error) is True

    def test_can_recover_for_subclass(self):
        """Test can_recover returns True for exception subclass."""

        class CustomError(IngeniousError):
            pass

        strategy = CircuitBreakerRecoveryStrategy(expected_exception=IngeniousError)
        error = CustomError("Test")

        assert strategy.can_recover(error) is True

    def test_recover_success_in_closed_state(self):
        """Test successful recovery in closed state."""
        strategy = CircuitBreakerRecoveryStrategy()
        error = IngeniousError("Test")

        def operation():
            return "success"

        result = strategy.recover(error, operation)

        assert result == "success"
        assert strategy.state == "closed"
        assert strategy.failure_count == 0

    def test_circuit_opens_after_threshold_failures(self):
        """Test circuit opens after failure threshold reached."""
        strategy = CircuitBreakerRecoveryStrategy(
            failure_threshold=3, expected_exception=IngeniousError
        )
        error = IngeniousError("Test")

        def failing_operation():
            raise IngeniousError("Operation failed")

        # Fail up to threshold
        for i in range(3):
            with pytest.raises(IngeniousError):
                strategy.recover(error, failing_operation)

        assert strategy.state == "open"
        assert strategy.failure_count == 3

    def test_open_circuit_raises_error_immediately(self):
        """Test open circuit raises error without calling operation."""
        strategy = CircuitBreakerRecoveryStrategy(
            failure_threshold=2,
            recovery_timeout=60.0,
            expected_exception=IngeniousError,
        )
        error = IngeniousError("Test")

        # Force circuit to open
        strategy.state = "open"
        strategy.last_failure_time = time.time()

        operation_called = False

        def operation():
            nonlocal operation_called
            operation_called = True
            return "success"

        with pytest.raises(IngeniousError):
            strategy.recover(error, operation)

        assert operation_called is False

    def test_circuit_transitions_to_half_open_after_timeout(self):
        """Test circuit transitions to half-open after recovery timeout."""
        strategy = CircuitBreakerRecoveryStrategy(
            failure_threshold=2,
            recovery_timeout=0.01,
            expected_exception=IngeniousError,
        )
        error = IngeniousError("Test")

        # Force circuit to open with old failure time
        strategy.state = "open"
        strategy.last_failure_time = time.time() - 1.0  # 1 second ago

        def operation():
            return "success"

        result = strategy.recover(error, operation)

        assert result == "success"
        assert strategy.state == "closed"  # Successful recovery closes circuit

    def test_half_open_closes_on_success(self):
        """Test half-open circuit closes on successful operation."""
        strategy = CircuitBreakerRecoveryStrategy(
            failure_threshold=2, expected_exception=IngeniousError
        )
        error = IngeniousError("Test")

        strategy.state = "half-open"
        strategy.failure_count = 2

        def operation():
            return "success"

        result = strategy.recover(error, operation)

        assert result == "success"
        assert strategy.state == "closed"
        assert strategy.failure_count == 0

    def test_half_open_opens_on_failure(self):
        """Test half-open circuit opens again on failure."""
        strategy = CircuitBreakerRecoveryStrategy(
            failure_threshold=2, expected_exception=IngeniousError
        )
        error = IngeniousError("Test")

        strategy.state = "half-open"
        strategy.failure_count = 1

        def failing_operation():
            raise IngeniousError("Failed again")

        with pytest.raises(IngeniousError):
            strategy.recover(error, failing_operation)

        assert strategy.state == "open"


class TestIngeniousError:
    """Test IngeniousError class functionality."""

    def test_error_with_context(self):
        """Test creating error with context."""
        error = IngeniousError(
            "Test error",
            context={"key": "value"},
            recoverable=True,
        )

        assert str(error) == "Test error"
        assert error.context.metadata["key"] == "value"
        assert error.recoverable is True

    def test_error_with_context_method(self):
        """Test adding context with with_context method."""
        error = IngeniousError("Test error")
        error.with_context(extra_key="extra_value")

        assert error.context.metadata["extra_key"] == "extra_value"

    def test_error_chaining(self):
        """Test error cause chaining."""
        original = ValueError("Original error")
        error = IngeniousError(
            "Wrapped error",
            cause=original,
        )

        assert error.cause == original

    def test_error_code_generation(self):
        """Test error code is generated."""
        error = IngeniousError("Test error")

        assert hasattr(error, "error_code")
        assert error.error_code is not None


class TestContextManagers:
    """Test error handling context managers."""

    def test_operation_context_captures_success(self):
        """Test operation_context captures successful operations."""
        from ingenious.core.error_handling import operation_context

        with operation_context("test_op", "test") as ctx:
            ctx.add_metadata(result="success")

        # Should not raise

    def test_operation_context_captures_failure(self):
        """Test operation_context captures failed operations."""
        from ingenious.core.error_handling import operation_context
        from ingenious.errors.base_error import IngeniousError

        with pytest.raises(IngeniousError, match="Test failure"):
            with operation_context("test_op", "test"):
                raise ValueError("Test failure")

    def test_database_operation_context(self):
        """Test database_operation context manager."""
        from ingenious.core.error_handling import database_operation

        with database_operation("test_query") as ctx:
            ctx.add_metadata(rows_affected=10)

        # Should not raise

    def test_api_operation_context(self):
        """Test api_operation context manager."""
        from ingenious.core.error_handling import api_operation

        with api_operation("test_api") as ctx:
            ctx.add_metadata(status_code=200)

        # Should not raise

    def test_file_operation_context(self):
        """Test file_operation context manager."""
        from ingenious.core.error_handling import file_operation

        with file_operation("test_file", "/path/to/file") as ctx:
            ctx.add_metadata(bytes_written=100)

        # Should not raise


class TestAsyncContextManagers:
    """Test async error handling context managers."""

    @pytest.mark.asyncio
    async def test_async_operation_context_success(self):
        """Test async_operation_context captures successful async operations."""
        from ingenious.core.error_handling import async_operation_context

        async with async_operation_context("async_test", "test") as ctx:
            ctx.add_metadata(result="async_success")
            await asyncio.sleep(0.01)

        # Should not raise

    @pytest.mark.asyncio
    async def test_async_operation_context_failure(self):
        """Test async_operation_context captures failed async operations."""
        from ingenious.core.error_handling import async_operation_context
        from ingenious.errors.base_error import IngeniousError

        with pytest.raises(IngeniousError, match="Async failure"):
            async with async_operation_context("async_test", "test"):
                await asyncio.sleep(0.01)
                raise ValueError("Async failure")
