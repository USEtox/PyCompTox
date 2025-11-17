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

from .config import load_api_key


class ListPresence:
    """
    Client for accessing list presence data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving information about chemical presence
    on various regulatory, screening, and informational lists. This includes EPA lists,
    state lists, international lists, and other chemical inventories.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
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
    ):
        """
        Initialize the ListPresence client.
        
        Args:
            api_key: CompTox API key (optional, will be loaded from config if not provided)
            base_url: Base URL for the CompTox API
            time_delay_between_calls: Delay between API calls in seconds
        
        Raises:
            ValueError: If no API key is provided or found in configuration
        """
        self.base_url = base_url
        self.time_delay = time_delay_between_calls
        self.last_call_time = 0
        
        # Get API key from parameter, config, or environment
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = load_api_key()
            if not self.api_key:
                raise ValueError(
                    "No API key provided. Either pass api_key parameter or "
                    "set it using save_api_key() or COMPTOX_API_KEY environment variable."
                )
    
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
            method: HTTP method (GET or POST)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON data for POST requests
        
        Returns:
            API response data
        
        Raises:
            PermissionError: If API key is invalid (403)
            ValueError: If request fails or returns no data
            RuntimeError: For other API errors
        """
        # Rate limiting
        if self.time_delay > 0:
            current_time = time.time()
            time_since_last_call = current_time - self.last_call_time
            if time_since_last_call < self.time_delay:
                time.sleep(self.time_delay - time_since_last_call)
            self.last_call_time = time.time()
        
        url = urljoin(self.base_url, endpoint)
        headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }
        
        if json_data is not None:
            headers["content-type"] = "application/json"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=json_data, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Check for specific error codes
            if response.status_code == 403:
                raise PermissionError(
                    "Invalid API key. Please check your API key configuration."
                )
            elif response.status_code == 404:
                raise ValueError(
                    f"Endpoint not found: {endpoint}. The API endpoint may not exist or the resource was not found."
                )
            elif response.status_code != 200:
                raise RuntimeError(
                    f"API request failed with status {response.status_code}: {response.text}"
                )
            
            # Try to parse JSON response
            try:
                data = response.json()
            except ValueError:
                raise ValueError("API response is not valid JSON")
            
            return data
            
        except requests.exceptions.Timeout:
            raise RuntimeError(f"Request timed out for endpoint: {endpoint}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request failed: {str(e)}")

    def list_presence_tags(self) -> List[Dict[str, str]]:
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
        return self._make_request("GET", endpoint)

    def list_presence_data_by_dtxsid(self, dtxsid: str) -> List[Dict[str, str]]:
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
        return self._make_request("GET", endpoint)
        
    def list_presence_data_by_dtxsid_batch(self, dtxsids: List[str]) -> List[Dict[str, str]]:
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