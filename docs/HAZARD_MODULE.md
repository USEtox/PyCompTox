# Hazard Module

The Hazard Module provides comprehensive access to toxicological hazard data from the EPA CompTox Dashboard. This module enables retrieval of various types of hazard information including toxicity values, study data, and health assessments.

## Overview

The hazard module contains multiple specialized classes for accessing different types of hazard data:

### Toxicity Reference Values

- **PPRTV**: Provisional Peer-Reviewed Toxicity Values for chemicals without established IRIS assessments
- **IRIS**: EPA Integrated Risk Information System assessments including RfDs, RfCs, and cancer assessments

### ToxRefDB (Toxicity Reference Database)

- **ToxRefDBEffects**: Dose-effect relationships from guideline toxicity studies
- **ToxRefDBSummary**: Study-level summaries including NOAEL, LOAEL, and endpoint information
- **ToxRefDBData**: Detailed dose-treatment group-effect information across all endpoints
- **ToxRefDBObservation**: Endpoint observation status distinguishing true negatives from missing data
- **ToxRefDBBatch**: Batch access to ToxRefDB data for multiple chemicals

### ToxValDB (Toxicity Values Database)

- **ToxValDB**: Comprehensive toxicity values database aggregating data from multiple sources
- **ToxValDBCancer**: Cancer hazard identification and weight-of-evidence data
- **ToxValDBSkinEye**: Skin and eye irritation/corrosion test data
- **ToxValDBGenetox**: Genotoxicity test data including Ames, Comet, micronucleus, and chromosomal aberration tests

### Health Assessments & Toxicokinetics

- **HAWC**: EPA Health Assessment Workspace Collaborative project links
- **ADMEIVIVE**: Toxicokinetics data (Absorption, Distribution, Metabolism, Excretion) including in vitro, in vivo, and in silico predictions

## Quick Start

```python
from pycomptox.hazard import (
    PPRTV, IRIS, ToxRefDBEffects, ToxRefDBSummary,
    ToxValDB, ToxValDBCancer, ToxValDBGenetox,
    ADMEIVIVE, HAWC
)

# Get IRIS assessment data
iris = IRIS()
iris_data = iris.get_data_by_dtxsid("DTXSID7020637")  # Formaldehyde

# Get genotoxicity data
genetox = ToxValDBGenetox()
genetox_summary = genetox.get_summary_by_dtxsid("DTXSID0021125")  # Benzene

# Get toxicokinetics data
adme = ADMEIVIVE()
adme_data = adme.get_all_data_by_dtxsid_ccd_projection("DTXSID7020182")  # Bisphenol A

# Get ToxRefDB dose-effect data
toxref = ToxRefDBEffects()
effects = toxref.get_data_by_dtxsid("DTXSID1037806")

# Batch operations
from pycomptox.hazard import ToxRefDBBatch
batch = ToxRefDBBatch()
dtxsids = ["DTXSID0021125", "DTXSID7020182", "DTXSID0020032"]
batch_data = batch.get_data_by_dtxsid_batch(dtxsids)
```

## Key Features

### Comprehensive Hazard Data Coverage

- **Toxicity Values**: Reference doses (RfDs), reference concentrations (RfCs), NOAEL, LOAEL values
- **Study Data**: Guideline toxicity studies with detailed dose-response information
- **Health Effects**: Cancer assessments, reproductive/developmental toxicity, systemic effects
- **Specialized Testing**: Genotoxicity, skin/eye irritation, neurotoxicity
- **Toxicokinetics**: ADME parameters, clearance rates, bioavailability

### Data Quality Features

- **Observation Status**: Distinguishes tested endpoints (true negatives) from untested endpoints (missing data)
- **Weight of Evidence**: Cancer hazard identification with strength of evidence assessments
- **Guideline Compliance**: Study data mapped to regulatory guideline requirements
- **Multiple Sources**: Data aggregated from ToxRefDB, ToxValDB, IRIS, HAWC, httk, and CvTdb

### Flexible Access Patterns

- **Single Chemical Queries**: Get all hazard data for one chemical
- **Batch Queries**: Retrieve data for up to 200 chemicals in one request
- **Study-Based Access**: Query by study type or specific study ID
- **Filtered Results**: Use projections for dashboard-specific data formats

## Common Use Cases

### Hazard Assessment Workflow

```python
from pycomptox.hazard import ToxValDB, ToxValDBCancer, ToxValDBGenetox, IRIS

dtxsid = "DTXSID7020182"  # Bisphenol A

# 1. Get general toxicity values
toxval = ToxValDB()
tox_data = toxval.get_data_by_dtxsid(dtxsid)

# 2. Check for cancer hazard
cancer = ToxValDBCancer()
cancer_data = cancer.get_data_by_dtxsid(dtxsid)

# 3. Check genotoxicity
genetox = ToxValDBGenetox()
genetox_data = genetox.get_summary_by_dtxsid(dtxsid)

# 4. Get EPA IRIS assessment if available
iris = IRIS()
iris_data = iris.get_data_by_dtxsid(dtxsid)

# Analyze combined data for comprehensive hazard profile
```

### Comparative Toxicity Analysis

```python
from pycomptox.hazard import ToxRefDBSummary

# Compare similar chemicals
dtxsids = ["DTXSID0021125", "DTXSID7020182", "DTXSID0020032"]

toxref = ToxRefDBSummary()

for dtxsid in dtxsids:
    summary = toxref.get_data_by_dtxsid(dtxsid)
    
    if summary:
        # Find lowest NOAEL across all studies
        noaels = [s.get('noael') for s in summary if s.get('noael')]
        if noaels:
            print(f"{dtxsid}: Lowest NOAEL = {min(noaels)}")
```

### Toxicokinetics Modeling

```python
from pycomptox.hazard import ADMEIVIVE

adme = ADMEIVIVE()

# Get all ADME parameters
data = adme.get_all_data_by_dtxsid_ccd_projection("DTXSID7020182")

# Extract key parameters for modeling
if data:
    params = {}
    for record in data:
        param_name = record.get('parameter')
        param_value = record.get('value')
        if param_name and param_value:
            params[param_name] = param_value
    
    # Use in PBPK/toxicokinetic models
    print(f"Clearance: {params.get('Clint', 'N/A')}")
    print(f"Fraction Unbound: {params.get('Fup', 'N/A')}")
    print(f"Volume of Distribution: {params.get('Vd', 'N/A')}")
```

## Data Sources

The hazard module integrates data from multiple authoritative sources:

- **ToxRefDB**: EPA's Toxicity Reference Database of guideline studies
- **ToxValDB**: Aggregated toxicity values from multiple databases
- **IRIS**: EPA Integrated Risk Information System
- **HAWC**: Health Assessment Workspace Collaborative
- **httk**: High-Throughput Toxicokinetics R package
- **CvTdb**: Concentration vs. Time database
- **invivoPKfit**: In vivo pharmacokinetics fitting package

## Best Practices

### Caching

All hazard classes support caching to minimize API calls:

```python
from pycomptox.hazard import ToxRefDBEffects

# Enable caching (default)
toxref = ToxRefDBEffects()
data1 = toxref.get_data_by_dtxsid("DTXSID1037806", use_cache=True)

# Subsequent calls use cached data
data2 = toxref.get_data_by_dtxsid("DTXSID1037806", use_cache=True)
```

### Batch Processing

Use batch methods when querying multiple chemicals:

```python
from pycomptox.hazard import ToxValDBGenetox

genetox = ToxValDBGenetox()

# Efficient batch query (single API call)
dtxsids = ["DTXSID0021125", "DTXSID7020182", "DTXSID0020032"]
batch_data = genetox.get_summary_by_dtxsid_batch(dtxsids)

# Less efficient individual queries (multiple API calls)
# for dtxsid in dtxsids:
#     data = genetox.get_summary_by_dtxsid(dtxsid)
```

### Error Handling

```python
from pycomptox.hazard import IRIS

iris = IRIS()

try:
    data = iris.get_data_by_dtxsid("DTXSID7020637")
    if data:
        print(f"Found IRIS assessment")
    else:
        print("No IRIS assessment available")
except ValueError as e:
    print(f"Invalid input: {e}")
except PermissionError as e:
    print(f"API key issue: {e}")
except RuntimeError as e:
    print(f"API error: {e}")
```

## API Classes Reference

For detailed documentation on each class, see:

- [PPRTV](api/pprtv.md)
- [IRIS](api/iris.md)
- [ToxRefDBEffects](api/toxrefdbeffects.md)
- [ToxRefDBSummary](api/toxrefdbsummary.md)
- [ToxRefDBData](api/toxrefdbdata.md)
- [ToxRefDBObservation](api/toxrefdbobservation.md)
- [ToxRefDBBatch](api/toxrefdbbatch.md)
- [ToxValDB](api/toxvaldb.md)
- [ToxValDBCancer](api/toxvaldbcancer.md)
- [ToxValDBSkinEye](api/toxvaldbskineye.md)
- [ToxValDBGenetox](api/toxvaldbgenetox.md)
- [ADMEIVIVE](api/admeivive.md)
- [HAWC](api/hawc.md)

## Related Documentation

- [API Key & Rate Limiting](API_KEY_AND_RATE_LIMITING.md)
- [Caching System](CACHING.md)
- [Batch Methods](BATCH_METHODS.md)
- [Best Practices](best_practices.md)
