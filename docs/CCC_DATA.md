# Chemical and Products Categories (CCC) Data

The `CCCData` class provides access to Chemical and Products Categories data from the EPA CompTox Dashboard, including Product Use Categories (PUC), production volume data, biomonitoring information, and functional use details.

## Overview

Chemical and Products Categories data helps understand how chemicals are used in commerce and products. This includes:

- **Product Use Categories (PUC)**: Hierarchical classification of product types
- **Production Volume**: Manufacturing and import volume data
- **Biomonitoring Data**: Chemical occurrence in biological samples
- **General Use Keywords**: Descriptive terms for chemical uses
- **Functional Use**: Reported functional applications
- **Weight Fractions**: Chemical concentration in products

## Quick Start

```python
from pycomptox import CCCData

# Initialize the client
ccc = CCCData()

# Get product use categories for a chemical
dtxsid = "DTXSID7020182"  # Bisphenol A
puc_data = ccc.product_use_category_by_dtxsid(dtxsid)

# Get production volume data
volume_data = ccc.production_volume_by_dtxsid(dtxsid)

# Get biomonitoring data for a specific CCD
biomonitoring = ccc.biomonitoring_data_by_dtxsid_and_ccd(
    dtxsid, 
    ccd="NHANES"
)
```

## API Methods

### Product Use Categories

Get Product Use Category (PUC) classifications for a chemical:

```python
ccc = CCCData()
puc_data = ccc.product_use_category_by_dtxsid("DTXSID7020182")

for puc in puc_data:
    print(f"PUC Code: {puc.get('pucCode')}")
    print(f"Description: {puc.get('description')}")
    print(f"Level: {puc.get('level')}")
```

**Returns**: List of dictionaries containing PUC codes, descriptions, and hierarchical information.

### Production Volume

Retrieve manufacturing and import volume data:

```python
volume_data = ccc.production_volume_by_dtxsid("DTXSID0020232")

for record in volume_data:
    print(f"Year: {record.get('year')}")
    print(f"Volume Range: {record.get('volumeRange')}")
    print(f"Source: {record.get('source')}")
```

**Returns**: Production volume records including year, volume range, and data source.

### Biomonitoring Data

Get biomonitoring data for a chemical from a specific Chemical Categories Database (CCD):

```python
# Get NHANES biomonitoring data
nhanes_data = ccc.biomonitoring_data_by_dtxsid_and_ccd(
    "DTXSID7020182",
    ccd="NHANES"
)

for sample in nhanes_data:
    print(f"Matrix: {sample.get('matrix')}")
    print(f"Detection Frequency: {sample.get('detectionFrequency')}")
    print(f"Median Concentration: {sample.get('medianConcentration')}")
```

**Parameters**:
- `dtxsid`: Chemical identifier
- `ccd`: Chemical Categories Database name (e.g., "NHANES", "ECOTOX")

**Returns**: Biomonitoring records with detection frequencies and concentration data.

### General Use Keywords

Retrieve descriptive keywords for chemical uses:

```python
keywords = ccc.general_use_keywords_by_dtxsid("DTXSID0020232")

for keyword in keywords:
    print(f"Keyword: {keyword.get('keyword')}")
    print(f"Category: {keyword.get('category')}")
```

**Returns**: List of use keywords and their categories.

### Reported Functional Use

Get reported functional applications for a chemical:

```python
functional_use = ccc.reported_functional_use_by_dtxsid("DTXSID7020182")

for use in functional_use:
    print(f"Function: {use.get('function')}")
    print(f"Product Type: {use.get('productType')}")
    print(f"Source: {use.get('source')}")
```

**Returns**: Functional use information including product types and data sources.

### Chemical Weight Fractions

Retrieve chemical concentration data in products:

```python
weight_fractions = ccc.chemical_weight_fraction_by_dtxsid("DTXSID0020232")

for fraction in weight_fractions:
    print(f"Product: {fraction.get('product')}")
    print(f"Min Weight %: {fraction.get('minWeightPercent')}")
    print(f"Max Weight %: {fraction.get('maxWeightPercent')}")
```

**Returns**: Weight fraction data showing chemical concentrations in various products.

## Configuration

### API Key Setup

```python
from pycomptox import save_api_key, CCCData

# Save your API key (one-time setup)
save_api_key("your-api-key-here")

# Or provide at initialization
ccc = CCCData(api_key="your-api-key-here")
```

### Rate Limiting

Add delays between API calls to avoid rate limiting:

```python
# Add 1-second delay between requests
ccc = CCCData(time_delay_between_calls=1.0)
```

### Custom Base URL

Use a different API endpoint:

```python
ccc = CCCData(base_url="https://custom-api-endpoint.gov/")
```

## Data Structure Examples

### Product Use Category Response

```python
[
    {
        "dtxsid": "DTXSID7020182",
        "pucCode": "PC-1",
        "pucLevel1": "Adhesives and Sealants",
        "pucLevel2": "Adhesive",
        "description": "Products used to bond materials together",
        "level": 2
    }
]
```

### Production Volume Response

```python
[
    {
        "dtxsid": "DTXSID0020232",
        "year": 2020,
        "volumeRange": "1M - 10M pounds",
        "source": "CDR",
        "productionType": "Manufactured"
    }
]
```

## Error Handling

```python
from pycomptox import CCCData

ccc = CCCData()

try:
    data = ccc.product_use_category_by_dtxsid("DTXSID7020182")
except PermissionError as e:
    print(f"Invalid API key: {e}")
except ValueError as e:
    print(f"Invalid input or no data found: {e}")
except RuntimeError as e:
    print(f"API error: {e}")
```

## Best Practices

1. **Cache Results**: Store retrieved data locally to minimize API calls
2. **Rate Limiting**: Use `time_delay_between_calls` for large batches
3. **Validate Input**: Always check DTXSID format before making requests
4. **Handle Missing Data**: Some chemicals may not have all data types available

## Use Cases

### Product Safety Assessment

```python
ccc = CCCData()
dtxsid = "DTXSID7020182"

# Get product categories
products = ccc.product_use_category_by_dtxsid(dtxsid)
print(f"Found in {len(products)} product categories")

# Get weight fractions
concentrations = ccc.chemical_weight_fraction_by_dtxsid(dtxsid)
max_concentration = max(c.get('maxWeightPercent', 0) for c in concentrations)
print(f"Maximum concentration: {max_concentration}%")
```

### Exposure Assessment

```python
# Get biomonitoring data
biodata = ccc.biomonitoring_data_by_dtxsid_and_ccd(
    "DTXSID7020182",
    ccd="NHANES"
)

# Get production volume
volume = ccc.production_volume_by_dtxsid("DTXSID7020182")

# Combined analysis for exposure potential
print(f"Detection frequency: {biodata[0].get('detectionFrequency')}")
print(f"Production volume: {volume[0].get('volumeRange')}")
```

## Related Documentation

- [Product Data API](PRODUCT_DATA.md) - Consumer product information
- [Functional Use API](FUNCTIONAL_USE.md) - Detailed functional use predictions
- [List Presence API](LIST_PRESENCE.md) - Chemical presence on regulatory lists

## API Reference

For complete API details, see [CCCData API Reference](api/cccdata.md).
