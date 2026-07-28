"""
Bioactivity Model API client for EPA CompTox Dashboard.

This module provides access to ToxCast computational models including:
- Model predictions by chemical DTXSID
- Model predictions filtered by specific model types (e.g., CERAPP, CoMPARA)

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient


class BioactivityModel(CachedAPIClient):
    """
    Client for accessing ToxCast bioactivity model predictions from EPA CompTox Dashboard.
    
    This class provides methods for retrieving computational model predictions,
    including endocrine disruption models like CERAPP (estrogen receptor) and
    CoMPARA (androgen receptor).
    
    Args:
        api_key (str, optional): API key for accessing the CompTox API. If not provided,
            will attempt to load from configuration file.
    
    Attributes:
        base_url (str): Base URL for the CompTox API
        api_key (str): API key for authentication
        session (requests.Session): Persistent session for API requests
    
    Example:
        >>> from pycomptox import BioactivityModel
        >>> model_client = BioactivityModel()
        >>> 
        >>> # Get all model predictions for a chemical
        >>> models = model_client.get_toxcast_model_by_dtxsid("DTXSID7020182")
        >>> 
        >>> # Get CERAPP model predictions specifically
        >>> cerapp = model_client.get_toxcast_model_by_dtxsid_and_model(
        ...     "DTXSID7020182", "CERAPP"
        ... )
    """

    #: Model predictions are rate-sensitive; throttle by default.
    default_time_delay: float = 0.1
    
    def get_toxcast_model_by_dtxsid(self, dtxsid: str, use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all ToxCast model predictions for a given chemical.
        
        Returns computational toxicity model predictions including endocrine disruption
        models (CERAPP for estrogen receptor, CoMPARA for androgen receptor) and other
        high-throughput screening models.
        
        Args:
            dtxsid: DSSTox Substance Identifier for the chemical (e.g., "DTXSID7020182")
        
        Returns:
            List of model prediction dictionaries. Each prediction contains:
                - id: Unique identifier for the prediction
                - dtxsid: Chemical identifier
                - model: Model name (e.g., "CERAPP", "CoMPARA")
                - receptor: Target receptor (e.g., "Estrogen Receptor")
                - agonist: Agonist activity prediction
                - antagonist: Antagonist activity prediction
                - binding: Binding affinity prediction
                - modelDesc: Detailed model description
        
        Raises:
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox import BioactivityModel
            >>> model_client = BioactivityModel()
            >>> 
            >>> # Get all model predictions for bisphenol A
            >>> models = model_client.get_toxcast_model_by_dtxsid("DTXSID7020182")
            >>> 
            >>> # Display available models
            >>> for model in models:
            ...     print(f"{model['model']}: {model['receptor']}")
            >>> 
            >>> # Check estrogen receptor activity
            >>> cerapp = next((m for m in models if m['model'] == 'CERAPP'), None)
            >>> if cerapp:
            ...     print(f"ER Agonist: {cerapp['agonist']}")
            ...     print(f"ER Antagonist: {cerapp['antagonist']}")
        
        Note:
            Common ToxCast models include:
            - CERAPP: Collaborative Estrogen Receptor Activity Prediction Project
            - CoMPARA: Collaborative Modeling Project for Androgen Receptor Activity
            Models provide binary (active/inactive) or probabilistic predictions.
        
        Reference:
            EPA's ToxCast program develops computational models to predict chemical
            bioactivity and prioritize chemicals for further testing. See EPA's
            ToxCast dashboard for model details and validation metrics.
        """
        endpoint = f"bioactivity/models/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_toxcast_model_by_dtxsid_and_model(
        self, dtxsid: str, model: str, use_cache: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve specific ToxCast model predictions for a chemical.
        
        Returns computational toxicity predictions filtered by model type. Useful
        for focusing on specific endpoints like estrogen or androgen receptor activity.
        
        Args:
            dtxsid: DSSTox Substance Identifier for the chemical (e.g., "DTXSID7020182")
            model: Model name to filter by (e.g., "CERAPP", "CoMPARA")
        
        Returns:
            List of model prediction dictionaries for the specified model:
                - id: Unique identifier for the prediction
                - dtxsid: Chemical identifier
                - model: Model name
                - receptor: Target receptor
                - agonist: Agonist activity prediction
                - antagonist: Antagonist activity prediction
                - binding: Binding affinity prediction
                - modelDesc: Detailed model description
        
        Raises:
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox import BioactivityModel
            >>> model_client = BioactivityModel()
            >>> 
            >>> # Get CERAPP predictions for bisphenol A
            >>> cerapp = model_client.get_toxcast_model_by_dtxsid_and_model(
            ...     "DTXSID7020182", "CERAPP"
            ... )
            >>> 
            >>> # Check estrogen receptor activity
            >>> if cerapp:
            ...     result = cerapp[0]
            ...     print(f"Chemical: {result['dtxsid']}")
            ...     print(f"ER Agonist: {result['agonist']}")
            ...     print(f"ER Antagonist: {result['antagonist']}")
            ...     print(f"ER Binding: {result['binding']}")
            >>> 
            >>> # Get androgen receptor predictions
            >>> compara = model_client.get_toxcast_model_by_dtxsid_and_model(
            ...     "DTXSID7020182", "CoMPARA"
            ... )
        
        Note:
            Available models include:
            - CERAPP: Estrogen receptor activity (agonist, antagonist, binding)
            - CoMPARA: Androgen receptor activity (agonist, antagonist, binding)
            Model names are case-sensitive in the API.
        
        Reference:
            CERAPP and CoMPARA models are consensus models developed through
            collaborative efforts. They integrate predictions from multiple
            QSAR models to provide robust bioactivity predictions.
        """
        endpoint = "bioactivity/models/search/"
        params = {"dtxsid": dtxsid, "model": model}
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)
