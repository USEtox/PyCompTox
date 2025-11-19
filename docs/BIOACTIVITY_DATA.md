# Bioactivity Data and AOP

PyCompTox provides comprehensive access to bioactivity data from the EPA's ToxCast program and Adverse Outcome Pathway (AOP) information.

## Overview

The bioactivity module consists of two main classes:

- **BioactivityData**: Access to ToxCast bioactivity data, including summary statistics, detailed assay results, and Activity-Exposure-Dose (AED) data
- **BioactivityAOP**: Access to Adverse Outcome Pathway data linking ToxCast assays to biological events and pathways

## BioactivityData Class

### Quick Start

```python
from pycomptox.bioactivity import BioactivityData

# Initialize client
client = BioactivityData()

# Get bioactivity summary for a chemical
summary = client.get_summary_by_dtxsid("DTXSID7020182")

# Get bioactivity data for an assay endpoint
data = client.get_data_by_aeid(3032)

# Batch retrieve data for multiple chemicals
batch_data = client.find_bioactivity_data_by_dtxsid_batch([
    "DTXSID7020182", 
    "DTXSID9026974"
])
```

### Summary Data Methods

Summary data provides aggregate statistics about bioactivity testing:

```python
# Get summary by chemical (DTXSID)
summary = client.get_summary_by_dtxsid("DTXSID9026974")

# Get summary filtered by tissue type
tissue_summary = client.get_summary_by_dtxsid_and_tissue(
    "DTXSID7024241", 
    "liver"
)

# Get summary statistics for an assay endpoint
aeid_summary = client.get_summary_by_aeid("3032")
# Returns: {
#   "aeid": 3032,
#   "activeMc": 150,      # Active multi-concentration hits
#   "totalMc": 1000,      # Total multi-concentration tested
#   "activeSc": 50,       # Active single-concentration hits
#   "totalSc": 200        # Total single-concentration tested
# }
```

**Activity Classification:**
- Multi-concentration: continuous hit call ≥ 0.9 = active
- Single-concentration: binary hit call (1 = active, 0 = inactive)

### Detailed Data Methods

Retrieve complete bioactivity records:

```python
# By sample identifier (SPID)
data = client.get_data_by_spid("EPAPLT0232A03")

# By data identifier (M4ID)
data = client.get_data_by_m4id("1135145")

# By chemical with optional projection
data = client.get_data_by_dtxsid_and_projection(
    "DTXSID7020182",
    projection="toxcast-summary-plot"
)

# By assay endpoint identifier
data = client.get_data_by_aeid(3032)
```

### Activity-Exposure-Dose (AED) Data

AED data links activity concentrations to exposure and dose estimates:

```python
# Get AED data for a chemical
aed_data = client.get_aed_data_by_dtxsid("DTXSID5021209")

# Batch retrieve AED data
aed_batch = client.find_aed_data_by_dtxsid_batch([
    "DTXSID5021209",
    "DTXSID7020182"
])
```

### Batch Operations

All batch methods accept lists and return data for multiple identifiers:

```python
# Batch by sample identifiers
spid_data = client.find_bioactivity_data_by_spid_batch([
    "EPAPLT0232A03",
    "EPAPLT0232A04"
])

# Batch by data identifiers
m4id_data = client.find_bioactivity_data_by_m4id_batch([
    1135145,
    1135146
])

# Batch by chemical identifiers
dtxsid_data = client.find_bioactivity_data_by_dtxsid_batch([
    "DTXSID7020182",
    "DTXSID9026974"
])

# Batch by assay endpoint identifiers
aeid_data = client.find_bioactivity_data_by_aeid_batch([
    3032,
    3033,
    3034
])
```

### Rate Limiting

Control API request frequency:

```python
# Add 500ms delay between requests
client = BioactivityData(time_delay_between_calls=0.5)
```

## BioactivityAOP Class

The AOP class links ToxCast assay endpoints to biological events and adverse outcome pathways.

### Quick Start

```python
from pycomptox.bioactivity import BioactivityAOP

# Initialize client
client = BioactivityAOP()

# Get AOP data by ToxCast assay endpoint
aop_data = client.get_aop_data_by_toxcast_aeid(63)

# Get AOP data by event number
events = client.get_aop_data_by_event_number(18)

# Get AOP data by gene
gene_aops = client.get_aop_data_by_entrez_gene_id(196)
```

### AOP Data Methods

```python
# By ToxCast assay endpoint ID (AEID)
aop_data = client.get_aop_data_by_toxcast_aeid(63)
# Returns list of records with:
# - toxcastAeid: ToxCast AEID
# - entrezGeneId: Associated gene
# - eventNumber: AOP event number
# - eventLink: Link to event details
# - aopNumber: AOP pathway number
# - aopLink: Link to AOP pathway

# By AOP event number
events = client.get_aop_data_by_event_number(18)
# Returns all assays and pathways associated with the event

# By Entrez Gene ID
gene_aops = client.get_aop_data_by_entrez_gene_id(196)
# Returns all AOP events and pathways involving the gene
```

### Understanding AOP Structure

AOPs (Adverse Outcome Pathways) connect:

1. **Molecular Initiating Events (MIEs)** - Initial biological perturbations
2. **Key Events (KEs)** - Intermediate biological changes
3. **Adverse Outcomes (AOs)** - Final health effects

Each record links:
- ToxCast assays → Biological events → Adverse outcomes
- Genes → Events → Pathways

### Example: Exploring Gene-Level AOPs

```python
from pycomptox.bioactivity import BioactivityAOP

client = BioactivityAOP()

# Get all AOPs for a specific gene
gene_id = 196  # AHR (Aryl Hydrocarbon Receptor)
aop_data = client.get_aop_data_by_entrez_gene_id(gene_id)

# Extract unique pathways
pathways = set()
events = set()

for record in aop_data:
    if record.get('aopNumber'):
        pathways.add(record['aopNumber'])
    if record.get('eventNumber'):
        events.add(record['eventNumber'])

print(f"Gene {gene_id} is involved in:")
print(f"  {len(pathways)} AOP pathways")
print(f"  {len(events)} biological events")
print(f"  {len(aop_data)} total ToxCast assays")
```

### Example: Linking Assays to Outcomes

```python
# Get AOP data for a specific ToxCast assay
aeid = 63
aop_records = client.get_aop_data_by_toxcast_aeid(aeid)

print(f"Assay {aeid} links to:")
for record in aop_records:
    print(f"  Event {record['eventNumber']}")
    print(f"    → AOP {record['aopNumber']}")
    print(f"    → Gene {record['entrezGeneId']}")
    print(f"    → {record['eventLink']}")
```

## Complete Examples

### Example 1: Comprehensive Chemical Bioactivity Profile

```python
from pycomptox import BioactivityData

client = BioactivityData()
dtxsid = "DTXSID7020182"  # Bisphenol A

# Get summary statistics
summary = client.get_summary_by_dtxsid(dtxsid)
print(f"Bioactivity summary for {dtxsid}:")
print(f"  Records: {len(summary) if isinstance(summary, list) else 1}")

# Get detailed data
detailed = client.get_data_by_dtxsid_and_projection(dtxsid)
print(f"  Detailed records: {len(detailed) if isinstance(detailed, list) else 1}")

# Get AED data
aed = client.get_aed_data_by_dtxsid(dtxsid)
print(f"  AED records: {len(aed) if isinstance(aed, list) else 1}")
```

### Example 2: Tissue-Specific Bioactivity Analysis

```python
from pycomptox import BioactivityData

client = BioactivityData()

# Compare bioactivity across tissues
dtxsid = "DTXSID7024241"
tissues = ["liver", "kidney", "heart", "brain"]

for tissue in tissues:
    data = client.get_summary_by_dtxsid_and_tissue(dtxsid, tissue)
    if data:
        print(f"{tissue.capitalize()}: {len(data)} records")
```

### Example 3: Batch Analysis of Multiple Chemicals

```python
from pycomptox import BioactivityData

client = BioactivityData()

# Analyze multiple chemicals at once
chemicals = [
    "DTXSID7020182",  # Bisphenol A
    "DTXSID9026974",  # Another chemical
    "DTXSID5021209",  # Another chemical
]

# Get bioactivity data
batch_data = client.find_bioactivity_data_by_dtxsid_batch(chemicals)

# Get AED data
aed_data = client.find_aed_data_by_dtxsid_batch(chemicals)

print(f"Retrieved data for {len(chemicals)} chemicals")
```

### Example 4: Pathway Analysis Through AOPs

```python
from pycomptox import BioactivityAOP, BioactivityData

aop_client = BioactivityAOP()
bio_client = BioactivityData()

# Start with a ToxCast assay
aeid = 3032

# Get bioactivity summary
summary = bio_client.get_summary_by_aeid(aeid)
print(f"Assay {aeid}:")
print(f"  Active MC: {summary.get('activeMc')}")
print(f"  Total MC: {summary.get('totalMc')}")

# Link to AOPs
aop_data = aop_client.get_aop_data_by_toxcast_aeid(aeid)
print(f"  Linked to {len(aop_data)} AOP records")

# Explore the biological context
for record in aop_data[:3]:  # First 3
    print(f"\n  Event {record['eventNumber']}:")
    print(f"    Gene: {record['entrezGeneId']}")
    print(f"    AOP: {record['aopNumber']}")
```

## Data Structure Reference

### Bioactivity Summary Record

```python
{
    "intendedTargetFamily": "nuclear receptor",
    "dtxsid": "DTXSID7020182",
    "tissue": "liver",
    "maxMedConc": 1.5,
    "continuousHitCall": 0.95,
    "chemicalName": "Bisphenol A",
    "hitCall": "active",
    "cutOff": 10.0,
    "logAC50": -5.5,
    "ac50": 3.16e-6,
    "acc": 5.0
}
```

### AOP Record

```python
{
    "id": 12345,
    "toxcastAeid": 63,
    "entrezGeneId": 196,
    "eventNumber": 18,
    "eventLink": "https://aopwiki.org/events/18",
    "aopNumber": 25,
    "aopLink": "https://aopwiki.org/aops/25"
}
```

## API Reference

For detailed method signatures and parameters, see:

- [BioactivityData API Reference](api/bioactivitydata.md)
- [BioactivityAOP API Reference](api/bioactivityaop.md)

## Related Documentation

- [Chemical Search](CHEMICAL_SEARCH.md) - Find chemicals to analyze
- [Chemical Details](CHEMICAL_DETAILS.md) - Get chemical information
- [Batch Methods](BATCH_METHODS.md) - Efficient batch processing
- [API Key Setup](API_KEY_AND_RATE_LIMITING.md) - Authentication and rate limits
