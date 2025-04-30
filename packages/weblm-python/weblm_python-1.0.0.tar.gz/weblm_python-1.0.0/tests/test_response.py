"""Tests for response models."""

import pytest
from pydantic import ValidationError

from weblm._response import ConvertResponse, ModelsResponse, ScrapeLinksResponse


class TestConvertResponse:
    """Test suite for ConvertResponse model."""

    def test_valid_data(self):
        """Test with valid data."""
        data = {
            "markdown": "# Test Markdown\n\nThis is a test.",
            "url": "https://example.com/",
            "token_count": 100,
            "model_name": "gemini-2.0-flash",
        }

        response = ConvertResponse.model_validate(data)

        assert response.markdown == data["markdown"]
        assert str(response.url) == data["url"]
        assert response.token_count == data["token_count"]
        assert response.model_name == data["model_name"]

    def test_minimal_data(self):
        """Test with minimal required data."""
        data = {"markdown": "# Test Markdown", "url": "https://example.com/"}

        response = ConvertResponse.model_validate(data)

        assert response.markdown == data["markdown"]
        assert str(response.url) == data["url"]
        assert response.token_count is None
        assert response.model_name is None

    def test_invalid_url(self):
        """Test with invalid URL."""
        data = {
            "markdown": "# Test Markdown",
            "url": "not-a-url",  # Invalid URL
        }

        with pytest.raises(ValidationError):
            ConvertResponse.model_validate(data)

    def test_missing_required(self):
        """Test with missing required fields."""
        # Missing markdown
        data1 = {"url": "https://example.com"}

        with pytest.raises(ValidationError):
            ConvertResponse.model_validate(data1)

        # Missing url
        data2 = {"markdown": "# Test Markdown"}

        with pytest.raises(ValidationError):
            ConvertResponse.model_validate(data2)


class TestScrapeLinksResponse:
    """Test suite for ScrapeLinksResponse model."""

    def test_valid_data(self):
        """Test with valid data."""
        data = {"urls": ["https://example.com/page1", "https://example.com/page2"]}

        response = ScrapeLinksResponse.model_validate(data)

        assert len(response.urls) == 2
        assert [str(url) for url in response.urls] == data["urls"]

    def test_empty_list(self):
        """Test with empty list of URLs."""
        data = {"urls": []}

        response = ScrapeLinksResponse.model_validate(data)

        assert len(response.urls) == 0

    def test_invalid_urls(self):
        """Test with invalid URLs."""
        data = {
            "urls": [
                "https://example.com",
                "not-a-url",  # Invalid URL
            ]
        }

        with pytest.raises(ValidationError):
            ScrapeLinksResponse.model_validate(data)

    def test_missing_urls(self):
        """Test with missing urls field."""
        data = {}

        with pytest.raises(ValidationError):
            ScrapeLinksResponse.model_validate(data)


class TestModelsResponse:
    """Test suite for ModelsResponse model."""

    def test_valid_data(self):
        """Test with valid data."""
        data = {
            "models": {
                "google": ["models/gemini-1.5-pro", "models/gemini-2.0-flash"],
                "anthropic": ["models/claude-3-opus"],
            }
        }

        response = ModelsResponse.model_validate(data)

        assert len(response.models) == 2
        assert "google" in response.models
        assert "anthropic" in response.models
        assert len(response.models["google"]) == 2
        assert len(response.models["anthropic"]) == 1

    def test_empty_providers(self):
        """Test with empty providers."""
        data = {"models": {}}

        response = ModelsResponse.model_validate(data)

        assert len(response.models) == 0

    def test_empty_models(self):
        """Test with provider with empty models list."""
        data = {"models": {"google": []}}

        response = ModelsResponse.model_validate(data)

        assert len(response.models) == 1
        assert len(response.models["google"]) == 0

    def test_missing_models(self):
        """Test with missing models field."""
        data = {}

        with pytest.raises(ValidationError):
            ModelsResponse.model_validate(data)
