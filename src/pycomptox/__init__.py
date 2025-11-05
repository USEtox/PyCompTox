"""
PyCompTox - A Python interface to the CompTox Dashboard Chemical API

This package provides a Python interface for interacting with the EPA's 
CompTox Dashboard Chemical API, allowing you to search and retrieve chemical 
information programmatically.
"""

from .search import Chemical
from .details import ChemicalDetails
from .property import ChemicalProperties
from .config import (
    save_api_key,
    load_api_key,
    delete_api_key,
    get_config_info,
    get_config_dir
)

__version__ = "0.3.0"
__all__ = [
    "Chemical",
    "ChemicalDetails",
    "ChemicalProperties",
    "save_api_key",
    "load_api_key",
    "delete_api_key",
    "get_config_info",
    "get_config_dir"
]
