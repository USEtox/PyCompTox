"""
Functional Use API client for EPA CompTox Dashboard.

This module provides access to functional use data including:
- Functional use data by chemical (DTXSID)
- Functional use probability predictions
- Functional use categories
- Batch operations for multiple chemicals

Author: PyCompTox Contributors
License: MIT
"""

import time
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urljoin

from ..base import CachedAPIClient


class FunctionalUse(CachedAPIClient):
    """
    Client for accessing functional use data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving functional use information,
    which describes how chemicals are used in products and applications.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float, **kwargs): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import FunctionalUse
        >>> func_use = FunctionalUse()
        >>> 
        >>> # Get functional use data for a chemical
        >>> data = func_use.functiona_use_by_dtxsid("DTXSID0020232")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0
    , **kwargs):
        """
        Initialize the FunctionalUse client.
        
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
    
    def functiona_use_by_dtxsid(self, dtxsid: str, use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get functional use data for a chemical.
        
        Retrieves functional use information for a specific chemical identified by
        its DSSTox Substance Identifier (DTXSID). Functional use describes how a
        chemical is used in products and industrial applications.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0020232')
        
        Returns:
            List of dictionaries containing functional use data for the chemical.
            Each entry includes use category, harmonized function, and other metadata.
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> func_use = FunctionalUse()
            >>> data = func_use.functiona_use_by_dtxsid("DTXSID0020232")
            >>> for use in data:
            ...     print(f"{use.get('harmonizedFunctionalUse', 'N/A')}")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/functional-use/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def functional_use_probability_by_dtxsid(self, dtxsid: str, use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get predicted functional use probabilities for a chemical.
        
        Retrieves predicted functional use probabilities for a specific chemical.
        These predictions estimate the likelihood that a chemical is used for
        various functional purposes based on modeling.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0020232')
        
        Returns:
            List of dictionaries containing functional use predictions with
            probability scores for different use categories.
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> func_use = FunctionalUse()
            >>> probs = func_use.functional_use_probability_by_dtxsid("DTXSID0020232")
            >>> for pred in probs:
            ...     print(f"{pred.get('functionalUse')}: {pred.get('probability')}")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/functional-use/probability/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def functiona_use_categories(self, use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get all functional use categories.
        
        Retrieves a complete list of functional use categories available in the
        database. This is useful for understanding the available classification
        system for chemical functional uses.
        
        Returns:
            List of dictionaries containing functional use categories with their
            names, descriptions, and hierarchical information.
        
        Example:
            >>> func_use = FunctionalUse()
            >>> categories = func_use.functiona_use_categories()
            >>> for cat in categories:
            ...     print(f"{cat.get('category', 'N/A')}: {cat.get('description', '')}")
        """
        endpoint = "exposure/functional-use/category"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def functional_use_by_dtxsid_batch(self, dtxsids: List[str], use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get functional use data for multiple chemicals in a single request.
        
        Retrieves functional use information for multiple chemicals at once using
        a batch API call. This is more efficient than making individual requests
        for each chemical.
        
        Args:
            dtxsids: List of DSSTox Substance Identifiers
        
        Returns:
            List of dictionaries containing functional use data for all requested
            chemicals. Results include the DTXSID and associated functional use
            information for each chemical.
        
        Raises:
            ValueError: If dtxsids is not a valid non-empty list
        
        Example:
            >>> func_use = FunctionalUse()
            >>> dtxsids = ["DTXSID0020232", "DTXSID7020182"]
            >>> batch_data = func_use.functional_use_by_dtxsid_batch(dtxsids)
            >>> for result in batch_data:
            ...     print(f"{result.get('dtxsid')}: {result.get('harmonizedFunctionalUse')}")
        """
        if not dtxsids or not isinstance(dtxsids, list) or len(dtxsids) == 0:
            raise ValueError("dtxsids must be a non-empty list of strings")
        
        if not all(isinstance(dtxsid, str) for dtxsid in dtxsids):
            raise ValueError("All elements in dtxsids must be strings")
        
        endpoint = "exposure/functional-use/search/by-dtxsid/"
        return self._make_request("POST", endpoint, json_data=dtxsids)