"""Utility functions for Wilma CLI."""

from typing import Any


# Avoid circular imports - define this function to be imported later
def get_message_summarizer() -> Any:
    """Get the MessageSummarizer class to avoid circular imports."""
    from wilhelminacli.utils.summarizer import MessageSummarizer

    return MessageSummarizer
