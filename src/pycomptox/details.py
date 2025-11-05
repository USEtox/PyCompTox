import requests
import time
from typing import List, Dict, Any, Optional, Literal
from urllib.parse import quote
from .config import load_api_key


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


class ChemicalDetails:
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
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        base_url: str = "https://comptox.epa.gov/ctx-api",
        time_delay_between_calls: float = 0.0
    ):
        """
        Initialize the ChemicalDetails client.
        
        Args:
            api_key (str, optional): The API key for accessing the CompTox Dashboard API.
                If not provided, the function will attempt to load it from:
                1. COMPTOX_API_KEY environment variable
                2. Saved configuration file (use save_api_key() to set)
            base_url (str, optional): The base URL for the API. 
                Defaults to "https://comptox.epa.gov/ctx-api".
            time_delay_between_calls (float, optional): Minimum time delay (in seconds) 
                between consecutive API calls. Defaults to 0.0 (no delay).
                
        Raises:
            ValueError: If no API key is provided and none can be loaded.
            
        Example:
            >>> # Using saved API key
            >>> client = ChemicalDetails()
            
            >>> # With explicit API key
            >>> client = ChemicalDetails(api_key="your_api_key")
            
            >>> # With rate limiting
            >>> client = ChemicalDetails(time_delay_between_calls=0.5)
        """
        # Load API key if not provided
        if api_key is None:
            api_key = load_api_key()
            if api_key is None:
                raise ValueError(
                    "No API key provided. Please either:\n"
                    "1. Pass api_key parameter: ChemicalDetails(api_key='your_key')\n"
                    "2. Set COMPTOX_API_KEY environment variable\n"
                    "3. Save key using: from pycomptox import save_api_key; save_api_key('your_key')"
                )
        
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.time_delay_between_calls = time_delay_between_calls
        self._last_call_time = 0.0
        
        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'application/json',
            'x-api-key': self.api_key
        })
    
    def _enforce_rate_limit(self) -> None:
        """
        Enforce rate limiting by pausing if necessary.
        
        This method checks the time since the last API call and pauses
        if the minimum delay hasn't elapsed yet.
        """
        if self.time_delay_between_calls > 0:
            current_time = time.time()
            time_since_last_call = current_time - self._last_call_time
            
            if time_since_last_call < self.time_delay_between_calls:
                sleep_time = self.time_delay_between_calls - time_since_last_call
                time.sleep(sleep_time)
    
    def _make_request(self, endpoint: str, method: str = 'GET', **kwargs) -> Any:
        """
        Make an API request to the CompTox Dashboard.
        
        This method automatically enforces rate limiting based on the
        time_delay_between_calls setting.
        
        Args:
            endpoint (str): The API endpoint path.
            method (str): The HTTP method (default: 'GET').
            **kwargs: Additional arguments to pass to requests.
            
        Returns:
            The JSON response from the API.
            
        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        # Enforce rate limiting before making the request
        self._enforce_rate_limit()
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Update last call time after successful request
            self._last_call_time = time.time()
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                raise ValueError(f"Data not found or invalid request: {e.response.text}")
            elif e.response.status_code == 401:
                raise PermissionError("Invalid API key or unauthorized access")
            elif e.response.status_code == 404:
                raise ValueError(f"Endpoint not found: {url}")
            elif e.response.status_code == 429:
                raise RuntimeError(
                    "Rate limit exceeded. Please increase time_delay_between_calls parameter."
                )
            else:
                raise
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")

    def data_by_dtxsid_batch(
        self, 
        dtxsids: List[str],
        projection: Optional[ProjectionType] = None
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
            RuntimeError: If the API request fails.
        
        Example:
            >>> details = ChemicalDetails()
            >>> dtxsids = ["DTXSID7020182", "DTXSID2021315"]
            >>> results = details.data_by_dtxsid_batch(dtxsids)
            >>> for chem in results:
            ...     print(f"{chem['preferredName']}: {chem['casrn']}")
            
            >>> # With specific projection
            >>> results = details.data_by_dtxsid_batch(dtxsids, projection="chemicalidentifier")
        """
        if len(dtxsids) > 1000:
            raise ValueError("Maximum 1000 DTXSIDs are allowed per batch request")
        
        if not dtxsids:
            raise ValueError("At least one DTXSID must be provided")
        
        endpoint = "/chemical/detail/search/by-dtxsid/"
        params = {}
        if projection:
            params['projection'] = projection
        
        return self._make_request(endpoint, method='POST', json=dtxsids, params=params)

    def data_by_dtxcid_batch(
        self, 
        dtxcids: List[str],
        projection: Optional[ProjectionType] = None
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
            projection (ProjectionType, optional): Set of attributes to return. Same options as data_by_dtxsid_batch.
        
        Returns:
            List[Dict[str, Any]]: List of chemical detail records with same structure as data_by_dtxsid_batch.
        
        Raises:
            ValueError: If more than 1000 DTXCIDs provided or request is invalid.
            RuntimeError: If the API request fails.
        
        Example:
            >>> details = ChemicalDetails()
            >>> dtxcids = ["DTXCID505", "DTXCID30182"]
            >>> results = details.data_by_dtxcid_batch(dtxcids)
            >>> for chem in results:
            ...     print(f"{chem['preferredName']}: {chem['molFormula']}")
        """
        if len(dtxcids) > 1000:
            raise ValueError("Maximum 1000 DTXCIDs are allowed per batch request")
        
        if not dtxcids:
            raise ValueError("At least one DTXCID must be provided")
        
        endpoint = "/chemical/detail/search/by-dtxcid/"
        params = {}
        if projection:
            params['projection'] = projection
        
        return self._make_request(endpoint, method='POST', json=dtxcids, params=params)

    def data_by_dtxsid(self, dtxsid: str, projection: Optional[ProjectionType] = None) -> Dict[str, Any]:
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
            RuntimeError: If the API request fails.
        
        Example:
            >>> details = ChemicalDetails()
            >>> # Get all details
            >>> data = details.data_by_dtxsid("DTXSID7020182")
            >>> print(f"{data['preferredName']}: {data['casrn']}")
            >>> print(f"Formula: {data['molFormula']}")
            >>> print(f"SMILES: {data['smiles']}")
            
            >>> # Get only identifiers
            >>> data = details.data_by_dtxsid("DTXSID7020182", projection="chemicalidentifier")
            >>> print(f"{data['preferredName']}: {data['dtxcid']}")
        """
        endpoint = f"/chemical/detail/search/by-dtxsid/{dtxsid}"
        params = {}
        if projection:
            params['projection'] = projection
        
        return self._make_request(endpoint, params=params)

    def data_by_dtxcid(self, dtxcid: str, projection: Optional[ProjectionType] = None) -> Dict[str, Any]:
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
            projection (ProjectionType, optional): Set of attributes to return. Same options as data_by_dtxsid.
        
        Returns:
            Dict[str, Any]: Chemical detail record with fields depending on projection.
        
        Raises:
            ValueError: If DTXCID is not found or request is invalid.
            RuntimeError: If the API request fails.
        
        Example:
            >>> details = ChemicalDetails()
            >>> # Get all details including predicted properties
            >>> data = details.data_by_dtxcid("DTXCID505", projection="ccdchemicaldetails")
            >>> print(f"{data['preferredName']}")
            >>> print(f"Boiling Point: {data.get('boilingPointDegcOperaPred', 'N/A')}")
            >>> print(f"Water Solubility: {data.get('waterSolubilityOpera', 'N/A')}")
        """
        endpoint = f"/chemical/detail/search/by-dtxcid/{dtxcid}"
        params = {}
        if projection:
            params['projection'] = projection
        
        return self._make_request(endpoint, params=params)

    def find_all_chemical_details(
        self,
        next_page: int = 1,
        projection: Optional[str] = None
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
            RuntimeError: If the API request fails.
        
        Warning:
            This endpoint returns large amounts of data. Use with caution and consider
            pagination. The API may return thousands of chemicals.
        
        Example:
            >>> details = ChemicalDetails()
            >>> # Get first page of all chemicals
            >>> chemicals = details.find_all_chemical_details(next_page=1)
            >>> print(f"Retrieved {len(chemicals)} chemicals")
            
            >>> # Get only IDs (lighter payload)
            >>> ids = details.find_all_chemical_details(projection="all-ids")
            >>> for chem in ids[:10]:
            ...     print(f"{chem['dtxsid']}: {chem['dtxcid']}")
        """
        endpoint = "/chemical/all"
        params = {'next': next_page}
        if projection:
            params['projection'] = projection
        
        return self._make_request(endpoint, params=params)