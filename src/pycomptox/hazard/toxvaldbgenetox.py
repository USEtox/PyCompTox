"""
ToxValDB Genotoxicity API client for EPA CompTox Dashboard.

This module provides access to genotoxicity test data including:
- Ames test results (bacterial mutagenicity)
- Comet assay results (DNA strand breaks)
- Micronucleus test results (chromosomal damage)
- Chromosomal aberration test results
- Summary and detailed genotoxicity assessments

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient

class ToxValDBGenetox(CachedAPIClient):
    """
    Client for accessing genotoxicity test data from EPA CompTox Dashboard.
    
    Genotoxicity testing, also known as short-term assays, is used to evaluate 
    the potential adverse effects of chemicals on human health. These tests can 
    help identify carcinogens, as about 80% of known human carcinogens are genotoxic.
    
    The results of genotoxicity tests are important because of the irreversible 
    nature and severity of the health effects that may result from genotoxic events.
    
    Common genotoxicity test types include:
    - Ames test: Comparative genetic analysis using multiple bacterial strains 
      of Salmonella typhimurium
    - Comet assay: Measurement of DNA strand breaks
    - Micronucleus test: Cytogenetic assay using fluorescence in situ hybridization 
      and chromosome painting
    - Chromosomal aberration test: Cytogenetic assay examining in vivo tissues to 
      reflect how chemicals are absorbed, excreted, distributed, and metabolized
    
    This class provides both summary-level and detailed genotoxicity data for chemicals.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        use_cache (bool): Whether to use caching by default. Default is True.
    
    Example:
        >>> from pycomptox.hazard import ToxValDBGenetox
        >>> genetox = ToxValDBGenetox()
        >>> 
        >>> # Get genotoxicity summary for a chemical
        >>> summary = genetox.get_summary_by_dtxsid("DTXSID0021125")
        >>> if summary:
        ...     print(f"Found {len(summary)} genotoxicity summary records")
    """
    
    def get_summary_by_dtxsid(self, dtxsid: str, 
                              use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get genotoxicity summary data by DTXSID.
        
        Retrieves summary-level genotoxicity test information for a chemical. 
        Summary data provides an overview of genotoxicity testing results across 
        different assay types.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0021125')
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing genotoxicity summary data with fields such as:
                - dtxsid (str): Chemical identifier
                - testType (str): Type of genotoxicity test
                - result (str): Overall test result (positive/negative)
                - callSummary (str): Summary of test calls
                - numberOfPositive (int): Number of positive results
                - numberOfNegative (int): Number of negative results
                - numberOfTests (int): Total number of tests
                - source (str): Data source
                - Notes: Exact fields vary by test type
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox.hazard import ToxValDBGenetox
            >>> genetox = ToxValDBGenetox()
            >>> 
            >>> # Get genotoxicity summary for benzene
            >>> summary = genetox.get_summary_by_dtxsid("DTXSID0021125")
            >>> 
            >>> if summary:
            ...     print(f"Found {len(summary)} genotoxicity summary records")
            ...     
            ...     for record in summary:
            ...         test_type = record.get('testType', 'Unknown')
            ...         result = record.get('result', 'N/A')
            ...         print(f"\n{test_type}: {result}")
            ...         
            ...         if record.get('numberOfTests'):
            ...             pos = record.get('numberOfPositive', 0)
            ...             neg = record.get('numberOfNegative', 0)
            ...             total = record.get('numberOfTests', 0)
            ...             print(f"  Tests: {pos} positive, {neg} negative (out of {total} total)")
            >>> else:
            ...     print("No genotoxicity summary data available")
        
        Note:
            - Not all chemicals have genotoxicity test data
            - Summary provides overview across multiple tests
            - For detailed test results, use get_detail_by_dtxsid()
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"hazard/genetox/summary/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_detail_by_dtxsid(self, dtxsid: str, projection: Optional[str] = None,
                           use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get detailed genotoxicity data by DTXSID.
        
        Retrieves detailed genotoxicity test information for a chemical, including 
        individual test results, experimental conditions, and study details. 
        Optionally use projection for CompTox Dashboard-specific formatting.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID7020182')
            projection: Optional projection name. Use 'ccd-genetox-details' for 
                CompTox Dashboard Genetoxicity Details page format. If None, 
                returns default GenetoxDetail data.
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing detailed genotoxicity data with fields such as:
                - dtxsid (str): Chemical identifier
                - testName (str): Specific test name
                - testType (str): Type of genotoxicity test
                - result (str): Test result (positive/negative/equivocal)
                - strain (str): Biological strain used
                - species (str): Test species
                - metabolicActivation (str): Metabolic activation system used
                - dose (str): Dose information
                - doseUnits (str): Dose units
                - endpoint (str): Measured endpoint
                - reference (str): Study reference
                - source (str): Data source
                - year (int): Study year
                - Notes: Exact fields vary by test type and projection
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox.hazard import ToxValDBGenetox
            >>> genetox = ToxValDBGenetox()
            >>> 
            >>> # Get detailed genotoxicity data
            >>> details = genetox.get_detail_by_dtxsid("DTXSID7020182")
            >>> 
            >>> if details:
            ...     print(f"Found {len(details)} detailed genotoxicity test records")
            ...     
            ...     # Group by test type
            ...     by_type = {}
            ...     for detail in details:
            ...         test_type = detail.get('testType', 'Unknown')
            ...         if test_type not in by_type:
            ...             by_type[test_type] = []
            ...         by_type[test_type].append(detail)
            ...     
            ...     # Display results by test type
            ...     for test_type, tests in sorted(by_type.items()):
            ...         print(f"\n{test_type}: {len(tests)} test(s)")
            ...         
            ...         # Count positive/negative results
            ...         pos = sum(1 for t in tests if 'positive' in str(t.get('result', '')).lower())
            ...         neg = sum(1 for t in tests if 'negative' in str(t.get('result', '')).lower())
            ...         print(f"  Positive: {pos}, Negative: {neg}")
            ...         
            ...         # Show example test
            ...         if tests:
            ...             ex = tests[0]
            ...             print(f"  Example: {ex.get('testName', 'N/A')}")
            ...             print(f"    Result: {ex.get('result', 'N/A')}")
            ...             if ex.get('strain'):
            ...                 print(f"    Strain: {ex['strain']}")
            >>> 
            >>> # Get with CompTox Dashboard projection
            >>> ccd_details = genetox.get_detail_by_dtxsid("DTXSID7020182", 
            ...                                             projection="ccd-genetox-details")
        
        Note:
            - Detailed data includes individual test results
            - Use projection='ccd-genetox-details' for dashboard-formatted data
            - Results may include multiple tests of the same type under different conditions
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"hazard/genetox/details/search/by-dtxsid/{dtxsid}"
        params = {"projection": projection} if projection else None
        
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)

    def get_summary_by_dtxsid_batch(self, dtxsids: List[str], 
                              use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get genotoxicity summary data for multiple chemicals in a single batch request.
        
        Batch retrieval of genotoxicity summary data for up to 200 chemicals.
        More efficient than making individual requests.
        
        Args:
            dtxsids: List of DSSTox Substance Identifiers (max 200)
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing genotoxicity summary data for all
            requested chemicals. Each entry includes similar fields as
            get_summary_by_dtxsid().
        
        Raises:
            ValueError: If dtxsids list is empty or contains more than 200 entries
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox.hazard import ToxValDBGenetox
            >>> genetox = ToxValDBGenetox()
            >>> 
            >>> # Get summary for multiple chemicals
            >>> dtxsids = ["DTXSID0021125", "DTXSID7020182", "DTXSID0020032"]
            >>> batch_summary = genetox.get_summary_by_dtxsid_batch(dtxsids)
            >>> 
            >>> # Group by chemical
            >>> by_chemical = {}
            >>> for record in batch_summary:
            ...     dtxsid = record['dtxsid']
            ...     if dtxsid not in by_chemical:
            ...         by_chemical[dtxsid] = []
            ...     by_chemical[dtxsid].append(record)
            >>> 
            >>> # Display summary for each chemical
            >>> for dtxsid, records in by_chemical.items():
            ...     print(f"\n{dtxsid}: {len(records)} test type(s)")
            ...     
            ...     # Check for positive results
            ...     positive = [r for r in records if 'positive' in str(r.get('result', '')).lower()]
            ...     if positive:
            ...         print(f"  WARNING: {len(positive)} positive genotoxicity result(s)")
        
        Note:
            - Maximum 200 DTXSIDs per request
            - Batch requests are more efficient than individual queries
            - Useful for screening chemical libraries for genotoxicity
        """
        if not dtxsids:
            raise ValueError("dtxsids list cannot be empty")
        
        if len(dtxsids) > 200:
            raise ValueError(f"Maximum 200 DTXSIDs allowed, got {len(dtxsids)}")
        
        endpoint = "hazard/genetox/summary/search/by-dtxsid/"
        return self._make_cached_request(
            endpoint, 
            json=dtxsids, 
            method='POST', 
            use_cache=use_cache
        )

    def get_detail_by_dtxsid_batch(self, dtxsids: List[str], projection: Optional[str] = None,
                           use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get detailed genotoxicity data for multiple chemicals in a single batch request.
        
        Batch retrieval of detailed genotoxicity test data for up to 200 chemicals.
        More efficient than making individual requests.
        
        Args:
            dtxsids: List of DSSTox Substance Identifiers (max 200)
            projection: Optional projection name. Use 'ccd-genetox-details' for 
                CompTox Dashboard format.
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing detailed genotoxicity data for all
            requested chemicals. Each entry includes similar fields as
            get_detail_by_dtxsid().
        
        Raises:
            ValueError: If dtxsids list is empty or contains more than 200 entries
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox.hazard import ToxValDBGenetox
            >>> genetox = ToxValDBGenetox()
            >>> 
            >>> # Get detailed data for multiple chemicals
            >>> dtxsids = ["DTXSID0021125", "DTXSID7020182"]
            >>> batch_details = genetox.get_detail_by_dtxsid_batch(dtxsids)
            >>> 
            >>> # Analyze results
            >>> if batch_details:
            ...     print(f"Retrieved {len(batch_details)} detailed test records")
            ...     
            ...     # Count by chemical
            ...     by_chemical = {}
            ...     for record in batch_details:
            ...         dtxsid = record['dtxsid']
            ...         by_chemical[dtxsid] = by_chemical.get(dtxsid, 0) + 1
            ...     
            ...     for dtxsid, count in by_chemical.items():
            ...         print(f"{dtxsid}: {count} detailed test record(s)")
            ...     
            ...     # Count test types across all chemicals
            ...     test_types = set(r.get('testType') for r in batch_details if r.get('testType'))
            ...     print(f"\nTest types represented: {', '.join(sorted(test_types))}")
        
        Note:
            - Maximum 200 DTXSIDs per request
            - Returns comprehensive test details for all chemicals
            - Batch requests are more efficient than individual queries
            - Results can be large for chemicals with extensive testing
        """
        if not dtxsids:
            raise ValueError("dtxsids list cannot be empty")
        
        if len(dtxsids) > 200:
            raise ValueError(f"Maximum 200 DTXSIDs allowed, got {len(dtxsids)}")
        
        endpoint = "hazard/genetox/details/search/by-dtxsid/"
        params = {"projection": projection} if projection else None
        
        return self._make_cached_request(
            endpoint, 
            json=dtxsids, 
            method='POST',
            params=params,
            use_cache=use_cache
        )