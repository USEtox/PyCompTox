"""
ToxRefDB Observation API client for EPA CompTox Dashboard.

This module provides access to observations and endpoint observation status from 
ToxRefDB guideline studies. Endpoint observation status enables distinction between 
true negatives (tested with no effect) and false negatives (missing effects).

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient

class ToxRefDBObservation(CachedAPIClient):
    """
    Client for accessing ToxRefDB observation and endpoint status data from EPA CompTox Dashboard.
    
    This class provides access to all observations and endpoint observation status 
    according to relevant guideline profiles for chemicals, studies, or study types.
    
    ToxRefDB curations are guideline studies with specific testing requirements. 
    Guideline profiles are used to populate a list of observations that should be 
    reported and tested within each study - the endpoint observation status.
    
    **Endpoint Observation Status** enables:
    - Automated distinction of **true negatives** (tested with no effect observed)
    - Better understanding of **false negatives** (missing/untested effects)
    - Identification of which endpoints were actually evaluated
    - Assessment of study completeness against guideline requirements
    
    This is critical for proper interpretation of toxicology data, as the absence 
    of an effect report could mean either:
    1. The endpoint was tested and no effect was observed (true negative)
    2. The endpoint was not tested or not reported (false negative/missing data)
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        use_cache (bool): Whether to use caching by default. Default is True.
    
    Example:
        >>> from pycomptox.hazard import ToxRefDBObservation
        >>> obs = ToxRefDBObservation()
        >>> 
        >>> # Get observations for a study
        >>> study_obs = obs.get_observations_by_study_id(63)
        >>> 
        >>> # Check endpoint observation status
        >>> for observation in study_obs:
        ...     endpoint = observation.get('endpoint', 'Unknown')
        ...     status = observation.get('observationStatus', 'Unknown')
        ...     print(f"{endpoint}: {status}")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0,
        **kwargs: Any
    ):
        """
        Initialize the ToxRefDBObservation client.
        
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

    def get_observations_by_study_type(
        self, 
        study_type: str, 
        page_number: int = 1,
        use_cache: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Get ToxRefDB observations by study type with pagination.
        
        Retrieves all observations and endpoint observation status for studies 
        of a specified type. Results are paginated to handle large datasets.
        
        Observation data includes:
        - Endpoints that should be tested per guideline requirements
        - Observation status (tested/not tested, effect/no effect)
        - True negatives vs. missing data distinction
        - Guideline compliance information
        
        Common study types include:
        - DEV: Developmental toxicity studies
        - REP/REPRO: Reproductive toxicity studies
        - DNT: Developmental neurotoxicity studies
        - CHRON: Chronic toxicity studies
        - SUBCHRON: Subchronic toxicity studies
        
        Args:
            study_type: Study type code (e.g., 'DEV', 'REP', 'DNT')
            page_number: Page number for paginated results (default is 1)
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            Dictionary containing paginated results with fields:
                - data (list): List of observation records for this page
                - pageNumber (int): Current page number
                - recordsOnPage (int): Number of records on this page
                - studyType (str): The requested study type
                
            Each record in 'data' contains fields such as:
                - dtxsid (str): Chemical identifier
                - studyId (int): Study identifier
                - studyType (str): Type of study
                - endpoint (str): Toxicological endpoint
                - observationStatus (str): Status (observed/not observed/tested/etc.)
                - target (str): Target organ or system
                - effect (str): Observed effect (if any)
                - ageAtObservation (str): Age when observation was made
                - sex (str): Sex of test animals
                - generation (str): Generation (for reproductive studies)
                - guidelineRequired (bool): Whether endpoint is required by guideline
                - Notes: Exact fields vary by study type
        
        Raises:
            ValueError: If study_type is not a valid non-empty string or page_number < 1
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxRefDBObservation
            >>> obs = ToxRefDBObservation()
            >>> 
            >>> # Get developmental study observations
            >>> dev_obs = obs.get_observations_by_study_type("DEV", page_number=1)
            >>> 
            >>> print(f"Page {dev_obs['pageNumber']}")
            >>> print(f"Records on this page: {dev_obs['recordsOnPage']}")
            >>> 
            >>> # Analyze observation status
            >>> if dev_obs.get('data'):
            ...     tested = 0
            ...     not_tested = 0
            ...     effects = 0
            ...     
            ...     for record in dev_obs['data']:
            ...         status = record.get('observationStatus', '')
            ...         if 'tested' in status.lower():
            ...             tested += 1
            ...         if 'effect' in str(record.get('effect', '')).lower():
            ...             effects += 1
            ...     
            ...     print(f"Tested endpoints: {tested}")
            ...     print(f"Endpoints with effects: {effects}")
            >>> 
            >>> # Check guideline compliance
            >>> if dev_obs.get('data'):
            ...     required = [r for r in dev_obs['data'] if r.get('guidelineRequired')]
            ...     print(f"Guideline-required observations: {len(required)}")
        
        Note:
            - Results are paginated; use page_number to navigate
            - Observation status distinguishes true negatives from missing data
            - Guideline profiles define expected observations per study type
        """
        if not study_type or not isinstance(study_type, str):
            raise ValueError("study_type must be a non-empty string")
        
        if not isinstance(page_number, int) or page_number < 1:
            raise ValueError("page_number must be a positive integer")
        
        endpoint = f"hazard/toxref/observations/search/by-study-type/{study_type}"
        params = {"page": page_number}
        
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)

    def get_observations_by_study_id(
        self, 
        study_id: int,
        use_cache: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Get ToxRefDB observations by study ID.
        
        Retrieves all observations and endpoint observation status for a specific 
        study. This provides a complete view of what endpoints were evaluated and 
        their observation status.
        
        Args:
            study_id: ToxRefDB study identifier (integer)
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing observation data with fields such as:
                - dtxsid (str): Chemical identifier
                - studyId (int): Study identifier
                - studyType (str): Type of study
                - endpoint (str): Toxicological endpoint name
                - observationStatus (str): Status (observed/not observed/tested/not tested)
                - effect (str): Observed effect description (if any)
                - target (str): Target organ or system
                - finding (str): Detailed finding description
                - sex (str): Sex of test animals
                - ageAtObservation (str): Age when observation was made
                - generation (str): Generation studied (for reproductive studies)
                - doseGroup (str): Dose group information
                - guidelineRequired (bool): Whether endpoint is required by guideline
                - observationMethod (str): Method used for observation
                - Notes: Exact fields vary by study type
        
        Raises:
            ValueError: If study_id is not a positive integer
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxRefDBObservation
            >>> obs = ToxRefDBObservation()
            >>> 
            >>> # Get observations for a specific study
            >>> study_obs = obs.get_observations_by_study_id(63)
            >>> 
            >>> if study_obs:
            ...     print(f"Found {len(study_obs)} observations")
            ...     
            ...     # Get study metadata from first record
            ...     first = study_obs[0]
            ...     print(f"\nStudy ID: {first.get('studyId')}")
            ...     print(f"Chemical: {first.get('dtxsid')}")
            ...     print(f"Study Type: {first.get('studyType')}")
            ...     
            ...     # Analyze observation status
            ...     status_counts = {}
            ...     for record in study_obs:
            ...         status = record.get('observationStatus', 'Unknown')
            ...         status_counts[status] = status_counts.get(status, 0) + 1
            ...     
            ...     print(f"\nObservation status breakdown:")
            ...     for status, count in sorted(status_counts.items()):
            ...         print(f"  {status}: {count}")
            ...     
            ...     # Find endpoints with effects
            ...     with_effects = [r for r in study_obs if r.get('effect')]
            ...     print(f"\nEndpoints with effects: {len(with_effects)}")
            ...     
            ...     if with_effects:
            ...         print("\nSample effects:")
            ...         for rec in with_effects[:3]:
            ...             endpoint = rec.get('endpoint', 'Unknown')
            ...             effect = rec.get('effect', 'N/A')
            ...             target = rec.get('target', 'N/A')
            ...             print(f"  {endpoint} ({target}): {effect}")
            ...     
            ...     # Check guideline compliance
            ...     required = [r for r in study_obs if r.get('guidelineRequired')]
            ...     tested = [r for r in required if 'tested' in str(r.get('observationStatus', '')).lower()]
            ...     print(f"\nGuideline compliance:")
            ...     print(f"  Required observations: {len(required)}")
            ...     print(f"  Tested: {len(tested)}")
            ...     if required:
            ...         compliance = (len(tested) / len(required)) * 100
            ...         print(f"  Compliance: {compliance:.1f}%")
        
        Note:
            - A single study may have many endpoint observations
            - Observation status distinguishes true negatives from missing data
            - Use this to assess study completeness and guideline compliance
        """
        if not isinstance(study_id, int) or study_id < 1:
            raise ValueError("study_id must be a positive integer")
        
        endpoint = f"hazard/toxref/observations/search/by-study-id/{study_id}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_observations_by_dtxsid(
        self, 
        dtxsid: str,
        use_cache: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Get ToxRefDB observations by DTXSID.
        
        Retrieves all observations and endpoint observation status for a chemical 
        across all studies in ToxRefDB. This provides a comprehensive view of 
        toxicological observations across different study types and conditions.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID1037806')
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing observation data across all studies 
            for the chemical. Each entry includes fields such as:
                - dtxsid (str): Chemical identifier
                - studyId (int): Study identifier
                - studyType (str): Type of study
                - endpoint (str): Toxicological endpoint
                - observationStatus (str): Status of observation
                - effect (str): Observed effect (if any)
                - target (str): Target organ or system
                - finding (str): Detailed finding
                - sex (str): Sex of test animals
                - species (str): Test species
                - ageAtObservation (str): Age at observation
                - generation (str): Generation (for reproductive studies)
                - exposureDuration (str): Duration of exposure
                - doseGroup (str): Dose group information
                - guidelineRequired (bool): Guideline requirement status
                - reference (str): Study reference
                - Notes: Exact fields vary by study
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxRefDBObservation
            >>> obs = ToxRefDBObservation()
            >>> 
            >>> # Get all observations for a chemical
            >>> chem_obs = obs.get_observations_by_dtxsid("DTXSID1037806")
            >>> 
            >>> if chem_obs:
            ...     print(f"Found {len(chem_obs)} observations")
            ...     
            ...     # Group by study type
            ...     by_type = {}
            ...     for record in chem_obs:
            ...         stype = record.get('studyType', 'Unknown')
            ...         if stype not in by_type:
            ...             by_type[stype] = []
            ...         by_type[stype].append(record)
            ...     
            ...     print(f"\nObservations by study type:")
            ...     for stype, records in sorted(by_type.items()):
            ...         print(f"  {stype}: {len(records)} observation(s)")
            ...     
            ...     # Identify all endpoints tested
            ...     endpoints = set(r.get('endpoint') for r in chem_obs if r.get('endpoint'))
            ...     print(f"\nUnique endpoints tested: {len(endpoints)}")
            ...     
            ...     # Find all target organs/systems
            ...     targets = set(r.get('target') for r in chem_obs if r.get('target'))
            ...     print(f"Target organs/systems: {', '.join(sorted(targets))}")
            ...     
            ...     # Analyze observation status across all studies
            ...     status_counts = {}
            ...     for record in chem_obs:
            ...         status = record.get('observationStatus', 'Unknown')
            ...         status_counts[status] = status_counts.get(status, 0) + 1
            ...     
            ...     print(f"\nObservation status across all studies:")
            ...     for status, count in sorted(status_counts.items()):
            ...         print(f"  {status}: {count}")
            ...     
            ...     # Find consistent effects across studies
            ...     effects_by_endpoint = {}
            ...     for record in chem_obs:
            ...         endpoint = record.get('endpoint')
            ...         effect = record.get('effect')
            ...         if endpoint and effect:
            ...             if endpoint not in effects_by_endpoint:
            ...                 effects_by_endpoint[endpoint] = []
            ...             effects_by_endpoint[endpoint].append(effect)
            ...     
            ...     print(f"\nEndpoints with effects in multiple studies:")
            ...     for endpoint, effects in effects_by_endpoint.items():
            ...         if len(effects) > 1:
            ...             print(f"  {endpoint}: {len(effects)} observation(s)")
            ...     
            ...     # Compare across study types
            ...     dev_obs = [r for r in chem_obs if r.get('studyType') == 'DEV']
            ...     rep_obs = [r for r in chem_obs if r.get('studyType') == 'REP']
            ...     
            ...     if dev_obs:
            ...         dev_effects = [r for r in dev_obs if r.get('effect')]
            ...         print(f"\nDevelopmental studies: {len(dev_obs)} obs, {len(dev_effects)} with effects")
            ...     
            ...     if rep_obs:
            ...         rep_effects = [r for r in rep_obs if r.get('effect')]
            ...         print(f"Reproductive studies: {len(rep_obs)} obs, {len(rep_effects)} with effects")
        
        Note:
            - Returns observations from all available studies for the chemical
            - May include multiple study types and conditions
            - Useful for comprehensive hazard assessment across all available data
            - Observation status helps distinguish tested vs. untested endpoints
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"hazard/toxref/observations/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)