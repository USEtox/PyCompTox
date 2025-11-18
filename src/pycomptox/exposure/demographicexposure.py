"""
Demographic Exposure API client for EPA CompTox Dashboard.

This module provides access to demographic-specific exposure prediction data including:
- SEEM (Systematic Empirical Evaluation of Models) predictions by demographic
- Age-specific exposure estimates
- Population subgroup predictions
- Batch operations for multiple chemicals

Author: PyCompTox Contributors
License: MIT
"""

import time
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urljoin

from ..base import CachedAPIClient


class DemographicExposure(CachedAPIClient):
    """
    Client for accessing demographic-specific exposure prediction data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving demographic-specific estimates of average
    (geometric mean) exposure rate (mg/kg bodyweight/day) for U.S. population subgroups.
    
    Predictions include:
    - Median estimates (50% confidence)
    - Upper 95th percentile estimates (95% confidence)
    - Demographic-specific predictions (age groups, etc.)
    
    Total population predictions are based on consensus exposure model predictions and
    the similarity of compounds to chemicals monitored by NHANES. The demographic-specific
    predictions use a heuristic model described in the 2014 publication "High Throughput
    Heuristics for Prioritizing Human Exposure to Environmental Chemicals".
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float, **kwargs): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import DemographicExposure
        >>> demo_exp = DemographicExposure()
        >>> 
        >>> # Get demographic exposure predictions for a chemical
        >>> data = demo_exp.prediction_SEEMs_data_by_dtxsid("DTXSID0020232")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0
    , **kwargs):
        """
        Initialize the DemographicExposure client.
        
        Args:
            api_key: CompTox API key (optional, will be loaded from config if not provided)
            base_url: Base URL for the CompTox API
            time_delay_between_calls: Delay between API calls in seconds
        
        Raises:
            ValueError: If no API key is provided or found in configuration
        """
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            time_delay_between_calls=time_delay_between_calls,
            **kwargs
        )
    
    def prediction_SEEMs_data_by_dtxsid(self, dtxsid: str, projection: str = "ccd-demographic", use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get demographic-specific SEEM exposure predictions for a chemical.
        
        Retrieves Systematic Empirical Evaluation of Models (SEEM) exposure predictions
        broken down by demographic groups for a specific chemical identified by its
        DSSTox Substance Identifier (DTXSID). Returns estimates of average (geometric mean)
        exposure rate (mg/kg bodyweight/day) for different U.S. population subgroups.
        
        The demographic-specific predictions use a heuristic model described in the 2014
        publication "High Throughput Heuristics for Prioritizing Human Exposure to
        Environmental Chemicals".
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0020232')
            projection: Optional projection specification. Default is 'ccd-demographic'.
        
        Returns:
            List of dictionaries containing demographic SEEM prediction data including:
            - Median exposure estimates by demographic group
            - Upper 95th percentile estimates by demographic group
            - Age-specific predictions
            - Population subgroup breakdowns
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> demo_exp = DemographicExposure()
            >>> data = demo_exp.prediction_SEEMs_data_by_dtxsid("DTXSID0020232")
            >>> for pred in data:
            ...     print(f"{pred.get('demographic')}: {pred.get('medianEstimate')} mg/kg/day")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/seem/demographic/search/by-dtxsid/{dtxsid}"
        params = {}
        if projection:
            params["projection"] = projection
        
        return self._make_cached_request(endpoint, params=params if params else None, use_cache=use_cache)

    def prediction_SEEMs_data_by_dtxsid_batch(self, dtxsid_list: List[str], use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get demographic SEEM exposure predictions for multiple chemicals in a single request.
        
        Retrieves demographic-specific SEEM exposure predictions for multiple chemicals
        at once using a batch API call. This is more efficient than making individual
        requests for each chemical when working with multiple DTXSIDs.
        
        Args:
            dtxsid_list: List of DSSTox Substance Identifiers
        
        Returns:
            List of dictionaries containing demographic SEEM prediction data for all
            requested chemicals. Each entry includes the DTXSID and associated
            demographic-specific exposure predictions (median and 95th percentile
            estimates by population subgroup).
        
        Raises:
            ValueError: If dtxsid_list is not a valid non-empty list
        
        Example:
            >>> demo_exp = DemographicExposure()
            >>> dtxsids = ["DTXSID0020232", "DTXSID0020267"]
            >>> batch_data = demo_exp.prediction_SEEMs_data_by_dtxsid_batch(dtxsids)
            >>> for result in batch_data:
            ...     print(f"{result.get('dtxsid')}: {result.get('demographic')} - {result.get('medianEstimate')}")
        """
        if not dtxsid_list or not isinstance(dtxsid_list, list) or len(dtxsid_list) == 0:
            raise ValueError("dtxsid_list must be a non-empty list of strings")
        
        if not all(isinstance(dtxsid, str) for dtxsid in dtxsid_list):
            raise ValueError("All elements in dtxsid_list must be strings")
        
        endpoint = "exposure/seem/demographic/search/by-dtxsid/"
        return self._make_request("POST", endpoint, json_data=dtxsid_list)



