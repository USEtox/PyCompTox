# Category-Based API Organization

PyCompTox is organized into four main categories that mirror the EPA CompTox Dashboard API structure:

- **chemical**: Chemical search, properties, and identification
- **bioactivity**: Bioactivity, toxicity, and assay data  
- **exposure**: Exposure predictions, functional use, and product data
- **hazard**: Hazard characterization *(coming in future releases)*

## Access Patterns

PyCompTox supports three flexible access patterns:

### 1. Direct Import (Traditional)

Import individual classes directly from the main package:

```python
>>> from pycomptox.chemical import Chemical, ChemicalProperties
>>> from pycomptox.bioactivity import AssaySearch, BioactivityData
>>> from pycomptox.exposure import ExposurePrediction, FunctionalUse

# Use the classes
chem = Chemical()
results = chem.search_by_starting_value("caffeine")

props = ChemicalProperties()
data = props.retrieve_properties_by_dtxsid(results[0]['dtxsid'])
```

### 2. Category-Based Import (Recommended)

Import category submodules for organized access:

```python
from pycomptox import chemical, bioactivity, exposure

# Chemical operations
chem = chemical.Chemical()
results = chem.search_by_starting_value("caffeine")

props = chemical.ChemicalProperties()
data = props.retrieve_properties_by_dtxsid(results[0]['dtxsid'])

# Bioactivity operations
assay = bioactivity.AssaySearch()
assay_data = assay.search_by_chemical(results[0]['dtxsid'])

# Exposure operations
exp = exposure.ExposurePrediction()
predictions = exp.general_prediction_SEEMs_by_dtxsid(results[0]['dtxsid'])
```

**Benefits:**
- Clear organization by functional area
- Easier discovery of related classes
- Better namespace management for large projects
- Aligns with EPA's API categories

### 3. Namespace Access

Import the package and use dot notation:

```python
import pycomptox as pct

# Access via categories
chem = pct.chemical.Chemical()
results = chem.search_by_name("caffeine")

assay = pct.bioactivity.AssaySearch()
exp = pct.exposure.ExposurePrediction()

# Direct access still works
chem2 = pct.Chemical()
props = pct.ChemicalProperties()
```

## Category Reference

### Chemical Category

Classes for chemical search, properties, and identification:

```python
from pycomptox import chemical

# Available classes:
chemical.Chemical          # Search by name, CAS, identifier
chemical.ChemicalDetails   # Detailed chemical information
chemical.ChemicalProperties # MW, LogP, structure, etc.
chemical.ChemSynonym       # Synonyms and alternative names
chemical.ChemicalList      # Curated chemical lists
chemical.ExtraData         # Additional chemical data
chemical.WikiLink          # Wikipedia links
chemical.PubChemLink       # PubChem database links
```

**Example:**
```python
from pycomptox import chemical

# Search for a chemical
chem = chemical.Chemical()
results = chem.search_by_starting_value("benzene")
dtxsid = results[0]['dtxsid']

# Get properties
props = chemical.ChemicalProperties()
prop_data = props.retrieve_properties_by_dtxsid(dtxsid)
print(f"MW: {prop_data['molecularWeight']}")

# Get synonyms
syn = chemical.ChemSynonym()
synonyms = syn.get_synonyms_by_dtxsid(dtxsid)
```

### Bioactivity Category

Classes for bioactivity, toxicity, and assay data:

```python
from pycomptox import bioactivity

# Available classes:
bioactivity.AssaySearch        # Search toxicity assays
bioactivity.AssayBioactivity   # Bioactivity data from assays
bioactivity.BioactivityModel   # Predictive models
bioactivity.BioactivityData    # Comprehensive datasets
bioactivity.BioactivityAOP     # Adverse Outcome Pathways
bioactivity.AnalyticalQC       # Quality control data
```

**Example:**
```python
from pycomptox import bioactivity

# Search for assays
assay = bioactivity.AssaySearch()
assays = assay.search_by_chemical("DTXSID0020232")

# Get bioactivity data
bio_data = bioactivity.BioactivityData()
data = bio_data.get_bioactivity_summary("DTXSID0020232")

# Check AOP linkages
aop = bioactivity.BioactivityAOP()
pathways = aop.get_aop_by_dtxsid("DTXSID0020232")
```

### Exposure Category

Classes for exposure predictions, functional use, and product data:

```python
from pycomptox import exposure

# Available classes:
exposure.ExposurePrediction    # General exposure predictions (SEEM)
exposure.DemographicExposure   # Demographic-specific predictions
exposure.FunctionalUse         # Functional use categories
exposure.ProductData           # Consumer product data
exposure.CCCData              # Chemical Categories data
exposure.ListPresence         # Regulatory/screening lists
exposure.HTTKData             # Toxicokinetics parameters
exposure.MMDB                 # Environmental monitoring
```

**Example:**
```python
from pycomptox import exposure

# Get exposure predictions
exp_pred = exposure.ExposurePrediction()
predictions = exp_pred.general_prediction_SEEMs_by_dtxsid("DTXSID0020232")

# Check functional use
func_use = exposure.FunctionalUse()
uses = func_use.functiona_use_by_dtxsid("DTXSID0020232")

# Get product data
products = exposure.ProductData()
prod_data = products.products_data_by_dtxsid("DTXSID0020232")

# Check list presence
lists = exposure.ListPresence()
presence = lists.list_presence_data_by_dtxsid("DTXSID0020232")
```

### Hazard Category

*(Coming in future releases)*

Will provide classes for hazard characterization, toxicity reference values, and risk assessment data.

## Complete Workflow Example

Here's a complete workflow using category-based organization:

```python
from pycomptox import chemical, bioactivity, exposure

# 1. Find chemical
chem = chemical.Chemical()
results = chem.search_by_starting_value("bisphenol A")
dtxsid = results[0]['dtxsid']
print(f"Found: {dtxsid}")

# 2. Get chemical properties
props = chemical.ChemicalProperties()
prop_data = props.retrieve_properties_by_dtxsid(dtxsid)
print(f"Molecular Weight: {prop_data['molecularWeight']}")
print(f"LogP: {prop_data['logP']}")

# 3. Check bioactivity
bio_data = bioactivity.BioactivityData()
bio_summary = bio_data.get_bioactivity_summary(dtxsid)
print(f"Active assays: {len(bio_summary)}")

# 4. Get exposure predictions
exp_pred = exposure.ExposurePrediction()
predictions = exp_pred.general_prediction_SEEMs_by_dtxsid(dtxsid)
print(f"Exposure pathways: {len(predictions)}")

# 5. Check functional use
func_use = exposure.FunctionalUse()
uses = func_use.functiona_use_by_dtxsid(dtxsid)
print(f"Functional uses: {', '.join([u['functionName'] for u in uses])}")

# 6. Check regulatory status
lists = exposure.ListPresence()
presence = lists.list_presence_data_by_dtxsid(dtxsid)
regulatory = [p['listName'] for p in presence if p['isPresent']]
print(f"On lists: {', '.join(regulatory)}")
```

## Migration Guide

If you have existing code using direct imports, **no changes are required**. The traditional import pattern continues to work:

```python
# Old code still works
from pycomptox import Chemical, ChemicalProperties
chem = Chemical()
```

To adopt category-based organization, simply update imports:

```python
# New organized approach
from pycomptox import chemical
chem = chemical.Chemical()
```

Both patterns can be mixed in the same project:

```python
# Mix as needed
from pycomptox.chemical import Chemical  # Direct import
from pycomptox import exposure  # Category import

chem = Chemical()
exp = exposure.ExposurePrediction()
```

## Best Practices

1. **For small scripts**: Use direct imports for brevity
   ```python
   from pycomptox.chemical import Chemical, ChemicalProperties
   ```

2. **For large projects**: Use category-based imports for organization
   ```python
   from pycomptox import chemical, bioactivity, exposure
   ```

3. **For libraries**: Import the package and use namespace access
   ```python
   import pycomptox as pct
   chem = pct.chemical.Chemical()
   ```

4. **Avoid wildcard imports**: Don't use `from pycomptox import *`
   - Use explicit imports for clarity
   - Better IDE support and linting

## API Reference

For detailed documentation of each class and method, see the [API Documentation](api/) section.
