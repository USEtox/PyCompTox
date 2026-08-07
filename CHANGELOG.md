# Changelog

All notable changes to PyCompTox will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.0] - 2026-07-28

This release repairs the public API surface and 16 client methods that could not
work at all, and standardises method naming. It contains **breaking changes**.

### Fixed

- **Restored `src/pycomptox/__init__.py`**, accidentally deleted in `7f72c34`.
  Without it `pycomptox` was an implicit namespace package: every documented
  top-level import (`from pycomptox import Chemical`, `from pycomptox import
  save_api_key`) raised `ImportError`, `__version__` was gone, and the `py.typed`
  marker was not honoured. 125 examples across the README, docs, and notebooks
  were affected. `__version__` is now read from installed package metadata so it
  cannot drift from `pyproject.toml`.

- **16 methods raised or 404'd on every call.** All are verified against the live
  API now:
  - Eight called a `self._make_request(...)` that was never defined, and did so
    with two different invented signatures — `AttributeError` every time:
    `Chemical.search_ms_ready_by_mass_range`,
    `Chemical.search_ms_ready_by_formula`, and the batch methods of
    `ListPresence`, `ExposurePrediction`, `DemographicExposure`, `ProductData`,
    `HTTKData`, and `FunctionalUse`.
  - Five `BioactivityData` batch methods hand-rolled their request and built the
    URL as `f"{base_url}{endpoint}"` with no separator, producing
    `.../ctx-apibioactivity/...` → HTTP 404. They also bypassed caching and rate
    limiting.
  - `Chemical.search_by_exact_formula` used `chemical/search/by-formula/`
    (404); the correct path is `chemical/search/by-exact-formula/`.
  - `BioactivityModel.get_toxcast_model_by_dtxsid` used
    `bioactivity/models/by-dtxsid/` (404); corrected to
    `bioactivity/models/search/by-dtxsid/`.
  - `BioactivityModel.get_toxcast_model_by_dtxsid_and_model` requested
    `bioactivity/models/search` (404); the trailing slash is required.

- **Requests can no longer hang forever.** Every call now has a `(10s, 60s)`
  connect/read timeout, configurable via the `timeout` argument.

- Docstrings no longer promise exceptions that were never raised. `RuntimeError`
  appeared in 62 docstrings and was raised zero times; 68 `Raises:` entries now
  name the real exception types.

- Type errors in `cache.py` (string parameters rebound to `Path`, heterogeneous
  dicts inferred as `object`) and a code path in `__main__.py` where `main()`
  could return `None` instead of an exit code.

- **Rate limiting now uses a monotonic clock.** `_enforce_rate_limit()` measured
  the interval between calls with `time.time()`, which can step backwards on an
  NTP correction or a VM/host suspend-resume. A backward jump made the measured
  interval negative, so the client slept for longer than the configured delay.
  It now uses `time.monotonic()`, and the 22 elapsed-time measurements in the
  test suite were converted too — a negative elapsed time from a backward clock
  jump is what surfaced this.

- **Reading configuration no longer writes to disk.** `get_config_dir()` created
  `~/.pycomptox` unconditionally, so `load_api_key()` — and therefore
  constructing any client — created a directory in the user's home as a side
  effect of a pure read. It is now created only by `save_api_key()`.
  `get_config_dir(create=True)` restores the old behaviour if needed.

- Documentation referenced 10 method names that never existed on any client
  (`search_by_name`, `search_by_casrn`, `get_chemical_by_dtxsid`,
  `get_bioactivity_summary`, `get_aop_by_dtxsid`, and others), across 52 call
  sites in the docs, README, and examples. All now name real methods.

- `ChemSynonym` documented and tested `alternateCasrn`/`deletedCasrn`, but the
  API (and the `ChemicalSynonymAll` schema) return `alternate`/`deleted`.
  Docstrings, docs, and tests corrected.

- `ChemicalList.get_public_lists_by_dtxsid` was documented and tested as
  returning a list of lists; it returns a list of record dicts.

### Added

- **Exception hierarchy** in `pycomptox.exceptions`, all deriving from
  `CompToxError`: `ConfigurationError`, `APIError`, `AuthenticationError`,
  `NotFoundError`, `RateLimitError`, `ServerError`, `TimeoutError`. Raw
  `requests` exceptions no longer leak to callers.
- **Automatic retries** with exponential backoff on 429 and 5xx, honouring
  `Retry-After`. Configurable via `max_retries`.
- **Spec-conformance test suite** (`tests/test_spec_conformance.py`) that checks
  every endpoint string in the source against vendored copies of the CompTox
  OpenAPI specs. This is what catches wrong paths and wrong HTTP methods in CI
  rather than at runtime; it found one of the bugs listed above. Refresh the
  specs with `python tests/specs/refresh.py`.
- **Import-surface tests** (`tests/test_public_api.py`) that fail if the package
  ever becomes a namespace package again.
- `tests/conftest.py` marks live-API tests as `integration` and skips them when
  no API key is present, so `pytest -m "not integration"` runs offline with no
  configuration.
- A `--run-slow` flag. 24 ToxRefDB tests that call the unfiltered
  `by-study-type` and `by-study-id` bulk endpoints are marked `slow` and skipped
  by default: those endpoints take 15–50s per call, which dominated the suite's
  runtime and pushed a full run into API rate limiting. Running just those four
  files went from over five minutes to 17 seconds. CI runs them on a weekly
  schedule. Use `pytest --run-slow` to include them locally.

  The flag is deliberately not `-m "not slow"` in `addopts`: pytest honours only
  one `-m` expression, so any command-line `-m` would silently override it and
  pull the slow tests back in.

### Changed — BREAKING

- **Caching is now off by default.** Previously every client cached every
  response to disk with no expiry, so stale results were easy to get
  unknowingly. Pass `use_cache=True` to a constructor or to any individual call
  to opt in. The cache directory is no longer created until something is written.

- **`CCCData` is renamed `CCDData`.** CCD stands for CompTox Chemicals Dashboard
  (the spec tag is "CCD Data Resource"), so the tripled C was a typo. The module
  `pycomptox/exposure/ccddata.py` was already correct and is unchanged.

- **Method naming is unified.** Retrieval methods use a `get_` prefix, search
  endpoints keep `search_`, and existence probes keep `check_`. Renames:

  | Old | New |
  | --- | --- |
  | `FunctionalUse.functiona_use_by_dtxsid` | `get_functional_use_by_dtxsid` |
  | `FunctionalUse.functiona_use_categories` | `get_functional_use_categories` |
  | `FunctionalUse.functional_use_probability_by_dtxsid` | `get_functional_use_probability_by_dtxsid` |
  | `FunctionalUse.functional_use_by_dtxsid_batch` | `get_functional_use_by_dtxsid_batch` |
  | `CCDData.product_use_category_by_dtxsid` | `get_product_use_category_by_dtxsid` |
  | `CCDData.production_volume_by_dtxsid` | `get_production_volume_by_dtxsid` |
  | `CCDData.biomonitoring_data_by_dtxsid_and_ccd` | `get_biomonitoring_data_by_dtxsid` |
  | `CCDData.general_use_keywords_by_dtxsid` | `get_general_use_keywords_by_dtxsid` |
  | `CCDData.reported_functional_use_by_dtxsid` | `get_reported_functional_use_by_dtxsid` |
  | `CCDData.chemical_weight_fraction_by_dtxsid` | `get_chemical_weight_fractions_by_dtxsid` |
  | `DemographicExposure.prediction_SEEMs_data_by_dtxsid` | `get_seem_prediction_by_dtxsid` |
  | `DemographicExposure.prediction_SEEMs_data_by_dtxsid_batch` | `get_seem_prediction_by_dtxsid_batch` |
  | `ExposurePrediction.general_prediction_SEEMs_by_dtxsid` | `get_general_seem_prediction_by_dtxsid` |
  | `ExposurePrediction.general_prediction_SEEMs_by_dtxsid_batch` | `get_general_seem_prediction_by_dtxsid_batch` |
  | `HTTKData.httk_data_by_dtxsid` | `get_httk_data_by_dtxsid` |
  | `HTTKData.httk_data_by_dtxsid_batch` | `get_httk_data_by_dtxsid_batch` |
  | `ListPresence.list_presence_tags` | `get_list_presence_tags` |
  | `ListPresence.list_presence_data_by_dtxsid` | `get_list_presence_data_by_dtxsid` |
  | `ListPresence.list_presence_data_by_dtxsid_batch` | `get_list_presence_data_by_dtxsid_batch` |
  | `MMDB.harmonized_single_sample_by_medium` | `get_harmonized_single_sample_by_medium` |
  | `MMDB.harmonized_single_sample_by_dtxsid` | `get_harmonized_single_sample_by_dtxsid` |
  | `MMDB.searchable_harmonized_medium_categories` | `get_harmonized_medium_categories` |
  | `MMDB.harmonized_aggregate_records_by_medium` | `get_harmonized_aggregate_records_by_medium` |
  | `ProductData.products_data_by_dtxsid` | `get_product_data_by_dtxsid` |
  | `ProductData.list_all_puc_product` | `get_all_puc_products` |
  | `ProductData.product_data_by_dtxsid_batch` | `get_product_data_by_dtxsid_batch` |
  | `ChemicalDetails.data_by_dtxsid` | `get_data_by_dtxsid` |
  | `ChemicalDetails.data_by_dtxcid` | `get_data_by_dtxcid` |
  | `ChemicalDetails.data_by_dtxsid_batch` | `get_data_by_dtxsid_batch` |
  | `ChemicalDetails.data_by_dtxcid_batch` | `get_data_by_dtxcid_batch` |
  | `ChemicalDetails.find_all_chemical_details` | `get_all_chemical_details` |
  | `BioactivityData.find_bioactivity_data_by_spid_batch` | `get_bioactivity_data_by_spid_batch` |
  | `BioactivityData.find_bioactivity_data_by_m4id_batch` | `get_bioactivity_data_by_m4id_batch` |
  | `BioactivityData.find_bioactivity_data_by_dtxsid_batch` | `get_bioactivity_data_by_dtxsid_batch` |
  | `BioactivityData.find_bioactivity_data_by_aeid_batch` | `get_bioactivity_data_by_aeid_batch` |
  | `BioactivityData.find_aed_data_by_dtxsid_batch` | `get_aed_data_by_dtxsid_batch` |
  | `AssayBioactivity.find_assay_annotations_by_aeid_batch` | `get_assay_annotations_by_aeid_batch` |

- **`ValueError` is no longer raised for API failures.** Missing API keys now
  raise `ConfigurationError` and HTTP failures raise the `APIError` subclasses.
  `ValueError` is still raised for local input validation. Catch `CompToxError`
  to handle everything the library raises.

- **`ipython` is no longer a runtime dependency.** It was declared but never
  imported by the library. `urllib3>=1.26` is now declared explicitly, since the
  retry configuration depends on it.

- **Python 3.12 is now the minimum.** 3.8 through 3.11 are no longer supported;
  CI tests 3.12 and 3.13. This also lets mypy pin `python_version = "3.12"`
  again, which recent releases refuse to do for targets below 3.10.

### Removed

- 35 redundant `__init__` overrides that only forwarded to `CachedAPIClient`
  without adding behaviour. Constructors now inherit the base signature, which
  also exposes the new `timeout` and `max_retries` arguments on every client.

  Three of those overrides did set a non-zero default delay. That is preserved
  through a new `default_time_delay` class attribute, which subclasses set
  instead of redefining `__init__`: `ChemicalList` and `PubChemLink` still
  default to 0.5s and `BioactivityModel` to 0.1s. `PubChemLink`'s parameter was
  also named `rate_limit_delay` rather than `time_delay_between_calls`; it now
  uses the standard name (**breaking** for anyone passing it by keyword).
- 81 unused imports across the package.
- `ipython` from the runtime dependencies (declared but never imported).

### Internal

- CI now runs the **whole** test suite. It previously ran only
  `tests/test_api.py`, 1 of 40 test files, which is why the 16 broken methods
  went unnoticed. Offline tests run on every push across 5 Python versions and 3
  operating systems without needing a secret; the live-API job runs separately.
- `mypy` now passes and no longer runs with `continue-on-error`. `black`,
  `isort`, `mypy`, and `flake8` were configured in `pyproject.toml` but not
  installed anywhere; they are now dev dependencies.
- `mkdocs build --strict` passes.
- Endpoint paths are normalised in one place. Leading slashes are stripped;
  trailing slashes are preserved, because the CompTox batch POST endpoints
  return 404 without them.
- Cache writes are atomic (temp file plus rename) instead of writing in place.

## [Unreleased]

### Added
- **Complete Hazard Module Implementation**
  - `ToxValDBGenetox` - Genotoxicity data from ToxValDB (4 methods: summary/detail single/batch)
  - `ToxRefDBData` - Dose-treatment group-effect data (3 methods: by study_type/study_id/dtxsid)
  - `ADMEIVIVE` - ADME-IVIVE toxicokinetics data (1 method: get_all_data_by_dtxsid_ccd_projection)
  - `ToxRefDBObservation` - Endpoint observation status (3 methods: by study_type/study_id/dtxsid)
- Comprehensive test suites for all hazard modules (90+ tests total)
- Complete API documentation for all 13 hazard module classes
- `HAZARD_MODULE.md` - Comprehensive overview guide with usage examples and best practices
- Updated MkDocs navigation with dedicated Hazard Module section

### Fixed
- Type annotations for `**kwargs` parameters in all hazard module `__init__` methods
- Documentation build warnings related to missing type annotations

## [0.6.0] - 2025-11-07

### Added
- **ChemicalList** module for accessing curated chemical lists
  - `get_all_list_types()` - Get available list type categories
  - `get_public_lists_by_type()` - Get lists by type (federal, international, state, other)
  - `get_public_lists_by_name()` - Search lists by name
  - `get_public_lists_by_dtxsid()` - Find lists containing a specific chemical
  - `get_dtxsids_by_listname_chem_name_start()` - Search chemicals in list by name prefix
  - `get_dtxsids_by_listname_chem_name_exact()` - Search chemicals in list by exact name
  - `get_dtxsids_by_listname_chem_name_contains()` - Search chemicals in list by substring
  - `get_dtxsids_by_listname_specific()` - Get all chemicals from a specific list
  - `get_all_public_lists()` - Get all public chemical lists
- Comprehensive test suite for ChemicalList (11 tests)
- GitHub Actions workflows for CI/CD
- Automated PyPI publishing workflow
- Pre-commit hooks configuration
- Release documentation and quick reference guides

### Changed
- Version bumped to 0.6.0
- Updated pyproject.toml with additional dev dependencies

## [0.5.0] - 2025-11-06

### Added
- **PubChemLink** module for checking PubChem GHS safety data
  - `check_existence_by_dtxsid()` - Check single chemical
  - `check_existence_by_dtxsid_batch()` - Batch check (up to 1000 chemicals)
- Comprehensive test suite for PubChemLink (9 tests)
- Documentation for PubChem GHS safety data links
- Jupyter notebook with PubChem examples
- Integration examples comparing Wikipedia and PubChem safety data

### Changed
- Version bumped to 0.5.0
- Updated MkDocs navigation to include PubChem documentation

## [0.4.0] - 2025-11-06

### Added
- **WikiLink** module for checking Wikipedia GHS safety data
  - `check_existence_by_dtxsid()` - Check single chemical
  - `check_existence_by_dtxsid_batch()` - Batch check (up to 1000 chemicals)
- Comprehensive test suite for WikiLink (7 tests)
- Documentation for Wikipedia GHS safety data links
- Jupyter notebook with Wikipedia examples
- MkDocs documentation site
  - Material theme
  - Auto-generated API documentation
  - User guides and examples

### Changed
- Version bumped to 0.4.0
- Enhanced documentation structure

## [0.3.0] - 2025-11-05

### Added
- **ExtraData** module for accessing additional chemical data
  - `get_data_by_dtxsid()` - Get extra data for single chemical
  - `get_data_by_dtxsid_batch()` - Get extra data for multiple chemicals
- **ChemicalProperties** module with 14 methods for property data
  - Physicochemical properties
  - Fate properties
  - ToxCast data
  - QSAR-ready descriptors
  - Toxicity data
  - Exposure data
  - Molar extinction curves
- Comprehensive test suites for all new modules
- Documentation for all property types and data sources

### Changed
- Improved error handling across all modules
- Enhanced type hints

## [0.2.0] - 2025-11-04

### Added
- **ChemicalDetails** module with 5 methods
  - `get_data_by_dtxsid()` - Get all data for a chemical
  - `data_by_dtxsid_with_projection()` - Get specific data fields
  - `get_data_by_dtxcid()` - Get data by DTXCID
  - `data_by_dtxcid_with_projection()` - Get specific fields by DTXCID
  - `ms_ready_by_dtxsid()` - Get mass spectrometry-ready structure
- 8 projection types for filtering detailed data
- Batch search methods to Chemical module:
  - `search_by_name_batch()`
  - `search_by_mass_batch()`
  - `search_equal_batch()`
- Rate limiting system (configurable delay between API calls)
- API key persistent storage
  - Save API key once, automatically loaded for all clients
  - Cross-platform support (Windows, macOS, Linux)
- Configuration management functions:
  - `save_api_key()`
  - `load_api_key()`
  - `delete_api_key()`
  - `get_config_info()`
  - `get_config_dir()`
- CLI tool for API key management (`pycomptox-setup`)

### Changed
- Improved error messages
- Enhanced documentation

## [0.1.0] - 2025-11-03

### Added
- Initial release
- **Chemical** (Search) module with 11 search methods:
  - `search_by_name()` - Search by chemical name
  - `search_by_synonym()` - Search by synonym
  - `search_by_casrn()` - Search by CAS Registry Number
  - `search_by_dtxsid()` - Search by DSSTox ID
  - `search_by_dtxcid()` - Search by DSSTox Compound ID
  - `search_by_inchikey()` - Search by InChIKey
  - `search_by_formula()` - Search by molecular formula
  - `search_by_mass()` - Search by molecular mass
  - `search_by_starting_value()` - Search by name prefix
  - `search_by_exact_value()` - Search by exact name
  - `search_equal()` - Search with exact matching
- Basic project structure
- Setup configuration with pyproject.toml
- README and LICENSE
- Initial documentation

### Technical Details
- Python 3.8+ support
- requests library for HTTP calls
- Type hints throughout
- Comprehensive docstrings

## Release Types

- **Major releases** (X.0.0): Breaking changes that require user code updates
- **Minor releases** (0.X.0): New features, backward compatible
- **Patch releases** (0.0.X): Bug fixes and minor improvements

## Links

- [PyPI](https://pypi.org/project/pycomptox/)
- [Documentation](https://usetox.github.io/PyCompTox/)
- [Source Code](https://github.com/USEtox/PyCompTox)
- [Issue Tracker](https://github.com/USEtox/PyCompTox/issues)
