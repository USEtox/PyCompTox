"""
ToxRefDB Batch API client for EPA CompTox Dashboard.

This module provides batch access to ToxRefDB data including:
- Dose-treatment group-effect information
- Doses not eliciting effects (NEL)
- Effect levels (LEL, LOAEL, NEL, NOAEL)
- Batch retrieval for multiple chemicals

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient

class ToxRefDBBatch(CachedAPIClient):
    """
    Client for batch access to ToxRefDB data from EPA CompTox Dashboard.
    
    ToxRefDB (Toxicity Reference Database) batch endpoint provides efficient 
    retrieval of all extracted dose-treatment group-effect information as well as 
    doses not eliciting effects for multiple chemicals in a single request.
    
    This includes:
    - All dose-response data from ToxRefDB studies
    - Treatment group information
    - Effect observations at various doses
    - Doses not eliciting effects (NEL)
    - Effect level classifications (LEL, LOAEL)
    
    Data from ToxRefDB is also summarized in ToxValDB, including inferred NEL 
    (No Effect Level) and NOAEL (No Observed Adverse Effect Level) based on 
    reported LEL (Lowest Effect Level) and LOAEL (Lowest Observed Adverse Effect Level).
    
    This batch endpoint is more efficient than making individual requests when 
    querying multiple chemicals for ToxRefDB data.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        use_cache (bool): Whether to use caching by default. Default is True.
    
    Example:
        >>> from pycomptox.hazard import ToxRefDBBatch
        >>> toxref_batch = ToxRefDBBatch()
        >>> 
        >>> # Get ToxRefDB data for multiple chemicals
        >>> dtxsids = ["DTXSID1037806", "DTXSID0021125"]
        >>> data = toxref_batch.get_data_by_dtxsid_batch(dtxsids)
        >>> if data:
        ...     print(f"Found {len(data)} ToxRefDB records")
    """
    
    def get_data_by_dtxsid_batch(
        self, 
        dtxsids: List[str], 
        use_cache: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Get ToxRefDB data for multiple chemicals in a single batch request.
        
        Exports all extracted dose-treatment group-effect information as well as 
        doses not eliciting effects from ToxRefDB for the chemicals listed in the 
        input. This provides comprehensive dose-response data for up to 200 chemicals 
        in a single efficient request.
        
        Args:
            dtxsids: List of DSSTox Substance Identifiers (max 200)
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing ToxRefDB data for all requested 
            chemicals. Each record includes fields such as:
                - dtxsid (str): Chemical identifier
                - studyId (int): Study identifier
                - studyType (str): Type of study
                - treatmentGroup (str): Treatment group identifier
                - dose (float): Dose administered
                - doseUnits (str): Units of dose
                - effect (str): Observed effect
                - effectLevel (str): Effect level classification (LEL, LOAEL, NEL, NOAEL)
                - organ (str): Target organ or system
                - species (str): Test species
                - sex (str): Sex of test animals
                - route (str): Exposure route
                - duration (str): Study duration
                - effectType (str): Type of effect
                - severity (str): Severity of effect
                - notes (str): Additional notes
                - Notes: Exact fields vary by study and effect
        
        Raises:
            ValueError: If dtxsids list is empty or contains more than 200 entries
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox.hazard import ToxRefDBBatch
            >>> toxref_batch = ToxRefDBBatch()
            >>> 
            >>> # Get ToxRefDB data for multiple chemicals
            >>> dtxsids = ["DTXSID1037806", "DTXSID0021125", "DTXSID7020182"]
            >>> batch_data = toxref_batch.get_data_by_dtxsid_batch(dtxsids)
            >>> 
            >>> if batch_data:
            ...     print(f"Retrieved {len(batch_data)} ToxRefDB records")
            ...     
            ...     # Group by chemical
            ...     by_chemical = {}
            ...     for record in batch_data:
            ...         dtxsid = record['dtxsid']
            ...         if dtxsid not in by_chemical:
            ...             by_chemical[dtxsid] = []
            ...         by_chemical[dtxsid].append(record)
            ...     
            ...     # Display summary for each chemical
            ...     for dtxsid, records in by_chemical.items():
            ...         print(f"\n{dtxsid}: {len(records)} record(s)")
            ...         
            ...         # Get unique study types
            ...         study_types = set(r.get('studyType') for r in records if r.get('studyType'))
            ...         print(f"  Study types: {', '.join(sorted(study_types))}")
            ...         
            ...         # Count effect levels
            ...         effect_levels = {}
            ...         for rec in records:
            ...             level = rec.get('effectLevel', 'Unknown')
            ...             effect_levels[level] = effect_levels.get(level, 0) + 1
            ...         
            ...         print(f"  Effect levels:")
            ...         for level, count in sorted(effect_levels.items()):
            ...             print(f"    {level}: {count}")
            ...         
            ...         # Find LOAELs
            ...         loaels = [r for r in records if r.get('effectLevel') == 'LOAEL']
            ...         if loaels:
            ...             print(f"  LOAELs found: {len(loaels)}")
            ...             # Show lowest LOAEL
            ...             numeric_loaels = [r for r in loaels if r.get('dose')]
            ...             if numeric_loaels:
            ...                 lowest = min(numeric_loaels, key=lambda x: x['dose'])
            ...                 print(f"    Lowest: {lowest['dose']} {lowest.get('doseUnits', '')} - {lowest.get('effect', 'N/A')}")
            >>> 
            >>> # Analyze effects across chemicals
            >>> if batch_data:
            ...     # Get all unique organs affected
            ...     organs = set(r.get('organ') for r in batch_data if r.get('organ'))
            ...     print(f"\nUnique target organs across all chemicals: {len(organs)}")
            ...     
            ...     # Count records by study type
            ...     by_study_type = {}
            ...     for rec in batch_data:
            ...         st = rec.get('studyType', 'Unknown')
            ...         by_study_type[st] = by_study_type.get(st, 0) + 1
            ...     
            ...     print(f"\nRecords by study type:")
            ...     for st, count in sorted(by_study_type.items(), key=lambda x: x[1], reverse=True):
            ...         print(f"  {st}: {count}")
        
        Note:
            - Maximum 200 DTXSIDs per request
            - This endpoint returns comprehensive dose-response data
            - Results can be very large for chemicals with extensive testing
            - Batch requests are much more efficient than individual queries
            - Data includes both adverse effects and doses not eliciting effects
            - Effect levels help identify critical doses for risk assessment
            - Not all chemicals have ToxRefDB data
            - ToxRefDB focuses on standardized guideline studies
        """
        if not dtxsids:
            raise ValueError("dtxsids list cannot be empty")
        
        if len(dtxsids) > 200:
            raise ValueError(f"Maximum 200 DTXSIDs allowed, got {len(dtxsids)}")
        
        endpoint = "hazard/toxref/search/by-dtxsid/"
        return self._make_cached_request(
            endpoint, 
            json=dtxsids, 
            method='POST', 
            use_cache=use_cache
        )

