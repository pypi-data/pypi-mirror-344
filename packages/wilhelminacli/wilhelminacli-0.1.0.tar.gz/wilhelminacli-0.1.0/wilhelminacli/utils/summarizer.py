"""AI summarizer for Wilma messages."""

import logging
import os
from typing import List

import anthropic
from anthropic.types import MessageParam
from wilhelmina.models import Message


class MessageSummarizer:
    """Summarizer for Wilma messages using Anthropic Claude."""

    def __init__(self) -> None:
        """Initialize the summarizer with API key from environment."""
        # Check for API key
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")

        # Get model from environment or use default
        self.model = os.environ.get("ANTHROPIC_MODEL", "claude-3-7-sonnet-20250219")

        # Initialize client
        try:
            self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
        except Exception as e:
            logging.exception("Error initializing Anthropic client: %s", e)
            raise ValueError(
                f"Failed to initialize Anthropic client: {e}. "
                f"Please check your ANTHROPIC_API_KEY environment variable."
            )

    async def summarize_message(self, message: Message) -> str:
        """Summarize a single message.

        Args:
            message: The message to summarize

        Returns:
            A summary of the message
        """
        prompt = f"""
        Summarize the following message and focus on:
        1. If I need to take any action based on the message
        2. If an action is required, what the action is and when it needs to be done
        3. What the main content and most important information in the message is

        Analyze the language of the message and respond in the SAME LANGUAGE.
        Be brief and concise in your summary.

        Subject: {message.subject}
        From: {message.sender}
        Date: {message.timestamp}

        {message.content_markdown}
        """

        response = await self._get_completion(prompt)
        return response

    async def summarize_messages(self, messages: List[Message]) -> str:
        """Summarize multiple messages.

        Args:
            messages: List of messages to summarize

        Returns:
            A summary of all messages
        """
        if not messages:
            return "No unread messages."

        messages_text = "\n\n".join(
            [
                f"ID: {msg.id}\nSubject: {msg.subject}\nFrom: {msg.sender}\nDate: {msg.timestamp}"
                for msg in messages
            ]
        )

        prompt = f"""
        Summarize the following unread messages and focus on:
        1. Which messages require actions from me
        2. For each action, what the action is and when it needs to be done
        3. Prioritize the messages based on their importance

        Respond in the SAME LANGUAGE as the majority of the messages.
        Be brief and concise in your summary.

        MESSAGES:
        {messages_text}
        """

        response = await self._get_completion(prompt)
        return response

    async def _get_completion(self, prompt: str) -> str:
        """Get a completion from the Claude API.

        Args:
            prompt: The prompt to send to Claude

        Returns:
            The generated response
        """
        try:
            # Create message parameters for the modern API
            messages: List[MessageParam] = [{"role": "user", "content": prompt}]

            # Call the API with the configured model
            try:
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    messages=messages,
                )
                if hasattr(response.content[0], "text"):
                    return str(response.content[0].text)
                else:
                    return str(response.content[0])
            except anthropic.BadRequestError as e:
                # Try fallback model if the configured model is invalid
                if "model" in str(e).lower():
                    logging.warning(
                        "Model %s not found, falling back to claude-3-sonnet-20240229", self.model
                    )
                    response = await self.client.messages.create(
                        model="claude-3-sonnet-20240229",
                        max_tokens=1000,
                        messages=messages,
                    )
                    if hasattr(response.content[0], "text"):
                        return str(response.content[0].text)
                    else:
                        return str(response.content[0])
                raise

        except Exception as e:
            logging.exception("Error in Anthropic API call: %s", e)
            raise ValueError(
                "Failed to generate summary: %s. Please check your ANTHROPIC_API_KEY "
                "environment variable and ensure your Anthropic model is valid.",
                e,
            )
