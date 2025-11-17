"""
Analytical QC Data API client for EPA CompTox Dashboard.

This module provides access to analytical quality control data for chemicals
tested in ToxCast high-throughput screening assays.

Author: PyCompTox Contributors
License: MIT
"""

import time
from typing import Dict, Any, Optional
import requests
from urllib.parse import urljoin

from .config import load_api_key


class AnalyticalQC:
    """
    Client for accessing analytical QC data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving quality control information about
    chemical sample preparation, stability, and analytical performance in ToxCast
    screening assays.
    
    Args:
        api_key (str, optional): API key for accessing the CompTox API. If not provided,
            will attempt to load from configuration file.
    
    Attributes:
        base_url (str): Base URL for the CompTox API
        api_key (str): API key for authentication
        session (requests.Session): Persistent session for API requests
    
    Example:
        >>> from pycomptox import AnalyticalQC
        >>> qc_client = AnalyticalQC()
        >>> 
        >>> # Get QC data for a chemical
        >>> qc_data = qc_client.get_analytical_qc_data_by_dtxsid("DTXSID7020182")
        >>> print(f"QC Level: {qc_data['qcLevel']}")
        >>> print(f"Quality Call: {qc_data['call']}")
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AnalyticalQC client.
        
        Args:
            api_key (str, optional): API key for CompTox API access
        """
        self.base_url = "https://comptox.epa.gov/ctx-api/"
        self.api_key = api_key or load_api_key()
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"x-api-key": self.api_key})
        self.session.headers.update({"accept": "application/json"})
        self._last_request_time = 0
        self._min_request_interval = 0.1  # Rate limiting: max 10 requests per second

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Make an HTTP request to the CompTox API with rate limiting and error handling.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            data: Request body data
        
        Returns:
            Parsed JSON response
        
        Raises:
            PermissionError: If API key is invalid or missing
            RuntimeError: For other API errors
        """
        # Rate limiting
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_request_interval:
            time.sleep(self._min_request_interval - elapsed)
        
        url = urljoin(self.base_url, endpoint)
        response = self.session.request(method, url, params=params, json=data)
        self._last_request_time = time.time()
        
        if response.status_code == 403:
            raise PermissionError(
                "API key is invalid or missing. Please provide a valid API key."
            )
        elif response.status_code == 404:
            # Return None for not found instead of raising
            return None
        elif not response.ok:
            raise RuntimeError(
                f"API request failed with status {response.status_code}: {response.text}"
            )
        
        return response.json()

    def get_analytical_qc_data_by_dtxsid(self, dtxsid: str) -> Optional[list]:
        """
        Retrieve analytical quality control data for a chemical.
        
        Returns QC information about chemical sample preparation, stability tests,
        and analytical performance during ToxCast screening. Multiple QC records
        may exist for a single chemical representing different samples or test runs.
        
        Args:
            dtxsid: DSSTox Substance Identifier for the chemical (e.g., "DTXSID7020182")
        
        Returns:
            List of QC data dictionaries, empty list if not found, or None on error.
            Each dictionary contains:
                - analyticalQcId: Unique identifier for QC record
                - dtxsid: Chemical identifier
                - chnm: Chemical name
                - spid: Sample identifier
                - qcLevel: Quality control level classification
                - t0: Initial time point measurement
                - t4: 4-hour time point measurement
                - call: Overall QC assessment call
                - annotation: QC annotations and notes
                - flags: Quality flags raised during testing
                - averageMass: Average molecular mass
                - log10VaporPressureOperaPred: Predicted vapor pressure (log10)
                - logkowOctanolWaterOperaPred: Predicted octanol-water partition coefficient
                - exportDate: Date of data export
                - dataVersion: Version of QC data
                - porCaution: Persistent/bioaccumulative/toxic (PBT) caution flag
        
        Raises:
            PermissionError: If API key is invalid
            RuntimeError: For other API errors
        
        Example:
            >>> from pycomptox import AnalyticalQC
            >>> qc_client = AnalyticalQC()
            >>> 
            >>> # Get QC data for bisphenol A
            >>> qc_records = qc_client.get_analytical_qc_data_by_dtxsid("DTXSID7020182")
            >>> 
            >>> if qc_records:
            ...     print(f"Found {len(qc_records)} QC records")
            ...     
            ...     # Examine first record
            ...     first_record = qc_records[0]
            ...     print(f"Chemical: {first_record['chnm']}")
            ...     print(f"Sample ID: {first_record['spid']}")
            ...     print(f"QC Level: {first_record['qcLevel']}")
            ...     print(f"QC Call: {first_record['call']}")
            ...     print(f"Stability T0: {first_record['t0']}")
            ...     print(f"Stability T4: {first_record['t4']}")
            ...     
            ...     if first_record['flags']:
            ...         print(f"Flags: {first_record['flags']}")
            ...     
            ...     if first_record.get('annotation'):
            ...         print(f"Annotation: {first_record['annotation']}")
            >>> else:
            ...     print("No QC data available for this chemical")
        
        Note:
            - Multiple QC records may exist for the same chemical (different samples/runs)
            - QC levels typically include designations like "Level 1", "Level 2", etc.
            - The 'call' field provides overall assessment (e.g., "S" for stable, "U" for unstable)
            - T0 and T4 measurements assess chemical stability over time
            - Flags indicate specific issues detected during QC process
            - Returns empty list if no QC data exists for the chemical
        
        Reference:
            EPA's ToxCast program performs rigorous analytical QC to ensure data
            quality. QC data includes sample preparation verification, stability
            testing, and analytical method performance validation.
        """
        endpoint = f"bioactivity/analyticalqc/search/by-dtxsid/{dtxsid}"
        result = self._make_request("GET", endpoint)
        return result if result is not None else []