import json
from typing import Dict, Type, TypeVar

import aiohttp
from pydantic import BaseModel

from ._exceptions import WebLMAPIError
from ._response import ConvertResponse, ModelsResponse, ScrapeLinksResponse

T = TypeVar("T", bound=BaseModel)


class AsyncWebLM:
    """
    Asynchronous client for interacting with the WebLM API for HTML to Markdown conversion
    and link scraping using API key authentication.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.weblm.dev"):
        """
        Initialize the async WebLM client.

        Args:
            api_key: API key for authentication
            base_url: The base URL for the API (default: https://api.weblm.dev)
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._session: aiohttp.ClientSession | None = None

    def _get_headers(self) -> Dict[str, str]:
        """
        Create request headers with API key authentication.

        Returns:
            Dict[str, str]: Headers for API requests
        """
        return {"Content-Type": "application/json", "X-API-Key": self.api_key}

    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Get or create an aiohttp ClientSession.

        Returns:
            aiohttp.ClientSession: Session for making requests
        """
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _make_request(
        self, method: str, endpoint: str, data: Dict | None = None
    ) -> Dict:
        """
        Make an asynchronous request to the API.

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
        session = await self._get_session()

        try:
            if method.upper() == "GET":
                async with session.get(url, headers=headers) as response:
                    await self._check_response(response)
                    if response.content_length and response.content_length > 0:
                        return await response.json()
                    return {}
            elif method.upper() == "POST":
                async with session.post(url, headers=headers, json=data) as response:
                    await self._check_response(response)
                    if response.content_length and response.content_length > 0:
                        return await response.json()
                    return {}
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

        except aiohttp.ClientError as e:
            raise WebLMAPIError(message=str(e))

    async def _check_response(self, response: aiohttp.ClientResponse) -> None:
        """
        Check response status and raise appropriate error if needed.

        Args:
            response: aiohttp response object

        Raises:
            WebLMAPIError: If the API returns an error
        """
        if response.status >= 400:
            try:
                error_data = await response.json()
                if "detail" in error_data:
                    error_message = error_data["detail"]
                else:
                    error_message = str(error_data)
            except (ValueError, json.JSONDecodeError, aiohttp.ContentTypeError):
                error_message = await response.text()

            raise WebLMAPIError(message=error_message, status_code=response.status)

    async def convert(
        self,
        url: str,
        return_token_count: bool = False,
        model_name: str = "gemini-2.0-flash",
    ) -> ConvertResponse:
        """
        Convert HTML from URL to Markdown asynchronously.

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

        response = await self._make_request("POST", "/v1/convert", data=data)
        return ConvertResponse.model_validate(response)

    async def smart_convert(
        self,
        url: str,
        return_token_count: bool = False,
        model_name: str = "gemini-2.0-flash",
    ) -> ConvertResponse:
        """
        Convert HTML to refined Markdown using AI asynchronously.

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

        response = await self._make_request("POST", "/v1/smart-convert", data=data)
        return ConvertResponse.model_validate(response)

    async def scrape_links(
        self, url: str, include_media: bool = False, domain_only: bool = True
    ) -> ScrapeLinksResponse:
        """
        Extract links from a webpage asynchronously.

        Args:
            url: The webpage URL to scrape
            include_media: Whether to include media links
            domain_only: Whether to only include links from the same domain

        Returns:
            Dict: List of extracted URLs with the following structure:
                {
                  "urls": [
                    "https://example.com/page1",
                    "https://example.com/page2"
                  ]
                }
        """
        data = {"url": url, "include_media": include_media, "domain_only": domain_only}

        response = await self._make_request("POST", "/v1/scrape-links", data=data)
        return ScrapeLinksResponse.model_validate(response)

    async def get_models(self) -> ModelsResponse:
        """
        Get list of available language models asynchronously.

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
        response = await self._make_request("GET", "/v1/models")
        return ModelsResponse.model_validate(response)

    async def transform(self, url: str, model_class: Type[T]) -> T:
        """
        Transform web content from a URL into a specific Pydantic model asynchronously.

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

            article = await client.transform("https://example.com/article", Article)
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
        response = await self._make_request("POST", "/v1/transform", data=data)

        # Parse the response with the provided model
        return model_class.model_validate(response)

    async def close(self) -> None:
        """
        Close the aiohttp session.
        """
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        """
        Enter context manager - allows using the client with 'async with'.
        
        Returns:
            AsyncWebLM: The client instance
        """
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context manager - ensures the session is closed properly.
        
        Args:
            exc_type: Exception type if an exception was raised
            exc_val: Exception value if an exception was raised
            exc_tb: Exception traceback if an exception was raised
        """
        await self.close()
