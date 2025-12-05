"""Azure Search integration for knowledge base conversation flow.

This module handles Azure AI Search operations including preflight validation,
search execution, result formatting, and error handling.
"""

from __future__ import annotations

import logging
import os
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, Awaitable, Dict, List, Optional, Protocol, Tuple, cast

from pydantic import SecretStr

from ingenious.services.retrieval.errors import PreflightError

if TYPE_CHECKING:
    from ingenious.config.config import Config

from ._helpers import diagnostics_enabled, mask_secret, unwrap_secret_or_str

# Try YAML; fall back to JSON/plaintext if PyYAML isn't installed
try:
    import yaml  # type: ignore[import-untyped]
except Exception:
    yaml = None


class _SearchConfigLike(Protocol):
    """Protocol for search configuration objects."""

    search_index_name: str
    search_endpoint: str
    search_key: SecretStr


class AzureSearchMixin:
    """Mixin class providing Azure Search functionality for ConversationFlow.

    This mixin extracts Azure Search-related methods from the main ConversationFlow
    class for better organization and maintainability.
    """

    if TYPE_CHECKING:
        _config: Config
        _kb_path: str
        _chroma_path: str

    def _azure_service(self) -> Any | None:
        """Return first azure_search_services entry or None."""
        cfg = getattr(self._config, "azure_search_services", None)
        if not cfg or len(cfg) == 0:
            return None
        return cfg[0]

    def _ensure_default_azure_index(self, logger: Optional[logging.Logger] = None) -> None:
        """Ensure an index_name is present for Azure service.

        Prefer env default, otherwise a safe fallback.
        Emits INFO when env default is used; WARNING on fallback default.
        """
        service = self._azure_service()
        if not service:
            return
        idx = getattr(service, "index_name", "")
        if idx:
            return

        env_idx = os.getenv("AZURE_SEARCH_DEFAULT_INDEX")
        if env_idx:
            setattr(service, "index_name", env_idx)
            if logger:
                logger.info(
                    "Azure Search 'index_name' not configured; using env AZURE_SEARCH_DEFAULT_INDEX=%r.",
                    env_idx,
                )
            return

        default_idx = "test-index"
        setattr(service, "index_name", default_idx)
        if logger:
            logger.warning(
                "Azure Search 'index_name' not configured; using fallback default %r. "
                "Set azure_search_services[0].index_name or AZURE_SEARCH_DEFAULT_INDEX to override.",
                default_idx,
            )

    def _should_use_azure_search(self) -> bool:
        """Return True if Azure AI Search is configured and available.

        Missing index_name is tolerated by applying a default when needed.
        """
        from ._helpers import is_azure_search_available

        service = self._azure_service()

        if not service:
            return False
        endpoint = getattr(service, "endpoint", "") or ""
        key_obj = getattr(service, "key", None) or getattr(service, "api_key", None)
        key_val = unwrap_secret_or_str(key_obj)
        has_creds = bool(endpoint and key_val and key_val != "mock-search-key-12345")

        if not has_creds:
            return False
        return is_azure_search_available()

    def _dump_kb_config_snapshot(self, logger: Optional[logging.Logger] = None) -> dict[str, Any]:
        """Build a masked snapshot of key Azure KB settings.

        When diagnostics are enabled, write it to a YAML/plaintext file and log an INFO line.
        """
        try:
            snap = self._build_snapshot_dict()
            if diagnostics_enabled():
                self._write_diagnostics_file(snap, logger)
                self._log_diagnostics(snap, logger)
        except Exception as e:
            if logger and diagnostics_enabled():
                logger.debug("Failed to build KB config snapshot: %s", e)
            snap = {}
        return snap

    def _build_snapshot_dict(self) -> Dict[str, Any]:
        """Build the snapshot dictionary from service and environment config."""
        svc = self._azure_service()
        endpoint = (getattr(svc, "endpoint", "") or "") if svc else ""
        key_obj = (getattr(svc, "key", None) or getattr(svc, "api_key", None)) if svc else None
        key_val = unwrap_secret_or_str(key_obj)
        index_name = (getattr(svc, "index_name", "") or "") if svc else ""

        env_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT", "")
        env_key = os.getenv("AZURE_SEARCH_KEY", "")
        env_index = os.getenv("AZURE_SEARCH_INDEX_NAME", "")

        return {
            "kb_service_endpoint": endpoint,
            "kb_service_index_name": index_name,
            "kb_service_key_masked": mask_secret(key_val),
            "kb_service_key_is_mock": (key_val == "mock-search-key-12345"),
            "env_AZURE_SEARCH_ENDPOINT": env_endpoint,
            "env_AZURE_SEARCH_INDEX_NAME": env_index,
            "env_AZURE_SEARCH_KEY_masked": mask_secret(env_key),
            "env_key_equals_service_key": bool(env_key and key_val and env_key == key_val),
        }

    def _write_diagnostics_file(
        self, snap: Dict[str, Any], logger: Optional[logging.Logger]
    ) -> None:
        """Write diagnostics snapshot to file."""
        try:
            filename = "Config_Values_knowldgebaseagent.yaml"
            with open(filename, "w", encoding="utf-8") as f:
                if yaml is not None:
                    yaml.safe_dump(snap, f, sort_keys=False)
                else:
                    for k, v in snap.items():
                        f.write(f"{k}: {v}\n")
        except Exception as write_err:
            if logger:
                logger.debug("Diagnostics write failed: %s", write_err)

    def _log_diagnostics(self, snap: Dict[str, Any], logger: Optional[logging.Logger]) -> None:
        """Log diagnostics information."""
        if logger:
            logger.info(
                "[KB Azure Config] endpoint=%s index=%s key=%s env_key=%s mock_key=%s",
                snap.get("kb_service_endpoint", ""),
                snap.get("kb_service_index_name", ""),
                snap.get("kb_service_key_masked", ""),
                snap.get("env_AZURE_SEARCH_KEY_masked", ""),
                snap.get("kb_service_key_is_mock", False),
            )

    def _require_valid_azure_index(
        self, logger: Optional[logging.Logger] = None
    ) -> Awaitable[None]:
        """Public entry point for Azure index validation.

        - Performs **synchronous** configuration validation immediately
        - Returns an **awaitable** coroutine for async network preflight
        """
        endpoint, index_name, key_val = self._validate_azure_index_config(logger)
        return self._preflight_azure_index_async(endpoint, index_name, key_val, logger)

    def _validate_azure_index_config(
        self, logger: Optional[logging.Logger] = None
    ) -> Tuple[str, str, str]:
        """Synchronous, fail-fast validation of Azure KB config.

        Returns:
            (endpoint, index_name, key_val) if validation passes.

        Raises:
            PreflightError for configuration issues.
        """
        snap = self._dump_kb_config_snapshot(logger)

        service = self._azure_service()
        if not service:
            raise PreflightError(
                provider="azure_search",
                reason="not_configured",
                detail="Azure Search service missing (azure_search_services[0]).",
                snapshot=snap,
            )

        self._ensure_default_azure_index(logger)

        endpoint = (getattr(service, "endpoint", "") or "").strip()
        index_name = (getattr(service, "index_name", "") or "").strip()
        key_obj = getattr(service, "key", None) or getattr(service, "api_key", None)
        key_val = unwrap_secret_or_str(key_obj)

        if not endpoint or not key_val or not index_name:
            snap = self._dump_kb_config_snapshot(logger)
            raise PreflightError(
                provider="azure_search",
                reason="incomplete_config",
                detail=(
                    f"endpoint_present={bool(endpoint)}, key_present={bool(key_val)}, "
                    f"index_name_present={bool(index_name)}"
                ),
                snapshot=snap,
            )

        return endpoint, index_name, key_val

    async def _preflight_azure_index_async(
        self,
        endpoint: str,
        index_name: str,
        key_val: str,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """Asynchronous network preflight: imports SDK and verifies connectivity."""
        from ingenious.services.azure_search.client_init import make_async_search_client

        try:
            from azure.search.documents.aio import (
                SearchClient as _SDKCheck,
            )

            _ = _SDKCheck
        except ImportError as e:
            raise PreflightError(
                provider="azure_search",
                reason="sdk_missing",
                detail=str(e),
                snapshot=self._dump_kb_config_snapshot(logger),
            )

        client = None
        try:
            cfg_stub: _SearchConfigLike = SimpleNamespace(
                search_index_name=index_name,
                search_endpoint=endpoint,
                search_key=SecretStr(key_val),
            )
            client = make_async_search_client(cfg_stub)
        except ImportError as e:
            raise PreflightError(
                provider="azure_search",
                reason="sdk_missing",
                detail=str(e),
                snapshot=self._dump_kb_config_snapshot(logger),
            )
        except Exception as e:
            raise PreflightError(
                provider="azure_search",
                reason="preflight_failed",
                detail=str(e),
                snapshot=self._dump_kb_config_snapshot(logger),
            )
        try:
            await client.get_document_count()
        except PreflightError:
            raise
        except Exception as e:
            raise PreflightError(
                provider="azure_search",
                reason="preflight_failed",
                detail=str(e),
                snapshot=self._dump_kb_config_snapshot(logger),
            )
        finally:
            try:
                if client:
                    await client.close()
            except Exception:
                pass  # nosec B110 - intentionally ignoring cleanup errors

    async def _try_azure_search(
        self,
        search_query: str,
        top_k: int,
        policy: str,
        logger: Optional[logging.Logger],
    ) -> Optional[str]:
        """Attempt Azure search with error handling and fallback logic."""
        last_err: Optional[Exception] = None
        provider: Any = None

        try:
            self._dump_kb_config_snapshot(logger)
            await self._require_valid_azure_index(logger)

            from ingenious.services.azure_search.provider import AzureSearchProvider

            provider = AzureSearchProvider(self._config)

            azure_result = await self._execute_azure_search_with_provider(
                provider, search_query, top_k
            )

            if self._should_fallback_from_azure(policy, azure_result):
                if logger:
                    logger.warning(
                        "Azure returned no results; falling back to ChromaDB (KB_FALLBACK_ON_EMPTY=1)."
                    )
                self._ensure_kb_directory()
                return await self._search_local_chroma(search_query, top_k, logger)

            return azure_result

        except ImportError as e:
            last_err = e
            self._handle_azure_import_error(e, policy, logger)
        except PreflightError as e:
            last_err = e
            self._handle_azure_preflight_error(e, policy, logger)
        except Exception as e:
            last_err = e
            self._handle_azure_general_error(e, policy, logger)
        finally:
            await self._close_azure_provider(provider)

        self._last_azure_error = last_err  # type: ignore
        return None

    async def _execute_azure_search_with_provider(
        self,
        provider: Any,
        search_query: str,
        top_k: int,
    ) -> str:
        """Execute Azure search using provided provider and format results."""
        chunks: List[Dict[str, Any]] = await provider.retrieve(search_query, top_k=top_k)

        if not chunks:
            return f"No relevant information found in Azure AI Search for query: {search_query}"

        return self._format_azure_results(chunks)

    def _format_azure_results(self, chunks: List[Dict[str, Any]]) -> str:
        """Format Azure search results into readable string."""
        parts: List[str] = []
        cap = self._azure_snippet_cap()

        for i, c in enumerate(chunks, 1):
            formatted_chunk = self._format_single_chunk(i, c, cap)
            parts.append(formatted_chunk)

        return "Found relevant information from Azure AI Search:\n\n" + "\n\n---\n\n".join(parts)

    def _format_single_chunk(self, index: int, chunk: Dict[str, Any], cap: int) -> str:
        """Format a single search result chunk."""
        title = chunk.get("title", chunk.get("id", f"Source {index}"))
        score = chunk.get("_final_score", "")
        snippet = chunk.get("snippet", "") or ""
        content = chunk.get("content", "") or ""

        if cap > 0:
            snippet = cast(str, snippet)[:cap]
            content = cast(str, content)[:cap]

        lines: list[str] = []
        if snippet:
            lines.append(cast(str, snippet))
        if content and content != snippet:
            lines.append(cast(str, content))
        body = "\n".join(lines) if lines else ""

        return f"[{index}] {title} (score={score})\n{body}"

    def _should_fallback_from_azure(self, policy: str, azure_result: str) -> bool:
        """Check if we should fallback from Azure to local based on policy and result."""
        return (
            policy == "prefer_azure"
            and self._fallback_on_empty()
            and azure_result.startswith("No relevant information")
        )

    def _handle_azure_import_error(
        self,
        error: ImportError,
        policy: str,
        logger: Optional[logging.Logger],
    ) -> None:
        """Handle Azure import errors based on policy."""
        if policy == "azure_only":
            raise PreflightError(
                provider="azure_search",
                reason="sdk_missing",
                detail="Azure Search SDK/provider not available; retrieval is disabled by policy.",
                snapshot=self._dump_kb_config_snapshot(logger),
            )
        if logger:
            logger.warning("Azure SDK/provider not available; falling back to ChromaDB.")

    def _handle_azure_preflight_error(
        self,
        error: PreflightError,
        policy: str,
        logger: Optional[logging.Logger],
    ) -> None:
        """Handle Azure preflight errors based on policy."""
        if policy == "azure_only":
            raise error
        if logger:
            logger.warning("Azure validation failed (%s); falling back to ChromaDB.", error)

    def _handle_azure_general_error(
        self,
        error: Exception,
        policy: str,
        logger: Optional[logging.Logger],
    ) -> None:
        """Handle general Azure errors based on policy."""
        if policy == "azure_only":
            raise PreflightError(
                provider="azure_search",
                reason="provider_failed",
                detail=str(error),
                snapshot=self._dump_kb_config_snapshot(logger),
            )
        if logger:
            logger.warning("Azure provider failed (%s); falling back to ChromaDB.", error)

    async def _close_azure_provider(self, provider: Optional[Any]) -> None:
        """Safely close Azure provider if it exists."""
        if provider:
            try:
                await provider.close()
            except Exception:
                pass  # nosec B110 - intentionally ignoring cleanup errors

    def _azure_snippet_cap(self) -> int:
        """Optional cap for Azure snippet/content length."""
        v = os.getenv("KB_AZURE_SNIPPET_CAP", "")
        try:
            n = int(v)
            return max(0, n)
        except Exception:
            return 0

    def _ensure_kb_directory(self) -> None:
        """Ensure the KB directory exists for local retrieval."""
        try:
            os.makedirs(self._kb_path, exist_ok=True)
        except Exception:
            pass  # nosec B110 - intentionally ignoring directory creation errors
