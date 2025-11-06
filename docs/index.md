# PyCompTox

A comprehensive Python interface to the EPA CompTox Dashboard Chemical API.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

PyCompTox provides a simple, Pythonic interface to the [EPA CompTox Dashboard](https://comptox.epa.gov/dashboard/) Chemical API, enabling researchers and developers to programmatically access chemical data including:

- **Chemical Search**: Search by name, CASRN, InChIKey, SMILES, formula, and mass
- **Chemical Details**: Retrieve comprehensive chemical information with customizable projections
- **Chemical Properties**: Access physicochemical properties, QSAR predictions, experimental data, and fate properties
- **Extra Data**: Get reference counts from literature, PubMed, and patents

## Features

✨ **Easy to Use**: Simple, intuitive API with consistent method signatures

🔑 **API Key Management**: Built-in persistent storage for API keys

⚡ **Batch Operations**: Efficient batch methods for querying multiple chemicals

🛡️ **Rate Limiting**: Built-in rate limiting to respect API constraints

📊 **Type Hints**: Full type annotations for better IDE support

🧪 **Well Tested**: Comprehensive test suite

📚 **Extensive Documentation**: Detailed documentation and examples

## Quick Start

### Installation

```bash
pip install pycomptox
```

Or for development:

```bash
git clone https://github.com/USEtox/PyCompTox.git
cd PyCompTox
pip install -e .
```

### Basic Usage

```python
from pycomptox import Chemical

# Initialize the client
chem = Chemical()

# Search for a chemical by name
results = chem.search_by_name("caffeine")

# Get the first result
if results:
    chemical = results[0]
    print(f"Name: {chemical['preferredName']}")
    print(f"DTXSID: {chemical['dtxsid']}")
    print(f"CASRN: {chemical['casrn']}")
```

### Get Chemical Details

```python
from pycomptox import ChemicalDetails

details = ChemicalDetails()

# Get comprehensive information
info = details.get_chemical_by_dtxsid(
    "DTXSID7020182",
    projection="chemicaldetailall"
)

print(f"Name: {info['preferredName']}")
print(f"Molecular Formula: {info['molFormula']}")
print(f"Molecular Weight: {info['molWeight']}")
```

### Get Chemical Properties

```python
from pycomptox import ChemicalProperties

props = ChemicalProperties()

# Get property summary
summary = props.get_property_summary_by_dtxsid("DTXSID7020182")

for prop in summary:
    print(f"{prop['propName']}: {prop.get('experimentalMedian', 'N/A')}")
```

### Get Reference Data

```python
from pycomptox import ExtraData

extra = ExtraData()

# Get reference counts
data = extra.get_data_by_dtxsid("DTXSID7020182")

print(f"Total references: {data['refs']}")
print(f"PubMed citations: {data['pubmed']}")
print(f"Patents: {data['googlePatent']}")
```

## API Key Setup

PyCompTox requires a CompTox Dashboard API key. You can obtain one from the [EPA CompTox Dashboard](https://comptox.epa.gov/dashboard/api).

### Save API Key

```python
from pycomptox import save_api_key

# Save your API key (one-time setup)
save_api_key("your-api-key-here")
```

Or use the command-line tool:

```bash
pycomptox-setup set your-api-key-here
```

### Alternative: Environment Variable

```bash
export COMPTOX_API_KEY=your-api-key-here
```

## Main Components

### Chemical Search (`Chemical`)

Search and discover chemicals using various identifiers:

- Name search
- CASRN lookup
- InChIKey search
- SMILES search
- Formula search
- Mass search
- Batch operations

[View Chemical Search Documentation →](CHEMICAL_SEARCH.md)

### Chemical Details (`ChemicalDetails`)

Retrieve detailed chemical information with customizable projections:

- Basic chemical data
- Identifiers (CASRN, InChI, SMILES)
- Synonyms
- Molecular properties
- Associated substances
- Batch retrieval

[View Chemical Details Documentation →](CHEMICAL_DETAILS.md)

### Chemical Properties (`ChemicalProperties`)

Access comprehensive property data:

- Property summaries
- Predicted properties (QSAR)
- Experimental measurements
- Environmental fate properties
- Range searches
- Batch operations

[View Chemical Properties Documentation →](CHEMICAL_PROPERTIES.md)

### Extra Data (`ExtraData`)

Get reference counts and metadata:

- Total reference counts
- PubMed citations
- Google Patent references
- Literature references
- Batch retrieval

[View Extra Data Documentation →](EXTRA_DATA.md)

## Documentation

- [Installation Guide](INSTALLATION.md)
- [Quick Start Tutorial](quick_start.md)
- [Configuration](configuration.md)
- [Best Practices](best_practices.md)
- [API Reference](api/chemical.md)
- [Examples](examples.md)

## Examples

See the `notebooks/` directory for Jupyter notebook examples:

- `chemical_search_examples.ipynb` - Chemical search examples
- `chemical_details_examples.ipynb` - Details retrieval examples
- `chemical_properties_examples.ipynb` - Properties access examples
- `extra_data_examples.ipynb` - Reference data examples

## Requirements

- Python 3.8 or higher
- `requests` library
- CompTox Dashboard API key

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](license.md) file for details.

## Acknowledgments

This package interfaces with the EPA CompTox Dashboard Chemical API. For more information about the CompTox Dashboard, visit:

- [CompTox Dashboard](https://comptox.epa.gov/dashboard/)
- [CompTox API Documentation](https://comptox.epa.gov/dashboard/api)

## Citation

If you use PyCompTox in your research, please cite:

```
PyCompTox: A Python Interface to the EPA CompTox Dashboard Chemical API
https://github.com/USEtox/PyCompTox
```

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/USEtox/PyCompTox).
