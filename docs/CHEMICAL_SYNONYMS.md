# Chemical Synonyms API

The `ChemSynonym` class provides access to chemical synonym data from the EPA CompTox Dashboard, including alternative names, identifiers, and quality-rated synonyms.

## Overview

The Chemical Synonyms API allows you to retrieve:

- **Valid and good quality synonyms** - Curated chemical names
- **Alternate identifiers** - Beilstein numbers, alternate CAS numbers
- **Categorized synonyms** - Organized by quality and type
- **Flexible projections** - Structured or flat list views
- **Batch operations** - Query up to 1000 chemicals at once

## Quick Start

```python
from pycomptox.chemical import ChemSynonym

# Initialize client
synonym_client = ChemSynonym()

# Get synonyms for Bisphenol A
synonyms = synonym_client.get_synonyms_by_dtxsid("DTXSID7020182")
print(f"Valid names: {synonyms['valid']}")
print(f"Good quality names: {synonyms['good']}")
```

## Installation

```bash
pip install pycomptox
```

## Basic Usage

### Getting Chemical Synonyms

Retrieve structured synonym data with categorized fields:

```python
from pycomptox import ChemSynonym

synonym_client = ChemSynonym()

# Get synonyms for Bisphenol A
data = synonym_client.get_synonyms_by_dtxsid("DTXSID7020182")

# Access different categories
print(f"DTXSID: {data['dtxsid']}")
print(f"Valid synonyms: {data['valid']}")
print(f"Good quality: {data['good']}")
print(f"Alternate CAS: {data['alternateCasrn']}")
print(f"Beilstein numbers: {data['beilstein']}")
```

### Using Projections

Get a flat list of synonyms with quality ratings:

```python
# Get flat list with quality ratings
flat_synonyms = synonym_client.get_synonyms_by_dtxsid(
    "DTXSID7020182",
    projection="ccd-synonyms"
)

# Display synonyms with their quality ratings
for item in flat_synonyms[:10]:
    print(f"{item['synonym']}: {item['quality']}")
```

### Batch Synonym Retrieval

Query multiple chemicals efficiently:

```python
# Get synonyms for multiple chemicals
dtxsids = [
    "DTXSID7020182",  # Bisphenol A
    "DTXSID2021315",  # Caffeine
    "DTXSID5020001"   # Acetic acid
]

results = synonym_client.get_synonyms_by_dtxsid_batch(dtxsids)

# Process each result
for data in results:
    dtxsid = data['dtxsid']
    valid_names = data['valid']
    print(f"\n{dtxsid}:")
    print(f"  Valid synonyms: {len(valid_names)}")
    print(f"  Sample names: {valid_names[:3]}")
```

## Response Structure

### Default Projection (Structured View)

```python
{
    "dtxsid": "DTXSID7020182",
    "pcCode": "string",
    "valid": [
        "Bisphenol A",
        "4,4'-Isopropylidenediphenol",
        "BPA"
    ],
    "good": [
        "Bisphenol A",
        "4,4'-Isopropylidenediphenol"
    ],
    "other": ["..."],
    "beilstein": ["..."],
    "alternateCasrn": ["..."],
    "deletedCasrn": ["..."]
}
```

**Fields:**
- `dtxsid` - DSSTox Substance Identifier
- `valid` - List of valid chemical names
- `good` - List of good quality names
- `other` - Other synonyms
- `beilstein` - Beilstein registry numbers
- `alternateCasrn` - Alternate CAS Registry Numbers
- `deletedCasrn` - Deleted CAS numbers
- `pcCode` - PC code

### CCD Projection (Flat List)

```python
[
    {
        "synonym": "Bisphenol A",
        "quality": "valid"
    },
    {
        "synonym": "BPA",
        "quality": "good"
    }
]
```

**Fields:**
- `synonym` - The synonym text
- `quality` - Quality rating (e.g., "valid", "good")

## Advanced Examples

### Finding Chemicals with Alternate CAS Numbers

```python
dtxsids = ["DTXSID7020182", "DTXSID2021315", "DTXSID5020001"]
results = synonym_client.get_synonyms_by_dtxsid_batch(dtxsids)

for data in results:
    alt_cas = data.get('alternateCasrn', [])
    if alt_cas:
        print(f"{data['dtxsid']}:")
        print(f"  Alternate CAS: {alt_cas}")
```

### Comparing Synonym Quality

```python
dtxsid = "DTXSID7020182"
data = synonym_client.get_synonyms_by_dtxsid(dtxsid)

valid_count = len(data.get('valid', []))
good_count = len(data.get('good', []))
other_count = len(data.get('other', []))

print(f"Synonym Quality Distribution:")
print(f"  Valid: {valid_count}")
print(f"  Good: {good_count}")
print(f"  Other: {other_count}")
```

### Working with Quality-Rated Synonyms

```python
# Get flat list with quality ratings
synonyms = synonym_client.get_synonyms_by_dtxsid(
    "DTXSID7020182",
    projection="ccd-synonyms"
)

# Group by quality
from collections import defaultdict
by_quality = defaultdict(list)

for item in synonyms:
    quality = item.get('quality', 'unknown')
    by_quality[quality].append(item['synonym'])

# Display grouped results
for quality, names in by_quality.items():
    print(f"\n{quality.upper()} ({len(names)}):")
    print(f"  {names[:5]}...")
```

### Integration with Other Modules

```python
from pycomptox import Chemical, ChemSynonym

search_client = Chemical()
synonym_client = ChemSynonym()

# Search for a chemical
results = search_client.search_by_name("Bisphenol")
dtxsid = results[0]['dtxsid']

# Get all its synonyms
synonyms = synonym_client.get_synonyms_by_dtxsid(dtxsid)

print(f"Found chemical: {results[0]['preferredName']}")
print(f"All valid names: {synonyms['valid']}")
```

## Rate Limiting

Control request frequency to avoid overwhelming the API:

```python
# Add delay between API calls
synonym_client = ChemSynonym(time_delay_between_calls=1.0)

# Now requests will be spaced 1 second apart
for dtxsid in dtxsid_list:
    synonyms = synonym_client.get_synonyms_by_dtxsid(dtxsid)
    process_synonyms(synonyms)
```

## Error Handling

```python
from pycomptox import ChemSynonym

synonym_client = ChemSynonym()

try:
    synonyms = synonym_client.get_synonyms_by_dtxsid("INVALID123")
except ValueError as e:
    print(f"Invalid DTXSID: {e}")
except PermissionError as e:
    print(f"API key error: {e}")
except RuntimeError as e:
    print(f"API error: {e}")
```

## API Methods Reference

### `get_synonyms_by_dtxsid(dtxsid, projection=None)`

Get synonyms for a single chemical.

**Parameters:**
- `dtxsid` (str) - DSSTox Substance Identifier
- `projection` (str, optional) - Projection type:
  - `None` (default): Structured view with categorized fields
  - `"ccd-synonyms"`: Flat list with quality ratings

**Returns:** Dict or List depending on projection

**Example:**
```python
synonyms = synonym_client.get_synonyms_by_dtxsid("DTXSID7020182")
```

### `get_synonyms_by_dtxsid_batch(dtxsid_list)`

Get synonyms for multiple chemicals (max 1000).

**Parameters:**
- `dtxsid_list` (List[str]) - List of DTXSIDs

**Returns:** List[Dict] - List of synonym data dictionaries

**Example:**
```python
dtxsids = ["DTXSID7020182", "DTXSID2021315"]
results = synonym_client.get_synonyms_by_dtxsid_batch(dtxsids)
```

## Best Practices

1. **Use batch methods** when querying multiple chemicals
2. **Enable rate limiting** for large-scale operations
3. **Cache results** to minimize API calls
4. **Handle errors** gracefully with try-except blocks
5. **Use projections** to get the data format you need

## Common Use Cases

### 1. Finding All Names for a Chemical

```python
dtxsid = "DTXSID7020182"
data = synonym_client.get_synonyms_by_dtxsid(dtxsid)

all_names = (
    data.get('valid', []) +
    data.get('good', []) +
    data.get('other', [])
)

unique_names = list(set(all_names))
print(f"Total unique names: {len(unique_names)}")
```

### 2. Exporting Synonym Data

```python
import csv

dtxsids = ["DTXSID7020182", "DTXSID2021315", "DTXSID5020001"]
results = synonym_client.get_synonyms_by_dtxsid_batch(dtxsids)

with open('synonyms.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['DTXSID', 'Synonym', 'Category'])
    
    for data in results:
        dtxsid = data['dtxsid']
        for category in ['valid', 'good', 'other']:
            for synonym in data.get(category, []):
                writer.writerow([dtxsid, synonym, category])
```

### 3. Building a Synonym Database

```python
synonym_db = {}

dtxsids = get_all_dtxsids()  # Your list of chemicals

for dtxsid in dtxsids:
    try:
        synonyms = synonym_client.get_synonyms_by_dtxsid(dtxsid)
        synonym_db[dtxsid] = synonyms
    except Exception as e:
        print(f"Error for {dtxsid}: {e}")
        continue

# Save to JSON
import json
with open('synonym_database.json', 'w') as f:
    json.dump(synonym_db, f, indent=2)
```

## Troubleshooting

### Issue: No synonyms returned

**Solution:** Some chemicals may have limited synonym data. Check all categories:

```python
data = synonym_client.get_synonyms_by_dtxsid(dtxsid)
for category in ['valid', 'good', 'other', 'beilstein', 'alternateCasrn']:
    synonyms = data.get(category, [])
    if synonyms:
        print(f"{category}: {len(synonyms)} items")
```

### Issue: Batch request fails

**Solution:** Ensure you're not exceeding the 1000 DTXSID limit:

```python
def batch_synonyms_chunked(dtxsids, chunk_size=1000):
    results = []
    for i in range(0, len(dtxsids), chunk_size):
        chunk = dtxsids[i:i+chunk_size]
        results.extend(synonym_client.get_synonyms_by_dtxsid_batch(chunk))
    return results
```

## See Also

- [Chemical Details API](CHEMICAL_DETAILS.md)
- [Chemical Properties API](CHEMICAL_PROPERTIES.md)
- [Setup & Configuration](MODERN_SETUP.md)
