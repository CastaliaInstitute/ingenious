"""SoCa evaluator conversation flow implementation with 6-agent pipeline.

This module provides a conversation flow for evaluating submissions against
criteria using a multi-agent pipeline:

Phase 1 (Parallel):
  - Submission Evaluator: Analyzes submission content
  - Criteria Evaluator: Parses criteria into rubrics
  - Next Steps Agent: Identifies improvement areas

Phase 2 (Sequential):
  - Scoring Agent: Scores against criteria using Phase 1 outputs

Phase 3 (Sequential):
  - Summarizer Agent: Creates executive summary

Phase 4 (Sequential):
  - Sanity Check Agent: Validates consistency and completeness
"""

import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import EVENT_LOGGER_NAME, CancellationToken
from jinja2 import Template

import ingenious.config.config as config
from ingen_prompt_tuner.models import (
    AgentContribution,
    CriterionResultSchema,
    EvaluationResponseSchema,
)
from ingen_prompt_tuner.prompts import (
    get_criteria_evaluator_prompts,
    get_next_steps_prompts,
    get_sanity_check_prompts,
    get_scoring_agent_prompts,
    get_submission_evaluator_prompts,
    get_summarizer_agent_prompts,
)
from ingenious.client.azure.builder.openai_chat_completions_client import (
    AzureOpenAIChatCompletionClientBuilder,
)
from ingenious.models.agent import LLMUsageTracker
from ingenious.models.chat import ChatRequest


@dataclass
class EvaluationContext:
    """Context data for evaluation pipeline."""

    submission_name: str
    submission_content: str
    criteria_text: str
    revision: str
    model_client: Any
    cancellation_token: CancellationToken


@dataclass
class AgentResult:
    """Result from a single agent execution."""

    output: str
    tokens: int
    agent_name: str
    display_name: str
    system_prompt: str
    user_prompt: str
    execution_time_ms: int


@dataclass
class PipelineState:
    """Mutable state for the evaluation pipeline."""

    total_tokens: int = 0
    agent_contributions: list[AgentContribution] = field(default_factory=list)
    agents_trace_data: list[dict[str, Any]] = field(default_factory=list)


def _clean_json_response(text: str) -> str:
    """Clean markdown formatting from JSON response."""
    clean = text.strip()
    if clean.startswith("```json"):
        clean = clean[7:]
    if clean.startswith("```"):
        clean = clean[3:]
    if clean.endswith("```"):
        clean = clean[:-3]
    return clean.strip()


def _render_template(template_str: str, variables: dict[str, Any]) -> str:
    """Render a Jinja2 template with variables."""
    template = Template(template_str)
    return template.render(**variables)


def _truncate_output(output: str, max_len: int = 200) -> str:
    """Truncate output for summary display."""
    return output[:max_len] + "..." if len(output) > max_len else output


async def _run_agent(
    agent_name: str,
    system_prompt: str,
    user_prompt: str,
    model_client: Any,
    cancellation_token: CancellationToken,
) -> tuple[str, int]:
    """Run a single agent and return its response and token count."""
    agent = AssistantAgent(
        name=agent_name,
        system_message=system_prompt,
        model_client=model_client,
    )

    response = await agent.on_messages(
        messages=[TextMessage(content=user_prompt, source="user")],
        cancellation_token=cancellation_token,
    )

    chat_msg = response.chat_message
    result_text = str(chat_msg.content) if hasattr(chat_msg, "content") else "{}"

    token_count = 0
    if hasattr(chat_msg, "models_usage") and chat_msg.models_usage is not None:
        usage = chat_msg.models_usage
        token_count = getattr(usage, "prompt_tokens", 0) + getattr(usage, "completion_tokens", 0)

    return _clean_json_response(result_text), token_count


def _record_agent_result(
    state: PipelineState,
    result: AgentResult,
    phase: int,
    order: int,
    input_summary: str,
) -> None:
    """Record agent result in pipeline state."""
    state.total_tokens += result.tokens
    state.agent_contributions.append(
        AgentContribution(
            agent_name=result.display_name,
            phase=phase,
            input_summary=input_summary,
            output_summary=_truncate_output(result.output),
            token_count=result.tokens,
            execution_time_ms=result.execution_time_ms,
        )
    )
    state.agents_trace_data.append(
        {
            "agent_name": result.display_name,
            "order": order,
            "input": result.user_prompt,
            "output": result.output,
            "token_usage": result.tokens,
            "system_prompt": result.system_prompt,
            "user_prompt": result.user_prompt,
        }
    )


async def _run_phase1(ctx: EvaluationContext, state: PipelineState) -> tuple[str, str, str]:
    """Run Phase 1: Parallel analysis agents."""
    logging.info("Phase 1: Running parallel analysis agents")
    phase_start = time.time()

    sub_sys, sub_user = get_submission_evaluator_prompts(ctx.revision)
    crit_sys, crit_user = get_criteria_evaluator_prompts(ctx.revision)
    next_sys, next_user = get_next_steps_prompts(ctx.revision)

    sub_user_rendered = _render_template(
        sub_user,
        {"submission_name": ctx.submission_name, "submission_content": ctx.submission_content},
    )
    crit_user_rendered = _render_template(crit_user, {"criteria_text": ctx.criteria_text})
    next_user_rendered = _render_template(
        next_user,
        {"submission_name": ctx.submission_name, "submission_content": ctx.submission_content},
    )

    results = await asyncio.gather(
        _run_agent(
            "submission_evaluator",
            sub_sys,
            sub_user_rendered,
            ctx.model_client,
            ctx.cancellation_token,
        ),
        _run_agent(
            "criteria_evaluator",
            crit_sys,
            crit_user_rendered,
            ctx.model_client,
            ctx.cancellation_token,
        ),
        _run_agent(
            "next_steps", next_sys, next_user_rendered, ctx.model_client, ctx.cancellation_token
        ),
        return_exceptions=True,
    )

    phase_time = int((time.time() - phase_start) * 1000)
    agent_time = phase_time // 3

    agent_configs = [
        (
            "submission_evaluator",
            "Submission Evaluator",
            sub_sys,
            sub_user_rendered,
            "Analyzed submission",
        ),
        (
            "criteria_evaluator",
            "Criteria Evaluator",
            crit_sys,
            crit_user_rendered,
            "Analyzed criteria",
        ),
        ("next_steps", "Next Steps Agent", next_sys, next_user_rendered, "Analyzed improvements"),
    ]

    outputs = ["{}", "{}", "{}"]
    for i, (agent_result, agent_cfg) in enumerate(zip(results, agent_configs)):
        agent_name, display_name, sys_prompt, user_prompt, input_summary = agent_cfg

        if isinstance(agent_result, BaseException):
            logging.error(f"{agent_name} failed: {agent_result}")
            output, tokens = json.dumps({"error": str(agent_result)}), 0
        else:
            output, tokens = agent_result

        outputs[i] = output
        _record_agent_result(
            state,
            AgentResult(
                output, tokens, agent_name, display_name, sys_prompt, user_prompt, agent_time
            ),
            phase=1,
            order=i + 1,
            input_summary=input_summary,
        )

    return outputs[0], outputs[1], outputs[2]


async def _run_sequential_agent(
    ctx: EvaluationContext,
    state: PipelineState,
    agent_name: str,
    display_name: str,
    get_prompts_fn: Any,
    template_vars: dict[str, Any],
    phase: int,
    order: int,
    input_summary: str,
) -> str:
    """Run a sequential agent phase."""
    logging.info(f"Phase {phase}: Running {display_name}")
    phase_start = time.time()

    sys_prompt, user_prompt = get_prompts_fn(ctx.revision)
    user_rendered = _render_template(user_prompt, template_vars)

    output, tokens = await _run_agent(
        agent_name, sys_prompt, user_rendered, ctx.model_client, ctx.cancellation_token
    )
    phase_time = int((time.time() - phase_start) * 1000)

    _record_agent_result(
        state,
        AgentResult(
            output, tokens, agent_name, display_name, sys_prompt, user_rendered, phase_time
        ),
        phase=phase,
        order=order,
        input_summary=input_summary,
    )

    return output


def _extract_next_steps(sanity_output: dict[str, Any], next_steps_output: str) -> list[str]:
    """Extract next steps from sanity check or original next steps output."""
    final_output = sanity_output.get("final_output", {})
    next_steps_list = final_output.get("nextSteps", [])

    if next_steps_list:
        return next_steps_list

    try:
        next_data = json.loads(next_steps_output)
        improvements = next_data.get("priority_improvements", [])
        return [imp.get("recommended_action", "") for imp in improvements[:5]]
    except (json.JSONDecodeError, KeyError):
        return []


def _build_final_response(
    sanity_output: str,
    summary_output: str,
    next_steps_output: str,
    agent_contributions: list[AgentContribution],
) -> tuple[str, str]:
    """Build the final evaluation response JSON."""
    try:
        sanity_data = json.loads(sanity_output)
        final_output = sanity_data.get("final_output", {})
        validation_status = sanity_data.get("validation_status", "passed")

        criterion_results = [
            CriterionResultSchema(
                criterionId=cr.get("criterionId", ""),
                score=float(cr.get("score", 0)),
                narrative=cr.get("narrative", ""),
            )
            for cr in final_output.get("criterionResults", [])
        ]

        next_steps_list = _extract_next_steps(sanity_data, next_steps_output)

        eval_response = EvaluationResponseSchema(
            criterionResults=criterion_results,
            overallScore=float(final_output.get("overallScore", 0)),
            summary=final_output.get("narrative", "Evaluation completed."),
            nextSteps=next_steps_list,
            agentContributions=agent_contributions,
            validationStatus=validation_status,
        )
        return eval_response.model_dump_json(), validation_status

    except (json.JSONDecodeError, KeyError) as e:
        logging.error(f"Failed to parse sanity check output: {e}")
        return _build_fallback_response(summary_output, agent_contributions)


def _build_fallback_response(
    summary_output: str,
    agent_contributions: list[AgentContribution],
) -> tuple[str, str]:
    """Build fallback response when sanity check parsing fails."""
    try:
        summary_data = json.loads(summary_output)
        eval_response = EvaluationResponseSchema(
            criterionResults=[],
            overallScore=float(summary_data.get("overallScore", 0)),
            summary=summary_data.get("overall_narrative", "Evaluation completed."),
            nextSteps=[],
            agentContributions=agent_contributions,
            validationStatus="flagged",
        )
        return eval_response.model_dump_json(), "flagged"
    except (json.JSONDecodeError, KeyError):
        error_response = {
            "criterionResults": [],
            "overallScore": 0,
            "summary": "Evaluation pipeline completed but output parsing failed.",
            "nextSteps": [],
            "agentContributions": [ac.model_dump() for ac in agent_contributions],
            "validationStatus": "flagged",
        }
        return json.dumps(error_response), "flagged"


def _build_error_response(
    error: Exception, agent_contributions: list[AgentContribution]
) -> tuple[str, str]:
    """Build error response when pipeline fails."""
    logging.error(f"Evaluation pipeline failed: {error}")
    error_response = {
        "criterionResults": [],
        "overallScore": 0,
        "summary": f"Evaluation pipeline failed: {str(error)}",
        "nextSteps": [],
        "agentContributions": [ac.model_dump() for ac in agent_contributions],
        "validationStatus": "error",
    }
    return json.dumps(error_response), f"Evaluation error: {str(error)[:50]}..."


class ConversationFlow:
    """Conversation flow for SoCa document evaluation using 6-agent pipeline."""

    @staticmethod
    async def get_conversation_response(
        message: str,
        topics: Optional[list[str]] = None,
        thread_memory: str = "",
        memory_record_switch: bool = True,
        thread_chat_history: Optional[list[dict[str, Any]]] = None,
        chatrequest: Optional[ChatRequest] = None,
        revision: str = "active",
    ) -> tuple[str, str, int, str]:
        """Get an evaluation response using the 6-agent pipeline."""
        if chatrequest:
            message = chatrequest.user_prompt
            _ = chatrequest.topic if chatrequest.topic else topics

        _config = config.get_config()
        model_config = _config.models[0]

        logger = logging.getLogger(EVENT_LOGGER_NAME)
        logger.setLevel(logging.INFO)
        logger.handlers = [
            LLMUsageTracker(
                agents=[
                    "submission_evaluator",
                    "criteria_evaluator",
                    "next_steps",
                    "scoring_agent",
                    "summarizer_agent",
                    "sanity_check",
                ],
                config=_config,
                chat_history_repository=None,
                revision_id=str(uuid.uuid4()),
                identifier=str(uuid.uuid4()),
                event_type="evaluation",
            )
        ]

        try:
            input_data = json.loads(message)
            submission_name = input_data.get("submission_name", "Untitled")
            submission_content = input_data.get("submission_content", message)
            criteria_text = input_data.get("criteria_text", "")
        except json.JSONDecodeError:
            submission_name = "Untitled"
            submission_content = message
            criteria_text = ""

        builder = AzureOpenAIChatCompletionClientBuilder(model_config)
        model_client = builder.build()

        ctx = EvaluationContext(
            submission_name=submission_name,
            submission_content=submission_content,
            criteria_text=criteria_text,
            revision=revision,
            model_client=model_client,
            cancellation_token=CancellationToken(),
        )
        state = PipelineState()

        try:
            submission_analysis, criteria_analysis, next_steps_output = await _run_phase1(
                ctx, state
            )

            scoring_output = await _run_sequential_agent(
                ctx,
                state,
                "scoring_agent",
                "Scoring Agent",
                get_scoring_agent_prompts,
                {
                    "submission_analysis": submission_analysis,
                    "criteria_analysis": criteria_analysis,
                    "next_steps": next_steps_output,
                    "criteria_text": criteria_text,
                },
                phase=2,
                order=4,
                input_summary="Combined Phase 1 outputs for scoring",
            )

            summary_output = await _run_sequential_agent(
                ctx,
                state,
                "summarizer_agent",
                "Summarizer Agent",
                get_summarizer_agent_prompts,
                {"scores": scoring_output, "submission_name": submission_name},
                phase=3,
                order=5,
                input_summary="Created summary from scoring results",
            )

            sanity_output = await _run_sequential_agent(
                ctx,
                state,
                "sanity_check",
                "Sanity Check Agent",
                get_sanity_check_prompts,
                {
                    "summary": summary_output,
                    "scores": scoring_output,
                    "criteria_text": criteria_text,
                },
                phase=4,
                order=6,
                input_summary="Validated evaluation for consistency",
            )

            result_json, validation_status = _build_final_response(
                sanity_output, summary_output, next_steps_output, state.agent_contributions
            )
            memory_summary = f"6-agent evaluation completed. Validation: {validation_status}"

        except Exception as e:
            result_json, memory_summary = _build_error_response(e, state.agent_contributions)

        finally:
            await model_client.close()

        agents_info = json.dumps(
            {
                "pipeline": "6-agent",
                "phases": 4,
                "agents": [
                    "Submission Evaluator",
                    "Criteria Evaluator",
                    "Next Steps Agent",
                    "Scoring Agent",
                    "Summarizer Agent",
                    "Sanity Check Agent",
                ],
                "total_tokens": state.total_tokens,
                "agents_trace_data": state.agents_trace_data,
            }
        )

        return result_json, memory_summary, state.total_tokens, agents_info
