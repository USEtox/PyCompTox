"""
Chemical Synonym API client for EPA CompTox Dashboard.

This module provides access to chemical synonyms including:
- Alternative names and identifiers
- Beilstein numbers
- Alternate CAS Registry Numbers
- Valid and good quality synonyms
- Other synonym categories

Author: PyCompTox Contributors
License: MIT
"""

import time
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urljoin

from .config import load_api_key


class ChemSynonym:
    """
    Client for accessing chemical synonym data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving chemical synonyms and alternative
    identifiers including:
    - Beilstein registry numbers
    - Alternate CAS Registry Numbers
    - Valid and good quality synonyms
    - Other synonym categories
    - Flat list or structured views
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import ChemSynonym
        >>> synonym_client = ChemSynonym()
        >>> 
        >>> # Get synonyms for Bisphenol A
        >>> synonyms = synonym_client.get_synonyms_by_dtxsid("DTXSID7020182")
        >>> print(f"Valid names: {synonyms['valid']}")
        >>> 
        >>> # Get flat list of synonyms
        >>> flat_synonyms = synonym_client.get_synonyms_by_dtxsid(
        ...     "DTXSID7020182", 
        ...     projection="ccd-synonyms"
        ... )
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0
    ):
        """
        Initialize the ChemSynonym client.
        
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
        json_data: Optional[Any] = None,
        params: Optional[Dict[str, str]] = None
    ) -> Any:
        """
        Make an HTTP request to the CompTox API.
        
        Args:
            method: HTTP method (GET or POST)
            endpoint: API endpoint path
            json_data: JSON data for POST requests
            params: Query parameters
        
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
        
        if method == "POST":
            headers["content-type"] = "application/json"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=json_data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            if response.status_code == 403:
                raise PermissionError(
                    "API key is invalid or expired. Please check your API key."
                )
            
            response.raise_for_status()
            
            data = response.json()
            if not data:
                raise ValueError("No data returned from API")
            
            return data
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ValueError(f"Resource not found: {endpoint}")
            else:
                raise RuntimeError(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")

    def get_synonyms_by_dtxsid(
        self,
        dtxsid: str,
        projection: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get synonyms for a chemical by DTXSID with optional projection.
        
        Fetches synonyms based on the specified projection. Available projections:
        - `ccd-synonyms`: Returns a flat list of synonym objects with quality ratings
        - `chemical-synonym-all` (default): Returns structured view with categorized synonyms
        
        GET /chemical/synonym/search/by-dtxsid/{dtxsid}
        
        Args:
            dtxsid (str): DSSTox Substance Identifier (e.g., "DTXSID7020182")
            projection (str, optional): Projection type ("ccd-synonyms" or None for default)
        
        Returns:
            Dict[str, Any]: Synonym data. Structure depends on projection:
            
            Default projection returns:
                - `beilstein` (List[str]): Beilstein registry numbers
                - `alternateCasrn` (List[str]): Alternate CAS Registry Numbers
                - `dtxsid` (str): DSSTox Substance Identifier
                - `pcCode` (str): PC code
                - `deletedCasrn` (List[str]): Deleted CAS Registry Numbers
                - `other` (List[str]): Other synonyms
                - `valid` (List[str]): Valid synonyms
                - `good` (List[str]): Good quality synonyms
            
            ccd-synonyms projection returns a list of:
                - `synonym` (str): Synonym text
                - `quality` (str): Quality rating
        
        Raises:
            ValueError: If DTXSID is not found or request fails
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> synonym_client = ChemSynonym()
            >>> 
            >>> # Get structured synonyms
            >>> data = synonym_client.get_synonyms_by_dtxsid("DTXSID7020182")
            >>> print(f"Valid names: {data.get('valid', [])}")
            >>> print(f"Alternate CAS: {data.get('alternateCasrn', [])}")
            >>> 
            >>> # Get flat list with quality ratings
            >>> flat_data = synonym_client.get_synonyms_by_dtxsid(
            ...     "DTXSID7020182",
            ...     projection="ccd-synonyms"
            ... )
            >>> for item in flat_data[:5]:
            ...     print(f"{item.get('synonym')}: {item.get('quality')}")
        """
        params = {}
        if projection:
            params["projection"] = projection
        
        endpoint = f"chemical/synonym/search/by-dtxsid/{dtxsid}"
        return self._make_request("GET", endpoint, params=params)

    def get_synonyms_by_dtxsid_batch(
        self,
        dtxsid_list: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Get synonyms for multiple chemicals in a single batch request.
        
        Batch retrieval of synonym data for up to 1000 chemicals. More efficient
        than making individual requests when querying multiple chemicals.
        
        POST /chemical/synonym/search/by-dtxsid/
        
        Args:
            dtxsid_list (List[str]): List of DSSTox Substance Identifiers
                (maximum 1000 DTXSIDs)
        
        Returns:
            List[Dict[str, Any]]: List of synonym data dictionaries, each containing:
                - `beilstein` (List[str]): Beilstein registry numbers
                - `alternateCasrn` (List[str]): Alternate CAS Registry Numbers
                - `dtxsid` (str): DSSTox Substance Identifier
                - `pcCode` (str): PC code
                - `deletedCasrn` (List[str]): Deleted CAS Registry Numbers
                - `other` (List[str]): Other synonyms
                - `valid` (List[str]): Valid synonyms
                - `good` (List[str]): Good quality synonyms
        
        Raises:
            ValueError: If more than 1000 DTXSIDs provided or request fails
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> synonym_client = ChemSynonym()
            >>> dtxsids = ["DTXSID7020182", "DTXSID2021315", "DTXSID5020001"]
            >>> results = synonym_client.get_synonyms_by_dtxsid_batch(dtxsids)
            >>> 
            >>> for data in results:
            ...     dtxsid = data.get("dtxsid", "")
            ...     valid_names = data.get("valid", [])
            ...     print(f"{dtxsid}: {len(valid_names)} valid synonyms")
            >>> 
            >>> # Find chemicals with alternate CAS numbers
            >>> for data in results:
            ...     alt_cas = data.get("alternateCasrn", [])
            ...     if alt_cas:
            ...         print(f"{data.get('dtxsid')}: {alt_cas}")
        """
        if len(dtxsid_list) > 1000:
            raise ValueError(f"Maximum 1000 DTXSIDs allowed, got {len(dtxsid_list)}")
        
        endpoint = "chemical/synonym/search/by-dtxsid/"
        return self._make_request("POST", endpoint, json_data=dtxsid_list)
        