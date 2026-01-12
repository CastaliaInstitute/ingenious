"""Evaluations module with AI-powered evaluation logic."""

import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Any, Optional

import httpx

from soca.config import settings
from soca.db import db
from soca.models import (
    CriteriaSet,
    CriterionResult,
    Evaluation,
    EvaluationResult,
    EvaluationStatus,
    Submission,
)
from soca.templates import get_user_prompt_template, render_template

logger = logging.getLogger(__name__)

# Retry configuration
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 2.0  # seconds
MAX_RETRY_DELAY = 30.0  # seconds


async def _call_prompt_tuner_api(
    prompt_tuner_url: str,
    prompt: str,
) -> tuple[bool, dict[str, Any] | None, str]:
    """Call the Prompt Tuner API with error handling.

    Returns:
        Tuple of (success, data, error_message)
    """
    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Calling Prompt Tuner API at {prompt_tuner_url}/api/v1/chat")
            response = await client.post(
                f"{prompt_tuner_url}/api/v1/chat",
                json={
                    "user_prompt": prompt,
                    "thread_id": str(uuid.uuid4()),
                    "conversation_flow": "soca-evaluator",
                },
                timeout=120.0,
            )

            if response.status_code == 200:
                data = response.json()
                agent_response = data.get("agent_response", "{}")

                # Parse the AI response
                try:
                    evaluation_data = json.loads(agent_response)
                    # Check if the response has valid criterion results
                    if evaluation_data.get("criterionResults"):
                        return True, evaluation_data, ""
                    else:
                        return False, None, "AI returned empty criterion results"
                except json.JSONDecodeError as e:
                    return False, None, f"Failed to parse AI response: {e}"
            elif response.status_code == 429:
                return False, None, "Rate limited by AI service"
            else:
                return False, None, f"API returned status {response.status_code}"

    except httpx.TimeoutException:
        return False, None, "Request timed out"
    except httpx.ConnectError:
        return False, None, f"Could not connect to {prompt_tuner_url}"
    except Exception as e:
        return False, None, f"Error: {str(e)}"


async def evaluate_submission(
    submission: Submission,
    criteria_set: CriteriaSet,
) -> EvaluationResult:
    """Evaluate a single submission against criteria using AI via Prompt Tuner.

    Includes retry logic with exponential backoff for transient failures.
    """
    # Build criteria text for template
    criteria_text = "\n".join(
        f"- {c.id}: {c.name} (weight: {c.weight}%, max score: {c.max_score}): {c.description}"
        for c in criteria_set.criteria
    )

    # Fetch and render user prompt template from Prompt Tuner
    template_content = await get_user_prompt_template("soca_evaluator_user.md")
    prompt = render_template(
        template_content,
        {
            "submission_name": submission.name,
            "submission_content": (
                submission.extracted_text[:8000]
                if submission.extracted_text
                else "No content available"
            ),
            "criteria_text": criteria_text,
        },
    )

    # Call Prompt Tuner API for AI evaluation with retries
    prompt_tuner_url = settings.ingenious_api_url or "http://localhost:8002"

    last_error = ""
    retry_delay = INITIAL_RETRY_DELAY

    for attempt in range(MAX_RETRIES):
        if attempt > 0:
            logger.info(
                f"Retry attempt {attempt + 1}/{MAX_RETRIES} for submission {submission.id} "
                f"after {retry_delay}s delay"
            )
            await asyncio.sleep(retry_delay)
            # Exponential backoff with cap
            retry_delay = min(retry_delay * 2, MAX_RETRY_DELAY)

        success, evaluation_data, error = await _call_prompt_tuner_api(prompt_tuner_url, prompt)

        if success and evaluation_data:
            # Map criterion results
            criterion_results = []
            for cr in evaluation_data.get("criterionResults", []):
                criterion_results.append(
                    CriterionResult(
                        criterion_id=cr.get("criterionId", ""),
                        score=float(cr.get("score", 0)),
                        narrative=cr.get("narrative", ""),
                    )
                )

            # If no criterion results from AI, create default ones
            if not criterion_results:
                for criterion in criteria_set.criteria:
                    criterion_results.append(
                        CriterionResult(
                            criterion_id=criterion.id,
                            score=criterion.max_score / 2,
                            narrative="Evaluation pending - AI response incomplete.",
                        )
                    )

            # Calculate overall score as weighted percentage (0-100)
            # Formula: sum of (score / maxScore) * weight for each criterion
            overall_score = 0.0
            criteria_lookup = {c.id: c for c in criteria_set.criteria}
            for cr in criterion_results:
                if cr.criterion_id in criteria_lookup:
                    criterion = criteria_lookup[cr.criterion_id]
                    if criterion.max_score > 0:
                        # (score / maxScore) * weight
                        weighted_pct = (cr.score / criterion.max_score) * criterion.weight
                        overall_score += weighted_pct

            logger.info(f"AI evaluation successful for submission {submission.id}")

            return EvaluationResult(
                submission_id=submission.id,
                submission_name=submission.name,
                submission_author=None,
                overall_score=round(overall_score, 2),
                criterion_results=criterion_results,
                summary=evaluation_data.get("summary", "Evaluation completed."),
            )

        last_error = error
        logger.warning(f"Evaluation attempt {attempt + 1} failed: {error}")

    # All retries exhausted - return error result
    logger.error(
        f"AI evaluation failed for submission {submission.id} after {MAX_RETRIES} attempts: {last_error}"
    )

    criterion_results = []
    for criterion in criteria_set.criteria:
        criterion_results.append(
            CriterionResult(
                criterion_id=criterion.id,
                score=0,
                narrative=f"AI evaluation failed after {MAX_RETRIES} attempts.",
            )
        )

    return EvaluationResult(
        submission_id=submission.id,
        submission_name=submission.name,
        submission_author=None,
        overall_score=0,
        criterion_results=criterion_results,
        summary=f"AI evaluation failed after {MAX_RETRIES} retries. Last error: {last_error}",
    )


async def run_evaluation(evaluation_id: str) -> Optional[Evaluation]:
    """Run an evaluation asynchronously."""
    evaluation = await db.get_evaluation(evaluation_id)
    if not evaluation:
        return None

    criteria_set = await db.get_criteria_set(evaluation.criteria_set_id)
    if not criteria_set:
        evaluation.status = EvaluationStatus.FAILED
        await db.update_evaluation(evaluation)
        return evaluation

    evaluation.status = EvaluationStatus.RUNNING
    evaluation.criteria_set_name = criteria_set.name
    await db.update_evaluation(evaluation)

    results = []
    for submission_id in evaluation.submission_ids:
        submission = await db.get_submission(submission_id)
        if submission:
            result = await evaluate_submission(submission, criteria_set)
            results.append(result)
            evaluation.results = results
            await db.update_evaluation(evaluation)

    evaluation.status = EvaluationStatus.COMPLETED
    evaluation.completed_at = datetime.utcnow().isoformat() + "Z"
    await db.update_evaluation(evaluation)

    return evaluation
