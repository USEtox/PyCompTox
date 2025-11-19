# Chemical Details Module

The `ChemicalDetails` class provides methods to retrieve detailed chemical information from the EPA CompTox Dashboard API. This complements the `Chemical` class by providing comprehensive data after you've identified the chemicals you're interested in.

## Installation & Setup

```python
from pycomptox.chemical import Chemical, ChemicalDetails

# Initialize clients
searcher = Chemical(api_key="your-api-key")
details_client = ChemicalDetails(api_key="your-api-key")
```

## Typical Workflow

The recommended workflow is to:
1. **Search** for chemicals using the `Chemical` class to find DTXSID or DTXCID identifiers
2. **Retrieve details** using the `ChemicalDetails` class with those identifiers

## Methods Overview

### 1. `data_by_dtxsid(dtxsid, projection=None)`
Retrieve detailed information for a single chemical by DTXSID.

**Parameters:**
- `dtxsid` (str): The DTXSID identifier (e.g., "DTXSID7020182")
- `projection` (str, optional): Type of data to return. Options:
  - `"chemicaldetailstandard"` - Standard details (default)
  - `"chemicalidentifier"` - Identifiers only (DTXSID, CAS, InChI, etc.)
  - `"chemicalstructure"` - Structure information (SMILES, InChI, etc.)
  - `"ntatoolkit"` - NTA toolkit data
  - `"ccdchemicaldetails"` - CCD chemical details
  - `"ccdassaydetails"` - CCD assay details
  - `"chemicaldetailall"` - All available details
  - `"compact"` - Minimal compact format

**Returns:** Dictionary containing chemical details

**Example:**
```python
from pycomptox.chemical import Chemical, ChemicalDetails

# Step 1: Search for chemical
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
```

### 2. `data_by_dtxcid(dtxcid, projection=None)`
Retrieve detailed information for a single chemical by DTXCID.

**Parameters:**
- `dtxcid` (str): The DTXCID identifier (e.g., "DTXCID30182")
- `projection` (str, optional): Same projection options as `data_by_dtxsid`

**Returns:** Dictionary containing chemical details

**Example:**
```python
# Get structure details for a chemical by DTXCID
details = details_client.data_by_dtxcid(
    "DTXCID30182", 
    projection="chemicalstructure"
)

print(f"SMILES: {details['smiles']}")
print(f"InChI: {details['inchiString']}")
print(f"MS-Ready SMILES: {details['msReadySmiles']}")
```

### 3. `data_by_dtxsid_batch(dtxsids, projection=None)`
Retrieve details for multiple chemicals by DTXSIDs in a single request.

**Parameters:**
- `dtxsids` (List[str]): List of DTXSID identifiers (max 1000)
- `projection` (str, optional): Same projection options as single methods

**Returns:** List of dictionaries containing chemical details

**Example:**
```python
# Step 1: Search for multiple chemicals
names = ["Caffeine", "Aspirin", "Ibuprofen"]
dtxsids = []
for name in names:
    results = searcher.search_by_exact_value("name", name)
    if results:
        dtxsids.append(results[0]['dtxsid'])

# Step 2: Get batch details
batch_details = details_client.data_by_dtxsid_batch(dtxsids)

for chem in batch_details:
    print(f"{chem['preferredName']}: {chem.get('casrn', 'N/A')}")
```

### 4. `data_by_dtxcid_batch(dtxcids, projection=None)`
Retrieve details for multiple chemicals by DTXCIDs in a single request.

**Parameters:**
- `dtxcids` (List[str]): List of DTXCID identifiers (max 1000)
- `projection` (str, optional): Same projection options as single methods

**Returns:** List of dictionaries containing chemical details

**Example:**
```python
dtxcids = ["DTXCID30182", "DTXCID505"]
batch_details = details_client.data_by_dtxcid_batch(
    dtxcids,
    projection="chemicalidentifier"
)
```

### 5. `find_all_chemical_details(next_page=1, projection=None)`
Retrieve detailed information for all chemicals in the database (paginated).

**Parameters:**
- `next_page` (int): Page number to retrieve (default: 1)
- `projection` (str, optional): Same projection options as other methods

**Returns:** Dictionary with:
- `data`: List of chemical details
- `nextPage`: Next page number (null if last page)

**Example:**
```python
# Get first page of all chemicals
page1 = details_client.find_all_chemical_details(next_page=1)
print(f"Found {len(page1['data'])} chemicals")

# Get next page if available
if page1['nextPage']:
    page2 = details_client.find_all_chemical_details(next_page=page1['nextPage'])
```

## Projection Types

The `projection` parameter allows you to request specific subsets of data:

### `chemicalidentifier` - Chemical Identifiers
Returns: DTXSID, DTXCID, CAS RN, preferred name, IUPAC name, InChI key

**Use case:** When you only need identifiers and names

### `chemicalstructure` - Chemical Structure
Returns: SMILES, InChI, MS-ready SMILES, QSAR-ready SMILES, structure image flag

**Use case:** For cheminformatics applications needing structure data

### `ntatoolkit` - Non-Targeted Analysis Toolkit
Returns: Molecular formula, mass, assay counts, QSAR-ready data

**Use case:** For mass spectrometry and non-targeted analysis workflows

### `chemicaldetailstandard` - Standard Details (default)
Returns: Most commonly used fields including identifiers, structure, mass, assays

**Use case:** General purpose chemical information

### `chemicaldetailall` - All Available Details
Returns: Complete data including all identifiers, structures, properties, assays

**Use case:** When you need comprehensive information

### `compact` - Minimal Format
Returns: Only essential fields in a compact format

**Use case:** When bandwidth or storage is a concern

## Complete Example: Search to Details

```python
from pycomptox.chemical import Chemical, ChemicalDetails

# Initialize clients
searcher = Chemical()
details_client = ChemicalDetails()

# Search for a chemical by CAS number
cas_rn = "80-05-7"
search_results = searcher.search_by_exact_value("rn", cas_rn)

if search_results:
    chemical = search_results[0]
    print(f"Found: {chemical['displayName']}")
    print(f"DTXSID: {chemical['dtxsid']}")
    
    # Get comprehensive details
    details = details_client.data_by_dtxsid(
        chemical['dtxsid'],
        projection="chemicaldetailall"
    )
    
    # Display key information
    print(f"\nDetailed Information:")
    print(f"Preferred Name: {details.get('preferredName')}")
    print(f"Molecular Formula: {details.get('molFormula')}")
    print(f"Molecular Weight: {details.get('monoisotopicMass')}")
    print(f"SMILES: {details.get('smiles')}")
    print(f"InChI Key: {details.get('inchikey')}")
    print(f"Active Assays: {details.get('activeAssays')} / {details.get('totalAssays')}")
```

## Rate Limiting

Like the `Chemical` class, `ChemicalDetails` includes built-in rate limiting:

```python
# Set a delay between API calls (in seconds)
details_client = ChemicalDetails(time_delay_between_calls=0.5)
```

This is useful when making multiple requests to avoid overwhelming the API.

## Error Handling

The class includes comprehensive error handling:

```python
try:
    details = details_client.data_by_dtxsid("INVALID_ID")
except Exception as e:
    print(f"Error: {e}")
```

Common errors:
- **404 Not Found**: DTXSID/DTXCID doesn't exist
- **400 Bad Request**: Invalid parameters or too many IDs in batch
- **401 Unauthorized**: Invalid or missing API key
- **429 Too Many Requests**: Rate limit exceeded

## Performance Tips

1. **Use batch methods** when retrieving details for multiple chemicals:
   ```python
   # Good - single request
   details = details_client.data_by_dtxsid_batch(dtxsids)
   
   # Less efficient - multiple requests
   details = [details_client.data_by_dtxsid(id) for id in dtxsids]
   ```

2. **Use projections** to limit data transfer:
   ```python
   # Only get identifiers if that's all you need
   details = details_client.data_by_dtxsid(
       dtxsid,
       projection="chemicalidentifier"
   )
   ```

3. **Cache results** for repeated queries:
   ```python
   cache = {}
   
   def get_cached_details(dtxsid):
       if dtxsid not in cache:
           cache[dtxsid] = details_client.data_by_dtxsid(dtxsid)
       return cache[dtxsid]
   ```

## API Reference

For more information about the underlying API, see:
- [CompTox Dashboard API Documentation](https://comptox.epa.gov/ctx-api)
- [Chemical Details Resource Endpoints](https://comptox.epa.gov/ctx-api/chemical-details)

## Related Documentation

- [Chemical Search Methods](BATCH_METHODS.md) - For finding chemicals
- [API Key and Rate Limiting](API_KEY_AND_RATE_LIMITING.md) - Configuration
- [What's New in v0.2.0](IMPROVEMENTS_v0.2.0.md) - Latest features
