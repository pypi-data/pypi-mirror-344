# Wilma CLI

A command-line interface for the Wilma school platform. This CLI allows you to authenticate, list messages, and view message contents from the Wilma platform using both regular and interactive modes.

## Features

- Command-line interface with typer and rich
- Interactive terminal UI for browsing and reading messages
- Message summarization using Claude AI
- Supports environment variables for configuration

## Installation

```bash
# Using pip
pip install wilhelminacli
pip install playwright
playwright install chromium

# Using Poetry
poetry add wilhelminacli
poetry run playwright install chromium
```

## Configuration

You can configure the client using a `.env` file in your project root directory. Create one by copying the example file:

```bash
cp .env.example .env
```

Then edit the file with your credentials:

```
WILMA_USERNAME=your_username
WILMA_PASSWORD=your_password
WILMA_BASE_URL=https://your-school.inschool.fi  # Optional
ANTHROPIC_API_KEY=your_api_key  # For message summarization
```

## CLI Usage

The package includes a command-line interface for easy testing and usage:

```bash
# Login to test credentials
wilma login

# Login with credentials from .env file
wilma login

# List messages (use --no-headless to see the browser)
wilma messages --no-headless

# Show a specific message
wilma message 12345

# Debug mode with visible browser
wilma messages --debug --no-headless

# Interactive mode with message browser UI
wilma messages -i

# Show only unread messages
wilma messages --unread

# Summarize unread messages with AI
wilma messages-summarize
```

### Interactive Mode

The interactive mode (`-i` flag) provides a terminal-based UI for browsing and reading messages:

- Navigate the message list using arrow keys
- Select a message with Enter to view its full content
- Press Escape or 'b' to go back from message detail to the message list
- Press Escape or 'q' to quit from the message list

Features of the interactive UI:
- Full-screen terminal interface
- Unread messages highlighted in green
- Message content displayed with proper formatting
- Navigation between message list and message detail screens

## AI Message Summarization

The CLI includes optional AI-powered message summarization using Anthropic's Claude API:

```bash
# Summarize a specific message
wilma message 12345 --summarize

# Summarize all unread messages
wilma messages-summarize
```

To use the summarization feature, you need to set the `ANTHROPIC_API_KEY` environment variable in your `.env` file.

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/frwickst/wilhelminacli.git
cd wilhelminacli

# Install development dependencies
poetry install

# Install Playwright browser
poetry run playwright install chromium
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=wilhelminacli
```

### Linting and Type Checking

```bash
# Format with ruff
poetry run ruff format wilhelminacli

# Run ruff for linting
poetry run ruff check wilhelminacli --fix

# Run mypy for type checking
poetry run mypy wilhelminacli
```

## License

MIT
