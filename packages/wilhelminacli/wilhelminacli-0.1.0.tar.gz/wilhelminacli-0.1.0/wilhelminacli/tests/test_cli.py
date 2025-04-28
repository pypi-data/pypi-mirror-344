"""Tests for Wilma CLI."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from typer.testing import CliRunner
from wilhelmina.models import Message

from wilhelminacli.cli import app

runner = CliRunner()


@pytest.fixture
def mock_messages() -> list[Message]:
    """Create mock message objects for testing."""
    return [
        Message(
            id=1,
            subject="Test message 1",
            timestamp="2025-04-16 13:31",
            folder="Inbox",
            sender_id=123,
            sender_type=1,
            sender="Teacher 1",
            content_html="<p>This is test message 1</p>",
            unread=True,
        ),
        Message(
            id=2,
            subject="Test message 2",
            timestamp="2025-04-15 10:20",
            folder="Inbox",
            sender_id=456,
            sender_type=1,
            sender="Teacher 2",
            content_html="<p>This is test message 2</p>",
            unread=False,
        ),
    ]


@patch("wilhelminacli.cli.asyncio.run")
@patch("wilhelminacli.cli._login")
def test_login_command(mock_login, mock_run) -> None:
    """Test the login command."""
    # Set up mocks
    mock_run.return_value = None

    # Run command with arguments
    result = runner.invoke(
        app,
        [
            "login",
            "--username",
            "testuser",
            "--password",
            "testpass",
            "--base-url",
            "https://test.inschool.fi",
        ],
    )

    # Check result
    assert result.exit_code == 0
    assert "Login successful" in result.stdout

    # Verify mock calls
    mock_run.assert_called_once()
    mock_login.assert_called_once_with(
        "testuser", "testpass", "https://test.inschool.fi", False, True
    )


@patch("wilhelminacli.cli.asyncio.run")
@patch("wilhelminacli.cli._get_messages")
def test_messages_command(mock_get_messages, mock_run, mock_messages) -> None:
    """Test the messages command."""
    # Set up mock
    mock_run.return_value = mock_messages

    # Run command with arguments
    result = runner.invoke(
        app,
        [
            "messages",
            "--username",
            "testuser",
            "--password",
            "testpass",
            "--base-url",
            "https://test.inschool.fi",
        ],
    )

    # Check result
    assert result.exit_code == 0

    # Check that messages are displayed in the table
    assert "Test message 1" in result.stdout
    assert "Test message 2" in result.stdout

    # Verify mock call
    mock_get_messages.assert_called_once_with(
        "testuser", "testpass", "https://test.inschool.fi", False, True, False
    )


@patch("wilhelminacli.cli.asyncio.run")
@patch("wilhelminacli.cli._get_message")
def test_message_command(mock_get_message, mock_run) -> None:
    """Test the message command."""
    # Set up mock
    mock_message = MagicMock()
    mock_message.subject = "Test message"
    mock_message.sender = "Teacher"
    mock_message.timestamp = "2025-04-16 13:31"
    mock_message.content_markdown = "Message content"
    mock_message.unread = True
    mock_message.allow_reply = True
    mock_message.allow_forward = True

    mock_run.return_value = mock_message

    # Run command with arguments
    result = runner.invoke(
        app, ["message", "123", "--username", "testuser", "--password", "testpass"]
    )

    # Check result
    assert result.exit_code == 0
    assert "Test message" in result.stdout
    assert "Message content" in result.stdout

    # Verify mock call
    mock_get_message.assert_called_once_with(
        123, "testuser", "testpass", "https://turku.inschool.fi", False, True
    )


@patch("wilhelminacli.cli.asyncio.run")
@patch("wilhelminacli.cli._get_message", new_callable=AsyncMock)
@patch("wilhelminacli.cli._summarize_message", new_callable=AsyncMock)
def test_message_with_summarize(mock_summarize, mock_get_message, mock_run) -> None:
    """Test the message command with summarize flag."""
    # Set up mocks
    mock_message = MagicMock()
    mock_message.subject = "Test message"
    mock_message.sender = "Teacher"
    mock_message.timestamp = "2025-04-16 13:31"
    mock_message.content_markdown = "Message content"
    mock_message.unread = True

    # Set return values
    mock_summarize.return_value = "This is a summary"

    # Mock asyncio.run for both function calls
    mock_run.side_effect = [mock_message, "This is a summary"]

    # Run command with arguments
    result = runner.invoke(
        app, ["message", "123", "--username", "testuser", "--password", "testpass", "--summarize"]
    )

    # Check result
    assert result.exit_code == 0
    assert "This is a summary" in result.stdout

    # Verify mock calls
    mock_get_message.assert_called_once()
    mock_summarize.assert_called_once_with(mock_message)
