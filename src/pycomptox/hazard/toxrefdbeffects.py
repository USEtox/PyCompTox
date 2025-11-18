"""
ToxRefDB Effects API client for EPA CompTox Dashboard.

This module provides access to ToxRefDB effects data including:
- Dose-treatment group-effect information
- Study-level toxicity data
- Effect levels (LEL, LOAEL, NEL, NOAEL)
- Chemical toxicity study results

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient


class ToxRefDBEffects(CachedAPIClient):
    """
    Client for accessing ToxRefDB effects data from EPA CompTox Dashboard.
    
    ToxRefDB (Toxicity Reference Database) contains detailed toxicity study data 
    extracted from standardized animal testing studies. This class provides access to 
    dose-treatment group-effect information including:
    
    - Effect levels (LEL, LOAEL, NEL, NOAEL)
    - Study types (developmental, reproductive, chronic, etc.)
    - Treatment group information
    - Organ and system effects
    - Dose-response relationships
    
    Data from ToxRefDB is also summarized in ToxValDB, including inferred NEL 
    (No Effect Level) and NOAEL (No Observed Adverse Effect Level) based on 
    reported LEL (Lowest Effect Level) and LOAEL (Lowest Observed Adverse Effect Level).
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        use_cache (bool): Whether to use caching by default. Default is True.
    
    Example:
        >>> from pycomptox.hazard import ToxRefDBEffects
        >>> toxref = ToxRefDBEffects()
        >>> 
        >>> # Get effects data for a chemical
        >>> effects = toxref.get_data_by_dtxsid("DTXSID1037806")
        >>> if effects:
        ...     print(f"Found {len(effects)} effect records")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0,
        **kwargs: Any
    ):
        """
        Initialize the ToxRefDBEffects client.
        
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

    def get_data_by_study_type(self, study_type: str, page_number: int = 1, 
                               use_cache: Optional[bool] = None) -> Dict[str, Any]:
        """
        Get ToxRefDB effects data by study type.
        
        Export of all extracted dose-treatment group-effect information from ToxRefDB 
        for a specific study type. This view is available as an enhanced data sheet 
        from batch search on the CompTox Chemicals Dashboard.
        
        Common study types include:
        - DEV: Developmental toxicity studies
        - REP: Reproductive toxicity studies
        - CHR: Chronic toxicity studies
        - SUB: Subchronic toxicity studies
        - DNT: Developmental neurotoxicity
        - MLT: Multigenerational reproductive toxicity
        
        Args:
            study_type: Study type code (e.g., 'DEV', 'REP', 'CHR')
            page_number: Optional page number for paginated results (default: 1)
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            Dictionary containing paginated effects data with fields such as:
                - data (List[Dict]): List of effect records
                - page (int): Current page number
                - totalPages (int): Total number of pages
                - totalRecords (int): Total number of records
                
            Each effect record may include:
                - dtxsid (str): Chemical identifier
                - studyId (int): Study identifier
                - studyType (str): Type of study
                - effectLevel (str): Effect level (LEL, LOAEL, etc.)
                - dose (float): Dose value
                - doseUnits (str): Dose units
                - effect (str): Observed effect
                - organ (str): Target organ/system
                - species (str): Test species
                - Notes: Exact fields vary by study
        
        Raises:
            ValueError: If study_type is not a valid non-empty string
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxRefDBEffects
            >>> toxref = ToxRefDBEffects()
            >>> 
            >>> # Get developmental toxicity study data
            >>> dev_data = toxref.get_data_by_study_type("DEV")
            >>> 
            >>> if 'data' in dev_data:
            ...     effects = dev_data['data']
            ...     print(f"Found {len(effects)} developmental effects on page 1")
            ...     print(f"Total pages: {dev_data.get('totalPages', 'N/A')}")
            ...     
            ...     # Display first effect
            ...     if effects:
            ...         effect = effects[0]
            ...         print(f"Chemical: {effect.get('dtxsid')}")
            ...         print(f"Effect: {effect.get('effect')}")
            ...         print(f"Dose: {effect.get('dose')} {effect.get('doseUnits')}")
            >>> 
            >>> # Get next page
            >>> page2 = toxref.get_data_by_study_type("DEV", page_number=2)
        
        Note:
            - Results are paginated to manage large datasets
            - Study type codes are case-sensitive
            - Not all chemicals have data for all study types
        """
        if not study_type or not isinstance(study_type, str):
            raise ValueError("study_type must be a non-empty string")
        
        if not isinstance(page_number, int) or page_number < 1:
            raise ValueError("page_number must be a positive integer")
        
        endpoint = f"hazard/toxref/effects/search/by-study-type/{study_type}"
        params = {"page_number": page_number} if page_number > 1 else None
        
        return self._make_cached_request(
            endpoint, 
            params=params, 
            use_cache=use_cache
        )

    def get_data_by_study_id(self, study_id: int, 
                             use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get ToxRefDB effects data by study ID.
        
        Export of all extracted dose-treatment group-effect information from ToxRefDB 
        for a specific study. Each study ID represents a unique toxicity study with 
        detailed dose-response information.
        
        Args:
            study_id: ToxRefDB study identifier (positive integer)
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing effect records from the study, with fields:
                - dtxsid (str): Chemical identifier
                - studyId (int): Study identifier
                - studyType (str): Type of study
                - treatmentGroup (str): Treatment group identifier
                - dose (float): Dose administered
                - doseUnits (str): Units of dose
                - effect (str): Observed effect
                - effectLevel (str): Effect level classification
                - organ (str): Target organ/system
                - species (str): Test species
                - sex (str): Sex of test animals
                - duration (str): Study duration
                - Notes: Exact fields vary by study
        
        Raises:
            ValueError: If study_id is not a positive integer
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxRefDBEffects
            >>> toxref = ToxRefDBEffects()
            >>> 
            >>> # Get effects data for study ID 63
            >>> study_effects = toxref.get_data_by_study_id(63)
            >>> 
            >>> if study_effects:
            ...     print(f"Study contains {len(study_effects)} effect records")
            ...     
            ...     # Group by dose level
            ...     by_dose = {}
            ...     for effect in study_effects:
            ...         dose = effect.get('dose', 'Unknown')
            ...         if dose not in by_dose:
            ...             by_dose[dose] = []
            ...         by_dose[dose].append(effect)
            ...     
            ...     # Show effects by dose
            ...     for dose, effects in sorted(by_dose.items()):
            ...         print(f"\nDose {dose} {effects[0].get('doseUnits', '')}:")
            ...         for e in effects:
            ...             print(f"  - {e.get('effect')} in {e.get('organ')}")
        
        Note:
            - Each study typically contains multiple dose groups and effects
            - Study IDs are internal ToxRefDB identifiers
            - Effects are reported at different dose levels (control, low, mid, high)
        """
        if not isinstance(study_id, int) or study_id < 1:
            raise ValueError("study_id must be a positive integer")
        
        endpoint = f"hazard/toxref/effects/search/by-study-id/{study_id}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_data_by_dtxsid(self, dtxsid: str, 
                           use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get ToxRefDB effects data by DTXSID.
        
        Export of all extracted dose-treatment group-effect information from ToxRefDB 
        for a specific chemical identified by its DSSTox Substance Identifier. Returns 
        all effects observed across all studies for the chemical.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID1037806')
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing effect records with fields such as:
                - dtxsid (str): Chemical identifier
                - studyId (int): Study identifier
                - studyType (str): Type of study
                - treatmentGroup (str): Treatment group
                - dose (float): Dose value
                - doseUnits (str): Dose units
                - effect (str): Observed effect description
                - effectLevel (str): Effect level (LEL, LOAEL, NEL, NOAEL)
                - organ (str): Target organ or system
                - species (str): Test species
                - sex (str): Sex of test animals
                - route (str): Exposure route
                - duration (str): Study duration
                - Notes: Exact fields vary by study
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxRefDBEffects
            >>> toxref = ToxRefDBEffects()
            >>> 
            >>> # Get all ToxRefDB effects for a chemical
            >>> effects = toxref.get_data_by_dtxsid("DTXSID1037806")
            >>> 
            >>> if effects:
            ...     print(f"Found {len(effects)} effect records")
            ...     
            ...     # Get unique study types
            ...     study_types = set(e.get('studyType') for e in effects if e.get('studyType'))
            ...     print(f"Study types: {', '.join(sorted(study_types))}")
            ...     
            ...     # Find lowest effect levels
            ...     loaels = [e for e in effects if e.get('effectLevel') == 'LOAEL']
            ...     if loaels:
            ...         print(f"\nFound {len(loaels)} LOAEL records")
            ...         for loael in loaels[:5]:  # Show first 5
            ...             print(f"  {loael.get('studyType')}: {loael.get('dose')} "
            ...                   f"{loael.get('doseUnits')} - {loael.get('effect')}")
            ...     
            ...     # Group by organ system
            ...     by_organ = {}
            ...     for effect in effects:
            ...         organ = effect.get('organ', 'Unknown')
            ...         by_organ[organ] = by_organ.get(organ, 0) + 1
            ...     
            ...     print(f"\nEffects by organ system:")
            ...     for organ, count in sorted(by_organ.items(), 
            ...                                key=lambda x: x[1], reverse=True)[:10]:
            ...         print(f"  {organ}: {count}")
            >>> else:
            ...     print("No ToxRefDB data available for this chemical")
        
        Note:
            - Not all chemicals have ToxRefDB data
            - ToxRefDB focuses on standardized guideline studies
            - Data includes both adverse and non-adverse effects
            - Effect levels help identify critical doses for risk assessment
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"hazard/toxref/effects/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)
