"""
IRIS (Integrated Risk Information System) API client for EPA CompTox Dashboard.

This module provides access to EPA IRIS data including:
- Chemical health hazard characterizations
- Reference doses (RfD) and concentrations (RfC)
- Cancer assessments and slope factors
- Hazard identification information
- Dose-response assessments

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient


class IRIS(CachedAPIClient):
    """
    Client for accessing EPA IRIS (Integrated Risk Information System) data.
    
    Integrated Risk Information System (IRIS): EPA's IRIS Program identifies and 
    characterizes the health hazards of chemicals found in the environment. Each 
    IRIS assessment can cover:
    - A single chemical
    - A group of related chemicals
    - A complex mixture
    
    IRIS assessments provide:
    - Oral reference doses (RfD) for non-cancer effects
    - Inhalation reference concentrations (RfC) for non-cancer effects
    - Cancer slope factors and unit risks
    - Weight of evidence for carcinogenicity
    - Critical effect descriptions
    - Uncertainty and modifying factors
    
    IRIS assessments are an important source of toxicity information used by:
    - EPA programs and regional offices
    - State and local health agencies
    - Other federal agencies
    - International health organizations
    - Risk assessors and researchers
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        use_cache (bool): Whether to use caching by default. Default is True.
    
    Example:
        >>> from pycomptox.hazard import IRIS
        >>> iris = IRIS()
        >>> 
        >>> # Get IRIS assessment data for a chemical
        >>> data = iris.get_data_by_dtxsid("DTXSID7020182")
        >>> if data:
        ...     print(f"Found {len(data)} IRIS assessment(s)")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0,
        **kwargs: Any
    ):
        """
        Initialize the IRIS client.
        
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
        Get all IRIS assessment data by DTXSID.
        
        Retrieves comprehensive IRIS assessment information for a chemical identified 
        by its DSSTox Substance Identifier. IRIS assessments include detailed health 
        hazard characterizations and toxicity reference values used in risk assessment.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID7020182')
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing IRIS assessment data with fields such as:
                - dtxsid (str): Chemical identifier
                - casrn (str): CAS Registry Number
                - chemicalName (str): Chemical name
                - irisUrl (str): URL to full IRIS assessment
                - lastUpdated (str): Last assessment update date
                - assessmentStatus (str): Status of assessment
                
                Non-cancer hazard data:
                - oralRfD (float): Oral reference dose
                - oralRfDUnits (str): RfD units (typically mg/kg-day)
                - oralRfDCriticalEffect (str): Critical effect for RfD
                - oralRfDPOD (float): Point of departure
                - oralRfDUF (int): Uncertainty factor
                - inhalationRfC (float): Inhalation reference concentration
                - inhalationRfCUnits (str): RfC units (typically mg/m³)
                - inhalationRfCCriticalEffect (str): Critical effect for RfC
                - inhalationRfCPOD (float): Point of departure
                - inhalationRfCUF (int): Uncertainty factor
                
                Cancer hazard data:
                - cancerWeightOfEvidence (str): Weight of evidence classification
                - oralSlopeFactor (float): Oral cancer slope factor
                - oralSlopeFactorUnits (str): Slope factor units
                - inhalationUnitRisk (float): Inhalation unit risk
                - inhalationUnitRiskUnits (str): Unit risk units
                
                - Notes: Exact fields vary by assessment
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import IRIS
            >>> iris = IRIS()
            >>> 
            >>> # Get IRIS data for formaldehyde
            >>> data = iris.get_data_by_dtxsid("DTXSID7020182")
            >>> 
            >>> if data:
            ...     print(f"Found {len(data)} IRIS assessment(s)")
            ...     
            ...     for assessment in data:
            ...         print(f"\nChemical: {assessment.get('chemicalName', 'N/A')}")
            ...         print(f"CAS: {assessment.get('casrn', 'N/A')}")
            ...         print(f"Status: {assessment.get('assessmentStatus', 'N/A')}")
            ...         
            ...         # Non-cancer oral hazard
            ...         if assessment.get('oralRfD'):
            ...             print(f"\nOral RfD: {assessment['oralRfD']} {assessment.get('oralRfDUnits', '')}")
            ...             if assessment.get('oralRfDCriticalEffect'):
            ...                 print(f"  Critical Effect: {assessment['oralRfDCriticalEffect']}")
            ...             if assessment.get('oralRfDUF'):
            ...                 print(f"  Uncertainty Factor: {assessment['oralRfDUF']}")
            ...         
            ...         # Non-cancer inhalation hazard
            ...         if assessment.get('inhalationRfC'):
            ...             print(f"\nInhalation RfC: {assessment['inhalationRfC']} {assessment.get('inhalationRfCUnits', '')}")
            ...             if assessment.get('inhalationRfCCriticalEffect'):
            ...                 print(f"  Critical Effect: {assessment['inhalationRfCCriticalEffect']}")
            ...         
            ...         # Cancer hazard
            ...         if assessment.get('cancerWeightOfEvidence'):
            ...             print(f"\nCancer Weight of Evidence: {assessment['cancerWeightOfEvidence']}")
            ...         
            ...         if assessment.get('oralSlopeFactor'):
            ...             print(f"Oral Slope Factor: {assessment['oralSlopeFactor']} {assessment.get('oralSlopeFactorUnits', '')}")
            ...         
            ...         if assessment.get('inhalationUnitRisk'):
            ...             print(f"Inhalation Unit Risk: {assessment['inhalationUnitRisk']} {assessment.get('inhalationUnitRiskUnits', '')}")
            ...         
            ...         # Link to full assessment
            ...         if assessment.get('irisUrl'):
            ...             print(f"\nFull Assessment: {assessment['irisUrl']}")
            ...         
            ...         if assessment.get('lastUpdated'):
            ...             print(f"Last Updated: {assessment['lastUpdated']}")
            >>> else:
            ...     print("No IRIS assessment available for this chemical")
            >>> 
            >>> # Example: Check for cancer classification
            >>> if data:
            ...     for assessment in data:
            ...         woe = assessment.get('cancerWeightOfEvidence', '')
            ...         if 'carcinogenic' in woe.lower():
            ...             print(f"WARNING: {assessment.get('chemicalName')} classified as carcinogenic")
        
        Note:
            - Only chemicals with completed IRIS assessments have data
            - IRIS assessments undergo rigorous scientific review
            - Assessments are periodically updated as new data becomes available
            - Not all chemicals have both oral and inhalation values
            - Not all chemicals have cancer assessments
            - IRIS values are widely used in regulatory risk assessment
            - Full assessments with supporting documentation available at irisUrl
            - Assessment status indicates stage: draft, final, under review, etc.
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"hazard/iris/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)
