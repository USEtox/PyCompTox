"""
MMDB API client for EPA CompTox Dashboard.

This module provides access to the Molecular Modeling Database (MMDB) including:
- Harmonized single-sample records by medium
- Environmental monitoring and measurement data

Author: PyCompTox Contributors
License: MIT
"""

import time
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urljoin

from .config import load_api_key


class MMDB:
    """
    Client for accessing Molecular Modeling Database (MMDB) from EPA CompTox Dashboard.
    
    This class provides methods for retrieving environmental monitoring and measurement
    data, including harmonized single-sample records organized by environmental medium.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import MMDB
        >>> mmdb = MMDB()
        >>> 
        >>> # Get single-sample records for surface water
        >>> data = mmdb.harmonized_single_sample_by_medium("surface water")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0
    ):
        """
        Initialize the MMDB client.
        
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
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Make an HTTP request to the CompTox API.
        
        Args:
            method: HTTP method (GET)
            endpoint: API endpoint path
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
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=30)
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

    def harmonized_single_sample_by_medium(self, medium: str, page_number: int = 1) -> Dict[str, Any]:
        """
        Get harmonized single-sample records by environmental medium.
        
        Retrieves harmonized single-sample environmental monitoring records filtered
        by the type of environmental medium (e.g., surface water, air, soil). The data
        is paginated to handle large result sets.
        
        Args:
            medium: Harmonized medium type (e.g., 'surface water', 'air', 'soil',
                'groundwater', 'sediment', 'biota')
            page_number: Page number for pagination (default: 1)
        
        Returns:
            Dictionary containing paginated single-sample records for the specified medium.
            The structure typically includes:
                - data: List of sample records
                - pagination information (page number, total pages, etc.)
        
        Raises:
            ValueError: If medium is not a valid non-empty string
        
        Example:
            >>> mmdb = MMDB()
            >>> # Get first page of surface water samples
            >>> data = mmdb.harmonized_single_sample_by_medium("surface water")
            >>> 
            >>> # Get second page
            >>> data_page2 = mmdb.harmonized_single_sample_by_medium("surface water", page_number=2)
        """
        if not medium or not isinstance(medium, str):
            raise ValueError("medium must be a non-empty string")
        
        if not isinstance(page_number, int) or page_number < 1:
            raise ValueError("page_number must be a positive integer")
        
        endpoint = "exposure/mmdb/single-sample/by-medium"
        params = {
            "medium": medium,
            "pageNumber": page_number
        }
        return self._make_request("GET", endpoint, params=params)
    
    def harmonized_single_sample_by_dtxsid(self, dtxsid: str) -> Dict[str, Any]:
        """
        Get harmonized single-sample records for a chemical.
        
        Retrieves harmonized single-sample environmental monitoring records for a
        specific chemical identified by its DSSTox Substance Identifier (DTXSID).
        This provides environmental occurrence data across different media and locations.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID7020182')
        
        Returns:
            Dictionary containing single-sample records for the specified chemical.
            Includes environmental measurements and detection information.
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> mmdb = MMDB()
            >>> samples = mmdb.harmonized_single_sample_by_dtxsid("DTXSID7020182")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/mmdb/single-sample/by-dtxsid/{dtxsid}"
        return self._make_request("GET", endpoint)

    def searchable_harmonized_medium_categories(self) -> List[Dict[str, Any]]:
        """
        Get all searchable harmonized medium categories.
        
        Retrieves a complete list of harmonized environmental medium categories
        available in the MMDB database, along with their definitions. This is useful
        for discovering valid medium types to use in other queries.
        
        Returns:
            List of dictionaries containing medium categories and their definitions.
            Each entry includes the medium name and description.
        
        Example:
            >>> mmdb = MMDB()
            >>> mediums = mmdb.searchable_harmonized_medium_categories()
            >>> for medium in mediums:
            ...     print(f"{medium['name']}: {medium.get('definition', '')}")
        """
        endpoint = "exposure/mmdb/mediums"
        return self._make_request("GET", endpoint)

    def harmonized_aggregate_records_by_medium(self, medium: str, page_number: int = 1) -> Dict[str, Any]:
        """
        Get harmonized aggregate records by environmental medium.
        
        Retrieves aggregated (summarized) environmental monitoring records filtered
        by the type of environmental medium. Aggregate records provide summary
        statistics across multiple samples, useful for trend analysis and overview.
        The data is paginated to handle large result sets.
        
        Args:
            medium: Harmonized medium type (e.g., 'surface water', 'air', 'soil',
                'groundwater', 'sediment', 'biota')
            page_number: Page number for pagination (default: 1)
        
        Returns:
            Dictionary containing paginated aggregate records for the specified medium.
            Includes summary statistics and aggregated measurements.
        
        Raises:
            ValueError: If medium is not a valid non-empty string or page_number is invalid
        
        Example:
            >>> mmdb = MMDB()
            >>> # Get first page of surface water aggregates
            >>> agg_data = mmdb.harmonized_aggregate_records_by_medium("surface water")
            >>> 
            >>> # Get second page
            >>> agg_page2 = mmdb.harmonized_aggregate_records_by_medium("surface water", page_number=2)
        """
        if not medium or not isinstance(medium, str):
            raise ValueError("medium must be a non-empty string")
        
        if not isinstance(page_number, int) or page_number < 1:
            raise ValueError("page_number must be a positive integer")
        
        endpoint = "exposure/mmdb/aggregate/by-medium"
        params = {
            "medium": medium,
            "pageNumber": page_number
        }
        return self._make_request("GET", endpoint, params=params)