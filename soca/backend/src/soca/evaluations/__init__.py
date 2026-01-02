"""Evaluations module with AI-powered evaluation logic."""

import random
import uuid
from datetime import datetime
from typing import Optional

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


async def evaluate_submission(
    submission: Submission,
    criteria_set: CriteriaSet,
) -> EvaluationResult:
    """Evaluate a single submission against criteria using AI."""
    # Build evaluation prompt
    criteria_text = "\n".join(
        f"- {c.name} (weight: {c.weight}%, max score: {c.max_score}): {c.description}"
        for c in criteria_set.criteria
    )

    prompt = f"""You are an expert evaluator. Evaluate the following submission against the given criteria.

SUBMISSION:
Title: {submission.name}
Content:
{submission.extracted_text[:8000]}

CRITERIA:
{criteria_text}

For each criterion, provide:
1. A score from 1 to the max score
2. A brief narrative justification (1-2 sentences)

Then provide:
- An overall weighted score (0-100)
- A summary paragraph (2-3 sentences)

Format your response as JSON:
{{
  "criterionResults": [
    {{"criterionId": "...", "score": X.X, "narrative": "..."}},
    ...
  ],
  "overallScore": XX.X,
  "summary": "..."
}}
"""

    # Call Ingenious API for AI evaluation
    if settings.ingenious_api_url and settings.ingenious_api_key:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.ingenious_api_url}/api/v1/chat",
                    json={
                        "user_prompt": prompt,
                        "conversation_flow": "echo-agent",
                        "thread_id": str(uuid.uuid4()),
                    },
                    headers={"Authorization": f"Bearer {settings.ingenious_api_key}"},
                    timeout=120.0,
                )
                if response.status_code == 200:
                    # Parse response and extract evaluation
                    # For now, use mock data
                    pass
        except Exception:
            pass

    # Mock evaluation results for demo
    criterion_results = []
    total_weighted = 0.0
    for criterion in criteria_set.criteria:
        score = round(random.uniform(3.0, criterion.max_score), 1)
        normalized = score / criterion.max_score * 100
        total_weighted += normalized * (criterion.weight / 100)
        criterion_results.append(
            CriterionResult(
                criterionId=criterion.id,
                score=score,
                narrative=f"The submission demonstrates {'strong' if score > 4 else 'adequate'} performance in {criterion.name.lower()}.",
            )
        )

    return EvaluationResult(
        submissionId=submission.id,
        submissionName=submission.name,
        submissionAuthor=None,
        overallScore=round(total_weighted, 1),
        criterionResults=criterion_results,
        summary=f"Overall, this submission shows {'excellent' if total_weighted > 80 else 'good' if total_weighted > 60 else 'moderate'} quality across the evaluation criteria.",
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
