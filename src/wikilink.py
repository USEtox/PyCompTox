"""
Chemical Wikipedia Links API client for EPA CompTox Dashboard.

This module provides access to Wikipedia GHS Safety data links for chemicals.
Returns Wikipedia URLs if GHS (Globally Harmonized System) safety data is available.

Author: PyCompTox Contributors
License: MIT
"""

import os
import time
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urljoin

from .config import load_api_key


class WikiLink:
    """
    Client for accessing Wikipedia GHS Safety data links from EPA CompTox Dashboard.
    
    This class provides methods for checking if Wikipedia has GHS Safety data
    for chemicals and retrieving the corresponding Wikipedia URLs.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import WikiLink
        >>> wiki = WikiLink()
        >>> 
        >>> # Check if Wikipedia has GHS data for Bisphenol A
        >>> result = wiki.check_existence_by_dtxsid("DTXSID7020182")
        >>> if result['safetyUrl']:
        ...     print(f"Wikipedia GHS data: {result['safetyUrl']}")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api",
        time_delay_between_calls: float = 0.0
    ):
        """Initialize the WikiLink client."""
        # Load API key from parameter, config file, or environment
        self.api_key = api_key or load_api_key()
        if not self.api_key:
            raise ValueError(
                "API key is required. Either pass it as a parameter, "
                "set COMPTOX_API_KEY environment variable, or save it using "
                "save_api_key() function."
            )
        
        # Ensure base_url ends with / for proper urljoin behavior with relative paths
        self.base_url = base_url.rstrip('/') + '/'
        self.time_delay_between_calls = time_delay_between_calls
        self._last_call_time = 0.0
        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'application/json',
            'x-api-key': self.api_key
        })
    
    def _enforce_rate_limit(self):
        """Enforce rate limiting between API calls."""
        if self.time_delay_between_calls > 0:
            elapsed = time.time() - self._last_call_time
            if elapsed < self.time_delay_between_calls:
                time.sleep(self.time_delay_between_calls - elapsed)
        self._last_call_time = time.time()
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Any] = None
    ) -> Any:
        """
        Make an HTTP request to the CompTox API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body for POST requests
            
        Returns:
            JSON response from the API
            
        Raises:
            ValueError: If resource not found (404)
            requests.exceptions.RequestException: For other API errors
        """
        self._enforce_rate_limit()
        
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data
            )
            
            if response.status_code == 404:
                raise ValueError(f"Resource not found: {endpoint}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Network error: {str(e)}")

    def check_existence_by_dtxsid(self, dtxsid: str) -> Dict[str, Any]:
        """
        Check if Wikipedia has GHS Safety data for a chemical by DTXSID.
        
        Returns the Wikipedia URL if GHS (Globally Harmonized System) safety data
        is available for the specified chemical, otherwise returns empty safetyUrl.
        
        Args:
            dtxsid (str): CompTox substance identifier (e.g., "DTXSID7020182")
            
        Returns:
            dict: Wikipedia link information with fields:
                - dtxsid: DSSTox Substance Identifier
                - safetyUrl: Wikipedia URL for GHS safety data (or empty string if not available)
                
        Raises:
            ValueError: If chemical not found or invalid DTXSID
            requests.exceptions.RequestException: For API errors
            
        Example:
            >>> wiki = WikiLink()
            >>> result = wiki.check_existence_by_dtxsid("DTXSID7020182")
            >>> print(f"DTXSID: {result['dtxsid']}")
            >>> if result['safetyUrl']:
            ...     print(f"Wikipedia GHS Safety URL: {result['safetyUrl']}")
            ... else:
            ...     print("No Wikipedia GHS data available")
            
            # Example output:
            # DTXSID: DTXSID7020182
            # Wikipedia GHS Safety URL: https://en.wikipedia.org/wiki/IISBACLAFKSPIT-UHFFFAOYSA-N#section=wiki-Classification
        """
        endpoint = f"chemical/wikipedia/by-dtxsid/{dtxsid}"
        result = self._make_request("GET", endpoint)
        # API may return a list, handle both cases
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        return result

    def check_existence_by_dtxsid_batch(self, dtxsids: List[str]) -> List[Dict[str, Any]]:
        """
        Check Wikipedia GHS Safety data availability for multiple chemicals in a single request.
        
        Batch retrieval of Wikipedia URLs for up to 1000 chemicals. More efficient than
        making individual requests when checking multiple chemicals.
        
        Args:
            dtxsids (List[str]): List of CompTox substance identifiers
                (maximum 1000 DTXSIDs)
            
        Returns:
            List[dict]: List of Wikipedia link information dictionaries, each containing:
                - dtxsid: DSSTox Substance Identifier
                - safetyUrl: Wikipedia URL for GHS safety data (or empty string if not available)
                
        Raises:
            ValueError: If more than 1000 DTXSIDs provided
            requests.exceptions.RequestException: For API errors
            
        Example:
            >>> wiki = WikiLink()
            >>> dtxsids = ["DTXSID7020182", "DTXSID2021315", "DTXSID5020001"]
            >>> results = wiki.check_existence_by_dtxsid_batch(dtxsids)
            >>> 
            >>> for result in results:
            ...     status = "✓ Has data" if result['safetyUrl'] else "✗ No data"
            ...     print(f"{result['dtxsid']}: {status}")
            ...     if result['safetyUrl']:
            ...         print(f"  URL: {result['safetyUrl']}")
            >>> 
            >>> # Count chemicals with Wikipedia GHS data
            >>> with_data = sum(1 for r in results if r['safetyUrl'])
            >>> print(f"\n{with_data}/{len(results)} chemicals have Wikipedia GHS data")
        """
        if len(dtxsids) > 1000:
            raise ValueError(f"Maximum 1000 DTXSIDs allowed, got {len(dtxsids)}")
        
        endpoint = "chemical/wikipedia/by-dtxsid/"
        return self._make_request("POST", endpoint, json_data=dtxsids)