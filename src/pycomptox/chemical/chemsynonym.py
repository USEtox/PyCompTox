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

from ..base import CachedAPIClient


class ChemSynonym(CachedAPIClient):
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
        time_delay_between_calls (float, **kwargs): Delay in seconds between API calls for
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
    , **kwargs):
        """
        Initialize the ChemSynonym client.
        
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
    
    def get_synonyms_by_dtxsid(
        self,
        dtxsid: str,
        projection: Optional[str] = None
    , use_cache: Optional[bool] = None) -> Dict[str, Any]:
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
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)

    def get_synonyms_by_dtxsid_batch(
        self,
        dtxsid_list: List[str]
    , use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
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
        return self._make_cached_request(endpoint, method='POST', json=dtxsid_list, use_cache=use_cache)
        