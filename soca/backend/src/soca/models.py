"""Pydantic models for SoCa."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EvaluationStatus(str, Enum):
    """Evaluation status enum."""

    DRAFT = "draft"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class User(BaseModel):
    """User model."""

    id: str
    email: str


class Submission(BaseModel):
    """Submission model."""

    id: str
    name: str
    description: Optional[str] = None
    file_url: str = Field(alias="fileUrl")
    file_name: str = Field(alias="fileName")
    file_type: str = Field(alias="fileType")
    file_size: int = Field(alias="fileSize")
    extracted_text: str = Field(default="", alias="extractedText")
    uploaded_at: str = Field(alias="uploadedAt")

    model_config = {"populate_by_name": True}


class Criterion(BaseModel):
    """Criterion model."""

    id: str
    name: str
    description: str
    weight: int
    max_score: int = Field(alias="maxScore")

    model_config = {"populate_by_name": True}


class CriteriaSet(BaseModel):
    """Criteria set model."""

    id: str
    name: str
    description: Optional[str] = None
    criteria: list[Criterion]
    created_at: str = Field(alias="createdAt")

    model_config = {"populate_by_name": True}


class CriterionResult(BaseModel):
    """Criterion result model."""

    criterion_id: str = Field(alias="criterionId")
    score: float
    narrative: str

    model_config = {"populate_by_name": True}


class EvaluationResult(BaseModel):
    """Evaluation result for a submission."""

    submission_id: str = Field(alias="submissionId")
    submission_name: str = Field(alias="submissionName")
    submission_author: Optional[str] = Field(default=None, alias="submissionAuthor")
    overall_score: float = Field(alias="overallScore")
    criterion_results: list[CriterionResult] = Field(alias="criterionResults")
    summary: str

    model_config = {"populate_by_name": True}


class Evaluation(BaseModel):
    """Evaluation model."""

    id: str
    name: str
    status: EvaluationStatus
    submission_ids: list[str] = Field(alias="submissionIds")
    criteria_set_id: str = Field(alias="criteriaSetId")
    criteria_set_name: Optional[str] = Field(default=None, alias="criteriaSetName")
    results: list[EvaluationResult] = Field(default_factory=list)
    created_at: str = Field(alias="createdAt")
    completed_at: Optional[str] = Field(default=None, alias="completedAt")

    model_config = {"populate_by_name": True}


# Request/Response models
class LoginRequest(BaseModel):
    """Login request."""

    email: str
    password: str


class LoginResponse(BaseModel):
    """Login response."""

    token: str
    user: User


class CreateEvaluationRequest(BaseModel):
    """Create evaluation request."""

    name: str
    submission_ids: list[str] = Field(alias="submissionIds")
    criteria_set_id: str = Field(alias="criteriaSetId")

    model_config = {"populate_by_name": True}


class CreateCriteriaSetRequest(BaseModel):
    """Create criteria set request."""

    name: str
    description: Optional[str] = None
    criteria: list[Criterion]


class UpdateSubmissionRequest(BaseModel):
    """Update submission request."""

    name: Optional[str] = None
    description: Optional[str] = None
