"""
Import-surface tests for the ``pycomptox`` package.

The top-level ``__init__.py`` was once deleted by accident, which turned
``pycomptox`` into an implicit namespace package. Everything still imported via
the subpackages, so the existing tests stayed green while every documented
top-level import (``from pycomptox import Chemical``) raised ImportError, and
``py.typed`` stopped being honoured.

These tests are offline and need no API key.
"""

import importlib
import pkgutil

import pytest

import pycomptox


def test_package_is_not_a_namespace_package():
    """A real __init__.py must exist, otherwise the public API and py.typed break."""
    assert pycomptox.__file__ is not None, (
        "pycomptox has no __file__, so it is an implicit namespace package. "
        "src/pycomptox/__init__.py is missing."
    )
    assert pycomptox.__file__.endswith("__init__.py")


def test_version_is_exposed():
    """__version__ is present and not the metadata-missing fallback."""
    assert isinstance(pycomptox.__version__, str)
    assert pycomptox.__version__ != "0.0.0.dev0", (
        "version metadata unavailable; install the package (uv sync / pip install -e .)"
    )


@pytest.mark.parametrize("name", pycomptox.__all__)
def test_every_exported_name_resolves(name):
    """Every name in __all__ is actually importable from the top level."""
    assert hasattr(pycomptox, name), f"pycomptox.__all__ lists {name!r} but it is not defined"


def test_subpackages_are_importable():
    """The four grouped subpackages import and expose their own __all__."""
    for group in ("chemical", "hazard", "exposure", "bioactivity"):
        module = importlib.import_module(f"pycomptox.{group}")
        assert module.__all__, f"pycomptox.{group} exposes no __all__"
        for name in module.__all__:
            assert hasattr(module, name), f"pycomptox.{group}.{name} missing"


def test_subpackage_clients_are_reexported_at_top_level():
    """Every client in a subpackage's __all__ is also available flat."""
    missing = []
    for group in ("chemical", "hazard", "exposure", "bioactivity"):
        module = importlib.import_module(f"pycomptox.{group}")
        for name in module.__all__:
            if not hasattr(pycomptox, name):
                missing.append(f"{group}.{name}")
    assert not missing, f"clients not re-exported at top level: {missing}"


def test_all_client_modules_import_cleanly():
    """Importing every submodule raises nothing - catches syntax and import errors."""
    failures = []
    for info in pkgutil.walk_packages(pycomptox.__path__, prefix="pycomptox."):
        if info.name.endswith("__main__"):
            continue
        try:
            importlib.import_module(info.name)
        except Exception as exc:  # pragma: no cover - failure path
            failures.append(f"{info.name}: {type(exc).__name__}: {exc}")
    assert not failures, "modules failed to import:\n  " + "\n  ".join(failures)


def test_exceptions_share_a_common_base():
    """All library exceptions derive from CompToxError so callers can catch one type."""
    for name in (
        "ConfigurationError",
        "APIError",
        "AuthenticationError",
        "NotFoundError",
        "RateLimitError",
        "ServerError",
        "TimeoutError",
    ):
        exc = getattr(pycomptox, name)
        assert issubclass(exc, pycomptox.CompToxError), f"{name} does not derive from CompToxError"


def test_client_construction_requires_a_key(monkeypatch, tmp_path):
    """With no key anywhere, constructing a client raises ConfigurationError."""
    monkeypatch.delenv("COMPTOX_API_KEY", raising=False)
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    with pytest.raises(pycomptox.ConfigurationError):
        pycomptox.Chemical()


def test_caching_is_off_by_default(tmp_path, monkeypatch):
    """Caching is opt-in, and merely constructing a client writes nothing to disk."""
    monkeypatch.setenv("COMPTOX_API_KEY", "dummy-key-for-construction")
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    client = pycomptox.Chemical()
    assert client.use_cache is False
    assert not (tmp_path / ".pycomptox" / "cache").exists(), (
        "constructing a client created the cache directory; it should be lazy"
    )


def test_reading_config_does_not_write_to_disk(monkeypatch, tmp_path):
    """Asking where config lives, or whether a key exists, must not create anything."""
    from pycomptox.config import get_api_key_file, get_config_dir

    monkeypatch.delenv("COMPTOX_API_KEY", raising=False)
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    get_config_dir()
    get_api_key_file()
    pycomptox.load_api_key()
    pycomptox.get_config_info()

    assert not list(tmp_path.iterdir()), (
        f"read-only config calls created {[p.name for p in tmp_path.iterdir()]}"
    )


def test_saving_a_key_creates_the_config_dir(monkeypatch, tmp_path):
    """The write path does create the directory, and the key round-trips."""
    monkeypatch.delenv("COMPTOX_API_KEY", raising=False)
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    pycomptox.save_api_key("round-trip-key")
    assert pycomptox.load_api_key() == "round-trip-key"
    assert pycomptox.delete_api_key() is True


def test_requests_have_a_timeout(monkeypatch, tmp_path):
    """A default timeout is always set, so a call can never hang forever."""
    monkeypatch.setenv("COMPTOX_API_KEY", "dummy-key-for-construction")
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    client = pycomptox.Chemical()
    assert client.timeout is not None
    connect, read = client.timeout
    assert connect > 0 and read > 0


@pytest.mark.parametrize(
    "endpoint,expected",
    [
        ("/chemical/search/equal/x", "chemical/search/equal/x"),
        ("chemical/search/equal/x", "chemical/search/equal/x"),
        # Trailing slashes are significant on this API and must survive.
        ("/exposure/httk/search/by-dtxsid/", "exposure/httk/search/by-dtxsid/"),
        ("exposure/httk/search/by-dtxsid/", "exposure/httk/search/by-dtxsid/"),
    ],
)
def test_endpoint_normalization(endpoint, expected):
    """Leading slashes are stripped; trailing slashes are preserved."""
    from pycomptox.base import CachedAPIClient

    assert CachedAPIClient._normalize_endpoint(endpoint) == expected
