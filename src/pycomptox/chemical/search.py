import requests
import time
from typing import List, Dict, Any, Optional
from urllib.parse import quote
from ..base import CachedAPIClient


class Chemical(CachedAPIClient):
    """
    A class for interacting with the CompTox Dashboard Chemical Search API.
    
    This class provides methods to search for chemicals using various criteria
    including name, identifiers, formulas, and mass ranges.
    
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
        time_delay_between_calls: float = 0.0,
        **kwargs
    ):
        """
        Initialize the Chemical search client.
        
        Args:
            api_key (str, optional): The API key for accessing the CompTox Dashboard API.
                If not provided, the function will attempt to load it from:
                1. COMPTOX_API_KEY environment variable
                2. Saved configuration file (use save_api_key() to set)
            base_url (str, optional): The base URL for the API. 
                Defaults to "https://comptox.epa.gov/ctx-api".
            time_delay_between_calls (float, optional): Minimum time delay (in seconds) 
                between consecutive API calls. Defaults to 0.0 (no delay).
                Set this to a positive value if rate limiting becomes necessary.
            **kwargs: Additional arguments for CachedAPIClient (cache_manager, use_cache)
                
        Raises:
            ValueError: If no API key is provided and none can be loaded.
            
        Example:
            >>> # Using a provided API key
            >>> client = Chemical(api_key="your_api_key")
            
            >>> # Using saved API key (after calling save_api_key())
            >>> client = Chemical()
            
            >>> # With rate limiting
            >>> client = Chemical(time_delay_between_calls=0.5)  # 0.5 second delay
        """
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            time_delay_between_calls=time_delay_between_calls,
            **kwargs
        )

    def search_by_starting_value(self, value: str, use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Search chemicals where name/identifier starts with the given value.
        
        GET /chemical/search/start-with/{word}
        NOTE: Search value needs to be URL encoded for synonyms
        
        Example:
            curl -X GET "https://comptox.epa.gov/ctx-api/chemical/search/start-with/DTXSID7020182" \\
            -H 'accept: application/json' 
        
        Args:
            value (str): The starting value to search for (e.g., chemical name, DTXSID, CAS number).
        
        Returns:
            List[Dict[str, Any]]: A list of chemical records matching the search criteria.
                Each record contains:
                - `preferredName` (str): The preferred chemical name
                - `isMarkush` (bool): Whether the chemical is a Markush structure
                - `searchName` (str): The name field that matched
                - `searchValue` (str): The value that was matched
                - `smiles` (str): The SMILES notation
                - `dtxcid` (str): The DSSTox Compound ID
                - `dtxsid` (str): The DSSTox Substance ID
                - `casrn` (str): The CAS Registry Number
                - `rank` (int): The search result ranking
                - hasStructureImage (int): Whether a structure image is available
        
        Raises:
            ValueError: If no data is found or the request is invalid.
            RuntimeError: If the API request fails.
        
        Example:
            >>> client = Chemical(api_key="your_api_key")
            >>> results = client.search_by_starting_value("DTXSID7020182")
            >>> print(results[0].get("preferredName"))
        """
        encoded_value = quote(value, safe='')
        endpoint = f"/chemical/search/start-with/{encoded_value}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def search_by_exact_value(self, value: str, use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Search chemicals by exact name/identifier match.
        
        GET /chemical/search/equal/{word}
        NOTE: Search value needs to be URL encoded for synonyms
        
        Example:
            curl -X GET "https://comptox.epa.gov/ctx-api/chemical/search/equal/DTXSID7020182" \\
                -H 'accept: application/json' 
        
        Args:
            value (str): The exact value to search for (e.g., chemical name, DTXSID, CAS number).
        
        Returns:
            List[Dict[str, Any]]: A list of chemical records that exactly match the search value.
                Each record contains the same fields as search_by_starting_value.
        
        Raises:
            ValueError: If no data is found or the request is invalid.
            RuntimeError: If the API request fails.
        
        Example:
            >>> client = Chemical(api_key="your_api_key")
            >>> results = client.search_by_exact_value("Bisphenol A")
            >>> print(results[0].get("dtxsid"))
        """
        encoded_value = quote(value, safe='')
        endpoint = f"/chemical/search/equal/{encoded_value}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def search_by_substring_value(self, value: str, use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Search chemicals where name/identifier contains the given substring.
        
        GET /chemical/search/contain/{word}
        NOTE: Search value needs to be URL encoded for synonyms
        
        Example:
            curl -X GET "https://comptox.epa.gov/ctx-api/chemical/search/contain/DTXCID505" \\
                -H 'accept: application/json' 
        
        Args:
            value (str): The substring to search for within chemical names/identifiers.
        
        Returns:
            List[Dict[str, Any]]: A list of chemical records containing the search substring.
                Each record contains the same fields as search_by_starting_value.
        
        Raises:
            ValueError: If no data is found or the request is invalid.
            RuntimeError: If the API request fails.
        
        Example:
            >>> client = Chemical(api_key="your_api_key")
            >>> results = client.search_by_substring_value("phenol")
            >>> for chem in results[:5]:
            ...     print(chem['preferredName'])
        """
        encoded_value = quote(value, safe='')
        endpoint = f"/chemical/search/contain/{encoded_value}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def search_by_msready_formula(self, formula: str, use_cache: Optional[bool] = None) -> List[str]:
        """
        Search chemicals by MS-ready molecular formula.
        
        GET /chemical/search/by-msready-formula/{formula}
        MS-ready formulas exclude certain atoms/groups that are not typically observed in mass spectrometry.
        
        Example:
            curl -X GET "https://comptox.epa.gov/ctx-api/chemical/search/by-msready-formula/C15H16O2" \\
                -H 'accept: application/json' 
        
        Args:
            formula (str): The MS-ready molecular formula (e.g., "C15H16O2").
        
        Returns:
            List[str]: A list of DTXSID identifiers for chemicals matching the formula.
        
        Raises:
            ValueError: If no data is found or the formula is invalid.
            RuntimeError: If the API request fails.
        
        Example:
            >>> client = Chemical(api_key="your_api_key")
            >>> dtxsids = client.search_by_msready_formula("C15H16O2")
            >>> print(f"Found {len(dtxsids)} chemicals with MS-ready formula C15H16O2")
        """
        encoded_formula = quote(formula, safe='')
        endpoint = f"/chemical/search/by-msready-formula/{encoded_formula}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def search_by_exact_formula(self, formula: str, use_cache: Optional[bool] = None) -> List[str]:
        """
        Search chemicals by exact molecular formula.
        
        GET /chemical/search/by-exact-formula/{formula}
        Searches for chemicals with the exact molecular formula (including all atoms).
        
        Example:
            curl -X GET "https://comptox.epa.gov/ctx-api/chemical/search/by-exact-formula/C15H16O2" \\
                    -H 'accept: application/json' 
        
        Args:
            formula (str): The exact molecular formula (e.g., "C15H16O2").
        
        Returns:
            List[str]: A list of DTXSID identifiers for chemicals matching the exact formula.
        
        Raises:
            ValueError: If no data is found or the formula is invalid.
            RuntimeError: If the API request fails.
        
        Example:
            >>> client = Chemical(api_key="your_api_key")
            >>> dtxsids = client.search_by_exact_formula("C15H16O2")
            >>> print(f"Found {len(dtxsids)} chemicals with exact formula C15H16O2")
        """
        encoded_formula = quote(formula, safe='')
        endpoint = f"/chemical/search/by-formula/{encoded_formula}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def search_ms_ready_by_mass_range(self, min_mass: float, max_mass: float, use_cache: Optional[bool] = None) -> List[str]:
        """
        Search MS-ready chemicals within a mass range.
        
        GET /chemical/msready/search/by-mass/{start}/{end}
        Searches for MS-ready chemicals with molecular mass between min_mass and max_mass.
        
        Example:
            curl -X GET "https://comptox.epa.gov/ctx-api/chemical/msready/search/by-mass/200.9/200.95" \\
                -H 'accept: application/json' 
        
        Args:
            min_mass (float): The minimum molecular mass.
            max_mass (float): The maximum molecular mass.
        
        Returns:
            List[str]: A list of DTXSID identifiers for MS-ready chemicals in the mass range.
        
        Raises:
            ValueError: If the mass range is invalid or no data is found.
            RuntimeError: If the API request fails.
        
        Example:
            >>> client = Chemical(api_key="your_api_key")
            >>> dtxsids = client.search_ms_ready_by_mass_range(200.9, 200.95)
            >>> print(f"Found {len(dtxsids)} MS-ready chemicals in mass range")
        """
        endpoint = f"/chemical/msready/search/by-mass/{min_mass}/{max_mass}"
        return self._make_request(endpoint)

    def search_ms_ready_by_formula(self, formula: str, use_cache: Optional[bool] = None) -> List[str]:
        """
        Search MS-ready chemicals by molecular formula.
        
        GET /chemical/msready/search/by-formula/{formula}
        Specifically searches for MS-ready chemicals with the given formula.
        
        Example:
            curl -X GET "https://comptox.epa.gov/ctx-api/chemical/msready/search/by-formula/C16H24N2O5S" \\
                        -H 'accept: application/json' 
        
        Args:
            formula (str): The molecular formula (e.g., "C16H24N2O5S").
        
        Returns:
            List[str]: A list of DTXSID identifiers for MS-ready chemicals matching the formula.
        
        Raises:
            ValueError: If the formula is invalid or no data is found.
            RuntimeError: If the API request fails.
        
        Example:
            >>> client = Chemical(api_key="your_api_key")
            >>> dtxsids = client.search_ms_ready_by_formula("C16H24N2O5S")
            >>> print(f"Found {len(dtxsids)} MS-ready chemicals")
        """
        encoded_formula = quote(formula, safe='')
        endpoint = f"/chemical/msready/search/by-formula/{encoded_formula}"
        return self._make_request(endpoint)

    def search_ms_ready_by_dtxcid(self, dtxcid: str, use_cache: Optional[bool] = None) -> List[str]:
        """
        Search MS-ready chemicals by DTXCID.
        
        GET /chemical/msready/search/by-dtxcid/{dtxcid}
        Returns MS-ready version(s) of a chemical identified by DTXCID.
        
        Example:
            curl -X GET "https://comptox.epa.gov/ctx-api/chemical/msready/search/by-dtxcid/DTXCID30182" \\
                    -H 'accept: application/json' 
        
        Args:
            dtxcid (str): The DSSTox Compound ID (e.g., "DTXCID30182").
        
        Returns:
            List[str]: A list of MS-ready DTXSID identifiers related to the given DTXCID.
        
        Raises:
            ValueError: If the DTXCID is invalid or no data is found.
            RuntimeError: If the API request fails.
        
        Example:
            >>> client = Chemical(api_key="your_api_key")
            >>> dtxsids = client.search_ms_ready_by_dtxcid("DTXCID30182")
            >>> print(f"Found {len(dtxsids)} MS-ready forms")
        """
        endpoint = f"/chemical/msready/search/by-dtxcid/{dtxcid}"
        return self._make_cached_request(endpoint, use_cache=use_cache)

    def search_chemical_count_by_ms_ready_formula(self, formula: str, use_cache: Optional[bool] = None) -> int:
        """
        Get the count of chemicals with a given MS-ready formula.
        
        GET /chemical/count/by-msready-formula/{formula}
        Returns the number of chemicals that have the specified MS-ready formula.
        
        Example:
            curl -X GET "https://comptox.epa.gov/ctx-api/chemical/count/by-msready-formula/C15H16O2" \\
                -H 'accept: application/hal+json' 
        
        Args:
            formula (str): The MS-ready molecular formula (e.g., "C15H16O2").
        
        Returns:
            int: The count of chemicals with the given MS-ready formula.
        
        Raises:
            ValueError: If the formula is invalid or no data is found.
            RuntimeError: If the API request fails.
        
        Example:
            >>> client = Chemical(api_key="your_api_key")
            >>> count = client.search_chemical_count_by_ms_ready_formula("C15H16O2")
            >>> print(f"There are {count} chemicals with MS-ready formula C15H16O2")
        """
        encoded_formula = quote(formula, safe='')
        endpoint = f"/chemical/count/by-msready-formula/{encoded_formula}"
        result = self._make_cached_request(endpoint, use_cache=use_cache)
        # The API might return a dict with a count field or just a number
        return result if isinstance(result, int) else result.get('count', 0)

    def search_chemical_count_by_exact_formula(self, formula: str, use_cache: Optional[bool] = None) -> int:
        """
        Get the count of chemicals with a given exact formula.
        
        GET /chemical/count/by-exact-formula/{formula}
        Returns the number of chemicals that have the specified exact molecular formula.
        
        Example:
            curl -X GET "https://comptox.epa.gov/ctx-api/chemical/count/by-exact-formula/C15H16O2" \\
                -H 'accept: application/hal+json' 
        
        Args:
            formula (str): The exact molecular formula (e.g., "C15H16O2").
        
        Returns:
            int: The count of chemicals with the given exact formula.
        
        Raises:
            ValueError: If the formula is invalid or no data is found.
            RuntimeError: If the API request fails.
        
        Example:
            >>> client = Chemical(api_key="your_api_key")
            >>> count = client.search_chemical_count_by_exact_formula("C15H16O2")
            >>> print(f"There are {count} chemicals with exact formula C15H16O2")
        """
        encoded_formula = quote(formula, safe='')
        endpoint = f"/chemical/count/by-exact-formula/{encoded_formula}"
        result = self._make_cached_request(endpoint, use_cache=use_cache)
        # The API might return a dict with a count field or just a number
        return result if isinstance(result, int) else result.get('count', 0)
    
    def search_by_exact_batch_values(self, values: List[str], use_cache: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Search by exact batch of values.
        
        POST /chemical/search/equal/
        NOTE: Search batch of values (values are separated by newline and maximum 200 values are allowed).
        
        Example:
            curl -X POST "https://comptox.epa.gov/ctx-api/chemical/search/equal/" \\
                -H 'accept: application/json'\\
                -H 'content-type: application/json' \\
                -d '"Bisphenol A\\nDTXSID7020182\\n80-05-7"' 
        
        Args:
            values (List[str]): A list of search values (chemical names, DTXSID, CAS numbers, etc.).
                Maximum 200 values are allowed per batch.
        
        Returns:
            List[Dict[str, Any]]: A list of chemical records matching the search values.
                Each record contains:
                - dtxsid (str): The DSSTox Substance ID
                - dtxcid (str): The DSSTox Compound ID
                - casrn (str): The CAS Registry Number
                - smiles (str): The SMILES notation
                - preferredName (str): The preferred chemical name
                - searchName (str): The name field that matched
                - searchValue (str): The value that was matched
                - rank (int): The search result ranking
                - hasStructureImage (int): Whether a structure image is available
                - isMarkush (bool): Whether the chemical is a Markush structure
                - searchMsgs (List[str]): Search messages
                - suggestions (List[str]): Alternative suggestions
                - isDuplicate (bool): Whether this is a duplicate result
        
        Raises:
            ValueError: If more than 200 values are provided, or no data is found.
            RuntimeError: If the API request fails.
        
        Example:
            >>> client = Chemical(api_key="your_api_key")
            >>> values = ["Bisphenol A", "DTXSID7020182", "80-05-7"]
            >>> results = client.search_by_exact_batch_values(values)
            >>> for result in results:
            ...     print(f"{result['preferredName']} - {result['dtxsid']}")
        """
        if len(values) > 200:
            raise ValueError("Maximum 200 values are allowed per batch search")
        
        if not values:
            raise ValueError("At least one value must be provided")
        
        # The API expects a JSON string with newline-separated values
        request_body = "\\n".join(values)
        
        endpoint = "/chemical/search/equal/"
        result = self._make_cached_request(endpoint, method='POST', json=request_body, use_cache=use_cache)
        
        # Ensure we always return a list
        if isinstance(result, list):
            return result
        elif isinstance(result, dict):
            return [result]
        else:
            return []

    def search_ms_ready_by_mass_range_batch(
        self, 
        masses: List[float], 
        error: float = 0.005,
        use_cache: Optional[bool] = None
    ) -> Dict[str, List[str]]:
        """
        Search MS-ready chemicals using batch of mass ranges.
        
        POST /chemical/msready/search/by-mass/
        Searches for MS-ready chemicals matching multiple masses with a given error tolerance.
        
        Example:
            curl -X POST "https://comptox.epa.gov/ctx-api/chemical/msready/search/by-mass/" \\
            -H 'accept: application/json'\\
            -H 'content-type: application/json' \\
            -d '{"masses":[0],"error":0}' 
        
        Args:
            masses (List[float]): A list of molecular masses to search for.
            error (float, optional): The mass error tolerance. Defaults to 0.005.
        
        Returns:
            Dict[str, List[str]]: A dictionary where keys are mass values (as strings)
                and values are lists of DTXSID identifiers matching that mass.
        
        Raises:
            ValueError: If no masses are provided or the request is invalid.
            RuntimeError: If the API request fails.
        
        Example:
            >>> client = Chemical(api_key="your_api_key")
            >>> masses = [200.9, 250.5, 300.2]
            >>> results = client.search_ms_ready_by_mass_range_batch(masses, error=0.01)
            >>> for mass, dtxsids in results.items():
            ...     print(f"Mass {mass}: {len(dtxsids)} chemicals found")
        """
        if not masses:
            raise ValueError("At least one mass value must be provided")
        
        request_body = {
            "masses": masses,
            "error": error
        }
        
        endpoint = "/chemical/msready/search/by-mass/"
        return self._make_cached_request(endpoint, method='POST', json=request_body, use_cache=use_cache)

    def search_ms_ready_by_dtxcid_batch(self, dtxcids: List[str], use_cache: Optional[bool] = None) -> Any:
        """
        Search MS-ready chemicals by batch of DTXCIDs.
        
        POST /chemical/msready/search/by-dtxcid/
        Returns MS-ready version(s) for multiple chemicals identified by their DTXCIDs.
        
        Example:
            curl -X POST "https://comptox.epa.gov/ctx-api/chemical/msready/search/by-dtxcid/" \\
                -H 'accept: application/json'\\
                -H 'content-type: application/json' \\
                -d '["DTXCID30182","DTXCID20182"]' 
        
        Args:
            dtxcids (List[str]): A list of DSSTox Compound IDs (e.g., ["DTXCID30182", "DTXCID40123"]).
        
        Returns:
            Any: The API response. This could be:
                - A dictionary mapping DTXCIDs to MS-ready forms
                - A list of results
                The exact format depends on the API response.
        
        Raises:
            ValueError: If no DTXCIDs are provided or the request is invalid.
            RuntimeError: If the API request fails.
        
        Example:
            >>> client = Chemical(api_key="your_api_key")
            >>> dtxcids = ["DTXCID30182", "DTXCID40123", "DTXCID50456"]
            >>> results = client.search_ms_ready_by_dtxcid_batch(dtxcids)
            >>> print(f"Results type: {type(results)}")
            >>> # Process based on actual response structure
        """
        if not dtxcids:
            raise ValueError("At least one DTXCID must be provided")
        
        endpoint = "/chemical/msready/search/by-dtxcid/"
        return self._make_cached_request(endpoint, method='POST', json=dtxcids, use_cache=use_cache)
