"""
MMDB API client for EPA CompTox Dashboard.

This module provides access to the Molecular Modeling Database (MMDB) including:
- Harmonized single-sample records by medium
- Environmental monitoring and measurement data

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional

from ..base import CachedAPIClient


class MMDB(CachedAPIClient):
    """
    Client for accessing Molecular Modeling Database (MMDB) from EPA CompTox Dashboard.
    
    This class provides methods for retrieving environmental monitoring and measurement
    data, including harmonized single-sample records organized by environmental medium.
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float, **kwargs): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import MMDB
        >>> mmdb = MMDB()
        >>> 
        >>> # Get single-sample records for surface water
        >>> data = mmdb.get_harmonized_single_sample_by_medium("surface water")
    """

    def get_harmonized_single_sample_by_medium(self, medium: str, page_number: int = 1, use_cache: Optional[bool] = None) -> Dict[str, Any]:
        """
        Get harmonized single-sample records by environmental medium.
        
        Retrieves harmonized single-sample environmental monitoring records filtered
        by the type of environmental medium (e.g., surface water, air, soil). The data
        is paginated to handle large result sets.
        
        Args:
            medium: Harmonized medium type (e.g., 'surface water', 'air', 'soil',
                'groundwater', 'sediment', 'biota')
            page_number: Page number for pagination (default: 1)
        
        Returns:
            Dictionary containing paginated single-sample records for the specified medium.
            The structure typically includes:
                - data: List of sample records
                - pagination information (page number, total pages, etc.)
        
        Raises:
            ValueError: If medium is not a valid non-empty string
        
        Example:
            >>> mmdb = MMDB()
            >>> # Get first page of surface water samples
            >>> data = mmdb.get_harmonized_single_sample_by_medium("surface water")
            >>> 
            >>> # Get second page
            >>> data_page2 = mmdb.get_harmonized_single_sample_by_medium("surface water", page_number=2)
        """
        if not medium or not isinstance(medium, str):
            raise ValueError("medium must be a non-empty string")
        
        if not isinstance(page_number, int) or page_number < 1:
            raise ValueError("page_number must be a positive integer")
        
        endpoint = "exposure/mmdb/single-sample/by-medium"
        params = {
            "medium": medium,
            "pageNumber": page_number
        }
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)
    
    def get_harmonized_single_sample_by_dtxsid(self, dtxsid: str, use_cache: Optional[bool] = None) -> Dict[str, Any]:
        """
        Get harmonized single-sample records for a chemical.
        
        Retrieves harmonized single-sample environmental monitoring records for a
        specific chemical identified by its DSSTox Substance Identifier (DTXSID).
        This provides environmental occurrence data across different media and locations.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., 'DTXSID7020182')
        
        Returns:
            Dictionary containing single-sample records for the specified chemical.
            Includes environmental measurements and detection information.
        
        Raises:
            ValueError: If dtxsid is not a valid non-empty string
        
        Example:
            >>> mmdb = MMDB()
            >>> samples = mmdb.get_harmonized_single_sample_by_dtxsid("DTXSID7020182")
        """
        if not dtxsid or not isinstance(dtxsid, str):
            raise ValueError("dtxsid must be a non-empty string")
        
        endpoint = f"exposure/mmdb/single-sample/by-dtxsid/{dtxsid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_harmonized_medium_categories(self, use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get all searchable harmonized medium categories.
        
        Retrieves a complete list of harmonized environmental medium categories
        available in the MMDB database, along with their definitions. This is useful
        for discovering valid medium types to use in other queries.
        
        Returns:
            List of dictionaries containing medium categories and their definitions.
            Each entry includes the medium name and description.
        
        Example:
            >>> mmdb = MMDB()
            >>> mediums = mmdb.get_harmonized_medium_categories()
            >>> for medium in mediums:
            ...     print(f"{medium['name']}: {medium.get('definition', '')}")
        """
        endpoint = "exposure/mmdb/mediums"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_harmonized_aggregate_records_by_medium(self, medium: str, page_number: int = 1, use_cache: Optional[bool] = None) -> Dict[str, Any]:
        """
        Get harmonized aggregate records by environmental medium.
        
        Retrieves aggregated (summarized) environmental monitoring records filtered
        by the type of environmental medium. Aggregate records provide summary
        statistics across multiple samples, useful for trend analysis and overview.
        The data is paginated to handle large result sets.
        
        Args:
            medium: Harmonized medium type (e.g., 'surface water', 'air', 'soil',
                'groundwater', 'sediment', 'biota')
            page_number: Page number for pagination (default: 1)
        
        Returns:
            Dictionary containing paginated aggregate records for the specified medium.
            Includes summary statistics and aggregated measurements.
        
        Raises:
            ValueError: If medium is not a valid non-empty string or page_number is invalid
        
        Example:
            >>> mmdb = MMDB()
            >>> # Get first page of surface water aggregates
            >>> agg_data = mmdb.get_harmonized_aggregate_records_by_medium("surface water")
            >>> 
            >>> # Get second page
            >>> agg_page2 = mmdb.get_harmonized_aggregate_records_by_medium("surface water", page_number=2)
        """
        if not medium or not isinstance(medium, str):
            raise ValueError("medium must be a non-empty string")
        
        if not isinstance(page_number, int) or page_number < 1:
            raise ValueError("page_number must be a positive integer")
        
        endpoint = "exposure/mmdb/aggregate/by-medium"
        params = {
            "medium": medium,
            "pageNumber": page_number
        }
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)