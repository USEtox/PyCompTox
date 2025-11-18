"""
PPRTV (Provisional Peer-Reviewed Toxicity Values) API client for EPA CompTox Dashboard.

This module provides access to PPRTV hazard data including:
- Toxicity reference values (RfC, RfD)
- Weight of evidence assessments
- Links to IRIS and PPRTV assessments

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient


class PPRTV(CachedAPIClient):
    """
    Client for accessing Provisional Peer-Reviewed Toxicity Values (PPRTV) data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving PPRTV hazard characterization data, including
    reference concentrations (RfC), reference doses (RfD), and weight of evidence assessments.
    
    PPRTV provides toxicity values for chemicals that do not have EPA IRIS assessments.
    These values support human health risk assessments and are developed following peer review.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        use_cache (bool): Whether to use caching by default. Default is True.
    
    Example:
        >>> from pycomptox.hazard import PPRTV
        >>> pprtv = PPRTV()
        >>> 
        >>> # Get PPRTV data for a chemical
        >>> data = pprtv.get_all_pprtv_chemical_by_dtxsid("DTXSID7020182")
        >>> if data:
        ...     print(f"RfC: {data[0].get('rfcValue')}")
        ...     print(f"RfD: {data[0].get('rfdValue')}")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0,
        **kwargs: Any
    ):
        """
        Initialize the PPRTV client.
        
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

    def get_all_pprtv_chemical_by_dtxsid(
        self,
        dtxsid: str,
        use_cache: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all PPRTV chemical data by DTXSID.
        
        Retrieves Provisional Peer-Reviewed Toxicity Values (PPRTV) hazard data for
        a specific chemical identified by its DSSTox Substance Identifier (DTXSID).
        
        PPRTV data includes reference concentrations (RfC) for inhalation exposure,
        reference doses (RfD) for oral exposure, weight of evidence classifications,
        and links to full assessments.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID7020182')
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing PPRTV data with fields:
                - id (int): Record identifier
                - dtxsid (str): DSSTox Substance Identifier
                - pprtvSubstanceId (int): PPRTV substance identifier
                - name (str): Chemical name
                - casrn (str): CAS Registry Number
                - lastRevision (int): Last revision date/number
                - pprtvAssessment (str): Link to PPRTV assessment
                - irisLink (str): Link to IRIS assessment (if available)
                - rfcValue (str): Reference Concentration for inhalation (mg/m³)
                - rfdValue (str): Reference Dose for oral exposure (mg/kg-day)
                - woe (str): Weight of Evidence classification
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import PPRTV
            >>> pprtv = PPRTV()
            >>> 
            >>> # Get PPRTV data for benzene
            >>> data = pprtv.get_all_pprtv_chemical_by_dtxsid("DTXSID7020182")
            >>> 
            >>> if data:
            ...     for record in data:
            ...         print(f"Chemical: {record['name']}")
            ...         print(f"CAS: {record['casrn']}")
            ...         if record.get('rfcValue'):
            ...             print(f"RfC (inhalation): {record['rfcValue']} mg/m³")
            ...         if record.get('rfdValue'):
            ...             print(f"RfD (oral): {record['rfdValue']} mg/kg-day")
            ...         if record.get('woe'):
            ...             print(f"Weight of Evidence: {record['woe']}")
            ...         if record.get('pprtvAssessment'):
            ...             print(f"Assessment: {record['pprtvAssessment']}")
            >>> else:
            ...     print("No PPRTV data available for this chemical")
        
        Note:
            - Not all chemicals have PPRTV assessments
            - RfC values are for inhalation exposure (mg/m³)
            - RfD values are for oral exposure (mg/kg-day)
            - Weight of Evidence (WoE) classifications indicate the strength
              of evidence for carcinogenicity or other health effects
            - PPRTV assessments are provisional and may be superseded by
              IRIS assessments
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"hazard/pprtv/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)
