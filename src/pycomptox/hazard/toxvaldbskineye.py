"""
ToxValDB Skin and Eye Irritation API client for EPA CompTox Dashboard.

This module provides access to skin and eye irritation test data including:
- Draize test results
- EpiOcular Eye Irritation Test (EIT) data
- Red blood cell test results
- Patch test data
- Irritation and corrosivity assessments

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient


class ToxValDBSkinEye(CachedAPIClient):
    """
    Client for accessing skin and eye irritation data from EPA CompTox Dashboard.
    
    Skin and eye irritation tests are used to assess the safety of products and 
    chemicals that may come into contact with the skin or eyes. These tests are 
    important for:
    - Product safety labeling
    - Chemical registration requirements
    - Agrochemical safety assessment
    - Drug development and safety evaluation
    
    Types of skin and eye irritation tests include:
    - Draize test: Traditional rabbit eye/skin irritation test
    - EpiOcular Eye Irritation Test (EIT): In vitro alternative
    - Red blood cells test: Hemolysis-based assessment
    - Patch test: Human skin sensitization test
    
    This class provides methods for retrieving irritation and corrosivity data
    for chemicals, including severity scores, study details, and test outcomes.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        use_cache (bool): Whether to use caching by default. Default is True.
    
    Example:
        >>> from pycomptox.hazard import ToxValDBSkinEye
        >>> skineye = ToxValDBSkinEye()
        >>> 
        >>> # Get skin/eye irritation data for a chemical
        >>> data = skineye.get_data_by_dtxsid("DTXSID0021125")
        >>> if data:
        ...     print(f"Found {len(data)} irritation test records")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0,
        **kwargs: Any
    ):
        """
        Initialize the ToxValDBSkinEye client.
        
        Args:
            api_key: CompTox API key (optional, will be loaded from config if not provided)
            base_url: Base URL for the CompTox API
            time_delay_between_calls: Delay between API calls in seconds
            kwargs: Additional arguments for CachedAPIClient (cache_manager, use_cache)
        
        Raises:
            ValueError: If no API key is provided or found in configuration
        """
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            time_delay_between_calls=time_delay_between_calls,
            **kwargs
        )

    def get_data_by_dtxsid(self, dtxsid: str, 
                           use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get skin and eye irritation data by DTXSID.
        
        Retrieves skin and eye irritation test data for a specific chemical identified 
        by its DSSTox Substance Identifier. Includes results from various irritation 
        and corrosivity tests used for hazard assessment and product labeling.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0021125')
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing skin/eye irritation data with fields such as:
                - dtxsid (str): Chemical identifier
                - testType (str): Type of irritation test
                - endpoint (str): Measured endpoint
                - result (str): Test result or classification
                - score (float): Irritation score (when applicable)
                - severity (str): Severity classification
                - species (str): Test species or system
                - exposureDuration (str): Duration of exposure
                - source (str): Data source
                - study (str): Study reference
                - Notes: Exact fields vary by test type
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxValDBSkinEye
            >>> skineye = ToxValDBSkinEye()
            >>> 
            >>> # Get skin/eye irritation data for benzene
            >>> data = skineye.get_data_by_dtxsid("DTXSID0021125")
            >>> 
            >>> if data:
            ...     print(f"Found {len(data)} irritation test records")
            ...     
            ...     # Group by test type
            ...     by_test = {}
            ...     for record in data:
            ...         test_type = record.get('testType', 'Unknown')
            ...         if test_type not in by_test:
            ...             by_test[test_type] = []
            ...         by_test[test_type].append(record)
            ...     
            ...     # Display results by test type
            ...     for test_type, records in by_test.items():
            ...         print(f"\n{test_type}:")
            ...         for rec in records:
            ...             result = rec.get('result', 'N/A')
            ...             severity = rec.get('severity', '')
            ...             print(f"  - {result} {severity}")
            ...             if rec.get('score'):
            ...                 print(f"    Score: {rec['score']}")
            >>> else:
            ...     print("No skin/eye irritation data available")
        
        Note:
            - Not all chemicals have irritation test data
            - Multiple test types may be available for the same chemical
            - Severity classifications vary by test method
            - Draize scores range from 0 (no irritation) to 4 (severe)
            - Data supports GHS hazard classification
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"hazard/skin-eye/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_data_by_dtxsid_batch(self, dtxsids: List[str], 
                                 use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get skin and eye irritation data for multiple chemicals in a single request.
        
        Batch retrieval of skin and eye irritation test data for up to 200 chemicals.
        More efficient than making individual requests when querying multiple chemicals.
        
        Args:
            dtxsids: List of DSSTox Substance Identifiers (max 200)
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing skin/eye irritation data for all
            requested chemicals. Each entry includes similar fields as
            get_data_by_dtxsid().
        
        Raises:
            ValueError: If dtxsids list is empty or contains more than 200 entries
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxValDBSkinEye
            >>> skineye = ToxValDBSkinEye()
            >>> 
            >>> # Get skin/eye data for multiple chemicals
            >>> dtxsids = ["DTXSID0021125", "DTXSID7020182", "DTXSID0020032"]
            >>> batch_data = skineye.get_data_by_dtxsid_batch(dtxsids)
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
            ...     print(f"{dtxsid}: {len(records)} test record(s)")
            ...     
            ...     # Check for severe irritation
            ...     severe = [r for r in records if 'severe' in str(r.get('severity', '')).lower()]
            ...     if severe:
            ...         print(f"  WARNING: {len(severe)} severe irritation result(s)")
            ...     
            ...     # List test types
            ...     tests = set(r.get('testType', 'Unknown') for r in records)
            ...     print(f"  Test types: {', '.join(tests)}")
        
        Note:
            - Maximum 200 DTXSIDs per request
            - Results may include multiple test records per chemical
            - Batch requests are more efficient than individual queries
            - Useful for screening chemical libraries for irritation potential
        """
        if not dtxsids:
            raise ValueError("dtxsids list cannot be empty")
        
        if len(dtxsids) > 200:
            raise ValueError(f"Maximum 200 DTXSIDs allowed, got {len(dtxsids)}")
        
        endpoint = "hazard/skin-eye/search/by-dtxsid/"
        return self._make_cached_request(
            endpoint, 
            json=dtxsids, 
            method='POST', 
            use_cache=use_cache
        )