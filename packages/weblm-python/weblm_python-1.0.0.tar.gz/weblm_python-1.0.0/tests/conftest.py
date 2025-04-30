"""Pytest fixtures for the weblm tests."""

from unittest.mock import AsyncMock, Mock, patch

import pytest


@pytest.fixture
def mock_response():
    """Create a mock response with common data."""
    return {
        "markdown": "# Test Markdown\n\nThis is a test.",
        "url": "https://example.com/",
        "token_count": 100,
        "model_name": "gemini-2.0-flash",
    }


@pytest.fixture
def mock_links_response():
    """Create a mock links response."""
    return {"urls": ["https://example.com/page1", "https://example.com/page2"]}


@pytest.fixture
def mock_models_response():
    """Create a mock models response."""
    return {"models": {"google": ["models/gemini-1.5-pro", "models/gemini-2.0-flash"]}}


@pytest.fixture
def mock_requests():
    """Patch requests.get and requests.post methods."""
    with patch("requests.get") as mock_get, patch("requests.post") as mock_post:
        response = Mock()
        response.status_code = 200
        response.raise_for_status.return_value = None
        response.json.return_value = {}
        response.content = True

        mock_get.return_value = response
        mock_post.return_value = response

        yield mock_get, mock_post


class AsyncContextManagerMock:
    """Mock class that simulates an async context manager."""

    def __init__(self, response):
        self.response = response

    async def __aenter__(self):
        return self.response

    async def __aexit__(self, exc_type, exc, tb):
        pass


@pytest.fixture
def mock_aiohttp_session():
    """Patch aiohttp.ClientSession for async tests."""
    # Create a mock response object
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.content_length = 100
    mock_response.json = AsyncMock(return_value={})

    # Create context manager mocks for get and post methods
    get_context = AsyncContextManagerMock(mock_response)
    post_context = AsyncContextManagerMock(mock_response)

    # Create a mock session
    mock_session = AsyncMock()

    # Make get and post return the context managers rather than coroutines
    mock_session.get = Mock(return_value=get_context)
    mock_session.post = Mock(return_value=post_context)
    mock_session.closed = False

    # Patch the ClientSession class
    with patch("aiohttp.ClientSession") as session_class:
        session_class.return_value = mock_session
        yield session_class, mock_response
