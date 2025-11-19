# Best Practices

Guidelines for effective use of PyCompTox.

## API Key Management

### ✅ Do

- Save API key using `save_api_key()` for persistent storage
- Use environment variables for CI/CD pipelines
- Keep API keys confidential and out of version control

### ❌ Don't

- Hardcode API keys in scripts
- Commit API keys to Git repositories
- Share API keys publicly

```python
# ✅ Good
from pycomptox import save_api_key
save_api_key("your-key")  # Save once, use everywhere

# ❌ Bad
chem = Chemical(api_key="hardcoded-key-123")  # Don't do this!
```

## Rate Limiting

### ✅ Do

- Use rate limiting for bulk operations
- Respect API limits to avoid throttling
- Use batch methods when querying multiple chemicals

### ❌ Don't

- Make rapid-fire requests without delays
- Query one chemical at a time when batch methods are available

```python
# ✅ Good - Use batch methods
dtxsids = ["DTXSID7020182", "DTXSID2021315", "DTXSID5020001"]
results = chem.get_chemical_by_dtxsid_batch(dtxsids)

# ❌ Bad - Individual requests
results = [chem.get_chemical_by_dtxsid(d) for d in dtxsids]
```

## Batch Operations

### Optimize Batch Sizes

```python
def process_large_dataset(dtxsids, batch_size=500):
    """Process large datasets efficiently."""
    from pycomptox.chemical import Chemical
    
    chem = Chemical(time_delay_between_calls=1.0)
    all_results = []
    
    for i in range(0, len(dtxsids), batch_size):
        batch = dtxsids[i:i + batch_size]
        # API max is 1000, but smaller batches are more reliable
        results = chem.get_chemical_by_dtxsid_batch(batch[:1000])
        all_results.extend(results)
    
    return all_results
```

## Error Handling

### ✅ Do

- Always wrap API calls in try-except blocks
- Handle specific exceptions appropriately
- Log errors for debugging

```python
import logging

logger = logging.getLogger(__name__)

def safe_search(name):
    """Safely search for a chemical."""
    try:
        chem = Chemical()
        results = chem.search_by_name(name)
        return results
    except ValueError as e:
        logger.warning(f"Chemical not found: {name}")
        return []
    except RuntimeError as e:
        logger.error(f"API error: {e}")
        return []
```

### ❌ Don't

- Use bare except clauses
- Silently ignore errors
- Let exceptions propagate without handling

```python
# ❌ Bad
try:
    results = chem.search_by_name(name)
except:  # Too broad!
    pass  # Silent failure!
```

## Performance Optimization

### Use Projections

Only request the data you need:

```python
from pycomptox.chemical import ChemicalDetails

details = ChemicalDetails()

# ✅ Good - Request only what you need
info = details.get_chemical_by_dtxsid(
    "DTXSID7020182",
    projection="chemicalidentifier"  # Minimal data
)

# ⚠️ Less efficient - Gets everything
info = details.get_chemical_by_dtxsid(
    "DTXSID7020182",
    projection="chemicaldetailall"  # All data
)
```

### Cache Results

Cache frequently accessed data:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_chemical_cached(dtxsid):
    """Get chemical with caching."""
    details = ChemicalDetails()
    return details.get_chemical_by_dtxsid(dtxsid)

# First call - fetches from API
data1 = get_chemical_cached("DTXSID7020182")

# Second call - returns cached result
data2 = get_chemical_cached("DTXSID7020182")  # Fast!
```

### Reuse Clients

Reuse client instances to benefit from connection pooling:

```python
# ✅ Good - Reuse client
chem = Chemical()
for name in chemical_names:
    results = chem.search_by_name(name)

# ❌ Bad - New client each time
for name in chemical_names:
    chem = Chemical()  # Wasteful!
    results = chem.search_by_name(name)
```

## Data Validation

### Validate DTXSIDs

```python
def is_valid_dtxsid(dtxsid):
    """Check if DTXSID format is valid."""
    import re
    pattern = r'^DTXSID\d+$'
    return bool(re.match(pattern, dtxsid))

# Use before API calls
if is_valid_dtxsid(dtxsid):
    data = chem.get_chemical_by_dtxsid(dtxsid)
```

### Handle Missing Data

```python
# ✅ Good - Check for None/missing values
result = chem.search_by_name("chemical")
if result and result[0].get('casrn'):
    casrn = result[0]['casrn']
else:
    casrn = "Not available"

# ❌ Bad - Assumes data exists
casrn = result[0]['casrn']  # May raise KeyError!
```

## Code Organization

### Create Wrapper Classes

```python
class ChemicalAnalyzer:
    """Unified interface for chemical analysis."""
    
    def __init__(self, rate_limit=1.0):
        self.search = Chemical(time_delay_between_calls=rate_limit)
        self.details = ChemicalDetails(time_delay_between_calls=rate_limit)
        self.properties = ChemicalProperties(time_delay_between_calls=rate_limit)
        self.extra = ExtraData(time_delay_between_calls=rate_limit)
    
    def analyze_chemical(self, identifier, id_type='name'):
        """Complete chemical analysis."""
        # Search
        if id_type == 'name':
            results = self.search.search_by_name(identifier)
        elif id_type == 'casrn':
            results = self.search.search_by_casrn(identifier)
        
        if not results:
            return None
        
        dtxsid = results[0]['dtxsid']
        
        # Gather all data
        return {
            'basic': results[0],
            'details': self.details.get_chemical_by_dtxsid(dtxsid),
            'properties': self.properties.get_property_summary_by_dtxsid(dtxsid),
            'references': self.extra.get_data_by_dtxsid(dtxsid)
        }
```

## Testing

### Write Unit Tests

```python
import pytest
from pycomptox.chemical import Chemical

@pytest.fixture
def chem_client():
    return Chemical()

def test_search_by_name(chem_client):
    results = chem_client.search_by_name("caffeine")
    assert len(results) > 0
    assert 'dtxsid' in results[0]

def test_invalid_search(chem_client):
    results = chem_client.search_by_name("xyz123notachemical")
    # Should return empty list, not raise error
    assert results == [] or len(results) == 0
```

### Use Mocking for Tests

```python
from unittest.mock import patch, MagicMock

def test_with_mock():
    with patch('pycomptox.search.Chemical.search_by_name') as mock_search:
        mock_search.return_value = [
            {'dtxsid': 'DTXSID123', 'preferredName': 'Test'}
        ]
        
        chem = Chemical()
        results = chem.search_by_name("test")
        
        assert len(results) == 1
        assert results[0]['dtxsid'] == 'DTXSID123'
```

## Documentation

### Document Your Code

```python
def analyze_toxicity(dtxsid: str) -> dict:
    """
    Analyze toxicity profile for a chemical.
    
    Args:
        dtxsid: DSSTox Substance Identifier
        
    Returns:
        Dictionary containing toxicity analysis:
            - properties: Property data
            - predictions: QSAR predictions
            - experimental: Experimental measurements
            
    Raises:
        ValueError: If chemical not found
        RuntimeError: If API request fails
        
    Example:
        >>> profile = analyze_toxicity("DTXSID7020182")
        >>> print(profile['properties'])
    """
    pass
```

## Logging

### Implement Structured Logging

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module
        }
        return json.dumps(log_data)

# Configure logger
logger = logging.getLogger('pycomptox')
handler = logging.FileHandler('pycomptox.json')
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
```

## Security

### Protect Sensitive Data

```python
import os
from pathlib import Path

def get_api_key():
    """Securely load API key."""
    # Try environment variable first
    key = os.environ.get('COMPTOX_API_KEY')
    
    if not key:
        # Try config file with restricted permissions
        key_file = Path.home() / '.pycomptox' / 'api_key.txt'
        if key_file.exists():
            # Check file permissions (Unix)
            if key_file.stat().st_mode & 0o077:
                raise PermissionError("API key file has insecure permissions")
            key = key_file.read_text().strip()
    
    return key
```

## See Also

- [Configuration Guide](configuration.md)
- [Quick Start](quick_start.md)
- [API Reference](api/chemical.md)
- [Examples](examples.md)
