# Changelog

All notable changes to PyCompTox will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-01-06

### Added
- **ExtraData API**: New `ExtraData` class for accessing reference counts and metadata
  - `get_data_by_dtxsid()` - Get reference data for single chemical
  - `get_data_by_dtxsid_batch()` - Batch retrieval of reference data
- **MkDocs Documentation**: Complete documentation site with Material theme
  - API reference documentation using mkdocstrings
  - User guides and tutorials
  - Examples and best practices
- **Jupyter Notebooks**: Added `extra_data_examples.ipynb` with 9 examples
- **Tests**: Complete test suite for ExtraData functionality

### Changed
- Updated package version to 0.4.0
- Updated `__init__.py` to export `ExtraData` class

### Fixed
- **URL Construction Bug**: Fixed URL joining issue in all API classes
  - Changed endpoints from absolute paths (`/chemical/...`) to relative paths (`chemical/...`)
  - Ensured `base_url` always ends with `/` for proper `urljoin` behavior
  - Fixed issue where `/ctx-api` was being dropped from URLs

## [0.3.0] - 2025-01-05

### Added
- **ChemicalProperties API**: Complete implementation with 14 methods
  - Property summaries (physchem and fate)
  - Predicted properties (QSAR models)
  - Experimental properties (measured data)
  - Environmental fate properties
  - Range searches and batch operations
- **Modern Setup Configuration**: 
  - Migrated to `pyproject.toml` (PEP 621, 517, 518, 561)
  - Added CLI entry points (`pycomptox-setup`)
  - Type checking support with `py.typed` marker
- **CLI Tool**: `__main__.py` with commands:
  - `set` - Save API key
  - `show` - Display configuration
  - `test` - Test API connectivity
  - `delete` - Remove saved API key
- **Documentation**: 
  - `CHEMICAL_PROPERTIES.md` - Complete API documentation
  - `INSTALLATION.md` - Installation guide
  - `MODERN_SETUP.md` - Setup documentation
- **Tests**: Comprehensive test suites for all modules
- **Notebooks**: `chemical_properties_examples.ipynb` with 10 examples

### Changed
- Updated package structure to use modern Python packaging
- Replaced `setup.py` with minimal shim
- Added optional dependencies for dev, notebook, and docs

## [0.2.0] - 2025-01-04

### Added
- **ChemicalDetails API**: Complete implementation with 5 methods and 8 projection types
- **Batch Operations**: Added batch methods for all API classes
- **Rate Limiting**: Configurable delay between API calls
- **API Key Management**: 
  - Persistent storage of API keys
  - Platform-specific config directories
  - Helper functions: `save_api_key()`, `load_api_key()`, `delete_api_key()`
- **Documentation**: 
  - `CHEMICAL_DETAILS.md` - Details API documentation
  - `IMPROVEMENTS_v0.2.0.md` - Feature documentation
- **Tests**: Test suites for details and batch operations
- **Notebooks**: `chemical_details_examples.ipynb` with 10 examples

### Changed
- Improved error handling across all API classes
- Enhanced type hints and docstrings

## [0.1.0] - 2025-01-03

### Added
- **Chemical Search API**: Initial implementation with 11 search methods
  - Search by name, CASRN, InChIKey, SMILES, formula, and mass
  - Batch search capabilities
- **Project Structure**: 
  - Package layout with `src/pycomptox/`
  - Basic `setup.py` configuration
  - MIT License
  - README with basic usage
- **Documentation**: 
  - `CHEMICAL_SEARCH.md` - Search API documentation
  - Initial examples
- **Tests**: Basic test suite
- **Notebooks**: `chemical_search_examples.ipynb` with 10 examples

### Infrastructure
- GitHub repository setup
- Python package structure
- Dependencies: requests

## [Unreleased]

### Planned Features
- Additional API endpoints (if available from CompTox)
- Async support for concurrent requests
- CLI tools for common operations
- Data export utilities
- Integration examples with pandas/numpy
- Performance optimizations

---

## Version Number Scheme

- **Major (X.0.0)**: Breaking changes
- **Minor (0.X.0)**: New features, backward compatible
- **Patch (0.0.X)**: Bug fixes, backward compatible

[0.4.0]: https://github.com/USEtox/PyCompTox/releases/tag/v0.4.0
[0.3.0]: https://github.com/USEtox/PyCompTox/releases/tag/v0.3.0
[0.2.0]: https://github.com/USEtox/PyCompTox/releases/tag/v0.2.0
[0.1.0]: https://github.com/USEtox/PyCompTox/releases/tag/v0.1.0
