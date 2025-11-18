"""
Chemical Module

This module provides classes for accessing chemical-related data from the EPA CompTox Dashboard,
including chemical search, properties, details, synonyms, and external links.

Available Classes:
    - Chemical: Search for chemicals by name, CAS, or identifier
    - ChemicalDetails: Get detailed chemical information
    - ChemicalProperties: Retrieve chemical properties (MW, LogP, etc.)
    - ChemSynonym: Access chemical synonyms and alternative names
    - ChemicalList: Work with curated chemical lists
    - ExtraData: Get additional chemical data
    - WikiLink: Access Wikipedia links for chemicals
    - PubChemLink: Get PubChem database links

Example:
    >>> from pycomptox import chemical
    >>> # Search for a chemical
    >>> chem = chemical.Chemical()
    >>> results = chem.search_by_name("caffeine")
    >>> 
    >>> # Get properties
    >>> props = chemical.ChemicalProperties()
    >>> data = props.retrieve_properties_by_dtxsid(results[0]['dtxsid'])
"""

from .search import Chemical
from .details import ChemicalDetails
from .property import ChemicalProperties
from .extradata import ExtraData
from .wikilink import WikiLink
from .pubchemlink import PubChemLink
from .chemlist import ChemicalList
from .chemsynonym import ChemSynonym

__all__ = [
    "Chemical",
    "ChemicalDetails",
    "ChemicalProperties",
    "ExtraData",
    "WikiLink",
    "PubChemLink",
    "ChemicalList",
    "ChemSynonym",
]
