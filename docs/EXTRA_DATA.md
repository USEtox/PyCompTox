# Chemical Extra Data API

The `ExtraData` class provides access to reference counts and additional metadata for chemicals in the CompTox Dashboard, including literature references, PubMed citations, and patent information.

## Overview

Extra data includes counts of various reference sources:
- **Total references**: Overall reference count
- **Literature**: Literature reference count
- **PubMed**: Number of PubMed citations
- **Google Patents**: Number of patent references

## Quick Start

```python
from pycomptox import ExtraData

# Initialize client
extra = ExtraData()

# Get extra data for a chemical
data = extra.get_data_by_dtxsid("DTXSID7020182")
print(f"PubMed citations: {data['pubmed']}")
print(f"Patents: {data['googlePatent']}")
```

## Available Methods

### 1. Get Extra Data by DTXSID

Retrieve reference counts for a single chemical.

```python
data = extra.get_data_by_dtxsid("DTXSID7020182")
```

**Returns:**
```python
{
    'dtxsid': 'DTXSID7020182',
    'dtxcid': 20182,
    'refs': 1523,
    'googlePatent': 345,
    'literature': 892,
    'pubmed': 286
}
```

**Fields:**
- `dtxsid`: DSSTox Substance Identifier
- `dtxcid`: DSSTox Compound Identifier
- `refs`: Total reference count
- `googlePatent`: Number of Google Patent references
- `literature`: Number of literature references
- `pubmed`: Number of PubMed citations

### 2. Get Extra Data (Batch)

Retrieve extra data for multiple chemicals in a single request (up to 1000).

```python
dtxsids = ["DTXSID7020182", "DTXSID2021315", "DTXSID5020001"]
results = extra.get_data_by_dtxsid_batch(dtxsids)

for data in results:
    print(f"{data['dtxsid']}: {data['refs']} total references")
```

## Complete Examples

### Example 1: Basic Reference Lookup

```python
from pycomptox import ExtraData

extra = ExtraData()

# Get reference data for Bisphenol A
data = extra.get_data_by_dtxsid("DTXSID7020182")

print(f"Chemical: {data['dtxsid']}")
print(f"Total references: {data['refs']}")
print(f"PubMed citations: {data['pubmed']}")
print(f"Patent references: {data['googlePatent']}")
print(f"Literature references: {data['literature']}")
```

### Example 2: Batch Reference Analysis

```python
from pycomptox import ExtraData

extra = ExtraData()

# Analyze multiple chemicals
chemicals = [
    "DTXSID7020182",  # Bisphenol A
    "DTXSID2021315",  # Caffeine
    "DTXSID5020001",  # 1,2,3-Trichloropropane
    "DTXSID3020637",  # Formaldehyde
    "DTXSID6020139"   # Benzene
]

results = extra.get_data_by_dtxsid_batch(chemicals)

# Sort by total references
sorted_data = sorted(results, key=lambda x: x['refs'], reverse=True)

print("Chemicals ranked by total references:")
for i, data in enumerate(sorted_data, 1):
    print(f"{i}. {data['dtxsid']}: {data['refs']} refs")
```

### Example 3: Compare Reference Sources

```python
from pycomptox import ExtraData

extra = ExtraData()

dtxsid = "DTXSID7020182"
data = extra.get_data_by_dtxsid(dtxsid)

# Calculate proportions
total = data['refs']
if total > 0:
    pubmed_pct = (data['pubmed'] / total) * 100
    patent_pct = (data['googlePatent'] / total) * 100
    lit_pct = (data['literature'] / total) * 100
    
    print(f"Reference breakdown for {dtxsid}:")
    print(f"  PubMed: {data['pubmed']} ({pubmed_pct:.1f}%)")
    print(f"  Patents: {data['googlePatent']} ({patent_pct:.1f}%)")
    print(f"  Literature: {data['literature']} ({lit_pct:.1f}%)")
```

### Example 4: Filter by Reference Count

```python
from pycomptox import ExtraData

extra = ExtraData()

# Get data for multiple chemicals
dtxsids = ["DTXSID7020182", "DTXSID2021315", "DTXSID5020001",
           "DTXSID3020637", "DTXSID6020139"]

results = extra.get_data_by_dtxsid_batch(dtxsids)

# Find highly-referenced chemicals (>100 PubMed citations)
highly_cited = [d for d in results if d['pubmed'] > 100]

print(f"Found {len(highly_cited)} highly-cited chemicals:")
for data in highly_cited:
    print(f"  {data['dtxsid']}: {data['pubmed']} PubMed citations")
```

### Example 5: Integration with Chemical Search

```python
from pycomptox.chemical import Chemical
from pycomptox.extra import ExtraData

# Search for chemicals
chem = Chemical()
results = chem.search_by_name("benzene")

# Get reference data for search results
extra = ExtraData()
dtxsids = [r['dtxsid'] for r in results[:10]]
ref_data = extra.get_data_by_dtxsid_batch(dtxsids)

# Combine results
for result in results[:10]:
    dtxsid = result['dtxsid']
    refs = next((d for d in ref_data if d['dtxsid'] == dtxsid), None)
    
    if refs:
        print(f"{result['preferredName']} ({dtxsid})")
        print(f"  References: {refs['refs']}")
        print(f"  PubMed: {refs['pubmed']}")
```

## Data Structure

### ExtraData Response

```python
{
    'dtxsid': str,        # DSSTox Substance Identifier
    'dtxcid': int,        # DSSTox Compound Identifier
    'refs': int,          # Total reference count
    'googlePatent': int,  # Google Patent references
    'literature': int,    # Literature references
    'pubmed': int         # PubMed citations
}
```

## Error Handling

```python
from pycomptox import ExtraData

extra = ExtraData()

try:
    data = extra.get_data_by_dtxsid("INVALID_ID")
except ValueError as e:
    print(f"Invalid DTXSID: {e}")
except RuntimeError as e:
    print(f"Network error: {e}")
```

## Rate Limiting

Configure rate limiting to avoid overwhelming the API:

```python
# Add 0.5 second delay between requests
extra = ExtraData(time_delay_between_calls=0.5)

# Make multiple requests - automatically rate limited
for dtxsid in dtxsid_list:
    data = extra.get_data_by_dtxsid(dtxsid)
```

## Batch Request Limits

- Maximum 1000 DTXSIDs per batch request
- For larger datasets, split into multiple batches

```python
def get_refs_in_batches(dtxsids, batch_size=1000):
    """Get reference data in batches."""
    extra = ExtraData()
    all_results = []
    
    for i in range(0, len(dtxsids), batch_size):
        batch = dtxsids[i:i + batch_size]
        results = extra.get_data_by_dtxsid_batch(batch)
        all_results.extend(results)
    
    return all_results
```

## See Also

- [Chemical Search API](CHEMICAL_SEARCH.md)
- [Chemical Details API](CHEMICAL_DETAILS.md)
- [Chemical Properties API](CHEMICAL_PROPERTIES.md)
- [Installation Guide](INSTALLATION.md)
