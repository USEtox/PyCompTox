# PyCompTox

A comprehensive Python interface to the EPA CompTox Dashboard Chemical API.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

PyCompTox provides a simple, Pythonic interface to the [EPA CompTox Dashboard](https://comptox.epa.gov/dashboard/) Chemical API, enabling researchers and developers to programmatically access chemical data including:

- **Chemical Search**: Search by name, CASRN, InChIKey, SMILES, formula, and mass
- **Chemical Details**: Retrieve comprehensive chemical information with customizable projections
- **Chemical Properties**: Access physicochemical properties, QSAR predictions, experimental data, and fate properties
- **Bioactivity Data**: ToxCast bioactivity data, assay results, and Activity-Exposure-Dose (AED) data
- **Adverse Outcome Pathways**: AOP data linking ToxCast assays to biological events and pathways
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
from pycomptox.chemical import Chemical

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
from pycomptox.chemical import ChemicalDetails

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
from pycomptox.chemical import ChemicalProperties

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

### Get Bioactivity Data

```python
from pycomptox.bioactivity import BioactivityData

bioactivity = BioactivityData()

# Get bioactivity summary for a chemical
summary = bioactivity.get_summary_by_dtxsid("DTXSID7020182")

# Get data for an assay endpoint
data = bioactivity.get_data_by_aeid(3032)

# Get Activity-Exposure-Dose data
aed = bioactivity.get_aed_data_by_dtxsid("DTXSID5021209")
```

### Get Adverse Outcome Pathway Data

```python
from pycomptox.bioactivity import BioactivityAOP

aop = BioactivityAOP()

# Get AOP data by ToxCast assay endpoint
aop_data = aop.get_aop_data_by_toxcast_aeid(63)

# Get AOP data by event number
events = aop.get_aop_data_by_event_number(18)

# Get AOP data by gene ID
gene_aops = aop.get_aop_data_by_entrez_gene_id(196)
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

### Bioactivity Data (`BioactivityData`)

Access ToxCast bioactivity data:

- Summary statistics by chemical, tissue, or assay
- Detailed assay results
- Activity-Exposure-Dose (AED) data
- Sample and data identifier lookups
- Batch operations

[View Bioactivity Data Documentation →](BIOACTIVITY_DATA.md)

### Adverse Outcome Pathways (`BioactivityAOP`)

Link ToxCast assays to biological outcomes:

- AOP data by ToxCast assay endpoint
- AOP data by event number
- AOP data by gene ID
- Pathway and event relationships

[View AOP Documentation →](BIOACTIVITY_DATA.md)

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
- [Quick API Reference](QUICK_REFERENCE.md)
- [Configuration](configuration.md)
- [Best Practices](best_practices.md)
- [Chemical Search](CHEMICAL_SEARCH.md)
- [Chemical Details](CHEMICAL_DETAILS.md)
- [Chemical Properties](CHEMICAL_PROPERTIES.md)
- [Bioactivity Data & AOP](BIOACTIVITY_DATA.md)
- [Extra Data](EXTRA_DATA.md)
- [Batch Methods](BATCH_METHODS.md)
- [API Key & Rate Limiting](API_KEY_AND_RATE_LIMITING.md)
- [API Reference](api/chemical.md)
- [Examples](examples.md)

## Examples

See the `tests/` directory for comprehensive examples:

- `test_api.py` - Chemical search examples
- `test_details.py` - Details retrieval examples
- `test_properties.py` - Properties access examples
- `test_bioactivitydata.py` - Bioactivity data examples
- `test_bioactivityaop.py` - AOP data examples
- `test_extradata.py` - Reference data examples
- `test_batch_methods.py` - Batch operation examples

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
