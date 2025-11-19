# API Key Management and Rate Limiting Guide

## Overview

This guide explains the new features added to PyCompTox:
1. **Persistent API Key Storage** - Save your API key once and reuse it automatically
2. **Rate Limiting** - Control the delay between API calls to respect usage limits

## API Key Management

### Why Store Your API Key?

Instead of providing your API key every time you create a `Chemical` client, you can save it once and PyCompTox will automatically load it. This is especially useful for:
- Interactive Python sessions
- Jupyter notebooks
- Scripts that run multiple times
- Sharing code without exposing your API key

### How to Save Your API Key

#### Method 1: Using the Command-Line Utility (Recommended)

```bash
# Save your API key
pycomptox-setup set YOUR_API_KEY_HERE

# Test that it works
pycomptox-setup test

# View your saved key (masked for security)
pycomptox-setup show

# Delete your saved key
pycomptox-setup delete
```

#### Method 2: Using Python

```python
from pycomptox import save_api_key, load_api_key, delete_api_key

# Save your API key
save_api_key("YOUR_API_KEY_HERE")

# Load your API key (returns None if not saved)
api_key = load_api_key()
print(api_key)

# Delete your API key
deleted = delete_api_key()  # Returns True if deleted, False if didn't exist
```

### Where Is My API Key Stored?

Your API key is stored in a plain text file in your user's application data directory:

- **Windows**: `C:\Users\<username>\AppData\Roaming\PyCompTox\api_key.txt`
- **macOS/Linux**: `~/.pycomptox/api_key.txt`

On Unix-like systems, the file permissions are set to `600` (readable only by the owner).

### API Key Loading Priority

PyCompTox looks for your API key in this order:

1. **Direct parameter**: `Chemical(api_key="your_key")`
2. **Environment variable**: `COMPTOX_API_KEY`
3. **Saved configuration file**: The file mentioned above

### Using the Saved API Key

Once saved, you can create a client without providing the API key:

```python
from pycomptox.chemical import Chemical

# API key is loaded automatically
client = Chemical()

# Use the client as normal
results = client.search_by_exact_value("Bisphenol A")
```

### Getting Configuration Information

```python
from pycomptox import get_config_info

info = get_config_info()
print(f"Config directory: {info['config_dir']}")
print(f"API key file: {info['api_key_file']}")
print(f"Has saved key: {info['has_saved_key']}")
print(f"Has env key: {info['has_env_key']}")
print(f"API key available: {info['api_key_available']}")
```

## Rate Limiting

### Why Rate Limiting?

API providers often limit the number of requests you can make per second or minute. Rate limiting helps you:
- Stay within API usage limits
- Avoid getting your API key throttled or blocked
- Be a good API citizen

### How to Use Rate Limiting

The `time_delay_between_calls` parameter controls the minimum delay between consecutive API calls:

```python
from pycomptox.chemical import Chemical

# Create a client with 0.5 second delay between calls
client = Chemical(time_delay_between_calls=0.5)

# Make multiple calls - delay is automatically enforced
for i in range(5):
    results = client.search_by_exact_value(f"DTXSID702018{i}")
    # Each call will have at least 0.5 seconds between them
```

### Default Behavior

By default, `time_delay_between_calls` is set to `0.0` seconds (no delay). This is appropriate for the current CompTox API which doesn't have strict rate limits.

### How It Works

The rate limiting mechanism:
1. Tracks the timestamp of the last API call
2. Before each new call, calculates the time elapsed since the last call
3. If less than `time_delay_between_calls` has elapsed, pauses for the remaining time
4. Makes the API call
5. Updates the last call timestamp

### Example: Batch Processing with Rate Limiting

```python
from pycomptox.chemical import Chemical
import time

# Create client with rate limiting
client = Chemical(time_delay_between_calls=1.0)  # 1 second between calls

chemicals = ["Bisphenol A", "Caffeine", "Aspirin", "Ibuprofen"]

start_time = time.time()
results = []

for chem_name in chemicals:
    print(f"Searching for {chem_name}...")
    try:
        result = client.search_by_substring_value(chem_name)
        results.append((chem_name, len(result)))
    except Exception as e:
        print(f"  Error: {e}")

elapsed = time.time() - start_time
print(f"\nProcessed {len(chemicals)} searches in {elapsed:.2f} seconds")
print(f"Average time per search: {elapsed/len(chemicals):.2f} seconds")

# Results
for name, count in results:
    print(f"  {name}: {count} results")
```

### Handling Rate Limit Errors

If you receive a 429 (Too Many Requests) error, increase the delay:

```python
from pycomptox.chemical import Chemical

try:
    # Try with no delay
    client = Chemical(time_delay_between_calls=0.0)
    results = client.search_by_substring_value("chemical")
except RuntimeError as e:
    if "Rate limit exceeded" in str(e):
        print("Rate limit hit! Recreating client with delay...")
        # Recreate with delay
        client = Chemical(time_delay_between_calls=2.0)
        results = client.search_by_substring_value("chemical")
```

### Testing Rate Limiting

You can test the rate limiting functionality:

```bash
python tests/test_api.py --test-rate-limit
```

This will make 3 API calls with a 0.5 second delay and verify the timing.

## Best Practices

### For API Key Management

1. **Never commit your API key to version control**
   - Add `*.txt` containing API keys to `.gitignore`
   - Use environment variables or saved configuration

2. **Use saved configuration for development**
   ```python
   # In your scripts
   from pycomptox.chemical import Chemical
   client = Chemical()  # Loads from saved config
   ```

3. **Use environment variables for production**
   ```bash
   export COMPTOX_API_KEY="your_key"
   python your_script.py
   ```

4. **Provide explicit key for testing/CI**
   ```python
   # In test scripts
   client = Chemical(api_key=os.getenv("TEST_API_KEY"))
   ```

### For Rate Limiting

1. **Start with no delay** (default: 0.0)
   - Only add delay if you encounter rate limiting

2. **Increase delay if needed**
   - Start with 0.5 seconds
   - Increase to 1.0 or 2.0 if still hitting limits

3. **Consider batching**
   - Group related searches together
   - Process results in batches

4. **Handle errors gracefully**
   ```python
   from pycomptox.chemical import Chemical
   
   client = Chemical(time_delay_between_calls=0.5)
   
   for item in large_list:
       try:
           result = client.search_by_exact_value(item)
           # Process result
       except RuntimeError as e:
           if "Rate limit exceeded" in str(e):
               # Increase delay and retry
               client.time_delay_between_calls = 2.0
               result = client.search_by_exact_value(item)
   ```

## Troubleshooting

### "No API key provided" Error

```python
ValueError: No API key provided. Please either:
1. Pass api_key parameter: Chemical(api_key='your_key')
2. Set COMPTOX_API_KEY environment variable
3. Save key using: from pycomptox import save_api_key; save_api_key('your_key')
```

**Solution**: Follow one of the three methods above to provide your API key.

### "Invalid API key or unauthorized access" Error

```python
PermissionError: Invalid API key or unauthorized access
```

**Solution**: Your API key is incorrect or expired. Get a new one from the CompTox Dashboard and save it again.

### "Rate limit exceeded" Error

```python
RuntimeError: Rate limit exceeded. Please increase time_delay_between_calls parameter.
```

**Solution**: Recreate your client with a larger `time_delay_between_calls` value:

```python
client = Chemical(time_delay_between_calls=2.0)
```

## Summary

- ✅ Save your API key once with `save_api_key()` or `pycomptox-setup`
- ✅ Create clients without providing API key: `Chemical()`
- ✅ Control rate limiting with `time_delay_between_calls` parameter
- ✅ Default delay is 0.0 seconds (no delay)
- ✅ Increase delay if you encounter rate limiting errors
- ✅ API key stored securely in user's application data directory
