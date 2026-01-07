"""Template management for SoCa.

Fetches Jinja2 templates from Prompt Tuner and renders them locally.
Falls back to default templates if Prompt Tuner is unavailable.
"""

import logging
from typing import Any

import httpx
from jinja2 import Template, TemplateError

from soca.config import settings

logger = logging.getLogger(__name__)

# Default templates (fallback if Prompt Tuner unavailable)
DEFAULT_EVALUATION_USER_PROMPT = """Evaluate the following submission against the given criteria.

SUBMISSION:
Title: {{ submission_name }}
Content:
{{ submission_content }}

CRITERIA (format: criterionId: Name (weight%, max score): Description):
{{ criteria_text }}

For each criterion, provide a score and narrative. Use the exact criterionId values provided above."""

DEFAULT_CRITERIA_GENERATOR_USER_PROMPT = """Analyze the following document and generate evaluation criteria.

DOCUMENT:
{{ document_text }}

Generate a comprehensive set of evaluation criteria based on this document.
The criteria should be:
- Specific to the document type and content
- Measurable with clear scoring guidelines
- Weighted appropriately (weights should sum to 100)
- Include 4-8 criteria for comprehensive coverage

Respond with a JSON object containing:
- name: A short descriptive name for this criteria set
- description: A 1-2 sentence description of what this criteria set evaluates
- criteria: Array of criterion objects with id, name, description, weight, maxScore"""

# Simple in-memory cache for templates
_template_cache: dict[str, str] = {}


async def get_user_prompt_template(template_name: str, revision: str = "active") -> str:
    """Fetch a user prompt template from Prompt Tuner.

    Args:
        template_name: Name of the template file (e.g., "soca_evaluator_user.md")
        revision: Prompt revision to use (default: "active")

    Returns:
        Template content as a string (Jinja2 template)
    """
    cache_key = f"{revision}:{template_name}"

    # Check cache first
    if cache_key in _template_cache:
        return _template_cache[cache_key]

    # Fetch from Prompt Tuner
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = f"{settings.ingenious_api_url}/api/prompts/{revision}/{template_name}"
            response = await client.get(url)

            if response.status_code == 200:
                data = response.json()
                template_content: str = data.get("content", "")
                if template_content:
                    _template_cache[cache_key] = template_content
                    logger.info(f"Fetched template {template_name} from Prompt Tuner")
                    return template_content

            logger.warning(f"Failed to fetch template {template_name}: {response.status_code}")
    except httpx.HTTPError as e:
        logger.warning(f"HTTP error fetching template {template_name}: {e}")
    except Exception as e:
        logger.warning(f"Error fetching template {template_name}: {e}")

    # Return fallback template
    return _get_fallback_template(template_name)


def _get_fallback_template(template_name: str) -> str:
    """Get fallback template when Prompt Tuner is unavailable."""
    fallbacks = {
        "soca_evaluator_user.md": DEFAULT_EVALUATION_USER_PROMPT,
        "criteria_generator_user.md": DEFAULT_CRITERIA_GENERATOR_USER_PROMPT,
    }
    return fallbacks.get(template_name, "")


def render_template(template_content: str, variables: dict[str, Any]) -> str:
    """Render a Jinja2 template with the given variables.

    Args:
        template_content: Jinja2 template string
        variables: Dictionary of variables to render

    Returns:
        Rendered template string
    """
    try:
        template = Template(template_content)
        return template.render(**variables)
    except TemplateError as e:
        logger.error(f"Template rendering error: {e}")
        # Fallback to simple string formatting if Jinja2 fails
        try:
            return template_content.format(**variables)
        except (KeyError, ValueError):
            return template_content


def clear_cache() -> None:
    """Clear the template cache."""
    _template_cache.clear()
    logger.info("Template cache cleared")
