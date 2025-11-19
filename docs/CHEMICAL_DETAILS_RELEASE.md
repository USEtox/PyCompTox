# PyCompTox v0.2.0 - Chemical Details Feature

## Overview

Version 0.2.0 adds the **Chemical Details Resource** to PyCompTox, enabling retrieval of comprehensive chemical information from the EPA CompTox Dashboard. This complements the existing search functionality by allowing you to get detailed data about chemicals after you've identified them.

## What's New

### ChemicalDetails Class

A new `ChemicalDetails` class provides methods for retrieving detailed chemical information:

```python
from pycomptox.chemical import Chemical, ChemicalDetails

# Search for a chemical
searcher = Chemical()
results = searcher.search_by_exact_value("name", "Bisphenol A")

# Get detailed information
details_client = ChemicalDetails()
details = details_client.data_by_dtxsid(results[0]['dtxsid'])
```

### Five New Methods

1. **`data_by_dtxsid(dtxsid, projection=None)`**
   - Retrieve details for a single chemical by DTXSID
   - Supports projection parameter for data filtering

2. **`data_by_dtxcid(dtxcid, projection=None)`**
   - Retrieve details for a single chemical by DTXCID
   - Same projection support as DTXSID method

3. **`data_by_dtxsid_batch(dtxsids, projection=None)`**
   - Batch retrieval for up to 1000 DTXSIDs
   - Single API call for multiple chemicals

4. **`data_by_dtxcid_batch(dtxcids, projection=None)`**
   - Batch retrieval for up to 1000 DTXCIDs
   - Efficient bulk data access

5. **`find_all_chemical_details(next_page=1, projection=None)`**
   - Paginated access to all chemicals in database
   - Navigate through results page by page

### Eight Projection Types

Control what data you receive with flexible projection options:

1. **`chemicaldetailstandard`** (default)
   - Most commonly used fields
   - Identifiers, structure, mass, assays

2. **`chemicalidentifier`**
   - Only identifiers and names
   - DTXSID, DTXCID, CAS, InChI key, names

3. **`chemicalstructure`**
   - Structure information
   - SMILES, InChI, MS-ready SMILES

4. **`ntatoolkit`**
   - Non-targeted analysis data
   - Formula, mass, assay counts

5. **`ccdchemicaldetails`**
   - CCD chemical details

6. **`ccdassaydetails`**
   - CCD assay details

7. **`chemicaldetailall`**
   - Complete comprehensive data
   - All available fields

8. **`compact`**
   - Minimal compact format
   - Essential fields only

## Usage Examples

### Basic Workflow: Search → Details

```python
from pycomptox import Chemical, ChemicalDetails

# Initialize clients
searcher = Chemical()
details_client = ChemicalDetails()

# Search by name
results = searcher.search_by_exact_value("name", "Caffeine")
dtxsid = results[0]['dtxsid']

# Get full details
details = details_client.data_by_dtxsid(dtxsid)
print(f"Name: {details['preferredName']}")
print(f"Formula: {details['molFormula']}")
print(f"SMILES: {details['smiles']}")
print(f"Mass: {details['monoisotopicMass']}")
```

### Using Projections

```python
# Get only structure information
structure = details_client.data_by_dtxsid(
    "DTXSID7020182",
    projection="chemicalstructure"
)
print(f"SMILES: {structure['smiles']}")
print(f"InChI: {structure['inchiString']}")

# Get only identifiers
identifiers = details_client.data_by_dtxsid(
    "DTXSID7020182",
    projection="chemicalidentifier"
)
print(f"CAS: {identifiers['casrn']}")
print(f"InChI Key: {identifiers['inchikey']}")
```

### Batch Operations

```python
# Search for multiple chemicals
names = ["Caffeine", "Aspirin", "Ibuprofen"]
dtxsids = []

for name in names:
    results = searcher.search_by_exact_value("name", name)
    if results:
        dtxsids.append(results[0]['dtxsid'])

# Get batch details in one request
batch_details = details_client.data_by_dtxsid_batch(dtxsids)

for chem in batch_details:
    print(f"{chem['preferredName']}: {chem.get('casrn', 'N/A')}")
```

### Search by CAS Number

```python
# Search by CAS Registry Number
cas_rn = "80-05-7"
results = searcher.search_by_exact_value("rn", cas_rn)

if results:
    dtxsid = results[0]['dtxsid']
    
    # Get comprehensive details
    details = details_client.data_by_dtxsid(
        dtxsid,
        projection="chemicaldetailall"
    )
    
    print(f"Name: {details['preferredName']}")
    print(f"SMILES: {details['smiles']}")
    print(f"Active Assays: {details['activeAssays']}")
```

## Technical Implementation

### Class Design

The `ChemicalDetails` class follows the same design patterns as `Chemical`:

- **Session Management**: Persistent `requests.Session` for connection pooling
- **Rate Limiting**: Built-in `_enforce_rate_limit()` method
- **Error Handling**: Comprehensive HTTP error handling
- **Type Hints**: Full type annotations including `Literal` for projections
- **API Key Management**: Automatic loading from config/environment

### API Endpoints Used

```
POST /chemical/detail/search/by-dtxsid/
POST /chemical/detail/search/by-dtxcid/
GET  /chemical/detail/search/by-dtxsid/{dtxsid}
GET  /chemical/detail/search/by-dtxcid/{dtxcid}
GET  /chemical/detail/
```

### Response Handling

- Single methods return dictionaries
- Batch methods return lists of dictionaries
- Paginated method returns dict with `data` and `nextPage`
- Projection parameter passed as query string

## Testing

### New Test File: `test_details.py`

Comprehensive test suite (280+ lines) demonstrating:

1. **Complete Workflow Tests**
   - Search by name → get details
   - Search by CAS RN → get structure
   - Batch search → batch details
   - Using DTXCID for details

2. **Projection Tests**
   - Testing different projection types
   - Verifying field presence

3. **Batch Operation Tests**
   - Batch DTXSID retrieval
   - Batch DTXCID retrieval

### Test Results

All tests passing with real API calls:
- ✓ Search and details workflow (4 scenarios)
- ✓ Projection options working correctly
- ✓ Batch operations successful
- ✓ Error handling for None values

## Documentation

### New Documentation Files

1. **`docs/CHEMICAL_DETAILS.md`** (comprehensive guide)
   - All 5 methods documented
   - Complete examples for each method
   - Projection type explanations
   - Performance tips
   - Error handling guide

2. **Updated `README.md`**
   - Added ChemicalDetails section
   - Updated features list
   - Added version history
   - Updated project structure

## Performance Benefits

### Batch Operations

Instead of making N separate API calls:

```python
# Inefficient - N requests
details_list = []
for dtxsid in dtxsids:
    details = details_client.data_by_dtxsid(dtxsid)
    details_list.append(details)
```

Make a single batch request:

```python
# Efficient - 1 request (up to 1000 chemicals)
details_list = details_client.data_by_dtxsid_batch(dtxsids)
```

### Projection Filtering

Request only the data you need:

```python
# Get full details (larger response)
full = details_client.data_by_dtxsid(dtxsid)

# Get only identifiers (smaller response)
ids = details_client.data_by_dtxsid(
    dtxsid,
    projection="chemicalidentifier"
)
```

## Typical Use Cases

### 1. Chemical Information Lookup

```python
# User provides a chemical name
name = "Bisphenol A"

# Search for it
results = searcher.search_by_exact_value("name", name)

# Get comprehensive details
details = details_client.data_by_dtxsid(results[0]['dtxsid'])
```

### 2. Structure Retrieval

```python
# Need SMILES for cheminformatics
structure = details_client.data_by_dtxsid(
    dtxsid,
    projection="chemicalstructure"
)
smiles = structure['smiles']
```

### 3. Mass Spectrometry Workflow

```python
# Find chemicals in mass range
dtxsids = searcher.search_ms_ready_by_mass_range(228.0, 228.2)

# Get NTA toolkit data for all matches
nta_data = details_client.data_by_dtxsid_batch(
    dtxsids,
    projection="ntatoolkit"
)

for chem in nta_data:
    print(f"{chem['preferredName']}: {chem['molFormula']}")
```

### 4. Assay Data Analysis

```python
# Get assay information
details = details_client.data_by_dtxsid(dtxsid)
print(f"Active Assays: {details['activeAssays']}")
print(f"Total Assays: {details['totalAssays']}")
print(f"Percent Active: {details['activeAssays']/details['totalAssays']*100:.1f}%")
```

## Migration Guide

No breaking changes! The ChemicalDetails class is entirely new functionality.

Existing code continues to work as before:

```python
# v0.1.0 code still works
from pycomptox import Chemical
client = Chemical()
results = client.search_by_exact_value("Bisphenol A")
```

To use the new features:

```python
# Add ChemicalDetails import
from pycomptox import Chemical, ChemicalDetails

# Use as needed
details_client = ChemicalDetails()
details = details_client.data_by_dtxsid("DTXSID7020182")
```

## What's Next

Future enhancements planned:
- Chemical Properties Resource
- Chemical Lists Resource
- Chemical Synonym Resource
- Additional projections as API evolves
- Caching mechanisms for frequently accessed chemicals
- Async support for concurrent batch operations

## References

- **API Documentation**: https://comptox.epa.gov/ctx-api/chemical-details
- **Package Documentation**: `docs/CHEMICAL_DETAILS.md`
- **Test Examples**: `tests/test_details.py`
- **Main README**: `README.md`

## Summary

Version 0.2.0 adds powerful chemical detail retrieval capabilities to PyCompTox:

✅ **5 new methods** for flexible data access
✅ **8 projection types** for data filtering
✅ **Batch operations** for up to 1000 chemicals
✅ **280+ lines** of test code with real workflows
✅ **Comprehensive documentation** with examples
✅ **No breaking changes** - backward compatible

The search → details workflow is now complete, enabling users to find chemicals and retrieve comprehensive information efficiently.
