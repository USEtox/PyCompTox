"""
Bioactivity Assay Search API client for EPA CompTox Dashboard.

This module provides search capabilities for bioactivity assays including:
- Search by starting value (prefix match)
- Search by exact value (exact match)
- Search by substring (contains match)

Author: PyCompTox Contributors
License: MIT
"""

import time
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urljoin, quote

from ..base import CachedAPIClient


class AssaySearch(CachedAPIClient):
    """
    Client for searching bioactivity assays in EPA CompTox Dashboard.
    
    This class provides methods for searching bioassays by:
    - Starting value (prefix match)
    - Exact value (exact match)
    - Substring value (contains match)
    
    All search values are automatically URL-encoded for safe API requests.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        use_cache (bool): Whether to use caching by default. Default is True.
    
    Example:
        >>> from pycomptox import AssaySearch
        >>> search_client = AssaySearch()
        >>> 
        >>> # Search for assays starting with "ATG_S"
        >>> results = search_client.search_by_starting_value("ATG_S")
        >>> 
        >>> # Search for exact assay name
        >>> exact = search_client.search_by_exact_value("ATG_STAT3_CIS")
        >>> 
        >>> # Search for assays containing substring
        >>> contains = search_client.search_by_substring_value("AT3_CIS", top=100)
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0,
        **kwargs
    ):
        """
        Initialize the AssaySearch client.
        
        Args:
            api_key: CompTox API key (optional, will be loaded from config if not provided)
            base_url: Base URL for the CompTox API
            time_delay_between_calls: Delay between API calls in seconds
            **kwargs: Additional arguments for CachedAPIClient (cache_manager, use_cache)
        
        Raises:
            ValueError: If no API key is provided or found in configuration
        """
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            time_delay_between_calls=time_delay_between_calls,
            **kwargs
        )
    

    def search_by_starting_value(self, value: str, top: int = 500, use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Search for bioactivity assays that start with the specified value.
        
        This method performs a prefix match search, returning all assays whose
        search names or values begin with the provided string.
        
        Args:
            value: Starting characters for search value (will be URL encoded)
            top: Maximum number of results to return (default: 500)
        
        Returns:
            List of assay search results. Each result contains:
                - id (int): Unique identifier
                - aeid (int): Assay endpoint ID
                - searchName (str): Name used for searching
                - searchValue (str): Value used for searching
                - searchValueDesc (str): Description of the search value
                - modifiedValue (str): Modified version of the value
        
        Raises:
            ValueError: If no data is found or value is invalid
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox import AssaySearch
            >>> search_client = AssaySearch()
            >>> 
            >>> # Find all assays starting with "ATG_S"
            >>> results = search_client.search_by_starting_value("ATG_S")
            >>> for result in results[:3]:
            ...     print(f"{result['searchValue']}: {result['searchValueDesc']}")
            >>> 
            >>> # Limit results
            >>> limited = search_client.search_by_starting_value("ATG_S", top=10)
        """
        # URL encode the search value
        encoded_value = quote(value, safe='')
        endpoint = f"bioactivity/search/start-with/{encoded_value}"
        params = {"top": top}
        
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)

    def search_by_exact_value(self, value: str, use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Search for bioactivity assays by exact value match.
        
        This method finds assays that exactly match the provided search value.
        
        Args:
            value: Exact search value to match (will be URL encoded)
        
        Returns:
            List of assay search results matching the exact value. Each result contains:
                - id (int): Unique identifier
                - aeid (int): Assay endpoint ID
                - searchName (str): Name used for searching
                - searchValue (str): Value used for searching
                - searchValueDesc (str): Description of the search value
                - modifiedValue (str): Modified version of the value
        
        Raises:
            ValueError: If no data is found or value is invalid
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox import AssaySearch
            >>> search_client = AssaySearch()
            >>> 
            >>> # Find exact assay match
            >>> result = search_client.search_by_exact_value("ATG_STAT3_CIS")
            >>> print(f"Found: {result[0]['searchValueDesc']}")
            >>> 
            >>> # Search by synonym (will be URL encoded automatically)
            >>> synonym_result = search_client.search_by_exact_value("caffeine")
        """
        # URL encode the search value
        encoded_value = quote(value, safe='')
        endpoint = f"bioactivity/search/equal/{encoded_value}"
        
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def search_by_substring_value(self, value: str, top: int = 0, use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Search for bioactivity assays containing the specified substring.
        
        This method performs a substring match search, returning all assays whose
        search names, values, or synonyms contain the provided string.
        
        Args:
            value: Substring to search for (will be URL encoded)
            top: Maximum number of results to return (default: 0 = no limit)
        
        Returns:
            List of assay search results containing the substring. Each result contains:
                - id (int): Unique identifier
                - aeid (int): Assay endpoint ID
                - searchName (str): Name used for searching
                - searchValue (str): Value used for searching
                - searchValueDesc (str): Description of the search value
                - modifiedValue (str): Modified version of the value
        
        Raises:
            ValueError: If no data is found or value is invalid
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox import AssaySearch
            >>> search_client = AssaySearch()
            >>> 
            >>> # Find all assays containing "AT3_CIS"
            >>> results = search_client.search_by_substring_value("AT3_CIS")
            >>> 
            >>> # Search by partial synonym (e.g., "razine" for atrazine)
            >>> synonym_results = search_client.search_by_substring_value("razine", top=50)
            >>> 
            >>> # Get all results (no limit)
            >>> all_results = search_client.search_by_substring_value("STAT")
        """
        # URL encode the search value
        encoded_value = quote(value, safe='')
        endpoint = f"bioactivity/search/contain/{encoded_value}"
        params = {"top": top} if top > 0 else {}
        
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)