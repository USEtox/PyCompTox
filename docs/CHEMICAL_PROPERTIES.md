# Chemical Properties API - PyCompTox v0.3.0

## Overview

The `ChemicalProperties` class provides access to chemical property data from the EPA CompTox Dashboard, including:

- **Property Summaries**: Aggregated physicochemical and fate properties
- **Predicted Properties**: QSAR model predictions  
- **Experimental Properties**: Measured values with citations
- **Environmental Fate**: Fate and transport properties

## Installation

```python
from pycomptox.chemical import ChemicalProperties

# Initialize client (API key auto-loaded)
props = ChemicalProperties()

# Or specify API key
props = ChemicalProperties(api_key="your_key_here")

# With rate limiting
props = ChemicalProperties(time_delay_between_calls=0.5)
```

## Methods Overview

### Property Summary Methods

#### `get_property_summary_by_dtxsid(dtxsid)`
Get summary of all physicochemical properties for a chemical.

**Returns:** List of property summaries with predicted and experimental ranges/medians

**Example:**
```python
summary = props.get_property_summary_by_dtxsid("DTXSID7020182")
for prop in summary:
    print(f"{prop['propName']}: {prop.get('experimentalMedian')} {prop.get('unit')}")
```

#### `get_summary_by_dtxsid_and_property(dtxsid, property_name)`
Get summary for a specific property.

**Example:**
```python
bp = props.get_summary_by_dtxsid_and_property("DTXSID7020182", "Boiling Point")
print(f"Boiling Point: {bp['experimentalMedian']} {bp['unit']}")
```

### Predicted Property Methods (QSAR)

#### `get_predicted_properties_by_dtxsid(dtxsid)`
Get all QSAR-predicted properties for a chemical.

**Returns:** List of predictions with model information and applicability domain

**Example:**
```python
predicted = props.get_predicted_properties_by_dtxsid("DTXSID7020182")
for prop in predicted:
    print(f"{prop['propName']}: {prop['propValue']} {prop.get('propUnit', '')}")
    print(f"  Model: {prop['modelName']}")
    print(f"  AD: {prop['adConclusion']}")
```

#### `get_predicted_property_by_name_and_range(property_name, min_value, max_value)`
Find chemicals with predicted property values in a range.

**Example:**
```python
# Find chemicals with Log P between 2 and 4
results = props.get_predicted_property_by_name_and_range("Log P", 2.0, 4.0)
print(f"Found {len(results)} chemicals")
```

#### `get_predicted_property_names()`
Get list of all available predicted property names.

**Example:**
```python
prop_names = props.get_predicted_property_names()
print(f"Available: {len(prop_names)} properties")
for prop in prop_names[:10]:
    print(f"  - {prop['propertyName']}")
```

#### `get_predicted_properties_by_dtxsid_batch(dtxsids)`
Batch retrieval for up to 1000 chemicals.

**Example:**
```python
dtxsids = ["DTXSID7020182", "DTXSID0020232", "DTXSID5020108"]
batch = props.get_predicted_properties_by_dtxsid_batch(dtxsids)

# Group by chemical
by_chem = {}
for prop in batch:
    by_chem.setdefault(prop['dtxsid'], []).append(prop)

for dtxsid, props_list in by_chem.items():
    print(f"{dtxsid}: {len(props_list)} properties")
```

### Experimental Property Methods

#### `get_experimental_properties_by_dtxsid(dtxsid)`
Get all experimental (measured) properties for a chemical.

**Returns:** List of measurements with sources, citations, and experimental conditions

**Example:**
```python
exp = props.get_experimental_properties_by_dtxsid("DTXSID7020182")
for prop in exp:
    print(f"{prop['propName']}: {prop['propValue']} {prop.get('propUnit', '')}")
    print(f"  Source: {prop.get('sourceName')}")
    print(f"  Temp: {prop.get('expDetailsTemperatureC')}°C")
    print(f"  Citation: {prop.get('briefCitation')}")
```

#### `get_experimental_properties_by_name_and_range(property_name, min_value, max_value)`
Find chemicals with experimental property values in a range.

**Example:**
```python
# Find chemicals with boiling point 100-200°C
results = props.get_experimental_properties_by_name_and_range(
    "Boiling Point", 100.0, 200.0
)
```

#### `get_all_experimental_property_names()`
Get list of all available experimental property names.

#### `get_experimental_properties_by_dtxsid_batch(dtxsids)`
Batch retrieval of experimental properties (max 1000).

### Environmental Fate Methods

#### `get_fate_summary_by_dtxsid(dtxsid)`
Get environmental fate and transport property summary.

**Example:**
```python
fate = props.get_fate_summary_by_dtxsid("DTXSID7020182")
for prop in fate:
    print(f"{prop['propName']}: {prop.get('predictedMedian')} {prop.get('unit')}")
```

#### `get_fate_summary_by_dtxsid_and_property(dtxsid, property_name)`
Get summary for a specific fate property.

**Example:**
```python
koc = props.get_fate_summary_by_dtxsid_and_property("DTXSID7020182", "Koc")
print(f"Koc: {koc['predictedMedian']} {koc['unit']}")
```

#### `get_fate_by_dtxsid_batch(dtxsids)`
Batch retrieval of fate properties (max 1000).

## Complete Workflow Example

```python
from pycomptox.chemical import Chemical, ChemicalProperties

# Initialize
searcher = Chemical()
props = ChemicalProperties()

# 1. Find chemical
results = searcher.search_by_exact_value("Bisphenol A")
dtxsid = results[0]['dtxsid']

# 2. Get property summary
summary = props.get_property_summary_by_dtxsid(dtxsid)
print(f"Property summaries: {len(summary)}")

# 3. Get predicted properties
predicted = props.get_predicted_properties_by_dtxsid(dtxsid)
print(f"Predicted properties: {len(predicted)}")

# 4. Get experimental properties
experimental = props.get_experimental_properties_by_dtxsid(dtxsid)
print(f"Experimental measurements: {len(experimental)}")

# 5. Get environmental fate
fate = props.get_fate_summary_by_dtxsid(dtxsid)
print(f"Fate properties: {len(fate)}")
```

## Batch Operations

For efficient data retrieval:

```python
# Search for multiple chemicals
names = ["Caffeine", "Aspirin", "Ibuprofen"]
dtxsids = []
for name in names:
    results = searcher.search_by_exact_value(name)
    if results:
        dtxsids.append(results[0]['dtxsid'])

# Get all predicted properties in one call
batch_predicted = props.get_predicted_properties_by_dtxsid_batch(dtxsids)

# Get all experimental properties
batch_experimental = props.get_experimental_properties_by_dtxsid_batch(dtxsids)

# Get all fate properties
batch_fate = props.get_fate_by_dtxsid_batch(dtxsids)
```

## Property Data Structure

### Property Summary
```python
{
    "propName": "Boiling Point",
    "unit": "°C",
    "experimentalRange": "200-220",
    "experimentalMedian": 210.0,
    "experimentalAverage": "210.5",
    "predictedRange": "205-215",
    "predictedMedian": 210.0,
    "predictedAverage": "210.2"
}
```

### Predicted Property
```python
{
    "id": 12345,
    "dtxsid": "DTXSID7020182",
    "dtxcid": "DTXCID30182",
    "propName": "Log P",
    "propValue": 3.32,
    "propUnit": "unitless",
    "modelName": "OPERA",
    "modelId": 1,
    "adMethod": "Local",
    "adConclusion": "Inside",
    "hasQmrf": true,
    "qmrfUrl": "https://..."
}
```

### Experimental Property
```python
{
    "id": 67890,
    "dtxsid": "DTXSID7020182",
    "propName": "Boiling Point",
    "propValue": 220.0,
    "propUnit": "°C",
    "sourceName": "ChemSpider",
    "lsCitation": "Author et al., 2020",
    "briefCitation": "Author 2020",
    "expDetailsTemperatureC": 25.0,
    "expDetailsPh": 7.0,
    "expDetailsPressureMmhg": 760.0,
    "publicSourceUrl": "https://..."
}
```

## Important Notes

### API Endpoint Availability

Some property endpoints may not be available depending on:
- API version
- API key permissions
- Endpoint implementation status

If you encounter 404 errors, the endpoint may not be available in the current API version.

### Rate Limiting

Use rate limiting for large batch operations:

```python
props = ChemicalProperties(time_delay_between_calls=0.5)
```

### Batch Size Limits

- Maximum 1000 DTXSIDs per batch request
- Requests with more than 1000 will raise `ValueError`

## Error Handling

```python
try:
    props_data = props.get_predicted_properties_by_dtxsid(dtxsid)
except ValueError as e:
    # 400 Bad Request or 404 Not Found
    print(f"Invalid request: {e}")
except PermissionError as e:
    # 401 Unauthorized
    print(f"API key issue: {e}")
except RuntimeError as e:
    # Network or rate limit errors
    print(f"Request failed: {e}")
```

## Jupyter Notebook Examples

See `notebooks/chemical_properties_examples.ipynb` for interactive examples including:
- Property summary analysis
- Predicted vs experimental comparison
- Batch operations
- Data visualization with pandas
- Complete workflow demonstrations

## API Reference

- **CompTox API Documentation**: https://comptox.epa.gov/ctx-api
- **Property Endpoints**: https://comptox.epa.gov/ctx-api/chemical/property
- **Fate Endpoints**: https://comptox.epa.gov/ctx-api/chemical/fate

## Related Documentation

- [Chemical Search Methods](BATCH_METHODS.md)
- [Chemical Details](CHEMICAL_DETAILS.md)
- [API Key Management](API_KEY_AND_RATE_LIMITING.md)
- [Quick Reference](QUICK_REFERENCE.md)
