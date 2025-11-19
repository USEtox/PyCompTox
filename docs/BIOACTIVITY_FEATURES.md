# New Features: Bioactivity Data and AOP Support

## Overview

PyCompTox now includes comprehensive support for bioactivity data and Adverse Outcome Pathway (AOP) information through two new classes:

- **BioactivityData**: Access to EPA ToxCast bioactivity data
- **BioactivityAOP**: Adverse Outcome Pathway data linking assays to biological events

## What's New

### BioactivityData Class

Access to ToxCast bioactivity data including:

- **Summary Statistics**: Get aggregate data by chemical, tissue, or assay endpoint
- **Detailed Assay Results**: Full bioactivity records with hit calls and concentration-response data
- **Activity-Exposure-Dose (AED) Data**: Link activity to exposure estimates
- **Multiple Identifier Types**: Query by DTXSID, SPID, M4ID, or AEID
- **Batch Operations**: Efficient retrieval for multiple chemicals or assays

#### Key Methods

```python
from pycomptox import BioactivityData

client = BioactivityData()

# Summary data
summary = client.get_summary_by_dtxsid("DTXSID7020182")
tissue_data = client.get_summary_by_dtxsid_and_tissue("DTXSID7024241", "liver")
aeid_summary = client.get_summary_by_aeid("3032")

# Detailed data
data = client.get_data_by_spid("EPAPLT0232A03")
data = client.get_data_by_m4id("1135145")
data = client.get_data_by_aeid(3032)

# AED data
aed = client.get_aed_data_by_dtxsid("DTXSID5021209")

# Batch operations
batch = client.find_bioactivity_data_by_dtxsid_batch(["DTXSID7020182", "DTXSID9026974"])
```

### BioactivityAOP Class

Access to Adverse Outcome Pathway data:

- **Assay-to-Event Mapping**: Link ToxCast assays to AOP key events
- **Event-to-Pathway Mapping**: Connect events to adverse outcome pathways
- **Gene-to-AOP Mapping**: Find pathways associated with specific genes
- **Comprehensive Coverage**: All three major access points (AEID, event, gene)

#### Key Methods

```python
from pycomptox import BioactivityAOP

client = BioactivityAOP()

# By ToxCast assay endpoint
aop_data = client.get_aop_data_by_toxcast_aeid(63)

# By AOP event number
events = client.get_aop_data_by_event_number(18)

# By Entrez gene ID
gene_aops = client.get_aop_data_by_entrez_gene_id(196)
```

## Documentation

### New Documentation Files

1. **BIOACTIVITY_DATA.md**: Complete guide with examples
   - Overview and quick start
   - Detailed method documentation
   - Data structure reference
   - Complete working examples
   - Understanding AOP structure

2. **api/bioactivitydata.md**: API reference for BioactivityData
3. **api/bioactivityaop.md**: API reference for BioactivityAOP

### Updated Documentation

- **index.md**: Added bioactivity features to overview
- **QUICK_REFERENCE.md**: Added quick reference tables for both classes
- **mkdocs.yml**: Updated navigation with new documentation

## Testing

### New Test Files

1. **test_bioactivitydata.py**: 10 comprehensive tests
   - Summary data retrieval
   - Detailed data methods
   - AED data access
   - Batch operations
   - Input validation

2. **test_bioactivityaop.py**: 8 comprehensive tests
   - AOP by ToxCast AEID
   - AOP by event number
   - AOP by gene ID
   - Multiple AEID lookups
   - Input validation
   - Data structure verification
   - Rate limiting
   - Error handling

### Test Results

All 119 tests passing (excluding test_bioactivitymodel.py):
- 10 new BioactivityData tests ✓
- 8 new BioactivityAOP tests ✓
- 101 existing tests ✓

## Usage Examples

### Example 1: Chemical Bioactivity Profile

```python
from pycomptox import BioactivityData

client = BioactivityData()
dtxsid = "DTXSID7020182"  # Bisphenol A

# Get all bioactivity data types
summary = client.get_summary_by_dtxsid(dtxsid)
detailed = client.get_data_by_dtxsid_and_projection(dtxsid)
aed = client.get_aed_data_by_dtxsid(dtxsid)

print(f"Summary records: {len(summary)}")
print(f"Detailed records: {len(detailed)}")
print(f"AED records: {len(aed)}")
```

### Example 2: Tissue-Specific Analysis

```python
from pycomptox import BioactivityData

client = BioactivityData()
dtxsid = "DTXSID7024241"

for tissue in ["liver", "kidney", "heart"]:
    data = client.get_summary_by_dtxsid_and_tissue(dtxsid, tissue)
    print(f"{tissue}: {len(data)} records")
```

### Example 3: AOP Pathway Exploration

```python
from pycomptox import BioactivityAOP

client = BioactivityAOP()

# Link assay to biological outcomes
aeid = 63
aop_data = client.get_aop_data_by_toxcast_aeid(aeid)

for record in aop_data:
    print(f"Event {record['eventNumber']} → AOP {record['aopNumber']}")
    print(f"  Gene: {record['entrezGeneId']}")
```

### Example 4: Gene-Level AOP Analysis

```python
from pycomptox import BioactivityAOP

client = BioactivityAOP()
gene_id = 196  # AHR gene

aop_data = client.get_aop_data_by_entrez_gene_id(gene_id)

# Count unique pathways and events
pathways = set(r['aopNumber'] for r in aop_data if r.get('aopNumber'))
events = set(r['eventNumber'] for r in aop_data if r.get('eventNumber'))

print(f"Gene {gene_id} involved in:")
print(f"  {len(pathways)} AOP pathways")
print(f"  {len(events)} biological events")
```

## Features

### Input Validation

Both classes include comprehensive input validation:
- Type checking (integers vs strings)
- Value validation (non-empty, positive values)
- List validation for batch methods
- Clear error messages

### Rate Limiting

Built-in rate limiting support:

```python
# Add delay between requests
client = BioactivityData(time_delay_between_calls=0.5)
aop = BioactivityAOP(time_delay_between_calls=0.5)
```

### Error Handling

Proper error handling for:
- Invalid API keys (PermissionError)
- Missing resources (ValueError)
- Network issues (RuntimeError)
- Timeout scenarios

### API Key Management

Uses existing PyCompTox API key infrastructure:

```python
from pycomptox import save_api_key

# One-time setup
save_api_key("your-api-key-here")

# Then classes work automatically
client = BioactivityData()  # Loads key automatically
```

## Integration

### Seamless Integration

Both classes integrate seamlessly with existing PyCompTox functionality:

```python
from pycomptox.chemical import Chemical
from pycomptox.bioactivity import BioactivityData, BioactivityAOP

# 1. Search for chemical
chem = Chemical()
results = chem.search_by_exact_value("name", "Bisphenol A")
dtxsid = results[0]['dtxsid']

# Get bioactivity data
bio = BioactivityData()
summary = bio.get_summary_by_dtxsid(dtxsid)

# Link to AOPs
aop = BioactivityAOP()
for record in summary[:5]:
    if 'aeid' in record:
        aop_data = aop.get_aop_data_by_toxcast_aeid(record['aeid'])
        print(f"AEID {record['aeid']} → {len(aop_data)} AOP records")
```

### Consistent API Design

Both classes follow PyCompTox patterns:
- Same initialization signature
- Consistent method naming
- Same error handling approach
- Familiar batch method patterns
- Rate limiting support

## Summary

The addition of BioactivityData and BioactivityAOP classes significantly expands PyCompTox capabilities:

✓ **Comprehensive ToxCast Data**: Access to EPA's bioactivity database
✓ **AOP Integration**: Link assays to adverse outcome pathways  
✓ **Multiple Access Methods**: Query by chemical, assay, event, or gene
✓ **Batch Operations**: Efficient multi-item retrieval
✓ **Well Tested**: 18 new tests, all passing
✓ **Fully Documented**: Complete guides and API references
✓ **Seamless Integration**: Works with existing PyCompTox classes

These additions enable researchers to:
- Evaluate chemical bioactivity profiles
- Analyze tissue-specific responses
- Link molecular events to adverse outcomes
- Explore gene-pathway relationships
- Conduct high-throughput bioactivity screening
