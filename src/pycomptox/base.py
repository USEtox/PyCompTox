"""
Base API client with caching support.

This module provides a base class that all API clients can inherit from
to get automatic caching functionality.

Author: PyCompTox Contributors
License: MIT
"""

import requests
import time
from typing import Any, Dict, Optional
from abc import ABC
from .config import load_api_key
from .cache import get_default_cache, CacheManager


class CachedAPIClient(ABC):
    """
    Base class for API clients with caching support.
    
    This class provides common functionality for all API clients including:
    - API key management
    - Rate limiting
    - Request caching
    - Session management
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        cache_manager (CacheManager, optional): Cache manager instance to use.
            If None, uses the default global cache.
        use_cache (bool): Whether to use caching by default. Default is True.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api",
        time_delay_between_calls: float = 0.0,
        cache_manager: Optional[CacheManager] = None,
        use_cache: bool = True
    ):
        """Initialize the cached API client."""
        # Load API key if not provided
        if api_key is None:
            api_key = load_api_key()
            if api_key is None:
                raise ValueError(
                    "No API key provided. Please either:\n"
                    "1. Pass api_key parameter\n"
                    "2. Set COMPTOX_API_KEY environment variable\n"
                    "3. Save key using: from pycomptox import save_api_key; save_api_key('your_key')"
                )
        
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.time_delay_between_calls = time_delay_between_calls
        self._last_call_time = 0.0
        self.use_cache = use_cache
        
        # Set up cache
        if cache_manager is None:
            self.cache_manager = get_default_cache()
        else:
            self.cache_manager = cache_manager
        
        # Set up session
        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'application/json',
            'x-api-key': self.api_key
        })
    
    def _enforce_rate_limit(self) -> None:
        """Enforce rate limiting by pausing if necessary."""
        if self.time_delay_between_calls > 0:
            elapsed = time.time() - self._last_call_time
            if elapsed < self.time_delay_between_calls:
                time.sleep(self.time_delay_between_calls - elapsed)
        self._last_call_time = time.time()
    
    def _make_cached_request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
        method: str = 'GET',
        use_cache: Optional[bool] = None
    ) -> Any:
        """
        Make an API request with caching support.
        
        Args:
            endpoint: API endpoint path (relative to base_url)
            params: Request parameters for GET requests
            json: JSON body for POST requests
            method: HTTP method ('GET' or 'POST')
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            API response data
        
        Raises:
            requests.RequestException: If the API request fails
        """
        if params is None:
            params = {}
        
        # Determine if we should use cache for this request
        should_cache = use_cache if use_cache is not None else self.use_cache
        
        # Create cache key from params and json body
        cache_params = params.copy()
        if json is not None:
            cache_params['__json__'] = json
        
        # Try to get from cache first
        if should_cache and self.cache_manager.enabled:
            cached_response = self.cache_manager.get(endpoint, cache_params)
            if cached_response is not None:
                return cached_response
        
        # Make API request
        self._enforce_rate_limit()
        
        url = f"{self.base_url}/{endpoint}"
        if method.upper() == 'POST':
            response = self.session.post(url, json=json, params=params)
        else:
            response = self.session.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Cache the response
        if should_cache and self.cache_manager.enabled:
            self.cache_manager.set(endpoint, cache_params, data)
        
        return data
