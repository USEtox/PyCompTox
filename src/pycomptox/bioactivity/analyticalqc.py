"""
Analytical QC Data API client for EPA CompTox Dashboard.

This module provides access to analytical quality control data for chemicals
tested in ToxCast high-throughput screening assays.

Author: PyCompTox Contributors
License: MIT
"""

from typing import Optional

from ..base import CachedAPIClient
from ..exceptions import NotFoundError


class AnalyticalQC(CachedAPIClient):
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
    
    def get_analytical_qc_data_by_dtxsid(self, dtxsid: str, use_cache: Optional[bool] = None) -> Optional[list]:
        """
        Retrieve analytical quality control data for a chemical.
        
        Returns QC information about chemical sample preparation, stability tests,
        and analytical performance during ToxCast screening. Multiple QC records
        may exist for a single chemical representing different samples or test runs.
        
        Args:
            dtxsid: DSSTox Substance Identifier for the chemical (e.g., "DTXSID7020182")
        
        Returns:
            List of QC data dictionaries, or an empty list if the chemical has
            no QC record. Each dictionary contains:
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
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.

        Note:
            A chemical with no QC record returns an empty list rather than
            raising NotFoundError.

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
        try:
            result = self._make_cached_request(endpoint, use_cache=use_cache)
            return result if result is not None else []
        except NotFoundError:
            # Chemicals with no analytical QC record answer 404; an absent
            # record is a normal result here, not an error.
            return []