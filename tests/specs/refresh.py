#!/usr/bin/env python3
"""
Refresh the vendored CompTox OpenAPI specs used by tests/test_spec_conformance.py.

The upstream specs are large and mostly schema definitions the conformance test
does not need, so only paths, HTTP methods, and summaries are kept.

Usage:
    python tests/specs/refresh.py
"""

import json
import pathlib
import urllib.request

SPEC_NAMES = ("chemical", "hazard", "exposure", "bioactivity")
BASE_URL = "https://comptox.epa.gov/ctx-api/docs"
OUT_DIR = pathlib.Path(__file__).parent


def slim(spec):
    """Keep only what the conformance test reads."""
    return {
        "info": {
            "version": spec["info"].get("version"),
            "title": spec["info"].get("title"),
        },
        "paths": {
            path: {
                method: {"summary": op.get("summary") or ""}
                for method, op in ops.items()
                if method in ("get", "post")
            }
            for path, ops in spec["paths"].items()
        },
    }


def main():
    for name in SPEC_NAMES:
        url = f"{BASE_URL}/{name}.json"
        with urllib.request.urlopen(url, timeout=60) as response:
            spec = json.load(response)
        out = OUT_DIR / f"{name}.json"
        out.write_text(json.dumps(slim(spec), indent=1, sort_keys=True) + "\n")
        print(f"{out}: {len(spec['paths'])} paths (spec version {spec['info'].get('version')})")


if __name__ == "__main__":
    main()
