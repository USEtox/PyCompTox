# PubChem GHS Safety Data Links

The `PubChemLink` class provides access to PubChem GHS (Globally Harmonized System) safety data availability information from the CompTox Dashboard API.

## Overview

PubChem is a free chemistry database maintained by the National Institutes of Health (NIH). The CompTox Dashboard can tell you whether a chemical has GHS safety classification data available on PubChem, providing direct links to that information.

## Quick Start

```python
from pycomptox import PubChemLink

# Initialize the client
client = PubChemLink()

# Check if a chemical has PubChem GHS data
result = client.check_existence_by_dtxsid("DTXSID7020182")
print(f"Has PubChem data: {result['isSafetyData']}")
print(f"URL: {result['safetyUrl']}")
```

## Methods

### check_existence_by_dtxsid()

Check if PubChem has GHS safety data for a single chemical.

**Parameters:**
- `dtxsid` (str): DSSTox Substance Identifier

**Returns:**
- Dictionary with:
  - `dtxsid` (str): The chemical's DTXSID
  - `isSafetyData` (bool): True if PubChem has GHS safety data
  - `safetyUrl` (str): URL to PubChem GHS classification page

**Example:**
```python
from pycomptox import PubChemLink

client = PubChemLink()
result = client.check_existence_by_dtxsid("DTXSID7020182")

if result['isSafetyData']:
    print(f"PubChem GHS data available at: {result['safetyUrl']}")
else:
    print("No PubChem GHS data available")
```

### check_existence_by_dtxsid_batch()

Check if PubChem has GHS safety data for multiple chemicals at once.

**Parameters:**
- `dtxsids` (List[str]): List of DSSTox Substance Identifiers (max 1000)

**Returns:**
- List of dictionaries, each with the same structure as `check_existence_by_dtxsid()`

**Example:**
```python
from pycomptox import PubChemLink

client = PubChemLink()
dtxsids = ["DTXSID7020182", "DTXSID2021315", "DTXSID5020001"]
results = client.check_existence_by_dtxsid_batch(dtxsids)

for result in results:
    status = "✓" if result['isSafetyData'] else "✗"
    print(f"{status} {result['dtxsid']}")
```

## Detailed Examples

### Example 1: Basic PubChem Data Check

```python
from pycomptox import PubChemLink

client = PubChemLink()

# Check for Bisphenol A
dtxsid = "DTXSID7020182"
result = client.check_existence_by_dtxsid(dtxsid)

print(f"Chemical: {dtxsid}")
print(f"Has PubChem GHS data: {result['isSafetyData']}")

if result['safetyUrl']:
    print(f"View GHS data at: {result['safetyUrl']}")
```

### Example 2: Batch Processing

```python
from pycomptox import PubChemLink

client = PubChemLink()

# Check multiple chemicals
chemicals = [
    "DTXSID7020182",  # Bisphenol A
    "DTXSID2021315",  # Caffeine
    "DTXSID5020001",  # 1,2,3-Trichloropropane
    "DTXSID3020637",  # Formaldehyde
    "DTXSID6020139"   # Benzene
]

results = client.check_existence_by_dtxsid_batch(chemicals)

# Count chemicals with PubChem data
with_data = sum(1 for r in results if r['isSafetyData'])
print(f"PubChem GHS data available: {with_data}/{len(results)}")

# Show results
for result in results:
    if result['isSafetyData']:
        print(f"✓ {result['dtxsid']}: {result['safetyUrl']}")
    else:
        print(f"✗ {result['dtxsid']}: No data")
```

### Example 3: Integration with Chemical Search

```python
from pycomptox.chemical import Chemical
from pycomptox.links import PubChemLink

# Search for phthalates
chem = Chemical()
search_results = chem.search_by_starting_value("phthalate")

# Check PubChem data for first 10 results
dtxsids = [r['dtxsid'] for r in search_results[:10]]

pubchem = PubChemLink()
pubchem_data = pubchem.check_existence_by_dtxsid_batch(dtxsids)

# Display results
for search_result in search_results[:10]:
    dtxsid = search_result['dtxsid']
    pubchem_result = next((p for p in pubchem_data if p['dtxsid'] == dtxsid), None)
    
    print(f"\n{search_result['preferredName']} ({dtxsid})")
    if pubchem_result and pubchem_result['isSafetyData']:
        print(f"  PubChem: {pubchem_result['safetyUrl'][:80]}...")
    else:
        print(f"  PubChem: No GHS data")
```

### Example 4: Data Analysis with Pandas

```python
from pycomptox import PubChemLink
import pandas as pd

client = PubChemLink()

# Check multiple chemicals
dtxsids = [
    "DTXSID7020182",
    "DTXSID2021315",
    "DTXSID5020001",
    "DTXSID3020637",
    "DTXSID6020139"
]

results = client.check_existence_by_dtxsid_batch(dtxsids)

# Convert to DataFrame
df = pd.DataFrame(results)

# Add a binary column for analysis
df['has_pubchem_data'] = df['isSafetyData']

# Show summary statistics
print(f"Total chemicals: {len(df)}")
print(f"With PubChem data: {df['has_pubchem_data'].sum()}")
print(f"Coverage: {df['has_pubchem_data'].mean():.1%}")

# Display chemicals with data
print("\nChemicals with PubChem GHS data:")
print(df[df['has_pubchem_data']][['dtxsid', 'safetyUrl']])
```

### Example 5: Compare Wikipedia vs PubChem Data

```python
from pycomptox import WikiLink, PubChemLink

wiki = WikiLink()
pubchem = PubChemLink()

dtxsids = [
    "DTXSID7020182",
    "DTXSID2021315",
    "DTXSID5020001"
]

# Get data from both sources
wiki_results = wiki.check_existence_by_dtxsid_batch(dtxsids)
pubchem_results = pubchem.check_existence_by_dtxsid_batch(dtxsids)

# Compare
print("GHS Data Availability Comparison:")
print("-" * 60)

for dtxsid in dtxsids:
    wiki_data = next((w for w in wiki_results if w['dtxsid'] == dtxsid), None)
    pubchem_data = next((p for p in pubchem_results if p['dtxsid'] == dtxsid), None)
    
    wiki_has = bool(wiki_data and wiki_data.get('safetyUrl'))
    pubchem_has = pubchem_data and pubchem_data['isSafetyData']
    
    print(f"\n{dtxsid}:")
    print(f"  Wikipedia: {'✓' if wiki_has else '✗'}")
    print(f"  PubChem:   {'✓' if pubchem_has else '✗'}")
    
    if wiki_has and pubchem_has:
        print(f"  ⭐ Data available in both sources")
```

### Example 6: Export Results

```python
from pycomptox import PubChemLink
import json

client = PubChemLink()

dtxsids = ["DTXSID7020182", "DTXSID2021315", "DTXSID5020001"]
results = client.check_existence_by_dtxsid_batch(dtxsids)

# Export to JSON
with open('pubchem_data.json', 'w') as f:
    json.dump(results, f, indent=2)
print("✓ Exported to pubchem_data.json")

# Export to CSV using pandas
import pandas as pd
df = pd.DataFrame(results)
df.to_csv('pubchem_data.csv', index=False)
print("✓ Exported to pubchem_data.csv")
```

### Example 7: Filter Chemicals by Data Availability

```python
from pycomptox.chemical import Chemical
from pycomptox.links import PubChemLink

# Search for a chemical class
chem = Chemical()
search_results = chem.search_by_starting_value("benzene")

# Get DTXSIDs
dtxsids = [r['dtxsid'] for r in search_results]

# Check PubChem data
pubchem = PubChemLink()
pubchem_data = pubchem.check_existence_by_dtxsid_batch(dtxsids)

# Filter to only chemicals with PubChem GHS data
with_data = [
    search_results[i] 
    for i, p in enumerate(pubchem_data) 
    if p['isSafetyData']
]

print(f"Found {len(with_data)} chemicals with PubChem GHS data:")
for chemical in with_data:
    print(f"  • {chemical['preferredName']} ({chemical['dtxsid']})")
```

## Error Handling

The `PubChemLink` class includes comprehensive error handling:

```python
from pycomptox import PubChemLink

client = PubChemLink()

# Handle invalid DTXSID
try:
    result = client.check_existence_by_dtxsid("")
except ValueError as e:
    print(f"Error: {e}")

# Handle batch size limit
try:
    too_many = [f"DTXSID{i}" for i in range(1001)]
    results = client.check_existence_by_dtxsid_batch(too_many)
except ValueError as e:
    print(f"Error: {e}")

# Handle network errors
try:
    result = client.check_existence_by_dtxsid("DTXSID7020182")
except RuntimeError as e:
    print(f"API Error: {e}")
```

## Rate Limiting

The client includes built-in rate limiting to avoid overwhelming the API:

```python
from pycomptox import PubChemLink

# Default rate limit: 0.5 seconds between calls
client = PubChemLink()

# Custom rate limit: 1 second between calls
client = PubChemLink(rate_limit_delay=1.0)

# Disable rate limiting (not recommended)
client = PubChemLink(rate_limit_delay=0)
```

## Response Structure

All methods return dictionaries with the following structure:

```python
{
    "dtxsid": "DTXSID7020182",
    "isSafetyData": True,
    "safetyUrl": "https://pubchem.ncbi.nlm.nih.gov/compound/DTXSID7020182#section=GHS-Classification"
}
```

**Fields:**
- `dtxsid`: The chemical's DSSTox identifier
- `isSafetyData`: Boolean indicating if PubChem has GHS safety data
- `safetyUrl`: Direct URL to PubChem GHS classification page (empty string if no data)

## API Endpoints

This class uses the following CompTox Dashboard API endpoints:

- **GET** `/chemical/ghslink/to-dtxsid/{dtxsid}` - Single chemical lookup
- **POST** `/chemical/ghslink/to-dtxsid/` - Batch chemical lookup (max 1000)

## See Also

- [WikiLink](WIKIPEDIA_LINKS.md) - Check Wikipedia GHS safety data availability
- [Chemical Search](CHEMICAL_SEARCH.md) - Find chemicals in the database
- [Chemical Details](CHEMICAL_DETAILS.md) - Get detailed chemical information
- [Chemical Properties](CHEMICAL_PROPERTIES.md) - Access chemical property data
