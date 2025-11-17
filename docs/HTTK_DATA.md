# HTTK Data

The `HTTKData` class provides access to High-Throughput Toxicokinetics (HTTK) data from the EPA CompTox Dashboard, including pharmacokinetic parameters and ADME properties.

## Overview

HTTK data includes:

- **Pharmacokinetic Parameters**: Volume of distribution, clearance, half-life
- **ADME Properties**: Absorption, distribution, metabolism, excretion
- **Model Parameters**: For toxicokinetic modeling and simulation
- **Batch Operations**: Efficient processing of multiple chemicals

## Quick Start

```python
from pycomptox import HTTKData

# Initialize the client
httk = HTTKData()

# Get HTTK data for a chemical
dtxsid = "DTXSID0020232"
httk_params = httk.httk_data_by_dtxsid(dtxsid)

# Batch operation
dtxsids = ["DTXSID0020232", "DTXSID7020182"]
batch_data = httk.httk_data_by_dtxsid_batch(dtxsids)
```

## API Methods

### HTTK Data by DTXSID

```python
httk = HTTKData()
params = httk.httk_data_by_dtxsid("DTXSID0020232")

for param in params:
    print(f"Parameter: {param.get('parameterName')}")
    print(f"Value: {param.get('parameterValue')}")
    print(f"Units: {param.get('parameterUnits')}")
    print(f"Model: {param.get('modelName')}")
```

### Batch Operations

```python
dtxsids = ["DTXSID0020232", "DTXSID7020182"]
batch_data = httk.httk_data_by_dtxsid_batch(dtxsids)

for result in batch_data:
    print(f"{result.get('dtxsid')}: {result.get('parameterName')}")
```

## Use Cases

### Toxicokinetic Modeling

```python
# Get PK parameters for dose-response modeling
httk = HTTKData()
dtxsid = "DTXSID0020232"
pk_data = httk.httk_data_by_dtxsid(dtxsid)

# Extract key parameters
for param in pk_data:
    if param.get('parameterName') == 'Vdist':
        vd = param.get('parameterValue')
    elif param.get('parameterName') == 'Clint':
        clearance = param.get('parameterValue')
```

### Batch Analysis

```python
# Analyze HTTK data for multiple chemicals
chemicals = ["DTXSID0020232", "DTXSID7020182", "DTXSID3020268"]
httk = HTTKData()
results = httk.httk_data_by_dtxsid_batch(chemicals)

# Group by chemical
from collections import defaultdict
by_chemical = defaultdict(list)
for result in results:
    by_chemical[result.get('dtxsid')].append(result)
```

## API Reference

For complete API details, see [HTTKData API Reference](api/httkdata.md).
