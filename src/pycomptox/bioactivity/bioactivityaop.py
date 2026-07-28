"""
Bioactivity AOP (Adverse Outcome Pathway) API client for EPA CompTox Dashboard.

This module provides access to Adverse Outcome Pathway data linking:
- ToxCast assay endpoints (AEIDs) to AOP events
- Event numbers to AOP pathways
- Entrez gene IDs to AOP events

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient


class BioactivityAOP(CachedAPIClient):
    """
    Client for accessing AOP (Adverse Outcome Pathway) data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving AOP data by:
    - ToxCast assay endpoint ID (AEID)
    - Event number
    - Entrez gene ID
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import BioactivityAOP
        >>> client = BioactivityAOP()
        >>> 
        >>> # Get AOP data by ToxCast AEID
        >>> aop_data = client.get_aop_data_by_toxcast_aeid(63)
        >>> 
        >>> # Get AOP data by event number
        >>> events = client.get_aop_data_by_event_number(18)
    """
    
    def get_aop_data_by_toxcast_aeid(self, toxcast_aeid: int, use_cache: Optional[bool] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get AOP data by ToxCast assay endpoint ID.
        
        Retrieves Adverse Outcome Pathway data associated with a specific
        ToxCast assay endpoint identifier (AEID).
        
        Args:
            toxcast_aeid: ToxCast assay endpoint identifier (integer)
        
        Returns:
            List of AOP records, each containing:
                - id: Record identifier
                - toxcastAeid: ToxCast AEID
                - entrezGeneId: Associated Entrez Gene ID
                - eventNumber: AOP event number
                - eventLink: Link to event details
                - aopNumber: AOP pathway number
                - aopLink: Link to AOP pathway
        
        Raises:
            ValueError: If toxcast_aeid is not a positive integer
        
        Example:
            >>> client = BioactivityAOP()
            >>> aop_data = client.get_aop_data_by_toxcast_aeid(63)
            >>> print(f"Found {len(aop_data)} AOP records")
        """
        if not isinstance(toxcast_aeid, int) or toxcast_aeid <= 0:
            raise ValueError("toxcast_aeid must be a positive integer")
        
        endpoint = f"bioactivity/aop/search/by-toxcast-aeid/{toxcast_aeid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_aop_data_by_event_number(self, event_number: int, use_cache: Optional[bool] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get AOP data by event number.
        
        Retrieves Adverse Outcome Pathway data for a specific event number,
        including all associated ToxCast assays and gene information.
        
        Args:
            event_number: AOP event number (integer)
        
        Returns:
            List of AOP records containing event, assay, and pathway information
        
        Raises:
            ValueError: If event_number is not a positive integer
        
        Example:
            >>> client = BioactivityAOP()
            >>> events = client.get_aop_data_by_event_number(18)
            >>> print(f"Event 18 has {len(events)} associated records")
        """
        if not isinstance(event_number, int) or event_number <= 0:
            raise ValueError("event_number must be a positive integer")
        
        endpoint = f"bioactivity/aop/search/by-event-number/{event_number}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_aop_data_by_entrez_gene_id(self, entrez_gene_id: int, use_cache: Optional[bool] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get AOP data by Entrez Gene ID.
        
        Retrieves Adverse Outcome Pathway data for a specific Entrez Gene ID,
        showing all AOP events and pathways associated with the gene.
        
        Args:
            entrez_gene_id: NCBI Entrez Gene identifier (integer)
        
        Returns:
            List of AOP records linking the gene to events and pathways
        
        Raises:
            ValueError: If entrez_gene_id is not a positive integer
        
        Example:
            >>> client = BioactivityAOP()
            >>> gene_aops = client.get_aop_data_by_entrez_gene_id(196)
            >>> print(f"Gene 196 is involved in {len(gene_aops)} AOP records")
        """
        if not isinstance(entrez_gene_id, int) or entrez_gene_id <= 0:
            raise ValueError("entrez_gene_id must be a positive integer")
        
        endpoint = f"bioactivity/aop/search/by-entrez-gene-id/{entrez_gene_id}"
        return self._make_cached_request(endpoint, use_cache=use_cache)