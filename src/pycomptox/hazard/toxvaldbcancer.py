"""
ToxValDB Cancer Summary API client for EPA CompTox Dashboard.

This module provides access to cancer hazard summary data including:
- Cancer classification and weight of evidence assessments
- Carcinogenicity evaluations from various agencies
- Cancer hazard identification data

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient


class ToxValDBCancer(CachedAPIClient):
    """
    Client for accessing ToxValDB cancer summary data from EPA CompTox Dashboard.
    
    A carcinogen is a substance that may cause cancer and pose a health hazard. 
    Carcinogens are subject to specific controls and regulations. National and 
    international health agencies evaluate new and existing chemicals to determine 
    if they are likely to be carcinogens through a process called cancer hazard identification. 
    This process combines human and animal data with supporting evidence to characterize 
    the weight-of-evidence (WOE) regarding the agent's potential as a human carcinogen. 
    
    The general categories recognized by the guidelines are:
    - Carcinogenic to humans
    - Likely to be carcinogenic to humans
    - Suggestive evidence of carcinogenic potential
    
    This class provides methods for retrieving summary-level cancer data associated 
    with chemicals.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        use_cache (bool): Whether to use caching by default. Default is True.
    
    Example:
        >>> from pycomptox.hazard import ToxValDBCancer
        >>> cancer = ToxValDBCancer()
        >>> 
        >>> # Get cancer data for a chemical
        >>> data = cancer.get_data_by_dtxsid("DTXSID0021125")
        >>> if data:
        ...     print(f"Cancer classification: {data[0].get('classification')}")
    """
    
    def get_data_by_dtxsid(self, dtxsid: str, 
                           use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get cancer summary data by DTXSID.
        
        Retrieves cancer hazard summary data for a specific chemical identified by 
        its DSSTox Substance Identifier (DTXSID). This includes cancer classifications,
        weight of evidence assessments, and carcinogenicity evaluations from various
        regulatory agencies and scientific organizations.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0021125')
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing cancer summary data with fields such as:
                - dtxsid (str): DSSTox Substance Identifier
                - classification (str): Cancer classification
                - source (str): Source of the assessment
                - woe (str): Weight of evidence
                - cancerType (str): Type of cancer
                - species (str): Test species
                - studyType (str): Type of study
                - evidence (str): Evidence description
                - route (str): Exposure route
                - Notes: Exact fields may vary based on the data source
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox.hazard import ToxValDBCancer
            >>> cancer = ToxValDBCancer()
            >>> 
            >>> # Get cancer data for benzene
            >>> data = cancer.get_data_by_dtxsid("DTXSID0021125")
            >>> 
            >>> if data:
            ...     for record in data:
            ...         print(f"Source: {record.get('source')}")
            ...         print(f"Classification: {record.get('classification')}")
            ...         if record.get('woe'):
            ...             print(f"Weight of Evidence: {record['woe']}")
            ...         if record.get('cancerType'):
            ...             print(f"Cancer Type: {record['cancerType']}")
            ...         print()
            >>> else:
            ...     print("No cancer data available for this chemical")
        
        Note:
            - Not all chemicals have cancer assessment data
            - Data may come from multiple sources (EPA, IARC, NTP, etc.)
            - Classifications and terminology vary by source
            - Weight of Evidence (WoE) indicates the strength and quality
              of evidence supporting the carcinogenicity assessment
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"hazard/cancer-summary/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_data_by_dtxsid_batch(self, dtxsids: List[str], 
                                 use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get cancer summary data for multiple chemicals in a single request.
        
        Batch retrieval of cancer hazard summary data for up to 200 chemicals.
        More efficient than making individual requests when querying multiple chemicals.
        
        Args:
            dtxsids: List of DSSTox Substance Identifiers (max 200)
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing cancer summary data for all
            requested chemicals. Each entry includes similar fields as
            get_data_by_dtxsid().
        
        Raises:
            ValueError: If dtxsids list is empty or contains more than 200 entries
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox.hazard import ToxValDBCancer
            >>> cancer = ToxValDBCancer()
            >>> 
            >>> # Get cancer data for multiple chemicals
            >>> dtxsids = ["DTXSID0021125", "DTXSID7020182", "DTXSID0020032"]
            >>> batch_data = cancer.get_data_by_dtxsid_batch(dtxsids)
            >>> 
            >>> # Group by chemical
            >>> by_chemical = {}
            >>> for record in batch_data:
            ...     dtxsid = record['dtxsid']
            ...     if dtxsid not in by_chemical:
            ...         by_chemical[dtxsid] = []
            ...     by_chemical[dtxsid].append(record)
            >>> 
            >>> # Display summary
            >>> for dtxsid, records in by_chemical.items():
            ...     print(f"{dtxsid}: {len(records)} cancer assessment(s)")
            ...     for record in records:
            ...         print(f"  - {record.get('source')}: {record.get('classification')}")
        
        Note:
            - Maximum 200 DTXSIDs per request
            - Results may include multiple assessments per chemical from different sources
            - Batch requests are more efficient than individual queries
        """
        if not dtxsids:
            raise ValueError("dtxsids list cannot be empty")
        
        if len(dtxsids) > 200:
            raise ValueError(f"Maximum 200 DTXSIDs allowed, got {len(dtxsids)}")
        
        endpoint = "hazard/cancer-summary/search/by-dtxsid/"
        return self._make_cached_request(
            endpoint, 
            json=dtxsids, 
            method='POST', 
            use_cache=use_cache
        )