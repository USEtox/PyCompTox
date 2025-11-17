"""
Product Data API client for EPA CompTox Dashboard.

This module provides access to product data including:
- Product composition and ingredient information
- Product Use Category (PUC) classifications
- Chemical presence in consumer products
- Batch operations for multiple chemicals

Author: PyCompTox Contributors
License: MIT
"""

import time
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urljoin

from .config import load_api_key


class ProductData:
    """
    Client for accessing product data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving information about consumer products
    that contain chemicals, including product use categories (PUC) and composition data.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import ProductData
        >>> prod_data = ProductData()
        >>> 
        >>> # Get product data for a chemical
        >>> products = prod_data.products_data_by_dtxsid("DTXSID0020232")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0
    ):
        """
        Initialize the ProductData client.
        
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

    def products_data_by_dtxsid(self, dtxsid: str) -> List[Dict[str, Any]]:
        """
        Get product data for a chemical.
        
        Retrieves information about consumer products that contain a specific chemical
        identified by its DSSTox Substance Identifier (DTXSID). This includes product
        names, manufacturers, product use categories (PUC), and composition information.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0020232')
        
        Returns:
            List of dictionaries containing product data. Each entry includes product
            information such as name, manufacturer, PUC classification, and chemical
            composition details.
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> prod_data = ProductData()
            >>> products = prod_data.products_data_by_dtxsid("DTXSID0020232")
            >>> for product in products:
            ...     print(f"{product.get('productName', 'N/A')}: {product.get('pucCode', 'N/A')}")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/product-data/search/by-dtxsid/{dtxsid}"
        return self._make_request("GET", endpoint)

    def list_all_puc_product(self) -> List[Dict[str, Any]]:
        """
        Get all Product Use Category (PUC) classifications.
        
        Retrieves a complete list of Product Use Category (PUC) codes and their
        definitions. PUCs provide a hierarchical classification system for categorizing
        consumer product types based on their use and function.
        
        Returns:
            List of dictionaries containing PUC information including codes,
            descriptions, and hierarchical relationships.
        
        Example:
            >>> prod_data = ProductData()
            >>> pucs = prod_data.list_all_puc_product()
            >>> for puc in pucs:
            ...     print(f"{puc.get('pucCode', 'N/A')}: {puc.get('pucDescription', '')}")
        """
        endpoint = "exposure/product-data/puc"
        return self._make_request("GET", endpoint)

    def product_data_by_dtxsid_batch(self, dtxsid_list: List[str]) -> List[Dict[str, Any]]:
        """
        Get product data for multiple chemicals in a single request.
        
        Retrieves product information for multiple chemicals at once using a batch
        API call. This is more efficient than making individual requests for each
        chemical when working with multiple DTXSIDs.
        
        Args:
            dtxsid_list: List of DSSTox Substance Identifiers
        
        Returns:
            List of dictionaries containing product data for all requested chemicals.
            Results include the DTXSID and associated product information for each
            chemical.
        
        Raises:
            ValueError: If dtxsid_list is not a valid non-empty list
        
        Example:
            >>> prod_data = ProductData()
            >>> dtxsids = ["DTXSID0020232", "DTXSID7020182"]
            >>> batch_results = prod_data.product_data_by_dtxsid_batch(dtxsids)
            >>> for result in batch_results:
            ...     print(f"{result.get('dtxsid')}: {result.get('productName')}")
        """
        if not dtxsid_list or not isinstance(dtxsid_list, list) or len(dtxsid_list) == 0:
            raise ValueError("dtxsid_list must be a non-empty list of strings")
        
        if not all(isinstance(dtxsid, str) for dtxsid in dtxsid_list):
            raise ValueError("All elements in dtxsid_list must be strings")
        
        endpoint = "exposure/product-data/search/by-dtxsid/"
        return self._make_request("POST", endpoint, json_data=dtxsid_list)
