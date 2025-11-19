# PyCompTox

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/comptox-python.svg)](https://pypi.org/project/comptox-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/USEtox/PyCompTox/workflows/CI/badge.svg)](https://github.com/USEtox/PyCompTox/actions/workflows/ci.yml)
[![Documentation Status](https://img.shields.io/badge/docs-mkdocs-blue.svg)](https://usetox.github.io/PyCompTox/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python interface for the EPA CompTox Dashboard Chemical API.

## Overview

PyCompTox provides a simple and intuitive Python interface to interact with the EPA's [CompTox Dashboard](https://comptox.epa.gov/) Chemical, Bioactivity, Exposure, and Hazard API. This package allows you to search for chemicals by name, identifiers (DTXSID, DTXCID, CAS numbers), molecular formulas, mass ranges, and much more.

## Installation

### Quick Install

```bash
pip install comptox-python[all]
```

install the latest released version.  
**Note**: do not install the package by ~~`pip install pycomptox`~~ which is a different package with the old comptox API.  

For the latest development version:

```bash
# Clone the repository
git clone https://github.com/USEtox/PyCompTox.git
cd PyCompTox

# Install the package
pip install -e .

# Or with development tools
pip install -e ".[dev]"

# Or with notebook support
pip install -e ".[notebook]"
```

PyCompTox now uses modern Python packaging with `pyproject.toml`. See [INSTALLATION.md](docs/INSTALLATION.md) for detailed installation options.

### Optional Dependencies

- **dev**: Development tools (pytest, black, mypy, flake8)
- **notebook**: Jupyter notebook support with pandas and matplotlib
- **all**: All optional dependencies

```bash
pip install -e ".[all]"
```

## API Key Setup

To use the CompTox Dashboard API, you need an API key. You can obtain one from the [CompTox Dashboard API documentation](https://www.epa.gov/comptox-tools/computational-toxicology-and-exposure-apis).

### Save Your API Key (Recommended)

Save your API key once and it will be automatically loaded for all future sessions:

```bash
pycomptox-setup set YOUR_API_KEY
```

The API key is stored securely in your user's application data directory:
- **Windows**: `%APPDATA%\PyCompTox\api_key.txt`
- **macOS/Linux**: `~/.pycomptox/api_key.txt`

### Manage Your API Key

```bash
# Test if your API key works
pycomptox-setup test

# Show your saved API key (masked)
pycomptox-setup show

# Delete your saved API key
pycomptox-setup delete
```

### Alternative Methods

You can also provide the API key in other ways:

1. **Environment Variable**: Set `COMPTOX_API_KEY` environment variable
2. **Direct Parameter**: Pass `api_key` parameter when creating the client


## API Key Storage

Your API key is stored securely in your user's application data directory:
- **Windows**: `C:\Users\<username>\AppData\Roaming\PyCompTox\api_key.txt`
- **macOS/Linux**: `~/.pycomptox/api_key.txt`

The file is created with user-only read permissions on Unix-like systems.

## API Documentation

For detailed API documentation, visit:  
[Chemical](https://comptox.epa.gov/ctx-api/docs/chemical.html), [Bioactivity](https://comptox.epa.gov/ctx-api/docs/bioactivity.html), [Exposure](https://comptox.epa.gov/ctx-api/docs/exposure.html), and [Hazard](https://comptox.epa.gov/ctx-api/docs/hazard.html).

## License

See the LICENSE file for details.

## Disclaimer

This package is not officially affiliated with or endorsed by the U.S. Environmental Protection Agency (EPA). It is an independent implementation of a Python client for the publicly available CompTox Dashboard API.  
You can find [the official Python client](https://github.com/USEPA/ctx-python) from the [official USEPA GitHub page](https://github.com/USEPA).  

Also, note that there is another package called [pycomptox](https://github.com/Kunal627/pycomptox) that is registered on `PyPi` nder the same name, which is why this package is installed by `pip install comptox-python`.
