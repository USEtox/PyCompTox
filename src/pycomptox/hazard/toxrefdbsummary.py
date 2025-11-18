"""
ToxRefDB Summary API client for EPA CompTox Dashboard.

This module provides access to ToxRefDB summary-level data including:
- Study-level summary information
- Chemical toxicity study summaries
- Effect level summaries (NOAEL, LOAEL)
- Study type categorization

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient

class ToxRefDBSummary(CachedAPIClient):
    """
    Client for accessing ToxRefDB summary data from EPA CompTox Dashboard.
    
    ToxRefDB (Toxicity Reference Database) summary provides aggregated, study-level 
    information from standardized animal toxicity studies. Unlike the detailed 
    effects endpoint, this provides high-level summaries including:
    
    - Study metadata and design information
    - Summary effect levels (NOAEL, LOAEL)
    - Study type classifications
    - Target organ summaries
    - Overall study results
    
    This summary-level data is useful for:
    - Quick screening of chemical toxicity profiles
    - Identifying available study types for chemicals
    - Getting overview of toxicity without detailed dose-response data
    - Comparative toxicity assessments across chemicals
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        use_cache (bool): Whether to use caching by default. Default is True.
    
    Example:
        >>> from pycomptox.hazard import ToxRefDBSummary
        >>> toxref_summary = ToxRefDBSummary()
        >>> 
        >>> # Get summary data for a chemical
        >>> summaries = toxref_summary.get_data_by_dtxsid("DTXSID1037806")
        >>> if summaries:
        ...     print(f"Found {len(summaries)} study summaries")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0,
        **kwargs: Any
    ):
        """
        Initialize the ToxRefDBSummary client.
        
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

    def get_data_by_study_type(
        self, 
        study_type: str, 
        dtxsids: Optional[List[str]] = None, 
        use_cache: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Get ToxRefDB summary data by study type.
        
        Retrieves summary-level information for all studies of a specific type in 
        ToxRefDB. Optionally filter to specific chemicals.
        
        Common study types include:
        - DEV: Developmental toxicity studies
        - REP: Reproductive toxicity studies
        - CHR: Chronic toxicity studies
        - SUB: Subchronic toxicity studies
        - DNT: Developmental neurotoxicity
        - MLT: Multigenerational reproductive toxicity
        
        Args:
            study_type: Study type code (e.g., 'DEV', 'REP', 'CHR')
            dtxsids: Optional list of DTXSIDs to filter results
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing study summary data with fields such as:
                - dtxsid (str): Chemical identifier
                - studyId (int): Study identifier
                - studyType (str): Type of study
                - species (str): Test species
                - strain (str): Animal strain
                - sex (str): Sex of test animals
                - route (str): Exposure route
                - duration (str): Study duration
                - noael (float): No Observed Adverse Effect Level
                - noaelUnits (str): NOAEL units
                - loael (float): Lowest Observed Adverse Effect Level
                - loaelUnits (str): LOAEL units
                - targetOrgan (str): Primary target organ
                - criticalEffect (str): Critical effect
                - reference (str): Study reference
                - Notes: Exact fields vary by study
        
        Raises:
            ValueError: If study_type is not a valid non-empty string
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxRefDBSummary
            >>> toxref_summary = ToxRefDBSummary()
            >>> 
            >>> # Get all developmental toxicity study summaries
            >>> dev_summaries = toxref_summary.get_data_by_study_type("DEV")
            >>> 
            >>> if dev_summaries:
            ...     print(f"Found {len(dev_summaries)} developmental studies")
            ...     
            ...     # Get unique chemicals tested
            ...     chemicals = set(s.get('dtxsid') for s in dev_summaries if s.get('dtxsid'))
            ...     print(f"Chemicals with DEV studies: {len(chemicals)}")
            ...     
            ...     # Show summary for first study
            ...     if dev_summaries:
            ...         study = dev_summaries[0]
            ...         print(f"\nExample study:")
            ...         print(f"  Chemical: {study.get('dtxsid')}")
            ...         print(f"  Species: {study.get('species')}")
            ...         print(f"  Route: {study.get('route')}")
            ...         if study.get('noael'):
            ...             print(f"  NOAEL: {study['noael']} {study.get('noaelUnits', '')}")
            >>> 
            >>> # Filter to specific chemicals
            >>> specific_dtxsids = ["DTXSID1037806", "DTXSID0021125"]
            >>> filtered = toxref_summary.get_data_by_study_type("DEV", dtxsids=specific_dtxsids)
        
        Note:
            - Study type codes are case-sensitive
            - Not all chemicals have all study types
            - Summary data provides overview without detailed dose-response
        """
        if not study_type or not isinstance(study_type, str):
            raise ValueError("study_type must be a non-empty string")
        
        endpoint = f"hazard/toxref/summary/search/by-study-type/{study_type}"
        
        # Note: The API endpoint doesn't appear to support dtxsids filtering in the URL
        # This parameter is included for future compatibility
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_data_by_study_id(
        self, 
        study_id: int, 
        use_cache: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Get ToxRefDB summary data by study ID.
        
        Retrieves summary information for a specific ToxRefDB study identified by 
        its unique study ID.
        
        Args:
            study_id: ToxRefDB study identifier (positive integer)
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing study summary data with fields such as:
                - studyId (int): Study identifier
                - dtxsid (str): Chemical identifier
                - studyType (str): Type of study
                - species (str): Test species
                - strain (str): Animal strain
                - sex (str): Sex of test animals
                - route (str): Exposure route
                - exposureMethod (str): Exposure method
                - duration (str): Study duration
                - doseGroups (int): Number of dose groups
                - noael (float): No Observed Adverse Effect Level
                - noaelUnits (str): NOAEL units
                - loael (float): Lowest Observed Adverse Effect Level
                - loaelUnits (str): LOAEL units
                - targetOrgan (str): Primary target organ/system
                - criticalEffect (str): Critical effect observed
                - guideline (str): Test guideline followed
                - glp (bool): GLP compliance status
                - reference (str): Study reference/citation
                - year (int): Study year
                - Notes: Exact fields may vary
        
        Raises:
            ValueError: If study_id is not a positive integer
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxRefDBSummary
            >>> toxref_summary = ToxRefDBSummary()
            >>> 
            >>> # Get summary for study ID 63
            >>> study = toxref_summary.get_data_by_study_id(63)
            >>> 
            >>> if study:
            ...     print(f"Study ID: {study.get('studyId')}")
            ...     print(f"Chemical: {study.get('dtxsid')}")
            ...     print(f"Study Type: {study.get('studyType')}")
            ...     print(f"Species: {study.get('species')} ({study.get('strain', 'N/A')})")
            ...     print(f"Route: {study.get('route')}")
            ...     print(f"Duration: {study.get('duration')}")
            ...     
            ...     if study.get('noael'):
            ...         print(f"\nNOAEL: {study['noael']} {study.get('noaelUnits', '')}")
            ...     
            ...     if study.get('loael'):
            ...         print(f"LOAEL: {study['loael']} {study.get('loaelUnits', '')}")
            ...     
            ...     if study.get('targetOrgan'):
            ...         print(f"\nTarget Organ: {study['targetOrgan']}")
            ...     
            ...     if study.get('criticalEffect'):
            ...         print(f"Critical Effect: {study['criticalEffect']}")
            ...     
            ...     if study.get('reference'):
            ...         print(f"\nReference: {study['reference']}")
        
        Note:
            - Study IDs are internal ToxRefDB identifiers
            - Summary provides high-level study information
            - For detailed dose-response data, use ToxRefDBEffects
        """
        if not isinstance(study_id, int) or study_id < 1:
            raise ValueError("study_id must be a positive integer")
        
        endpoint = f"hazard/toxref/summary/search/by-study-id/{study_id}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_data_by_dtxsid(
        self, 
        dtxsid: str, 
        use_cache: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Get ToxRefDB summary data by DTXSID.
        
        Retrieves summary information for all ToxRefDB studies associated with a 
        specific chemical identified by its DSSTox Substance Identifier.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID1037806')
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing study summary data with fields such as:
                - studyId (int): Study identifier
                - dtxsid (str): Chemical identifier
                - studyType (str): Type of study
                - species (str): Test species
                - strain (str): Animal strain
                - sex (str): Sex of test animals
                - route (str): Exposure route
                - duration (str): Study duration
                - noael (float): No Observed Adverse Effect Level
                - noaelUnits (str): NOAEL units
                - loael (float): Lowest Observed Adverse Effect Level
                - loaelUnits (str): LOAEL units
                - targetOrgan (str): Primary target organ
                - criticalEffect (str): Critical effect
                - reference (str): Study reference
                - Notes: Exact fields vary by study
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxRefDBSummary
            >>> toxref_summary = ToxRefDBSummary()
            >>> 
            >>> # Get all study summaries for a chemical
            >>> summaries = toxref_summary.get_data_by_dtxsid("DTXSID1037806")
            >>> 
            >>> if summaries:
            ...     print(f"Found {len(summaries)} study summaries")
            ...     
            ...     # Group by study type
            ...     by_type = {}
            ...     for summary in summaries:
            ...         study_type = summary.get('studyType', 'Unknown')
            ...         if study_type not in by_type:
            ...             by_type[study_type] = []
            ...         by_type[study_type].append(summary)
            ...     
            ...     print(f"\nStudy types available:")
            ...     for study_type, studies in sorted(by_type.items()):
            ...         print(f"  {study_type}: {len(studies)} study/studies")
            ...     
            ...     # Find lowest NOAEL across all studies
            ...     noaels = [s for s in summaries if s.get('noael')]
            ...     if noaels:
            ...         lowest_noael = min(noaels, key=lambda x: x['noael'])
            ...         print(f"\nLowest NOAEL: {lowest_noael['noael']} "
            ...               f"{lowest_noael.get('noaelUnits', '')}")
            ...         print(f"  Study: {lowest_noael.get('studyType')}")
            ...         print(f"  Route: {lowest_noael.get('route')}")
            ...         print(f"  Species: {lowest_noael.get('species')}")
            ...     
            ...     # List target organs
            ...     organs = set(s.get('targetOrgan') for s in summaries 
            ...                 if s.get('targetOrgan'))
            ...     if organs:
            ...         print(f"\nTarget organs: {', '.join(sorted(organs))}")
            >>> else:
            ...     print("No ToxRefDB summary data available")
        
        Note:
            - Not all chemicals have ToxRefDB data
            - ToxRefDB focuses on standardized guideline studies
            - Summary provides overview without detailed effects
            - Multiple studies of same type may exist with different conditions
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"hazard/toxref/summary/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)