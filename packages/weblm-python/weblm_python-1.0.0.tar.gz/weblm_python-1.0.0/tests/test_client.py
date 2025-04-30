"""Tests for the synchronous WebLM client."""

from unittest.mock import MagicMock, patch

import pytest
import requests
from pydantic import BaseModel

from weblm import WebLM, WebLMAPIError
from weblm._response import ConvertResponse, ModelsResponse, ScrapeLinksResponse


class TestWebLM:
    """Test suite for WebLM synchronous client."""

    def setup_method(self):
        """Set up a test client."""
        self.client = WebLM(api_key="test_api_key")

    def test_initialization(self):
        """Test client initialization."""
        assert self.client.api_key == "test_api_key"
        assert self.client.base_url == "https://api.weblm.dev"

        # Test with custom base URL
        client = WebLM(api_key="test_api_key", base_url="https://custom.api.com/")
        assert client.base_url == "https://custom.api.com"

    def test_get_headers(self):
        """Test header generation."""
        headers = self.client._get_headers()
        assert headers == {
            "Content-Type": "application/json",
            "X-API-Key": "test_api_key",
        }

    def test_convert(self, mock_requests, mock_response):
        """Test convert method."""
        mock_get, mock_post = mock_requests
        mock_post.return_value.json.return_value = mock_response

        result = self.client.convert(url="https://example.com", return_token_count=True)

        # Check the request was made correctly
        mock_post.assert_called_once()
        assert mock_post.call_args[1]["json"] == {
            "url": "https://example.com",
            "return_token_count": True,
            "model_name": "gemini-2.0-flash",
        }

        # Check response parsing
        assert isinstance(result, ConvertResponse)
        assert result.markdown == mock_response["markdown"]
        assert str(result.url) == mock_response["url"]
        assert result.token_count == mock_response["token_count"]
        assert result.model_name == mock_response["model_name"]

    def test_smart_convert(self, mock_requests, mock_response):
        """Test smart_convert method."""
        mock_get, mock_post = mock_requests
        mock_post.return_value.json.return_value = mock_response

        result = self.client.smart_convert(
            url="https://example.com", model_name="gemini-1.5-pro"
        )

        # Check the request was made correctly
        mock_post.assert_called_once()
        assert mock_post.call_args[1]["json"] == {
            "url": "https://example.com",
            "return_token_count": False,
            "model_name": "gemini-1.5-pro",
        }

        # Check response parsing
        assert isinstance(result, ConvertResponse)
        assert result.markdown == mock_response["markdown"]

    def test_scrape_links(self, mock_requests, mock_links_response):
        """Test scrape_links method."""
        mock_get, mock_post = mock_requests
        mock_post.return_value.json.return_value = mock_links_response

        result = self.client.scrape_links(
            url="https://example.com", include_media=True, domain_only=False
        )

        # Check the request was made correctly
        mock_post.assert_called_once()
        assert mock_post.call_args[1]["json"] == {
            "url": "https://example.com",
            "include_media": True,
            "domain_only": False,
        }

        # Check response parsing
        assert isinstance(result, ScrapeLinksResponse)
        assert len(result.urls) == len(mock_links_response["urls"])
        assert [str(url) for url in result.urls] == mock_links_response["urls"]

    def test_get_models(self, mock_requests, mock_models_response):
        """Test get_models method."""
        mock_get, mock_post = mock_requests
        mock_get.return_value.json.return_value = mock_models_response

        result = self.client.get_models()

        # Check the request was made correctly
        mock_get.assert_called_once()

        # Check response parsing
        assert isinstance(result, ModelsResponse)
        assert result.models == mock_models_response["models"]

    def test_transform(self, mock_requests):
        """Test transform method."""

        # Define a test model
        class TestModel(BaseModel):
            title: str
            content: str

        # Set up mock response
        test_data = {"title": "Test Title", "content": "Test Content"}
        mock_get, mock_post = mock_requests
        mock_post.return_value.json.return_value = test_data

        # Test transform
        result = self.client.transform(url="https://example.com", model_class=TestModel)

        # Check request
        mock_post.assert_called_once()
        assert mock_post.call_args[1]["json"]["url"] == "https://example.com"
        assert "model_schema" in mock_post.call_args[1]["json"]

        # Check result
        assert isinstance(result, TestModel)
        assert result.title == "Test Title"
        assert result.content == "Test Content"

    def test_transform_invalid_model(self):
        """Test transform with invalid model class."""

        class NotAPydanticModel:
            pass

        with pytest.raises(
            ValueError, match="model_class must be a Pydantic BaseModel"
        ):
            self.client.transform(
                url="https://example.com", model_class=NotAPydanticModel
            )

    def test_api_error_handling(self):
        """Test API error handling."""
        # Create a mock HTTP error with a proper response object
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"detail": "Page not found"}

        mock_http_error = requests.HTTPError("404 Client Error")
        mock_http_error.response = mock_response

        # Patch requests.post to raise the HTTP error
        with patch("requests.post") as mock_post:
            mock_post.side_effect = mock_http_error

            with pytest.raises(WebLMAPIError) as excinfo:
                self.client.convert(url="https://example.com")

            # Now the error should contain the message from the response JSON
            assert "Page not found" in str(excinfo.value)
            assert excinfo.value.status_code == 404

    @patch("requests.post")
    def test_request_exception(self, mock_post):
        """Test handling of request exceptions."""
        # Use a more specific exception that will be caught
        mock_post.side_effect = requests.RequestException("Connection error")

        with pytest.raises(WebLMAPIError) as excinfo:
            self.client.convert(url="https://example.com")

        assert "Connection error" in str(excinfo.value)
