# Caching System

PyCompTox includes a comprehensive caching system to reduce network traffic, improve performance, and minimize load on EPA's servers.

## Overview

The caching system provides:

- **Automatic caching** of all API responses
- **Unlimited cache size** by default
- **Export/import** functionality for cache portability
- **Cache statistics** and management
- **Per-request control** via `use_cache` parameter
- **Configurable expiration** for cache entries

## Quick Start

### Basic Usage

Caching is enabled by default and works automatically:

```python
from pycomptox import chemical

# First call - fetches from API and caches the response
chem = chemical.Chemical()
results1 = chem.search_by_starting_value("caffeine")  # API call + cache

# Second call - returns cached response (no API call)
results2 = chem.search_by_starting_value("caffeine")  # from cache
```

### Bypassing Cache

Use `use_cache=False` to bypass the cache for specific requests:

```python
from pycomptox import chemical

chem = chemical.Chemical()

# Force fresh data from API
results = chem.search_by_starting_value("caffeine", use_cache=False)
```

### Cache Management

```python
from pycomptox import cache_status, clear_cache

# Get cache statistics
status = cache_status()
print(f"Total entries: {status['total_entries']}")
print(f"Cache size: {status['total_size_mb']} MB")
print(f"Endpoints cached: {list(status['endpoints'].keys())}")

# Clear entire cache
cleared = clear_cache()
print(f"Cleared {cleared} cache entries")

# Clear specific endpoint
cleared = clear_cache("chemical/search")
```

## Cache Configuration

### Default Cache Location

By default, cache files are stored in:
- **Windows**: `C:\Users\<username>\.pycomptox\cache\`
- **macOS/Linux**: `~/.pycomptox/cache/`

### Custom Cache Configuration

```python
from pycomptox import CacheManager, set_default_cache

# Create custom cache with expiration
custom_cache = CacheManager(
    cache_dir="/path/to/custom/cache",
    max_age_days=7,  # Expire entries after 7 days
    enabled=True
)

# Set as default for all API clients
set_default_cache(custom_cache)

# Or use with specific client
from pycomptox import chemical
chem = chemical.Chemical(cache_manager=custom_cache)
```

### Disable Caching

```python
from pycomptox import CacheManager, set_default_cache

# Disable caching globally
disabled_cache = CacheManager(enabled=False)
set_default_cache(disabled_cache)

# Or disable for specific client
from pycomptox import chemical
chem = chemical.Chemical(use_cache=False)
```

## Cache Export and Import

### Exporting Cache

Export cache to share with others or backup:

```python
from pycomptox import export_cache

# Export entire cache to a file
result = export_cache("my_cache_backup.json")

print(f"Exported {result['entries_exported']} entries")
print(f"File size: {result['file_size_mb']} MB")
```

### Importing Cache

Import previously exported cache:

```python
from pycomptox import import_cache

# Import cache from file
result = import_cache("my_cache_backup.json")

print(f"Imported {result['entries_imported']} entries")
print(f"Skipped {result['entries_skipped']} existing entries")

# Overwrite existing entries
result = import_cache("my_cache_backup.json", overwrite=True)
```

## Cache Statistics

Get detailed information about cache usage:

```python
from pycomptox import cache_status

status = cache_status()

# Basic information
print(f"Cache enabled: {status['enabled']}")
print(f"Cache directory: {status['cache_dir']}")
print(f"Max age (days): {status['max_age_days']}")

# Size statistics
print(f"\nTotal entries: {status['total_entries']}")
print(f"Total size: {status['total_size_mb']} MB")

# Per-endpoint breakdown
print("\nEntries by endpoint:")
for endpoint, count in status['endpoints'].items():
    print(f"  {endpoint}: {count} entries")

# Time information
print(f"\nOldest entry: {status['oldest_entry']}")
print(f"Newest entry: {status['newest_entry']}")
```

## Advanced Usage

### Cleanup Expired Entries

If using cache expiration, manually trigger cleanup:

```python
from pycomptox import CacheManager

cache = CacheManager(max_age_days=30)

# Remove entries older than 30 days
removed = cache.cleanup_expired()
print(f"Removed {removed} expired entries")
```

### Per-Client Cache Configuration

Different clients can use different cache settings:

```python
from pycomptox import chemical, exposure, CacheManager

# Cache for chemical data (7 day expiration)
chem_cache = CacheManager(
    cache_dir="~/.pycomptox/cache/chemical",
    max_age_days=7
)

# Cache for exposure data (30 day expiration)
exp_cache = CacheManager(
    cache_dir="~/.pycomptox/cache/exposure",
    max_age_days=30
)

# Use different caches for different clients
chem = chemical.Chemical(cache_manager=chem_cache)
exp_pred = exposure.ExposurePrediction(cache_manager=exp_cache)
```

### Selective Caching

Cache some requests but not others:

```python
from pycomptox import chemical

chem = chemical.Chemical()

# Cache this search
results1 = chem.search_by_starting_value("common_chemical", use_cache=True)

# Don't cache this rare search
results2 = chem.search_by_starting_value("rare_chemical", use_cache=False)

# Use default setting (True)
results3 = chem.search_by_starting_value("another_chemical")
```

## Cache Management Best Practices

### 1. Monitor Cache Size

Regularly check cache size to prevent disk space issues:

```python
from pycomptox import cache_status

status = cache_status()

# Alert if cache exceeds 1 GB
if status['total_size_mb'] > 1024:
    print("Warning: Cache size exceeds 1 GB")
    print("Consider clearing old entries or setting expiration")
```

### 2. Set Appropriate Expiration

For data that changes frequently, use shorter expiration:

```python
from pycomptox import CacheManager, set_default_cache

# Expire entries after 7 days
cache = CacheManager(max_age_days=7)
set_default_cache(cache)

# Periodically cleanup
cache.cleanup_expired()
```

### 3. Export Cache for Reuse

Share cache with team members or across projects:

```python
from pycomptox import export_cache, import_cache

# Export cache
export_cache("shared_cache.json")

# On another machine or project
import_cache("shared_cache.json")
```

### 4. Clear Cache Selectively

Clear specific endpoints when data might be stale:

```python
from pycomptox import clear_cache

# Clear only chemical search cache
clear_cache("chemical/search")

# Keep other cached data
```

### 5. Disable for Development

Disable cache during development to always get fresh data:

```python
from pycomptox import CacheManager, set_default_cache

# Development mode - no caching
dev_cache = CacheManager(enabled=False)
set_default_cache(dev_cache)
```

## Performance Benefits

Caching provides significant performance improvements:

```python
import time
from pycomptox import chemical, clear_cache

chem = chemical.Chemical()

# Clear cache for fair test
clear_cache()

# First call (no cache)
start = time.time()
results1 = chem.search_by_starting_value("caffeine")
time1 = time.time() - start
print(f"First call (API): {time1:.3f} seconds")

# Second call (cached)
start = time.time()
results2 = chem.search_by_starting_value("caffeine")
time2 = time.time() - start
print(f"Second call (cache): {time2:.3f} seconds")

print(f"Speedup: {time1/time2:.1f}x faster")
```

Typical results:
- **First call (API)**: 0.5-2.0 seconds
- **Second call (cache)**: 0.001-0.005 seconds
- **Speedup**: 100-1000x faster

## Cache File Format

Cache entries are stored as JSON files with the following structure:

```json
{
  "timestamp": "2025-11-18T10:30:00.123456",
  "endpoint": "chemical/search",
  "params": {
    "name": "caffeine"
  },
  "response": {
    "dtxsid": "DTXSID0020268",
    "preferredName": "Caffeine",
    "casrn": "58-08-2"
  }
}
```

This format allows:
- Easy inspection of cached data
- Manual editing if needed
- Version control friendly (when exported)

## Troubleshooting

### Cache Not Working

Check cache status to diagnose issues:

```python
from pycomptox import cache_status

status = cache_status()

if not status['enabled']:
    print("Cache is disabled")
elif status['total_entries'] == 0:
    print("Cache is empty - first requests will populate it")
else:
    print(f"Cache working: {status['total_entries']} entries")
```

### Cache Directory Permissions

If cache fails silently, check directory permissions:

```python
from pycomptox import cache_status
from pathlib import Path

status = cache_status()
cache_dir = Path(status['cache_dir'])

if cache_dir.exists():
    if not cache_dir.is_dir():
        print("Cache path exists but is not a directory")
    elif not os.access(cache_dir, os.W_OK):
        print("No write permission for cache directory")
else:
    print("Cache directory does not exist - will be created on first use")
```

### Corrupted Cache Entries

The cache system automatically removes corrupted entries:

```python
from pycomptox import CacheManager

cache = CacheManager()

# This will return None and delete corrupted file
result = cache.get("endpoint", {"param": "value"})
```

### Large Cache Size

If cache grows too large:

```python
from pycomptox import cache_status, clear_cache, CacheManager, set_default_cache

status = cache_status()
print(f"Cache size: {status['total_size_mb']} MB")

# Option 1: Clear entire cache
clear_cache()

# Option 2: Clear specific endpoints
clear_cache("chemical/search")

# Option 3: Enable expiration for future entries
cache = CacheManager(max_age_days=30)
set_default_cache(cache)
cache.cleanup_expired()
```

## API Reference

For complete API documentation, see:
- [Cache API Reference](api/cache.md)
