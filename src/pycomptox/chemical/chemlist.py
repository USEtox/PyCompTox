"""
Chemical Lists Module

This module provides access to the CompTox Dashboard Chemical Lists API.
"""

from typing import Optional, Literal
from ..base import CachedAPIClient


ProjectionType = Literal[
    "chemicallistall",
    "chemicallistwithdtxsids", 
    "chemicallistname",
    "ccdchemicaldetaillists"
]


class ChemicalList(CachedAPIClient):
    """Client for accessing Chemical List information from the CompTox Dashboard API."""

    #: List endpoints return large payloads; throttle by default.
    default_time_delay: float = 0.5
    
    def get_all_list_types(self, use_cache: Optional[bool] = None):
        return self._make_cached_request("chemical/list/type", use_cache=use_cache)

    def get_public_lists_by_type(self, list_type, projection="chemicallistall", use_cache: Optional[bool] = None):
        if not list_type:
            raise ValueError("list_type must be a non-empty string")
        endpoint = f"chemical/list/search/by-type/{list_type}"
        return self._make_cached_request(endpoint, params={"projection": projection}, use_cache=use_cache)

    def get_public_lists_by_name(self, name, use_cache: Optional[bool] = None):
        if not name:
            raise ValueError("name must be a non-empty string")
        return self._make_cached_request(f"chemical/list/search/by-name/{name}", use_cache=use_cache)

    def get_public_lists_by_dtxsid(self, dtxsid, use_cache: Optional[bool] = None):
        if not dtxsid:
            raise ValueError("dtxsid must be a non-empty string")
        return self._make_cached_request(f"chemical/list/search/by-dtxsid/{dtxsid}", use_cache=use_cache)

    def get_dtxsids_by_listname_chem_name_start(self, list_name, chem_name_start, use_cache: Optional[bool] = None):
        if not list_name:
            raise ValueError("list_name must be a non-empty string")
        if not chem_name_start:
            raise ValueError("chem_name_start must be a non-empty string")
        return self._make_cached_request(f"chemical/list/search/{list_name}/by-start/{chem_name_start}", use_cache=use_cache)

    def get_dtxsids_by_listname_chem_name_exact(self, list_name, chem_name_exact, use_cache: Optional[bool] = None):
        if not list_name:
            raise ValueError("list_name must be a non-empty string")
        if not chem_name_exact:
            raise ValueError("chem_name_exact must be a non-empty string")
        return self._make_cached_request(f"chemical/list/search/{list_name}/by-equal/{chem_name_exact}", use_cache=use_cache)

    def get_dtxsids_by_listname_chem_name_contains(self, list_name, chem_name_contains, use_cache: Optional[bool] = None):
        if not list_name:
            raise ValueError("list_name must be a non-empty string")
        if not chem_name_contains:
            raise ValueError("chem_name_contains must be a non-empty string")
        return self._make_cached_request(f"chemical/list/search/{list_name}/by-contain/{chem_name_contains}", use_cache=use_cache)

    def get_dtxsids_by_listname_specific(self, list_name, use_cache: Optional[bool] = None):
        if not list_name:
            raise ValueError("list_name must be a non-empty string")
        return self._make_cached_request(f"chemical/list/{list_name}", use_cache=use_cache)

    def get_all_public_lists(self, projection="chemicallistall", use_cache: Optional[bool] = None):
        return self._make_cached_request("chemical/list", params={"projection": projection}, use_cache=use_cache)

