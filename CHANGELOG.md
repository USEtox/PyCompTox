# Changelog

All notable changes to PyCompTox will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
  - `data_by_dtxsid()` - Get all data for a chemical
  - `data_by_dtxsid_with_projection()` - Get specific data fields
  - `data_by_dtxcid()` - Get data by DTXCID
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
