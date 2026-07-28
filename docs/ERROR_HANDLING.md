# Error Handling

Every error PyCompTox raises derives from `CompToxError`, so a single `except`
clause can catch anything the library produces while still letting you handle
the common cases individually.

## The hierarchy

```
CompToxError                    # base - catch this to handle everything
├── ConfigurationError          # no API key available
├── TimeoutError                # request exceeded the timeout
└── APIError                    # unsuccessful HTTP response
    ├── AuthenticationError     # 401 / 403 - key missing, invalid, or no access
    ├── NotFoundError           # 404 - identifier or resource does not exist
    ├── RateLimitError          # 429 - rate limit exceeded
    └── ServerError             # 5xx - the API failed
```

`ValueError` is still raised for local input validation — an empty DTXSID, a
batch over the documented size limit — because those are programming errors
caught before any request is made.

## Basic usage

```python
from pycomptox import Chemical
from pycomptox.exceptions import CompToxError, NotFoundError, RateLimitError

client = Chemical()

try:
    results = client.search_by_exact_value("Bisphenol A")
except NotFoundError:
    print("No such chemical")
except RateLimitError as exc:
    print(f"Rate limited; retry after {exc.retry_after}s")
except CompToxError as exc:
    print(f"Something else went wrong: {exc}")
```

## Inspecting an API error

`APIError` and its subclasses carry the details of the failed response:

```python
from pycomptox.exceptions import APIError

try:
    client.search_by_exact_value("Bisphenol A")
except APIError as exc:
    print(exc.status_code)     # e.g. 404
    print(exc.url)             # the URL that was requested
    print(exc.response_text)   # response body, truncated to 500 chars
```

## Treating "not found" as an empty result

For many endpoints a 404 just means the chemical has no data of that kind,
which is often not an error in your program:

```python
from pycomptox import ToxValDB
from pycomptox.exceptions import NotFoundError

tox = ToxValDB()

def safe_get(dtxsid):
    try:
        return tox.get_data_by_dtxsid(dtxsid)
    except NotFoundError:
        return []

for dtxsid in ["DTXSID7020182", "DTXSID9999999"]:
    print(dtxsid, len(safe_get(dtxsid)))
```

## Timeouts and retries

Every request carries a timeout and retries transient failures automatically,
so most 429 and 5xx blips resolve without reaching your code.

- **Timeout** defaults to 10s connect, 60s read. Override with `timeout`, as a
  single number or a `(connect, read)` pair.
- **Retries** default to 3 attempts with exponential backoff, applied to 429 and
  5xx responses. A `Retry-After` header is honoured when present. Override with
  `max_retries`.

```python
# A slow bulk endpoint, with more patience and more retries
client = Chemical(timeout=(10, 300), max_retries=5)

# Fail fast instead
client = Chemical(timeout=5, max_retries=0)
```

`RateLimitError` or `ServerError` is raised only after the retries are
exhausted. If you hit rate limits routinely, add client-side throttling instead
of relying on retries:

```python
client = Chemical(time_delay_between_calls=0.5)   # >= 0.5s between calls
```

Some clients set a non-zero default because their endpoints are heavier or more
rate-sensitive — `ChemicalList` and `PubChemLink` default to 0.5s, and
`BioactivityModel` to 0.1s. Pass `time_delay_between_calls` explicitly to
override, including `0.0` to disable it.

## Missing API key

Constructing any client without a resolvable key raises `ConfigurationError`
immediately, rather than failing later on the first request:

```python
from pycomptox import Chemical
from pycomptox.exceptions import ConfigurationError

try:
    client = Chemical()
except ConfigurationError as exc:
    print(exc)   # lists every way to supply a key
```

See [API Key & Rate Limiting](API_KEY_AND_RATE_LIMITING.md) for how keys are
resolved.

## Migrating from 0.6.x

Before 0.7.0 the library let raw `requests` exceptions reach callers, and its
docstrings advertised `RuntimeError` and `PermissionError` that were never
actually raised. Code that caught those needs updating:

| 0.6.x | 0.7.0 |
| --- | --- |
| `except requests.exceptions.HTTPError` | `except APIError` |
| `except requests.exceptions.Timeout` | `except pycomptox.exceptions.TimeoutError` |
| `except RuntimeError` (never raised) | `except APIError` |
| `except PermissionError` (never raised) | `except AuthenticationError` |
| `except ValueError` for a missing key | `except ConfigurationError` |

`ValueError` is unchanged for input validation.
