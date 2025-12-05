"""ChromaDB/local search integration for knowledge base conversation flow.

This module handles local ChromaDB operations including collection initialization,
document loading, and search execution.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from ingenious.config.config import Config


class ChromaSearchMixin:
    """Mixin class providing ChromaDB/local search functionality.

    This mixin extracts ChromaDB-related methods from the main ConversationFlow
    class for better organization and maintainability.
    """

    if TYPE_CHECKING:
        _config: Config
        _kb_path: str
        _chroma_path: str
        _chroma_db: Any
        _chroma_collection: Any
        _chroma_initialized: bool

    def _ensure_kb_directory(self) -> None:
        """Ensure the KB directory exists for local retrieval."""
        try:
            os.makedirs(self._kb_path, exist_ok=True)
        except Exception:
            pass  # nosec B110 - intentionally ignoring directory creation errors

    def _init_chroma(self, logger: Optional[logging.Logger] = None) -> None:
        """Lazy-init a private Chroma client and collection in kb_path/.chroma."""
        if self._chroma_initialized:
            return

        try:
            import chromadb
            from chromadb.config import Settings
        except ImportError as e:
            if logger:
                logger.warning("chromadb not installed; local retrieval will fail: %s", e)
            self._chroma_initialized = True
            return

        self._ensure_kb_directory()

        try:
            self._chroma_db = chromadb.Client(
                Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory=self._chroma_path,
                    anonymized_telemetry=False,
                )
            )
        except TypeError:
            self._chroma_db = chromadb.Client(
                Settings(persist_directory=self._chroma_path, anonymized_telemetry=False)
            )

        self._chroma_collection = self._chroma_db.get_or_create_collection(name="kb_collection")
        self._chroma_initialized = True

        doc_count_before = self._chroma_collection.count()
        self._read_kb_files_into_chroma(logger)
        doc_count_after = self._chroma_collection.count()

        if logger:
            logger.info(
                "Chroma initialised: %d documents before scan, %d after",
                doc_count_before,
                doc_count_after,
            )

    def _read_kb_files_into_chroma(self, logger: Optional[logging.Logger] = None) -> None:
        """Scan kb_path for .txt/.md, add to ChromaDB if not already present."""
        if not self._chroma_collection:
            return

        extensions = (".txt", ".md")
        kb_path = Path(self._kb_path)

        if not kb_path.is_dir():
            if logger:
                logger.warning("KB path does not exist or is not a directory: %s", kb_path)
            return

        existing_ids = set(self._chroma_collection.get()["ids"])

        new_docs: List[str] = []
        new_ids: List[str] = []
        new_meta: List[Dict[str, Any]] = []

        for file_path in kb_path.iterdir():
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in extensions:
                continue

            file_id = file_path.name
            if file_id in existing_ids:
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="replace")
                if not content.strip():
                    continue
                new_docs.append(content)
                new_ids.append(file_id)
                new_meta.append({"source": file_id})
            except Exception as e:
                if logger:
                    logger.debug("Failed to read KB file %s: %s", file_path, e)

        if new_docs:
            self._chroma_collection.add(documents=new_docs, ids=new_ids, metadatas=new_meta)
            if logger:
                logger.info("Added %d new documents to ChromaDB.", len(new_docs))

    async def _search_local_chroma(
        self, query: str, top_k: int, logger: Optional[logging.Logger] = None
    ) -> str:
        """Search local ChromaDB collection for relevant documents."""
        self._init_chroma(logger)

        if not self._chroma_collection:
            return f"No relevant information found in local knowledge base for: {query}"

        try:
            results = self._chroma_collection.query(
                query_texts=[query],
                n_results=min(top_k, self._chroma_collection.count() or 1),
            )
        except Exception as e:
            if logger:
                logger.warning("ChromaDB query failed: %s", e)
            return f"Error searching local knowledge base: {str(e)}"

        return self._format_chroma_results(query, results)

    def _format_chroma_results(self, query: str, results: Dict[str, Any]) -> str:
        """Format ChromaDB search results into readable string."""
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        if not documents:
            return f"No relevant information found in local knowledge base for: {query}"

        parts: List[str] = []
        for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances), 1):
            source = meta.get("source", f"Document {i}") if meta else f"Document {i}"
            score = round(1.0 - dist, 3) if isinstance(dist, (int, float)) else "N/A"
            snippet = (doc[:500] + "...") if len(doc) > 500 else doc
            parts.append(f"[{i}] {source} (score={score})\n{snippet}")

        return "Found relevant information from local knowledge base:\n\n" + "\n\n---\n\n".join(
            parts
        )

    def _fallback_on_empty(self) -> bool:
        """Check if fallback is enabled when Azure returns empty results."""
        v = os.getenv("KB_FALLBACK_ON_EMPTY", "0")
        return v.strip().lower() in {"1", "true", "yes", "on"}
