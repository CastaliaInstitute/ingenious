"""Prompts module for managing AI agent prompts."""

from ingen_prompt_tuner.models import Prompt, Revision

# Default system prompt for SoCa evaluations (configurable via UI)
DEFAULT_EVALUATION_SYSTEM_PROMPT = """You are an expert document evaluator. You evaluate submissions against specific criteria.

Rules:
1. Each criterion score must be between 1 and the max score specified
2. Overall score must be the weighted average (0-100)
3. Narratives should be 1-2 sentences each
4. Be objective and fair in your assessment
5. Use the exact criterionId values provided in the request"""

# Default system prompt for criteria generation from documents
DEFAULT_CRITERIA_GENERATOR_SYSTEM_PROMPT = """You are an expert document analyst specializing in extracting evaluation criteria from unstructured documents.

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


# In-memory revision storage
_revisions: dict[str, Revision] = {
    "active": Revision(
        id="active",
        name="active",
        created_at="2024-01-15T10:00:00Z",
        prompt_count=2,
    ),
}


def get_revisions() -> list[Revision]:
    """Get all revisions."""
    return list(_revisions.values())


def _get_base_prompts() -> list[Prompt]:
    """Get base prompt templates for SoCa."""
    return [
        Prompt(
            filename="soca_evaluator_system.md",
            description="System prompt for SoCa document evaluation agent",
            content=DEFAULT_EVALUATION_SYSTEM_PROMPT,
            size=len(DEFAULT_EVALUATION_SYSTEM_PROMPT),
            tags=["system", "soca", "evaluation"],
            variables=[],
        ),
        Prompt(
            filename="criteria_generator_system.md",
            description="System prompt for extracting evaluation criteria from documents",
            content=DEFAULT_CRITERIA_GENERATOR_SYSTEM_PROMPT,
            size=len(DEFAULT_CRITERIA_GENERATOR_SYSTEM_PROMPT),
            tags=["system", "criteria", "generator"],
            variables=[],
        ),
    ]


# In-memory storage for edited prompts
_edited_prompts: dict[str, dict[str, str]] = {}


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


def get_evaluation_system_prompt(revision: str = "active") -> str:
    """Get the current evaluation system prompt for SoCa.

    This is used by the chat endpoint to get the configurable system prompt.
    """
    prompt = get_prompt(revision, "soca_evaluator_system.md")
    if prompt:
        return prompt.content
    return DEFAULT_EVALUATION_SYSTEM_PROMPT


def get_criteria_generator_system_prompt(revision: str = "active") -> str:
    """Get the current criteria generator system prompt.

    This is used by the chat endpoint to get the configurable system prompt
    for criteria generation from documents.
    """
    prompt = get_prompt(revision, "criteria_generator_system.md")
    if prompt:
        return prompt.content
    return DEFAULT_CRITERIA_GENERATOR_SYSTEM_PROMPT
