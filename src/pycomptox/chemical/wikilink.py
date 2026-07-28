"""
Chemical Wikipedia Links API client for EPA CompTox Dashboard.

This module provides access to Wikipedia GHS Safety data links for chemicals.
Returns Wikipedia URLs if GHS (Globally Harmonized System) safety data is available.

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient


class WikiLink(CachedAPIClient):
    """
    Client for accessing Wikipedia GHS Safety data links from EPA CompTox Dashboard.
    
    This class provides methods for checking if Wikipedia has GHS Safety data
    for chemicals and retrieving the corresponding Wikipedia URLs.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float, **kwargs): Delay in seconds between API calls for
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
    
    def check_existence_by_dtxsid(self, dtxsid: str, use_cache: Optional[bool] = None) -> Dict[str, Any]:
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
            NotFoundError: If the chemical is not found.
            ValueError: If the DTXSID is not a valid non-empty string.
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
            
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
        result = self._make_cached_request(endpoint, use_cache=use_cache)
        # API may return a list, handle both cases
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        return result

    def check_existence_by_dtxsid_batch(self, dtxsids: List[str], use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
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
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
            
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
        return self._make_cached_request(endpoint, method='POST', json=dtxsids, use_cache=use_cache)