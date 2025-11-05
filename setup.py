"""
Backward compatibility shim for setup.py.

Modern configuration is now in pyproject.toml (PEP 621).
This file exists only for backward compatibility with older tools.
"""

from setuptools import setup

# All configuration is now in pyproject.toml
# This shim ensures compatibility with tools that still expect setup.py
setup()
