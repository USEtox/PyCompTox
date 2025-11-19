# PyCompTox - Quick API Reference

Quick reference for all available methods in PyCompTox v0.2.0.

## Chemical Search (`Chemical` class)

```python
from pycomptox.chemical import Chemical

client = Chemical(api_key=None, base_url="...", time_delay_between_calls=0.0)
```

### Search Methods (Return List[Dict])

| Method | Description | Example |
|--------|-------------|---------|
| `search_by_starting_value(value)` | Prefix search | `client.search_by_starting_value("Bisphenol")` |
| `search_by_exact_value(identifier, value)` | Exact match | `client.search_by_exact_value("name", "Bisphenol A")` |
| `search_by_substring_value(value)` | Contains search | `client.search_by_substring_value("phenol")` |

**identifier parameter options**: `"name"`, `"rn"` (CAS), `"dtxsid"`, `"dtxcid"`, `"inchikey"`

### Formula Search Methods (Return List[str] - DTXSIDs)

| Method | Description | Example |
|--------|-------------|---------|
| `search_by_msready_formula(formula)` | MS-ready formula | `client.search_by_msready_formula("C15H16O2")` |
| `search_by_exact_formula(formula)` | Exact formula | `client.search_by_exact_formula("C15H16O2")` |
| `search_ms_ready_by_formula(formula)` | MS-ready by formula | `client.search_ms_ready_by_formula("C16H24N2O5S")` |

### Mass Range Search (Return List[str] - DTXSIDs)

| Method | Description | Example |
|--------|-------------|---------|
| `search_ms_ready_by_mass_range(min, max)` | Mass range | `client.search_ms_ready_by_mass_range(200.9, 200.95)` |

### DTXCID Methods

| Method | Description | Example |
|--------|-------------|---------|
| `search_ms_ready_by_dtxcid(dtxcid)` | Get MS-ready by DTXCID | `client.search_ms_ready_by_dtxcid("DTXCID30182")` |

### Count Methods (Return int)

| Method | Description | Example |
|--------|-------------|---------|
| `search_chemical_count_by_ms_ready_formula(formula)` | Count MS-ready | `client.search_chemical_count_by_ms_ready_formula("C15H16O2")` |
| `search_chemical_count_by_exact_formula(formula)` | Count exact | `client.search_chemical_count_by_exact_formula("C15H16O2")` |

### Batch Methods

| Method | Max | Returns | Example |
|--------|-----|---------|---------|
| `search_by_exact_batch_values(identifier, values)` | 200 | List[Dict] | `client.search_by_exact_batch_values("name", ["Caffeine", "Aspirin"])` |
| `search_ms_ready_by_mass_range_batch(ranges)` | 200 | Dict | `client.search_ms_ready_by_mass_range_batch([[228.0, 228.2], [300.0, 300.5]])` |
| `search_ms_ready_by_dtxcid_batch(dtxcids)` | 200 | Dict | `client.search_ms_ready_by_dtxcid_batch(["DTXCID30182", "DTXCID505"])` |

---

## Chemical Details (`ChemicalDetails` class)

```python
from pycomptox.chemical import ChemicalDetails

client = ChemicalDetails(api_key=None, base_url="...", time_delay_between_calls=0.0)
```

### Single Retrieval Methods (Return Dict)

| Method | Description | Example |
|--------|-------------|---------|
| `data_by_dtxsid(dtxsid, projection=None)` | Get by DTXSID | `client.data_by_dtxsid("DTXSID7020182")` |
| `data_by_dtxcid(dtxcid, projection=None)` | Get by DTXCID | `client.data_by_dtxcid("DTXCID30182")` |

### Batch Retrieval Methods (Return List[Dict])

| Method | Max | Description | Example |
|--------|-----|-------------|---------|
| `data_by_dtxsid_batch(dtxsids, projection=None)` | 1000 | Batch by DTXSIDs | `client.data_by_dtxsid_batch(["DTXSID7020182", "DTXSID0020232"])` |
| `data_by_dtxcid_batch(dtxcids, projection=None)` | 1000 | Batch by DTXCIDs | `client.data_by_dtxcid_batch(["DTXCID30182", "DTXCID505"])` |

### Paginated Method

| Method | Description | Example |
|--------|-------------|---------|
| `find_all_chemical_details(next_page=1, projection=None)` | Get all (paginated) | `client.find_all_chemical_details(next_page=1)` |

Returns: `{"data": [list of dicts], "nextPage": int or None}`

### Projection Types

Use `projection` parameter to control returned data:

| Projection | Fields Returned | Use Case |
|------------|-----------------|----------|
| `"chemicaldetailstandard"` | Standard fields (default) | General purpose |
| `"chemicalidentifier"` | Identifiers only | Just need IDs/names |
| `"chemicalstructure"` | Structure data | Cheminformatics |
| `"ntatoolkit"` | NTA data | Mass spectrometry |
| `"ccdchemicaldetails"` | CCD chemical | CCD workflows |
| `"ccdassaydetails"` | CCD assay | Assay analysis |
| `"chemicaldetailall"` | All fields | Complete data |
| `"compact"` | Minimal fields | Bandwidth/storage |

---

## Configuration & Utilities

### API Key Management

```python
from pycomptox import save_api_key, load_api_key, delete_api_key, get_config_info

# Save API key (one-time setup)
save_api_key("your_api_key_here")

# Load API key (automatic in Chemical/ChemicalDetails)
api_key = load_api_key()

# Delete saved API key
delete_api_key()

# Get config information
info = get_config_info()
print(f"Config directory: {info['config_dir']}")
print(f"API key saved: {info['has_api_key']}")
```

### Command Line Tool

```bash
# Save API key
pycomptox-setup set YOUR_API_KEY

# Test API key
pycomptox-setup test

# Show API key (masked)
pycomptox-setup show

# Delete API key
pycomptox-setup delete
```

---

## Complete Workflow Example

```python
from pycomptox.chemical import Chemical, ChemicalDetails

# Initialize clients (API key auto-loaded)
searcher = Chemical()
details_client = ChemicalDetails()

# Step 1: Search for chemicals
chemical_names = ["Caffeine", "Aspirin", "Ibuprofen"]
dtxsids = []

for name in chemical_names:
    results = searcher.search_by_exact_value("name", name)
    if results:
        print(f"Found: {results[0]['displayName']} ({results[0]['dtxsid']})")
        dtxsids.append(results[0]['dtxsid'])

# Step 2: Get batch details
batch_details = details_client.data_by_dtxsid_batch(dtxsids)

# Step 3: Process results
for chem in batch_details:
    print(f"\nChemical: {chem['preferredName']}")
    print(f"  CAS RN: {chem.get('casrn', 'N/A')}")
    print(f"  Formula: {chem.get('molFormula', 'N/A')}")
    print(f"  Mass: {chem.get('monoisotopicMass', 'N/A')}")
    print(f"  SMILES: {chem.get('smiles', 'N/A')[:50]}...")
    print(f"  Active Assays: {chem.get('activeAssays', 'N/A')}")
```

---

## Common Patterns

### Search by CAS Number

```python
cas_rn = "80-05-7"
results = searcher.search_by_exact_value("rn", cas_rn)
dtxsid = results[0]['dtxsid']
details = details_client.data_by_dtxsid(dtxsid)
```

### Get Structure Information

```python
structure = details_client.data_by_dtxsid(
    dtxsid,
    projection="chemicalstructure"
)
smiles = structure['smiles']
inchi = structure['inchiString']
```

### Mass Range to Details

```python
# Find chemicals in mass range
dtxsids = searcher.search_ms_ready_by_mass_range(228.0, 228.2)

# Get details for all
details_list = details_client.data_by_dtxsid_batch(dtxsids[:100])  # First 100
```

### Multiple Searches to Batch Details

```python
# Search multiple ways
dtxsids = set()

# By names
for name in ["Caffeine", "Aspirin"]:
    results = searcher.search_by_exact_value("name", name)
    if results:
        dtxsids.add(results[0]['dtxsid'])

# By CAS numbers
for cas in ["58-08-2", "50-78-2"]:
    results = searcher.search_by_exact_value("rn", cas)
    if results:
        dtxsids.add(results[0]['dtxsid'])

# Get all details at once
details_list = details_client.data_by_dtxsid_batch(list(dtxsids))
```

---

## Bioactivity Data (`BioactivityData` class)

```python
from pycomptox.bioactivity import BioactivityData

client = BioactivityData(api_key=None, base_url="...", time_delay_between_calls=0.0)
```

### Summary Methods (Return Dict or List[Dict])

| Method | Description | Example |
|--------|-------------|---------|
| `get_summary_by_dtxsid(dtxsid)` | Chemical bioactivity summary | `client.get_summary_by_dtxsid("DTXSID7020182")` |
| `get_summary_by_dtxsid_and_tissue(dtxsid, tissue)` | Tissue-filtered summary | `client.get_summary_by_dtxsid_and_tissue("DTXSID7024241", "liver")` |
| `get_summary_by_aeid(aeid)` | Assay endpoint summary | `client.get_summary_by_aeid("3032")` |

### Detailed Data Methods (Return Dict or List[Dict])

| Method | Description | Example |
|--------|-------------|---------|
| `get_data_by_spid(spid)` | Data by sample ID | `client.get_data_by_spid("EPAPLT0232A03")` |
| `get_data_by_m4id(m4id)` | Data by data ID | `client.get_data_by_m4id("1135145")` |
| `get_data_by_dtxsid_and_projection(dtxsid, projection)` | Data with projection | `client.get_data_by_dtxsid_and_projection("DTXSID7020182", "toxcast-summary-plot")` |
| `get_data_by_aeid(aeid)` | Data by assay endpoint | `client.get_data_by_aeid(3032)` |

### AED Data Methods (Return Dict or List[Dict])

| Method | Description | Example |
|--------|-------------|---------|
| `get_aed_data_by_dtxsid(dtxsid)` | Activity-Exposure-Dose data | `client.get_aed_data_by_dtxsid("DTXSID5021209")` |

### Batch Methods

| Method | Returns | Example |
|--------|---------|---------|
| `find_bioactivity_data_by_spid_batch(spids)` | List[Dict] | `client.find_bioactivity_data_by_spid_batch(["EPAPLT0232A03", "EPAPLT0232A04"])` |
| `find_bioactivity_data_by_m4id_batch(m4ids)` | List[Dict] | `client.find_bioactivity_data_by_m4id_batch([1135145, 1135146])` |
| `find_bioactivity_data_by_dtxsid_batch(dtxsids)` | List[Dict] | `client.find_bioactivity_data_by_dtxsid_batch(["DTXSID7020182", "DTXSID9026974"])` |
| `find_bioactivity_data_by_aeid_batch(aeids)` | List[Dict] | `client.find_bioactivity_data_by_aeid_batch([3032, 3033])` |
| `find_aed_data_by_dtxsid_batch(dtxsids)` | List[Dict] | `client.find_aed_data_by_dtxsid_batch(["DTXSID5021209", "DTXSID7020182"])` |

---

## Bioactivity AOP (`BioactivityAOP` class)

```python
from pycomptox.bioactivity import BioactivityAOP

client = BioactivityAOP(api_key=None, base_url="...", time_delay_between_calls=0.0)
```

### AOP Data Methods (Return List[Dict])

| Method | Description | Example |
|--------|-------------|---------|
| `get_aop_data_by_toxcast_aeid(aeid)` | AOP by ToxCast AEID | `client.get_aop_data_by_toxcast_aeid(63)` |
| `get_aop_data_by_event_number(event_num)` | AOP by event number | `client.get_aop_data_by_event_number(18)` |
| `get_aop_data_by_entrez_gene_id(gene_id)` | AOP by gene ID | `client.get_aop_data_by_entrez_gene_id(196)` |

**AOP Record Fields:**
- `toxcastAeid`: ToxCast assay endpoint ID
- `entrezGeneId`: NCBI Entrez Gene ID
- `eventNumber`: AOP event number
- `eventLink`: Link to AOP event details
- `aopNumber`: AOP pathway number
- `aopLink`: Link to AOP pathway

---

## Rate Limiting

All classes support rate limiting:

```python
# Add 0.5 second delay between API calls
searcher = Chemical(time_delay_between_calls=0.5)
details_client = ChemicalDetails(time_delay_between_calls=0.5)
bioactivity = BioactivityData(time_delay_between_calls=0.5)
aop = BioactivityAOP(time_delay_between_calls=0.5)
```

---

## Error Handling

```python
try:
    results = searcher.search_by_exact_value("name", "Some Chemical")
    if results:
        details = details_client.data_by_dtxsid(results[0]['dtxsid'])
except ValueError as e:
    print(f"Invalid data: {e}")
except PermissionError as e:
    print(f"API key issue: {e}")
except RuntimeError as e:
    print(f"Request failed: {e}")
```

Common HTTP errors:
- **400 Bad Request**: Invalid parameters
- **401 Unauthorized**: Invalid/missing API key
- **404 Not Found**: Resource doesn't exist
- **429 Too Many Requests**: Rate limit exceeded

---

## Additional Resources

- **Full Documentation**: `README.md`
- **Chemical Details Guide**: `docs/CHEMICAL_DETAILS.md`
- **Bioactivity Data Guide**: `docs/BIOACTIVITY_DATA.md`
- **Batch Methods Guide**: `docs/BATCH_METHODS.md`
- **API Key Guide**: `docs/API_KEY_AND_RATE_LIMITING.md`
- **v0.2.0 Release Notes**: `docs/CHEMICAL_DETAILS_RELEASE.md`
- **Test Examples**: `tests/test_api.py`, `tests/test_batch_methods.py`, `tests/test_details.py`, `tests/test_bioactivitydata.py`, `tests/test_bioactivityaop.py`
- **CompTox API Docs**: https://comptox.epa.gov/ctx-api
