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


async def _run_agent(
    agent_name: str,
    system_prompt: str,
    user_prompt: str,
    model_client: Any,
    cancellation_token: CancellationToken,
) -> tuple[str, int]:
    """Run a single agent and return its response and token count.

    Args:
        agent_name: Name of the agent
        system_prompt: System prompt for the agent
        user_prompt: User message to send
        model_client: Azure OpenAI client
        cancellation_token: Cancellation token

    Returns:
        Tuple of (response_text, token_count)
    """
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

    # Get token count
    token_count = 0
    if hasattr(chat_msg, "models_usage") and chat_msg.models_usage is not None:
        usage = chat_msg.models_usage
        token_count = getattr(usage, "prompt_tokens", 0) + getattr(usage, "completion_tokens", 0)

    return _clean_json_response(result_text), token_count


class ConversationFlow:
    """Conversation flow for SoCa document evaluation using 6-agent pipeline.

    The pipeline processes evaluations through 4 phases:
    - Phase 1: Parallel analysis (Submission, Criteria, Next Steps)
    - Phase 2: Scoring based on Phase 1 outputs
    - Phase 3: Summary generation
    - Phase 4: Validation and sanity check
    """

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
        """Get an evaluation response using the 6-agent pipeline.

        Args:
            message: User's submission to evaluate (contains criteria and content).
            topics: List of topics for context.
            thread_memory: Previous conversation memory.
            memory_record_switch: Whether memory recording is enabled.
            thread_chat_history: Previous conversation history.
            chatrequest: ChatRequest object for backward compatibility.
            revision: Prompt revision to use.

        Returns:
            Tuple of (evaluation_result_json, memory_summary, token_count, agents_info).
        """
        if chatrequest:
            message = chatrequest.user_prompt
            _ = chatrequest.topic if chatrequest.topic else topics

        _config = config.get_config()
        model_config = _config.models[0]

        # Initialize logging
        logger = logging.getLogger(EVENT_LOGGER_NAME)
        logger.setLevel(logging.INFO)

        llm_logger = LLMUsageTracker(
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
        logger.handlers = [llm_logger]

        # Parse the input message to extract submission and criteria
        try:
            input_data = json.loads(message)
            submission_name = input_data.get("submission_name", "Untitled")
            submission_content = input_data.get("submission_content", message)
            criteria_text = input_data.get("criteria_text", "")
        except json.JSONDecodeError:
            # Fall back to using message as content
            submission_name = "Untitled"
            submission_content = message
            criteria_text = ""

        # Create model client
        builder = AzureOpenAIChatCompletionClientBuilder(model_config)
        model_client = builder.build()
        cancellation_token = CancellationToken()

        total_tokens = 0
        agent_contributions: list[AgentContribution] = []
        # Track detailed agent data for trace storage
        agents_trace_data: list[dict[str, Any]] = []

        try:
            # =========================================================
            # PHASE 1: PARALLEL ANALYSIS
            # =========================================================
            logging.info("Phase 1: Running parallel analysis agents")
            phase1_start = time.time()

            # Get prompts for Phase 1 agents
            sub_sys, sub_user = get_submission_evaluator_prompts(revision)
            crit_sys, crit_user = get_criteria_evaluator_prompts(revision)
            next_sys, next_user = get_next_steps_prompts(revision)

            # Render user prompts with variables
            sub_user_rendered = _render_template(
                sub_user,
                {"submission_name": submission_name, "submission_content": submission_content},
            )
            crit_user_rendered = _render_template(crit_user, {"criteria_text": criteria_text})
            next_user_rendered = _render_template(
                next_user,
                {"submission_name": submission_name, "submission_content": submission_content},
            )

            # Run Phase 1 agents in parallel
            phase1_results = await asyncio.gather(
                _run_agent(
                    "submission_evaluator",
                    sub_sys,
                    sub_user_rendered,
                    model_client,
                    cancellation_token,
                ),
                _run_agent(
                    "criteria_evaluator",
                    crit_sys,
                    crit_user_rendered,
                    model_client,
                    cancellation_token,
                ),
                _run_agent(
                    "next_steps",
                    next_sys,
                    next_user_rendered,
                    model_client,
                    cancellation_token,
                ),
                return_exceptions=True,
            )

            phase1_time = int((time.time() - phase1_start) * 1000)

            # Process Phase 1 results
            submission_analysis = "{}"
            criteria_analysis = "{}"
            next_steps_output = "{}"

            # User prompts for Phase 1 agents
            phase1_user_prompts = [sub_user_rendered, crit_user_rendered, next_user_rendered]
            phase1_system_prompts = [sub_sys, crit_sys, next_sys]

            for i, agent_result in enumerate(phase1_results):
                agent_name = ["submission_evaluator", "criteria_evaluator", "next_steps"][i]
                display_name = ["Submission Evaluator", "Criteria Evaluator", "Next Steps Agent"][i]
                if isinstance(agent_result, BaseException):
                    logging.error(f"{agent_name} failed: {agent_result}")
                    tokens = 0
                    output = json.dumps({"error": str(agent_result)})
                else:
                    # agent_result is tuple[str, int] here
                    output, tokens = agent_result
                    total_tokens += tokens

                if i == 0:
                    submission_analysis = output
                elif i == 1:
                    criteria_analysis = output
                else:
                    next_steps_output = output

                agent_contributions.append(
                    AgentContribution(
                        agent_name=display_name,
                        phase=1,
                        input_summary=f"Analyzed {'submission' if i == 0 else 'criteria' if i == 1 else 'improvements'}",
                        output_summary=output[:200] + "..." if len(output) > 200 else output,
                        token_count=tokens,
                        execution_time_ms=phase1_time // 3,  # Approximate per agent
                    )
                )

                # Track for trace storage
                agents_trace_data.append(
                    {
                        "agent_name": display_name,
                        "order": i + 1,
                        "input": phase1_user_prompts[i],
                        "output": output,
                        "token_usage": tokens,
                        "system_prompt": phase1_system_prompts[i],
                        "user_prompt": phase1_user_prompts[i],
                    }
                )

            # =========================================================
            # PHASE 2: SCORING
            # =========================================================
            logging.info("Phase 2: Running Scoring Agent")
            phase2_start = time.time()

            score_sys, score_user = get_scoring_agent_prompts(revision)
            score_user_rendered = _render_template(
                score_user,
                {
                    "submission_analysis": submission_analysis,
                    "criteria_analysis": criteria_analysis,
                    "next_steps": next_steps_output,
                    "criteria_text": criteria_text,
                },
            )

            scoring_output, scoring_tokens = await _run_agent(
                "scoring_agent",
                score_sys,
                score_user_rendered,
                model_client,
                cancellation_token,
            )
            total_tokens += scoring_tokens
            phase2_time = int((time.time() - phase2_start) * 1000)

            agent_contributions.append(
                AgentContribution(
                    agent_name="Scoring Agent",
                    phase=2,
                    input_summary="Combined Phase 1 outputs for scoring",
                    output_summary=scoring_output[:200] + "..."
                    if len(scoring_output) > 200
                    else scoring_output,
                    token_count=scoring_tokens,
                    execution_time_ms=phase2_time,
                )
            )

            # Track for trace storage
            agents_trace_data.append(
                {
                    "agent_name": "Scoring Agent",
                    "order": 4,
                    "input": score_user_rendered,
                    "output": scoring_output,
                    "token_usage": scoring_tokens,
                    "system_prompt": score_sys,
                    "user_prompt": score_user_rendered,
                }
            )

            # =========================================================
            # PHASE 3: SUMMARIZATION
            # =========================================================
            logging.info("Phase 3: Running Summarizer Agent")
            phase3_start = time.time()

            sum_sys, sum_user = get_summarizer_agent_prompts(revision)
            sum_user_rendered = _render_template(
                sum_user,
                {"scores": scoring_output, "submission_name": submission_name},
            )

            summary_output, summary_tokens = await _run_agent(
                "summarizer_agent",
                sum_sys,
                sum_user_rendered,
                model_client,
                cancellation_token,
            )
            total_tokens += summary_tokens
            phase3_time = int((time.time() - phase3_start) * 1000)

            agent_contributions.append(
                AgentContribution(
                    agent_name="Summarizer Agent",
                    phase=3,
                    input_summary="Created summary from scoring results",
                    output_summary=summary_output[:200] + "..."
                    if len(summary_output) > 200
                    else summary_output,
                    token_count=summary_tokens,
                    execution_time_ms=phase3_time,
                )
            )

            # Track for trace storage
            agents_trace_data.append(
                {
                    "agent_name": "Summarizer Agent",
                    "order": 5,
                    "input": sum_user_rendered,
                    "output": summary_output,
                    "token_usage": summary_tokens,
                    "system_prompt": sum_sys,
                    "user_prompt": sum_user_rendered,
                }
            )

            # =========================================================
            # PHASE 4: SANITY CHECK
            # =========================================================
            logging.info("Phase 4: Running Sanity Check Agent")
            phase4_start = time.time()

            sanity_sys, sanity_user = get_sanity_check_prompts(revision)
            sanity_user_rendered = _render_template(
                sanity_user,
                {
                    "summary": summary_output,
                    "scores": scoring_output,
                    "criteria_text": criteria_text,
                },
            )

            sanity_output, sanity_tokens = await _run_agent(
                "sanity_check",
                sanity_sys,
                sanity_user_rendered,
                model_client,
                cancellation_token,
            )
            total_tokens += sanity_tokens
            phase4_time = int((time.time() - phase4_start) * 1000)

            agent_contributions.append(
                AgentContribution(
                    agent_name="Sanity Check Agent",
                    phase=4,
                    input_summary="Validated evaluation for consistency",
                    output_summary=sanity_output[:200] + "..."
                    if len(sanity_output) > 200
                    else sanity_output,
                    token_count=sanity_tokens,
                    execution_time_ms=phase4_time,
                )
            )

            # Track for trace storage
            agents_trace_data.append(
                {
                    "agent_name": "Sanity Check Agent",
                    "order": 6,
                    "input": sanity_user_rendered,
                    "output": sanity_output,
                    "token_usage": sanity_tokens,
                    "system_prompt": sanity_sys,
                    "user_prompt": sanity_user_rendered,
                }
            )

            # =========================================================
            # BUILD FINAL RESPONSE
            # =========================================================
            try:
                sanity_data = json.loads(sanity_output)
                final_output = sanity_data.get("final_output", {})
                validation_status = sanity_data.get("validation_status", "passed")

                # Extract criterion results
                criterion_results = []
                for cr in final_output.get("criterionResults", []):
                    criterion_results.append(
                        CriterionResultSchema(
                            criterionId=cr.get("criterionId", ""),
                            score=float(cr.get("score", 0)),
                            narrative=cr.get("narrative", ""),
                        )
                    )

                # Extract next steps from the sanity check output or original next steps
                next_steps_list = final_output.get("nextSteps", [])
                if not next_steps_list:
                    try:
                        next_data = json.loads(next_steps_output)
                        improvements = next_data.get("priority_improvements", [])
                        next_steps_list = [
                            imp.get("recommended_action", "") for imp in improvements[:5]
                        ]
                    except (json.JSONDecodeError, KeyError):
                        next_steps_list = []

                eval_response = EvaluationResponseSchema(
                    criterionResults=criterion_results,
                    overallScore=float(final_output.get("overallScore", 0)),
                    summary=final_output.get("narrative", "Evaluation completed."),
                    nextSteps=next_steps_list,
                    agentContributions=agent_contributions,
                    validationStatus=validation_status,
                )
                result_json = eval_response.model_dump_json()

            except (json.JSONDecodeError, KeyError) as e:
                logging.error(f"Failed to parse sanity check output: {e}")
                # Fallback: try to build from summary output
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
                    result_json = eval_response.model_dump_json()
                except (json.JSONDecodeError, KeyError):
                    error_response = {
                        "criterionResults": [],
                        "overallScore": 0,
                        "summary": "Evaluation pipeline completed but output parsing failed.",
                        "nextSteps": [],
                        "agentContributions": [ac.model_dump() for ac in agent_contributions],
                        "validationStatus": "flagged",
                    }
                    result_json = json.dumps(error_response)

            memory_summary = f"6-agent evaluation completed. Validation: {validation_status}"

        except Exception as e:
            logging.error(f"Evaluation pipeline failed: {e}")
            error_response = {
                "criterionResults": [],
                "overallScore": 0,
                "summary": f"Evaluation pipeline failed: {str(e)}",
                "nextSteps": [],
                "agentContributions": [ac.model_dump() for ac in agent_contributions],
                "validationStatus": "error",
            }
            result_json = json.dumps(error_response)
            memory_summary = f"Evaluation error: {str(e)[:50]}..."

        finally:
            await model_client.close()

        # Build agents info string for tracing (includes full trace data)
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
                "total_tokens": total_tokens,
                "agents_trace_data": agents_trace_data,
            }
        )

        return result_json, memory_summary, total_tokens, agents_info
