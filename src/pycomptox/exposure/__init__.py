"""
Exposure Module

This module provides classes for accessing exposure-related data from the EPA CompTox Dashboard,
including exposure predictions, functional use, product data, list presence, and environmental monitoring.

Available Classes:
    - ExposurePrediction: Get general exposure predictions (SEEM methodology)
    - DemographicExposure: Get demographic-specific exposure predictions
    - FunctionalUse: Access functional use categories and probabilities
    - ProductData: Get consumer product composition data
    - CCDData: Access Chemical and Products Categories data
    - ListPresence: Check chemical presence in regulatory/screening lists
    - HTTKData: Get High-Throughput Toxicokinetics parameters
    - MMDB: Access Molecular Modeling Database (environmental monitoring)

Example:
    >>> from pycomptox import exposure
    >>> # Get exposure predictions
    >>> exp_pred = exposure.ExposurePrediction()
    >>> predictions = exp_pred.get_general_seem_prediction_by_dtxsid("DTXSID0020232")
    >>> 
    >>> # Get functional use data
    >>> func_use = exposure.FunctionalUse()
    >>> uses = func_use.get_functional_use_by_dtxsid("DTXSID0020232")
    >>> 
    >>> # Check list presence
    >>> lists = exposure.ListPresence()
    >>> presence = lists.get_list_presence_data_by_dtxsid("DTXSID0020232")
"""

from .ccddata import CCDData
from .mmdb import MMDB
from .functionaluse import FunctionalUse
from .productdata import ProductData
from .httkdata import HTTKData
from .listpresence import ListPresence
from .exposureprediction import ExposurePrediction
from .demographicexposure import DemographicExposure

__all__ = [
    "CCDData",
    "MMDB",
    "FunctionalUse",
    "ProductData",
    "HTTKData",
    "ListPresence",
    "ExposurePrediction",
    "DemographicExposure",
]
