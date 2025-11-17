"""
HTTK Data API client for EPA CompTox Dashboard.

This module provides access to High-Throughput Toxicokinetics (HTTK) data including:
- Toxicokinetic parameters (clearance, volume of distribution, half-life, etc.)
- In vitro and in vivo measured values
- Predicted values from in silico models
- Computed values from mathematical models
- Batch operations for multiple chemicals

Author: PyCompTox Contributors
License: MIT
"""

import time
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urljoin

from .config import load_api_key


class HTTKData:
    """
    Client for accessing High-Throughput Toxicokinetics (HTTK) data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving human toxicokinetic parameters including:
    - Intrinsic hepatic clearance
    - Fraction unbound in plasma
    - Volume of distribution
    - PK half-life
    - Steady-state plasma concentration
    
    Values are measured (in vitro or in vivo), predicted from chemical properties using
    in silico tools, or computed with mathematical models simulating toxicokinetics.
    
    The in vitro measured values reflect data curated for the open source R package "httk"
    (https://CRAN.R-project.org/package=httk). The computed values are generated with httk
    using reported in vitro values. In vivo measured values are estimated from
    toxicokinetic concentration vs. time data in CvTdb (https://doi.org/10.1038/s41597-020-0455-1)
    using R package "invivoPKfit" (https://github.com/USEPA/CompTox-ExpoCast-invivoPKfit).
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import HTTKData
        >>> httk = HTTKData()
        >>> 
        >>> # Get HTTK data for a chemical
        >>> data = httk.httk_data_by_dtxsid("DTXSID0020232")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0
    ):
        """
        Initialize the HTTKData client.
        
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

    def httk_data_by_dtxsid(self, dtxsid: str) -> List[Dict[str, Any]]:
        """
        Get high-throughput toxicokinetics (HTTK) data for a chemical.
        
        Retrieves toxicokinetic parameters for a specific chemical identified by its
        DSSTox Substance Identifier (DTXSID). Returns measured, predicted, and computed
        toxicokinetic values including clearance, volume of distribution, half-life,
        and steady-state plasma concentration.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0020232')
        
        Returns:
            List of dictionaries containing HTTK data. Each entry includes:
            - Intrinsic hepatic clearance
            - Fraction unbound in plasma
            - Volume of distribution
            - PK half-life
            - Steady-state plasma concentration
            - Data source (in vitro, in vivo, predicted, computed)
            - Species information
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> httk = HTTKData()
            >>> data = httk.httk_data_by_dtxsid("DTXSID0020232")
            >>> for param in data:
            ...     print(f"{param.get('parameter')}: {param.get('value')} {param.get('units')}")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/httk/search/by-dtxsid/{dtxsid}"
        return self._make_request("GET", endpoint)

    def httk_data_by_dtxsid_batch(self, dtxsid_list: List[str]) -> List[Dict[str, Any]]:
        """
        Get HTTK data for multiple chemicals in a single request.
        
        Retrieves toxicokinetic parameters for multiple chemicals at once using a batch
        API call. This is more efficient than making individual requests for each chemical
        when working with multiple DTXSIDs.
        
        Args:
            dtxsid_list: List of DSSTox Substance Identifiers
        
        Returns:
            List of dictionaries containing HTTK data for all requested chemicals.
            Each entry includes the DTXSID and associated toxicokinetic parameters.
        
        Raises:
            ValueError: If dtxsid_list is not a valid non-empty list
        
        Example:
            >>> httk = HTTKData()
            >>> dtxsids = ["DTXSID0020232", "DTXSID7020182"]
            >>> batch_data = httk.httk_data_by_dtxsid_batch(dtxsids)
            >>> for result in batch_data:
            ...     print(f"{result.get('dtxsid')}: {result.get('parameter')} = {result.get('value')}")
        """
        if not dtxsid_list or not isinstance(dtxsid_list, list) or len(dtxsid_list) == 0:
            raise ValueError("dtxsid_list must be a non-empty list of strings")
        
        if not all(isinstance(dtxsid, str) for dtxsid in dtxsid_list):
            raise ValueError("All elements in dtxsid_list must be strings")
        
        endpoint = "exposure/httk/search/by-dtxsid/"
        return self._make_request("POST", endpoint, json_data=dtxsid_list)
