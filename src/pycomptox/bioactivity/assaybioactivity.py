"""
Bioactivity Assay Data API client for EPA CompTox Dashboard.

This module provides access to detailed bioassay data including:
- Single concentration data by assay endpoint ID (AEID)
- Assay endpoints by gene symbol
- Detailed assay data with multiple projection options

Author: PyCompTox Contributors
License: MIT
"""

from typing import List, Dict, Any, Optional, Union

from ..base import CachedAPIClient


class AssayBioactivity(CachedAPIClient):
    """
    Client for accessing bioactivity assay data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving:
    - Single concentration assay data by AEID
    - Assay endpoints associated with gene symbols
    - Detailed assay information with various projections
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
        use_cache (bool): Whether to use caching by default. Default is True.
    
    Example:
        >>> from pycomptox import AssayBioactivity
        >>> assay_client = AssayBioactivity()
        >>> 
        >>> # Get single concentration data
        >>> single_conc = assay_client.get_single_concentration_by_aeid(3032)
        >>> 
        >>> # Get assay endpoints for a gene
        >>> endpoints = assay_client.get_assay_endpoints_list("TUBA1A")
        >>> 
        >>> # Get detailed assay data with projection
        >>> assay_data = assay_client.get_assay_data_by_aeid_with_projections(
        ...     3032, 
        ...     projection="ccd-assay-gene"
        ... )
    """
    
    def get_single_concentration_by_aeid(
        self, 
        aeid: int,
        projection: str = "single-conc",
        use_cache: Optional[bool] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Get single concentration data by assay endpoint ID (AEID).
        
        Retrieves single concentration bioactivity data for a specific assay endpoint.
        
        Args:
            aeid: Assay Endpoint Identifier (AEID)
            projection: Data projection type (default: "single-conc")
        
        Returns:
            Single concentration data containing:
                - aeid (int): Assay endpoint ID
                - preferredName (str): Preferred chemical name
                - dtxsid (str): DSSTox substance identifier
                - casn (str): CAS Registry Number
                - hitc (int): Hit call
                - coff (float): Cutoff value
                - s2id (int): Sample ID
                - bmad (float): Baseline median absolute deviation
                - endpointName (str): Name of the endpoint
                - maxMedVal (float): Maximum median value
        
        Raises:
            ValueError: If AEID is invalid or no data found
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox import AssayBioactivity
            >>> assay_client = AssayBioactivity()
            >>> 
            >>> # Get single concentration data for AEID 3032
            >>> data = assay_client.get_single_concentration_by_aeid(3032)
            >>> print(f"Endpoint: {data['endpointName']}")
            >>> print(f"Hit call: {data['hitc']}")
            >>> 
            >>> # Process multiple chemicals
            >>> for item in data if isinstance(data, list) else [data]:
            ...     if item['hitc'] == 1:
            ...         print(f"{item['preferredName']} is active")
        """
        endpoint = f"bioactivity/assay/single-conc/search/by-aeid/{aeid}"
        params = {"projection": projection}
        
        data = self._make_cached_request(endpoint, params=params, use_cache=use_cache)
        
        # Raise ValueError if no data found for the AEID
        if data is None or (isinstance(data, (list, dict)) and not data):
            raise ValueError(f"No data found for AEID {aeid}")
        
        return data

    def get_assay_endpoints_list(self, gene_symbol: str, use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get list of assay endpoints associated with a gene symbol.
        
        Retrieves all assay endpoints that target the specified gene.
        
        Args:
            gene_symbol: Gene symbol (e.g., "TUBA1A", "TP53", "ESR1")
        
        Returns:
            List of assay endpoints. Each endpoint contains:
                - aeid (int): Assay endpoint ID
                - assayComponentEndpointDesc (str): Endpoint description
                - assayComponentEndpointName (str): Endpoint name
                - geneSymbol (str): Gene symbol
                - getsingleConcActive (str): Single concentration activity status
                - multiConcActives (str): Multi-concentration activity status
        
        Raises:
            ValueError: If gene symbol is invalid or no data found
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox import AssayBioactivity
            >>> assay_client = AssayBioactivity()
            >>> 
            >>> # Get all assay endpoints for tubulin gene
            >>> endpoints = assay_client.get_assay_endpoints_list("TUBA1A")
            >>> print(f"Found {len(endpoints)} endpoints for TUBA1A")
            >>> 
            >>> # Filter for active assays
            >>> for endpoint in endpoints:
            ...     if endpoint['multiConcActives']:
            ...         print(f"{endpoint['assayComponentEndpointName']}: {endpoint['assayComponentEndpointDesc']}")
            >>> 
            >>> # Get endpoints for estrogen receptor
            >>> esr1_endpoints = assay_client.get_assay_endpoints_list("ESR1")
        """
        endpoint = f"bioactivity/assay/search/by-gene/{gene_symbol}"
        
        data = self._make_cached_request(endpoint, use_cache=use_cache)
        
        # Raise ValueError if no endpoints found for the gene symbol
        if data is None or (isinstance(data, (list, dict)) and not data):
            raise ValueError(f"No assay endpoints found for gene symbol '{gene_symbol}'")
        
        return data

    def get_assay_data_by_aeid_with_projections(
        self,
        aeid: int,
        projection: Optional[str] = None,
        use_cache: Optional[bool] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Get detailed assay data by AEID with optional projection.
        
        Fetches comprehensive assay data with support for multiple projections.
        If no projection is specified, returns full assay data.
        
        Args:
            aeid: Assay Endpoint Identifier (AEID)
            projection: Optional projection type. Available options:
                - None (default): Full assay data
                - "ccd-assay-annotation": Assay annotations only
                - "ccd-assay-gene": Gene information only
                - "ccd-assay-citations": Citations only
                - "ccd-assay-tcpl": ToxCast pipeline methods
                - "ccd-assay-reagents": Reagent information
                - "assay-all": All available data
        
        Returns:
            Assay data dictionary with fields depending on projection.
            Full data (no projection) includes:
                - Basic assay info: aeid, assayComponentEndpointName, assayComponentEndpointDesc
                - Target info: intendedTargetType, intendedTargetFamily, biologicalProcessTarget
                - Assay design: assayDesignType, detectionTechnologyType, assayFormatType
                - Organism info: organism, tissue, cellFormat
                - Gene data: List of associated genes
                - Citations: List of references
                - Methods: mc2-mc6 and sc1-sc2 method lists
        
        Raises:
            ValueError: If AEID is invalid, projection type is invalid, or no data found
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox import AssayBioactivity
            >>> assay_client = AssayBioactivity()
            >>> 
            >>> # Get full assay data
            >>> full_data = assay_client.get_assay_data_by_aeid_with_projections(3032)
            >>> print(f"Assay: {full_data['assayComponentEndpointName']}")
            >>> print(f"Target: {full_data['intendedTargetFamily']}")
            >>> 
            >>> # Get only gene information
            >>> gene_data = assay_client.get_assay_data_by_aeid_with_projections(
            ...     3032, 
            ...     projection="ccd-assay-gene"
            ... )
            >>> for gene in gene_data if isinstance(gene_data, list) else [gene_data]:
            ...     print(f"{gene['geneSymbol']}: {gene['geneName']}")
            >>> 
            >>> # Get assay annotations
            >>> annotations = assay_client.get_assay_data_by_aeid_with_projections(
            ...     3032,
            ...     projection="ccd-assay-annotation"
            ... )
            >>> 
            >>> # Get citations
            >>> citations = assay_client.get_assay_data_by_aeid_with_projections(
            ...     3032,
            ...     projection="ccd-assay-citations"
            ... )
        """
        endpoint = f"bioactivity/assay/search/by-aeid/{aeid}"
        params = {"projection": projection} if projection else {}
        
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)
    
    def get_count_available_assays(self, use_cache: Optional[bool] = None) -> int:
        """
        Get count of all available assays in the database.
        
        Returns the total number of assay endpoints available in the CompTox
        ToxCast/Tox21 database.
        
        Returns:
            Integer count of available assays
        
        Raises:
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox import AssayBioactivity
            >>> assay_client = AssayBioactivity()
            >>> 
            >>> # Get total count of assays
            >>> count = assay_client.get_count_available_assays()
            >>> print(f"Total assays available: {count}")
        """
        endpoint = "bioactivity/assay/count"
        
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def get_list_of_dtxsids_by_aeid(
        self, 
        aeid: int,
        projection: str = "dtxsidsonly",
        use_cache: Optional[bool] = None
    ) -> Union[List[str], List[Dict[str, Any]]]:
        """
        Get list of DTXSIDs for chemicals tested in a specific assay.
        
        Retrieves all DSSTox substance identifiers (DTXSIDs) for chemicals
        that have been tested in the specified assay endpoint.
        
        Args:
            aeid: Assay Endpoint Identifier (AEID)
            projection: Data projection type (default: "dtxsidsonly")
        
        Returns:
            List of DTXSIDs (if projection is "dtxsidsonly") or list of 
            chemical data dictionaries (for other projections)
        
        Raises:
            ValueError: If AEID is invalid or no data found
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox import AssayBioactivity
            >>> assay_client = AssayBioactivity()
            >>> 
            >>> # Get list of chemicals tested in assay 3032
            >>> dtxsids = assay_client.get_list_of_dtxsids_by_aeid(3032)
            >>> print(f"Found {len(dtxsids)} chemicals tested")
            >>> 
            >>> # Use first few DTXSIDs for further analysis
            >>> for dtxsid in dtxsids[:5]:
            ...     print(dtxsid)
        """
        endpoint = f"bioactivity/assay/chemicals/search/by-aeid/{aeid}"
        params = {"projection": projection}
        
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)

    def get_all_assays(self, projection: str = "assay-all", use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get all assays from the ToxCast/Tox21 database.
        
        Retrieves comprehensive information for all assay endpoints in the database.
        This includes metadata about assay sources, components, endpoints, genes,
        citations, and analytical methods.
        
        Args:
            projection: Data projection type (default: "assay-all")
        
        Returns:
            List of assay dictionaries with extensive metadata
        
        Raises:
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox import AssayBioactivity
            >>> assay_client = AssayBioactivity()
            >>> all_assays = assay_client.get_all_assays()
            >>> print(f"Total assays: {len(all_assays)}")
        """
        endpoint = "bioactivity/assay/"
        params = {"projection": projection}
        
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)
    
    def get_assay_annotations_by_aeid_batch(
        self, 
        aeids: List[int],
        use_cache: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Get assay annotations for multiple assay endpoint IDs in batch.
        
        Retrieves comprehensive assay annotation data for a list of AEIDs in a 
        single request. More efficient than making individual requests when 
        querying multiple assays.
        
        Args:
            aeids: List of Assay Endpoint Identifiers (AEIDs) to query
        
        Returns:
            List of assay annotation dictionaries. Each contains:
                - aeid (int): Assay endpoint ID
                - assayComponentEndpointName (str): Endpoint name
                - assayComponentEndpointDesc (str): Endpoint description
                - assayComponentName (str): Component name
                - assayComponentDesc (str): Component description
                - assayName (str): Assay name
                - assayDesc (str): Assay description
                - intendedTargetFamily (str): Target family
                - intendedTargetType (str): Target type
                - biologicalProcessTarget (str): Biological process
                - detectionTechnology (str): Detection method
                - detectionTechnologyType (str): Detection technology type
                - assayDesignType (str): Assay design
                - assayFormatType (str): Assay format
                - organism (str): Test organism
                - tissue (str): Tissue type
                - cellFormat (str): Cell format
                - gene (list): List of gene dictionaries with symbols and descriptions
                - citations (list): List of publication citations
                - assayList (list): List of assay classifications
                - aid (int): Assay ID
                - acid (int): Assay component ID
                - asid (int): Assay source ID
                - organismId (int): Organism identifier
        
        Raises:
            ValueError: If AEIDs list is empty or invalid
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> from pycomptox import AssayBioactivity
            >>> assay_client = AssayBioactivity()
            >>> 
            >>> # Get annotations for multiple assays
            >>> aeids = [3032, 3033, 3034]
            >>> annotations = assay_client.get_assay_annotations_by_aeid_batch(aeids)
            >>> 
            >>> # Process each assay
            >>> for assay in annotations:
            ...     print(f"AEID {assay['aeid']}: {assay['assayComponentEndpointName']}")
            ...     print(f"  Target: {assay['intendedTargetFamily']}")
            ...     print(f"  Organism: {assay['organism']}")
            ...     
            ...     # Check for gene associations
            ...     if assay.get('gene'):
            ...         gene_symbols = [g['geneSymbol'] for g in assay['gene']]
            ...         print(f"  Genes: {', '.join(gene_symbols)}")
            >>> 
            >>> # Filter by target family
            >>> receptor_assays = [
            ...     a for a in annotations 
            ...     if 'receptor' in a.get('intendedTargetFamily', '').lower()
            ... ]
        
        Note:
            - Batch requests are more efficient than individual queries
            - Maximum recommended batch size is around 100 AEIDs
            - Results are returned in the same order as input AEIDs
            - This is a POST request that sends the AEID list in the request body
        """
        if not aeids:
            raise ValueError("AEIDs list cannot be empty")
        
        # Ensure all AEIDs are integers
        try:
            aeid_list = [int(aeid) for aeid in aeids]
        except (ValueError, TypeError) as e:
            raise ValueError(f"All AEIDs must be valid integers: {e}")
        
        endpoint = "bioactivity/assay/search/by-aeid/"
        
        # Use the base class _make_cached_request method which properly handles
        # URL construction, caching, rate limiting, and error handling
        data = self._make_cached_request(
            endpoint, 
            json=aeid_list, 
            method='POST', 
            use_cache=use_cache
        )
        
        if data is None or (isinstance(data, (list, dict)) and not data):
            raise ValueError("No data returned from API for provided AEIDs")
        
        return data
