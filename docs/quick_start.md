# Quick Start Guide

Get up and running with PyCompTox in minutes!

## Prerequisites

- Python 3.8 or higher
- CompTox Dashboard API key ([Get one here](https://comptox.epa.gov/dashboard/api))

## Installation

Install PyCompTox using pip:

```bash
pip install comptox-python[all]
```

**Note**: do not install the package by ~~`pip install pycomptox`~~ which is a different package with the old comptox API.  

## API Key Configuration

Before using PyCompTox, you need to configure your API key.

### Method 1: Save API Key (Recommended)

```python
from pycomptox import save_api_key

# Save your API key permanently
save_api_key("your-api-key-here")
```

Or use the command-line tool:

```bash
pycomptox-setup set your-api-key-here
```

### Method 2: Environment Variable

```bash
# Linux/Mac
export COMPTOX_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:COMPTOX_API_KEY="your-api-key-here"
```

### Method 3: Pass Directly

```python
from pycomptox import Chemical

chem = Chemical(api_key="your-api-key-here")
```

## Your First Query

### Search for a Chemical

```python
from pycomptox import Chemical

# Initialize client
chem = Chemical()

# Search by name
results = chem.search_by_name("caffeine")

# Display results
for result in results[:5]:
    print(f"{result['preferredName']} - {result['dtxsid']}")
```

**Output:**
```
Caffeine - DTXSID2021315
Caffeine citrate - DTXSID60145239
...
```

### Get Chemical Details

```python
from pycomptox import ChemicalDetails

details = ChemicalDetails()

# Get basic information
info = details.get_chemical_by_dtxsid("DTXSID2021315")

print(f"Name: {info['preferredName']}")
print(f"Formula: {info['molFormula']}")
print(f"Weight: {info['molWeight']}")
```

**Output:**
```
Name: Caffeine
Formula: C8H10N4O2
Weight: 194.19
```

### Get Chemical Properties

```python
from pycomptox import ChemicalProperties

props = ChemicalProperties()

# Get property summary
summary = props.get_property_summary_by_dtxsid("DTXSID2021315")

print("Properties:")
for prop in summary[:5]:
    print(f"  {prop['propName']}: {prop.get('experimentalMedian', 'N/A')}")
```

### Get Reference Data

```python
from pycomptox import ExtraData

extra = ExtraData()

# Get reference counts
data = extra.get_data_by_dtxsid("DTXSID2021315")

print(f"Total References: {data['refs']}")
print(f"PubMed: {data['pubmed']}")
print(f"Patents: {data['googlePatent']}")
```

## Common Workflows

### Workflow 1: Find a Chemical and Get All Data

```python
from pycomptox.chemical import Chemical, ChemicalDetails, ChemicalProperties
from pycomptox.extra import ExtraData

# 1. Search for chemical
chem = Chemical()
results = chem.search_by_name("bisphenol A")
dtxsid = results[0]['dtxsid']

# 2. Get detailed information
details = ChemicalDetails()
info = details.get_chemical_by_dtxsid(dtxsid, projection="chemicaldetailall")

# 3. Get properties
props = ChemicalProperties()
properties = props.get_property_summary_by_dtxsid(dtxsid)

# 4. Get reference data
extra = ExtraData()
refs = extra.get_data_by_dtxsid(dtxsid)

# Display results
print(f"Chemical: {info['preferredName']}")
print(f"DTXSID: {dtxsid}")
print(f"CASRN: {info['casrn']}")
print(f"Formula: {info['molFormula']}")
print(f"Properties: {len(properties)}")
print(f"References: {refs['refs']}")
```

### Workflow 2: Batch Analysis

```python
from pycomptox import Chemical, ExtraData

# Get multiple chemicals
chem = Chemical()
dtxsids = [
    "DTXSID7020182",  # Bisphenol A
    "DTXSID2021315",  # Caffeine
    "DTXSID6020139"   # Benzene
]

# Get reference data for all
extra = ExtraData()
ref_data = extra.get_data_by_dtxsid_batch(dtxsids)

# Sort by reference count
sorted_data = sorted(ref_data, key=lambda x: x['refs'], reverse=True)

print("Most referenced:")
for data in sorted_data:
    print(f"  {data['dtxsid']}: {data['refs']} refs")
```

### Workflow 3: Property Analysis

```python
from pycomptox import ChemicalProperties

props = ChemicalProperties()

# Get predicted properties
dtxsid = "DTXSID7020182"
predicted = props.get_predicted_properties_by_dtxsid(dtxsid)

# Get experimental properties
experimental = props.get_experimental_properties_by_dtxsid(dtxsid)

print(f"Predicted properties: {len(predicted)}")
print(f"Experimental properties: {len(experimental)}")

# Compare a specific property
prop_name = "Log P"
pred = [p for p in predicted if prop_name in p.get('propName', '')]
exp = [p for p in experimental if prop_name in p.get('propName', '')]

if pred:
    print(f"Predicted {prop_name}: {pred[0]['propValue']}")
if exp:
    print(f"Experimental {prop_name}: {exp[0]['propValue']}")
```

## Next Steps

- [Chemical Search API](CHEMICAL_SEARCH.md) - Comprehensive search capabilities
- [Chemical Details API](CHEMICAL_DETAILS.md) - Retrieve detailed information
- [Chemical Properties API](CHEMICAL_PROPERTIES.md) - Access property data
- [Extra Data API](EXTRA_DATA.md) - Get reference counts
- [Best Practices](best_practices.md) - Tips for effective usage
- [Examples](examples.md) - More code examples

## Getting Help

- Check the [API Reference](api/chemical.md)
- Browse [Examples](examples.md)
- Review the Jupyter notebooks in `notebooks/`
- Open an issue on [GitHub](https://github.com/USEtox/PyCompTox/issues)
