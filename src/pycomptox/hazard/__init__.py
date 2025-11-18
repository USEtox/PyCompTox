"""
Hazard Module

This module provides classes for accessing hazard-related data from the EPA CompTox Dashboard.

Available Classes:
    - PPRTV: Access to Provisional Peer-Reviewed Toxicity Values
    - ToxValDBCancer: Access to cancer hazard identification and WoE data
    - ToxRefDBEffects: Access to ToxRefDB dose-effect data
    - ToxRefDBSummary: Access to ToxRefDB study-level summaries
    - ToxRefDBBatch: Batch access to ToxRefDB data for multiple chemicals
    - ToxValDBSkinEye: Access to skin and eye irritation test data
    - ToxValDB: Access to comprehensive toxicity values database
    - HAWC: Access to EPA Health Assessment Workspace Collaborative links
    - IRIS: Access to EPA Integrated Risk Information System assessments
    - ToxValDBGenetox: Access to genotoxicity test data (Ames, Comet, micronucleus, chromosomal aberration)
    - ToxRefDBData: Access to extracted dose-treatment group-effect information from ToxRefDB
    - ADMEIVIVE: Access to ADME-IVIVE toxicokinetics data (in vitro, in vivo, in silico)
    - ToxRefDBObservation: Access to ToxRefDB observations and endpoint observation status

Planned functionality:
    - Additional hazard characterization data
    - Toxicity reference values from other sources
    - Hazard classifications
    - Risk assessment data
"""

from .pprtv import PPRTV
from .toxvaldbcancer import ToxValDBCancer
from .toxrefdbeffects import ToxRefDBEffects
from .toxrefdbsummary import ToxRefDBSummary
from .toxrefdbbatch import ToxRefDBBatch
from .toxvaldbskineye import ToxValDBSkinEye
from .toxvaldb import ToxValDB
from .hawc import HAWC
from .iris import IRIS
from .toxvaldbgenetox import ToxValDBGenetox
from .toxrefdbdata import ToxRefDBData
from .admeivive import ADMEIVIVE
from .toxrefdbobservation import ToxRefDBObservation

__all__ = [
    'PPRTV',
    'ToxValDBCancer',
    'ToxRefDBEffects',
    'ToxRefDBSummary',
    'ToxRefDBBatch',
    'ToxValDBSkinEye',
    'ToxValDB',
    'HAWC',
    'IRIS',
    'ToxValDBGenetox',
    'ToxRefDBData',
    'ADMEIVIVE',
    'ToxRefDBObservation'
]
