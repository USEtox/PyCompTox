"""
List Presence API client for EPA CompTox Dashboard.

This module provides access to list presence data including:
- Chemical presence on regulatory and screening lists
- List presence tags and categories
- Batch operations for multiple chemicals

Author: PyCompTox Contributors
License: MIT
"""

import time
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urljoin

from ..base import CachedAPIClient


class ListPresence(CachedAPIClient):
    """
    Client for accessing list presence data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving information about chemical presence
    on various regulatory, screening, and informational lists. This includes EPA lists,
    state lists, international lists, and other chemical inventories.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float, **kwargs): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import ListPresence
        >>> list_pres = ListPresence()
        >>> 
        >>> # Get list presence data for a chemical
        >>> data = list_pres.list_presence_data_by_dtxsid("DTXSID0020232")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0
    , **kwargs):
        """
        Initialize the ListPresence client.
        
        Args:
            api_key: CompTox API key (optional, will be loaded from config if not provided)
            base_url: Base URL for the CompTox API
            time_delay_between_calls: Delay between API calls in seconds
        
        Raises:
            ValueError: If no API key is provided or found in configuration
        """
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            time_delay_between_calls=time_delay_between_calls,
            **kwargs
        )
    
    def list_presence_tags(self, use_cache: Optional[bool] = None) -> List[Dict[str, str]]:
        """
        Get all available list presence tags.
        
        Retrieves a complete list of available list presence tags, which categorize
        the different types of chemical lists tracked in the CompTox Dashboard.
        These tags help identify regulatory lists, screening lists, and other
        chemical inventories.
        
        Returns:
            List of dictionaries containing list presence tags with their names,
            descriptions, and category information.
        
        Example:
            >>> list_pres = ListPresence()
            >>> tags = list_pres.list_presence_tags()
            >>> for tag in tags:
            ...     print(f"{tag.get('tag', 'N/A')}: {tag.get('description', '')}")
        """
        endpoint = "exposure/list-presence/tags"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def list_presence_data_by_dtxsid(self, dtxsid: str, use_cache: Optional[bool] = None) -> List[Dict[str, str]]:
        """
        Get list presence data for a chemical.
        
        Retrieves information about which regulatory, screening, and informational
        lists contain a specific chemical identified by its DSSTox Substance
        Identifier (DTXSID). This includes EPA lists, state lists, international
        lists, and other chemical inventories.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0020232')
        
        Returns:
            List of dictionaries containing list presence information. Each entry
            includes the list name, source, category, and presence status.
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> list_pres = ListPresence()
            >>> data = list_pres.list_presence_data_by_dtxsid("DTXSID0020232")
            >>> for item in data:
            ...     print(f"{item.get('listName', 'N/A')}: {item.get('presenceStatus', 'N/A')}")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/list-presence/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)
        
    def list_presence_data_by_dtxsid_batch(self, dtxsids: List[str], use_cache: Optional[bool] = None) -> List[Dict[str, str]]:
        """
        Get list presence data for multiple chemicals in a single request.
        
        Retrieves list presence information for multiple chemicals at once using a
        batch API call. This is more efficient than making individual requests for
        each chemical when working with multiple DTXSIDs.
        
        Args:
            dtxsids: List of DSSTox Substance Identifiers
        
        Returns:
            List of dictionaries containing list presence data for all requested
            chemicals. Results include the DTXSID and associated list presence
            information for each chemical.
        
        Raises:
            ValueError: If dtxsids is not a valid non-empty list
        
        Example:
            >>> list_pres = ListPresence()
            >>> dtxsids = ["DTXSID0020232", "DTXSID0020245"]
            >>> batch_data = list_pres.list_presence_data_by_dtxsid_batch(dtxsids)
            >>> for result in batch_data:
            ...     print(f"{result.get('dtxsid')}: {result.get('listName')}")
        """
        if not dtxsids or not isinstance(dtxsids, list) or len(dtxsids) == 0:
            raise ValueError("dtxsids must be a non-empty list of strings")
        
        if not all(isinstance(dtxsid, str) for dtxsid in dtxsids):
            raise ValueError("All elements in dtxsids must be strings")
        
        endpoint = "exposure/list-presence/search/by-dtxsid/"
        return self._make_request("POST", endpoint, json_data=dtxsids)