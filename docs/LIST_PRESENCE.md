# List Presence

The `ListPresence` class provides access to chemical list presence data from the EPA CompTox Dashboard, showing which regulatory, screening, or reference lists contain specific chemicals.

## Overview

List presence data includes:

- **Regulatory Lists**: TSCA, REACH, DSL, etc.
- **Screening Lists**: ToxCast, Tox21, ECOTOX
- **Reference Lists**: Various chemical inventories and databases
- **List Metadata**: Descriptions, sources, and categorizations
- **Batch Operations**: Efficient processing of multiple chemicals

## Quick Start

```python
from pycomptox import ListPresence

# Initialize the client
list_presence = ListPresence()

# Get available list tags
tags = list_presence.list_presence_tags()

# Get list presence for a chemical
dtxsid = "DTXSID0020232"
presence = list_presence.list_presence_data_by_dtxsid(dtxsid)

# Batch operation
dtxsids = ["DTXSID0020232", "DTXSID7020182"]
batch_data = list_presence.list_presence_data_by_dtxsid_batch(dtxsids)
```

## API Methods

### List Presence Tags

```python
list_presence = ListPresence()
tags = list_presence.list_presence_tags()

for tag in tags:
    print(f"{tag.get('listName')}: {tag.get('listDescription')}")
```

### List Presence Data by DTXSID

```python
presence = list_presence.list_presence_data_by_dtxsid("DTXSID0020232")

for item in presence:
    print(f"List: {item.get('listName')}")
    print(f"Present: {item.get('isPresent')}")
    print(f"Category: {item.get('listCategory')}")
```

### Batch Operations

```python
dtxsids = ["DTXSID0020232", "DTXSID7020182"]
batch_data = list_presence.list_presence_data_by_dtxsid_batch(dtxsids)

for result in batch_data:
    print(f"{result.get('dtxsid')}: {result.get('listName')}")
```

## Use Cases

### Regulatory Status Check

```python
# Check if chemicals are on regulatory lists
list_presence = ListPresence()
dtxsid = "DTXSID0020232"
presence = list_presence.list_presence_data_by_dtxsid(dtxsid)

regulatory_lists = ["TSCA", "REACH", "DSL"]
for item in presence:
    if item.get('listName') in regulatory_lists and item.get('isPresent'):
        print(f"Found on {item.get('listName')}")
```

### Data Availability Assessment

```python
# Check which screening programs have data
screening_lists = ["ToxCast", "Tox21", "ECOTOX"]
presence = list_presence.list_presence_data_by_dtxsid("DTXSID0020232")

available_data = [
    item.get('listName') for item in presence
    if item.get('listName') in screening_lists and item.get('isPresent')
]
print(f"Data available in: {', '.join(available_data)}")
```

### Batch Analysis

```python
# Analyze list presence for multiple chemicals
chemicals = ["DTXSID0020232", "DTXSID7020182", "DTXSID3020268"]
batch_data = list_presence.list_presence_data_by_dtxsid_batch(chemicals)

# Group by list
from collections import defaultdict
by_list = defaultdict(list)
for result in batch_data:
    if result.get('isPresent'):
        by_list[result.get('listName')].append(result.get('dtxsid'))
```

## API Reference

For complete API details, see [ListPresence API Reference](api/listpresence.md).
