"""
PubChem GHS Safety Data Link Module

This module provides access to the CompTox Dashboard PubChem GHS Safety Data Link API.
It allows checking whether chemicals have GHS safety data available on PubChem.

Classes:
    PubChemLink: Client for accessing PubChem GHS safety data links
"""

from typing import List, Dict, Any, Optional
import requests
import time
from pathlib import Path

from ..base import CachedAPIClient


class PubChemLink(CachedAPIClient):
    """
    Client for accessing PubChem GHS Safety Data Link information from the CompTox Dashboard API.
    
    This class provides methods to check whether chemicals have GHS (Globally Harmonized System)
    safety data available on PubChem.
    
    Attributes:
        base_url (str): Base URL for the CompTox Dashboard API
        api_key (Optional[str]): API key for authentication
        rate_limit_delay (float): Minimum delay between API calls in seconds
        session (requests.Session): HTTP session for making requests
        
    Examples:
        >>> from pycomptox import PubChemLink
        >>> client = PubChemLink()
        >>> result = client.check_existence_by_dtxsid("DTXSID7020182")
        >>> print(result['isSafetyData'])
        True
        >>> print(result['safetyUrl'])
        'https://pubchem.ncbi.nlm.nih.gov/compound/DTXSID7020182#section=GHS-Classification'
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        rate_limit_delay: float = 0.5,
        base_url: str = "https://comptox.epa.gov/ctx-api",
        **kwargs
    ):
        """
        Initialize the PubChemLink client.
        
        Args:
            api_key: Optional API key for authentication. If not provided,
                    will attempt to load from saved configuration.
            rate_limit_delay: Minimum delay between API calls in seconds (default: 0.5)
            base_url: Base URL for the CompTox Dashboard API
            **kwargs: Additional arguments for CachedAPIClient
            
        Examples:
            >>> # Initialize with default settings (loads saved API key)
            >>> client = PubChemLink()
            
            >>> # Initialize with custom API key
            >>> client = PubChemLink(api_key="your-api-key-here")
            
            >>> # Initialize with custom rate limiting
            >>> client = PubChemLink(rate_limit_delay=1.0)
        """
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            time_delay_between_calls=rate_limit_delay,
            **kwargs
        )
    
    def check_existence_by_dtxsid(self, dtxsid: str, use_cache: Optional[bool] = None) -> Dict[str, Any]:
        """
        Check if PubChem has GHS Safety data for a chemical identified by DTXSID.
        
        This method queries the CompTox Dashboard API to determine whether PubChem
        contains GHS (Globally Harmonized System) safety data for the specified chemical.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., "DTXSID7020182")
            
        Returns:
            Dictionary containing:
                - dtxsid (str): The chemical's DTXSID
                - isSafetyData (bool): True if PubChem has GHS safety data
                - safetyUrl (str): URL to the PubChem GHS classification page, or empty string if no data
                
        Raises:
            ValueError: If dtxsid is empty or invalid format
            RuntimeError: If the API request fails
            
        Examples:
            >>> from pycomptox import PubChemLink
            >>> client = PubChemLink()
            
            >>> # Check for Bisphenol A
            >>> result = client.check_existence_by_dtxsid("DTXSID7020182")
            >>> print(f"Has PubChem data: {result['isSafetyData']}")
            Has PubChem data: True
            >>> print(f"URL: {result['safetyUrl']}")
            URL: https://pubchem.ncbi.nlm.nih.gov/compound/DTXSID7020182#section=GHS-Classification
            
            >>> # Check chemical without PubChem data
            >>> result = client.check_existence_by_dtxsid("DTXSID0000001")
            >>> print(f"Has PubChem data: {result['isSafetyData']}")
            Has PubChem data: False
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"chemical/ghslink/to-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def check_existence_by_dtxsid_batch(self, dtxsids: List[str], use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Check if PubChem has GHS Safety data for multiple chemicals by DTXSID.
        
        This method performs a batch query to check PubChem GHS safety data availability
        for multiple chemicals at once. This is more efficient than making individual
        requests for each chemical.
        
        Args:
            dtxsids: List of DSSTox Substance Identifiers (e.g., ["DTXSID7020182", "DTXSID2021315"])
                    Maximum 1000 DTXSIDs per request.
                    
        Returns:
            List of dictionaries, each containing:
                - dtxsid (str): The chemical's DTXSID
                - isSafetyData (bool): True if PubChem has GHS safety data
                - safetyUrl (str): URL to the PubChem GHS classification page, or empty string if no data
                
        Raises:
            ValueError: If dtxsids is empty, not a list, or contains more than 1000 items
            RuntimeError: If the API request fails
            
        Examples:
            >>> from pycomptox import PubChemLink
            >>> client = PubChemLink()
            
            >>> # Check multiple chemicals
            >>> dtxsids = ["DTXSID7020182", "DTXSID2021315", "DTXSID5020001"]
            >>> results = client.check_existence_by_dtxsid_batch(dtxsids)
            >>> for result in results:
            ...     print(f"{result['dtxsid']}: {result['isSafetyData']}")
            DTXSID7020182: True
            DTXSID2021315: True
            DTXSID5020001: False
            
            >>> # Find chemicals with PubChem data
            >>> with_data = [r for r in results if r['isSafetyData']]
            >>> print(f"Found {len(with_data)} chemicals with PubChem GHS data")
            Found 2 chemicals with PubChem GHS data
        """
        if not dtxsids or not isinstance(dtxsids, list):
            raise ValueError("dtxsids must be a non-empty list")
        
        if len(dtxsids) > 1000:
            raise ValueError("Maximum 1000 DTXSIDs allowed per batch request")
        
        endpoint = "chemical/ghslink/to-dtxsid/"
        return self._make_cached_request(endpoint, method='POST', json=dtxsids, use_cache=use_cache)
