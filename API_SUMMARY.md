# PyCompTox API Summary

## Overview

PyCompTox provides a complete Python interface to the EPA CompTox Dashboard Chemical API. The library is organized into 6 main classes, each covering different aspects of the API.

## Version History

- **v0.1.0** - Initial release with Chemical Search
- **v0.2.0** - Added API key management, rate limiting, and batch methods
- **v0.3.0** - Added ChemicalDetails, ChemicalProperties, and ExtraData classes
- **v0.4.0** - Added WikiLink class for Wikipedia GHS safety data
- **v0.5.0** - Added PubChemLink class for PubChem GHS safety data

## API Classes

### 1. Chemical (Search)
**Module:** `pycomptox.search`  
**Purpose:** Search for chemicals in the CompTox Dashboard database

**Methods:** 14 total
- Single search: 11 methods
  - `search_by_name()`
  - `search_by_synonym()`
  - `search_by_casrn()`
  - `search_by_dtxsid()`
  - `search_by_dtxcid()`
  - `search_by_inchikey()`
  - `search_by_formula()`
  - `search_by_mass()`
  - `search_by_starting_value()`
  - `search_by_exact_value()`
  - `search_equal()`
- Batch search: 3 methods
  - `search_by_name_batch()`
  - `search_by_mass_batch()`
  - `search_equal_batch()`

**Documentation:** [CHEMICAL_SEARCH.md](docs/CHEMICAL_SEARCH.md)

### 2. ChemicalDetails
**Module:** `pycomptox.details`  
**Purpose:** Get detailed information about chemicals

**Methods:** 5 total
- `data_by_dtxsid()` - Get all data for a chemical
- `data_by_dtxsid_with_projection()` - Get specific data fields
- `data_by_dtxcid()` - Get data by DTXCID
- `data_by_dtxcid_with_projection()` - Get specific fields by DTXCID
- `ms_ready_by_dtxsid()` - Get mass spectrometry-ready structure

**Projections:** 8 types
- `summary` - Basic information
- `synonym` - Alternative names
- `toxval` - Toxicity values
- `ntatoolkit` - Non-targeted analysis data
- `pathway` - Biological pathways
- `bioassay` - Bioassay data
- `qsar` - QSAR predictions
- `expo` - Exposure data

**Documentation:** [CHEMICAL_DETAILS.md](docs/CHEMICAL_DETAILS.md)

### 3. ChemicalProperties
**Module:** `pycomptox.property`  
**Purpose:** Access chemical property data

**Methods:** 14 total
- `file_by_dtxsid()` - Get downloadable property files
- `get_properties_by_dtxsid()` - Get all properties
- `get_fate_properties()` - Get fate properties
- `get_physchem_properties()` - Get physicochemical properties
- `get_toxcast_properties()` - Get ToxCast data
- `get_qsar_ready_properties()` - Get QSAR-ready molecular descriptors
- `get_toxicity_properties()` - Get toxicity data
- `get_exposure_properties()` - Get exposure data
- `get_molar_extinction_curves()` - Get UV-Vis spectra
- `search_property_by_name()` - Search for properties by name
- `search_property_by_dtxsid()` - Search properties for a chemical
- `get_msready_structure()` - Get MS-ready structure
- `get_batch_properties()` - Get properties for multiple chemicals
- `get_batch_properties_by_name()` - Get specific properties for multiple chemicals

**Documentation:** [CHEMICAL_PROPERTIES.md](docs/CHEMICAL_PROPERTIES.md)

### 4. ExtraData
**Module:** `pycomptox.extradata`  
**Purpose:** Access additional chemical data sources

**Methods:** 2 total
- `get_data_by_dtxsid()` - Get extra data for single chemical
- `get_data_by_dtxsid_batch()` - Get extra data for multiple chemicals

**Data Sources:**
- PubMed references
- Associated chemicals
- Related substances
- Chemical lists
- Source information
- QC levels

**Documentation:** [EXTRA_DATA.md](docs/EXTRA_DATA.md)

### 5. WikiLink
**Module:** `pycomptox.wikilink`  
**Purpose:** Check Wikipedia GHS safety data availability

**Methods:** 2 total
- `check_existence_by_dtxsid()` - Check single chemical
- `check_existence_by_dtxsid_batch()` - Check multiple chemicals (max 1000)

**Returns:**
- DTXSID
- Safety data availability flag
- Wikipedia URL to GHS classification

**Documentation:** [WIKIPEDIA_LINKS.md](docs/WIKIPEDIA_LINKS.md)

### 6. PubChemLink
**Module:** `pycomptox.pubchemlink`  
**Purpose:** Check PubChem GHS safety data availability

**Methods:** 2 total
- `check_existence_by_dtxsid()` - Check single chemical
- `check_existence_by_dtxsid_batch()` - Check multiple chemicals (max 1000)

**Returns:**
- DTXSID
- Safety data availability flag
- PubChem URL to GHS classification

**Documentation:** [PUBCHEM_LINKS.md](docs/PUBCHEM_LINKS.md)

## Configuration Functions

**Module:** `pycomptox.config`

- `save_api_key()` - Save API key to persistent storage
- `load_api_key()` - Load saved API key
- `delete_api_key()` - Remove saved API key
- `get_config_info()` - Display current configuration
- `get_config_dir()` - Get configuration directory path

## Common Features

All API classes share these features:

### 1. API Key Management
```python
from pycomptox import Chemical, save_api_key

# Save API key once
save_api_key("your-api-key-here")

# All clients automatically load the saved key
client = Chemical()
```

### 2. Rate Limiting
```python
# Default rate limit: 0.5 seconds between calls
client = Chemical()

# Custom rate limit
client = Chemical(rate_limit_delay=1.0)

# Disable rate limiting (not recommended)
client = Chemical(rate_limit_delay=0)
```

### 3. Error Handling
All methods include comprehensive error handling:
- `ValueError` - Invalid input parameters
- `RuntimeError` - API request failures

### 4. Type Hints
Full type hint support for better IDE integration:
```python
from pycomptox import Chemical
from typing import List, Dict

client: Chemical = Chemical()
results: List[Dict[str, Any]] = client.search_by_name("benzene")
```

## Quick Start Examples

### Search for Chemicals
```python
from pycomptox import Chemical

client = Chemical()
results = client.search_by_name("caffeine")
for result in results:
    print(f"{result['preferredName']}: {result['dtxsid']}")
```

### Get Chemical Details
```python
from pycomptox import ChemicalDetails

client = ChemicalDetails()
details = client.data_by_dtxsid("DTXSID7020182")
print(f"Name: {details['preferredName']}")
print(f"Formula: {details['molFormula']}")
```

### Get Chemical Properties
```python
from pycomptox import ChemicalProperties

client = ChemicalProperties()
props = client.get_physchem_properties("DTXSID7020182")
print(f"Properties: {len(props)}")
```

### Check Safety Data Sources
```python
from pycomptox import WikiLink, PubChemLink

wiki = WikiLink()
pubchem = PubChemLink()

dtxsid = "DTXSID7020182"
wiki_result = wiki.check_existence_by_dtxsid(dtxsid)
pubchem_result = pubchem.check_existence_by_dtxsid(dtxsid)

print(f"Wikipedia: {wiki_result['safetyUrl']}")
print(f"PubChem: {pubchem_result['safetyUrl']}")
```

### Complete Chemical Profile
```python
from pycomptox import (
    Chemical, ChemicalDetails, ChemicalProperties,
    WikiLink, PubChemLink, ExtraData
)

# Search for chemical
search = Chemical()
results = search.search_by_name("bisphenol a")
dtxsid = results[0]['dtxsid']

# Get detailed information
details = ChemicalDetails()
info = details.data_by_dtxsid(dtxsid)

# Get properties
props = ChemicalProperties()
physchem = props.get_physchem_properties(dtxsid)

# Get safety data sources
wiki = WikiLink()
pubchem = PubChemLink()
wiki_data = wiki.check_existence_by_dtxsid(dtxsid)
pubchem_data = pubchem.check_existence_by_dtxsid(dtxsid)

# Get extra data
extra = ExtraData()
extra_data = extra.get_data_by_dtxsid(dtxsid)

# Display complete profile
print(f"Chemical: {info['preferredName']}")
print(f"DTXSID: {dtxsid}")
print(f"Formula: {info['molFormula']}")
print(f"Properties: {len(physchem)}")
print(f"Wikipedia GHS: {wiki_data.get('safetyUrl', 'N/A')}")
print(f"PubChem GHS: {pubchem_data.get('safetyUrl', 'N/A')}")
print(f"PubMed refs: {len(extra_data.get('pubMedData', []))}")
```

## Installation

```bash
pip install pycomptox
```

## CLI Tools

PyCompTox includes a command-line tool for API key management:

```bash
# Save API key
pycomptox-setup set YOUR_API_KEY

# Show current configuration
pycomptox-setup show

# Test API connection
pycomptox-setup test

# Delete API key
pycomptox-setup delete
```

## Documentation

Full documentation is available at: [https://usetox.github.io/PyCompTox/](https://usetox.github.io/PyCompTox/)

- [Installation Guide](docs/INSTALLATION.md)
- [Quick Start Guide](docs/quick_start.md)
- [API Reference](docs/)
- [Examples](docs/examples.md)
- [Best Practices](docs/best_practices.md)

## Testing

All modules include comprehensive test suites:

```bash
# Run all tests
pytest

# Run specific module tests
pytest tests/test_search.py
pytest tests/test_details.py
pytest tests/test_property.py
pytest tests/test_extradata.py
pytest tests/test_wikilink.py
pytest tests/test_pubchemlink.py

# Run with coverage
pytest --cov=pycomptox
```

## Jupyter Notebooks

Example notebooks are available in the `notebooks/` directory:

- `chemical_search_examples.ipynb` - Chemical search examples
- `chemical_details_examples.ipynb` - Details and projections
- `chemical_properties_examples.ipynb` - Property data access
- `extradata_examples.ipynb` - Extra data examples
- `wikipedia_links_examples.ipynb` - Wikipedia safety data
- `pubchem_links_examples.ipynb` - PubChem safety data

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/contributing.md) for guidelines.

## Support

- GitHub Issues: [https://github.com/USEtox/PyCompTox/issues](https://github.com/USEtox/PyCompTox/issues)
- Documentation: [https://usetox.github.io/PyCompTox/](https://usetox.github.io/PyCompTox/)
- CompTox Dashboard: [https://comptox.epa.gov/dashboard](https://comptox.epa.gov/dashboard)
