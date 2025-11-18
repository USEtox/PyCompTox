"""
HAWC (Health Assessment Workspace Collaborative) API client for EPA CompTox Dashboard.

This module provides access to EPA HAWC links and data including:
- Links between CompTox Dashboard and HAWC assessments
- Health and environmental risk assessment information
- Study evaluation data
- Assessment transparency and data usability information

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient

class HAWC(CachedAPIClient):
    """
    Client for accessing EPA HAWC (Health Assessment Workspace Collaborative) data.
    
    EPA Health Assessment Workspace Collaborative (HAWC) is an interactive, 
    expert-driven, content management system for EPA health and environmental risk 
    assessment programs that is intended to promote:
    - Transparency in assessment processes
    - Data usability and accessibility
    - Understanding of data and decisions supporting assessments
    
    EPA HAWC is an application that allows the data and decisions supporting an 
    assessment to be evaluated and managed in modules (e.g., study evaluation, 
    summary study data) that can then be publicly accessed online.
    
    This class provides methods for retrieving links between chemicals in the 
    CompTox Chemicals Dashboard and their corresponding HAWC assessments.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        use_cache (bool): Whether to use caching by default. Default is True.
    
    Example:
        >>> from pycomptox.hazard import HAWC
        >>> hawc = HAWC()
        >>> 
        >>> # Get HAWC assessment links for a chemical
        >>> links = hawc.get_ccd_hawc_link_mapper_by_dtxsid("DTXSID7020182")
        >>> if links:
        ...     print(f"Found {len(links)} HAWC assessment(s)")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0,
        **kwargs: Any
    ):
        """
        Initialize the HAWC client.
        
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

    def get_ccd_hawc_link_mapper_by_dtxsid(self, dtxsid: str, 
                                   use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get CompTox Dashboard - EPA HAWC link mapper by DTXSID.
        
        Retrieves links between a chemical in the CompTox Chemicals Dashboard (CCD) 
        and its corresponding assessments in the EPA Health Assessment Workspace 
        Collaborative (HAWC) platform. This provides access to detailed health and 
        environmental risk assessment information for the chemical.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID7020182')
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing HAWC link information with fields such as:
                - dtxsid (str): Chemical identifier
                - hawcUrl (str): URL to the HAWC assessment
                - hawcAssessmentId (int): HAWC assessment identifier
                - assessmentName (str): Name of the assessment
                - assessmentType (str): Type of assessment
                - program (str): EPA program conducting the assessment
                - status (str): Assessment status
                - lastUpdated (str): Last update date
                - description (str): Assessment description
                - Notes: Exact fields may vary
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox.hazard import HAWC
            >>> hawc = HAWC()
            >>> 
            >>> # Get HAWC links for formaldehyde
            >>> links = hawc.get_ccd_hawc_link_mapper_by_dtxsid("DTXSID7020182")
            >>> 
            >>> if links:
            ...     print(f"Found {len(links)} HAWC assessment(s) for this chemical")
            ...     
            ...     for link in links:
            ...         print(f"\nAssessment: {link.get('assessmentName', 'N/A')}")
            ...         print(f"Type: {link.get('assessmentType', 'N/A')}")
            ...         print(f"Program: {link.get('program', 'N/A')}")
            ...         print(f"Status: {link.get('status', 'N/A')}")
            ...         
            ...         if link.get('hawcUrl'):
            ...             print(f"HAWC URL: {link['hawcUrl']}")
            ...         
            ...         if link.get('description'):
            ...             print(f"Description: {link['description'][:100]}...")
            ...         
            ...         # Access the HAWC assessment
            ...         if link.get('hawcAssessmentId'):
            ...             print(f"Assessment ID: {link['hawcAssessmentId']}")
            >>> else:
            ...     print("No HAWC assessments found for this chemical")
            >>> 
            >>> # Example: Filter by assessment type
            >>> if links:
            ...     iris_assessments = [l for l in links 
            ...                        if 'IRIS' in l.get('program', '')]
            ...     if iris_assessments:
            ...         print(f"\nIRIS assessments: {len(iris_assessments)}")
        
        Note:
            - Not all chemicals have HAWC assessments
            - HAWC assessments are created for chemicals undergoing EPA review
            - Links provide direct access to detailed assessment data
            - HAWC platform allows viewing study evaluation and summary data
            - Assessments may be in various stages (in progress, completed, etc.)
            - Multiple assessments may exist for the same chemical from different programs
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"hazard/hawc/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)