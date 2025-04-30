class WebLMAPIError(Exception):
    """Exception raised for WebLM API errors."""

    def __init__(self, message: str, status_code: int | None = None):
        """
        Initialize WebLM API Error.

        Args:
            message: Error message
            status_code: HTTP status code
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self):
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message
