"""SoCa FastAPI application."""

import csv
import io
import json
import uuid
from datetime import datetime
from typing import Any, Optional

from fastapi import BackgroundTasks, Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from soca.auth import authenticate_user, create_access_token, get_current_user
from soca.config import settings
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
    return await db.list_submissions()


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

    # Extract text (simplified - in production, use PDF parser, etc.)
    extracted_text = ""
    if file.content_type == "text/plain":
        extracted_text = content.decode("utf-8", errors="ignore")
    elif file.content_type == "text/markdown":
        extracted_text = content.decode("utf-8", errors="ignore")

    # For demo, store file URL as placeholder
    # In production, upload to Azure Blob Storage
    file_url = f"/files/{uuid.uuid4()}/{file.filename}"

    submission = Submission(
        id=str(uuid.uuid4()),
        name=name or file.filename or "Untitled",
        description=description,
        fileUrl=file_url,
        fileName=file.filename or "file",
        fileType=file.content_type or "application/octet-stream",
        fileSize=file_size,
        extractedText=extracted_text[:10000],  # Limit text size
        uploadedAt=datetime.utcnow().isoformat() + "Z",
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
        description=request.description if request.description is not None else existing.description,
        fileUrl=existing.file_url,
        fileName=existing.file_name,
        fileType=existing.file_type,
        fileSize=existing.file_size,
        extractedText=existing.extracted_text,
        uploadedAt=existing.uploaded_at,
    )
    return await db.update_submission(updated)


# Criteria endpoints
@app.get("/api/criteria-sets", response_model=list[CriteriaSet])
async def list_criteria_sets(current_user: User = Depends(get_current_user)) -> list[CriteriaSet]:
    """List all criteria sets."""
    return await db.list_criteria_sets()


@app.get("/api/criteria-templates", response_model=list[CriteriaSet])
async def list_criteria_templates(
    current_user: User = Depends(get_current_user),
) -> list[CriteriaSet]:
    """List available criteria templates."""
    return get_templates()


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
        createdAt=datetime.utcnow().isoformat() + "Z",
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
        createdAt=existing.createdAt,
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


# Evaluations endpoints
@app.get("/api/evaluations", response_model=list[Evaluation])
async def list_evaluations(current_user: User = Depends(get_current_user)) -> list[Evaluation]:
    """List all evaluations."""
    return await db.list_evaluations()


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
        submissionIds=request.submission_ids,
        criteriaSetId=request.criteria_set_id,
        criteriaSetName=criteria_set_name,
        results=[],
        createdAt=datetime.utcnow().isoformat() + "Z",
    )
    return await db.create_evaluation(evaluation)


@app.post("/api/evaluations/{evaluation_id}/run", response_model=Evaluation)
async def run_evaluation_endpoint(
    evaluation_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
) -> Evaluation:
    """Run an evaluation."""
    evaluation = await db.get_evaluation(evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    # Run evaluation (in demo mode, run synchronously for simplicity)
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
        export_data = {
            "evaluation": {
                "id": evaluation.id,
                "name": evaluation.name,
                "status": evaluation.status.value,
                "criteriaSet": evaluation.criteria_set_name,
                "createdAt": evaluation.created_at,
                "completedAt": evaluation.completed_at,
            },
            "results": [],
        }
        for result in evaluation.results:
            sub = submissions_map.get(result.submission_id)
            result_data = {
                "submission": sub.name if sub else result.submission_id,
                "overallScore": result.overall_score,
                "summary": result.summary,
                "criteriaScores": [],
            }
            for cr in result.criterion_results:
                crit = criteria_map.get(cr.criterion_id)
                result_data["criteriaScores"].append({
                    "criterion": crit.name if crit else cr.criterion_id,
                    "score": cr.score,
                    "narrative": cr.narrative,
                })
            export_data["results"].append(result_data)

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


# Health check
@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.host, port=settings.port)  # type: ignore[arg-type]
