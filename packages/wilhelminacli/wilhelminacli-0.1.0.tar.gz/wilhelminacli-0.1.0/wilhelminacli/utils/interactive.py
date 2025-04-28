"""Interactive terminal UI for Wilma client."""

import asyncio
import time
from typing import Any, Callable, Dict, List, Optional

from rich.console import Console
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, Markdown, OptionList, Static
from textual.widgets.option_list import Option
from wilhelmina import WilmaClient
from wilhelmina.models import Message

from wilhelminacli.utils import get_message_summarizer


def filter_unread_messages(messages: List[Message]) -> List[Message]:
    return [message for message in messages if message.unread]


def format_message_text(message: Message) -> str:
    """Format message text for display."""
    # Escape square brackets to prevent markup interpretation
    message_id = str(message.id).replace("[", "\\[").replace("]", "\\]")
    subject = message.subject.replace("[", "\\[").replace("]", "\\]")
    sender = message.sender.replace("[", "\\[").replace("]", "\\]")

    if message.unread:
        return f"[green]{message.timestamp} - {subject} [italic]from[/italic] {sender} ({message_id})[/green]"
    return f"{message.timestamp} - {subject} [italic]from {sender}[/italic] ({message_id})"


class MessagesScreen(Screen[Any]):
    """Screen showing the list of messages."""

    BINDINGS = [
        ("escape", "app.quit", "Quit"),
        ("q", "app.quit", "Quit"),
        ("u", "toggle_unread", "Toggle Unread"),
    ]

    def __init__(
        self,
        messages: List[Message],
        all_messages: List[Message],
        on_select_message: Callable[[int], None],
        on_toggle_unread: Callable[[], None],
        show_unread_only: bool = False,
        name: Optional[str] = None,
    ):
        """Initialize with messages and callback."""
        super().__init__(name=name)
        self.messages = messages
        self.all_messages = all_messages
        self.on_select_message = on_select_message
        self.on_toggle_unread = on_toggle_unread
        self.show_unread_only = show_unread_only
        # Map option indices to message ids
        self.message_map: Dict[str, int] = {}

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        title_text = "Unread Messages" if self.show_unread_only else "Messages"
        status_text = (
            "Press 'u' to show all messages"
            if self.show_unread_only
            else "Press 'u' to show only unread"
        )

        yield Header(show_clock=True)
        yield Label(f"{title_text} ({status_text})", id="messages-title")
        yield self._create_messages_list()
        yield Footer()

    def _create_messages_list(self) -> OptionList:
        """Create the messages list widget."""
        messages_list = OptionList(id="messages-list")

        for i, message in enumerate(self.messages):
            option_id = f"msg-{i}"
            # Create the option with unique ID
            option = Option(format_message_text(message), id=option_id)
            # Store the message ID in our map
            self.message_map[option_id] = message.id
            messages_list.add_option(option)

        return messages_list

    @on(OptionList.OptionSelected)
    def handle_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle message selection."""
        # Get the message ID from our map using the option's ID
        if event.option.id and event.option.id in self.message_map:
            message_id = self.message_map[event.option.id]
            self.on_select_message(message_id)

    def action_toggle_unread(self) -> None:
        """Toggle between showing all messages and only unread messages."""
        self.on_toggle_unread()


class MessageDetailScreen(Screen[Any]):
    """Screen showing the details of a message."""

    BINDINGS = [
        ("escape", "go_back", "Back"),
        ("q", "app.quit", "Quit"),
        ("s", "summarize", "Summarize"),
    ]

    def __init__(
        self,
        message: Message,
        on_back: Callable[[], None],
        existing_summary: Optional[str] = None,
        name: Optional[str] = None,
    ):
        """Initialize with message content and callback."""
        super().__init__(name=name)
        self.message = message
        self.on_back = on_back
        self.summary = existing_summary
        self.summarizing = False
        self.show_summary = existing_summary is not None
        self.spinner_task: Optional[asyncio.Task[None]] = None

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header(show_clock=True)

        # Message header section
        yield Container(
            Label(self.message.subject, id="message-title"),
            Label(f"{self.message.timestamp} · {self.message.sender}", id="message-metadata"),
            id="header-container",
        )

        # Main content area - dynamically adjusts based on summary state
        if self.show_summary:
            # Split view mode when summary is shown
            yield Horizontal(
                # Left panel - Original message
                Vertical(
                    Label("Original message", id="message-section-label"),
                    ScrollableContainer(
                        Markdown(self.message.content_markdown),
                        id="message-content",
                    ),
                    id="original-message-container",
                ),
                # Right panel - Summary
                Vertical(
                    Label("AI Summary", id="summary-section-label"),
                    ScrollableContainer(
                        Markdown(self.summary or ""),
                        id="summary-content",
                    ),
                    id="summary-container",
                ),
                id="split-content-container",
            )
        else:
            # Full view mode when no summary
            yield Vertical(
                ScrollableContainer(
                    Markdown(self.message.content_markdown),
                    id="message-content-full",
                ),
                id="full-content-container",
            )

        # Status bar for summary progress with extra visible indicators
        summary_status = ""
        if self.summarizing:
            summary_status = "⏳ LOADING: Fetching summary from Claude AI... ⏳"
        elif self.summary:
            summary_status = "✅ SUCCESS: Summary available ✅"
        else:
            summary_status = "💡 TIP: Press S to summarize with Claude AI 💡"

        # Create a dedicated status area that will stand out
        yield Container(
            Static(summary_status, id="summary-status"),
            id="status-container",
            classes="status-normal",
        )

        # Footer at the bottom
        yield Footer()

    def action_go_back(self) -> None:
        """Go back to messages list."""
        self.on_back()

    def update_status(self, message: str, status_type: str = "normal") -> None:
        """Update the status message and container appearance.

        Args:
            message: The message to display
            status_type: Status type ("normal", "loading", "success", "error")
        """
        try:
            # Update the status text
            status_widget = self.query_one("#summary-status", Static)
            status_widget.update(message)

            # Update the container class based on status type
            status_container = self.query_one("#status-container", Container)

            # Remove any existing status classes
            for class_name in ["status-normal", "status-loading", "status-success", "status-error"]:
                if status_container.has_class(class_name):
                    status_container.remove_class(class_name)

            # Add the new status class
            status_container.add_class(f"status-{status_type}")

        except Exception as e:
            self.log(f"Error updating status: {e}")

    def start_spinner(self) -> None:
        """Start a spinning animation in the status text."""

        async def spin() -> None:
            spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            stages = [
                "Connecting to Claude API...",
                "Preparing request...",
                "Sending data to Claude...",
                "Claude is thinking...",
                "Claude is analyzing the message...",
                "Creating summary...",
            ]
            idx = 0
            stage_idx = 0
            stage_changes = 0
            try:
                while self.summarizing:
                    # Update spinner character
                    char = spinner_chars[idx % len(spinner_chars)]

                    # Change the message occasionally to show progress
                    if idx % 30 == 0 and stage_changes < len(stages):
                        stage_idx = stage_changes
                        stage_changes += 1

                    # Get current stage message
                    stage_msg = stages[stage_idx % len(stages)]

                    # Update the status with spinner and current stage - make it more noticeable
                    self.update_status(f"[{char}] {stage_msg} [{char}]", "loading")

                    # Increment and sleep
                    idx += 1
                    await asyncio.sleep(0.1)
            except Exception as e:
                self.log(f"Spinner error: {e}")

        if self.spinner_task:
            self.spinner_task.cancel()
        self.spinner_task = asyncio.create_task(spin())

    def action_summarize(self) -> None:
        """Summarize the message with AI."""
        # Don't do anything if already summarizing
        if self.summarizing:
            return

        self.summarizing = True
        self.update_status("⏳ Connecting to Claude API...", "loading")
        self.start_spinner()

        async def get_summary() -> None:
            try:
                MessageSummarizer = get_message_summarizer()
                summarizer = MessageSummarizer()

                start_time = time.time()

                try:
                    # Update status to show we're now summarizing
                    self.update_status("⏳ Claude is analyzing the message...", "loading")

                    # Get the summary
                    self.summary = await summarizer.summarize_message(self.message)
                    elapsed = time.time() - start_time

                    # Update status and appearance
                    self.summarizing = False
                    self.show_summary = True
                    self.update_status(f"✓ Summary ready (took {elapsed:.1f}s)", "success")

                    # Recreate the screen with the new layout
                    current_screen = self.app.screen
                    if isinstance(current_screen, MessageDetailScreen):
                        self.app.pop_screen()
                        new_screen = MessageDetailScreen(
                            message=self.message,
                            on_back=self.on_back,
                            existing_summary=self.summary,
                        )
                        self.app.push_screen(new_screen)

                except ValueError as e:
                    self.summarizing = False
                    error_msg = (
                        "ANTHROPIC_API_KEY not set" if "ANTHROPIC_API_KEY" in str(e) else str(e)
                    )
                    self.update_status(f"⚠️ Error: {error_msg}", "error")

                except Exception as e:
                    self.summarizing = False
                    self.update_status(f"⚠️ API error: {str(e)}", "error")

            except Exception as e:
                self.summarizing = False
                self.update_status(f"⚠️ Error: {str(e)}", "error")

            finally:
                if self.spinner_task:
                    self.spinner_task.cancel()

        asyncio.create_task(get_summary())


class WilmaApp(App[Any]):
    """Textual app for Wilma client."""

    TITLE = "Wilma Client"
    CSS = """
    /* Global styles and theme */
    Screen {
        background: $surface;
        layers: base overlay;
    }

    /* Messages list screen */
    #messages-title {
        dock: top;
        padding: 1;
        background: $boost;
        color: $text;
        text-align: center;
        text-style: bold;
        width: 100%;
        height: 3;
    }

    #messages-list {
        width: 100%;
        height: 1fr;
        border: solid $primary;
        padding: 0;
    }

    OptionList > .option {
        padding: 1;
    }

    OptionList > .option.--highlight {
        background: $accent;
    }

    /* Message detail screen */
    #header-container {
        width: 100%;
        height: auto;
        padding: 1;
        background: $boost;
        border-bottom: solid $primary;
    }

    #message-title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        text-align: center;
    }

    #message-metadata {
        width: 100%;
        text-align: center;
        color: $text-muted;
    }

    /* Full content view (no summary) */
    #full-content-container {
        width: 100%;
        height: 1fr;
    }

    #message-content-full {
        width: 100%;
        height: 1fr;
        padding: 1;
    }

    /* Split view (with summary) */
    #split-content-container {
        width: 100%;
        height: 1fr;
    }

    #original-message-container {
        width: 1fr;
        height: 1fr;
        border-right: solid $primary;
    }

    #summary-container {
        width: 2fr;
        height: 1fr;
    }

    #message-section-label, #summary-section-label {
        background: $primary-darken-1;
        color: $text;
        padding: 1;
        width: 100%;
        text-align: center;
    }

    #summary-section-label {
        background: $success-darken-1;
    }

    #message-content, #summary-content {
        width: 100%;
        height: 1fr;
        padding: 1;
    }

    #summary-content {
        background: $success 10%;
    }

    /* Status container - make it more visible and prominent */
    #status-container {
        dock: bottom;
        width: 100%;
        height: auto;
        min-height: 3;
        margin-top: 1;
        margin-bottom: 1;
        border: solid $primary;
        padding: 1;
    }

    #status-container.status-normal {
        background: $surface;
        border-title-color: $primary;
    }

    #status-container.status-loading {
        background: $warning 30%;
        border-title-color: $warning;
        color: $warning;
    }

    #status-container.status-success {
        background: $success 30%;
        border-title-color: $success;
        color: $success;
    }

    #status-container.status-error {
        background: $error 30%;
        border-title-color: $error;
        color: $error;
    }

    #summary-status {
        width: 100%;
        height: auto;
        padding: 0 1;
        text-align: center;
        text-style: bold;
        display: block;   /* Ensure it's displayed as a block */
        box-sizing: border-box;  /* Include padding in element size */
    }
    """

    def __init__(
        self,
        client: WilmaClient,
        messages: List[Message],
        console: Console,
        show_unread_only: bool = False,
    ):
        """Initialize with client and messages."""
        super().__init__()
        self.wilma_client = client
        self.all_messages = messages
        self.show_unread_only = show_unread_only
        self.console = console

        # Filter messages if needed
        if self.show_unread_only:
            self.filtered_messages = filter_unread_messages(self.all_messages)
        else:
            self.filtered_messages = self.all_messages

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Container()  # Placeholder

    def on_mount(self) -> None:
        """Set up the app on mount."""
        self.push_screen(
            MessagesScreen(
                self.filtered_messages,
                self.all_messages,
                self.show_message_detail,
                self.toggle_unread_filter,
                self.show_unread_only,
            )
        )

    def toggle_unread_filter(self) -> None:
        """Toggle between showing all messages and only unread messages."""
        self.show_unread_only = not self.show_unread_only

        # Update filtered messages
        if self.show_unread_only:
            self.filtered_messages = filter_unread_messages(self.all_messages)
        else:
            self.filtered_messages = self.all_messages

        # Replace the current screen with a new one showing the updated message list
        self.pop_screen()
        self.push_screen(
            MessagesScreen(
                self.filtered_messages,
                self.all_messages,
                self.show_message_detail,
                self.toggle_unread_filter,
                self.show_unread_only,
            )
        )

    def show_message_detail(self, message_id: int) -> None:
        """Show message detail screen."""

        async def get_message() -> None:
            try:
                message = await self.wilma_client.get_message_content(message_id)
                self.push_screen(MessageDetailScreen(message, self.show_messages, None))
            except Exception as e:
                self.console.print(f"[red]Error loading message: {e}[/red]")
                self.exit()

        asyncio.create_task(get_message())

    def show_messages(self) -> None:
        """Show messages screen."""
        self.pop_screen()

    async def action_quit(self) -> None:
        """Quit the application."""
        self.exit()


async def run_interactive_ui(
    username: str,
    password: str,
    base_url: str,
    debug: bool = False,
    headless: bool = True,
    console: Optional[Console] = None,
    unread: bool = False,
) -> None:
    """Run the interactive UI.

    Args:
        username: Username for Wilma
        password: Password for Wilma
        base_url: Base URL for Wilma
        debug: Enable debug logging
        headless: Run browser in headless mode
        console: Rich console to use for output
        unread: Show only unread messages
    """
    if console is None:
        console = Console()

    try:
        async with WilmaClient(base_url, debug=debug, headless=headless) as client:
            console.print("Logging in...")
            await client.login(username, password)

            console.print("Fetching messages...")
            # Get all messages - filtering will happen in the UI
            messages = await client.get_messages()

            # Run the Textual app with the unread flag
            app = WilmaApp(client, messages, console, show_unread_only=unread)
            await app.run_async()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
