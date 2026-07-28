"""
Conformance tests: every endpoint the code calls must exist in the CompTox OpenAPI spec.

These tests are offline and need no API key. They exist because a family of bugs
in this library was of exactly one shape: a client built a URL that the API does
not serve, and nothing caught it until someone called the method against the
live service. Comparing the endpoint strings in the source against the vendored
specs catches that class of bug in CI instead.

The vendored specs in ``tests/specs/`` are slimmed copies of

    https://comptox.epa.gov/ctx-api/docs/{chemical,hazard,exposure,bioactivity}.json

Refresh them with ``python tests/specs/refresh.py`` when the API changes.

Two details of this API that the tests deliberately encode:

- **Trailing slashes are significant.** The batch POST endpoints answer on
  ``.../search/by-dtxsid/`` and return 404 without the trailing slash, so paths
  are compared with the trailing slash preserved.
- **A few live endpoints are absent from the published spec** (see
  ``UNDOCUMENTED_ENDPOINTS``). Those are allow-listed rather than treated as
  failures, because they were verified to return 200.
"""

import ast
import json
import pathlib
import re
from collections import defaultdict

import pytest

SRC_DIR = pathlib.Path(__file__).parent.parent / "src" / "pycomptox"
SPEC_DIR = pathlib.Path(__file__).parent / "specs"
SPEC_NAMES = ("chemical", "hazard", "exposure", "bioactivity")

# Endpoints the library calls that are missing from the published OpenAPI spec
# but verified to return HTTP 200 against the live API. Each needs a reason.
UNDOCUMENTED_ENDPOINTS = {
    ("GET", "chemical/all"): "Paginated full-chemical dump; live but undocumented.",
    ("GET", "chemical/ghslink/to-dtxsid/{}"): "PubChem GHS link; live but undocumented.",
    ("POST", "chemical/ghslink/to-dtxsid/"): "PubChem GHS link batch; live but undocumented.",
    ("GET", "chemical/wikipedia/by-dtxsid/{}"): "Wikipedia GHS link; live but undocumented.",
    ("POST", "chemical/wikipedia/by-dtxsid/"): "Wikipedia GHS link batch; live but undocumented.",
    ("POST", "hazard/toxref/search/by-dtxsid/"): "ToxRefDB batch; live but undocumented.",
}


def _normalize(path: str) -> str:
    """Collapse path parameters to ``{}``, drop a leading slash, keep the trailing one."""
    return re.sub(r"\{[^}]*\}", "{}", path).lstrip("/")


def _load_spec_endpoints():
    """Return {(METHOD, normalized_path): spec_name} for every documented operation."""
    endpoints = {}
    for name in SPEC_NAMES:
        spec = json.loads((SPEC_DIR / f"{name}.json").read_text())
        for path, ops in spec["paths"].items():
            for method in ops:
                endpoints[(method.upper(), _normalize(path))] = name
    return endpoints


def _iter_code_endpoints():
    """
    Yield (module, method_name, http_method, normalized_endpoint) for each call site.

    Walks the AST rather than grepping, so the HTTP method is read from the
    actual ``_make_cached_request`` keyword argument.
    """
    for f in sorted(SRC_DIR.rglob("*.py")):
        if f.name.startswith("__"):
            continue
        source = f.read_text()
        tree = ast.parse(source)
        for cls in [n for n in tree.body if isinstance(n, ast.ClassDef)]:
            for fn in cls.body:
                if not isinstance(fn, ast.FunctionDef):
                    continue
                segment = ast.get_source_segment(source, fn) or ""
                literals = re.findall(r'endpoint\s*=\s*f?"([^"]*)"', segment)
                if not literals:
                    continue
                http_method = (
                    "POST" if re.search(r"""method\s*=\s*['"]POST['"]""", segment) else "GET"
                )
                for raw in literals:
                    yield (
                        f"{f.parent.name}/{f.name}",
                        f"{cls.name}.{fn.name}",
                        http_method,
                        _normalize(raw),
                    )


SPEC_ENDPOINTS = _load_spec_endpoints()
CODE_ENDPOINTS = list(_iter_code_endpoints())


def test_specs_are_vendored():
    """All four specs are present and non-trivial."""
    assert len(SPEC_ENDPOINTS) > 100, f"only {len(SPEC_ENDPOINTS)} spec endpoints loaded"


def test_code_endpoints_were_discovered():
    """The AST walk actually found call sites, so a green suite means something."""
    assert len(CODE_ENDPOINTS) > 90, f"only {len(CODE_ENDPOINTS)} endpoints found in source"


@pytest.mark.parametrize(
    "module,method,http_method,endpoint",
    CODE_ENDPOINTS,
    ids=[f"{m}::{h}::{e}" for _, m, h, e in CODE_ENDPOINTS],
)
def test_endpoint_exists_in_spec(module, method, http_method, endpoint):
    """Every endpoint the library calls is documented, or explicitly allow-listed."""
    key = (http_method, endpoint)
    if key in UNDOCUMENTED_ENDPOINTS:
        pytest.skip(f"allow-listed: {UNDOCUMENTED_ENDPOINTS[key]}")

    if key in SPEC_ENDPOINTS:
        return

    # Give a specific diagnosis for the two mistakes that actually happened.
    without_slash = (http_method, endpoint.rstrip("/"))
    with_slash = (http_method, endpoint + "/")
    if with_slash in SPEC_ENDPOINTS:
        pytest.fail(
            f"{method} calls {http_method} {endpoint!r} but the spec documents "
            f"{endpoint + '/'!r}. The trailing slash is significant on this API - "
            f"without it the endpoint returns 404."
        )
    if without_slash in SPEC_ENDPOINTS and endpoint.endswith("/"):
        pytest.fail(
            f"{method} calls {http_method} {endpoint!r} but the spec documents "
            f"{endpoint.rstrip('/')!r}."
        )
    other = [m for (m, p) in SPEC_ENDPOINTS if p == endpoint]
    if other:
        pytest.fail(
            f"{method} calls {endpoint!r} with {http_method}, but the spec only "
            f"documents it for {', '.join(sorted(other))}."
        )
    pytest.fail(
        f"{method} ({module}) calls {http_method} {endpoint!r}, which is not in "
        f"the CompTox OpenAPI spec and is not allow-listed in "
        f"UNDOCUMENTED_ENDPOINTS. Either the path is wrong or the spec needs "
        f"refreshing (python tests/specs/refresh.py)."
    )


def test_allowlist_has_no_stale_entries():
    """An allow-listed endpoint that is now documented, or unused, should be removed."""
    called = {(h, e) for _, _, h, e in CODE_ENDPOINTS}
    stale = []
    for key in UNDOCUMENTED_ENDPOINTS:
        if key in SPEC_ENDPOINTS:
            stale.append(f"{key} is now documented in the spec")
        elif key not in called:
            stale.append(f"{key} is no longer called by any client")
    assert not stale, "stale UNDOCUMENTED_ENDPOINTS entries:\n  " + "\n  ".join(stale)


def test_report_unimplemented_endpoints():
    """
    Informational: list documented endpoints no client covers.

    This is coverage reporting, not a failure - the library does not aim to wrap
    every endpoint. It prints so the gap stays visible in CI output.
    """
    called = {(h, e) for _, _, h, e in CODE_ENDPOINTS}
    missing = defaultdict(list)
    for (method, path), spec_name in sorted(SPEC_ENDPOINTS.items()):
        if (method, path) not in called:
            missing[spec_name].append(f"{method} {path}")

    total = sum(len(v) for v in missing.values())
    print(f"\n{total} of {len(SPEC_ENDPOINTS)} documented endpoints are not implemented:")
    for spec_name in SPEC_NAMES:
        if missing[spec_name]:
            print(f"  {spec_name} ({len(missing[spec_name])}):")
            for entry in missing[spec_name]:
                print(f"    {entry}")
    assert total < len(SPEC_ENDPOINTS), "no endpoints implemented at all"
