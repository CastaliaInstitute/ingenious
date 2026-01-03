"""Criteria generator conversation flow implementation.

This module provides a conversation flow for extracting structured evaluation
criteria from unstructured document text using the Ingenious framework.
"""

import json
import logging
import uuid
from typing import Any, Optional

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import EVENT_LOGGER_NAME, CancellationToken

import ingenious.config.config as config
from ingen_prompt_tuner.models import CriteriaGenerationResponseSchema
from ingen_prompt_tuner.prompts import get_criteria_generator_system_prompt
from ingenious.client.azure.builder.openai_chat_completions_client import (
    AzureOpenAIChatCompletionClientBuilder,
)
from ingenious.models.agent import LLMUsageTracker
from ingenious.models.chat import ChatRequest


class ConversationFlow:
    """Conversation flow for criteria extraction from documents.

    Provides a static method for analyzing documents and extracting
    structured evaluation criteria using an AutoGen agent with structured output.
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
    ) -> tuple[str, str, int]:
        """Extract evaluation criteria from document text.

        Analyzes the provided document text and generates structured criteria
        suitable for use with SoCa's evaluation system.

        Args:
            message: Document text to analyze for criteria extraction.
            topics: List of topics for context. Defaults to None.
            thread_memory: Previous conversation memory. Defaults to empty string.
            memory_record_switch: Whether memory recording is enabled. Defaults to True.
            thread_chat_history: Previous conversation history. Defaults to None.
            chatrequest: ChatRequest object for backward compatibility. Defaults to None.
            revision: Prompt revision to use. Defaults to "active".

        Returns:
            Tuple of (criteria_json, memory_summary, token_count).
        """
        # Use provided message or extract from chatrequest
        if chatrequest:
            message = chatrequest.user_prompt
            _ = chatrequest.topic if chatrequest.topic else topics

        _config = config.get_config()
        model_config = _config.models[0]

        # Initialize LLM usage tracking
        logger = logging.getLogger(EVENT_LOGGER_NAME)
        logger.setLevel(logging.INFO)

        llm_logger = LLMUsageTracker(
            agents=["criteria_generator_agent"],
            config=_config,
            chat_history_repository=None,
            revision_id=str(uuid.uuid4()),
            identifier=str(uuid.uuid4()),
            event_type="criteria_generation",
        )

        logger.handlers = [llm_logger]

        # Get the configurable system prompt
        system_prompt = get_criteria_generator_system_prompt(revision)

        # Add structured output instructions
        criteria_system_prompt = f"""{system_prompt}

IMPORTANT: You MUST respond with valid JSON matching this exact schema:
{{
    "name": "string - descriptive name for the criteria set",
    "description": "string - brief description of the criteria set",
    "criteria": [
        {{
            "id": "string - unique ID in format 'criterion-N'",
            "name": "string - short criterion name (2-5 words)",
            "description": "string - evaluation guidance (1-2 sentences)",
            "weight": number - percentage weight (0-100, all must sum to 100),
            "maxScore": number - either 5 or 10
        }}
    ]
}}

Ensure all weights sum to exactly 100.
Respond ONLY with valid JSON, no markdown formatting or additional text."""

        # Create the Azure OpenAI client
        builder = AzureOpenAIChatCompletionClientBuilder(model_config)
        model_client = builder.build()

        # Create the criteria generator agent
        generator_agent = AssistantAgent(
            name="criteria_generator_agent",
            system_message=criteria_system_prompt,
            model_client=model_client,
        )

        # Create cancellation token
        cancellation_token = CancellationToken()

        token_count = 0

        try:
            # Send the document text to the agent
            response = await generator_agent.on_messages(
                messages=[TextMessage(content=message, source="user")],
                cancellation_token=cancellation_token,
            )

            # Extract response content
            chat_msg = response.chat_message
            result_text = str(chat_msg.content) if hasattr(chat_msg, "content") else "{}"

            # Parse and validate the response
            try:
                # Clean markdown formatting if present
                clean_result = result_text.strip()
                if clean_result.startswith("```json"):
                    clean_result = clean_result[7:]
                if clean_result.startswith("```"):
                    clean_result = clean_result[3:]
                if clean_result.endswith("```"):
                    clean_result = clean_result[:-3]
                clean_result = clean_result.strip()

                # Validate against schema
                parsed = CriteriaGenerationResponseSchema.model_validate_json(clean_result)

                # Validate and normalize weight sum
                total_weight = sum(c.weight for c in parsed.criteria)
                if total_weight != 100 and parsed.criteria:
                    # Normalize weights to sum to 100 if close
                    if 80 <= total_weight <= 120:
                        for criterion in parsed.criteria:
                            criterion.weight = round(criterion.weight * 100 / total_weight)
                        # Adjust last criterion to ensure exact sum
                        adjustment = 100 - sum(c.weight for c in parsed.criteria[:-1])
                        parsed.criteria[-1].weight = adjustment
                    else:
                        logging.warning(f"Weight sum is {total_weight}, expected 100")

                result = parsed.model_dump_json()
            except Exception as parse_error:
                logging.warning(f"Failed to parse response: {parse_error}")
                result = result_text

            # Get token count
            if hasattr(llm_logger, "total_tokens"):
                token_count = llm_logger.total_tokens

            memory_summary = "Criteria extraction completed successfully"

        except Exception as e:
            logging.error(f"Criteria generation failed: {e}")
            error_response = {
                "name": "Error",
                "description": f"Criteria generation failed: {str(e)}",
                "criteria": [],
            }
            result = json.dumps(error_response)
            memory_summary = f"Criteria generation error: {str(e)[:50]}..."

        finally:
            # Close the model client connection
            await model_client.close()

        return result, memory_summary, token_count
