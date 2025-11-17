"""
Bioactivity AOP (Adverse Outcome Pathway) API client for EPA CompTox Dashboard.

This module provides access to Adverse Outcome Pathway data linking:
- ToxCast assay endpoints (AEIDs) to AOP events
- Event numbers to AOP pathways
- Entrez gene IDs to AOP events

Author: PyCompTox Contributors
License: MIT
"""

import time
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urljoin

from .config import load_api_key


class BioactivityAOP:
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
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0
    ):
        """
        Initialize the BioactivityAOP client.
        
        Args:
            api_key: CompTox API key (optional, will be loaded from config if not provided)
            base_url: Base URL for the CompTox API
            time_delay_between_calls: Delay between API calls in seconds
        
        Raises:
            ValueError: If no API key is provided or found in configuration
        """
        self.base_url = base_url
        self.time_delay = time_delay_between_calls
        self.last_call_time = 0
        
        # Get API key from parameter, config, or environment
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = load_api_key()
            if not self.api_key:
                raise ValueError(
                    "No API key provided. Either pass api_key parameter or "
                    "set it using save_api_key() or COMPTOX_API_KEY environment variable."
                )
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Make an HTTP request to the CompTox API.
        
        Args:
            method: HTTP method (GET)
            endpoint: API endpoint path
            params: Query parameters
        
        Returns:
            API response data
        
        Raises:
            PermissionError: If API key is invalid (403)
            ValueError: If request fails or returns no data
            RuntimeError: For other API errors
        """
        # Rate limiting
        if self.time_delay > 0:
            current_time = time.time()
            time_since_last_call = current_time - self.last_call_time
            if time_since_last_call < self.time_delay:
                time.sleep(self.time_delay - time_since_last_call)
            self.last_call_time = time.time()
        
        url = urljoin(self.base_url, endpoint)
        headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Check for specific error codes
            if response.status_code == 403:
                raise PermissionError(
                    "Invalid API key. Please check your API key configuration."
                )
            elif response.status_code == 404:
                raise ValueError(
                    f"Endpoint not found: {endpoint}. The API endpoint may not exist or the resource was not found."
                )
            elif response.status_code != 200:
                raise RuntimeError(
                    f"API request failed with status {response.status_code}: {response.text}"
                )
            
            # Try to parse JSON response
            try:
                data = response.json()
            except ValueError:
                raise ValueError("API response is not valid JSON")
            
            return data
            
        except requests.exceptions.Timeout:
            raise RuntimeError(f"Request timed out for endpoint: {endpoint}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request failed: {str(e)}")

    def get_aop_data_by_toxcast_aeid(self, toxcast_aeid: int) -> Optional[List[Dict[str, Any]]]:
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
        return self._make_request("GET", endpoint)

    def get_aop_data_by_event_number(self, event_number: int) -> Optional[List[Dict[str, Any]]]:
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
        return self._make_request("GET", endpoint)

    def get_aop_data_by_entrez_gene_id(self, entrez_gene_id: int) -> Optional[List[Dict[str, Any]]]:
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
        return self._make_request("GET", endpoint)