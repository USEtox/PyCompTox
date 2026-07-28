"""
PyCompTox - A Python interface to the EPA CompTox Dashboard API.

This package provides typed clients for the EPA's CompTox Dashboard API,
covering chemical, hazard, exposure, and bioactivity data.

Clients are grouped into four subpackages, and every client is also re-exported
at the top level, so both of these work:

    >>> from pycomptox import Chemical              # flat
    >>> from pycomptox.chemical import Chemical     # grouped
    >>> from pycomptox import chemical              # module
    >>> chem = chemical.Chemical()

Getting started:

    >>> from pycomptox import save_api_key, Chemical
    >>> save_api_key("your_api_key")          # once per machine
    >>> client = Chemical()
    >>> results = client.search_by_exact_value("Bisphenol A")
    >>> print(results[0]["dtxsid"])
    DTXSID7020182

An API key can also come from the ``COMPTOX_API_KEY`` environment variable, or
be set from the shell with ``pycomptox-setup set YOUR_API_KEY``.

Response caching is available but **off by default**. Enable it per client or
per call:

    >>> client = Chemical(use_cache=True)
    >>> client.search_by_exact_value("Bisphenol A", use_cache=True)
"""

from . import bioactivity, chemical, exposure, hazard
from .bioactivity import (
    AnalyticalQC,
    AssayBioactivity,
    AssaySearch,
    BioactivityAOP,
    BioactivityData,
    BioactivityModel,
)
from .cache import (
    CacheManager,
    cache_status,
    clear_cache,
    export_cache,
    get_default_cache,
    import_cache,
    set_default_cache,
)
from .chemical import (
    Chemical,
    ChemicalDetails,
    ChemicalList,
    ChemicalProperties,
    ChemSynonym,
    ExtraData,
    PubChemLink,
    WikiLink,
)
from .config import (
    delete_api_key,
    get_config_dir,
    get_config_info,
    load_api_key,
    save_api_key,
)
from .exceptions import (
    APIError,
    AuthenticationError,
    CompToxError,
    ConfigurationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
)
from .exposure import (
    CCDData,
    DemographicExposure,
    ExposurePrediction,
    FunctionalUse,
    HTTKData,
    ListPresence,
    MMDB,
    ProductData,
)
from .hazard import (
    ADMEIVIVE,
    HAWC,
    IRIS,
    PPRTV,
    ToxRefDBBatch,
    ToxRefDBData,
    ToxRefDBEffects,
    ToxRefDBObservation,
    ToxRefDBSummary,
    ToxValDB,
    ToxValDBCancer,
    ToxValDBGenetox,
    ToxValDBSkinEye,
)

try:  # pragma: no cover - depends on install method
    from importlib.metadata import version

    __version__ = version("comptox-python")
except Exception:  # pragma: no cover - source checkout without metadata
    __version__ = "0.0.0.dev0"

__all__ = [
    "__version__",
    # subpackages
    "chemical",
    "hazard",
    "exposure",
    "bioactivity",
    # chemical clients
    "Chemical",
    "ChemicalDetails",
    "ChemicalProperties",
    "ChemSynonym",
    "ChemicalList",
    "ExtraData",
    "WikiLink",
    "PubChemLink",
    # hazard clients
    "PPRTV",
    "IRIS",
    "HAWC",
    "ADMEIVIVE",
    "ToxValDB",
    "ToxValDBCancer",
    "ToxValDBGenetox",
    "ToxValDBSkinEye",
    "ToxRefDBData",
    "ToxRefDBBatch",
    "ToxRefDBEffects",
    "ToxRefDBSummary",
    "ToxRefDBObservation",
    # exposure clients
    "CCDData",
    "MMDB",
    "FunctionalUse",
    "ProductData",
    "HTTKData",
    "ListPresence",
    "ExposurePrediction",
    "DemographicExposure",
    # bioactivity clients
    "AssaySearch",
    "AssayBioactivity",
    "BioactivityModel",
    "BioactivityData",
    "BioactivityAOP",
    "AnalyticalQC",
    # configuration
    "save_api_key",
    "load_api_key",
    "delete_api_key",
    "get_config_info",
    "get_config_dir",
    # caching
    "CacheManager",
    "get_default_cache",
    "set_default_cache",
    "clear_cache",
    "cache_status",
    "export_cache",
    "import_cache",
    # exceptions
    "CompToxError",
    "ConfigurationError",
    "APIError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "TimeoutError",
]
