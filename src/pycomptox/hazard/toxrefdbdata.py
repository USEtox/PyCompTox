"""
ToxRefDB Data API client for EPA CompTox Dashboard.

This module provides access to extracted dose-treatment group-effect information 
and doses not eliciting effects from ToxRefDB. ToxRefDB data is also summarized 
in ToxValDB, including inferred NEL and NOAEL effect levels based on reported 
LEL and LOAEL values.

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient

class ToxRefDBData(CachedAPIClient):
    """
    Client for accessing ToxRefDB dose-treatment group-effect data from EPA CompTox Dashboard.
    
    This class provides access to all extracted dose-treatment group-effect information 
    as well as doses not eliciting effects from ToxRefDB for specified chemicals, studies, 
    or study types.
    
    ToxRefDB contains comprehensive toxicology study information that is also summarized 
    in ToxValDB, including:
    - Dose-response data for treatment groups
    - Effect levels (LEL, LOAEL)
    - No-effect levels (NEL, NOAEL - inferred)
    - Study-specific toxicological endpoints
    
    Data can be retrieved by:
    - Study type (e.g., DEV for developmental toxicity studies)
    - Study ID (individual study identifier)
    - DTXSID (chemical substance identifier)
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        use_cache (bool): Whether to use caching by default. Default is True.
    
    Example:
        >>> from pycomptox.hazard import ToxRefDBData
        >>> toxref = ToxRefDBData()
        >>> 
        >>> # Get data for developmental toxicity studies
        >>> dev_data = toxref.get_data_by_study_type("DEV")
        >>> print(f"Page {dev_data['page']} of {dev_data['totalPages']}")
        >>> print(f"Found {len(dev_data['content'])} records on this page")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0,
        **kwargs: Any
    ):
        """
        Initialize the ToxRefDBData client.
        
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
        page_number: int = 1,
        use_cache: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Get ToxRefDB data by study type with pagination.
        
        Retrieves dose-treatment group-effect information for all studies of a 
        specified type. Results are paginated to handle large datasets.
        
        Common study types include:
        - DEV: Developmental toxicity studies
        - REP: Reproductive toxicity studies
        - DNT: Developmental neurotoxicity studies
        - CHRON: Chronic toxicity studies
        - SUBCHRON: Subchronic toxicity studies
        - ACUTE: Acute toxicity studies
        - NEURO: Neurotoxicity studies
        
        Args:
            study_type: Study type code (e.g., 'DEV', 'REP', 'DNT')
            page_number: Page number for paginated results (default is 1)
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            Dictionary containing paginated results with fields:
                - data (list): List of data records for this page
                - pageNumber (int): Current page number
                - recordsOnPage (int): Number of records on this page
                - studyType (str): The requested study type
                
            Each record in 'data' contains fields such as:
                - dtxsid (str): Chemical identifier
                - studyId (int): Study identifier
                - studyType (str): Type of study
                - effectLevel (str): Effect level (LEL, LOAEL, etc.)
                - dose (float): Dose amount
                - doseUnits (str): Dose units
                - effect (str): Observed effect
                - target (str): Target organ/system
                - species (str): Test species
                - Notes: Exact fields vary by study
        
        Raises:
            ValueError: If study_type is not a valid non-empty string or page_number < 1
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxRefDBData
            >>> toxref = ToxRefDBData()
            >>> 
            >>> # Get developmental toxicity study data
            >>> dev_data = toxref.get_data_by_study_type("DEV", page_number=1)
            >>> 
            >>> print(f"Page {dev_data['pageNumber']}")
            >>> print(f"Records on this page: {dev_data['recordsOnPage']}")
            >>> print(f"Total records: {len(dev_data['data'])}")
            >>> 
            >>> # Process records
            >>> for record in dev_data['data'][:5]:  # First 5 records
            ...     print(f"\nStudy ID: {record.get('studyId')}")
            ...     print(f"Chemical: {record.get('dtxsid')}")
            ...     print(f"Effect: {record.get('effect', 'N/A')}")
            ...     if record.get('dose'):
            ...         print(f"Dose: {record['dose']} {record.get('doseUnits', '')}")
            >>> 
            >>> # Iterate through pages
            >>> page = 1
            >>> while True:
            ...     page_data = toxref.get_data_by_study_type("DEV", page_number=page)
            ...     # Process page_data['data']
            ...     if len(page_data['data']) < page_data['recordsOnPage']:
            ...         break  # Last page
            ...     page += 1
        
        Note:
            - Results are paginated; use page_number to navigate through pages
            - Check if data length is less than recordsOnPage to detect last page
            - Data includes both effect levels and no-effect levels
        """
        if not study_type or not isinstance(study_type, str):
            raise ValueError("study_type must be a non-empty string")
        
        if not isinstance(page_number, int) or page_number < 1:
            raise ValueError("page_number must be a positive integer")
        
        endpoint = f"hazard/toxref/data/search/by-study-type/{study_type}"
        params = {"page": page_number}
        
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)

    def get_data_by_study_id(
        self,
        study_id: int,
        use_cache: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Get ToxRefDB data by study ID.
        
        Retrieves all dose-treatment group-effect information for a specific study.
        Each study may have multiple dose groups and endpoints.
        
        Args:
            study_id: ToxRefDB study identifier (integer)
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing dose-effect data with fields such as:
                - dtxsid (str): Chemical identifier
                - studyId (int): Study identifier
                - studyType (str): Type of study
                - effectLevel (str): Effect level (LEL, LOAEL, NEL, NOAEL)
                - dose (float): Dose amount
                - doseUnits (str): Dose units (mg/kg/day, ppm, etc.)
                - effect (str): Observed effect description
                - target (str): Target organ or system
                - species (str): Test species (rat, mouse, etc.)
                - sex (str): Sex of test animals
                - exposureDuration (str): Duration of exposure
                - exposureRoute (str): Route of exposure
                - generation (str): Generation studied (for reproductive studies)
                - Notes: Exact fields vary by study type
        
        Raises:
            ValueError: If study_id is not a positive integer
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxRefDBData
            >>> toxref = ToxRefDBData()
            >>> 
            >>> # Get data for a specific study
            >>> study_data = toxref.get_data_by_study_id(63)
            >>> 
            >>> if study_data:
            ...     print(f"Found {len(study_data)} dose-effect records")
            ...     
            ...     # Get study metadata from first record
            ...     first = study_data[0]
            ...     print(f"\nStudy ID: {first.get('studyId')}")
            ...     print(f"Chemical: {first.get('dtxsid')}")
            ...     print(f"Study Type: {first.get('studyType')}")
            ...     print(f"Species: {first.get('species')}")
            ...     print(f"Exposure Route: {first.get('exposureRoute')}")
            ...     
            ...     # Group by effect level
            ...     by_level = {}
            ...     for record in study_data:
            ...         level = record.get('effectLevel', 'Unknown')
            ...         if level not in by_level:
            ...             by_level[level] = []
            ...         by_level[level].append(record)
            ...     
            ...     print(f"\nEffect levels found:")
            ...     for level, records in sorted(by_level.items()):
            ...         print(f"  {level}: {len(records)} record(s)")
            ...     
            ...     # Show LOAELs
            ...     if 'LOAEL' in by_level:
            ...         print(f"\nLOAEL values:")
            ...         for rec in by_level['LOAEL'][:3]:
            ...             print(f"  {rec.get('dose')} {rec.get('doseUnits')} - {rec.get('effect')}")
        
        Note:
            - A single study may have multiple dose groups and endpoints
            - Data includes both observed effects and no-effect doses
            - Effect levels may include LEL, LOAEL, NEL, NOAEL
        """
        if not isinstance(study_id, int) or study_id < 1:
            raise ValueError("study_id must be a positive integer")
        
        endpoint = f"hazard/toxref/data/search/by-study-id/{study_id}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_data_by_dtxsid(
        self,
        dtxsid: str,
        use_cache: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Get ToxRefDB data by DTXSID.
        
        Retrieves all dose-treatment group-effect information for a chemical across 
        all studies in ToxRefDB. This provides a comprehensive view of toxicological 
        data for a specific substance.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID1037806')
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing dose-effect data across all studies 
            for the chemical. Each entry includes fields such as:
                - dtxsid (str): Chemical identifier
                - studyId (int): Study identifier
                - studyType (str): Type of study
                - effectLevel (str): Effect level classification
                - dose (float): Dose amount
                - doseUnits (str): Dose units
                - effect (str): Observed effect
                - target (str): Target organ/system
                - species (str): Test species
                - sex (str): Sex of test animals
                - exposureDuration (str): Duration of exposure
                - exposureRoute (str): Route of exposure
                - reference (str): Study reference
                - Notes: Exact fields vary by study
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import ToxRefDBData
            >>> toxref = ToxRefDBData()
            >>> 
            >>> # Get all ToxRefDB data for a chemical
            >>> data = toxref.get_data_by_dtxsid("DTXSID1037806")
            >>> 
            >>> if data:
            ...     print(f"Found {len(data)} dose-effect records")
            ...     
            ...     # Group by study type
            ...     by_type = {}
            ...     for record in data:
            ...         stype = record.get('studyType', 'Unknown')
            ...         if stype not in by_type:
            ...             by_type[stype] = []
            ...         by_type[stype].append(record)
            ...     
            ...     print(f"\nStudy types represented:")
            ...     for stype, records in sorted(by_type.items()):
            ...         print(f"  {stype}: {len(records)} record(s)")
            ...     
            ...     # Find lowest LOAEL across all studies
            ...     loaels = [r for r in data if r.get('effectLevel') == 'LOAEL' and r.get('dose')]
            ...     if loaels:
            ...         # Group by units for comparison
            ...         by_units = {}
            ...         for rec in loaels:
            ...             units = rec.get('doseUnits', 'unknown')
            ...             dose = rec.get('dose')
            ...             if units not in by_units:
            ...                 by_units[units] = []
            ...             by_units[units].append(dose)
            ...         
            ...         print(f"\nLowest LOAELs by unit:")
            ...         for units, doses in by_units.items():
            ...             print(f"  {min(doses)} {units}")
            ...     
            ...     # List unique targets
            ...     targets = set(r.get('target') for r in data if r.get('target'))
            ...     print(f"\nTarget organs/systems: {', '.join(sorted(targets))}")
        
        Note:
            - Returns data from all available studies for the chemical
            - May include multiple study types and species
            - Useful for comprehensive hazard assessment
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"hazard/toxref/data/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)