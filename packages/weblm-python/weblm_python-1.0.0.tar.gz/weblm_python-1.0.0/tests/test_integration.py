"""Integration tests for the weblm package.

These tests demonstrate how different components work together.
Note: These tests use mocks and don't make actual API calls.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import requests
from pydantic import BaseModel

from weblm import AsyncWebLM, WebLM, WebLMAPIError


class TestIntegration:
    """Integration test suite for WebLM package."""

    def test_error_propagation(self):
        """Test error propagation through the client."""
        # Create a mock HTTP error with a proper response object
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"detail": "Internal Server Error"}

        mock_http_error = requests.HTTPError("500 Server Error")
        mock_http_error.response = mock_response

        # Patch requests.post to raise the HTTP error
        with patch("requests.post") as mock_post:
            mock_post.side_effect = mock_http_error

            # Create client and test error propagation
            client = WebLM(api_key="test_key")

            with pytest.raises(WebLMAPIError) as excinfo:
                client.convert(url="https://example.com")

            # Verify error details
            assert "Internal Server Error" in str(excinfo.value)
            assert excinfo.value.status_code == 500

    def test_model_transformation(self, mock_requests):
        """Test transforming web content into a custom model."""

        # Define a custom model
        class Article(BaseModel):
            title: str
            content: str
            author: str = None

        # Set up mock response
        article_data = {
            "title": "Test Article",
            "content": "This is the article content.",
            "author": "Test Author",
        }

        mock_get, mock_post = mock_requests
        mock_post.return_value.json.return_value = article_data

        # Create client and transform
        client = WebLM(api_key="test_key")
        article = client.transform(url="https://example.com", model_class=Article)

        # Verify transformation
        assert isinstance(article, Article)
        assert article.title == "Test Article"
        assert article.content == "This is the article content."
        assert article.author == "Test Author"

        # Verify request contained model schema
        _, kwargs = mock_post.call_args
        assert "json" in kwargs
        assert "model_schema" in kwargs["json"]
        assert kwargs["json"]["model_schema"]["properties"]["title"]["type"] == "string"

    @pytest.mark.asyncio
    async def test_async_workflow(
        self, mock_aiohttp_session, mock_response, mock_links_response
    ):
        """Test async workflow combining multiple operations."""
        import asyncio

        # Set up mocks - we need to access the context manager's returned value
        _, cm_response = mock_aiohttp_session

        # Create a counter to toggle between responses
        response_counter = {"count": 0}

        # Configure json to return different responses based on call count
        async def json_side_effect(*args, **kwargs):
            response_counter["count"] += 1

            if response_counter["count"] == 1:
                return mock_response
            else:
                return mock_links_response

        cm_response.json = AsyncMock(side_effect=json_side_effect)

        # Create client
        client = AsyncWebLM(api_key="test_key")

        try:
            # Run concurrent operations
            convert_task = client.convert(url="https://example.com")
            links_task = client.scrape_links(url="https://example.com")

            # Wait for both to complete
            convert_result, links_result = await asyncio.gather(
                convert_task, links_task
            )

            # Verify results
            assert convert_result.markdown == mock_response["markdown"]
            assert len(links_result.urls) == len(mock_links_response["urls"])

        finally:
            # Clean up
            await client.close()
