"""
ADME-IVIVE API client for EPA CompTox Dashboard.

This module provides access to toxicokinetics data in humans, including:
- In vitro measured values
- In vivo measured values
- In silico predictions
- Computed values from mathematical models

Data sources include httk R package and CvTdb (Concentration vs. Time database).

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient

class ADMEIVIVE(CachedAPIClient):
    """
    Client for accessing ADME-IVIVE (Absorption, Distribution, Metabolism, Excretion - 
    In Vitro to In Vivo Extrapolation) toxicokinetics data from EPA CompTox Dashboard.
    
    This class provides access to toxicokinetics data describing how chemicals behave 
    in the human body. Data values are:
    
    1. **Measured** - either in vitro or in vivo
    2. **Predicted** - from chemical properties using in silico tools
    3. **Computed** - with mathematical models simulating toxicokinetics
    
    Key Parameters:
    - Intrinsic hepatic clearance
    - Fraction unbound in plasma
    - Volume of distribution
    - PK half-life
    - Steady-state plasma concentration
    
    Data Sources:
    - **httk R package**: In vitro measured values (https://CRAN.R-project.org/package=httk)
    - **CvTdb**: In vivo concentration vs. time data (https://doi.org/10.1038/s41597-020-0455-1)
    - **invivoPKfit**: In vivo estimates (https://github.com/USEPA/CompTox-ExpoCast-invivoPKfit)
    
    Note: Some measured values may be assumed from surrogate species data. The Data 
    Source Species column identifies the species source for measured data. These 
    assumed measured values are used in calculations to estimate other outcomes.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        use_cache (bool): Whether to use caching by default. Default is True.
    
    Example:
        >>> from pycomptox.hazard import ADMEIVIVE
        >>> adme = ADMEIVIVE()
        >>> 
        >>> # Get ADME-IVIVE data for bisphenol A
        >>> data = adme.get_all_data_by_dtxsid_ccd_projection("DTXSID7020182")
        >>> 
        >>> if data:
        ...     for record in data:
        ...         param = record.get('parameter', 'Unknown')
        ...         value = record.get('value', 'N/A')
        ...         units = record.get('units', '')
        ...         print(f"{param}: {value} {units}")
    """
    
    def get_all_data_by_dtxsid_ccd_projection(
        self, 
        dtxsid: str, 
        projection: Optional[str] = None,
        use_cache: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Get ADME-IVIVE toxicokinetics data by DTXSID.
        
        Retrieves all ADME-IVIVE (Absorption, Distribution, Metabolism, Excretion - 
        In Vitro to In Vivo Extrapolation) data for a chemical. Optionally use 
        projection for CompTox Dashboard-specific formatting.
        
        The data includes toxicokinetic parameters such as:
        - Intrinsic hepatic clearance (CLint)
        - Fraction unbound in plasma (Fup)
        - Volume of distribution (Vd)
        - Pharmacokinetic half-life (t½)
        - Steady-state plasma concentration (Css)
        - Oral bioavailability
        - Renal clearance
        - Blood:plasma ratio
        
        Data types include:
        - **In vitro measured**: Direct measurements from in vitro assays
        - **In vivo measured**: Derived from concentration-time data (CvTdb)
        - **In silico predicted**: Predictions from chemical properties
        - **Computed**: Calculated using httk or invivoPKfit models
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID7020182')
            projection: Optional projection name. Use 'ccd-adme-data' for 
                CompTox Dashboard ADME-IVIVE page format. If None, returns 
                default ADME-IVIVE data.
            use_cache: Whether to use cache for this request. If None, uses
                the instance default setting.
        
        Returns:
            List of dictionaries containing ADME-IVIVE data with fields such as:
                - dtxsid (str): Chemical identifier
                - parameter (str): ADME parameter name
                - value (float): Parameter value
                - units (str): Units of measurement
                - dataType (str): Type of data (measured/predicted/computed)
                - source (str): Data source (httk, CvTdb, in silico tool)
                - species (str): Species for measured data
                - method (str): Measurement or prediction method
                - reference (str): Literature reference
                - confidence (str): Confidence level or quality indicator
                - Notes: Exact fields vary by projection
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox.hazard import ADMEIVIVE
            >>> adme = ADMEIVIVE()
            >>> 
            >>> # Get ADME-IVIVE data for bisphenol A
            >>> data = adme.get_all_data_by_dtxsid_ccd_projection("DTXSID7020182")
            >>> 
            >>> if data:
            ...     print(f"Found {len(data)} ADME-IVIVE parameters")
            ...     
            ...     # Group by data type
            ...     by_type = {}
            ...     for record in data:
            ...         dtype = record.get('dataType', 'Unknown')
            ...         if dtype not in by_type:
            ...             by_type[dtype] = []
            ...         by_type[dtype].append(record)
            ...     
            ...     print(f"\nData types available:")
            ...     for dtype, records in sorted(by_type.items()):
            ...         print(f"  {dtype}: {len(records)} parameter(s)")
            ...     
            ...     # Show key parameters
            ...     print(f"\nKey toxicokinetic parameters:")
            ...     key_params = ['Clint', 'Fup', 'Vd', 't1/2', 'Css']
            ...     for record in data:
            ...         param = record.get('parameter', '')
            ...         if any(kp in param for kp in key_params):
            ...             value = record.get('value', 'N/A')
            ...             units = record.get('units', '')
            ...             source = record.get('source', 'Unknown')
            ...             print(f"  {param}: {value} {units} ({source})")
            >>> 
            >>> # Get with CompTox Dashboard projection
            >>> ccd_data = adme.get_all_data_by_dtxsid_ccd_projection(
            ...     "DTXSID7020182", 
            ...     projection="ccd-adme-data"
            ... )
            >>> 
            >>> # Compare in vitro vs in vivo data
            >>> if data:
            ...     in_vitro = [r for r in data if 'in vitro' in str(r.get('dataType', '')).lower()]
            ...     in_vivo = [r for r in data if 'in vivo' in str(r.get('dataType', '')).lower()]
            ...     print(f"\nIn vitro parameters: {len(in_vitro)}")
            ...     print(f"In vivo parameters: {len(in_vivo)}")
        
        Note:
            - Data may include measured, predicted, and computed values
            - Some measured values may be from surrogate species
            - Check 'species' field to identify data source species
            - Computed values are derived using httk or invivoPKfit R packages
            - Use projection='ccd-adme-data' for dashboard-formatted data
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"hazard/adme-ivive/search/by-dtxsid/{dtxsid}"
        params = {"projection": projection} if projection else None
        
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)
