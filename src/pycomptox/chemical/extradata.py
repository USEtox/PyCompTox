"""
Chemical Extra Data API client for EPA CompTox Dashboard.

This module provides access to additional reference data including:
- Literature references count
- PubMed references
- Google Patent references
- General reference counts

Author: PyCompTox Contributors
License: MIT
"""

import os
import time
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urljoin

from ..base import CachedAPIClient


class ExtraData(CachedAPIClient):
    """
    Client for accessing chemical extra data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving reference counts and
    additional metadata for chemicals including:
    - Total reference counts
    - Literature references
    - PubMed citations
    - Google Patent references
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float, **kwargs): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import ExtraData
        >>> extra = ExtraData()
        >>> 
        >>> # Get extra data for Bisphenol A
        >>> data = extra.get_data_by_dtxsid("DTXSID7020182")
        >>> print(f"PubMed refs: {data['pubmed']}")
        >>> print(f"Patents: {data['googlePatent']}")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api",
        time_delay_between_calls: float = 0.0,
        **kwargs
    ):
        """Initialize the ExtraData client."""
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            time_delay_between_calls=time_delay_between_calls,
            **kwargs
        )
    
    def get_data_by_dtxsid(self, dtxsid: str, use_cache: Optional[bool] = None) -> Dict[str, Any]:
        """
        Get extra reference data for a chemical by DTXSID.
        
        Returns counts of various reference sources including literature,
        PubMed citations, Google Patents, and total reference counts.
        
        Args:
            dtxsid (str): CompTox substance identifier (e.g., "DTXSID7020182")
            
        Returns:
            dict: Extra data with fields:
                - dtxsid: DSSTox Substance Identifier
                - dtxcid: DSSTox Compound Identifier
                - refs: Total reference count
                - googlePatent: Number of Google Patent references
                - literature: Number of literature references
                - pubmed: Number of PubMed citations
                
        Raises:
            ValueError: If chemical not found or invalid DTXSID
            requests.exceptions.RequestException: For API errors
            
        Example:
            >>> extra = ExtraData()
            >>> data = extra.get_data_by_dtxsid("DTXSID7020182")
            >>> print(f"DTXSID: {data['dtxsid']}")
            >>> print(f"Total references: {data['refs']}")
            >>> print(f"PubMed citations: {data['pubmed']}")
            >>> print(f"Patents: {data['googlePatent']}")
            >>> print(f"Literature: {data['literature']}")
        """
        endpoint = f"chemical/extra-data/search/by-dtxsid/{dtxsid}"
        result = self._make_cached_request(endpoint, use_cache=use_cache)
        # API returns a list, return first element if available
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        return result

    def get_data_by_dtxsid_batch(self, dtxsids: List[str], use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get extra reference data for multiple chemicals in a single request.
        
        Batch retrieval of reference counts and metadata for up to 1000 chemicals.
        More efficient than making individual requests when querying multiple chemicals.
        
        Args:
            dtxsids (List[str]): List of CompTox substance identifiers
                (maximum 1000 DTXSIDs)
            
        Returns:
            List[dict]: List of extra data dictionaries, each containing:
                - `dtxsid`: DSSTox Substance Identifier
                - `dtxcid`: DSSTox Compound Identifier
                - `refs`: Total reference count
                - `googlePatent`: Number of Google Patent references
                - `literature`: Number of literature references
                - `pubmed`: Number of PubMed citations
                
        Raises:
            ValueError: If more than 1000 DTXSIDs provided
            requests.exceptions.RequestException: For API errors
            
        Example:
            >>> extra = ExtraData()
            >>> dtxsids = ["DTXSID7020182", "DTXSID2021315", "DTXSID5020001"]
            >>> results = extra.get_data_by_dtxsid_batch(dtxsids)
            >>> 
            >>> for data in results:
            ...     pubmed_count = data.get("pubmed", 0)
            ...     dtxsid = data.get("dtxsid", "")
            ...     print(f"{dtxsid}: {pubmed_count} PubMed refs")
            >>> 
            >>> # Find chemicals with most references
            >>> sorted_data = sorted(results, key=lambda x: x.get("refs", 0), reverse=True)
            >>> top = sorted_data[0]
            >>> print(f"Most referenced: {top.get('dtxsid')} with {top.get('refs')} refs")
        """
        if len(dtxsids) > 1000:
            raise ValueError(f"Maximum 1000 DTXSIDs allowed, got {len(dtxsids)}")
        
        endpoint = "chemical/extra-data/search/by-dtxsid/"
        return self._make_cached_request(endpoint, method='POST', json=dtxsids, use_cache=use_cache)