"""
Base API client shared by every PyCompTox client.

This module provides :class:`CachedAPIClient`, the single place where HTTP
concerns live: API key resolution, URL construction, timeouts, retries,
rate limiting, error translation, and optional response caching.

Author: PyCompTox Contributors
License: MIT
"""

import time
from abc import ABC
from typing import Any, Dict, Optional, Tuple, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .cache import CacheManager, get_default_cache
from .config import load_api_key
from .exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
)

#: Default base URL for the EPA CompTox Dashboard API.
DEFAULT_BASE_URL = "https://comptox.epa.gov/ctx-api"

#: Default ``(connect, read)`` timeout in seconds applied to every request.
DEFAULT_TIMEOUT: Tuple[float, float] = (10.0, 60.0)

#: Number of automatic retries for transient failures (429 and 5xx).
DEFAULT_MAX_RETRIES = 3

#: HTTP statuses that are retried with exponential backoff.
RETRY_STATUS_CODES = (429, 500, 502, 503, 504)


class CachedAPIClient(ABC):
    """
    Base class for all CompTox API clients.

    Provides functionality common to every client:

    - API key resolution (explicit argument, environment, saved config file)
    - Request timeouts, so a call can never hang indefinitely
    - Automatic retries with exponential backoff on 429 and 5xx responses
    - Optional client-side rate limiting
    - Translation of HTTP errors into the :mod:`pycomptox.exceptions` hierarchy
    - Optional on-disk response caching (disabled by default)

    Args:
        api_key (str, optional): CompTox API key. If not provided, it is loaded
            from the ``COMPTOX_API_KEY`` environment variable or the saved
            configuration file.
        base_url (str): Base URL for the CompTox API.
        time_delay_between_calls (float, optional): Minimum delay in seconds
            between consecutive API calls. If None, the client's
            ``default_time_delay`` applies (0.0 for most clients; a few
            rate-sensitive ones default higher).
        cache_manager (CacheManager, optional): Cache manager to use. Only
            consulted when caching is enabled. If None, the default global
            cache is used.
        use_cache (bool): Whether to cache responses by default. Default is
            False - caching is opt-in, either per client or per call.
        timeout (float or tuple, optional): Request timeout in seconds, either
            a single value or a ``(connect, read)`` pair. Defaults to
            ``(10.0, 60.0)``.
        max_retries (int): Number of automatic retries for transient failures.
            Default is 3.

    Raises:
        ConfigurationError: If no API key is provided and none can be loaded.
    """

    #: Per-client default for ``time_delay_between_calls``, used when the caller
    #: does not pass one. Subclasses whose endpoints are heavy or rate-sensitive
    #: override this instead of redefining ``__init__``.
    default_time_delay: float = 0.0

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        time_delay_between_calls: Optional[float] = None,
        cache_manager: Optional[CacheManager] = None,
        use_cache: bool = False,
        timeout: Optional[Union[float, Tuple[float, float]]] = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ):
        """Initialize the API client."""
        if api_key is None:
            api_key = load_api_key()
            if api_key is None:
                raise ConfigurationError(
                    "No API key provided. Please either:\n"
                    "1. Pass the api_key parameter\n"
                    "2. Set the COMPTOX_API_KEY environment variable\n"
                    "3. Save a key using: "
                    "from pycomptox import save_api_key; save_api_key('your_key')\n"
                    "4. Run: pycomptox-setup set YOUR_API_KEY"
                )

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.time_delay_between_calls = (
            self.default_time_delay
            if time_delay_between_calls is None
            else time_delay_between_calls
        )
        self._last_call_time = 0.0
        self.use_cache = use_cache
        self.timeout = DEFAULT_TIMEOUT if timeout is None else timeout

        self.cache_manager = get_default_cache() if cache_manager is None else cache_manager

        self.session = requests.Session()
        self.session.headers.update(
            {
                "accept": "application/json",
                "x-api-key": self.api_key,
            }
        )

        # Retry transient failures (429 and 5xx) with exponential backoff.
        #
        # POST is included in allowed_methods, which is not urllib3's default
        # because POST is generally not idempotent. It is safe here: every POST
        # this library makes is a read-only batch query (a list of identifiers
        # in, matching records out), so replaying one has no side effects.
        #
        # respect_retry_after_header honours a Retry-After header instead of
        # guessing the delay. raise_on_status=False lets the exhausted response
        # come back to us so _raise_for_status can turn it into a typed
        # exception rather than urllib3's MaxRetryError.
        retry = Retry(
            total=max_retries,
            status_forcelist=list(RETRY_STATUS_CODES),
            allowed_methods=frozenset(["GET", "POST"]),
            backoff_factor=0.5,
            respect_retry_after_header=True,
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _enforce_rate_limit(self) -> None:
        """
        Pause if needed so calls are at least ``time_delay_between_calls`` apart.

        Uses ``time.monotonic()`` rather than ``time.time()``: the wall clock can
        step backwards (NTP correction, VM or host suspend/resume), which would
        make the measured interval negative and cause an over-long sleep.
        """
        if self.time_delay_between_calls > 0:
            elapsed = time.monotonic() - self._last_call_time
            if elapsed < self.time_delay_between_calls:
                time.sleep(self.time_delay_between_calls - elapsed)
        self._last_call_time = time.monotonic()

    @staticmethod
    def _normalize_endpoint(endpoint: str) -> str:
        """
        Normalize an endpoint path to a canonical form.

        Strips any leading slash, so ``"/chemical/search/equal/x"`` and
        ``"chemical/search/equal/x"`` produce the same URL and the same cache
        key. Without this, the two forms yield a double-slashed URL and
        duplicate cache entries.

        Trailing slashes are deliberately preserved: the CompTox API treats
        them as significant. The batch POST endpoints answer on
        ``.../search/by-dtxsid/`` and return 404 without the trailing slash.
        """
        return endpoint.lstrip("/")

    def _raise_for_status(self, response: requests.Response) -> None:
        """Translate an unsuccessful HTTP response into a PyCompTox exception."""
        if response.ok:
            return

        status = response.status_code
        url = response.url
        body = (response.text or "")[:500]
        message = f"CompTox API request failed with HTTP {status} for {url}"

        if status in (401, 403):
            raise AuthenticationError(
                f"{message}. Check that your API key is valid and has access to this dataset.",
                status_code=status,
                url=url,
                response_text=body,
            )
        if status == 404:
            raise NotFoundError(
                f"{message}. The requested resource or identifier was not found.",
                status_code=status,
                url=url,
                response_text=body,
            )
        if status == 429:
            retry_after = response.headers.get("Retry-After")
            try:
                parsed_retry_after = float(retry_after) if retry_after is not None else None
            except ValueError:
                parsed_retry_after = None
            raise RateLimitError(
                f"{message}. Rate limit exceeded; consider increasing "
                f"time_delay_between_calls.",
                status_code=status,
                url=url,
                response_text=body,
                retry_after=parsed_retry_after,
            )
        if status >= 500:
            raise ServerError(message, status_code=status, url=url, response_text=body)

        raise APIError(message, status_code=status, url=url, response_text=body)

    def _make_cached_request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
        method: str = "GET",
        use_cache: Optional[bool] = None,
    ) -> Any:
        """
        Make an API request, optionally served from and stored in the cache.

        Args:
            endpoint: API endpoint path, relative to ``base_url``. Leading and
                trailing slashes are ignored.
            params: Query string parameters.
            json: JSON body, for POST requests.
            method: HTTP method, ``"GET"`` or ``"POST"``.
            use_cache: Whether to use the cache for this call. If None, the
                client's ``use_cache`` setting applies.

        Returns:
            The decoded JSON response.

        Raises:
            AuthenticationError: On HTTP 401 or 403.
            NotFoundError: On HTTP 404.
            RateLimitError: On HTTP 429.
            ServerError: On HTTP 5xx.
            APIError: On any other unsuccessful response, or an undecodable body.
            TimeoutError: If the request exceeds the configured timeout.
        """
        endpoint = self._normalize_endpoint(endpoint)
        method = method.upper()

        if params is None:
            params = {}

        should_cache = use_cache if use_cache is not None else self.use_cache

        # The method is part of the key: the same path can serve a single-item
        # GET and a batch POST, whose responses must not collide.
        cache_params: Dict[str, Any] = dict(params)
        cache_params["__method__"] = method
        if json is not None:
            cache_params["__json__"] = json

        if should_cache and self.cache_manager.enabled:
            cached_response = self.cache_manager.get(endpoint, cache_params)
            if cached_response is not None:
                return cached_response

        self._enforce_rate_limit()

        url = f"{self.base_url}/{endpoint}"
        try:
            if method == "POST":
                response = self.session.post(
                    url, json=json, params=params, timeout=self.timeout
                )
            else:
                response = self.session.get(url, params=params, timeout=self.timeout)
        except requests.exceptions.Timeout as exc:
            raise TimeoutError(
                f"Request to {url} timed out after {self.timeout}s"
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise APIError(f"Request to {url} failed: {exc}", url=url) from exc

        self._raise_for_status(response)

        try:
            data = response.json()
        except ValueError as exc:
            raise APIError(
                f"CompTox API returned a non-JSON response for {url}",
                status_code=response.status_code,
                url=url,
                response_text=(response.text or "")[:500],
            ) from exc

        if should_cache and self.cache_manager.enabled:
            self.cache_manager.set(endpoint, cache_params, data)

        return data
