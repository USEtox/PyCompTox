# Batch Methods Implementation Notes

## Summary

Three batch methods have been implemented for the PyCompTox Chemical Search API:

1. `search_by_exact_batch_values(values)` - Batch search by exact values
2. `search_ms_ready_by_mass_range_batch(masses, error)` - Batch search by mass ranges  
3. `search_ms_ready_by_dtxcid_batch(dtxcids)` - Batch search MS-ready by DTXCIDs

## Implementation Details

### 1. search_by_exact_batch_values

**Endpoint**: `POST /chemical/search/equal/`

**Input Format**:
- List of strings (chemical names, DTXSIDs, CAS numbers, etc.)
- Maximum 200 values per batch
- Values are joined with `\\n` separator

**Current Behavior**:
- The API appears to treat the batch as a single search string
- May need further investigation on the correct format

**Usage**:
```python
values = ["DTXSID7020182", "Bisphenol A", "80-05-7"]
results = client.search_by_exact_batch_values(values)
```

### 2. search_ms_ready_by_mass_range_batch

**Endpoint**: `POST /chemical/msready/search/by-mass/`

**Input Format**:
```python
{
    "masses": [200.9, 201.0, 201.1],
    "error": 0.01
}
```

**Output Format**:
- Dictionary with mass values as keys
- Each key maps to a list of DTXSID identifiers

**Usage**:
```python
masses = [200.9, 201.0, 201.1]
results = client.search_ms_ready_by_mass_range_batch(masses, error=0.01)
# Returns: {"200.9": ["DTXSID1...", ...], "201.0": [...], ...}
```

### 3. search_ms_ready_by_dtxcid_batch

**Endpoint**: `POST /chemical/msready/search/by-dtxcid/`

**Input Format**:
- List of DTXCID strings

**Output Format**:
- List of MS-ready DTXSID identifiers
- The API returns all MS-ready forms for all input DTXCIDs

**Usage**:
```python
dtxcids = ["DTXCID30182", "DTXCID20182"]
results = client.search_ms_ready_by_dtxcid_batch(dtxcids)
# Returns: ["DTXSID1...", "DTXSID2...", ...]
```

## Testing Results

### Test 1: Batch Exact Search
- ✓ Method implemented and working
- ⚠ API behavior may not match documentation
- The API appears to concatenate values and search as one string

### Test 2: Mass Range Batch
- ✓ Implemented correctly
- ✓ Returns dictionary with mass keys
- ✓ Each mass maps to list of DTXSIDs

### Test 3: DTXCID Batch  
- ✓ Implemented correctly
- ✓ Returns flat list of all MS-ready forms
- ✓ Successfully found 24 MS-ready forms for 3 input DTXCIDs

## Known Issues

1. **search_by_exact_batch_values**: The API may not support true batch searching as documented. It appears to treat the newline-separated string as a single search query. This may require:
   - Further API documentation review
   - Contact with API maintainers
   - Alternative implementation approach

## Recommendations

1. **For search_by_exact_batch_values**: Consider implementing a wrapper that:
   - Calls the single-value search endpoint for each value
   - Aggregates results
   - Applies rate limiting between calls

2. **Rate Limiting**: When using batch methods, consider setting appropriate delays:
   ```python
   client = Chemical(time_delay_between_calls=0.5)
   ```

3. **Error Handling**: Implement retry logic for batch operations

4. **Validation**: All three methods include input validation for empty lists

## Future Enhancements

1. Add retry logic for failed batch operations
2. Implement chunking for large batches
3. Add progress callbacks for long-running batch operations
4. Consider async implementation for better performance
5. Add result caching to avoid duplicate API calls

## Code Location

- Implementation: `src/pycomptox/search.py`
- Tests: `tests/test_batch_methods.py`
- Lines: ~470-600 in search.py
