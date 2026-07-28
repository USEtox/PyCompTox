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

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient


class HTTKData(CachedAPIClient):
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
        time_delay_between_calls (float, **kwargs): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import HTTKData
        >>> httk = HTTKData()
        >>> 
        >>> # Get HTTK data for a chemical
        >>> data = httk.get_httk_data_by_dtxsid("DTXSID0020232")
    """
    
    def get_httk_data_by_dtxsid(self, dtxsid: str, use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
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
            >>> data = httk.get_httk_data_by_dtxsid("DTXSID0020232")
            >>> for param in data:
            ...     print(f"{param.get('parameter')}: {param.get('value')} {param.get('units')}")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/httk/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_httk_data_by_dtxsid_batch(self, dtxsid_list: List[str], use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
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
            >>> batch_data = httk.get_httk_data_by_dtxsid_batch(dtxsids)
            >>> for result in batch_data:
            ...     print(f"{result.get('dtxsid')}: {result.get('parameter')} = {result.get('value')}")
        """
        if not dtxsid_list or not isinstance(dtxsid_list, list) or len(dtxsid_list) == 0:
            raise ValueError("dtxsid_list must be a non-empty list of strings")
        
        if not all(isinstance(dtxsid, str) for dtxsid in dtxsid_list):
            raise ValueError("All elements in dtxsid_list must be strings")
        
        endpoint = "exposure/httk/search/by-dtxsid/"
        return self._make_cached_request(
            endpoint, method='POST', json=dtxsid_list, use_cache=use_cache
        )
