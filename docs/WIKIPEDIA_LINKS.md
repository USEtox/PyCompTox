# Wikipedia Links API

The `WikiLink` class provides access to Wikipedia GHS (Globally Harmonized System) Safety data availability for chemicals in the CompTox Dashboard.

## Overview

The WikiLink API allows you to check if Wikipedia has GHS Safety data for chemicals and retrieve the corresponding Wikipedia URLs. This is useful for:
- Finding Wikipedia safety information links
- Checking availability of GHS classification data
- Accessing standardized safety data documentation

## Quick Start

```python
from pycomptox import WikiLink

# Initialize client
wiki = WikiLink()

# Check if Wikipedia has GHS data
result = wiki.check_existence_by_dtxsid("DTXSID7020182")
if result['safetyUrl']:
    print(f"Wikipedia GHS Safety: {result['safetyUrl']}")
```

## Available Methods

### 1. Check Wikipedia Existence by DTXSID

Check if Wikipedia has GHS Safety data for a single chemical.

```python
result = wiki.check_existence_by_dtxsid("DTXSID7020182")
```

**Returns:**
```python
{
    'dtxsid': 'DTXSID7020182',
    'safetyUrl': 'https://en.wikipedia.org/wiki/IISBACLAFKSPIT-UHFFFAOYSA-N#section=wiki-Classification'
}
```

**Fields:**
- `dtxsid`: DSSTox Substance Identifier
- `safetyUrl`: Wikipedia URL for GHS safety data (empty string if not available)

### 2. Check Wikipedia Existence (Batch)

Check Wikipedia GHS data availability for multiple chemicals (up to 1000).

```python
dtxsids = ["DTXSID7020182", "DTXSID2021315", "DTXSID5020001"]
results = wiki.check_existence_by_dtxsid_batch(dtxsids)

for result in results:
    status = "✓" if result['safetyUrl'] else "✗"
    print(f"{status} {result['dtxsid']}")
```

## Complete Examples

### Example 1: Basic Wikipedia Check

```python
from pycomptox import WikiLink

wiki = WikiLink()

# Check for Bisphenol A
dtxsid = "DTXSID7020182"
result = wiki.check_existence_by_dtxsid(dtxsid)

print(f"Chemical: {dtxsid}")
if result['safetyUrl']:
    print(f"✓ Wikipedia GHS data available")
    print(f"  URL: {result['safetyUrl']}")
else:
    print(f"✗ No Wikipedia GHS data")
```

### Example 2: Batch Wikipedia Check

```python
from pycomptox import WikiLink

wiki = WikiLink()

# Check multiple chemicals
chemicals = [
    "DTXSID7020182",  # Bisphenol A
    "DTXSID2021315",  # Caffeine
    "DTXSID5020001",  # 1,2,3-Trichloropropane
    "DTXSID3020637",  # Formaldehyde
    "DTXSID6020139"   # Benzene
]

results = wiki.check_existence_by_dtxsid_batch(chemicals)

# Count availability
with_data = sum(1 for r in results if r['safetyUrl'])
print(f"Wikipedia GHS data available: {with_data}/{len(results)}")

# Show details
for result in results:
    if result['safetyUrl']:
        print(f"✓ {result['dtxsid']}")
        print(f"  {result['safetyUrl']}")
    else:
        print(f"✗ {result['dtxsid']}: No data")
```

### Example 3: Integration with Chemical Search

```python
from pycomptox.chemical import Chemical
from pycomptox.links import WikiLink

# Search for chemicals
chem = Chemical()
results = chem.search_by_starting_value("phthalate")

# Check Wikipedia availability
wiki = WikiLink()
dtxsids = [r['dtxsid'] for r in results[:10]]
wiki_data = wiki.check_existence_by_dtxsid_batch(dtxsids)

# Combine results
for search_result in results[:10]:
    dtxsid = search_result['dtxsid']
    wiki_result = next((w for w in wiki_data if w['dtxsid'] == dtxsid), None)
    
    print(f"{search_result['preferredName']}")
    if wiki_result and wiki_result['safetyUrl']:
        print(f"  Wikipedia: {wiki_result['safetyUrl']}")
    else:
        print(f"  Wikipedia: No GHS data")
```

### Example 4: Filter Chemicals with Wikipedia Data

```python
from pycomptox import WikiLink

wiki = WikiLink()

# Get batch of chemicals
dtxsids = ["DTXSID7020182", "DTXSID2021315", "DTXSID5020001",
           "DTXSID3020637", "DTXSID6020139"]

results = wiki.check_existence_by_dtxsid_batch(dtxsids)

# Filter to only chemicals with Wikipedia data
with_wiki = [r for r in results if r['safetyUrl']]

print(f"Chemicals with Wikipedia GHS data: {len(with_wiki)}")
for item in with_wiki:
    print(f"  {item['dtxsid']}: {item['safetyUrl']}")
```

### Example 5: Create Wikipedia Links Dataset

```python
from pycomptox import WikiLink
import pandas as pd

wiki = WikiLink()

# Get data for chemicals of interest
dtxsids = ["DTXSID7020182", "DTXSID2021315", "DTXSID5020001"]
results = wiki.check_existence_by_dtxsid_batch(dtxsids)

# Convert to DataFrame
df = pd.DataFrame(results)
df['has_wiki'] = df['safetyUrl'].apply(lambda x: bool(x))

print("Wikipedia Data Availability:")
print(df)

# Export to CSV
df.to_csv('wikipedia_links.csv', index=False)
```

### Example 6: Compare Chemical Classes

```python
from pycomptox import WikiLink

wiki = WikiLink()

# Define chemical classes
chemical_classes = {
    'Bisphenols': ['DTXSID7020182', 'DTXSID4020216', 'DTXSID1020265'],
    'Phthalates': ['DTXSID5020607', 'DTXSID6021232', 'DTXSID2021781'],
}

for class_name, dtxsids in chemical_classes.items():
    results = wiki.check_existence_by_dtxsid_batch(dtxsids)
    with_data = sum(1 for r in results if r['safetyUrl'])
    coverage = (with_data / len(results)) * 100
    
    print(f"{class_name}: {with_data}/{len(results)} ({coverage:.0f}%) have Wikipedia GHS data")
```

### Example 7: Complete Safety Profile

```python
from pycomptox.chemical import Chemical, ChemicalDetails
from pycomptox.links import WikiLink

dtxsid = "DTXSID7020182"

# Get basic info
chem = Chemical()
search = chem.search_by_exact_value(dtxsid)

# Get detailed info
details = ChemicalDetails()
info = details.data_by_dtxsid(dtxsid)

# Get Wikipedia link
wiki = WikiLink()
wiki_data = wiki.check_existence_by_dtxsid(dtxsid)

# Display complete profile
print(f"Chemical Profile: {info['preferredName']}")
print(f"DTXSID: {dtxsid}")
print(f"CASRN: {info.get('casrn', 'N/A')}")
print(f"Formula: {info.get('molFormula', 'N/A')}")

if wiki_data['safetyUrl']:
    print(f"\nWikipedia GHS Safety Data:")
    print(f"  {wiki_data['safetyUrl']}")
else:
    print(f"\nNo Wikipedia GHS safety data available")
```

## Data Structure

### WikiLink Response

```python
{
    'dtxsid': str,    # DSSTox Substance Identifier
    'safetyUrl': str  # Wikipedia URL (or empty string if not available)
}
```

## Error Handling

```python
from pycomptox import WikiLink

wiki = WikiLink()

try:
    result = wiki.check_existence_by_dtxsid("DTXSID7020182")
    if result['safetyUrl']:
        print(f"Has data: {result['safetyUrl']}")
    else:
        print("No Wikipedia GHS data available")
except ValueError as e:
    print(f"Invalid DTXSID: {e}")
except RuntimeError as e:
    print(f"Network error: {e}")
```

## Rate Limiting

Configure rate limiting for bulk operations:

```python
# Add 0.5 second delay between requests
wiki = WikiLink(time_delay_between_calls=0.5)

# Make multiple requests - automatically rate limited
for dtxsid in dtxsid_list:
    result = wiki.check_existence_by_dtxsid(dtxsid)
```

## Batch Request Limits

- Maximum 1000 DTXSIDs per batch request
- For larger datasets, split into multiple batches

```python
def check_wiki_in_batches(dtxsids, batch_size=1000):
    """Check Wikipedia data in batches."""
    wiki = WikiLink()
    all_results = []
    
    for i in range(0, len(dtxsids), batch_size):
        batch = dtxsids[i:i + batch_size]
        results = wiki.check_existence_by_dtxsid_batch(batch)
        all_results.extend(results)
    
    return all_results
```

## Understanding Wikipedia GHS Links

Wikipedia GHS Safety data includes:
- Hazard statements (H-statements)
- Precautionary statements (P-statements)
- Signal words (Danger, Warning)
- Pictograms (symbols)

The URLs typically point to the chemical's Wikipedia page with a direct link to the GHS Classification section.

## See Also

- [Chemical Search API](CHEMICAL_SEARCH.md)
- [Chemical Details API](CHEMICAL_DETAILS.md)
- [Chemical Properties API](CHEMICAL_PROPERTIES.md)
- [Extra Data API](EXTRA_DATA.md)
- [Installation Guide](INSTALLATION.md)
