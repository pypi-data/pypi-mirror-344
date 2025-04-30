import json
from typing import Dict, Type, TypeVar

import requests
from pydantic import BaseModel

from ._exceptions import WebLMAPIError
from ._response import ConvertResponse, ModelsResponse, ScrapeLinksResponse

T = TypeVar("T", bound=BaseModel)


class WebLM:
    """
    Client for interacting with the WebLM API for HTML to Markdown conversion
    and link scraping using API key authentication.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.weblm.dev"):
        """
        Initialize the WebLM client.

        Args:
            api_key: API key for authentication
            base_url: The base URL for the API (default: https://api.weblm.dev)
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _get_headers(self) -> Dict[str, str]:
        """
        Create request headers with API key authentication.

        Returns:
            Dict[str, str]: Headers for API requests
        """
        return {"Content-Type": "application/json", "X-API-Key": self.api_key}

    def _make_request(
        self, method: str, endpoint: str, data: Dict | None = None
    ) -> Dict:
        """
        Make a request to the API.

        Args:
            method: HTTP method (GET, POST)
            endpoint: API endpoint
            data: Request body data

        Returns:
            Dict: API response

        Raises:
            WebLMAPIError: If the API returns an error
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()

            if response.content:
                return response.json()
            return {}

        except requests.RequestException as e:
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_data = e.response.json()
                    if "detail" in error_data:
                        error_message = error_data["detail"]
                    else:
                        error_message = str(error_data)
                except (ValueError, json.JSONDecodeError):
                    error_message = e.response.text

                raise WebLMAPIError(
                    message=error_message, status_code=e.response.status_code
                )
            raise WebLMAPIError(message=str(e))

    def convert(
        self,
        url: str,
        return_token_count: bool = False,
        model_name: str = "gemini-2.0-flash",
    ) -> ConvertResponse:
        """
        Convert HTML from URL to Markdown.

        Args:
            url: The webpage URL to convert
            return_token_count: Whether to return token count
            model_name: AI model name to use

        Returns:
            Dict: Markdown conversion result with the following structure:
                {
                  "markdown": "string",
                  "url": "https://example.com",
                  "token_count": 123,  # Only if return_token_count is true
                  "model_name": "string"  # Only if return_token_count is true
                }
        """
        data = {
            "url": url,
            "return_token_count": return_token_count,
            "model_name": model_name,
        }

        response = self._make_request("POST", "/v1/convert", data=data)
        return ConvertResponse.model_validate(response)

    def smart_convert(
        self,
        url: str,
        return_token_count: bool = False,
        model_name: str = "gemini-2.0-flash",
    ) -> ConvertResponse:
        """
        Convert HTML to refined Markdown using AI.

        Args:
            url: The webpage URL to convert
            return_token_count: Whether to return token count
            model_name: AI model name to use

        Returns:
            Dict: AI-enhanced markdown conversion result with the following structure:
                {
                  "markdown": "string",
                  "url": "https://example.com",
                  "token_count": 123,  # Only if return_token_count is true
                  "model_name": "string"  # Only if return_token_count is true
                }
        """
        data = {
            "url": url,
            "return_token_count": return_token_count,
            "model_name": model_name,
        }

        response = self._make_request("POST", "/v1/smart-convert", data=data)
        return ConvertResponse.model_validate(response)

    def scrape_links(
        self, url: str, include_media: bool = False, domain_only: bool = True
    ) -> ScrapeLinksResponse:
        """
        Extract links from a webpage.

        Args:
            url: The webpage URL to scrape
            include_media: Whether to include media links
            domain_only: Whether to only include links from the same domain

        Returns:
            ScrapeLinksResponse: List of extracted URLs with the following structure:
                {
                  "urls": [
                    "https://example.com/page1",
                    "https://example.com/page2"
                  ]
                }
        """
        data = {"url": url, "include_media": include_media, "domain_only": domain_only}

        response = self._make_request("POST", "/v1/scrape-links", data=data)
        return ScrapeLinksResponse.model_validate(response)

    def get_models(self) -> ModelsResponse:
        """
        Get list of available language models.

        Returns:
            ModelsResponse: Available models by provider with the following structure:
                {
                  "google": [
                    "models/gemini-1.5-pro",
                    "models/gemini-2.0-flash",
                    // ... other models
                  ]
                }
        """
        response = self._make_request("GET", "/v1/models")
        return ModelsResponse.model_validate(response)

    def transform(self, url: str, model_class: Type[T]) -> T:
        """
        Transform web content from a URL into a specific Pydantic model.

        The backend will scrape the URL, extract relevant data based on the model,
        and return the data in the format defined by the provided Pydantic model.

        Args:
            url: The webpage URL to transform
            model_class: Pydantic model class to use for the result format

        Returns:
            T: Instance of the provided model class with extracted data

        Example:
            ```python
            from pydantic import BaseModel

            class Article(BaseModel):
                title: str
                content: str
                author: str
                published_date: str

            article = client.transform("https://example.com/article", Article)
            print(article.title)
            ```
        """
        if not issubclass(model_class, BaseModel):
            raise ValueError("model_class must be a Pydantic BaseModel")

        # Get model schema
        model_schema = model_class.model_json_schema()

        # Prepare request data
        data = {"url": url, "model_schema": model_schema}

        # Make the request
        response = self._make_request("POST", "/v1/transform", data=data)

        # Parse the response with the provided model
        return model_class.model_validate(response)
