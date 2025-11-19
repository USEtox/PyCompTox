# Configuration Guide

Learn how to configure PyCompTox for optimal usage.

## API Key Configuration

PyCompTox requires a CompTox Dashboard API key. You can obtain one from the [EPA CompTox Dashboard](https://comptox.epa.gov/dashboard/api).

### Persistent Storage (Recommended)

Save your API key once and use it across all scripts:

```python
from pycomptox import save_api_key

save_api_key("your-api-key-here")
```

Or use the command-line tool:

```bash
# Set API key
pycomptox-setup set your-api-key-here

# Show current configuration
pycomptox-setup show

# Test API connection
pycomptox-setup test

# Delete saved API key
pycomptox-setup delete
```

### Storage Location

API keys are stored in platform-specific locations:

- **Windows**: `C:\Users\<username>\AppData\Roaming\PyCompTox\api_key.txt`
- **macOS**: `~/Library/Application Support/PyCompTox/api_key.txt`
- **Linux**: `~/.config/PyCompTox/api_key.txt`

### Environment Variable

Set the `COMPTOX_API_KEY` environment variable:

```bash
# Linux/Mac
export COMPTOX_API_KEY=your-api-key-here

# Windows (Command Prompt)
set COMPTOX_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:COMPTOX_API_KEY="your-api-key-here"
```

### Direct Initialization

Pass the API key directly when creating a client:

```python
from pycomptox.chemical import Chemical

chem = Chemical(api_key="your_api_key_here")
```

## Rate Limiting

Configure rate limiting to avoid overwhelming the API:

```python
from pycomptox.chemical import Chemical

# Add 0.5 second delay between requests
chem = Chemical(time_delay_between_calls=0.5)

# Make multiple requests - automatically rate limited
for name in ["caffeine", "aspirin", "ibuprofen"]:
    results = chem.search_by_name(name)
```

### Recommended Settings

- **Light usage** (< 10 requests/minute): No delay needed
- **Moderate usage** (10-60 requests/minute): 0.5-1.0 second delay
- **Heavy usage** (> 60 requests/minute): 1.0-2.0 second delay

## Custom Base URL

Use a different API endpoint (e.g., for testing):

```python
from pycomptox.chemical import Chemical

chem = Chemical(base_url="https://custom-api-endpoint.com/ctx-api")
```

## Session Configuration

All clients use `requests.Session` for connection pooling and persistence. You can access the session to customize headers or other settings:

```python
from pycomptox.chemical import Chemical

chem = Chemical()

# Add custom headers
chem.session.headers.update({
    'User-Agent': 'MyApp/1.0'
})

# Configure timeouts (not built-in, requires modification)
# chem.session.timeout = 30
```

## Batch Request Configuration

Configure batch sizes for optimal performance:

```python
from pycomptox.chemical import Chemical

def process_in_batches(dtxsids, batch_size=100):
    """Process DTXSIDs in batches."""
    chem = Chemical(time_delay_between_calls=1.0)
    
    for i in range(0, len(dtxsids), batch_size):
        batch = dtxsids[i:i + batch_size]
        # Process batch (max 1000 per API)
        results = chem.get_chemical_by_dtxsid_batch(batch[:1000])
        yield results
```

## Error Handling Configuration

Configure how your application handles errors:

```python
from pycomptox.chemical import Chemical
import requests

chem = Chemical()

try:
    results = chem.search_by_name("caffeine")
except ValueError as e:
    # Handle not found errors
    print(f"Not found: {e}")
except RuntimeError as e:
    # Handle network errors
    print(f"Network error: {e}")
except requests.exceptions.RequestException as e:
    # Handle other request errors
    print(f"Request error: {e}")
```

## Logging Configuration

Add logging to track API calls:

```python
import logging
from pycomptox.chemical import Chemical

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create logger
logger = logging.getLogger('pycomptox')

chem = Chemical()

# Log API calls
def logged_search(name):
    logger.info(f"Searching for: {name}")
    results = chem.search_by_name(name)
    logger.info(f"Found {len(results)} results")
    return results

results = logged_search("caffeine")
```

## Advanced Configuration Example

```python
from pycomptox.chemical import Chemical, ChemicalDetails, ChemicalProperties
from pycomptox.extra import ExtraData
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pycomptox.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('pycomptox')

class CompToxClient:
    """Unified CompTox API client with advanced configuration."""
    
    def __init__(self, api_key=None, rate_limit=1.0, base_url=None):
        """
        Initialize CompTox client.
        
        Args:
            api_key: API key (optional if saved)
            rate_limit: Delay between requests in seconds
            base_url: Custom API endpoint (optional)
        """
        kwargs = {
            'time_delay_between_calls': rate_limit
        }
        if api_key:
            kwargs['api_key'] = api_key
        if base_url:
            kwargs['base_url'] = base_url
        
        self.search = Chemical(**kwargs)
        self.details = ChemicalDetails(**kwargs)
        self.properties = ChemicalProperties(**kwargs)
        self.extra = ExtraData(**kwargs)
        
        logger.info("CompTox client initialized")
    
    def get_complete_profile(self, dtxsid):
        """Get complete chemical profile."""
        logger.info(f"Fetching complete profile for {dtxsid}")
        
        return {
            'details': self.details.get_chemical_by_dtxsid(
                dtxsid, 
                projection='chemicaldetailall'
            ),
            'properties': self.properties.get_property_summary_by_dtxsid(dtxsid),
            'references': self.extra.get_data_by_dtxsid(dtxsid)
        }

# Usage
client = CompToxClient(rate_limit=0.5)
profile = client.get_complete_profile("DTXSID7020182")
```

## Configuration File

Create a configuration file for reusable settings:

```python
# config.py
COMPTOX_CONFIG = {
    'rate_limit': 1.0,
    'batch_size': 100,
    'timeout': 30,
    'retry_attempts': 3
}

# usage.py
from config import COMPTOX_CONFIG
from pycomptox.chemical import Chemical

chem = Chemical(
    time_delay_between_calls=COMPTOX_CONFIG['rate_limit']
)
```

## Testing Configuration

For testing, use a separate configuration:

```python
# test_config.py
import pytest
from pycomptox.chemical import Chemical

@pytest.fixture
def test_client():
    """Create a test client with extended delays."""
    return Chemical(time_delay_between_calls=2.0)

def test_search(test_client):
    results = test_client.search_by_name("caffeine")
    assert len(results) > 0
```

## See Also

- [Installation Guide](INSTALLATION.md)
- [Quick Start](quick_start.md)
- [Best Practices](best_practices.md)
- [API Reference](api/chemical.md)
