"""
Bioactivity Data API client for EPA CompTox Dashboard.

This module provides access to bioactivity data including:
- Summary data by DTXSID, tissue, and AEID
- Detailed bioactivity data by various identifiers
- AED (Activity-Exposure-Dose) data
- Batch operations for multiple identifiers

Author: PyCompTox Contributors
License: MIT
"""

import time
from typing import List, Dict, Any, Optional, Union
import requests
from urllib.parse import urljoin

from ..base import CachedAPIClient


class BioactivityData(CachedAPIClient):
    """
    Client for accessing bioactivity data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving:
    - Summary data by DTXSID, tissue, and AEID
    - Detailed bioactivity data records
    - AED (Activity-Exposure-Dose) data
    - Batch operations for multiple identifiers
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import BioactivityData
        >>> client = BioactivityData()
        >>> 
        >>> # Get summary data
        >>> summary = client.get_summary_by_dtxsid("DTXSID9026974")
        >>> 
        >>> # Get data by AEID
        >>> data = client.get_data_by_aeid(3032)
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api/",
        time_delay_between_calls: float = 0.0,
        **kwargs
    ):
        """
        Initialize the BioactivityData client.
        
        Args:
            api_key: CompTox API key (optional, will be loaded from config if not provided)
            base_url: Base URL for the CompTox API
            time_delay_between_calls: Delay between API calls in seconds
            **kwargs: Additional arguments for CachedAPIClient (cache_manager, use_cache)
        
        Raises:
            ValueError: If no API key is provided or found in configuration
        """
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            time_delay_between_calls=time_delay_between_calls,
            **kwargs
        )

    def get_summary_by_dtxsid_and_tissue(self, dtxsid: str, tissue: str, use_cache: Optional[bool] = None) -> dict:
        """
        Get bioactivity summary data for a chemical filtered by tissue type.
        
        Retrieves summary bioactivity data for a specific chemical (by DTXSID)
        filtered by tissue of origin.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID7024241')
            tissue: Tissue of origin (e.g., 'liver', 'kidney')
        
        Returns:
            Dictionary containing summary bioactivity data including:
                - intendedTargetFamily: Target family
                - dtxsid: Chemical identifier
                - tissue: Tissue type
                - maxMedConc: Maximum median concentration
                - continuousHitCall: Continuous hit call value
                - chemicalName: Name of chemical
                - hitCall: Hit call classification
                - cutOff: Activity cutoff value
                - logAC50: Log of AC50 value
                - ac50: Half maximal activity concentration
                - acc: Activity concentration at cutoff
        
        Raises:
            ValueError: If dtxsid or tissue is not a valid string
        
        Example:
            >>> client = BioactivityData()
            >>> summary = client.get_summary_by_dtxsid_and_tissue('DTXSID7024241', 'liver')
            >>> print(summary['chemicalName'])
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        if not tissue or not isinstance(tissue, str):
            raise ValueError("tissue must be a non-empty string")
        
        endpoint = "bioactivity/data/summary/search/by-tissue/"
        params = {"dtxsid": dtxsid, "tissue": tissue}
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)

    def get_summary_by_dtxsid(self, dtxsid: str, use_cache: Optional[bool] = None) -> dict:
        """
        Get bioactivity summary data for a chemical.
        
        Retrieves summary bioactivity data for a specific chemical identified
        by its DSSTox Substance Identifier (DTXSID).
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID9026974')
        
        Returns:
            Summary bioactivity data for the chemical
        
        Raises:
            ValueError: If dtxsid is not a valid string
        
        Example:
            >>> client = BioactivityData()
            >>> summary = client.get_summary_by_dtxsid('DTXSID9026974')
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"bioactivity/data/summary/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_summary_by_aeid(self, aeid: str, use_cache: Optional[bool] = None) -> dict:
        """
        Get summary by aeid
        get /bioactivity/data/summary/search/by-aeid/{aeid}
        Return summary data for given aeid
        aeid int32 Numeric assay endpoint identifier
        Examples: 3032

        curl -X GET "https://comptox.epa.gov/ctx-api/bioactivity/data/summary/search/by-aeid/3032" \
        -H 'accept: application/json' 

        response
        200 OK
        US EPA's Toxicity Forecaster (ToxCast) program makes invitro medium- and high-throughput screening assay data publicly available for prioritization and hazard characterization.The summary endpoint returns the number of active hits and total multi- and single-concentration chemicals tested for specific ‘aeids’. For multi-concentration data, a continuous hit call value greater than or equal to 0.9 is considered active, whereas values less than 0.9 are considered inactive. For single concentration data, the hit call value is binary where 1 is active and 0 is inactive. Multiple samples of the same chemical may be tested for a given assay endpoint, and all samples per endpoint are reflected in these counts.
        {
        "aeid": 0,
        "activeMc": 0,
        "totalMc": 0,
        "activeSc": 0,
        "totalSc": 0
        }
        """
        if not isinstance(aeid, (int, str)):
            raise ValueError("aeid must be an integer or string")
        
        endpoint = f"bioactivity/data/summary/search/by-aeid/{aeid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_data_by_spid(self, spid: str, use_cache: Optional[bool] = None) -> dict:
        """
        Get bioactivity data by sample identifier.
        
        Retrieves bioactivity data for a specific sample identified by its SPID
        (Sample Identifier).
        
        Args:
            spid: Sample identifier (e.g., 'EPAPLT0232A03')
        
        Returns:
            Bioactivity data for the specified sample
        
        Raises:
            ValueError: If spid is not a valid non-empty string
        
        Example:
            >>> client = BioactivityData()
            >>> data = client.get_data_by_spid('EPAPLT0232A03')
        """
        if not spid or not isinstance(spid, str):
            raise ValueError("spid must be a non-empty string")
        
        endpoint = f"bioactivity/data/search/by-spid/{spid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_data_by_m4id(self, m4id: str, use_cache: Optional[bool] = None) -> dict:
        """
        Get bioactivity data by data identifier.
        
        Retrieves a single bioactivity data record for a specific M4ID
        (numeric data identifier).
        
        Args:
            m4id: Numeric data identifier (e.g., '1135145')
        
        Returns:
            Single bioactivity data record for the specified M4ID
        
        Raises:
            ValueError: If m4id is not an integer or string
        
        Example:
            >>> client = BioactivityData()
            >>> data = client.get_data_by_m4id('1135145')
        """
        if not isinstance(m4id, (int, str)):
            raise ValueError("m4id must be an integer or string")
        
        endpoint = f"bioactivity/data/search/by-m4id/{m4id}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_data_by_dtxsid_and_projection(self, dtxsid: str, projection: str="", use_cache: Optional[bool] = None) -> dict:
        """
        Get bioactivity data for a chemical with optional projection.
        
        Retrieves bioactivity data for a specific chemical identified by DTXSID,
        with optional projection parameter to control the format of returned data.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID7020182')
            projection: Optional projection type. Use 'toxcast-summary-plot' for
                summary plot data, or omit for default BioactivityDataAll format.
        
        Returns:
            Bioactivity data for the chemical in requested format
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> client = BioactivityData()
            >>> # Get default format
            >>> data = client.get_data_by_dtxsid_and_projection('DTXSID7020182')
            >>> # Get summary plot format
            >>> plot_data = client.get_data_by_dtxsid_and_projection(
            ...     'DTXSID7020182', projection='toxcast-summary-plot')
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"bioactivity/data/search/by-dtxsid/{dtxsid}"
        params = {"projection": projection} if projection else None
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)

    def get_data_by_aeid(self, aeid: int, use_cache: Optional[bool] = None) -> dict:
        """
        Get detailed bioactivity data for an assay endpoint.
        
        Retrieves all bioactivity data records associated with a specific
        assay endpoint identifier (AEID).
        
        Args:
            aeid: Numeric assay endpoint identifier (e.g., 3032)
        
        Returns:
            All bioactivity data records for the specified assay endpoint
        
        Raises:
            ValueError: If aeid is not a positive integer
        
        Example:
            >>> client = BioactivityData()
            >>> data = client.get_data_by_aeid(3032)
        """
        if not isinstance(aeid, int) or aeid <= 0:
            raise ValueError("aeid must be a positive integer")
        
        endpoint = f"bioactivity/data/search/by-aeid/{aeid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_aed_data_by_dtxsid(self, dtxsid: str, use_cache: Optional[bool] = None) -> dict:
        """
        Get Activity-Exposure-Dose (AED) data for a chemical.
        
        Retrieves AED bioactivity data for a specific chemical identified
        by its DSSTox Substance Identifier (DTXSID).
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID5021209')
        
        Returns:
            AED bioactivity data for the chemical
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> client = BioactivityData()
            >>> aed_data = client.get_aed_data_by_dtxsid('DTXSID5021209')
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"bioactivity/data/aed/search/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def find_bioactivity_data_by_spid_batch(self, spids: list, use_cache: Optional[bool] = None) -> dict:
        """
        Batch retrieve bioactivity data by sample identifiers.
        
        Retrieves bioactivity data for multiple samples in a single request.
        
        Args:
            spids: List of sample identifiers (e.g., ['EPAPLT0232A03', 'EPAPLT0232A04'])
        
        Returns:
            Bioactivity data for all requested sample identifiers
        
        Raises:
            ValueError: If spids is not a non-empty list or contains non-string values
        
        Example:
            >>> client = BioactivityData()
            >>> data = client.find_bioactivity_data_by_spid_batch(
            ...     ['EPAPLT0232A03', 'EPAPLT0232A04'])
        """
        if not spids or not isinstance(spids, list):
            raise ValueError("spids must be a non-empty list")
        if not all(isinstance(spid, str) for spid in spids):
            raise ValueError("All spids must be strings")
        
        endpoint = "bioactivity/data/search/by-spid/"
        # Note: Batch POST requests bypass cache since they're not typically cacheable
        self._enforce_rate_limit()
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=spids)
        response.raise_for_status()
        return response.json()

    def find_bioactivity_data_by_m4id_batch(self, m4ids: list, use_cache: Optional[bool] = None) -> dict:
        """
        Batch retrieve bioactivity data by data identifiers.
        
        Retrieves bioactivity data for multiple M4IDs (data identifiers) in a single request.
        
        Args:
            m4ids: List of numeric data identifiers (e.g., [1135145, 1135146])
        
        Returns:
            Bioactivity data for all requested data identifiers
        
        Raises:
            ValueError: If m4ids is not a non-empty list or contains invalid values
        
        Example:
            >>> client = BioactivityData()
            >>> data = client.find_bioactivity_data_by_m4id_batch([1135145, 1135146])
        """
        if not m4ids or not isinstance(m4ids, list):
            raise ValueError("m4ids must be a non-empty list")
        if not all(isinstance(m4id, (int, str)) for m4id in m4ids):
            raise ValueError("All m4ids must be integers or strings")
        
        endpoint = "bioactivity/data/search/by-m4id/"
        # Note: Batch POST requests bypass cache since they're not typically cacheable
        self._enforce_rate_limit()
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=m4ids)
        response.raise_for_status()
        return response.json()

    def find_bioactivity_data_by_dtxsid_batch(self, dtxsids: list, use_cache: Optional[bool] = None) -> dict:
        """
        Batch retrieve bioactivity data by chemical identifiers.
        
        Retrieves bioactivity data for multiple chemicals identified by their
        DSSTox Substance Identifiers (DTXSIDs) in a single request.
        
        Args:
            dtxsids: List of DSSTox Substance Identifiers
                (e.g., ['DTXSID7020182', 'DTXSID9026974'])
        
        Returns:
            Bioactivity data for all requested chemicals
        
        Raises:
            ValueError: If dtxsids is not a non-empty list or contains non-string values
        
        Example:
            >>> client = BioactivityData()
            >>> data = client.find_bioactivity_data_by_dtxsid_batch(
            ...     ['DTXSID7020182', 'DTXSID9026974'])
        """
        if not dtxsids or not isinstance(dtxsids, list):
            raise ValueError("dtxsids must be a non-empty list")
        if not all(isinstance(dtxsid, str) for dtxsid in dtxsids):
            raise ValueError("All dtxsids must be strings")
        
        endpoint = "bioactivity/data/search/by-dtxsid/"
        # Note: Batch POST requests bypass cache since they're not typically cacheable
        self._enforce_rate_limit()
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=dtxsids)
        response.raise_for_status()
        return response.json()

    def find_bioactivity_data_by_aeid_batch(self, aeids: list, use_cache: Optional[bool] = None) -> dict:
        """
        Batch retrieve bioactivity data by assay endpoint identifiers.
        
        Retrieves bioactivity data for multiple assay endpoints in a single request.
        
        Args:
            aeids: List of numeric assay endpoint identifiers (e.g., [3032, 3033])
        
        Returns:
            Bioactivity data for all requested assay endpoints
        
        Raises:
            ValueError: If aeids is not a non-empty list or contains non-positive integers
        
        Example:
            >>> client = BioactivityData()
            >>> data = client.find_bioactivity_data_by_aeid_batch([3032, 3033])
        """
        if not aeids or not isinstance(aeids, list):
            raise ValueError("aeids must be a non-empty list")
        if not all(isinstance(aeid, int) and aeid > 0 for aeid in aeids):
            raise ValueError("All aeids must be positive integers")
        
        endpoint = "bioactivity/data/search/by-aeid/"
        # Note: Batch POST requests bypass cache since they're not typically cacheable
        self._enforce_rate_limit()
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=aeids)
        response.raise_for_status()
        return response.json()

    def find_aed_data_by_dtxsid_batch(self, dtxsids: list, use_cache: Optional[bool] = None) -> dict:
        """
        Batch retrieve Activity-Exposure-Dose (AED) data by chemical identifiers.
        
        Retrieves AED bioactivity data for multiple chemicals identified by their
        DSSTox Substance Identifiers (DTXSIDs) in a single request.
        
        Args:
            dtxsids: List of DSSTox Substance Identifiers
                (e.g., ['DTXSID5021209', 'DTXSID7020182'])
        
        Returns:
            AED bioactivity data for all requested chemicals
        
        Raises:
            ValueError: If dtxsids is not a non-empty list or contains non-string values
        
        Example:
            >>> client = BioactivityData()
            >>> aed_data = client.find_aed_data_by_dtxsid_batch(
            ...     ['DTXSID5021209', 'DTXSID7020182'])
        """
        if not dtxsids or not isinstance(dtxsids, list):
            raise ValueError("dtxsids must be a non-empty list")
        if not all(isinstance(dtxsid, str) for dtxsid in dtxsids):
            raise ValueError("All dtxsids must be strings")
        
        endpoint = "bioactivity/data/aed/search/by-dtxsid"
        # Note: Batch POST requests bypass cache since they're not typically cacheable
        self._enforce_rate_limit()
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=dtxsids)
        response.raise_for_status()
        return response.json()
