"""Pydantic models for Prompt Tuner."""

from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    """User model."""

    id: str
    email: str


class Revision(BaseModel):
    """Revision model."""

    id: str
    name: str
    created_at: str = Field(alias="createdAt")
    prompt_count: int = Field(alias="promptCount")

    model_config = {"populate_by_name": True}


class Prompt(BaseModel):
    """Prompt model."""

    filename: str
    description: Optional[str] = None
    content: str
    size: int
    tags: list[str]
    variables: list[str]


class AgentTrace(BaseModel):
    """Agent trace model."""

    agent_name: str = Field(alias="agentName")
    order: int
    input: str
    output: str
    token_usage: int = Field(alias="tokenUsage")
    system_prompt: str = Field(default="", alias="systemPrompt")
    user_prompt: str = Field(default="", alias="userPrompt")

    model_config = {"populate_by_name": True}


class ConversationTrace(BaseModel):
    """Conversation trace model."""

    trace_id: str = Field(alias="traceId")
    thread_id: str = Field(alias="threadId")
    workflow: str
    revision: str
    user_query: str = Field(alias="userQuery")
    timestamp: str
    agents: list[AgentTrace]
    total_tokens: int = Field(alias="totalTokens")

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


class UpdatePromptRequest(BaseModel):
    """Update prompt request."""

    content: str


class CreateRevisionRequest(BaseModel):
    """Create revision request."""

    name: str = Field(description="Name for the new revision")
    copy_from: Optional[str] = Field(
        default=None,
        description="Optional: revision to copy prompts from",
        alias="copyFrom",
    )

    model_config = {"populate_by_name": True}


class ChatRequest(BaseModel):
    """Chat request for AI agent invocation."""

    user_prompt: str
    thread_id: str
    conversation_flow: str = "soca-evaluator"
    topic: Optional[list[str]] = None


class ChatResponseModel(BaseModel):
    """Chat response from AI agent."""

    thread_id: str
    message_id: str
    agent_response: str
    token_count: int = 0
    memory_summary: Optional[str] = None


# =============================================================================
# INTERMEDIATE SCHEMAS FOR 6-AGENT PIPELINE
# =============================================================================


class SubmissionAnalysisSchema(BaseModel):
    """Output schema for Submission Evaluator agent."""

    main_claims: list[str] = Field(description="Key claims/arguments identified")
    evidence: list[str] = Field(description="Supporting evidence/data points")
    structure_summary: str = Field(description="How the submission is organized")
    strengths: list[str] = Field(description="Identified strengths")
    gaps: list[str] = Field(description="Areas lacking clarity or evidence")
    word_count: int = Field(description="Approximate word count")
    key_topics: list[str] = Field(description="Main topics covered")


class ScoringRubricSchema(BaseModel):
    """Scoring rubric for a single criterion."""

    criterionId: str = Field(description="Original criterion ID")
    name: str = Field(description="Criterion name")
    weight: int = Field(description="Criterion weight")
    maxScore: int = Field(description="Maximum possible score")
    scoring_rubric: dict[str, str] = Field(description="Score levels to descriptions")
    key_indicators: list[str] = Field(description="Things to look for")
    pitfalls: list[str] = Field(description="Issues that lower scores")
    excellence_markers: list[str] = Field(description="Things indicating excellence")


class CriteriaAnalysisSchema(BaseModel):
    """Output schema for Criteria Evaluator agent."""

    criteria_analysis: list[ScoringRubricSchema] = Field(description="Analysis for each criterion")


class ImprovementSchema(BaseModel):
    """Single improvement recommendation."""

    area: str = Field(description="What aspect needs improvement")
    current_state: str = Field(description="Brief description of current state")
    recommended_action: str = Field(description="Specific action to take")
    expected_impact: str = Field(description="How this will improve the submission")


class NextStepsAnalysisSchema(BaseModel):
    """Output schema for Next Steps agent."""

    priority_improvements: list[ImprovementSchema] = Field(
        description="Top 3-5 most impactful improvements"
    )
    quick_wins: list[str] = Field(description="Small changes with immediate impact")
    long_term_enhancements: list[str] = Field(description="Substantial future improvements")
    overall_direction: str = Field(description="Overall direction for improvement")


class CriterionScoreSchema(BaseModel):
    """Individual criterion score from Scoring Agent."""

    criterionId: str = Field(description="Criterion ID")
    score: int = Field(description="Score from 1 to maxScore")
    narrative: str = Field(description="Justification referencing evidence")
    confidence: str = Field(description="high, medium, or low")


class ScoringOutputSchema(BaseModel):
    """Output schema for Scoring Agent."""

    criterion_scores: list[CriterionScoreSchema] = Field(description="Scores for each criterion")


class SummaryOutputSchema(BaseModel):
    """Output schema for Summarizer Agent."""

    executive_summary: str = Field(description="High-level summary")
    key_strengths: list[str] = Field(description="Top 2-3 strengths")
    key_improvements: list[str] = Field(description="Top 2-3 improvements")
    overall_narrative: str = Field(description="Comprehensive narrative")
    overallScore: float = Field(description="Weighted percentage 0-100")
    score_breakdown: str = Field(description="How score was calculated")


class ValidationCheckSchema(BaseModel):
    """Individual validation check result."""

    name: str = Field(description="Check name")
    passed: bool = Field(description="Whether check passed")


class ValidationIssueSchema(BaseModel):
    """Validation issue found by Sanity Check Agent."""

    check_name: str = Field(description="Which check failed")
    description: str = Field(description="What's wrong")
    severity: str = Field(description="error or warning")
    suggested_fix: Optional[str] = Field(default=None, description="How to correct it")


class FinalOutputSchema(BaseModel):
    """Final validated output from Sanity Check Agent."""

    overallScore: float = Field(description="Validated overall score")
    narrative: str = Field(description="Validated overall narrative")
    criterionResults: list["CriterionResultSchema"] = Field(
        description="Validated criterion scores"
    )
    nextSteps: list[str] = Field(description="Improvement recommendations")


class SanityCheckOutputSchema(BaseModel):
    """Output schema for Sanity Check Agent."""

    validation_status: str = Field(description="passed or flagged")
    checks_performed: list[ValidationCheckSchema] = Field(description="Check results")
    issues_found: list[ValidationIssueSchema] = Field(description="Issues found")
    final_output: FinalOutputSchema = Field(description="Validated final result")


class AgentContribution(BaseModel):
    """Tracks an individual agent's contribution to the evaluation."""

    agent_name: str = Field(description="Name of the agent")
    phase: int = Field(description="Pipeline phase (1-4)")
    input_summary: str = Field(description="Summary of input received")
    output_summary: str = Field(description="Summary of output produced")
    token_count: int = Field(description="Tokens used by this agent")
    execution_time_ms: int = Field(default=0, description="Execution time in milliseconds")


# =============================================================================
# EVALUATION RESULT SCHEMAS
# =============================================================================


# Structured output models for AI evaluation (enforced JSON schema)
class CriterionResultSchema(BaseModel):
    """Individual criterion evaluation result with enforced schema."""

    criterionId: str = Field(description="The unique identifier of the criterion being evaluated")
    score: float = Field(description="The score given for this criterion (1 to max_score)")
    narrative: str = Field(description="A 1-2 sentence justification for the score")


class EvaluationResponseSchema(BaseModel):
    """Evaluation response schema enforced by structured outputs."""

    criterionResults: list[CriterionResultSchema] = Field(
        description="List of evaluation results for each criterion"
    )
    overallScore: float = Field(description="Weighted average score from 0-100")
    summary: str = Field(description="A 2-3 sentence summary of the overall evaluation")
    nextSteps: list[str] = Field(
        default_factory=list,
        description="Actionable improvement recommendations from the evaluation",
    )
    agentContributions: list[AgentContribution] = Field(
        default_factory=list, description="Details of each agent's contribution to the evaluation"
    )
    validationStatus: str = Field(
        default="passed", description="Sanity check validation status: passed or flagged"
    )


# Structured output models for criteria generation
class GeneratedCriterionSchema(BaseModel):
    """Individual criterion generated from document analysis."""

    id: str = Field(description="Unique identifier in format 'criterion-N'")
    name: str = Field(description="Short name for the criterion (2-5 words)")
    description: str = Field(description="Evaluation guidance (1-2 sentences)")
    weight: int = Field(ge=0, le=100, description="Weight as percentage (0-100)")
    maxScore: int = Field(description="Maximum score for this criterion (5 or 10)")


class CriteriaGenerationResponseSchema(BaseModel):
    """Response schema for criteria generation from document analysis."""

    name: str = Field(description="Descriptive name for the criteria set")
    description: str = Field(
        default="Auto-generated criteria based on document analysis",
        description="Brief description of the criteria set",
    )
    criteria: list[GeneratedCriterionSchema] = Field(
        description="List of extracted evaluation criteria (3-7 items)"
    )
