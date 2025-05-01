"""
API Exceptions
=============

This module contains exceptions related to external API interactions.
These exceptions are used when making requests to external APIs and handling responses.

Examples:
---------

```python
from unifyops_core.exceptions import ApiClientError

# Raise an API client configuration error
raise ApiClientError(
    message="Invalid API client configuration",
    details=[{"loc": ["api_key"], "msg": "API key is missing"}]
)

# Raise an API response error
from unifyops_core.exceptions import ApiResponseError

raise ApiResponseError(
    message="Failed to parse API response",
    details=[{"loc": ["response", "data"], "msg": "Unexpected response format"}],
    status_code=502
)
"""

from fastapi import status
from unifyops_core.exceptions.base import AppException


class ApiError(AppException):
    """Base exception for all API-related errors."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_type = "api_error"


class ApiClientError(ApiError):
    """
    Exception raised when there's an error with the API client configuration
    or request preparation.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    error_type = "api_client_error"


class ApiResponseError(ApiError):
    """
    Exception raised when there's an error processing or parsing the API response.
    """
    status_code = status.HTTP_502_BAD_GATEWAY
    error_type = "api_response_error"


class ApiAuthenticationError(ApiError):
    """
    Exception raised when authentication with an external API fails.
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    error_type = "api_authentication_error"


class ApiRateLimitError(ApiError):
    """
    Exception raised when an external API rate limit is exceeded.
    """
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    error_type = "api_rate_limit_error"


class ApiTimeoutError(ApiError):
    """
    Exception raised when an API request times out.
    """
    status_code = status.HTTP_504_GATEWAY_TIMEOUT
    error_type = "api_timeout_error"


class ApiServiceUnavailableError(ApiError):
    """
    Exception raised when an external API service is unavailable.
    """
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    error_type = "api_service_unavailable_error" 