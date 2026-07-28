"""
Exception hierarchy for PyCompTox.

All errors raised by PyCompTox clients derive from :class:`CompToxError`, so
callers can catch every library-specific failure with a single ``except``
clause while still being able to distinguish the common cases.

Example:
    >>> from pycomptox import Chemical
    >>> from pycomptox.exceptions import NotFoundError, RateLimitError
    >>> client = Chemical()
    >>> try:
    ...     details = client.search_by_exact_value("not-a-real-chemical")
    ... except NotFoundError:
    ...     print("No such chemical")
    ... except RateLimitError as exc:
    ...     print(f"Slow down; retry after {exc.retry_after}s")
"""

from typing import Any, Optional

__all__ = [
    "CompToxError",
    "ConfigurationError",
    "APIError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "TimeoutError",
]


class CompToxError(Exception):
    """Base class for every error raised by PyCompTox."""


class ConfigurationError(CompToxError):
    """Raised when the client is misconfigured, e.g. no API key is available."""


class APIError(CompToxError):
    """
    Raised when the CompTox API returns an unsuccessful HTTP response.

    Attributes:
        status_code (int, optional): HTTP status code returned by the API.
        url (str, optional): The URL that was requested.
        response_text (str, optional): Raw response body, truncated.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        url: Optional[str] = None,
        response_text: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.url = url
        self.response_text = response_text


class AuthenticationError(APIError):
    """Raised on HTTP 401/403 - the API key is missing, invalid, or lacks access."""


class NotFoundError(APIError):
    """Raised on HTTP 404 - the requested resource or identifier does not exist."""


class RateLimitError(APIError):
    """
    Raised on HTTP 429 - the API rate limit has been exceeded.

    Attributes:
        retry_after (float, optional): Seconds to wait before retrying, taken
            from the ``Retry-After`` response header when present.
    """

    def __init__(self, *args: Any, retry_after: Optional[float] = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.retry_after = retry_after


class ServerError(APIError):
    """Raised on HTTP 5xx - the CompTox API failed to handle the request."""


class TimeoutError(CompToxError):  # noqa: A001 - deliberately shadows the builtin name
    """Raised when a request exceeds the configured timeout."""
