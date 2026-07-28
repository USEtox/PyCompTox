from typing import List, Dict, Any, Optional, Literal
from ..base import CachedAPIClient


# Type alias for projection parameter
ProjectionType = Literal[
    "chemicaldetailstandard",
    "chemicalidentifier", 
    "chemicalstructure",
    "ntatoolkit",
    "ccdchemicaldetails",
    "ccdassaydetails",
    "chemicaldetailall",
    "compact"
]


class ChemicalDetails(CachedAPIClient):
    """
    A class for retrieving detailed chemical information from the CompTox Dashboard API.
    
    This class provides methods to get comprehensive chemical data including:
    - Chemical identifiers and names
    - Chemical structures (SMILES, InChI)
    - Physical and chemical properties
    - Assay information
    - Related data sources
    
    Attributes:
        api_key (str): The API key for accessing the CompTox Dashboard API.
        base_url (str): The base URL for the CompTox API.
        session (requests.Session): A requests session for making API calls.
        time_delay_between_calls (float): Minimum time delay (in seconds) between API calls.
        _last_call_time (float): Timestamp of the last API call.
        use_cache (bool): Whether to use caching by default.
    """
    
    def get_data_by_dtxsid_batch(
        self, 
        dtxsids: List[str],
        projection: Optional[ProjectionType] = None,
        use_cache: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Get detailed data for a batch of DTXSIDs.
        
        POST /chemical/detail/search/by-dtxsid/
        Besides batch of the values, the user can also define projection (set of attributes to return).
        Maximum 1000 DTXSIDs per request.
        
        Example:
            curl -X POST "https://comptox.epa.gov/ctx-api/chemical/detail/search/by-dtxsid/" \\
                -H 'accept: application/json'\\
                -H 'content-type: application/json' \\
                -d '["DTXSID7020182"]' 
        
        Args:
            dtxsids (List[str]): List of DSSTox Substance Identifiers. Maximum 1000 per request.
            projection (ProjectionType, optional): Set of attributes to return. Options:
                - "chemicaldetailstandard": Standard chemical details
                - "chemicalidentifier": Chemical identifiers only
                - "chemicalstructure": Structure information
                - "ntatoolkit": NTA toolkit attributes
                - "ccdchemicaldetails": CCD chemical details
                - "ccdassaydetails": CCD assay details
                - "chemicaldetailall": All chemical details (default)
                - "compact": Compact format
        
        Returns:
            List[Dict[str, Any]]: List of chemical detail records. Each record may contain:
                - id, preferredName, molFormula, casrn, dtxsid, dtxcid
                - smiles, msReadySmiles, qsarReadySmiles
                - inchiString, inchikey, iupacName
                - activeAssays, totalAssays, percentAssays
                - pubchemCid, pubchemCount, pubmedCount
                - monoisotopicMass, averageMass
                - And many more fields depending on projection
        
        Raises:
            ValueError: If more than 1000 DTXSIDs provided or request is invalid.
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> details = ChemicalDetails()
            >>> dtxsids = ["DTXSID7020182", "DTXSID2021315"]
            >>> results = details.get_data_by_dtxsid_batch(dtxsids)
            >>> for chem in results:
            ...     print(f"{chem['preferredName']}: {chem['casrn']}")
            
            >>> # With specific projection
            >>> results = details.get_data_by_dtxsid_batch(dtxsids, projection="chemicalidentifier")
        """
        if len(dtxsids) > 1000:
            raise ValueError("Maximum 1000 DTXSIDs are allowed per batch request")
        
        if not dtxsids:
            raise ValueError("At least one DTXSID must be provided")
        
        endpoint = "chemical/detail/search/by-dtxsid/"
        params = {}
        if projection:
            params['projection'] = projection
        
        return self._make_cached_request(endpoint, method='POST', json=dtxsids, params=params, use_cache=use_cache)

    def get_data_by_dtxcid_batch(
        self, 
        dtxcids: List[str],
        projection: Optional[ProjectionType] = None,
        use_cache: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Get detailed data for a batch of DTXCIDs.
        
        POST /chemical/detail/search/by-dtxcid/
        Besides batch of the values, the user can also define projection (set of attributes to return).
        Maximum 1000 DTXCIDs per request.
        
        Example:
            curl -X POST "https://comptox.epa.gov/ctx-api/chemical/detail/search/by-dtxcid/" \\
                -H 'accept: application/json'\\
                -H 'content-type: application/json' \\
                -d '["DTXCID505"]' 

        RESPONSE
        200 OK
        example: {
            "id": "string",
            "preferredName": "string",
            "activeAssays": 0,
            "cpdataCount": 0,
            "molFormula": "string",
            "percentAssays": 0,
            "compoundId": 0,
            "pubchemCount": 0,
            "totalAssays": 0,
            "qcLevelDesc": "string",
            "toxcastSelect": "string",
            "isMarkush": false,
            "pprtvLink": "string",
            "sourcesCount": 0,
            "irisLink": "string",
            "multicomponent": 0,
            "msReadySmiles": "string",
            "iupacName": "string",
            "inchiString": "string",
            "pubchemCid": 0,
            "inchikey": "string",
            "pubmedCount": 0,
            "qsarReadySmiles": "string",
            "smiles": "string",
            "isotope": 0,
            "qcNotes": "string",
            "dtxcid": "string",
            "qcLevel": 0,
            "dtxsid": "string",
            "casrn": "string",
            "genericSubstanceId": 0,
            "wikipediaArticle": "string",
            "relatedSubstanceCount": 0,
            "hasStructureImage": 0,
            "monoisotopicMass": 0,
            "descriptorStringTsv": "string",
            "relatedStructureCount": 0
            }
        400: When user has submitted more than allowed number (1000) of DTXCID(s).
        
        Args:
            dtxcids (List[str]): List of DSSTox Compound Identifiers. Maximum 1000 per request.
            projection (ProjectionType, optional): Set of attributes to return. Same options as get_data_by_dtxsid_batch.
        
        Returns:
            List[Dict[str, Any]]: List of chemical detail records with same structure as get_data_by_dtxsid_batch.
        
        Raises:
            ValueError: If more than 1000 DTXCIDs provided or request is invalid.
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> details = ChemicalDetails()
            >>> dtxcids = ["DTXCID505", "DTXCID30182"]
            >>> results = details.get_data_by_dtxcid_batch(dtxcids)
            >>> for chem in results:
            ...     print(f"{chem['preferredName']}: {chem['molFormula']}")
        """
        if len(dtxcids) > 1000:
            raise ValueError("Maximum 1000 DTXCIDs are allowed per batch request")
        
        if not dtxcids:
            raise ValueError("At least one DTXCID must be provided")
        
        endpoint = "chemical/detail/search/by-dtxcid/"
        params = {}
        if projection:
            params['projection'] = projection
        
        return self._make_cached_request(endpoint, method='POST', json=dtxcids, params=params, use_cache=use_cache)

    def get_data_by_dtxsid(self, dtxsid: str, projection: Optional[ProjectionType] = None, use_cache: Optional[bool] = None) -> Dict[str, Any]:
        """
        Get detailed data by DTXSID.
        
        GET /chemical/detail/search/by-dtxsid/{dtxsid}
        Specify the dtxsid as part of the path, and optionally define projection (set of attributes to return).
        
        Example:
            curl -X GET "https://comptox.epa.gov/ctx-api/chemical/detail/search/by-dtxsid/DTXSID7020182" \\
                -H 'accept: application/json' 
        
        RESPONSE
        200 OK
        example1: {
            "id": "string",
            "preferredName": "string",
            "activeAssays": 0,
            "cpdataCount": 0,
            "molFormula": "string",
            "percentAssays": 0,
            "compoundId": 0,
            "pubchemCount": 0,
            "totalAssays": 0,
            "qcLevelDesc": "string",
            "toxcastSelect": "string",
            "isMarkush": false,
            "pprtvLink": "string",
            "sourcesCount": 0,
            "irisLink": "string",
            "multicomponent": 0,
            "msReadySmiles": "string",
            "iupacName": "string",
            "inchiString": "string",
            "pubchemCid": 0,
            "inchikey": "string",
            "pubmedCount": 0,
            "qsarReadySmiles": "string",
            "smiles": "string",
            "isotope": 0,
            "qcNotes": "string",
            "dtxcid": "string",
            "qcLevel": 0,
            "dtxsid": "string",
            "casrn": "string",
            "genericSubstanceId": 0,
            "wikipediaArticle": "string",
            "relatedSubstanceCount": 0,
            "hasStructureImage": 0,
            "monoisotopicMass": 0,
            "descriptorStringTsv": "string",
            "relatedStructureCount": 0
            }
        example2: {
            "preferredName": "string",
            "iupacName": "string",
            "inchikey": "string",
            "dtxcid": "string",
            "dtxsid": "string",
            "casrn": "string"
            }
        example3: {
            "id": "string",
            "preferredName": "string",
            "msReadySmiles": "string",
            "inchiString": "string",
            "inchikey": "string",
            "qsarReadySmiles": "string",
            "smiles": "string",
            "dtxcid": "string",
            "dtxsid": "string",
            "casrn": "string",
            "hasStructureImage": 0
            }
        
        Args:
            dtxsid (str): DSSTox Substance Identifier (e.g., "DTXSID7020182").
            projection (ProjectionType, optional): Set of attributes to return. Default: "chemicaldetailall".
                Options:
                - "chemicaldetailstandard": Standard chemical details
                - "chemicalidentifier": Identifiers only (preferredName, iupacName, inchikey, dtxcid, dtxsid, casrn)
                - "chemicalstructure": Structure info (smiles, InChI, hasStructureImage, etc.)
                - "ntatoolkit": NTA toolkit attributes
                - "ccdchemicaldetails": CCD chemical details with properties
                - "ccdassaydetails": CCD assay details
                - "chemicaldetailall": All available attributes (default)
                - "compact": Compact format
        
        Returns:
            Dict[str, Any]: Chemical detail record with fields depending on projection.
        
        Raises:
            ValueError: If DTXSID is not found or request is invalid.
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> details = ChemicalDetails()
            >>> # Get all details
            >>> data = details.get_data_by_dtxsid("DTXSID7020182")
            >>> print(f"{data['preferredName']}: {data['casrn']}")
            >>> print(f"Formula: {data['molFormula']}")
            >>> print(f"SMILES: {data['smiles']}")
            
            >>> # Get only identifiers
            >>> data = details.get_data_by_dtxsid("DTXSID7020182", projection="chemicalidentifier")
            >>> print(f"{data['preferredName']}: {data['dtxcid']}")
        """
        endpoint = f"chemical/detail/search/by-dtxsid/{dtxsid}"
        params = {}
        if projection:
            params['projection'] = projection
        
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)

    def get_data_by_dtxcid(self, dtxcid: str, projection: Optional[ProjectionType] = None, use_cache: Optional[bool] = None) -> Dict[str, Any]:
        """
        Get data by dtxcid
        get /chemical/detail/search/by-dtxcid/{dtxcid}
        Specify the dtxcid as part of the path, and optionally user can also define projection (set of attributes to return).
        PATH PARAMETERS
        dtxcid string
        QUERY-STRING PARAMETERS
        projection enum
        Default: chemicaldetailall
        Allowed: chemicaldetailstandard ┃ chemicalidentifier ┃ chemicalstructure ┃ ntatoolkit ┃ ccdchemicaldetails ┃ ccdassaydetails ┃ chemicaldetailall ┃ compact

        curl -X GET "https://comptox.epa.gov/ctx-api/chemical/detail/search/by-dtxcid/DTXCID505" \
            -H 'accept: application/json' 

        RESPONSE
        200 OK
        example1:{
            "id": "string",
            "preferredName": "string",
            "activeAssays": 0,
            "cpdataCount": 0,
            "molFormula": "string",
            "percentAssays": 0,
            "compoundId": 0,
            "pubchemCount": 0,
            "totalAssays": 0,
            "qcLevelDesc": "string",
            "toxcastSelect": "string",
            "isMarkush": false,
            "pprtvLink": "string",
            "sourcesCount": 0,
            "irisLink": "string",
            "multicomponent": 0,
            "msReadySmiles": "string",
            "iupacName": "string",
            "inchiString": "string",
            "pubchemCid": 0,
            "inchikey": "string",
            "pubmedCount": 0,
            "qsarReadySmiles": "string",
            "smiles": "string",
            "isotope": 0,
            "qcNotes": "string",
            "dtxcid": "string",
            "qcLevel": 0,
            "dtxsid": "string",
            "casrn": "string",
            "genericSubstanceId": 0,
            "wikipediaArticle": "string",
            "relatedSubstanceCount": 0,
            "hasStructureImage": 0,
            "monoisotopicMass": 0,
            "descriptorStringTsv": "string",
            "relatedStructureCount": 0
            }
        example2: {
            "preferredName": "string",
            "iupacName": "string",
            "inchikey": "string",
            "dtxcid": "string",
            "dtxsid": "string",
            "casrn": "string"
            }
        example3: {
            "id": "string",
            "preferredName": "string",
            "msReadySmiles": "string",
            "inchiString": "string",
            "inchikey": "string",
            "qsarReadySmiles": "string",
            "smiles": "string",
            "dtxcid": "string",
            "dtxsid": "string",
            "casrn": "string",
            "hasStructureImage": 0
            }
        example4:{
            "id": "string",
            "preferredName": "string",
            "activeAssays": 0,
            "cpdataCount": 0,
            "molFormula": "string",
            "percentAssays": 0,
            "compoundId": 0,
            "pubchemCount": 0,
            "averageMass": 0,
            "totalAssays": 0,
            "qcLevelDesc": "string",
            "toxcastSelect": "string",
            "isMarkush": false,
            "pprtvLink": "string",
            "sourcesCount": 0,
            "irisLink": "string",
            "multicomponent": 0,
            "msReadySmiles": "string",
            "iupacName": "string",
            "inchiString": "string",
            "pubchemCid": 0,
            "inchikey": "string",
            "pubmedCount": 0,
            "qsarReadySmiles": "string",
            "smiles": "string",
            "stereo": "string",
            "isotope": 0,
            "qcNotes": "string",
            "dtxcid": "string",
            "qcLevel": 0,
            "dtxsid": "string",
            "casrn": "string",
            "genericSubstanceId": 0,
            "wikipediaArticle": "string",
            "relatedSubstanceCount": 0,
            "hasStructureImage": 0,
            "monoisotopicMass": 0,
            "descriptorStringTsv": "string",
            "relatedStructureCount": 0,
            "hrFatheadMinnow": 0,
            "hrDiphniaLc50": 0,
            "pkabOperaPred": 0,
            "surfaceTension": 0,
            "toxvalData": "string",
            "devtoxTestPred": 0,
            "henrysLawAtm": 0,
            "oralRatLd50Mol": 0,
            "pkaaOperaPred": 0,
            "expocat": "string",
            "density": 0,
            "nhanes": "string",
            "operaKmDaysOperaPred": 0,
            "waterSolubilityOpera": 0,
            "octanolWaterPartition": 0,
            "waterSolubilityTest": 0,
            "flashPointDegcTestPred": 0,
            "expocatMedianPrediction": "string",
            "viscosityCpCpTestPred": 0,
            "thermalConductivity": 0,
            "tetrahymenaPyriformis": 0,
            "biodegradationHalfLifeDays": 0,
            "vaporPressureMmhgOperaPred": 0,
            "atmosphericHydroxylationRate": 0,
            "bioconcentrationFactorOperaPred": 0,
            "octanolAirPartitionCoeff": 0,
            "meltingPointDegcOperaPred": 0,
            "soilAdsorptionCoefficient": 0,
            "bioconcentrationFactorTestPred": 0,
            "boilingPointDegcOperaPred": 0,
            "meltingPointDegcTestPred": 0,
            "vaporPressureMmhgTestPred": 0,
            "amesMutagenicityTestPred": 0,
            "boilingPointDegcTestPred": 0
            }
        example5: 
        All attributes use for NTA Informatics Toolkit.
        {
            "preferredName": "string",
            "activeAssays": 0,
            "cpdataCount": 0,
            "molFormula": "string",
            "percentAssays": 0,
            "totalAssays": 0,
            "sourcesCount": 0,
            "msReadySmiles": "string",
            "inchikey": "string",
            "smiles": "string",
            "dtxcid": "string",
            "dtxsid": "string",
            "casrn": "string",
            "monoisotopicMass": 0,
            "expocat": "string",
            "nhanes": "string",
            "expocatMedianPrediction": "string"
            }
        
        Args:
            dtxcid (str): DSSTox Compound Identifier (e.g., "DTXCID505").
            projection (ProjectionType, optional): Set of attributes to return. Same options as get_data_by_dtxsid.
        
        Returns:
            Dict[str, Any]: Chemical detail record with fields depending on projection.
        
        Raises:
            ValueError: If DTXCID is not found or request is invalid.
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Example:
            >>> details = ChemicalDetails()
            >>> # Get all details including predicted properties
            >>> data = details.get_data_by_dtxcid("DTXCID505", projection="ccdchemicaldetails")
            >>> print(f"{data['preferredName']}")
            >>> print(f"Boiling Point: {data.get('boilingPointDegcOperaPred', 'N/A')}")
            >>> print(f"Water Solubility: {data.get('waterSolubilityOpera', 'N/A')}")
        """
        endpoint = f"chemical/detail/search/by-dtxcid/{dtxcid}"
        params = {}
        if projection:
            params['projection'] = projection
        
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)

    def get_all_chemical_details(
        self,
        next_page: int = 1,
        projection: Optional[str] = None,
        use_cache: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Find all chemical details (paginated).
        
        GET /chemical/all
        Returns all chemical details. Results are paginated.
        
        Example:
            curl -X GET "https://comptox.epa.gov/ctx-api/chemical/all" \\
                    -H 'accept: application/json' 
        
        Args:
            next_page (int, optional): Page number for pagination. Default: 1.
            projection (str, optional): Specifies if projection is used. 
                Option: "all-ids" returns only id, dtxcid, and dtxsid.
                If omitted, the default ChemicalDetailStandard2 data is returned.
        
        Returns:
            List[Dict[str, Any]]: List of chemical records. Each record contains:
                Without projection (ChemicalDetailStandard2):
                - id, preferredName, molFormula, averageMass
                - qcLevelDesc, iupacName, inchiString, inchikey
                - smiles, qcLevel, dtxsid, casrn, monoisotopicMass
                
                With projection="all-ids":
                - id, dtxcid, dtxsid
        
        Raises:
            ValueError: If request is invalid.
            AuthenticationError: If the API key is missing, invalid, or lacks access.
            NotFoundError: If the requested identifier does not exist.
            RateLimitError: If the API rate limit is exceeded.
            APIError: For any other unsuccessful API response.
        
        Warning:
            This endpoint returns large amounts of data. Use with caution and consider
            pagination. The API may return thousands of chemicals.
        
        Example:
            >>> details = ChemicalDetails()
            >>> # Get first page of all chemicals
            >>> chemicals = details.get_all_chemical_details(next_page=1)
            >>> print(f"Retrieved {len(chemicals)} chemicals")
            
            >>> # Get only IDs (lighter payload)
            >>> ids = details.get_all_chemical_details(projection="all-ids")
            >>> for chem in ids[:10]:
            ...     print(f"{chem['dtxsid']}: {chem['dtxcid']}")
        """
        endpoint = "chemical/all"
        params: Dict[str, Any] = {'next': next_page}
        if projection:
            params['projection'] = projection
        
        return self._make_cached_request(endpoint, params=params, use_cache=use_cache)