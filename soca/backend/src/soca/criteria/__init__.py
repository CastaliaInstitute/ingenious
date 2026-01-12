"""Criteria module for AI-powered criteria generation."""

import json
import logging
import uuid
from datetime import datetime, timezone
from io import BytesIO
from typing import Optional

import httpx

from soca.config import settings
from soca.models import CriteriaSet, Criterion
from soca.templates import get_user_prompt_template, render_template

logger = logging.getLogger(__name__)

# MIME types for file type detection
_PLAIN_TEXT_TYPES = ("text/plain", "text/markdown")
_PDF_TYPE = "application/pdf"
_DOCX_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def _extract_text_from_plain(content: bytes) -> str:
    """Extract text from plain text or markdown file.

    Args:
        content: Raw file bytes

    Returns:
        Decoded text content
    """
    return content.decode("utf-8", errors="ignore")


def _extract_text_from_pdf(content: bytes) -> str:
    """Extract text from PDF file.

    Args:
        content: Raw PDF file bytes

    Returns:
        Extracted text from all pages

    Raises:
        ValueError: If pypdf is not installed or extraction fails
    """
    try:
        import pypdf

        reader = pypdf.PdfReader(BytesIO(content))
        text_parts = [page.extract_text() for page in reader.pages if page.extract_text()]
        return "\n\n".join(text_parts)
    except ImportError:
        logger.warning("pypdf not installed, PDF extraction unavailable")
        raise ValueError("PDF extraction requires pypdf library")
    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        raise ValueError(f"Failed to extract text from PDF: {e}")


def _extract_text_from_docx(content: bytes) -> str:
    """Extract text from DOCX file.

    Args:
        content: Raw DOCX file bytes

    Returns:
        Extracted text from all paragraphs

    Raises:
        ValueError: If python-docx is not installed or extraction fails
    """
    try:
        import docx

        doc = docx.Document(BytesIO(content))
        text_parts = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
        return "\n\n".join(text_parts)
    except ImportError:
        logger.warning("python-docx not installed, DOCX extraction unavailable")
        raise ValueError("DOCX extraction requires python-docx library")
    except Exception as e:
        logger.error(f"DOCX extraction failed: {e}")
        raise ValueError(f"Failed to extract text from DOCX: {e}")


def _is_pdf_file(content_type: str, filename: str) -> bool:
    """Check if file is a PDF based on content type or extension."""
    return content_type == _PDF_TYPE or filename.lower().endswith(".pdf")


def _is_docx_file(content_type: str, filename: str) -> bool:
    """Check if file is a DOCX based on content type or extension."""
    return content_type == _DOCX_TYPE or filename.lower().endswith(".docx")


async def extract_text_from_file(content: bytes, content_type: str, filename: str) -> str:
    """Extract text from uploaded file based on content type.

    Args:
        content: Raw file bytes
        content_type: MIME type of the file
        filename: Original filename for extension fallback

    Returns:
        Extracted text content

    Raises:
        ValueError: If file type is unsupported or extraction fails
    """
    if content_type in _PLAIN_TEXT_TYPES:
        return _extract_text_from_plain(content)

    if _is_pdf_file(content_type, filename):
        return _extract_text_from_pdf(content)

    if _is_docx_file(content_type, filename):
        return _extract_text_from_docx(content)

    raise ValueError(f"Unsupported file type: {content_type}")


async def generate_criteria_from_text(
    document_text: str,
    name_override: Optional[str] = None,
    description_override: Optional[str] = None,
) -> CriteriaSet:
    """Generate a criteria set from document text using Prompt Tuner AI.

    Args:
        document_text: The document text to analyze
        name_override: Optional name to use instead of AI-generated
        description_override: Optional description to use instead of AI-generated

    Returns:
        Generated CriteriaSet with unique IDs

    Raises:
        ValueError: If AI response cannot be parsed
        httpx.HTTPError: If Prompt Tuner API call fails
    """
    prompt_tuner_url = settings.ingenious_api_url or "http://localhost:8002"

    # Fetch and render user prompt template from Prompt Tuner
    template_content = await get_user_prompt_template("criteria_generator_user.md")
    prompt = render_template(
        template_content,
        {"document_text": document_text[:10000]},
    )

    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Calling Prompt Tuner API at {prompt_tuner_url}/api/v1/chat")
            response = await client.post(
                f"{prompt_tuner_url}/api/v1/chat",
                json={
                    "user_prompt": prompt,
                    "thread_id": str(uuid.uuid4()),
                    "conversation_flow": "criteria-generator",
                },
                timeout=120.0,
            )

            if response.status_code != 200:
                logger.error(f"Prompt Tuner API returned status {response.status_code}")
                raise ValueError(f"Prompt Tuner API error: {response.status_code}")

            data = response.json()
            agent_response = data.get("agent_response", "{}")

            # Parse the AI response
            try:
                criteria_data = json.loads(agent_response)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON: {e}")
                raise ValueError(f"Invalid AI response format: {e}")

            # Build criteria list with unique IDs
            criteria = []
            for i, c in enumerate(criteria_data.get("criteria", [])):
                criteria.append(
                    Criterion(
                        id=f"c{i + 1}-{uuid.uuid4().hex[:8]}",
                        name=c.get("name", f"Criterion {i + 1}"),
                        description=c.get("description", ""),
                        weight=int(c.get("weight", 20)),
                        max_score=int(c.get("maxScore", 5)),
                    )
                )

            if not criteria:
                raise ValueError("AI did not generate any criteria")

            # Create the CriteriaSet
            return CriteriaSet(
                id=str(uuid.uuid4()),
                name=name_override or criteria_data.get("name", "Generated Criteria Set"),
                description=description_override or criteria_data.get("description"),
                criteria=criteria,
                created_at=datetime.now(timezone.utc).isoformat(),
            )

    except httpx.TimeoutException:
        logger.error("Prompt Tuner API request timed out")
        raise ValueError("AI service timeout - please try again")
    except httpx.ConnectError:
        logger.error(f"Could not connect to Prompt Tuner API at {prompt_tuner_url}")
        raise ValueError("AI service unavailable - check Prompt Tuner is running")
