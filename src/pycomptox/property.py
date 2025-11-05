"""
Chemical Properties API client for EPA CompTox Dashboard.

This module provides access to chemical property data including:
- Property summaries (physchem and environmental fate)
- Predicted properties (QSAR models)
- Experimental properties (measured data)
- Environmental fate and transport properties

Author: PyCompTox Contributors
License: MIT
"""

import os
import time
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urljoin

from .config import load_api_key


class ChemicalProperties:
    """
    Client for accessing chemical property data from EPA CompTox Dashboard.
    
    This class provides methods for retrieving:
    - Property summaries (physchem and fate)
    - Predicted properties from QSAR models
    - Experimental property measurements
    - Environmental fate and transport data
    
    Args:
        api_key (str, optional): CompTox API key. If not provided, will attempt
            to load from saved configuration or COMPTOX_API_KEY environment variable.
        base_url (str): Base URL for the CompTox API. Defaults to EPA's endpoint.
        time_delay_between_calls (float): Delay in seconds between API calls for
            rate limiting. Default is 0.0 (no delay).
    
    Example:
        >>> from pycomptox import ChemicalProperties
        >>> props = ChemicalProperties()
        >>> 
        >>> # Get property summary for Bisphenol A
        >>> summary = props.get_property_summary_by_dtxsid("DTXSID7020182")
        >>> 
        >>> # Get experimental properties
        >>> exp_props = props.get_experimental_properties_by_dtxsid("DTXSID7020182")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://comptox.epa.gov/ctx-api",
        time_delay_between_calls: float = 0.0
    ):
        """Initialize the ChemicalProperties client."""
        # Load API key from parameter, config file, or environment
        self.api_key = api_key or load_api_key()
        if not self.api_key:
            raise ValueError(
                "API key is required. Either pass it as a parameter, "
                "set COMPTOX_API_KEY environment variable, or save it using "
                "save_api_key() function."
            )
        
        # Ensure base_url ends with / for proper urljoin behavior with relative paths
        self.base_url = base_url.rstrip('/') + '/'
        self.time_delay_between_calls = time_delay_between_calls
        self._last_call_time = 0.0
        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'application/json',
            'x-api-key': self.api_key
        })
    
    def _enforce_rate_limit(self):
        """Enforce rate limiting between API calls."""
        if self.time_delay_between_calls > 0:
            elapsed = time.time() - self._last_call_time
            if elapsed < self.time_delay_between_calls:
                time.sleep(self.time_delay_between_calls - elapsed)
        self._last_call_time = time.time()
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Any] = None
    ) -> Any:
        """
        Make an HTTP request to the CompTox API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body for POST requests
            
        Returns:
            Response data (dict, list, or str)
            
        Raises:
            ValueError: For invalid requests (400)
            PermissionError: For unauthorized requests (401)
            RuntimeError: For other HTTP errors
        """
        self._enforce_rate_limit()
        
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                raise ValueError(f"Bad request: {response.text}")
            elif response.status_code == 401:
                raise PermissionError("Invalid API key or unauthorized access")
            elif response.status_code == 404:
                raise ValueError(f"Resource not found: {endpoint}")
            elif response.status_code == 429:
                raise RuntimeError("Rate limit exceeded. Please slow down requests.")
            else:
                raise RuntimeError(
                    f"Request failed with status {response.status_code}: {response.text}"
                )
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Network error: {str(e)}")

    def get_property_summary_by_dtxsid(self, dtxsid: str) -> List[Dict[str, Any]]:
        """
        Get physicochemical property summary by DTXSID.
        
        Returns a summary of predicted and experimental property values including
        ranges, medians, and averages for various physicochemical properties.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., "DTXSID7020182")
            
        Returns:
            List of dictionaries containing property summaries with fields:
                - propName: Property name
                - unit: Unit of measurement
                - predictedRange: Range of predicted values
                - predictedMedian: Median predicted value
                - predictedAverage: Average predicted value
                - experimentalRange: Range of experimental values
                - experimentalMedian: Median experimental value
                - experimentalAverage: Average experimental value
                
        Example:
            >>> props = ChemicalProperties()
            >>> summary = props.get_property_summary_by_dtxsid("DTXSID7020182")
            >>> for prop in summary:
            ...     print(f"{prop['propName']}: {prop.get('experimentalMedian', 'N/A')}")
        """
        endpoint = f"chemical/property/summary/search/by-dtxsid/{dtxsid}"
        return self._make_request("GET", endpoint)

    def get_summary_by_dtxsid_and_property(
        self, 
        dtxsid: str, 
        property_name: str
    ) -> Dict[str, Any]:
        """
        Get physicochemical property summary for a specific property and chemical.
        
        Args:
            dtxsid: DSSTox Substance Identifier
            property_name: Name of the property (e.g., "Boiling Point", "Melting Point")
            
        Returns:
            Dictionary containing summary for the specified property with fields:
                - propName: Property name
                - unit: Unit of measurement
                - predictedRange: Range of predicted values
                - predictedMedian: Median predicted value
                - predictedAverage: Average predicted value
                - experimentalRange: Range of experimental values
                - experimentalMedian: Median experimental value
                - experimentalAverage: Average experimental value
                
        Example:
            >>> props = ChemicalProperties()
            >>> bp_summary = props.get_summary_by_dtxsid_and_property(
            ...     "DTXSID7020182", 
            ...     "Boiling Point"
            ... )
            >>> print(f"Boiling Point: {bp_summary.get('experimentalMedian')} {bp_summary.get('unit')}")
        """
        endpoint = "chemical/property/summary/search/"
        params = {
            "dtxsid": dtxsid,
            "propName": property_name
        }
        return self._make_request("GET", endpoint, params=params)

    def get_predicted_property_by_name_and_range(
        self, 
        property_name: str, 
        min_value: float, 
        max_value: float
    ) -> List[Dict[str, Any]]:
        """
        Get chemicals with predicted property values within a specified range.
        
        Search for chemicals where a specific predicted property falls within
        the given range. Useful for finding chemicals with desired characteristics.
        
        Args:
            property_name: Property identifier/name
            min_value: Minimum value of the range (inclusive)
            max_value: Maximum value of the range (inclusive)
            
        Returns:
            List of dictionaries containing predicted property data with fields:
                - id: Property record ID
                - dtxsid: DSSTox Substance Identifier
                - dtxcid: DSSTox Compound Identifier
                - smiles: SMILES notation
                - canonQsarSmiles: Canonical QSAR-ready SMILES
                - propName: Property name
                - propCategory: Property category
                - propDescription: Property description
                - modelName: Prediction model name
                - modelId: Model identifier
                - propValue: Predicted value
                - propUnit: Unit of measurement
                - propValueString: Value as string
                - adMethod: Applicability domain method
                - adConclusion: AD conclusion
                - hasQmrf: Has QMRF documentation
                - And more fields...
                
        Example:
            >>> props = ChemicalProperties()
            >>> # Find chemicals with log P between 2 and 4
            >>> results = props.get_predicted_property_by_name_and_range(
            ...     "Log P", 2.0, 4.0
            ... )
            >>> for chem in results[:5]:
            ...     print(f"{chem['dtxsid']}: {chem['propValue']}")
        """
        endpoint = f"chemical/property/predicted/search/by-range/{property_name}/{min_value}/{max_value}"
        return self._make_request("GET", endpoint)

    def get_predicted_properties_by_dtxsid(self, dtxsid: str) -> List[Dict[str, Any]]:
        """
        Get all predicted (QSAR) properties for a chemical by DTXSID.
        
        Returns all available predicted property values from various QSAR models
        for the specified chemical.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., "DTXSID7020182")
            
        Returns:
            List of dictionaries containing predicted property data. Each entry includes:
                - dtxsid: DSSTox Substance Identifier
                - dtxcid: DSSTox Compound Identifier
                - propName: Property name
                - propValue: Predicted value
                - propUnit: Unit of measurement
                - modelName: Name of prediction model
                - modelId: Model identifier
                - adConclusion: Applicability domain conclusion
                - hasQmrf: Whether QMRF documentation exists
                - And more fields...
                
        Example:
            >>> props = ChemicalProperties()
            >>> predicted = props.get_predicted_properties_by_dtxsid("DTXSID7020182")
            >>> for prop in predicted:
            ...     print(f"{prop['propName']}: {prop['propValue']} {prop.get('propUnit', '')}")
        """
        endpoint = f"chemical/property/predicted/search/by-dtxsid/{dtxsid}"
        return self._make_request("GET", endpoint)

    def get_predicted_property_names(self) -> List[Dict[str, str]]:
        """
        Get list of all available predicted property names.
        
        Returns a list of all property names that have predicted (QSAR) values
        in the database. Useful for discovering what properties can be queried.
        
        Returns:
            List of dictionaries with 'propertyName' field
            
        Example:
            >>> props = ChemicalProperties()
            >>> prop_names = props.get_predicted_property_names()
            >>> print(f"Available properties: {len(prop_names)}")
            >>> for prop in prop_names[:10]:
            ...     print(f"  - {prop['propertyName']}")
        """
        endpoint = "chemical/property/predicted/name"
        return self._make_request("GET", endpoint)

    def get_experimental_properties_by_name_and_range(
        self, 
        property_name: str, 
        min_value: float, 
        max_value: float
    ) -> List[Dict[str, Any]]:
        """
        Get chemicals with experimental property values within a specified range.
        
        Search for chemicals where a specific experimental (measured) property
        falls within the given range.
        
        Args:
            property_name: Property name (e.g., "Boiling Point", "Melting Point")
            min_value: Minimum value of the range (inclusive)
            max_value: Maximum value of the range (inclusive)
            
        Returns:
            List of dictionaries containing experimental property data with fields:
                - id: Property record ID
                - dtxsid: DSSTox Substance Identifier
                - dtxcid: DSSTox Compound Identifier
                - smiles: SMILES notation
                - propName: Property name
                - propValue: Measured value
                - propUnit: Unit of measurement
                - propValueOriginal: Original reported value
                - sourceName: Data source name
                - lsCitation: Literature citation
                - briefCitation: Brief citation
                - expDetailsPh: pH conditions
                - expDetailsTemperatureC: Temperature in Celsius
                - expDetailsPressureMmhg: Pressure in mmHg
                - publicSourceUrl: URL to public source
                - And more fields...
                
        Example:
            >>> props = ChemicalProperties()
            >>> # Find chemicals with boiling point between 100-200°C
            >>> results = props.get_experimental_properties_by_name_and_range(
            ...     "Boiling Point", 100.0, 200.0
            ... )
            >>> for chem in results[:5]:
            ...     print(f"{chem['dtxsid']}: {chem['propValue']} {chem['propUnit']}")
        """
        endpoint = f"chemical/property/experimental/search/by-range/{property_name}/{min_value}/{max_value}"
        return self._make_request("GET", endpoint)

    def get_experimental_properties_by_dtxsid(self, dtxsid: str) -> List[Dict[str, Any]]:
        """
        Get all experimental (measured) properties for a chemical by DTXSID.
        
        Returns all available experimental property measurements from various
        data sources for the specified chemical.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., "DTXSID7020182")
            
        Returns:
            List of dictionaries containing experimental property data. Each entry includes:
                - dtxsid: DSSTox Substance Identifier
                - propName: Property name
                - propValue: Measured value
                - propUnit: Unit of measurement
                - sourceName: Data source
                - lsCitation: Literature citation
                - expDetailsTemperatureC: Temperature conditions
                - expDetailsPh: pH conditions
                - publicSourceUrl: URL to data source
                - And more fields...
                
        Example:
            >>> props = ChemicalProperties()
            >>> exp_props = props.get_experimental_properties_by_dtxsid("DTXSID7020182")
            >>> for prop in exp_props:
            ...     print(f"{prop['propName']}: {prop['propValue']} {prop.get('propUnit', '')}")
            ...     print(f"  Source: {prop.get('sourceName', 'N/A')}")
        """
        endpoint = f"chemical/property/experimental/search/by-dtxsid/{dtxsid}"
        return self._make_request("GET", endpoint)

    def get_all_experimental_property_names(self) -> List[Dict[str, str]]:
        """
        Get list of all available experimental property names.
        
        Returns a list of all property names that have experimental (measured)
        values in the database. Useful for discovering what properties can be queried.
        
        Returns:
            List of dictionaries with 'propertyName' field
            
        Example:
            >>> props = ChemicalProperties()
            >>> exp_names = props.get_all_experimental_property_names()
            >>> print(f"Available experimental properties: {len(exp_names)}")
            >>> for prop in exp_names[:10]:
            ...     print(f"  - {prop['propertyName']}")
        """
        endpoint = "chemical/property/experimental/name"
        return self._make_request("GET", endpoint)

    def get_fate_summary_by_dtxsid(self, dtxsid: str) -> List[Dict[str, Any]]:
        """
        Get environmental fate and transport property summary by DTXSID.
        
        Returns a summary of predicted and experimental environmental fate
        properties including ranges, medians, and averages.
        
        Args:
            dtxsid: DSSTox Substance Identifier (e.g., "DTXSID7020182")
            
        Returns:
            List of dictionaries containing fate property summaries with fields:
                - propName: Property name
                - unit: Unit of measurement
                - predictedRange: Range of predicted values
                - predictedMedian: Median predicted value
                - predictedAverage: Average predicted value
                - experimentalRange: Range of experimental values
                - experimentalMedian: Median experimental value
                - experimentalAverage: Average experimental value
                
        Example:
            >>> props = ChemicalProperties()
            >>> fate = props.get_fate_summary_by_dtxsid("DTXSID7020182")
            >>> for prop in fate:
            ...     print(f"{prop['propName']}: {prop.get('predictedMedian', 'N/A')} {prop.get('unit', '')}")
        """
        endpoint = f"chemical/fate/summary/search/by-dtxsid/{dtxsid}"
        return self._make_request("GET", endpoint)

    def get_fate_summary_by_dtxsid_and_property(
        self, 
        dtxsid: str, 
        property_name: str
    ) -> Dict[str, Any]:
        """
        Get environmental fate property summary for a specific property and chemical.
        
        Args:
            dtxsid: DSSTox Substance Identifier
            property_name: Name of the fate/transport property
            
        Returns:
            Dictionary containing summary for the specified fate property with fields:
                - propName: Property name
                - unit: Unit of measurement
                - predictedRange: Range of predicted values
                - predictedMedian: Median predicted value
                - predictedAverage: Average predicted value
                - experimentalRange: Range of experimental values
                - experimentalMedian: Median experimental value
                - experimentalAverage: Average experimental value
                
        Example:
            >>> props = ChemicalProperties()
            >>> koc = props.get_fate_summary_by_dtxsid_and_property(
            ...     "DTXSID7020182", 
            ...     "Koc"
            ... )
            >>> print(f"Koc: {koc.get('predictedMedian')} {koc.get('unit')}")
        """
        endpoint = "chemical/fate/summary/search/"
        params = {
            "dtxsid": dtxsid,
            "propName": property_name
        }
        return self._make_request("GET", endpoint, params=params)

    def get_predicted_properties_by_dtxsid_batch(
        self, 
        dtxsids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Get predicted properties for multiple chemicals in a single request.
        
        Batch retrieval of predicted (QSAR) properties for up to 1000 chemicals.
        More efficient than making individual requests.
        
        Args:
            dtxsids: List of DSSTox Substance Identifiers (max 1000)
            
        Returns:
            List of dictionaries containing predicted property data for all
            requested chemicals. Each entry includes the same fields as
            get_predicted_properties_by_dtxsid().
            
        Raises:
            ValueError: If more than 1000 DTXSIDs are provided
            
        Example:
            >>> props = ChemicalProperties()
            >>> dtxsids = ["DTXSID7020182", "DTXSID0020232", "DTXSID5020108"]
            >>> batch_props = props.get_predicted_properties_by_dtxsid_batch(dtxsids)
            >>> 
            >>> # Group by chemical
            >>> by_chemical = {}
            >>> for prop in batch_props:
            ...     dtxsid = prop['dtxsid']
            ...     if dtxsid not in by_chemical:
            ...         by_chemical[dtxsid] = []
            ...     by_chemical[dtxsid].append(prop)
            >>> 
            >>> for dtxsid, properties in by_chemical.items():
            ...     print(f"{dtxsid}: {len(properties)} properties")
        """
        if len(dtxsids) > 1000:
            raise ValueError(f"Maximum 1000 DTXSIDs allowed, got {len(dtxsids)}")
        
        endpoint = "chemical/property/predicted/search/by-dtxsid/"
        return self._make_request("POST", endpoint, json_data=dtxsids)

    def get_experimental_properties_by_dtxsid_batch(
        self, 
        dtxsids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Get experimental properties for multiple chemicals in a single request.
        
        Batch retrieval of experimental (measured) properties for up to 1000 chemicals.
        More efficient than making individual requests.
        
        Args:
            dtxsids: List of DSSTox Substance Identifiers (max 1000)
            
        Returns:
            List of dictionaries containing experimental property data for all
            requested chemicals. Each entry includes the same fields as
            get_experimental_properties_by_dtxsid().
            
        Raises:
            ValueError: If more than 1000 DTXSIDs are provided
            
        Example:
            >>> props = ChemicalProperties()
            >>> dtxsids = ["DTXSID7020182", "DTXSID0020232", "DTXSID5020108"]
            >>> batch_props = props.get_experimental_properties_by_dtxsid_batch(dtxsids)
            >>> 
            >>> # Group by chemical
            >>> by_chemical = {}
            >>> for prop in batch_props:
            ...     dtxsid = prop['dtxsid']
            ...     if dtxsid not in by_chemical:
            ...         by_chemical[dtxsid] = []
            ...     by_chemical[dtxsid].append(prop)
            >>> 
            >>> for dtxsid, properties in by_chemical.items():
            ...     print(f"{dtxsid}: {len(properties)} experimental properties")
        """
        if len(dtxsids) > 1000:
            raise ValueError(f"Maximum 1000 DTXSIDs allowed, got {len(dtxsids)}")
        
        endpoint = "chemical/property/experimental/search/by-dtxsid/"
        return self._make_request("POST", endpoint, json_data=dtxsids)

    def get_fate_by_dtxsid_batch(
        self, 
        dtxsids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Get environmental fate properties for multiple chemicals in a single request.
        
        Batch retrieval of environmental fate and transport properties for
        up to 1000 chemicals. More efficient than making individual requests.
        
        Args:
            dtxsids: List of DSSTox Substance Identifiers (max 1000)
            
        Returns:
            List of dictionaries containing fate property data for all
            requested chemicals. Each entry includes similar fields as
            experimental properties (propName, propValue, propUnit, etc.)
            
        Raises:
            ValueError: If more than 1000 DTXSIDs are provided
            
        Example:
            >>> props = ChemicalProperties()
            >>> dtxsids = ["DTXSID7020182", "DTXSID0020232", "DTXSID5020108"]
            >>> fate_props = props.get_fate_by_dtxsid_batch(dtxsids)
            >>> 
            >>> # Group by chemical
            >>> by_chemical = {}
            >>> for prop in fate_props:
            ...     dtxsid = prop['dtxsid']
            ...     if dtxsid not in by_chemical:
            ...         by_chemical[dtxsid] = []
            ...     by_chemical[dtxsid].append(prop)
            >>> 
            >>> for dtxsid, properties in by_chemical.items():
            ...     print(f"{dtxsid}: {len(properties)} fate properties")
        """
        if len(dtxsids) > 1000:
            raise ValueError(f"Maximum 1000 DTXSIDs allowed, got {len(dtxsids)}")
        
        endpoint = "chemical/fate/search/by-dtxsid/"
        return self._make_request("POST", endpoint, json_data=dtxsids)