# Molecular Modeling Database (MMDB)

The `MMDB` class provides access to the Molecular Modeling Database from the EPA CompTox Dashboard, which contains environmental monitoring and measurement data for chemicals detected in various environmental media.

## Overview

The MMDB aggregates chemical occurrence data from environmental monitoring programs, providing:

- **Single-Sample Records**: Individual environmental measurements
- **Aggregate Records**: Summary statistics across multiple samples
- **Medium-Specific Data**: Organized by environmental medium (water, air, soil, etc.)
- **Harmonized Data**: Standardized across multiple monitoring programs

## Quick Start

```python
from pycomptox import MMDB

# Initialize the client
mmdb = MMDB()

# Get single-sample data for surface water
water_samples = mmdb.harmonized_single_sample_by_medium("surface water")

# Get data for a specific chemical
chemical_data = mmdb.harmonized_single_sample_by_dtxsid("DTXSID7020182")

# Get available medium categories
mediums = mmdb.searchable_harmonized_medium_categories()

# Get aggregate records
aggregates = mmdb.harmonized_aggregate_records_by_medium("surface water")
```

## API Methods

### Harmonized Single-Sample by Medium

Retrieve individual environmental sample measurements filtered by medium type:

```python
mmdb = MMDB()

# Get surface water samples (page 1)
samples = mmdb.harmonized_single_sample_by_medium("surface water")

print(f"Total samples: {samples.get('totalRecords')}")
print(f"Current page: {samples.get('pageNumber')}")

for sample in samples.get('data', []):
    print(f"Chemical: {sample.get('chemicalName')}")
    print(f"Concentration: {sample.get('concentration')} {sample.get('units')}")
    print(f"Location: {sample.get('location')}")
    print(f"Date: {sample.get('sampleDate')}")
```

**Parameters**:
- `medium`: Medium type (e.g., 'surface water', 'air', 'soil', 'groundwater')
- `page_number`: Page number for pagination (default: 1)

**Returns**: Paginated dictionary with sample records and metadata.

### Pagination Support

Handle large datasets with pagination:

```python
mmdb = MMDB()
medium = "surface water"
all_samples = []

# Get first page
page_1 = mmdb.harmonized_single_sample_by_medium(medium, page_number=1)
all_samples.extend(page_1.get('data', []))

# Get additional pages
total_pages = page_1.get('totalPages', 1)
for page in range(2, total_pages + 1):
    page_data = mmdb.harmonized_single_sample_by_medium(medium, page_number=page)
    all_samples.extend(page_data.get('data', []))

print(f"Retrieved {len(all_samples)} total samples")
```

### Harmonized Single-Sample by DTXSID

Get all environmental samples for a specific chemical:

```python
# Get samples for Bisphenol A
bpa_samples = mmdb.harmonized_single_sample_by_dtxsid("DTXSID7020182")

# Analyze by medium
from collections import Counter
medium_counts = Counter(s.get('medium') for s in bpa_samples)
print("Detection by medium:")
for medium, count in medium_counts.most_common():
    print(f"  {medium}: {count} samples")
```

**Returns**: List of all sample records for the specified chemical.

### Searchable Harmonized Medium Categories

Get all available medium types and their definitions:

```python
mmdb = MMDB()
mediums = mmdb.searchable_harmonized_medium_categories()

print("Available environmental media:")
for medium in mediums:
    print(f"  {medium.get('name')}: {medium.get('definition')}")
```

Common medium types include:
- `surface water` - Rivers, lakes, streams
- `groundwater` - Subsurface water
- `air` - Atmospheric samples
- `soil` - Terrestrial samples
- `sediment` - Aquatic sediments
- `biota` - Biological samples

**Returns**: List of medium categories with names and definitions.

### Harmonized Aggregate Records by Medium

Retrieve summary statistics aggregated across multiple samples:

```python
mmdb = MMDB()

# Get aggregate data for surface water
aggregates = mmdb.harmonized_aggregate_records_by_medium("surface water")

for agg in aggregates.get('data', []):
    print(f"Chemical: {agg.get('chemicalName')}")
    print(f"Median Concentration: {agg.get('medianConcentration')}")
    print(f"95th Percentile: {agg.get('percentile95')}")
    print(f"Detection Frequency: {agg.get('detectionFrequency')}%")
    print(f"Number of Samples: {agg.get('sampleCount')}")
```

**Parameters**:
- `medium`: Medium type
- `page_number`: Page number for pagination (default: 1)

**Returns**: Paginated dictionary with aggregate statistics.

## Configuration

### API Key Setup

```python
from pycomptox import save_api_key, MMDB

# Save your API key (one-time setup)
save_api_key("your-api-key-here")

# Or provide at initialization
mmdb = MMDB(api_key="your-api-key-here")
```

### Rate Limiting

Add delays between API calls:

```python
# Add 0.5-second delay between requests
mmdb = MMDB(time_delay_between_calls=0.5)
```

## Data Structure Examples

### Single-Sample Response

```python
{
    "totalRecords": 15420,
    "pageNumber": 1,
    "totalPages": 155,
    "pageSize": 100,
    "data": [
        {
            "dtxsid": "DTXSID7020182",
            "chemicalName": "Bisphenol A",
            "casrn": "80-05-7",
            "medium": "surface water",
            "concentration": 0.145,
            "units": "µg/L",
            "detectionLimit": 0.01,
            "detectionStatus": "detected",
            "location": "Mississippi River",
            "latitude": 38.6270,
            "longitude": -90.1994,
            "sampleDate": "2020-06-15",
            "monitoringProgram": "NAWQA",
            "sampleId": "USGS-2020-1234"
        }
    ]
}
```

### Aggregate Response

```python
{
    "data": [
        {
            "dtxsid": "DTXSID7020182",
            "chemicalName": "Bisphenol A",
            "medium": "surface water",
            "sampleCount": 1523,
            "detectionFrequency": 67.2,
            "minConcentration": 0.001,
            "medianConcentration": 0.085,
            "meanConcentration": 0.123,
            "percentile95": 0.450,
            "maxConcentration": 2.34,
            "units": "µg/L"
        }
    ]
}
```

## Error Handling

```python
from pycomptox import MMDB

mmdb = MMDB()

try:
    data = mmdb.harmonized_single_sample_by_medium("surface water")
except PermissionError as e:
    print(f"Invalid API key: {e}")
except ValueError as e:
    print(f"Invalid input or no data found: {e}")
except RuntimeError as e:
    print(f"API error: {e}")
```

## Use Cases

### Environmental Occurrence Assessment

```python
mmdb = MMDB()
dtxsid = "DTXSID7020182"

# Get all samples
samples = mmdb.harmonized_single_sample_by_dtxsid(dtxsid)

# Calculate detection statistics
detected = [s for s in samples if s.get('detectionStatus') == 'detected']
detection_rate = len(detected) / len(samples) * 100

print(f"Detection rate: {detection_rate:.1f}%")
print(f"Total samples: {len(samples)}")
print(f"Detected in: {len(detected)} samples")
```

### Medium-Specific Analysis

```python
# Compare chemical detection across different media
mediums = ["surface water", "groundwater", "air", "soil"]
results = {}

for medium in mediums:
    try:
        data = mmdb.harmonized_aggregate_records_by_medium(medium)
        results[medium] = len(data.get('data', []))
    except Exception as e:
        results[medium] = 0

print("Chemicals detected by medium:")
for medium, count in results.items():
    print(f"  {medium}: {count} chemicals")
```

### Temporal Trends

```python
# Analyze concentration trends over time
samples = mmdb.harmonized_single_sample_by_dtxsid("DTXSID7020182")

# Filter to detected samples with dates
detected_samples = [
    s for s in samples 
    if s.get('detectionStatus') == 'detected' and s.get('sampleDate')
]

# Sort by date
from datetime import datetime
detected_samples.sort(key=lambda x: datetime.fromisoformat(x['sampleDate']))

# Analyze by year
from collections import defaultdict
yearly_data = defaultdict(list)

for sample in detected_samples:
    year = sample['sampleDate'][:4]
    yearly_data[year].append(sample['concentration'])

for year, concentrations in sorted(yearly_data.items()):
    avg_conc = sum(concentrations) / len(concentrations)
    print(f"{year}: {avg_conc:.3f} µg/L (n={len(concentrations)})")
```

### Geographic Distribution

```python
# Map detection locations
samples = mmdb.harmonized_single_sample_by_medium("surface water", page_number=1)

locations = []
for sample in samples.get('data', []):
    if sample.get('latitude') and sample.get('longitude'):
        locations.append({
            'chemical': sample.get('chemicalName'),
            'lat': sample.get('latitude'),
            'lon': sample.get('longitude'),
            'concentration': sample.get('concentration')
        })

print(f"Found {len(locations)} georeferenced samples")
```

## Best Practices

1. **Use Aggregates First**: For overview analysis, start with aggregate records
2. **Pagination**: Handle pagination properly for large datasets
3. **Filter by Medium**: Medium-specific queries are more efficient
4. **Cache Data**: Store results locally to minimize repeated API calls
5. **Validate Coordinates**: Check for valid lat/lon before geographic analysis

## Related Documentation

- [Exposure Prediction API](EXPOSURE_PREDICTIONS.md) - Predicted exposure levels
- [List Presence API](LIST_PRESENCE.md) - Chemical list membership
- [HTTK Data API](HTTK_DATA.md) - Toxicokinetic parameters

## API Reference

For complete API details, see [MMDB API Reference](api/mmdb.md).
