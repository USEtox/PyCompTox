# Exposure Prediction APIs

PyCompTox provides two complementary APIs for exposure predictions: `ExposurePrediction` for general population estimates and `DemographicExposure` for demographic-specific predictions. Both use SEEM (Systematic Empirical Evaluation of Models) methodology.

## Overview

Exposure predictions estimate the average (geometric mean) exposure rate in mg/kg bodyweight/day for the U.S. population:

- **50% Confidence**: Median estimate - we are 50% confident exposure is below this value
- **95% Confidence**: Upper 95th percentile - we are 95% confident exposure is below this value

### ExposurePrediction (General Population)

Based on consensus exposure model predictions and chemical similarity to NHANES-monitored chemicals. Method described in the 2018 publication "Consensus Modeling of Median Chemical Intake for the U.S. Population Based on Predictions of Exposure Pathways".

### DemographicExposure (Population Subgroups)

Uses a heuristic model for demographic-specific predictions. Method described in the 2014 publication "High Throughput Heuristics for Prioritizing Human Exposure to Environmental Chemicals".

## Quick Start

### General Population Predictions

```python
from pycomptox.exposure import ExposurePrediction

# Initialize client
exp_pred = ExposurePrediction()

# Get general population exposure estimates
dtxsid = "DTXSID0020232"
predictions = exp_pred.general_prediction_SEEMs_by_dtxsid(dtxsid)

for pred in predictions:
    print(f"Pathway: {pred.get('pathway')}")
    print(f"Median: {pred.get('medianEstimate')} mg/kg/day")
    print(f"95th Percentile: {pred.get('upper95')}")
```

### Demographic-Specific Predictions

```python
from pycomptox.exposure import DemographicExposure

# Initialize client
demo_exp = DemographicExposure()

# Get demographic-specific estimates
predictions = demo_exp.prediction_SEEMs_data_by_dtxsid(dtxsid)

for pred in predictions:
    print(f"Demographic: {pred.get('demographic')}")
    print(f"Age Group: {pred.get('ageGroup')}")
    print(f"Median: {pred.get('medianEstimate')} mg/kg/day")
```

## ExposurePrediction API

### General SEEM Predictions

Get exposure predictions for the total U.S. population:

```python
exp_pred = ExposurePrediction()

# Basic usage
predictions = exp_pred.general_prediction_SEEMs_by_dtxsid("DTXSID0020232")

# With projection
predictions = exp_pred.general_prediction_SEEMs_by_dtxsid(
    "DTXSID0020232",
    projection="ccd-general"
)

# Analyze results
for pred in predictions:
    pathway = pred.get('pathway')
    median = pred.get('medianEstimate')
    upper = pred.get('upper95')
    
    print(f"{pathway}:")
    print(f"  Median exposure: {median} mg/kg/day")
    print(f"  95th percentile: {upper} mg/kg/day")
```

**Parameters**:
- `dtxsid`: Chemical identifier
- `projection`: Optional projection type (default: "ccd-general")

**Returns**: List of predictions by exposure pathway including median and 95th percentile estimates.

### Batch Operations

Process multiple chemicals efficiently:

```python
exp_pred = ExposurePrediction()

dtxsids = [
    "DTXSID0020232",
    "DTXSID7020182",
    "DTXSID0020245"
]

batch_results = exp_pred.general_prediction_SEEMs_by_dtxsid_batch(dtxsids)

for result in batch_results:
    dtxsid = result.get('dtxsid')
    median = result.get('medianEstimate')
    print(f"{dtxsid}: {median} mg/kg/day")
```

## DemographicExposure API

### Demographic SEEM Predictions

Get exposure predictions broken down by demographic groups:

```python
demo_exp = DemographicExposure()

# Basic usage
predictions = demo_exp.prediction_SEEMs_data_by_dtxsid("DTXSID0020232")

# With projection
predictions = demo_exp.prediction_SEEMs_data_by_dtxsid(
    "DTXSID0020232",
    projection="ccd-demographic"
)

# Analyze by demographic
for pred in predictions:
    demo = pred.get('demographic')
    age = pred.get('ageGroup')
    median = pred.get('medianEstimate')
    
    print(f"{demo} ({age}): {median} mg/kg/day")
```

**Parameters**:
- `dtxsid`: Chemical identifier
- `projection`: Optional projection type (default: "ccd-demographic")

**Returns**: List of predictions by demographic group including age-specific estimates.

### Demographic Batch Operations

```python
demo_exp = DemographicExposure()

dtxsids = ["DTXSID0020232", "DTXSID0020267"]
batch_results = demo_exp.prediction_SEEMs_data_by_dtxsid_batch(dtxsids)

# Group by demographic
from collections import defaultdict
by_demographic = defaultdict(list)

for result in batch_results:
    demo = result.get('demographic')
    by_demographic[demo].append(result)

for demo, results in by_demographic.items():
    print(f"\n{demo}: {len(results)} chemicals")
```

## Configuration

### API Key Setup

```python
from pycomptox import save_api_key

# Save your API key (one-time)
save_api_key("your-api-key-here")

# Or provide at initialization
exp_pred = ExposurePrediction(api_key="your-api-key-here")
demo_exp = DemographicExposure(api_key="your-api-key-here")
```

### Rate Limiting

```python
# Add delays between requests
exp_pred = ExposurePrediction(time_delay_between_calls=1.0)
demo_exp = DemographicExposure(time_delay_between_calls=1.0)
```

## Data Structure Examples

### General Prediction Response

```python
[
    {
        "dtxsid": "DTXSID0020232",
        "chemicalName": "Acetaminophen",
        "pathway": "Dietary",
        "medianEstimate": 0.0034,
        "upper95": 0.012,
        "lowerCI": 0.0021,
        "upperCI": 0.0055,
        "units": "mg/kg/day",
        "modelSource": "SEEM Consensus",
        "dataQuality": "High"
    },
    {
        "dtxsid": "DTXSID0020232",
        "pathway": "Dermal",
        "medianEstimate": 0.00089,
        "upper95": 0.0034,
        "units": "mg/kg/day",
        "modelSource": "SEEM Consensus"
    }
]
```

### Demographic Prediction Response

```python
[
    {
        "dtxsid": "DTXSID0020232",
        "chemicalName": "Acetaminophen",
        "demographic": "Children",
        "ageGroup": "0-5 years",
        "medianEstimate": 0.0067,
        "upper95": 0.021,
        "units": "mg/kg/day"
    },
    {
        "dtxsid": "DTXSID0020232",
        "demographic": "Adults",
        "ageGroup": "18-65 years",
        "medianEstimate": 0.0028,
        "upper95": 0.0095,
        "units": "mg/kg/day"
    }
]
```

## Use Cases

### Risk Prioritization

```python
exp_pred = ExposurePrediction()

# Get exposure predictions
chemicals = ["DTXSID0020232", "DTXSID7020182", "DTXSID0020245"]
predictions = exp_pred.general_prediction_SEEMs_by_dtxsid_batch(chemicals)

# Sort by exposure level
sorted_preds = sorted(
    predictions,
    key=lambda x: x.get('upper95', 0),
    reverse=True
)

print("Chemicals ranked by 95th percentile exposure:")
for i, pred in enumerate(sorted_preds, 1):
    print(f"{i}. {pred.get('chemicalName')}: {pred.get('upper95')} mg/kg/day")
```

### Vulnerable Population Assessment

```python
demo_exp = DemographicExposure()
dtxsid = "DTXSID0020232"

# Get demographic predictions
predictions = demo_exp.prediction_SEEMs_data_by_dtxsid(dtxsid)

# Identify highest-exposed demographic
max_exposure = max(predictions, key=lambda x: x.get('upper95', 0))

print(f"Highest exposure in: {max_exposure.get('demographic')}")
print(f"Age group: {max_exposure.get('ageGroup')}")
print(f"95th percentile: {max_exposure.get('upper95')} mg/kg/day")

# Compare to general population
gen_pred = ExposurePrediction()
general = gen_pred.general_prediction_SEEMs_by_dtxsid(dtxsid)
gen_upper95 = general[0].get('upper95')

ratio = max_exposure.get('upper95') / gen_upper95
print(f"Demographic exposure is {ratio:.1f}x general population")
```

### Exposure Pathway Analysis

```python
exp_pred = ExposurePrediction()

# Get predictions with all pathways
predictions = exp_pred.general_prediction_SEEMs_by_dtxsid("DTXSID0020232")

# Calculate total exposure
total_median = sum(p.get('medianEstimate', 0) for p in predictions)
total_upper95 = sum(p.get('upper95', 0) for p in predictions)

print(f"Total median exposure: {total_median:.4f} mg/kg/day")
print(f"Total 95th percentile: {total_upper95:.4f} mg/kg/day")

# Pathway contributions
print("\nPathway contributions:")
for pred in predictions:
    pathway = pred.get('pathway')
    median = pred.get('medianEstimate', 0)
    contribution = (median / total_median) * 100
    print(f"  {pathway}: {contribution:.1f}%")
```

### Uncertainty Analysis

```python
exp_pred = ExposurePrediction()
predictions = exp_pred.general_prediction_SEEMs_by_dtxsid("DTXSID0020232")

for pred in predictions:
    pathway = pred.get('pathway')
    median = pred.get('medianEstimate')
    lower = pred.get('lowerCI')
    upper = pred.get('upperCI')
    
    if lower and upper:
        uncertainty_range = upper - lower
        relative_uncertainty = (uncertainty_range / median) * 100
        print(f"{pathway}: {relative_uncertainty:.1f}% relative uncertainty")
```

## Interpretation Guidelines

### Confidence Levels

- **Median (50%)**: Half of the population is expected to have exposures below this value
- **95th Percentile (95%)**: Only 5% of the population is expected to exceed this exposure level

### Exposure Units

All predictions are in **mg/kg bodyweight/day**:
- Accounts for body weight differences
- Allows comparison across demographics
- Standard unit for exposure assessment

### Data Quality Indicators

Consider these factors when interpreting predictions:
- **Model Source**: Consensus models generally have higher confidence
- **Chemical Similarity**: Predictions more reliable for chemicals similar to NHANES-monitored chemicals
- **Demographic Coverage**: Some demographics may have limited data

## Best Practices

1. **Use Both APIs**: Compare general and demographic predictions for comprehensive assessment
2. **Consider Uncertainty**: Always report both median and 95th percentile
3. **Validate Predictions**: Compare with measured data when available
4. **Document Assumptions**: Note which projection was used
5. **Account for Multiple Pathways**: Sum across pathways for total exposure

## Error Handling

```python
from pycomptox.exposure import ExposurePrediction, DemographicExposure

try:
    exp_pred = ExposurePrediction()
    predictions = exp_pred.general_prediction_SEEMs_by_dtxsid("DTXSID0020232")
except PermissionError as e:
    print(f"Invalid API key: {e}")
except ValueError as e:
    print(f"Invalid input or no predictions available: {e}")
except RuntimeError as e:
    print(f"API error: {e}")
```

## Related Documentation

- [HTTK Data API](HTTK_DATA.md) - Toxicokinetic parameters
- [Bioactivity Data API](BIOACTIVITY_DATA.md) - Toxicity data
- [Product Data API](PRODUCT_DATA.md) - Product use information

## API References

- [ExposurePrediction API Reference](api/exposureprediction.md)
- [DemographicExposure API Reference](api/demographicexposure.md)
