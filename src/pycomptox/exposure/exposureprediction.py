"""
Exposure Prediction API client for EPA CompTox Dashboard.

This module provides access to exposure prediction data including:
- SEEM (Systematic Empirical Evaluation of Models) predictions
- General population exposure estimates
- Demographic-specific predictions
- Batch operations for multiple chemicals

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient


class ExposurePrediction(CachedAPIClient):
    """
    Client for accessing exposure prediction data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving estimated exposure rates (mg/kg bodyweight/day)
    for the U.S. population. Predictions include:
    - Median estimates (50% confidence)
    - Upper 95th percentile estimates (95% confidence)
    
    Total population predictions are based on consensus exposure model predictions and
    the similarity of compounds to chemicals monitored by NHANES. The method was described
    in the 2018 publication: "Consensus Modeling of Median Chemical Intake for the U.S.
    Population Based on Predictions of Exposure Pathways".
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float, **kwargs): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import ExposurePrediction
        >>> exp_pred = ExposurePrediction()
        >>> 
        >>> # Get exposure predictions for a chemical
        >>> data = exp_pred.get_general_seem_prediction_by_dtxsid("DTXSID0020232")
    """
    
    def get_general_seem_prediction_by_dtxsid(
            self, dtxsid: str, 
            projection: str = "ccd-general"
            , use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get general SEEM exposure predictions for a chemical.
        
        Retrieves Systematic Empirical Evaluation of Models (SEEM) exposure predictions
        for a specific chemical identified by its DSSTox Substance Identifier (DTXSID).
        Returns estimates of average (geometric mean) exposure rate (mg/kg bodyweight/day)
        for the U.S. population.
        
        Predictions include:
        - Median estimate (50% confidence)
        - Upper 95th percentile estimate (95% confidence)
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID0020232')
            projection: Optional projection specification. Default is 'ccd-general'.
        
        Returns:
            List of dictionaries containing SEEM prediction data including:
            - Median exposure estimates
            - Upper 95th percentile estimates
            - Exposure pathways
            - Model predictions and confidence intervals
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> exp_pred = ExposurePrediction()
            >>> data = exp_pred.get_general_seem_prediction_by_dtxsid("DTXSID0020232")
            >>> for pred in data:
            ...     print(f"Median: {pred.get('medianEstimate')} mg/kg/day")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/seem/general/search/by-dtxsid/{dtxsid}"
        params = {}
        if projection:
            params["projection"] = projection
        
        return self._make_cached_request(endpoint, params=params if params else None, use_cache=use_cache)

    def get_general_seem_prediction_by_dtxsid_batch(
            self, dtxsid_list: List[str], use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get general SEEM exposure predictions for multiple chemicals in a single request.
        
        Retrieves SEEM exposure predictions for multiple chemicals at once using a batch
        API call. This is more efficient than making individual requests for each chemical
        when working with multiple DTXSIDs.
        
        Args:
            dtxsid_list: List of DSSTox Substance Identifiers
        
        Returns:
            List of dictionaries containing SEEM prediction data for all requested
            chemicals. Each entry includes the DTXSID and associated exposure
            predictions (median and 95th percentile estimates).
        
        Raises:
            ValueError: If dtxsid_list is not a valid non-empty list
        
        Example:
            >>> exp_pred = ExposurePrediction()
            >>> dtxsids = ["DTXSID0020232", "DTXSID0020245"]
            >>> batch_data = exp_pred.get_general_seem_prediction_by_dtxsid_batch(dtxsids)
            >>> for result in batch_data:
            ...     print(f"{result.get('dtxsid')}: {result.get('medianEstimate')} mg/kg/day")
        """
        if not dtxsid_list or not isinstance(dtxsid_list, list) or len(dtxsid_list) == 0:
            raise ValueError("dtxsid_list must be a non-empty list of strings")
        
        if not all(isinstance(dtxsid, str) for dtxsid in dtxsid_list):
            raise ValueError("All elements in dtxsid_list must be strings")
        
        endpoint = "exposure/seem/general/search/by-dtxsid/"
        return self._make_cached_request(
            endpoint, method='POST', json=dtxsid_list, use_cache=use_cache
        )
