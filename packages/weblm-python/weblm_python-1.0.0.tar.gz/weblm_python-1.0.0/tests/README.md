# WebLM Tests

This directory contains tests for the WebLM Python client library.

## Structure

The test suite is organized as follows:

- `test_client.py`: Tests for the synchronous client (`WebLM`)
- `test_async_client.py`: Tests for the asynchronous client (`AsyncWebLM`) 
- `test_response.py`: Tests for response models
- `test_exceptions.py`: Tests for exception handling
- `test_integration.py`: Integration tests demonstrating component interactions

## Running Tests

To run the tests, first install the development dependencies:

```bash
pip install -r requirements-dev.txt
```

Then, run the tests using pytest:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_client.py

# Run with coverage
pytest --cov=weblm

# Generate coverage report
pytest --cov=weblm --cov-report=html
```

## Test Strategy

The tests use mocks to simulate API responses without making actual network requests. This approach allows for:

1. **Fast execution**: Tests run quickly without network delays
2. **Deterministic results**: Tests are not affected by network issues or API changes
3. **Comprehensive testing**: Different response scenarios can be easily simulated

The main test fixtures are defined in `conftest.py` and include:

- `mock_response`: Provides sample response data for conversion endpoints
- `mock_links_response`: Provides sample response data for link scraping
- `mock_models_response`: Provides sample response data for model listings
- `mock_requests`: Mocks for the synchronous requests library
- `mock_aiohttp_session`: Mocks for the asynchronous aiohttp library

## Common Issues

### Async Tests

For async tests to work properly, you need to have `pytest-asyncio` installed. If you see errors like:

```
async def function and no async plugin installed
```

Make sure you have installed `pytest-asyncio` and added the `@pytest.mark.asyncio` decorator to your async test functions.

### URL Normalization

When testing with URLs, be aware that Pydantic's `HttpUrl` type normalizes URLs by adding a trailing slash if one isn't present. This means that if you compare:

```python
assert str(response.url) == "https://example.com"  # This may fail
```

The assertion might fail because the actual value includes a trailing slash (`https://example.com/`). Make sure your test data includes trailing slashes for URLs to match properly.

### Error Testing

When testing error conditions with the `WebLMAPIError`, make sure to use proper HTTP exceptions. Simple `Exception` objects might not be caught correctly. Use `requests.RequestException` or mock the `Response` object for synchronous tests. 