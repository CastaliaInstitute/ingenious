"""SoCa evaluator conversation flow implementation.

This module provides a conversation flow for evaluating submissions against
criteria using the Ingenious framework with AutoGen agents.
"""

import json
import logging
import uuid
from typing import Any, Optional

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import EVENT_LOGGER_NAME, CancellationToken

import ingenious.config.config as config
from ingen_prompt_tuner.models import EvaluationResponseSchema
from ingen_prompt_tuner.prompts import get_evaluation_system_prompt
from ingenious.client.azure.builder.openai_chat_completions_client import (
    AzureOpenAIChatCompletionClientBuilder,
)
from ingenious.models.agent import LLMUsageTracker
from ingenious.models.chat import ChatRequest


class ConversationFlow:
    """Conversation flow for SoCa document evaluation.

    Provides a static method for evaluating submissions against criteria
    using an AutoGen evaluation agent with structured output support.
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
        """Get an evaluation response for the submission.

        Evaluates the submission against the provided criteria and returns
        structured evaluation results.

        Args:
            message: User's submission to evaluate (JSON with criteria and content).
            topics: List of topics for context. Defaults to None.
            thread_memory: Previous conversation memory as string. Defaults to empty string.
            memory_record_switch: Whether memory recording is enabled. Defaults to True.
            thread_chat_history: Previous conversation history as list. Defaults to None.
            chatrequest: ChatRequest object for backward compatibility. Defaults to None.
            revision: Prompt revision to use. Defaults to "active".

        Returns:
            Tuple of (evaluation_result_json, memory_summary, token_count, system_prompt).
        """
        # Use provided message or extract from chatrequest
        if chatrequest:
            message = chatrequest.user_prompt
            # topics can be used for future topic-based routing
            _ = chatrequest.topic if chatrequest.topic else topics

        _config = config.get_config()
        model_config = _config.models[0]

        # Initialize LLM usage tracking
        logger = logging.getLogger(EVENT_LOGGER_NAME)
        logger.setLevel(logging.INFO)

        llm_logger = LLMUsageTracker(
            agents=["soca_evaluator_agent"],
            config=_config,
            chat_history_repository=None,
            revision_id=str(uuid.uuid4()),
            identifier=str(uuid.uuid4()),
            event_type="evaluation",
        )

        logger.handlers = [llm_logger]

        # Get the configurable system prompt from the prompts module
        system_prompt = get_evaluation_system_prompt(revision)

        # Add structured output instructions to the system prompt
        evaluation_system_prompt = f"""{system_prompt}

IMPORTANT: You MUST respond with valid JSON matching this exact schema:
{{
    "criterionResults": [
        {{
            "criterionId": "string - the exact criterion ID from the request",
            "score": number - score between 1 and max_score for the criterion,
            "narrative": "string - 1-2 sentence justification for the score"
        }}
    ],
    "overallScore": number - weighted percentage from 0-100 (calculate as sum of (score/maxScore)*weight for each criterion),
    "summary": "string - 2-3 sentence summary of the overall evaluation"
}}

Respond ONLY with valid JSON, no markdown formatting or additional text."""

        # Create the Azure OpenAI client using the provided model configuration
        builder = AzureOpenAIChatCompletionClientBuilder(model_config)
        model_client = builder.build()

        # Create the evaluation agent
        evaluation_agent = AssistantAgent(
            name="soca_evaluator_agent",
            system_message=evaluation_system_prompt,
            model_client=model_client,
        )

        # Create cancellation token
        cancellation_token = CancellationToken()

        token_count = 0

        try:
            # Send the user message to the evaluation agent
            response = await evaluation_agent.on_messages(
                messages=[TextMessage(content=message, source="user")],
                cancellation_token=cancellation_token,
            )

            # Extract the response content
            chat_msg = response.chat_message
            result_text = str(chat_msg.content) if hasattr(chat_msg, "content") else "{}"

            # Try to parse and validate the response
            try:
                # Clean up the response if it has markdown formatting
                clean_result = result_text.strip()
                if clean_result.startswith("```json"):
                    clean_result = clean_result[7:]
                if clean_result.startswith("```"):
                    clean_result = clean_result[3:]
                if clean_result.endswith("```"):
                    clean_result = clean_result[:-3]
                clean_result = clean_result.strip()

                # Validate against schema
                parsed = EvaluationResponseSchema.model_validate_json(clean_result)
                result = parsed.model_dump_json()
            except Exception:
                # If parsing fails, use the raw result
                result = result_text

            # Get token count from the response's models_usage
            # AutoGen AgentChat includes RequestUsage with prompt_tokens and completion_tokens
            if hasattr(chat_msg, "models_usage") and chat_msg.models_usage is not None:
                usage = chat_msg.models_usage
                token_count = getattr(usage, "prompt_tokens", 0) + getattr(
                    usage, "completion_tokens", 0
                )

            # Fallback to LLM logger if response doesn't have usage
            if token_count == 0 and hasattr(llm_logger, "tokens"):
                token_count = llm_logger.tokens

            memory_summary = "Evaluation completed successfully"

        except Exception as e:
            logging.error(f"Evaluation failed: {e}")
            error_response = {
                "criterionResults": [],
                "overallScore": 0,
                "summary": f"Evaluation failed: {str(e)}",
            }
            result = json.dumps(error_response)
            memory_summary = f"Evaluation error: {str(e)[:50]}..."

        finally:
            # Close the model client connection
            await model_client.close()

        return result, memory_summary, token_count, evaluation_system_prompt
