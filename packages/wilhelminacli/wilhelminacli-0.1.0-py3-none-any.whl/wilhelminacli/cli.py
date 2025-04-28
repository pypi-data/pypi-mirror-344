"""CLI for Wilma client."""

import asyncio
import logging
import os
from typing import List

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from wilhelmina import WilmaClient
from wilhelmina.models import Message

from wilhelminacli.utils import get_message_summarizer
from wilhelminacli.utils.interactive import run_interactive_ui

app = typer.Typer(help="CLI for Wilma school portal")
console = Console()

# Load environment variables from .env file
load_dotenv()

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, console=console)],
)


@app.command("login")
def login(
    username: str = typer.Option(None, help="Username for Wilma"),
    password: str = typer.Option(None, help="Password for Wilma", hide_input=True),
    base_url: str = typer.Option(None, help="Base URL for Wilma"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging"),
    headless: bool = typer.Option(
        True, "--headless/--no-headless", help="Run browser in headless mode"
    ),
) -> None:
    """Login to Wilma."""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("wilma").setLevel(logging.DEBUG)

    # Use environment variables if not provided as arguments
    username = username or os.environ.get("WILMA_USERNAME", "")
    password = password or os.environ.get("WILMA_PASSWORD", "")
    base_url = base_url or os.environ.get("WILMA_BASE_URL", "https://turku.inschool.fi")

    # Prompt for credentials if still not available
    if not username:
        username = typer.prompt("Username")
    if not password:
        password = typer.prompt("Password", hide_input=True)

    try:
        asyncio.run(_login(username, password, base_url, debug, headless))
        console.print("[green]Login successful![/green]")
    except Exception as e:
        console.print(f"[red]Authentication failed: {e}[/red]")


async def _login(username: str, password: str, base_url: str, debug: bool, headless: bool) -> None:
    """Internal async login function."""
    async with WilmaClient(base_url, debug=debug, headless=headless) as client:
        await client.login(username, password)


@app.command("messages")
def list_messages(
    username: str = typer.Option(None, help="Username for Wilma"),
    password: str = typer.Option(None, help="Password for Wilma", hide_input=True),
    base_url: str = typer.Option(None, help="Base URL for Wilma"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging"),
    headless: bool = typer.Option(
        True, "--headless/--no-headless", help="Run browser in headless mode"
    ),
    interactive: bool = typer.Option(False, "-i", "--interactive", help="Use interactive mode"),
    unread: bool = typer.Option(False, "-u", "--unread", help="Show only unread messages"),
    summarize: bool = typer.Option(False, "--summarize", help="Summarize unread messages with AI"),
) -> None:
    """List recent messages."""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("wilma").setLevel(logging.DEBUG)

    # Use environment variables if not provided as arguments
    username = username or os.environ.get("WILMA_USERNAME", "")
    password = password or os.environ.get("WILMA_PASSWORD", "")
    base_url = base_url or os.environ.get("WILMA_BASE_URL", "https://turku.inschool.fi")

    # Prompt for credentials if still not available
    if not username:
        username = typer.prompt("Username")
    if not password:
        password = typer.prompt("Password", hide_input=True)

    try:
        if interactive:
            # Use interactive mode
            asyncio.run(
                run_interactive_ui(
                    username=username,
                    password=password,
                    base_url=base_url,
                    debug=debug,
                    headless=headless,
                    console=console,
                    unread=unread,
                )
            )
        else:
            # Use traditional table view
            messages = asyncio.run(
                _get_messages(username, password, base_url, debug, headless, unread)
            )

            # If summarize flag is provided, summarize unread messages
            if summarize:
                unread_messages = [msg for msg in messages if msg.unread]
                if unread_messages:
                    console.print("[bold]Hämtar AI-sammanfattning av olästa meddelanden...[/bold]")
                    summary = asyncio.run(_summarize_messages(unread_messages))
                    console.print("\n[bold]Sammanfattning:[/bold]")
                    console.print(summary)
                    console.print("\n[italic]Detaljerad lista över meddelanden:[/italic]\n")
                else:
                    console.print("[bold]Inga olästa meddelanden att sammanfatta.[/bold]\n")

            table = Table(title="Messages" if not unread else "Unread Messages")
            table.add_column("ID", justify="right")
            table.add_column("Subject")
            table.add_column("Date")
            table.add_column("Sender")

            for msg in messages:
                # Format the table row based on unread status
                if msg.unread:
                    table.add_row(
                        str(msg.id),
                        f"[green]{msg.subject}[/green]",
                        f"[green]{msg.timestamp}[/green]",
                        f"[green]{msg.sender}[/green]",
                    )
                else:
                    table.add_row(
                        str(msg.id),
                        msg.subject,
                        msg.timestamp,
                        msg.sender,
                    )

            console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


async def _get_messages(
    username: str,
    password: str,
    base_url: str,
    debug: bool,
    headless: bool,
    only_unread: bool = False,
) -> List[Message]:
    """Internal async function to get messages."""
    async with WilmaClient(base_url, debug=debug, headless=headless) as client:
        await client.login(username, password)
        return await client.get_messages(only_unread=only_unread)


async def _summarize_messages(messages: List[Message]) -> str:
    """Summarize messages with AI.

    Args:
        messages: List of messages to summarize

    Returns:
        AI-generated summary of messages
    """
    try:
        MessageSummarizer = get_message_summarizer()
        summarizer = MessageSummarizer()
        result = await summarizer.summarize_messages(messages)
        return str(result)
    except Exception as e:
        logging.exception("Error summarizing messages: %s", e)
        return "Kunde inte skapa sammanfattning. Kontrollera att ANTHROPIC_API_KEY är korrekt."


async def _summarize_message(message: Message) -> str:
    """Summarize a single message with AI.

    Args:
        message: Message to summarize

    Returns:
        AI-generated summary of the message
    """
    try:
        MessageSummarizer = get_message_summarizer()
        summarizer = MessageSummarizer()
        result = await summarizer.summarize_message(message)
        return str(result)
    except Exception as e:
        logging.exception("Error summarizing message: %s", e)
        return "Kunde inte skapa sammanfattning. Kontrollera att ANTHROPIC_API_KEY är korrekt."


@app.command("message")
def show_message(
    message_id: int = typer.Argument(..., help="ID of the message to show"),
    username: str = typer.Option(None, help="Username for Wilma"),
    password: str = typer.Option(None, help="Password for Wilma", hide_input=True),
    base_url: str = typer.Option(None, help="Base URL for Wilma"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging"),
    headless: bool = typer.Option(
        True, "--headless/--no-headless", help="Run browser in headless mode"
    ),
    summarize: bool = typer.Option(False, "--summarize", help="Summarize the message with AI"),
) -> None:
    """Show a specific message."""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("wilma").setLevel(logging.DEBUG)

    # Use environment variables if not provided as arguments
    username = username or os.environ.get("WILMA_USERNAME", "")
    password = password or os.environ.get("WILMA_PASSWORD", "")
    base_url = base_url or os.environ.get("WILMA_BASE_URL", "https://turku.inschool.fi")

    # Prompt for credentials if still not available
    if not username:
        username = typer.prompt("Username")
    if not password:
        password = typer.prompt("Password", hide_input=True)

    try:
        message = asyncio.run(
            _get_message(message_id, username, password, base_url, debug, headless)
        )

        console.print(f"[bold]{message.subject}[/bold]")
        console.print(f"From: {message.sender}")
        console.print(f"Date: {message.timestamp}")
        if message.unread:
            console.print("[green]Status: Unread[/green]")

        # If summarize flag is provided, show AI summary
        if summarize:
            console.print("\n[bold]Hämtar AI-sammanfattning...[/bold]")
            summary = asyncio.run(_summarize_message(message))
            console.print("\n[bold]Sammanfattning:[/bold]")
            console.print(summary)
            console.print("\n[italic]Originalmeddelande:[/italic]")

        console.print("")
        console.print(message.content_markdown)

        if message.allow_reply:
            console.print("\n[green]You can reply to this message[/green]")
        if message.allow_forward:
            console.print("[green]You can forward this message[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


async def _get_message(
    message_id: int, username: str, password: str, base_url: str, debug: bool, headless: bool
) -> Message:
    """Internal async function to get a message."""
    async with WilmaClient(base_url, debug=debug, headless=headless) as client:
        await client.login(username, password)
        return await client.get_message_content(message_id)


@app.command("messages-summarize")
def summarize_messages(
    username: str = typer.Option(None, help="Username for Wilma"),
    password: str = typer.Option(None, help="Password for Wilma", hide_input=True),
    base_url: str = typer.Option(None, help="Base URL for Wilma"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging"),
    headless: bool = typer.Option(
        True, "--headless/--no-headless", help="Run browser in headless mode"
    ),
) -> None:
    """Summarize unread messages with AI."""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("wilma").setLevel(logging.DEBUG)

    # Use environment variables if not provided as arguments
    username = username or os.environ.get("WILMA_USERNAME", "")
    password = password or os.environ.get("WILMA_PASSWORD", "")
    base_url = base_url or os.environ.get("WILMA_BASE_URL", "https://turku.inschool.fi")

    # Prompt for credentials if still not available
    if not username:
        username = typer.prompt("Username")
    if not password:
        password = typer.prompt("Password", hide_input=True)

    try:
        # Get unread messages
        messages = asyncio.run(
            _get_messages(username, password, base_url, debug, headless, only_unread=True)
        )

        if not messages:
            console.print("[bold]Inga olästa meddelanden att sammanfatta.[/bold]")
            return

        console.print("[bold]Hämtar AI-sammanfattning av olästa meddelanden...[/bold]")
        summary = asyncio.run(_summarize_messages(messages))
        console.print("\n[bold]Sammanfattning:[/bold]")
        console.print(summary)

        # Show table with messages
        console.print("\n[italic]Lista över olästa meddelanden:[/italic]\n")
        table = Table(title="Unread Messages")
        table.add_column("ID", justify="right")
        table.add_column("Subject")
        table.add_column("Date")
        table.add_column("Sender")

        for msg in messages:
            table.add_row(
                str(msg.id),
                f"[green]{msg.subject}[/green]",
                f"[green]{msg.timestamp}[/green]",
                f"[green]{msg.sender}[/green]",
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    app()
