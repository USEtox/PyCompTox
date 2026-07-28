"""
Shared pytest configuration for the PyCompTox test suite.

Most tests in this suite call the live EPA CompTox API, which means they need a
valid API key and a network connection. Rather than annotating 40 files by hand,
this module marks every test as ``integration`` unless its module is listed in
:data:`OFFLINE_MODULES`, and skips the integration tests when no key is present.

A second axis is speed. Some ToxRefDB endpoints are unfiltered bulk scans that
take 15-50 seconds each, and the tests covering them dominate the suite's
runtime. Those are marked ``slow`` and skipped unless ``--run-slow`` is passed.

That makes these commands possible:

    pytest -m "not integration"   # offline, no API key needed
    pytest                        # live suite, without the slow bulk endpoints
    pytest --run-slow             # everything, including the bulk endpoints

Contributors without a key still get a meaningful signal from the offline subset,
and CI can run the offline tests on every push without a secret.

``slow`` is handled with a ``--run-slow`` flag rather than a ``-m "not slow"``
entry in ``addopts``: pytest accepts only one ``-m`` expression, so a
command-line ``-m`` would silently override an ``addopts`` one and quietly pull
the slow tests back in. A flag composes with any ``-m`` selection.
"""

import os
import pathlib

import pytest

# Modules whose tests run without network access or an API key.
OFFLINE_MODULES = {
    "test_spec_conformance",  # compares source against vendored OpenAPI specs
    "test_cache",             # exercises CacheManager against a temp directory
    "test_public_api",        # import-surface checks
    "test_base_client",       # HTTP layer, against a local test server
}


def _api_key_available() -> bool:
    """True if an API key can be resolved from the environment or saved config."""
    if os.getenv("COMPTOX_API_KEY"):
        return True
    if os.name == "nt":
        config_dir = pathlib.Path(
            os.getenv("APPDATA", pathlib.Path.home() / "AppData" / "Roaming")
        ) / "PyCompTox"
    else:
        config_dir = pathlib.Path.home() / ".pycomptox"
    key_file = config_dir / "api_key.txt"
    try:
        return key_file.is_file() and bool(key_file.read_text(encoding="utf-8").strip())
    except OSError:
        return False


HAS_API_KEY = _api_key_available()


def pytest_addoption(parser):
    """Add --run-slow, which opts into the slow bulk-endpoint tests."""
    parser.addoption(
        "--run-slow",
        action="store_true",
        default=False,
        help="Run tests marked 'slow' (ToxRefDB bulk endpoints; adds several minutes).",
    )


def pytest_collection_modifyitems(config, items):
    """
    Apply the unit/integration split, and skip ``slow`` tests unless asked for.

    Runs after collection so markers are applied uniformly without every test
    file having to declare them.
    """
    skip_integration = pytest.mark.skip(
        reason="needs a CompTox API key (set COMPTOX_API_KEY or run pycomptox-setup set KEY)"
    )
    skip_slow = pytest.mark.skip(reason="slow bulk-endpoint test; use --run-slow to include")
    run_slow = config.getoption("--run-slow")

    for item in items:
        module_name = item.module.__name__.rsplit(".", 1)[-1] if item.module else ""
        if module_name in OFFLINE_MODULES:
            item.add_marker(pytest.mark.unit)
            continue
        item.add_marker(pytest.mark.integration)
        if not HAS_API_KEY:
            item.add_marker(skip_integration)
        elif "slow" in item.keywords and not run_slow:
            item.add_marker(skip_slow)
