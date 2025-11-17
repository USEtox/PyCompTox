"""
CCC Data API client for EPA CompTox Dashboard.

This module provides access to Chemical and Products Categories (CCC) data including:
- Product Use Category (PUC) data by chemical identifier

Author: PyCompTox Contributors
License: MIT
"""

import time
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urljoin

from .config import load_api_key


class CCCData:
    """
    Client for accessing Chemical and Products Categories (CCC) data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving Product Use Category (PUC) information
    for chemicals, which describes how chemicals are used in consumer products.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import CCCData
        >>> ccc = CCCData()
        >>> 
        >>> # Get product use category data
        >>> puc_data = ccc.product_use_category_by_dtxsid("DTXSID0020232")
        >>> print(f"Products: {puc_data[0].get('prodCount')}")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0
    ):
        """
        Initialize the CCCData client.
        
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

    def product_use_category_by_dtxsid(self, dtxsid: str) -> List[Dict[str, Any]]:
        """
        Get Product Use Category data for a chemical.
        
        Retrieves Product Use Category (PUC) information that describes how a chemical
        is used in consumer products. The PUC system categorizes products by general
        category, product family, and product type.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0020232')
        
        Returns:
            List of dictionaries containing PUC data with fields:
                - id: Record identifier
                - dtxsid: Chemical identifier
                - displayPuc: Display name for the PUC
                - pucKind: Kind of PUC classification
                - prodCount: Number of products
                - genCat: General category
                - prodfam: Product family
                - prodtype: Product type
                - definition: Definition of the category
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> ccc = CCCData()
            >>> puc_data = ccc.product_use_category_by_dtxsid("DTXSID0020232")
            >>> for puc in puc_data:
            ...     print(f"{puc['displayPuc']}: {puc['prodCount']} products")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/ccd/puc/search/by-dtxsid/{dtxsid}"
        return self._make_request("GET", endpoint)
    
    def production_volume_by_dtxsid(self, dtxsid: str) -> Dict[str, Any]:
        """
        Get Production Volume data for a chemical.
        
        Retrieves production volume information for a specific chemical identified
        by its DSSTox Substance Identifier (DTXSID).
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0020232')
        
        Returns:
            Dictionary containing production volume data with fields:
                - id: Record identifier
                - dtxsid: Chemical identifier
                - name: Production volume name/category
                - amount: Production volume amount
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> ccc = CCCData()
            >>> prod_vol = ccc.production_volume_by_dtxsid("DTXSID0020232")
            >>> print(f"Amount: {prod_vol['amount']}")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/ccd/production-volume/search/by-dtxsid/{dtxsid}"
        return self._make_request("GET", endpoint)

    def biomonitoring_data_by_dtxsid_and_ccd(self, dtxsid: str, projection: str = "") -> List[Dict[str, Any]]:
        """
        Get NHANES biomonitoring data for a chemical.
        
        Retrieves NHANES (National Health and Nutrition Examination Survey) biomonitoring
        inferences for a specific chemical. The data includes demographic information,
        median values, and confidence bounds.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID7020182')
            projection: Optional projection type. Use 'ccd-biomonitoring' for CCD exposure
                biomonitoring page format. If omitted, default CCDBiomonitoring data is returned.
        
        Returns:
            List of dictionaries containing biomonitoring data with fields:
                - id: Record identifier
                - dtxsid: Chemical identifier
                - demographic: Demographic group
                - median: Median value
                - upperBound: Upper confidence bound
                - lowerBound: Lower confidence bound
                - nhanesCohort: NHANES cohort identifier
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> ccc = CCCData()
            >>> biomon = ccc.biomonitoring_data_by_dtxsid_and_ccd("DTXSID7020182")
            >>> for record in biomon:
            ...     print(f"{record['demographic']}: {record['median']}")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/ccd/monitoring-data/search/by-dtxsid/{dtxsid}"
        params = {"projection": projection} if projection else None
        return self._make_request("GET", endpoint, params=params)

    def general_use_keywords_by_dtxsid(self, dtxsid: str) -> List[Dict[str, Any]]:
        """
        Get general use keywords data for a chemical.
        
        Retrieves keywords that describe the general uses of a chemical across
        various sources. This provides a high-level overview of how the chemical
        is commonly used.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0020232')
        
        Returns:
            List of dictionaries containing keyword data with fields:
                - id: Record identifier
                - keywordset: Set of keywords describing uses
                - sourceCount: Number of sources reporting this use
                - dtxsid: Chemical identifier
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> ccc = CCCData()
            >>> keywords = ccc.general_use_keywords_by_dtxsid("DTXSID0020232")
            >>> for kw in keywords:
            ...     print(f"{kw['keywordset']}: {kw['sourceCount']} sources")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/ccd/keywords/search/by-dtxsid/{dtxsid}"
        return self._make_request("GET", endpoint)

    def reported_functional_use_by_dtxsid(self, dtxsid: str) -> List[Dict[str, Any]]:
        """
        Get reported functional use data for a chemical.
        
        Retrieves reported functional use categories for a chemical, describing
        the specific functions or purposes for which the chemical is used in
        products (e.g., preservative, solvent, surfactant).
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0020232')
        
        Returns:
            List of dictionaries containing functional use data with fields:
                - id: Record identifier
                - dtxsid: Chemical identifier
                - category: Functional use category
                - definition: Definition of the functional use
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> ccc = CCCData()
            >>> func_uses = ccc.reported_functional_use_by_dtxsid("DTXSID0020232")
            >>> for use in func_uses:
            ...     print(f"{use['category']}: {use['definition']}")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/ccd/functional-use/search/by-dtxsid/{dtxsid}"
        return self._make_request("GET", endpoint)

    def chemical_weight_fraction_by_dtxsid(self, dtxsid: str) -> List[Dict[str, Any]]:
        """
        Get chemical weight fraction data for a chemical.
        
        Retrieves information about the weight fractions (concentrations) of a chemical
        in various products. This includes the product name, category, and the range
        of weight fractions reported.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0020232')
        
        Returns:
            List of dictionaries containing weight fraction data with fields:
                - id: Record identifier
                - dtxsid: Chemical identifier
                - prodName: Product name
                - displayPuc: Display name for Product Use Category
                - pucKind: Kind of PUC classification
                - lowerweightfraction: Lower bound of weight fraction
                - upperweightfraction: Upper bound of weight fraction
                - weightfractiontype: Type of weight fraction measurement
                - gencat: General category
                - prodfam: Product family
                - prod_type: Product type
                - pucDefinition: Definition of the PUC
                - sourceName: Name of data source
                - sourceDescription: Description of data source
                - sourceUrl: URL of data source
                - sourceDownloadDate: Date source was downloaded
                - productCount: Number of products
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> ccc = CCCData()
            >>> weight_fracs = ccc.chemical_weight_fraction_by_dtxsid("DTXSID0020232")
            >>> for wf in weight_fracs:
            ...     print(f"{wf['prodName']}: {wf['lowerweightfraction']}-{wf['upperweightfraction']}")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/ccd/chem-weight-fractions/search/by-dtxsid/{dtxsid}"
        return self._make_request("GET", endpoint)

