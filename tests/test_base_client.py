"""
Offline tests for the shared HTTP layer in :mod:`pycomptox.base`.

Every client routes through ``CachedAPIClient._make_cached_request``, so the
retry, timeout, error-translation, and cache-key behaviour tested here applies
to all 130 client methods. These tests use a local HTTP server rather than the
live API, so they need no key and no network.
"""

import http.server
import json
import threading

import pytest

from pycomptox.base import CachedAPIClient
from pycomptox.cache import CacheManager
from pycomptox.exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    NotFoundError,
    RateLimitError,
    ServerError,
)


class _Client(CachedAPIClient):
    """Concrete subclass; CachedAPIClient is abstract only by convention."""


class _Handler(http.server.BaseHTTPRequestHandler):
    """Serves scripted responses driven by the request path."""

    # {path_suffix: [status, ...]} - one status per call, last one repeats.
    script = {}
    calls = {}

    def log_message(self, *args):  # silence the test server
        pass

    def _respond(self):
        key = self.path.split("?")[0].rstrip("/").rsplit("/", 1)[-1]
        _Handler.calls[key] = _Handler.calls.get(key, 0) + 1
        statuses = _Handler.script.get(key, [200])
        index = min(_Handler.calls[key] - 1, len(statuses) - 1)
        status = statuses[index]

        body = json.dumps({"ok": status == 200, "path": self.path}).encode()
        self.send_response(status)
        if status == 429:
            self.send_header("Retry-After", "0")
        if key == "notjson":
            body = b"<html>not json</html>"
            self.send_header("Content-Type", "text/html")
        else:
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    do_GET = _respond
    do_POST = _respond


@pytest.fixture
def server():
    """Run the scripted HTTP server on a free port for one test."""
    _Handler.script = {}
    _Handler.calls = {}
    httpd = http.server.HTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield httpd, f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()
    httpd.server_close()


@pytest.fixture
def client(server):
    _, base_url = server
    return _Client(api_key="test-key", base_url=base_url, max_retries=2)


def test_missing_api_key_raises_configuration_error(monkeypatch, tmp_path):
    monkeypatch.delenv("COMPTOX_API_KEY", raising=False)
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    with pytest.raises(ConfigurationError, match="No API key provided"):
        _Client()


def test_api_key_is_sent_as_header(client):
    assert client.session.headers["x-api-key"] == "test-key"


def test_successful_request_returns_decoded_json(client):
    assert client._make_cached_request("ok")["ok"] is True


@pytest.mark.parametrize(
    "status,expected",
    [
        (401, AuthenticationError),
        (403, AuthenticationError),
        (404, NotFoundError),
        (400, APIError),
    ],
)
def test_http_errors_map_to_typed_exceptions(client, status, expected):
    _Handler.script["boom"] = [status]
    with pytest.raises(expected) as excinfo:
        client._make_cached_request("boom")
    assert excinfo.value.status_code == status


def test_rate_limit_error_after_retries_exhausted(client):
    _Handler.script["throttled"] = [429]
    with pytest.raises(RateLimitError) as excinfo:
        client._make_cached_request("throttled")
    assert excinfo.value.status_code == 429
    # initial attempt + 2 retries
    assert _Handler.calls["throttled"] == 3


def test_server_error_after_retries_exhausted(client):
    _Handler.script["down"] = [503]
    with pytest.raises(ServerError):
        client._make_cached_request("down")
    assert _Handler.calls["down"] == 3


def test_transient_failure_is_retried_then_succeeds(client):
    """A 503 followed by a 200 resolves without the caller seeing an error."""
    _Handler.script["flaky"] = [503, 200]
    assert client._make_cached_request("flaky")["ok"] is True
    assert _Handler.calls["flaky"] == 2


def test_post_is_retried(client):
    """POST retries too: every POST this library makes is a read-only query."""
    _Handler.script["batchflaky"] = [500, 200]
    result = client._make_cached_request("batchflaky", method="POST", json=["DTXSID1"])
    assert result["ok"] is True
    assert _Handler.calls["batchflaky"] == 2


def test_non_json_response_raises_api_error(client):
    with pytest.raises(APIError, match="non-JSON"):
        client._make_cached_request("notjson")


def test_timeout_is_applied_to_requests(client):
    assert client.timeout == (10.0, 60.0)


def test_explicit_timeout_is_respected(server):
    _, base_url = server
    assert _Client(api_key="k", base_url=base_url, timeout=1.5).timeout == 1.5


def test_leading_slash_does_not_double_up(client):
    """A leading slash must not produce a double-slashed URL."""
    result = client._make_cached_request("/ok")
    assert "//ok" not in result["path"]
    assert result["path"] == "/ok"


def test_trailing_slash_is_preserved(client):
    """The CompTox batch POST endpoints 404 without their trailing slash."""
    result = client._make_cached_request("batch/", method="POST", json=[])
    assert result["path"].endswith("/")


def test_caching_is_off_by_default(client):
    """Two identical calls hit the network twice when caching is not requested."""
    client._make_cached_request("uncached")
    client._make_cached_request("uncached")
    assert _Handler.calls["uncached"] == 2


def test_per_call_cache_opt_in(server, tmp_path):
    _, base_url = server
    cache = CacheManager(cache_dir=str(tmp_path / "cache"))
    client = _Client(api_key="k", base_url=base_url, cache_manager=cache)
    client._make_cached_request("cached", use_cache=True)
    client._make_cached_request("cached", use_cache=True)
    assert _Handler.calls["cached"] == 1, "second call should have been served from cache"


def test_get_and_post_do_not_share_a_cache_entry(server, tmp_path):
    """The same path served by GET and POST must cache separately."""
    _, base_url = server
    cache = CacheManager(cache_dir=str(tmp_path / "cache"))
    client = _Client(api_key="k", base_url=base_url, cache_manager=cache)
    client._make_cached_request("shared", use_cache=True)
    client._make_cached_request("shared", method="POST", json=["x"], use_cache=True)
    assert _Handler.calls["shared"] == 2, "GET and POST collided in the cache"


def test_rate_limiting_uses_a_monotonic_clock(client, monkeypatch):
    """
    Rate limiting must not be confused by a wall clock that steps backwards.

    The wall clock can jump back (NTP correction, VM or host suspend/resume). If
    the delay were measured with time.time(), a backward jump would make the
    measured interval negative and the client would sleep for longer than the
    configured delay. This simulates a 60s backward jump in time.time() and
    asserts the delay is still bounded by the configured value.
    """
    import time as time_module

    client.time_delay_between_calls = 0.2
    real_time = time_module.time()
    monkeypatch.setattr(time_module, "time", lambda: real_time - 60)

    client._make_cached_request("mono")
    start = time_module.monotonic()
    client._make_cached_request("mono")
    elapsed = time_module.monotonic() - start

    # Bounded well below the 60s a wall-clock implementation would have slept.
    assert elapsed < 5, f"rate limiter slept {elapsed:.1f}s; it is using the wall clock"


def test_default_time_delay_class_attribute_is_honoured(server):
    """Subclasses set a default delay without redefining __init__."""
    _, base_url = server

    class _Throttled(CachedAPIClient):
        default_time_delay = 0.25

    assert _Throttled(api_key="k", base_url=base_url).time_delay_between_calls == 0.25
    # an explicit argument still wins, including an explicit zero
    assert _Throttled(api_key="k", base_url=base_url,
                      time_delay_between_calls=0.0).time_delay_between_calls == 0.0
