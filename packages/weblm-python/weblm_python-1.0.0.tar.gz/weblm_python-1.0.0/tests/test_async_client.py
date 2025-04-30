"""Tests for the asynchronous WebLM client."""

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest
from pydantic import BaseModel

from weblm import AsyncWebLM, WebLMAPIError
from weblm._response import ConvertResponse, ModelsResponse, ScrapeLinksResponse


class TestAsyncWebLM:
    """Test suite for AsyncWebLM client."""

    def setup_method(self):
        """Set up a test client."""
        self.client = AsyncWebLM(api_key="test_api_key")

    def teardown_method(self):
        """Clean up after tests."""
        if self.client._session is not None and not self.client._session.closed:
            # Use a safer approach compatible with newer asyncio
            try:
                asyncio.run(self.client.close())
            except RuntimeError:
                # Handle case where there's already a running event loop
                pass

    def test_initialization(self):
        """Test client initialization."""
        assert self.client.api_key == "test_api_key"
        assert self.client.base_url == "https://api.weblm.dev"
        assert self.client._session is None

        # Test with custom base URL
        client = AsyncWebLM(api_key="test_api_key", base_url="https://custom.api.com/")
        assert client.base_url == "https://custom.api.com"

    def test_get_headers(self):
        """Test header generation."""
        headers = self.client._get_headers()
        assert headers == {
            "Content-Type": "application/json",
            "X-API-Key": "test_api_key",
        }

    @pytest.mark.asyncio
    async def test_get_session(self, mock_aiohttp_session):
        """Test session creation."""
        mock_session_class, _ = mock_aiohttp_session

        session = await self.client._get_session()
        assert session is not None
        mock_session_class.assert_called_once()

        # Test session reuse
        second_session = await self.client._get_session()
        assert second_session is session
        assert mock_session_class.call_count == 1

    @pytest.mark.asyncio
    async def test_convert(self, mock_aiohttp_session, mock_response):
        """Test convert method."""
        _, mock_response_obj = mock_aiohttp_session
        mock_response_obj.json = AsyncMock(return_value=mock_response)

        result = await self.client.convert(
            url="https://example.com", return_token_count=True
        )

        # Check response parsing
        assert isinstance(result, ConvertResponse)
        assert result.markdown == mock_response["markdown"]
        assert str(result.url) == mock_response["url"]
        assert result.token_count == mock_response["token_count"]
        assert result.model_name == mock_response["model_name"]

    @pytest.mark.asyncio
    async def test_smart_convert(self, mock_aiohttp_session, mock_response):
        """Test smart_convert method."""
        _, mock_response_obj = mock_aiohttp_session
        mock_response_obj.json = AsyncMock(return_value=mock_response)

        result = await self.client.smart_convert(
            url="https://example.com", model_name="gemini-1.5-pro"
        )

        # Check response parsing
        assert isinstance(result, ConvertResponse)
        assert result.markdown == mock_response["markdown"]

    @pytest.mark.asyncio
    async def test_scrape_links(self, mock_aiohttp_session, mock_links_response):
        """Test scrape_links method."""
        _, mock_response_obj = mock_aiohttp_session
        mock_response_obj.json = AsyncMock(return_value=mock_links_response)

        result = await self.client.scrape_links(
            url="https://example.com", include_media=True, domain_only=False
        )

        # Check response parsing
        assert isinstance(result, ScrapeLinksResponse)
        assert len(result.urls) == len(mock_links_response["urls"])
        assert [str(url) for url in result.urls] == mock_links_response["urls"]

    @pytest.mark.asyncio
    async def test_get_models(self, mock_aiohttp_session, mock_models_response):
        """Test get_models method."""
        _, mock_response_obj = mock_aiohttp_session
        mock_response_obj.json = AsyncMock(return_value=mock_models_response)

        result = await self.client.get_models()

        # Check response parsing
        assert isinstance(result, ModelsResponse)
        assert result.models == mock_models_response["models"]

    @pytest.mark.asyncio
    async def test_transform(self, mock_aiohttp_session):
        """Test transform method."""

        # Define a test model
        class TestModel(BaseModel):
            title: str
            content: str

        # Set up mock response
        test_data = {"title": "Test Title", "content": "Test Content"}
        _, mock_response_obj = mock_aiohttp_session
        mock_response_obj.json = AsyncMock(return_value=test_data)

        # Test transform
        result = await self.client.transform(
            url="https://example.com", model_class=TestModel
        )

        # Check result
        assert isinstance(result, TestModel)
        assert result.title == "Test Title"
        assert result.content == "Test Content"

    @pytest.mark.asyncio
    async def test_transform_invalid_model(self):
        """Test transform with invalid model class."""

        class NotAPydanticModel:
            pass

        with pytest.raises(
            ValueError, match="model_class must be a Pydantic BaseModel"
        ):
            await self.client.transform(
                url="https://example.com", model_class=NotAPydanticModel
            )

    @pytest.mark.asyncio
    async def test_api_error_handling(self, mock_aiohttp_session):
        """Test API error handling."""
        _, mock_response_obj = mock_aiohttp_session

        # Simulate a 404 error
        mock_response_obj.status = 404
        mock_response_obj.json = AsyncMock(return_value={"detail": "Page not found"})

        with pytest.raises(WebLMAPIError) as excinfo:
            await self.client.convert(url="https://example.com")

        assert "Page not found" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_close(self):
        """Test close method."""
        # Create a mock session
        mock_session = Mock()
        mock_session.closed = False
        mock_session.close = AsyncMock()

        # Assign it to the client
        self.client._session = mock_session

        # Call close
        await self.client.close()

        # Check close was called
        mock_session.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_no_session(self):
        """Test close method when no session exists."""
        # Ensure no session exists
        self.client._session = None

        # Call close (should not raise)
        await self.client.close()

    @pytest.mark.asyncio
    async def test_context_manager(self, mock_aiohttp_session):
        """Test using AsyncWebLM as an async context manager."""
        # Setup the mocks
        mock_session_class, mock_response_obj = mock_aiohttp_session
        session_instance = mock_session_class.return_value
        mock_response_obj.json = AsyncMock(return_value={
            "markdown": "# Test",
            "url": "https://example.com"
        })
        
        # Use the client as a context manager
        async with AsyncWebLM(api_key="test_api_key") as client:
            # Perform an operation to create a session
            result = await client.convert(url="https://example.com")
            assert result.markdown == "# Test"
            assert client._session is not None
            assert not client._session.closed
            
        # After exiting the context, session.close() should have been called
        session_instance.close.assert_called_once()
