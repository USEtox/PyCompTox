# Examples

Comprehensive examples for common PyCompTox workflows.

## Basic Examples

### Example 1: Search and Display Chemical Information

```python
from pycomptox import Chemical, ChemicalDetails

# Search for a chemical
chem = Chemical()
results = chem.search_by_name("aspirin")

if results:
    chemical = results[0]
    print(f"Name: {chemical['preferredName']}")
    print(f"DTXSID: {chemical['dtxsid']}")
    print(f"CASRN: {chemical.get('casrn', 'N/A')}")
    
    # Get detailed information
    details = ChemicalDetails()
    info = details.get_chemical_by_dtxsid(
        chemical['dtxsid'],
        projection="chemicaldetailall"
    )
    
    print(f"\nDetailed Information:")
    print(f"Formula: {info.get('molFormula', 'N/A')}")
    print(f"Weight: {info.get('molWeight', 'N/A')}")
    print(f"SMILES: {info.get('smiles', 'N/A')}")
```

### Example 2: Property Analysis

```python
from pycomptox import ChemicalProperties

props = ChemicalProperties()

# Get property summary
dtxsid = "DTXSID7020182"  # Bisphenol A
summary = props.get_property_summary_by_dtxsid(dtxsid)

print(f"Properties for {dtxsid}:")
for prop in summary:
    name = prop['propName']
    exp_median = prop.get('experimentalMedian', 'N/A')
    pred_median = prop.get('predictedMedian', 'N/A')
    unit = prop.get('unit', '')
    
    print(f"  {name}: Exp={exp_median}, Pred={pred_median} {unit}")
```

### Example 3: Batch Processing

```python
from pycomptox import Chemical, ExtraData

# Get multiple chemicals
chem = Chemical()
chemicals = ["caffeine", "aspirin", "ibuprofen"]

# Search for all
dtxsids = []
for name in chemicals:
    results = chem.search_by_name(name)
    if results:
        dtxsids.append(results[0]['dtxsid'])

# Get reference data in batch
extra = ExtraData()
ref_data = extra.get_data_by_dtxsid_batch(dtxsids)

# Display results
for data in sorted(ref_data, key=lambda x: x['pubmed'], reverse=True):
    print(f"{data['dtxsid']}: {data['pubmed']} PubMed citations")
```

## Advanced Examples

### Example 4: Complete Chemical Profile

```python
from pycomptox import Chemical, ChemicalDetails, ChemicalProperties, ExtraData

def get_chemical_profile(identifier, id_type='name'):
    """Get complete chemical profile."""
    # Search
    chem = Chemical()
    if id_type == 'name':
        results = chem.search_by_name(identifier)
    elif id_type == 'casrn':
        results = chem.search_by_casrn(identifier)
    elif id_type == 'dtxsid':
        results = [{'dtxsid': identifier}]
    else:
        raise ValueError(f"Unknown id_type: {id_type}")
    
    if not results:
        return None
    
    dtxsid = results[0]['dtxsid']
    
    # Gather all data
    details = ChemicalDetails()
    props = ChemicalProperties()
    extra = ExtraData()
    
    return {
        'search_result': results[0],
        'details': details.get_chemical_by_dtxsid(
            dtxsid,
            projection='chemicaldetailall'
        ),
        'property_summary': props.get_property_summary_by_dtxsid(dtxsid),
        'predicted_props': props.get_predicted_properties_by_dtxsid(dtxsid),
        'experimental_props': props.get_experimental_properties_by_dtxsid(dtxsid),
        'references': extra.get_data_by_dtxsid(dtxsid)
    }

# Usage
profile = get_chemical_profile("bisphenol A")
if profile:
    print(f"Name: {profile['details']['preferredName']}")
    print(f"Formula: {profile['details']['molFormula']}")
    print(f"Property summaries: {len(profile['property_summary'])}")
    print(f"Predicted properties: {len(profile['predicted_props'])}")
    print(f"Experimental properties: {len(profile['experimental_props'])}")
    print(f"PubMed citations: {profile['references']['pubmed']}")
```

### Example 5: Property Comparison Across Chemicals

```python
from pycomptox.chemical import ChemicalProperties
import pandas as pd

def compare_properties(dtxsids, property_names):
    """Compare specific properties across chemicals."""
    props = ChemicalProperties()
    
    # Get property data
    all_data = props.get_property_summary_by_dtxsid_batch(dtxsids)
    
    # Extract specific properties
    results = []
    for dtxsid in dtxsids:
        chem_props = [p for p in all_data if p.get('dtxsid') == dtxsid]
        row = {'dtxsid': dtxsid}
        
        for prop_name in property_names:
            matching = [p for p in chem_props if p['propName'] == prop_name]
            if matching:
                row[prop_name] = matching[0].get('experimentalMedian', 'N/A')
            else:
                row[prop_name] = 'N/A'
        
        results.append(row)
    
    return pd.DataFrame(results)

# Usage
chemicals = ["DTXSID7020182", "DTXSID2021315", "DTXSID6020139"]
properties = ["Boiling Point", "Melting Point", "Log P"]

df = compare_properties(chemicals, properties)
print(df)
```

### Example 6: Finding Chemicals by Property Range

```python
from pycomptox import ChemicalProperties

props = ChemicalProperties()

# Find chemicals with Log P between 2 and 4
results = props.get_predicted_property_by_name_and_range("Log P", 2.0, 4.0)

print(f"Found {len(results)} chemicals with Log P between 2 and 4:")
for chem in results[:10]:
    print(f"  {chem['dtxsid']}: Log P = {chem['propValue']}")
```

### Example 7: Literature Analysis

```python
from pycomptox import Chemical, ExtraData

def analyze_chemical_class(search_term, top_n=10):
    """Analyze literature coverage for a chemical class."""
    # Search for chemicals
    chem = Chemical()
    results = chem.search_by_name(search_term)
    
    if not results:
        return None
    
    # Get DTXSIDs
    dtxsids = [r['dtxsid'] for r in results[:50]]
    
    # Get reference data
    extra = ExtraData()
    ref_data = extra.get_data_by_dtxsid_batch(dtxsids)
    
    # Sort by total references
    sorted_data = sorted(ref_data, key=lambda x: x['refs'], reverse=True)
    
    # Display top N
    print(f"Top {top_n} most-referenced chemicals for '{search_term}':")
    for i, data in enumerate(sorted_data[:top_n], 1):
        print(f"{i}. {data['dtxsid']}")
        print(f"   Total: {data['refs']}, PubMed: {data['pubmed']}, "
              f"Patents: {data['googlePatent']}")
    
    # Statistics
    total_refs = sum(d['refs'] for d in ref_data)
    avg_refs = total_refs / len(ref_data) if ref_data else 0
    
    print(f"\nStatistics:")
    print(f"  Total chemicals analyzed: {len(ref_data)}")
    print(f"  Total references: {total_refs}")
    print(f"  Average references per chemical: {avg_refs:.1f}")
    
    return ref_data

# Usage
analyze_chemical_class("phthalate", top_n=5)
```

### Example 8: Caching Wrapper

```python
from functools import lru_cache
from pycomptox import ChemicalDetails

class CachedChemicalClient:
    """Chemical client with caching."""
    
    def __init__(self):
        self.details = ChemicalDetails(time_delay_between_calls=0.5)
    
    @lru_cache(maxsize=256)
    def get_chemical_cached(self, dtxsid, projection='chemicalidentifier'):
        """Get chemical with caching."""
        return self.details.get_chemical_by_dtxsid(dtxsid, projection)
    
    def clear_cache(self):
        """Clear the cache."""
        self.get_chemical_cached.cache_clear()
    
    def cache_info(self):
        """Get cache statistics."""
        return self.get_chemical_cached.cache_info()

# Usage
client = CachedChemicalClient()

# First call - fetches from API
data1 = client.get_chemical_cached("DTXSID7020182")

# Second call - returns cached result (fast!)
data2 = client.get_chemical_cached("DTXSID7020182")

# Check cache statistics
print(client.cache_info())
```

### Example 9: DataFrame Integration

```python
from pycomptox import Chemical, ChemicalDetails, ExtraData
import pandas as pd

def create_chemical_dataframe(chemical_names):
    """Create pandas DataFrame from chemical data."""
    chem = Chemical()
    details = ChemicalDetails()
    extra = ExtraData()
    
    data = []
    
    for name in chemical_names:
        # Search
        results = chem.search_by_name(name)
        if not results:
            continue
        
        dtxsid = results[0]['dtxsid']
        
        # Get details
        info = details.get_chemical_by_dtxsid(dtxsid)
        refs = extra.get_data_by_dtxsid(dtxsid)
        
        # Combine
        data.append({
            'search_name': name,
            'preferred_name': info.get('preferredName', ''),
            'dtxsid': dtxsid,
            'casrn': info.get('casrn', ''),
            'formula': info.get('molFormula', ''),
            'weight': info.get('molWeight', ''),
            'total_refs': refs['refs'],
            'pubmed': refs['pubmed'],
            'patents': refs['googlePatent']
        })
    
    return pd.DataFrame(data)

# Usage
chemicals = ["caffeine", "aspirin", "ibuprofen", "acetaminophen"]
df = create_chemical_dataframe(chemicals)

# Analyze
print(df)
print(f"\nAverage PubMed citations: {df['pubmed'].mean():.1f}")
print(f"Most referenced: {df.loc[df['pubmed'].idxmax(), 'preferred_name']}")
```

### Example 10: Error-Resilient Batch Processing

```python
from pycomptox import Chemical
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def robust_batch_search(identifiers, id_type='name'):
    """Robust batch search with error handling."""
    chem = Chemical(time_delay_between_calls=0.5)
    
    results = []
    errors = []
    
    for identifier in identifiers:
        try:
            if id_type == 'name':
                res = chem.search_by_name(identifier)
            elif id_type == 'casrn':
                res = chem.search_by_casrn(identifier)
            else:
                logger.warning(f"Unknown id_type: {id_type}")
                continue
            
            if res:
                results.append({
                    'identifier': identifier,
                    'dtxsid': res[0]['dtxsid'],
                    'preferred_name': res[0].get('preferredName', ''),
                    'success': True
                })
                logger.info(f"✓ Found {identifier}")
            else:
                errors.append({
                    'identifier': identifier,
                    'error': 'No results found',
                    'success': False
                })
                logger.warning(f"✗ No results for {identifier}")
                
        except Exception as e:
            errors.append({
                'identifier': identifier,
                'error': str(e),
                'success': False
            })
            logger.error(f"✗ Error for {identifier}: {e}")
    
    return {
        'results': results,
        'errors': errors,
        'success_rate': len(results) / len(identifiers) * 100
    }

# Usage
chemicals = ["caffeine", "invalid123", "aspirin", "fake_chemical", "benzene"]
output = robust_batch_search(chemicals)

print(f"\nSuccess rate: {output['success_rate']:.1f}%")
print(f"Successful: {len(output['results'])}")
print(f"Failed: {len(output['errors'])}")
```

## See Also

- [API Reference](api/chemical.md)
- [Best Practices](best_practices.md)
- [Configuration](configuration.md)
