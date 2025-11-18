"""
ToxValDB (Toxicity Values Database) API client for EPA CompTox Dashboard.

This module provides access to ToxValDB, a comprehensive compilation of toxicity 
information from worldwide sources including:
- LOAELs (Lowest Observed Adverse Effect Levels)
- NOAELs (No Observed Adverse Effect Levels)
- BMDs (Benchmark Doses)
- LD50s (Lethal Dose 50%)
- RfDs (Reference Doses)
- RfCs (Reference Concentrations)
- And other quantitative toxicity values

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient

class ToxValDB(CachedAPIClient):
    """
    Client for accessing ToxValDB (Toxicity Values Database) from EPA CompTox Dashboard.
    
    The Toxicity Values Database (ToxValDB) is a compilation of toxicity information 
    from world-wide sites, databases, and sources, which can save the user time by 
    providing information in one location. The data are largely limited to summary 
    values from individual studies or chemical-level assessments, and is focused 
    on quantitative values such as:
    
    - LOAELs (Lowest Observed Adverse Effect Levels)
    - NOAELs (No Observed Adverse Effect Levels)
    - BMDs (Benchmark Doses)
    - LD50s (Lethal Dose 50%)
    - RfDs (Reference Doses)
    - RfCs (Reference Concentrations)
    - Cancer slope factors
    - Inhalation unit risks
    
    Important Notes:
    - Users must apply judgment in use of the information
    - Consult the original scientific paper or data source when possible
    - Understanding the context of the data is essential
    - The ToxValDB SQL download is available at:
      https://www.epa.gov/comptox-tools/downloadable-computational-toxicology-data#AT
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        use_cache (bool): Whether to use caching by default. Default is True.
    
    Example:
        >>> from pycomptox.hazard import ToxValDB
        >>> toxval = ToxValDB()
        >>> 
        >>> # Get all toxicity values for a chemical
        >>> data = toxval.get_data_by_dtxsid("DTXSID0021125")
        >>> if data:
        ...     print(f"Found {len(data)} toxicity values")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0,
        **kwargs: Any
    ):
        """
        Initialize the ToxValDB client.
        
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
        Get all ToxValDB toxicity data by DTXSID.
        
        Retrieves all toxicity values compiled in ToxValDB for a specific chemical 
        identified by its DSSTox Substance Identifier. This includes quantitative 
        toxicity values from multiple studies, sources, and endpoints.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0021125')
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing toxicity data with fields such as:
                - dtxsid (str): Chemical identifier
                - toxvalType (str): Type of toxicity value (NOAEL, LOAEL, LD50, etc.)
                - toxvalNumeric (float): Numeric toxicity value
                - toxvalUnits (str): Units of the value
                - studyType (str): Type of study
                - studyDuration (str): Duration of study
                - species (str): Test species
                - strain (str): Animal strain
                - sex (str): Sex of test subjects
                - exposureRoute (str): Route of exposure
                - exposureMethod (str): Method of exposure
                - criticalEffect (str): Critical effect observed
                - source (str): Original data source
                - sourceUrl (str): URL to source
                - year (int): Year of study/assessment
                - riskAssessmentClass (str): Risk assessment classification
                - Notes: Exact fields vary by record type and source
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxValDB
            >>> toxval = ToxValDB()
            >>> 
            >>> # Get all toxicity data for benzene
            >>> data = toxval.get_data_by_dtxsid("DTXSID0021125")
            >>> 
            >>> if data:
            ...     print(f"Found {len(data)} toxicity records")
            ...     
            ...     # Group by toxicity value type
            ...     by_type = {}
            ...     for record in data:
            ...         tox_type = record.get('toxvalType', 'Unknown')
            ...         if tox_type not in by_type:
            ...             by_type[tox_type] = []
            ...         by_type[tox_type].append(record)
            ...     
            ...     # Display summary by type
            ...     for tox_type, records in sorted(by_type.items()):
            ...         print(f"\n{tox_type}: {len(records)} record(s)")
            ...         
            ...         # Show first few values
            ...         for rec in records[:3]:
            ...             value = rec.get('toxvalNumeric')
            ...             units = rec.get('toxvalUnits', '')
            ...             species = rec.get('species', '')
            ...             route = rec.get('exposureRoute', '')
            ...             print(f"  {value} {units} ({species}, {route})")
            ...     
            ...     # Find reference doses
            ...     rfds = [r for r in data if 'RfD' in r.get('toxvalType', '')]
            ...     if rfds:
            ...         print(f"\nReference Doses (RfD): {len(rfds)}")
            ...         for rfd in rfds:
            ...             print(f"  {rfd.get('toxvalNumeric')} {rfd.get('toxvalUnits')}")
            ...             print(f"  Source: {rfd.get('source')}")
            ...             if rfd.get('criticalEffect'):
            ...                 print(f"  Critical Effect: {rfd['criticalEffect']}")
            >>> else:
            ...     print("No ToxValDB data available for this chemical")
        
        Note:
            - Data comes from multiple international sources
            - Multiple values of the same type may exist from different studies
            - Always check study context (species, route, duration, etc.)
            - Consult original sources for complete study details
            - Values span various endpoints and assessment types
            - Quality and completeness vary by source
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"hazard/toxval/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_data_by_dtxsid_batch(self, dtxsids: List[str], 
                                use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get all ToxValDB data for multiple chemicals in a single request.
        
        Batch retrieval of toxicity values from ToxValDB for up to 200 chemicals.
        More efficient than making individual requests when querying multiple chemicals.
        
        Args:
            dtxsids: List of DSSTox Substance Identifiers (max 200)
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing toxicity data for all requested 
            chemicals. Each entry includes similar fields as get_data_by_dtxsid().
        
        Raises:
            ValueError: If dtxsids list is empty or contains more than 200 entries
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxValDB
            >>> toxval = ToxValDB()
            >>> 
            >>> # Get toxicity data for multiple chemicals
            >>> dtxsids = ["DTXSID0021125", "DTXSID7020182", "DTXSID0020032"]
            >>> batch_data = toxval.get_data_by_dtxsid_batch(dtxsids)
            >>> 
            >>> # Group by chemical
            >>> by_chemical = {}
            >>> for record in batch_data:
            ...     dtxsid = record['dtxsid']
            ...     if dtxsid not in by_chemical:
            ...         by_chemical[dtxsid] = []
            ...     by_chemical[dtxsid].append(record)
            >>> 
            >>> # Display summary for each chemical
            >>> for dtxsid, records in by_chemical.items():
            ...     print(f"\n{dtxsid}: {len(records)} toxicity value(s)")
            ...     
            ...     # Get unique toxicity value types
            ...     types = set(r.get('toxvalType', 'Unknown') for r in records)
            ...     print(f"  Value types: {', '.join(sorted(types)[:5])}")
            ...     
            ...     # Find acute toxicity values
            ...     ld50s = [r for r in records if 'LD50' in r.get('toxvalType', '')]
            ...     if ld50s:
            ...         print(f"  LD50 values: {len(ld50s)}")
            ...         # Show lowest LD50 (most toxic)
            ...         numeric_ld50s = [r for r in ld50s if r.get('toxvalNumeric')]
            ...         if numeric_ld50s:
            ...             lowest = min(numeric_ld50s, key=lambda x: x['toxvalNumeric'])
            ...             print(f"    Lowest: {lowest['toxvalNumeric']} "
            ...                   f"{lowest.get('toxvalUnits', '')} "
            ...                   f"({lowest.get('species', '')})")
            ...     
            ...     # Find chronic reference values
            ...     refs = [r for r in records if 'RfD' in r.get('toxvalType', '') 
            ...             or 'RfC' in r.get('toxvalType', '')]
            ...     if refs:
            ...         print(f"  Reference values: {len(refs)}")
        
        Note:
            - Maximum 200 DTXSIDs per request
            - Results include all available toxicity values for each chemical
            - Batch requests are more efficient than individual queries
            - Useful for comparative toxicity screening
            - Total number of records can be very large for chemicals with extensive data
        """
        if not dtxsids:
            raise ValueError("dtxsids list cannot be empty")
        
        if len(dtxsids) > 200:
            raise ValueError(f"Maximum 200 DTXSIDs allowed, got {len(dtxsids)}")
        
        endpoint = "hazard/toxval/search/by-dtxsid/"
        return self._make_cached_request(
            endpoint, 
            json=dtxsids, 
            method='POST', 
            use_cache=use_cache
        )