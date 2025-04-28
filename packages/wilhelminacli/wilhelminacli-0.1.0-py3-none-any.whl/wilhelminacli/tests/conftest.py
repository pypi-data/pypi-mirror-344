"""Test configuration."""

import logging
from typing import Generator

import pytest


def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line("markers", "asyncio: mark test as an asyncio test")


@pytest.fixture(autouse=True)
def disable_logging() -> Generator[None, None, None]:
    """Disable logging for tests."""
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)
