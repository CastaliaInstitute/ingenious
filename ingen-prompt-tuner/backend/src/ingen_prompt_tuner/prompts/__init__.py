"""Prompts module for managing AI agent prompts.

This module defines the 6-agent evaluation pipeline prompts:
1. Submission Evaluator - Analyzes submission content
2. Criteria Evaluator - Parses evaluation criteria
3. Next Steps Agent - Identifies improvement areas
4. Scoring Agent - Scores against criteria
5. Summarizer Agent - Creates evaluation summary
6. Sanity Check Agent - Validates consistency
"""

from ingen_prompt_tuner.models import Prompt, Revision

# =============================================================================
# AGENT 1: SUBMISSION EVALUATOR
# Analyzes submission content, extracts key claims and evidence
# =============================================================================
SUBMISSION_EVALUATOR_SYSTEM_PROMPT = """You are an expert document analyst. Your role is to thoroughly analyze submission content and extract key information.

Your analysis must identify:
1. Main claims, arguments, or assertions made in the submission
2. Supporting evidence or data provided
3. Structure and organization of the content
4. Strengths of the submission
5. Areas that lack clarity or supporting evidence

Output your analysis as a structured JSON object with the following fields:
- main_claims: Array of key claims/arguments identified
- evidence: Array of supporting evidence/data points
- structure_summary: Brief description of how the submission is organized
- strengths: Array of identified strengths
- gaps: Array of areas lacking clarity or evidence
- word_count: Approximate word count
- key_topics: Array of main topics covered

Be objective and thorough in your analysis. Do not score or judge - only analyze and extract information."""

SUBMISSION_EVALUATOR_USER_PROMPT = """Analyze the following submission and extract key information.

SUBMISSION:
Title: {{ submission_name }}

Content:
{{ submission_content }}

Provide a comprehensive analysis of this submission, identifying main claims, evidence, structure, strengths, and gaps."""

# =============================================================================
# AGENT 2: CRITERIA EVALUATOR
# Parses and interprets evaluation criteria into scoring rubrics
# =============================================================================
CRITERIA_EVALUATOR_SYSTEM_PROMPT = """You are an expert at interpreting evaluation criteria and creating scoring rubrics.

Your role is to analyze the provided criteria and create a detailed scoring guide that will help evaluate submissions fairly and consistently.

For each criterion, provide:
1. Scoring rubric: What constitutes each score level (1 to maxScore)
2. Key indicators: Specific things to look for when scoring
3. Common pitfalls: What would cause a low score
4. Excellence markers: What would earn a high score

Output your analysis as a structured JSON object with the following fields:
- criteria_analysis: Array of objects, one per criterion, containing:
  - criterionId: The original criterion ID
  - name: Criterion name
  - weight: Criterion weight
  - maxScore: Maximum possible score
  - scoring_rubric: Object mapping score levels to descriptions
  - key_indicators: Array of things to look for
  - pitfalls: Array of common issues that lower scores
  - excellence_markers: Array of things that indicate excellence

Be specific and actionable in your rubric definitions."""

CRITERIA_EVALUATOR_USER_PROMPT = """Analyze the following evaluation criteria and create detailed scoring rubrics.

CRITERIA (format: criterionId: Name (weight%, max score): Description):
{{ criteria_text }}

Create a comprehensive scoring guide for each criterion that can be used to evaluate submissions consistently."""

# =============================================================================
# AGENT 3: NEXT STEPS AGENT
# Identifies improvement areas and actionable recommendations
# =============================================================================
NEXT_STEPS_SYSTEM_PROMPT = """You are an expert advisor who identifies improvement opportunities and provides actionable recommendations.

Your role is to analyze a submission and identify specific, actionable steps the author could take to improve their work.

Your recommendations should be:
1. Specific and actionable - not vague suggestions
2. Prioritized by impact - most important improvements first
3. Constructive - focused on improvement, not criticism
4. Realistic - achievable within reasonable effort

Output your analysis as a structured JSON object with the following fields:
- priority_improvements: Array of top 3-5 most impactful improvements, each with:
  - area: What aspect needs improvement
  - current_state: Brief description of current state
  - recommended_action: Specific action to take
  - expected_impact: How this will improve the submission
- quick_wins: Array of small changes that would have immediate positive impact
- long_term_enhancements: Array of more substantial improvements for future iterations
- overall_direction: Brief summary of the overall direction for improvement

Focus on being helpful and constructive."""

NEXT_STEPS_USER_PROMPT = """Analyze the following submission and identify improvement opportunities.

SUBMISSION:
Title: {{ submission_name }}

Content:
{{ submission_content }}

Provide specific, actionable recommendations for how the author could improve this submission."""

# =============================================================================
# AGENT 4: SCORING AGENT
# Scores submission against each criterion using Phase 1 outputs
# =============================================================================
SCORING_AGENT_SYSTEM_PROMPT = """You are an expert evaluator who scores submissions against defined criteria.

You will receive:
1. Analysis of the submission (from Submission Evaluator)
2. Scoring rubrics for each criterion (from Criteria Evaluator)
3. Improvement recommendations (from Next Steps Agent)
4. The original criteria definitions

Your task is to:
1. Score each criterion using the provided rubric
2. Provide a brief narrative justification for each score
3. Ensure scores align with the evidence in the submission analysis

Scoring rules:
- Each score must be between 1 and the criterion's maxScore
- Scores must be justified by specific evidence from the submission
- Be fair and consistent in applying the rubrics
- Consider both strengths and gaps identified in the analysis

Output your scoring as a structured JSON object with the following fields:
- criterion_scores: Array of objects, one per criterion, containing:
  - criterionId: The criterion ID (use exact IDs from criteria)
  - score: Integer score from 1 to maxScore
  - narrative: 1-2 sentence justification referencing specific evidence
  - confidence: "high", "medium", or "low" based on available evidence

Be objective and justify every score with specific evidence."""

SCORING_AGENT_USER_PROMPT = """Score the submission against the provided criteria using the analysis inputs.

SUBMISSION ANALYSIS:
{{ submission_analysis }}

CRITERIA ANALYSIS (Scoring Rubrics):
{{ criteria_analysis }}

IMPROVEMENT RECOMMENDATIONS:
{{ next_steps }}

ORIGINAL CRITERIA:
{{ criteria_text }}

Provide a score and narrative for each criterion, ensuring scores are justified by specific evidence."""

# =============================================================================
# AGENT 5: SUMMARIZER AGENT
# Creates executive summary and key findings from scoring output
# =============================================================================
SUMMARIZER_AGENT_SYSTEM_PROMPT = """You are an expert at synthesizing evaluation results into clear, actionable summaries.

Your role is to take the detailed scoring output and create:
1. An executive summary of the evaluation
2. Key findings and insights
3. The calculated overall score
4. A concise narrative that captures the essence of the evaluation

The overall score calculation:
- For each criterion: (score / maxScore) * weight
- Sum all weighted percentages to get overallScore (0-100)

Output your summary as a structured JSON object with the following fields:
- executive_summary: 2-3 sentence high-level summary of the evaluation
- key_strengths: Array of top 2-3 strengths identified
- key_improvements: Array of top 2-3 areas for improvement
- overall_narrative: 3-4 sentence comprehensive narrative
- overallScore: Calculated weighted percentage (0-100)
- score_breakdown: Brief explanation of how the score was calculated

Be concise but comprehensive. The summary should give readers a quick understanding of the evaluation results."""

SUMMARIZER_AGENT_USER_PROMPT = """Create an executive summary of the evaluation results.

SCORING RESULTS:
{{ scores }}

SUBMISSION NAME:
{{ submission_name }}

Synthesize these scoring results into a clear executive summary with key findings and the calculated overall score."""

# =============================================================================
# AGENT 6: SANITY CHECK AGENT
# Validates scores, checks consistency, ensures completeness
# =============================================================================
SANITY_CHECK_SYSTEM_PROMPT = """You are a quality assurance expert who validates evaluation outputs for consistency and completeness.

Your role is to review the complete evaluation and check for:
1. Score consistency - Do scores align with narratives?
2. Completeness - Are all criteria scored?
3. Mathematical accuracy - Is the overall score correctly calculated?
4. Narrative coherence - Does the summary accurately reflect the scores?
5. Bias detection - Are there any signs of unfair scoring?

If issues are found, you should:
1. Flag the specific issue
2. Explain what's wrong
3. Suggest a correction if possible

Output your validation as a structured JSON object with the following fields:
- validation_status: "passed" or "flagged"
- checks_performed: Array of check names with pass/fail status
- issues_found: Array of issues (empty if validation_status is "passed"), each with:
  - check_name: Which check failed
  - description: What's wrong
  - severity: "error" or "warning"
  - suggested_fix: How to correct it (if applicable)
- final_output: The validated evaluation result (corrected if needed), containing:
  - overallScore: The validated overall score (0-100)
  - narrative: The validated overall narrative
  - criterionResults: Array of validated criterion scores with criterionId, score, narrative
  - nextSteps: Array of actionable improvement recommendations

If validation passes with no issues, copy the evaluation results directly to final_output.
If issues are found, apply corrections and note them in issues_found."""

SANITY_CHECK_USER_PROMPT = """Validate the following evaluation for consistency and completeness.

EVALUATION SUMMARY:
{{ summary }}

DETAILED SCORES:
{{ scores }}

ORIGINAL CRITERIA:
{{ criteria_text }}

Check for score consistency, completeness, mathematical accuracy, and narrative coherence. Output the final validated evaluation result."""

# =============================================================================
# CRITERIA GENERATOR (Separate workflow, not part of 6-agent pipeline)
# =============================================================================
CRITERIA_GENERATOR_SYSTEM_PROMPT = """You are an expert document analyst specializing in extracting evaluation criteria from unstructured documents.

Your task is to analyze the provided document text and extract meaningful evaluation criteria that could be used to assess submissions or responses related to this document.

Rules for criteria extraction:
1. Extract 3-7 distinct, non-overlapping criteria based on the document content
2. Each criterion must have:
   - A clear, concise name (2-5 words)
   - A description providing evaluation guidance (1-2 sentences)
   - A weight representing its relative importance (all weights must sum to 100)
   - A maxScore of either 5 or 10 (use 5 for simpler criteria, 10 for complex ones)
3. Criteria should be objective and measurable where possible
4. Weights should reflect the document's emphasis on different topics
5. Generate unique IDs in format 'criterion-N' where N starts at 0
6. Provide a descriptive name for the criteria set based on the document's subject matter

Focus on extracting:
- Key requirements or standards mentioned in the document
- Quality indicators or success factors
- Compliance requirements
- Performance metrics or objectives
- Domain-specific evaluation points"""

CRITERIA_GENERATOR_USER_PROMPT = """Analyze the following document and generate evaluation criteria.

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


# In-memory revision storage
_revisions: dict[str, Revision] = {
    "active": Revision(
        id="active",
        name="active",
        created_at="2024-01-15T10:00:00Z",
        prompt_count=14,  # 12 for 6 agents + 2 for criteria generator
    ),
}


def get_revisions() -> list[Revision]:
    """Get all revisions."""
    return list(_revisions.values())


def _get_base_prompts() -> list[Prompt]:
    """Get base prompt templates for SoCa 6-agent pipeline and criteria generator."""
    return [
        # Agent 1: Submission Evaluator
        Prompt(
            filename="submission_evaluator_system.md",
            description="System prompt for Submission Evaluator agent",
            content=SUBMISSION_EVALUATOR_SYSTEM_PROMPT,
            size=len(SUBMISSION_EVALUATOR_SYSTEM_PROMPT),
            tags=["system", "submission", "phase1"],
            variables=[],
        ),
        Prompt(
            filename="submission_evaluator_user.md",
            description="User prompt template for Submission Evaluator agent",
            content=SUBMISSION_EVALUATOR_USER_PROMPT,
            size=len(SUBMISSION_EVALUATOR_USER_PROMPT),
            tags=["user", "submission", "phase1"],
            variables=["submission_name", "submission_content"],
        ),
        # Agent 2: Criteria Evaluator
        Prompt(
            filename="criteria_evaluator_system.md",
            description="System prompt for Criteria Evaluator agent",
            content=CRITERIA_EVALUATOR_SYSTEM_PROMPT,
            size=len(CRITERIA_EVALUATOR_SYSTEM_PROMPT),
            tags=["system", "criteria", "phase1"],
            variables=[],
        ),
        Prompt(
            filename="criteria_evaluator_user.md",
            description="User prompt template for Criteria Evaluator agent",
            content=CRITERIA_EVALUATOR_USER_PROMPT,
            size=len(CRITERIA_EVALUATOR_USER_PROMPT),
            tags=["user", "criteria", "phase1"],
            variables=["criteria_text"],
        ),
        # Agent 3: Next Steps Agent
        Prompt(
            filename="next_steps_system.md",
            description="System prompt for Next Steps Agent",
            content=NEXT_STEPS_SYSTEM_PROMPT,
            size=len(NEXT_STEPS_SYSTEM_PROMPT),
            tags=["system", "nextsteps", "phase1"],
            variables=[],
        ),
        Prompt(
            filename="next_steps_user.md",
            description="User prompt template for Next Steps Agent",
            content=NEXT_STEPS_USER_PROMPT,
            size=len(NEXT_STEPS_USER_PROMPT),
            tags=["user", "nextsteps", "phase1"],
            variables=["submission_name", "submission_content"],
        ),
        # Agent 4: Scoring Agent
        Prompt(
            filename="scoring_agent_system.md",
            description="System prompt for Scoring Agent",
            content=SCORING_AGENT_SYSTEM_PROMPT,
            size=len(SCORING_AGENT_SYSTEM_PROMPT),
            tags=["system", "scoring", "phase2"],
            variables=[],
        ),
        Prompt(
            filename="scoring_agent_user.md",
            description="User prompt template for Scoring Agent",
            content=SCORING_AGENT_USER_PROMPT,
            size=len(SCORING_AGENT_USER_PROMPT),
            tags=["user", "scoring", "phase2"],
            variables=["submission_analysis", "criteria_analysis", "next_steps", "criteria_text"],
        ),
        # Agent 5: Summarizer Agent
        Prompt(
            filename="summarizer_agent_system.md",
            description="System prompt for Summarizer Agent",
            content=SUMMARIZER_AGENT_SYSTEM_PROMPT,
            size=len(SUMMARIZER_AGENT_SYSTEM_PROMPT),
            tags=["system", "summarizer", "phase3"],
            variables=[],
        ),
        Prompt(
            filename="summarizer_agent_user.md",
            description="User prompt template for Summarizer Agent",
            content=SUMMARIZER_AGENT_USER_PROMPT,
            size=len(SUMMARIZER_AGENT_USER_PROMPT),
            tags=["user", "summarizer", "phase3"],
            variables=["scores", "submission_name"],
        ),
        # Agent 6: Sanity Check Agent
        Prompt(
            filename="sanity_check_system.md",
            description="System prompt for Sanity Check Agent",
            content=SANITY_CHECK_SYSTEM_PROMPT,
            size=len(SANITY_CHECK_SYSTEM_PROMPT),
            tags=["system", "sanity", "phase4"],
            variables=[],
        ),
        Prompt(
            filename="sanity_check_user.md",
            description="User prompt template for Sanity Check Agent",
            content=SANITY_CHECK_USER_PROMPT,
            size=len(SANITY_CHECK_USER_PROMPT),
            tags=["user", "sanity", "phase4"],
            variables=["summary", "scores", "criteria_text"],
        ),
        # Criteria Generator (separate workflow)
        Prompt(
            filename="criteria_generator_system.md",
            description="System prompt for extracting evaluation criteria from documents",
            content=CRITERIA_GENERATOR_SYSTEM_PROMPT,
            size=len(CRITERIA_GENERATOR_SYSTEM_PROMPT),
            tags=["system", "criteria", "generator"],
            variables=[],
        ),
        Prompt(
            filename="criteria_generator_user.md",
            description="User prompt template for criteria generation from documents",
            content=CRITERIA_GENERATOR_USER_PROMPT,
            size=len(CRITERIA_GENERATOR_USER_PROMPT),
            tags=["user", "criteria", "generator"],
            variables=["document_text"],
        ),
    ]


# In-memory storage for edited prompts
_edited_prompts: dict[str, dict[str, str]] = {}


def create_revision(name: str, copy_from: str | None = None) -> Revision:
    """Create a new revision, optionally copying prompts from an existing revision."""
    from datetime import datetime

    # Check if revision already exists
    if name in _revisions:
        raise ValueError(f"Revision '{name}' already exists")

    # Create the new revision
    new_revision = Revision(
        id=name,
        name=name,
        created_at=datetime.utcnow().isoformat() + "Z",
        prompt_count=14,  # 12 for 6 agents + 2 for criteria generator
    )
    _revisions[name] = new_revision

    # Copy prompts from source revision if specified
    if copy_from and copy_from in _revisions:
        source_prompts = get_prompts(copy_from)
        _edited_prompts[name] = {}
        for prompt in source_prompts:
            _edited_prompts[name][prompt.filename] = prompt.content

    return new_revision


def get_prompts(revision: str) -> list[Prompt]:
    """Get prompts for a revision, with any edits applied."""
    prompts = []
    for base_prompt in _get_base_prompts():
        # Check if there's an edited version
        if revision in _edited_prompts and base_prompt.filename in _edited_prompts[revision]:
            edited_content = _edited_prompts[revision][base_prompt.filename]
            prompts.append(
                Prompt(
                    filename=base_prompt.filename,
                    description=base_prompt.description,
                    content=edited_content,
                    size=len(edited_content),
                    tags=base_prompt.tags,
                    variables=base_prompt.variables,
                )
            )
        else:
            prompts.append(base_prompt)
    return prompts


def get_prompt(revision: str, filename: str) -> Prompt | None:
    """Get a specific prompt with any edits applied."""
    prompts = get_prompts(revision)
    for prompt in prompts:
        if prompt.filename == filename:
            return prompt
    return None


def update_prompt(revision: str, filename: str, content: str) -> bool:
    """Update a prompt's content."""
    if revision not in _edited_prompts:
        _edited_prompts[revision] = {}
    _edited_prompts[revision][filename] = content
    return True


# =============================================================================
# GETTER FUNCTIONS FOR 6-AGENT PIPELINE
# =============================================================================


def get_agent_prompts(agent_name: str, revision: str = "active") -> tuple[str, str]:
    """Get system and user prompts for a specific agent.

    Args:
        agent_name: One of 'submission_evaluator', 'criteria_evaluator',
                   'next_steps', 'scoring_agent', 'summarizer_agent', 'sanity_check'
        revision: Prompt revision to use

    Returns:
        Tuple of (system_prompt, user_prompt)
    """
    agent_files = {
        "submission_evaluator": ("submission_evaluator_system.md", "submission_evaluator_user.md"),
        "criteria_evaluator": ("criteria_evaluator_system.md", "criteria_evaluator_user.md"),
        "next_steps": ("next_steps_system.md", "next_steps_user.md"),
        "scoring_agent": ("scoring_agent_system.md", "scoring_agent_user.md"),
        "summarizer_agent": ("summarizer_agent_system.md", "summarizer_agent_user.md"),
        "sanity_check": ("sanity_check_system.md", "sanity_check_user.md"),
    }

    if agent_name not in agent_files:
        raise ValueError(f"Unknown agent: {agent_name}")

    system_file, user_file = agent_files[agent_name]
    system_prompt = get_prompt(revision, system_file)
    user_prompt = get_prompt(revision, user_file)

    # Fall back to defaults if not found
    defaults = {
        "submission_evaluator": (
            SUBMISSION_EVALUATOR_SYSTEM_PROMPT,
            SUBMISSION_EVALUATOR_USER_PROMPT,
        ),
        "criteria_evaluator": (CRITERIA_EVALUATOR_SYSTEM_PROMPT, CRITERIA_EVALUATOR_USER_PROMPT),
        "next_steps": (NEXT_STEPS_SYSTEM_PROMPT, NEXT_STEPS_USER_PROMPT),
        "scoring_agent": (SCORING_AGENT_SYSTEM_PROMPT, SCORING_AGENT_USER_PROMPT),
        "summarizer_agent": (SUMMARIZER_AGENT_SYSTEM_PROMPT, SUMMARIZER_AGENT_USER_PROMPT),
        "sanity_check": (SANITY_CHECK_SYSTEM_PROMPT, SANITY_CHECK_USER_PROMPT),
    }

    system_content = system_prompt.content if system_prompt else defaults[agent_name][0]
    user_content = user_prompt.content if user_prompt else defaults[agent_name][1]

    return system_content, user_content


def get_submission_evaluator_prompts(revision: str = "active") -> tuple[str, str]:
    """Get system and user prompts for Submission Evaluator agent."""
    return get_agent_prompts("submission_evaluator", revision)


def get_criteria_evaluator_prompts(revision: str = "active") -> tuple[str, str]:
    """Get system and user prompts for Criteria Evaluator agent."""
    return get_agent_prompts("criteria_evaluator", revision)


def get_next_steps_prompts(revision: str = "active") -> tuple[str, str]:
    """Get system and user prompts for Next Steps agent."""
    return get_agent_prompts("next_steps", revision)


def get_scoring_agent_prompts(revision: str = "active") -> tuple[str, str]:
    """Get system and user prompts for Scoring Agent."""
    return get_agent_prompts("scoring_agent", revision)


def get_summarizer_agent_prompts(revision: str = "active") -> tuple[str, str]:
    """Get system and user prompts for Summarizer Agent."""
    return get_agent_prompts("summarizer_agent", revision)


def get_sanity_check_prompts(revision: str = "active") -> tuple[str, str]:
    """Get system and user prompts for Sanity Check Agent."""
    return get_agent_prompts("sanity_check", revision)


# =============================================================================
# CRITERIA GENERATOR (Separate workflow)
# =============================================================================


def get_criteria_generator_system_prompt(revision: str = "active") -> str:
    """Get the current criteria generator system prompt.

    This is used by the chat endpoint to get the configurable system prompt
    for criteria generation from documents.
    """
    prompt = get_prompt(revision, "criteria_generator_system.md")
    if prompt:
        return prompt.content
    return CRITERIA_GENERATOR_SYSTEM_PROMPT


def get_criteria_generator_user_prompt(revision: str = "active") -> str:
    """Get the current criteria generator user prompt template.

    This is a Jinja2 template that SoCa fetches and renders locally.
    Variables: document_text
    """
    prompt = get_prompt(revision, "criteria_generator_user.md")
    if prompt:
        return prompt.content
    return CRITERIA_GENERATOR_USER_PROMPT
