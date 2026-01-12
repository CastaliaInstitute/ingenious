"""SoCa FastAPI application."""

import csv
import io
import json
import logging
import uuid
from datetime import datetime
from typing import Any, Optional

import httpx
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from soca.auth import authenticate_user, create_access_token, get_current_user
from soca.config import settings
from soca.criteria import extract_text_from_file, generate_criteria_from_text
from soca.db import db, get_templates
from soca.evaluations import run_evaluation
from soca.models import (
    CreateCriteriaSetRequest,
    CreateEvaluationRequest,
    CriteriaSet,
    Evaluation,
    EvaluationStatus,
    LoginRequest,
    LoginResponse,
    Submission,
    UpdateSubmissionRequest,
    User,
)

logger = logging.getLogger(__name__)

app = FastAPI(title="SoCa API", version="0.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Auth endpoints
@app.post("/api/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest) -> LoginResponse:
    """Login with email and password."""
    user = authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.id, "email": user.email})
    return LoginResponse(token=token, user=user)


@app.get("/api/auth/me")
async def get_me(current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    """Get current user info."""
    return {"user": current_user}


# Submissions endpoints
@app.get("/api/submissions", response_model=list[Submission])
async def list_submissions(current_user: User = Depends(get_current_user)) -> list[Submission]:
    """List all submissions."""
    submissions: list[Submission] = await db.list_submissions()
    return submissions


@app.post("/api/submissions", response_model=Submission)
async def create_submission(
    file: UploadFile = File(...),
    name: Optional[str] = None,
    description: Optional[str] = None,
    current_user: User = Depends(get_current_user),
) -> Submission:
    """Upload a new submission."""
    content = await file.read()
    file_size = len(content)

    # Extract text using the comprehensive extraction function
    extracted_text = ""
    try:
        extracted_text = await extract_text_from_file(
            content=content,
            content_type=file.content_type or "application/octet-stream",
            filename=file.filename or "file",
        )
    except ValueError as e:
        # Log but don't fail - store empty text for unsupported types
        import logging

        logging.getLogger(__name__).warning(f"Text extraction failed: {e}")

    # For demo, store file URL as placeholder
    # In production, upload to Azure Blob Storage
    file_url = f"/files/{uuid.uuid4()}/{file.filename}"

    submission = Submission(
        id=str(uuid.uuid4()),
        name=name or file.filename or "Untitled",
        description=description,
        file_url=file_url,
        file_name=file.filename or "file",
        file_type=file.content_type or "application/octet-stream",
        file_size=file_size,
        extracted_text=extracted_text[:10000],  # Limit text size
        uploaded_at=datetime.utcnow().isoformat() + "Z",
    )

    return await db.create_submission(submission)


@app.delete("/api/submissions/{submission_id}")
async def delete_submission(
    submission_id: str,
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """Delete a submission."""
    success = await db.delete_submission(submission_id)
    if not success:
        raise HTTPException(status_code=404, detail="Submission not found")
    return {"status": "deleted"}


@app.patch("/api/submissions/{submission_id}", response_model=Submission)
async def update_submission(
    submission_id: str,
    request: UpdateSubmissionRequest,
    current_user: User = Depends(get_current_user),
) -> Submission:
    """Update a submission's metadata."""
    existing = await db.get_submission(submission_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Submission not found")

    # Update only provided fields
    updated = Submission(
        id=existing.id,
        name=request.name if request.name is not None else existing.name,
        description=request.description
        if request.description is not None
        else existing.description,
        file_url=existing.file_url,
        file_name=existing.file_name,
        file_type=existing.file_type,
        file_size=existing.file_size,
        extracted_text=existing.extracted_text,
        uploaded_at=existing.uploaded_at,
    )
    return await db.update_submission(updated)


# Criteria endpoints
@app.get("/api/criteria-sets", response_model=list[CriteriaSet])
async def list_criteria_sets(current_user: User = Depends(get_current_user)) -> list[CriteriaSet]:
    """List all criteria sets."""
    criteria_sets: list[CriteriaSet] = await db.list_criteria_sets()
    return criteria_sets


@app.get("/api/criteria-templates", response_model=list[CriteriaSet])
async def list_criteria_templates(
    current_user: User = Depends(get_current_user),
) -> list[CriteriaSet]:
    """List available criteria templates."""
    templates: list[CriteriaSet] = get_templates()
    return templates


@app.post("/api/criteria-sets", response_model=CriteriaSet)
async def create_criteria_set(
    request: CreateCriteriaSetRequest,
    current_user: User = Depends(get_current_user),
) -> CriteriaSet:
    """Create a new criteria set."""
    criteria_set = CriteriaSet(
        id=str(uuid.uuid4()),
        name=request.name,
        description=request.description,
        criteria=request.criteria,
        created_at=datetime.utcnow().isoformat() + "Z",
    )
    return await db.create_criteria_set(criteria_set)


@app.patch("/api/criteria-sets/{criteria_set_id}", response_model=CriteriaSet)
async def update_criteria_set(
    criteria_set_id: str,
    request: CreateCriteriaSetRequest,
    current_user: User = Depends(get_current_user),
) -> CriteriaSet:
    """Update a criteria set."""
    existing = await db.get_criteria_set(criteria_set_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Criteria set not found")

    updated = CriteriaSet(
        id=criteria_set_id,
        name=request.name,
        description=request.description,
        criteria=request.criteria,
        created_at=existing.created_at,
    )
    return await db.update_criteria_set(updated)


@app.delete("/api/criteria-sets/{criteria_set_id}")
async def delete_criteria_set(
    criteria_set_id: str,
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """Delete a criteria set."""
    success = await db.delete_criteria_set(criteria_set_id)
    if not success:
        raise HTTPException(status_code=404, detail="Criteria set not found")
    return {"status": "deleted"}


@app.post("/api/criteria-sets/generate", response_model=CriteriaSet)
async def generate_criteria_set(
    file: Optional[UploadFile] = File(default=None),
    document_text: Optional[str] = Form(default=None),
    name: Optional[str] = Form(default=None),
    current_user: User = Depends(get_current_user),
) -> CriteriaSet:
    """Generate a criteria set from document text or uploaded file using AI.

    Supports two input methods:
    1. Direct text: Pass document_text as form field
    2. File upload: Upload PDF, DOCX, or TXT file

    The AI will analyze the document and generate appropriate evaluation criteria.
    """
    # Validate that at least one input method is provided
    if not file and not document_text:
        raise HTTPException(status_code=400, detail="Either file or document_text must be provided")

    # Extract text from file if provided
    if file:
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        try:
            document_text = await extract_text_from_file(
                content=content,
                content_type=file.content_type or "application/octet-stream",
                filename=file.filename or "file",
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Validate extracted/provided text
    if not document_text or len(document_text.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail="Document text is too short to generate meaningful criteria",
        )

    # Call AI to generate criteria
    try:
        criteria_set = await generate_criteria_from_text(
            document_text=document_text,
            name_override=name,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Save to database
    return await db.create_criteria_set(criteria_set)


# Evaluations endpoints
@app.get("/api/evaluations", response_model=list[Evaluation])
async def list_evaluations(current_user: User = Depends(get_current_user)) -> list[Evaluation]:
    """List all evaluations."""
    evaluations: list[Evaluation] = await db.list_evaluations()
    return evaluations


@app.get("/api/evaluations/{evaluation_id}", response_model=Evaluation)
async def get_evaluation(
    evaluation_id: str,
    current_user: User = Depends(get_current_user),
) -> Evaluation:
    """Get a specific evaluation."""
    evaluation = await db.get_evaluation(evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return evaluation


@app.post("/api/evaluations", response_model=Evaluation)
async def create_evaluation(
    request: CreateEvaluationRequest,
    current_user: User = Depends(get_current_user),
) -> Evaluation:
    """Create a new evaluation."""
    # Get criteria set name
    criteria_set = await db.get_criteria_set(request.criteria_set_id)
    criteria_set_name = criteria_set.name if criteria_set else None

    evaluation = Evaluation(
        id=str(uuid.uuid4()),
        name=request.name,
        status=EvaluationStatus.DRAFT,
        submission_ids=request.submission_ids,
        criteria_set_id=request.criteria_set_id,
        criteria_set_name=criteria_set_name,
        results=[],
        created_at=datetime.utcnow().isoformat() + "Z",
    )
    return await db.create_evaluation(evaluation)


@app.post("/api/evaluations/{evaluation_id}/run", response_model=Evaluation)
async def run_evaluation_endpoint(
    evaluation_id: str,
    current_user: User = Depends(get_current_user),
) -> Evaluation:
    """Run an evaluation."""
    evaluation = await db.get_evaluation(evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    # Run evaluation synchronously
    result = await run_evaluation(evaluation_id)
    if not result:
        raise HTTPException(status_code=500, detail="Evaluation failed")

    return result


@app.get("/api/evaluations/{evaluation_id}/export/{format}")
async def export_evaluation(
    evaluation_id: str,
    format: str,
    current_user: User = Depends(get_current_user),
) -> StreamingResponse:
    """Export evaluation results in specified format."""
    evaluation = await db.get_evaluation(evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    # Get submissions for names
    submissions_map = {}
    for sid in evaluation.submission_ids:
        sub = await db.get_submission(sid)
        if sub:
            submissions_map[sid] = sub

    # Get criteria set for criterion names
    criteria_set = await db.get_criteria_set(evaluation.criteria_set_id)
    criteria_map = {}
    if criteria_set:
        for c in criteria_set.criteria:
            criteria_map[c.id] = c

    if format == "json":
        # JSON export
        results_list: list[dict[str, Any]] = []
        for result in evaluation.results:
            sub = submissions_map.get(result.submission_id)
            criteria_scores: list[dict[str, Any]] = []
            for cr in result.criterion_results:
                crit = criteria_map.get(cr.criterion_id)
                criteria_scores.append(
                    {
                        "criterion": crit.name if crit else cr.criterion_id,
                        "score": cr.score,
                        "narrative": cr.narrative,
                    }
                )
            result_data: dict[str, Any] = {
                "submission": sub.name if sub else result.submission_id,
                "overallScore": result.overall_score,
                "summary": result.summary,
                "criteriaScores": criteria_scores,
            }
            results_list.append(result_data)

        export_data: dict[str, Any] = {
            "evaluation": {
                "id": evaluation.id,
                "name": evaluation.name,
                "status": evaluation.status.value,
                "criteriaSet": evaluation.criteria_set_name,
                "createdAt": evaluation.created_at,
                "completedAt": evaluation.completed_at,
            },
            "results": results_list,
        }

        content = json.dumps(export_data, indent=2)
        return StreamingResponse(
            io.BytesIO(content.encode()),
            media_type="application/json",
            headers={"Content-Disposition": f'attachment; filename="{evaluation.name}.json"'},
        )

    elif format == "csv":
        # CSV export
        output = io.StringIO()
        writer = csv.writer(output)

        # Build header with all criteria
        criteria_names = [c.name for c in criteria_set.criteria] if criteria_set else []
        header = ["Rank", "Submission", "Overall Score"] + criteria_names + ["Summary"]
        writer.writerow(header)

        # Sort results by score descending
        sorted_results = sorted(evaluation.results, key=lambda r: r.overall_score, reverse=True)

        for rank, result in enumerate(sorted_results, 1):
            sub = submissions_map.get(result.submission_id)
            row = [rank, sub.name if sub else result.submission_id, result.overall_score]

            # Add criterion scores in order
            score_map = {cr.criterion_id: cr.score for cr in result.criterion_results}
            if criteria_set:
                for c in criteria_set.criteria:
                    row.append(score_map.get(c.id, ""))
            row.append(result.summary)
            writer.writerow(row)

        content = output.getvalue()
        return StreamingResponse(
            io.BytesIO(content.encode()),
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{evaluation.name}.csv"'},
        )

    else:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")


@app.delete("/api/evaluations/{evaluation_id}")
async def delete_evaluation(
    evaluation_id: str,
    current_user: User = Depends(get_current_user),
) -> dict[str, Any]:
    """Delete an evaluation and its associated traces in Prompt Tuner."""
    success = await db.delete_evaluation(evaluation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    # Delete associated traces in Prompt Tuner (graceful degradation on failure)
    traces_deleted = 0
    prompt_tuner_url = settings.ingenious_api_url or "http://localhost:8002"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{prompt_tuner_url}/api/traces/by-thread/{evaluation_id}",
                timeout=10.0,
            )
            if response.status_code == 200:
                data = response.json()
                traces_deleted = data.get("deleted_count", 0)
                logger.info(f"Deleted {traces_deleted} traces for evaluation {evaluation_id}")
            else:
                logger.warning(
                    f"Failed to delete traces for evaluation {evaluation_id}: "
                    f"status {response.status_code}"
                )
    except Exception as e:
        logger.warning(f"Could not delete traces for evaluation {evaluation_id}: {e}")

    return {"status": "deleted", "traces_deleted": traces_deleted}


# Health check
@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.host, port=settings.port)
