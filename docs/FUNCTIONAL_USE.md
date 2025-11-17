# Functional Use Data

The `FunctionalUse` class provides access to functional use data from the EPA CompTox Dashboard, describing how chemicals are used in products and applications.

## Overview

Functional use data includes:

- **Functional Use by Chemical**: Reported functional applications
- **Functional Use Probability**: Predicted likelihood of various uses
- **Functional Use Categories**: Complete taxonomy of use categories
- **Batch Operations**: Efficient processing of multiple chemicals

## Quick Start

```python
from pycomptox import FunctionalUse

# Initialize the client
func_use = FunctionalUse()

# Get functional use data for a chemical
dtxsid = "DTXSID0020232"
uses = func_use.functiona_use_by_dtxsid(dtxsid)

# Get predicted probabilities
probabilities = func_use.functional_use_probability_by_dtxsid(dtxsid)

# Get all categories
categories = func_use.functiona_use_categories()
```

## API Methods

### Functional Use by DTXSID

```python
func_use = FunctionalUse()
uses = func_use.functiona_use_by_dtxsid("DTXSID0020232")

for use in uses:
    print(f"Function: {use.get('harmonizedFunctionalUse')}")
    print(f"Category: {use.get('category')}")
    print(f"Source: {use.get('dataSource')}")
```

### Functional Use Probability

```python
probabilities = func_use.functional_use_probability_by_dtxsid("DTXSID0020232")

for prob in probabilities:
    print(f"{prob.get('functionalUse')}: {prob.get('probability'):.2%}")
```

### Functional Use Categories

```python
categories = func_use.functiona_use_categories()

for cat in categories:
    print(f"{cat.get('category')}: {cat.get('description')}")
```

### Batch Operations

```python
dtxsids = ["DTXSID0020232", "DTXSID7020182"]
batch_data = func_use.functional_use_by_dtxsid_batch(dtxsids)
```

## API Reference

For complete API details, see [FunctionalUse API Reference](api/functionaluse.md).
