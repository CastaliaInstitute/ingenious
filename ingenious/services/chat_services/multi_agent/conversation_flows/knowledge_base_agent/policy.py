"""Knowledge base policy management.

This module handles policy-based backend selection for knowledge base queries,
supporting azure_only, prefer_azure, prefer_local, and local_only modes.
"""

from __future__ import annotations

import logging
import os
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ingenious.models.chat import ChatRequest


class KBPolicy(Enum):
    """Knowledge base backend policy options.

    Attributes:
        AZURE_ONLY: Only use Azure AI Search, fail if unavailable.
        PREFER_AZURE: Try Azure first, fall back to local on failure.
        PREFER_LOCAL: Try local first, fall back to Azure if empty.
        LOCAL_ONLY: Only use local ChromaDB, never use Azure.
    """

    AZURE_ONLY = "azure_only"
    PREFER_AZURE = "prefer_azure"
    PREFER_LOCAL = "prefer_local"
    LOCAL_ONLY = "local_only"


class KBMode(Enum):
    """Knowledge base response mode options.

    Attributes:
        DIRECT: Return search results directly (deterministic).
        ASSIST: Use LLM to compose a response from search results.
    """

    DIRECT = "direct"
    ASSIST = "assist"


# Safe, conservative defaults for top_k values
TOPK_DIRECT_DEFAULT: int = 3
TOPK_ASSIST_DEFAULT: int = 5


class KBPolicyManager:
    """Manages knowledge base policy and configuration.

    This class centralizes policy resolution, mode selection,
    and top_k parameter handling.
    """

    def __init__(
        self,
        config: Any,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """Initialize the policy manager.

        Args:
            config: Application configuration object.
            logger: Optional logger for diagnostics.
        """
        self._config = config
        self._logger = logger

    def get_policy(self) -> KBPolicy:
        """Resolve the current KB policy from config or environment.

        Priority: config.knowledge_base_policy > KB_POLICY env > azure_only default

        Returns:
            The resolved KBPolicy.
        """
        policy_val = getattr(self._config, "knowledge_base_policy", None) or os.getenv(
            "KB_POLICY", "azure_only"
        )

        try:
            policy_str = str(policy_val).strip().lower()
        except Exception:
            policy_str = "azure_only"

        try:
            return KBPolicy(policy_str)
        except ValueError:
            if self._logger:
                self._logger.warning("Invalid KB_POLICY '%s', defaulting to azure_only", policy_val)
            return KBPolicy.AZURE_ONLY

    def get_mode(self) -> tuple[KBMode, bool]:
        """Resolve the KB mode from config or environment.

        Returns:
            Tuple of (mode, was_coerced). was_coerced is True if an invalid
            value was corrected to the default.
        """
        raw_mode_val = getattr(self._config, "knowledge_base_mode", None) or os.getenv(
            "KB_MODE", "direct"
        )

        try:
            raw_mode = str(raw_mode_val).strip().lower()
        except Exception:
            return KBMode.DIRECT, True

        try:
            return KBMode(raw_mode), False
        except ValueError:
            if self._logger:
                self._logger.warning("Invalid KB_MODE '%s', defaulting to direct", raw_mode_val)
            return KBMode.DIRECT, True

    def should_fallback_on_empty(self) -> bool:
        """Check if empty results should trigger backend fallback.

        Returns:
            True if KB_FALLBACK_ON_EMPTY is enabled.
        """
        val = os.getenv("KB_FALLBACK_ON_EMPTY", "")
        return val.strip().lower() in {"1", "true", "yes"}

    def get_azure_snippet_cap(self) -> int:
        """Get the optional Azure snippet content cap.

        Returns:
            Maximum snippet length, or 0 for no cap.
        """
        val = os.getenv("KB_AZURE_SNIPPET_CAP", "")
        try:
            n = int(val)
            return max(0, n)
        except Exception:
            return 0

    def get_top_k(
        self,
        mode: KBMode,
        chat_request: Optional["ChatRequest"] = None,
    ) -> int:
        """Resolve top_k parameter with proper priority.

        Priority: request override > env override > mode default

        Args:
            mode: The current KB mode (direct or assist).
            chat_request: Optional request that may contain top_k override.

        Returns:
            The resolved top_k value.
        """
        # 1) Check request override
        if chat_request is not None:
            override = self._resolve_topk_from_request(chat_request)
            if override is not None:
                return override

        # 2) Check env override based on mode
        if mode == KBMode.ASSIST:
            env_val = (os.getenv("KB_TOPK_ASSIST") or "").strip()
            if env_val.isdigit() and int(env_val) > 0:
                return int(env_val)
            return TOPK_ASSIST_DEFAULT
        else:
            env_val = (os.getenv("KB_TOPK_DIRECT") or "").strip()
            if env_val.isdigit() and int(env_val) > 0:
                return int(env_val)
            return TOPK_DIRECT_DEFAULT

    def _resolve_topk_from_request(self, chat_request: "ChatRequest") -> Optional[int]:
        """Extract top_k override from request.

        Args:
            chat_request: The chat request to examine.

        Returns:
            The top_k value if found, None otherwise.
        """
        topk_keys = ("kb_top_k", "top_k", "search_top_k")

        # Check direct attributes
        for attr in topk_keys:
            result = self._parse_positive_int(getattr(chat_request, attr, None))
            if result is not None:
                return result

        # Check nested parameters dict
        params = getattr(chat_request, "parameters", None)
        if isinstance(params, dict):
            for key in topk_keys:
                result = self._parse_positive_int(params.get(key))
                if result is not None:
                    return result

        return None

    def _parse_positive_int(self, val: Any) -> Optional[int]:
        """Parse a value as a positive integer.

        Args:
            val: The value to parse.

        Returns:
            The integer if valid and positive, None otherwise.
        """
        try:
            if isinstance(val, int) and val > 0:
                return val
            if isinstance(val, str):
                stripped = val.strip()
                if stripped.isdigit() and int(stripped) > 0:
                    return int(stripped)
        except Exception:  # nosec B110
            pass
        return None

    def should_use_azure(self, azure_available: bool) -> bool:
        """Determine if Azure should be used based on policy and availability.

        Args:
            azure_available: Whether Azure Search is available.

        Returns:
            True if Azure should be attempted.
        """
        policy = self.get_policy()

        if policy == KBPolicy.LOCAL_ONLY:
            return False

        if policy == KBPolicy.AZURE_ONLY:
            return True  # Will fail later if not available

        if policy == KBPolicy.PREFER_AZURE:
            return azure_available

        # PREFER_LOCAL - don't use Azure initially, may fallback later
        return False

    def allows_local_fallback(self) -> bool:
        """Check if the current policy allows falling back to local search.

        Returns:
            True if local fallback is allowed.
        """
        policy = self.get_policy()
        return policy in {KBPolicy.PREFER_AZURE, KBPolicy.PREFER_LOCAL, KBPolicy.LOCAL_ONLY}


def diagnostics_enabled() -> bool:
    """Check if KB diagnostics are enabled.

    Returns:
        True if KB_DIAGNOSTICS is set to 1/true/yes.
    """
    val = os.getenv("KB_DIAGNOSTICS", "")
    return val.strip().lower() in {"1", "true", "yes"}
