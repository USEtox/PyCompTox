"""
Bioactivity Module

This module provides classes for accessing bioactivity and toxicity data from the EPA CompTox Dashboard,
including assay data, bioactivity models, analytical QC, and adverse outcome pathways.

Available Classes:
    - AssaySearch: Search for toxicity assays
    - AssayBioactivity: Get bioactivity data from assays
    - BioactivityModel: Access predictive bioactivity models
    - BioactivityData: Retrieve comprehensive bioactivity datasets
    - BioactivityAOP: Access Adverse Outcome Pathway (AOP) data
    - AnalyticalQC: Get analytical quality control data

Example:
    >>> from pycomptox import bioactivity
    >>> # Search for assays
    >>> assay = bioactivity.AssaySearch()
    >>> results = assay.search_by_chemical("DTXSID0020232")
    >>> 
    >>> # Get bioactivity data
    >>> bio_data = bioactivity.BioactivityData()
    >>> data = bio_data.get_bioactivity_summary("DTXSID0020232")
"""

from .assaysearch import AssaySearch
from .assaybioactivity import AssayBioactivity
from .bioactivitymodel import BioactivityModel
from .analyticalqc import AnalyticalQC
from .bioactivitydata import BioactivityData
from .bioactivityaop import BioactivityAOP

__all__ = [
    "AssaySearch",
    "AssayBioactivity",
    "BioactivityModel",
    "BioactivityData",
    "BioactivityAOP",
    "AnalyticalQC",
]
