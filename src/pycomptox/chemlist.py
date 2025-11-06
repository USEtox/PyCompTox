"""
Chemical Lists Module

This module provides access to the CompTox Dashboard Chemical Lists API.
"""

from typing import List, Dict, Any, Optional, Literal
import requests
import time


ProjectionType = Literal[
    "chemicallistall",
    "chemicallistwithdtxsids", 
    "chemicallistname",
    "ccdchemicaldetaillists"
]


class ChemicalList:
    """Client for accessing Chemical List information from the CompTox Dashboard API."""
    
    def __init__(self, api_key=None, rate_limit_delay=0.5, base_url="https://comptox.epa.gov/ctx-api"):
        self.base_url = base_url.rstrip("/")
        self.rate_limit_delay = rate_limit_delay
        self._last_call_time = 0
        
        if api_key:
            self.api_key = api_key
        else:
            from pycomptox.config import load_api_key
            self.api_key = load_api_key()
        
        self.session = requests.Session()
        self.session.headers.update({"accept": "application/json", "Content-Type": "application/json"})
        if self.api_key:
            self.session.headers["x-api-key"] = self.api_key
    
    def _enforce_rate_limit(self):
        if self.rate_limit_delay > 0:
            elapsed = time.time() - self._last_call_time
            if elapsed < self.rate_limit_delay:
                time.sleep(self.rate_limit_delay - elapsed)
        self._last_call_time = time.time()
    
    def _make_request(self, method, endpoint, **kwargs):
        self._enforce_rate_limit()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise RuntimeError(f"API request failed: {e}")

    def get_all_list_types(self):
        return self._make_request("GET", "chemical/list/type")

    def get_public_lists_by_type(self, list_type, projection="chemicallistall"):
        if not list_type:
            raise ValueError("list_type must be a non-empty string")
        endpoint = f"chemical/list/search/by-type/{list_type}"
        return self._make_request("GET", endpoint, params={"projection": projection})

    def get_public_lists_by_name(self, name):
        if not name:
            raise ValueError("name must be a non-empty string")
        return self._make_request("GET", f"chemical/list/search/by-name/{name}")

    def get_public_lists_by_dtxsid(self, dtxsid):
        if not dtxsid:
            raise ValueError("dtxsid must be a non-empty string")
        return self._make_request("GET", f"chemical/list/search/by-dtxsid/{dtxsid}")

    def get_dtxsids_by_listname_chem_name_start(self, list_name, chem_name_start):
        if not list_name:
            raise ValueError("list_name must be a non-empty string")
        if not chem_name_start:
            raise ValueError("chem_name_start must be a non-empty string")
        return self._make_request("GET", f"chemical/list/search/{list_name}/by-start/{chem_name_start}")

    def get_dtxsids_by_listname_chem_name_exact(self, list_name, chem_name_exact):
        if not list_name:
            raise ValueError("list_name must be a non-empty string")
        if not chem_name_exact:
            raise ValueError("chem_name_exact must be a non-empty string")
        return self._make_request("GET", f"chemical/list/search/{list_name}/by-equal/{chem_name_exact}")

    def get_dtxsids_by_listname_chem_name_contains(self, list_name, chem_name_contains):
        if not list_name:
            raise ValueError("list_name must be a non-empty string")
        if not chem_name_contains:
            raise ValueError("chem_name_contains must be a non-empty string")
        return self._make_request("GET", f"chemical/list/search/{list_name}/by-contain/{chem_name_contains}")

    def get_dtxsids_by_listname_specific(self, list_name):
        if not list_name:
            raise ValueError("list_name must be a non-empty string")
        return self._make_request("GET", f"chemical/list/{list_name}")

    def get_all_public_lists(self, projection="chemicallistall"):
        return self._make_request("GET", "chemical/list/", params={"projection": projection})
