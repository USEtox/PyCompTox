# PyCompTox

A Python interface for the EPA CompTox Dashboard Chemical API.

## Overview

PyCompTox provides a simple and intuitive Python interface to interact with the EPA's [CompTox Dashboard](https://comptox.epa.gov/) Chemical API. This package allows you to search for chemicals by name, identifiers (DTXSID, DTXCID, CAS numbers), molecular formulas, and mass ranges.

## Features

### Chemical Search (`Chemical` class)
- **Search chemicals by**:
  - Starting value (prefix search)
  - Exact value match
  - Substring/contains search
  - Molecular formula (exact and MS-ready)
  - Mass range (for MS-ready chemicals)
  - DTXCID
- **Batch operations**: Search multiple values in a single API call

### Chemical Details (`ChemicalDetails` class)
- **Retrieve detailed information** for chemicals by DTXSID or DTXCID
- **Flexible projections**: Request only the data you need
  - Chemical identifiers (CAS, InChI, names)
  - Chemical structures (SMILES, InChI strings)
  - NTA toolkit data (for mass spectrometry)
  - Assay data
  - Complete details
- **Batch retrieval**: Get details for up to 1000 chemicals at once
- **Paginated access**: Retrieve all chemicals in the database

### General Features
- **API Key Management**: Save your API key once and use it automatically
- **Rate Limiting**: Built-in rate limiting to respect API usage limits
- **Type-Safe**: Full type hints for better IDE support and code quality
- **Error Handling**: Comprehensive error handling with clear exception messages
- **Well Documented**: Detailed docstrings and examples

## Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/USEtox/PyCompTox.git
cd PyCompTox

# Install the package
pip install -e .

# Or with development tools
pip install -e ".[dev]"

# Or with notebook support
pip install -e ".[notebook]"
```

PyCompTox now uses modern Python packaging with `pyproject.toml`. See [INSTALLATION.md](docs/INSTALLATION.md) for detailed installation options.

### Optional Dependencies

- **dev**: Development tools (pytest, black, mypy, flake8)
- **notebook**: Jupyter notebook support with pandas and matplotlib
- **all**: All optional dependencies

```bash
pip install -e ".[all]"
```

## API Key Setup

To use the CompTox Dashboard API, you need an API key. You can obtain one from the [CompTox Dashboard API documentation](https://comptox.epa.gov/ctx-api/).

### Save Your API Key (Recommended)

Save your API key once and it will be automatically loaded for all future sessions:

```bash
python setup_api_key.py set YOUR_API_KEY
```

The API key is stored securely in your user's application data directory:
- **Windows**: `%APPDATA%\PyCompTox\api_key.txt`
- **macOS/Linux**: `~/.pycomptox/api_key.txt`

### Manage Your API Key

```bash
# Test if your API key works
python setup_api_key.py test

# Show your saved API key (masked)
python setup_api_key.py show

# Delete your saved API key
python setup_api_key.py delete
```

### Alternative Methods

You can also provide the API key in other ways:

1. **Environment Variable**: Set `COMPTOX_API_KEY` environment variable
2. **Direct Parameter**: Pass `api_key` parameter when creating the client

## Quick Start

```python
from pycomptox import Chemical

# Option 1: Use saved API key (automatic - recommended)
client = Chemical()

# Option 2: Provide API key directly
client = Chemical(api_key="your_api_key_here")

# Option 3: Save API key from Python
from pycomptox import save_api_key
save_api_key("your_api_key_here")
client = Chemical()

# Search for chemicals starting with "Bisphenol"
results = client.search_by_starting_value("Bisphenol")
for chem in results:
    print(f"{chem['preferredName']} - {chem['dtxsid']}")

# Search by exact identifier
results = client.search_by_exact_value("DTXSID7020182")
print(f"Chemical: {results[0]['preferredName']}")
print(f"CAS RN: {results[0]['casrn']}")

# Search by molecular formula
dtxsids = client.search_by_msready_formula("C15H16O2")
print(f"Found {len(dtxsids)} chemicals with formula C15H16O2")

# Search by mass range
dtxsids = client.search_ms_ready_by_mass_range(200.9, 200.95)
print(f"Found {len(dtxsids)} chemicals in mass range")
```

## API Methods

### Search Methods

#### `search_by_starting_value(value: str)`
Search chemicals where name/identifier starts with the given value.

```python
results = client.search_by_starting_value("Bisphenol")
```

#### `search_by_exact_value(value: str)`
Search chemicals by exact name/identifier match.

```python
results = client.search_by_exact_value("Bisphenol A")
```

#### `search_by_substring_value(value: str)`
Search chemicals where name/identifier contains the given substring.

```python
results = client.search_by_substring_value("phenol")
```

#### `search_by_msready_formula(formula: str)`
Search chemicals by MS-ready molecular formula.

```python
dtxsids = client.search_by_msready_formula("C15H16O2")
```

#### `search_by_exact_formula(formula: str)`
Search chemicals by exact molecular formula.

```python
dtxsids = client.search_by_exact_formula("C15H16O2")
```

#### `search_ms_ready_by_mass_range(min_mass: float, max_mass: float)`
Search MS-ready chemicals within a mass range.

```python
dtxsids = client.search_ms_ready_by_mass_range(200.9, 200.95)
```

#### `search_ms_ready_by_formula(formula: str)`
Search MS-ready chemicals by molecular formula.

```python
dtxsids = client.search_ms_ready_by_formula("C16H24N2O5S")
```

#### `search_ms_ready_by_dtxcid(dtxcid: str)`
Search MS-ready chemicals by DTXCID.

```python
dtxsids = client.search_ms_ready_by_dtxcid("DTXCID30182")
```

### Count Methods

#### `search_chemical_count_by_ms_ready_formula(formula: str)`
Get the count of chemicals with a given MS-ready formula.

```python
count = client.search_chemical_count_by_ms_ready_formula("C15H16O2")
```

#### `search_chemical_count_by_exact_formula(formula: str)`
Get the count of chemicals with a given exact formula.

```python
count = client.search_chemical_count_by_exact_formula("C15H16O2")
```

## Response Format

### Chemical Search Results

Methods like `search_by_starting_value`, `search_by_exact_value`, and `search_by_substring_value` return a list of dictionaries with the following structure:

```python
{
    "preferredName": str,      # The preferred chemical name
    "isMarkush": bool,          # Whether the chemical is a Markush structure
    "searchName": str,          # The name field that matched
    "searchValue": str,         # The value that was matched
    "smiles": str,              # The SMILES notation
    "dtxcid": str,              # The DSSTox Compound ID
    "dtxsid": str,              # The DSSTox Substance ID
    "casrn": str,               # The CAS Registry Number
    "rank": int,                # The search result ranking
    "hasStructureImage": int    # Whether a structure image is available
}
```

### Formula/Mass Search Results

Methods like `search_by_msready_formula` and `search_ms_ready_by_mass_range` return a list of DTXSID strings:

```python
["DTXSID1012345", "DTXSID2067890", ...]
```

## Rate Limiting

PyCompTox includes built-in rate limiting to respect API usage limits. You can configure the delay between API calls:

```python
# Create a client with a 0.5 second delay between calls
client = Chemical(time_delay_between_calls=0.5)

# Make multiple calls - automatic delay will be enforced
for formula in ["C15H16O2", "C16H24N2O5S", "C10H8"]:
    results = client.search_by_msready_formula(formula)
    print(f"Found {len(results)} chemicals for {formula}")
```

The default delay is 0.0 seconds (no delay). If you encounter rate limiting errors, increase this value.

## Chemical Details

Once you've found the chemicals you're interested in, use the `ChemicalDetails` class to retrieve comprehensive information:

```python
from pycomptox import Chemical, ChemicalDetails

# Step 1: Search for a chemical
searcher = Chemical()
results = searcher.search_by_exact_value("name", "Bisphenol A")
dtxsid = results[0]['dtxsid']  # DTXSID7020182

# Step 2: Get detailed information
details_client = ChemicalDetails()
details = details_client.data_by_dtxsid(dtxsid)

print(f"Name: {details['preferredName']}")
print(f"Formula: {details['molFormula']}")
print(f"SMILES: {details['smiles']}")
print(f"Molecular Weight: {details['monoisotopicMass']}")
print(f"Active Assays: {details['activeAssays']}")

# Get only structure information
structure = details_client.data_by_dtxsid(
    dtxsid,
    projection="chemicalstructure"
)
print(f"InChI: {structure['inchiString']}")

# Batch retrieval for multiple chemicals
names = ["Caffeine", "Aspirin", "Ibuprofen"]
dtxsids = []
for name in names:
    results = searcher.search_by_exact_value("name", name)
    if results:
        dtxsids.append(results[0]['dtxsid'])

batch_details = details_client.data_by_dtxsid_batch(dtxsids)
for chem in batch_details:
    print(f"{chem['preferredName']}: {chem.get('casrn', 'N/A')}")
```

See [CHEMICAL_DETAILS.md](docs/CHEMICAL_DETAILS.md) for complete documentation on:
- All available methods
- Projection types and use cases
- Performance tips
- Complete workflow examples

## Examples

See the `tests/` folder for usage examples:

```bash
# Run basic search tests
python tests/test_api.py

# Run batch search tests
python tests/test_batch_methods.py

# Run chemical details tests (complete workflow)
python tests/test_details.py
```

## Error Handling

The package provides clear error messages for common issues:

```python
try:
    # API key is loaded automatically
    client = Chemical()
    results = client.search_by_exact_value("NonexistentChemical")
except ValueError as e:
    # API key not configured or data not found
    print(f"Error: {e}")
except PermissionError as e:
    # Invalid API key
    print(f"API key issue: {e}")
except RuntimeError as e:
    # Network or rate limit errors
    print(f"Request failed: {e}")
```

## Project Structure

```
PyCompTox/
├── src/
│   └── pycomptox/
│       ├── __init__.py      # Package initialization
│       ├── config.py        # API key management
│       ├── search.py        # Chemical search API client
│       └── details.py       # Chemical details API client
├── tests/
│   ├── __init__.py          # Test package
│   ├── test_api.py          # Basic search tests
│   ├── test_batch_methods.py # Batch search tests
│   └── test_details.py      # Chemical details tests
├── docs/
│   ├── API_KEY_AND_RATE_LIMITING.md  # Configuration guide
│   ├── BATCH_METHODS.md              # Batch operations guide
│   ├── CHEMICAL_DETAILS.md           # Details API guide
│   └── IMPROVEMENTS_v0.2.0.md        # v0.2.0 release notes
├── setup_api_key.py         # API key management utility
├── requirements.txt         # Package dependencies
├── README.md               # This file
└── LICENSE                 # License information
```

## API Key Storage

Your API key is stored securely in your user's application data directory:
- **Windows**: `C:\Users\<username>\AppData\Roaming\PyCompTox\api_key.txt`
- **macOS/Linux**: `~/.pycomptox/api_key.txt`

The file is created with user-only read permissions on Unix-like systems.

## Version History

### v0.2.0 (Current)
- ✅ Chemical Details Resource implementation
  - 5 methods for retrieving detailed chemical information
  - Support for 8 projection types
  - Batch retrieval (up to 1000 chemicals)
  - Paginated access to all chemicals
- ✅ Comprehensive test suite with real workflow examples
- ✅ Detailed documentation for all features

### v0.1.0
- ✅ Chemical Search Resource implementation
  - 11 search methods
  - 3 batch search methods
- ✅ API key persistent storage
- ✅ Rate limiting support
- ✅ Complete type hints

See [IMPROVEMENTS_v0.2.0.md](docs/IMPROVEMENTS_v0.2.0.md) for detailed v0.2.0 release notes.

## Contributing

Contributions are welcome! Future enhancements may include:

- Additional API endpoints (chemical properties, lists, etc.)
- Caching mechanisms
- Async support
- Pytest-based unit tests
- More comprehensive error recovery

## API Documentation

For detailed API documentation, visit:
https://comptox.epa.gov/ctx-api/docs/chemical.html

## License

See the LICENSE file for details.

## Disclaimer

This package is not officially affiliated with or endorsed by the U.S. Environmental Protection Agency (EPA). It is an independent implementation of a Python client for the publicly available CompTox Dashboard API.
