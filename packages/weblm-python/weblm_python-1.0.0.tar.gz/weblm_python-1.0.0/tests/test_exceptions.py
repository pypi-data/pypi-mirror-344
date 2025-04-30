"""Tests for WebLM exceptions."""

from weblm._exceptions import WebLMAPIError


class TestWebLMAPIError:
    """Test suite for WebLMAPIError."""

    def test_initialization(self):
        """Test error initialization."""
        # Without status code
        error1 = WebLMAPIError(message="Test error")
        assert error1.message == "Test error"
        assert error1.status_code is None
        assert str(error1) == "Test error"

        # With status code
        error2 = WebLMAPIError(message="Not found", status_code=404)
        assert error2.message == "Not found"
        assert error2.status_code == 404
        assert str(error2) == "[404] Not found"

    def test_exception_hierarchy(self):
        """Test that WebLMAPIError is an Exception."""
        error = WebLMAPIError(message="Test error")
        assert isinstance(error, Exception)
