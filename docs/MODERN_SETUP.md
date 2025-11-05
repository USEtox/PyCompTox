# Modern Setup Configuration - PyCompTox v0.3.0

## Overview

PyCompTox has been upgraded to use modern Python packaging standards (PEP 621) with `pyproject.toml` as the primary configuration file.

## What Changed

### ✅ New: pyproject.toml

All project metadata and configuration is now in `pyproject.toml`:

- **Package metadata**: name, version, description, authors, URLs
- **Dependencies**: Core and optional dependencies
- **Build system**: Modern build backend (setuptools>=61.0)
- **Tool configurations**: black, mypy, pytest, coverage, isort
- **Entry points**: CLI command `pycomptox-setup`

### ✅ Updated: setup.py

`setup.py` is now a minimal backward compatibility shim:
- All configuration moved to `pyproject.toml`
- Keeps compatibility with older tools
- Simply calls `setup()` with no arguments

### ✅ New: __main__.py

Added CLI module with command-line interface:
- `pycomptox-setup set YOUR_KEY` - Save API key
- `pycomptox-setup show` - Show configuration
- `pycomptox-setup test` - Test API connection
- `pycomptox-setup delete` - Delete saved key

Can also use: `python -m pycomptox [command]`

### ✅ New: py.typed

Added PEP 561 marker file for type checking support:
- Enables type checkers (mypy) to use package types
- Provides better IDE autocomplete
- Full type annotation support

### ✅ New: MANIFEST.in

Controls distribution contents:
- Includes: README, LICENSE, docs, type markers, tests
- Excludes: cache files, build artifacts, notebooks

## Optional Dependencies

### Development Tools

```bash
pip install -e ".[dev]"
```

Includes:
- pytest, pytest-cov (testing)
- black (formatting)
- flake8 (linting)
- mypy (type checking)
- types-requests (type stubs)

### Notebook Support

```bash
pip install -e ".[notebook]"
```

Includes:
- jupyter (notebooks)
- pandas (data analysis)
- matplotlib (visualization)

### All Optional Dependencies

```bash
pip install -e ".[all]"
```

Includes everything (dev + notebook).

## Tool Configurations

### Black (Code Formatting)

```toml
[tool.black]
line-length = 100
target-version = ["py38", "py39", "py310", "py311", "py312"]
```

Usage:
```bash
black src/ tests/
```

### MyPy (Type Checking)

```toml
[tool.mypy]
python_version = "3.8"
check_untyped_defs = true
ignore_missing_imports = true
```

Usage:
```bash
mypy src/pycomptox
```

### Pytest (Testing)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

Usage:
```bash
pytest tests/
pytest tests/ -v  # verbose
pytest tests/ -k "test_properties"  # specific tests
```

### Coverage (Test Coverage)

```toml
[tool.coverage.run]
source = ["pycomptox"]
branch = true
```

Usage:
```bash
pytest --cov=pycomptox tests/
pytest --cov=pycomptox --cov-report=html tests/
```

### Isort (Import Sorting)

```toml
[tool.isort]
profile = "black"
line_length = 100
```

Usage:
```bash
isort src/ tests/
```

## Installation Methods

### Standard Install

```bash
pip install .
```

Installs only core dependencies (requests).

### Editable Install (Development)

```bash
pip install -e .
```

Installs in editable mode - changes to source code are immediately available without reinstalling.

### With Optional Dependencies

```bash
# Development tools
pip install -e ".[dev]"

# Notebook support
pip install -e ".[notebook]"

# Everything
pip install -e ".[all]"
```

## Building Distribution

### Install Build Tools

```bash
pip install build
```

### Build Packages

```bash
python -m build
```

Creates:
- `dist/pycomptox-0.3.0-py3-none-any.whl` (wheel - recommended)
- `dist/pycomptox-0.3.0.tar.gz` (source distribution)

### Install from Wheel

```bash
pip install dist/pycomptox-0.3.0-py3-none-any.whl
```

## Entry Point Scripts

After installation, these commands are available:

```bash
# Using the pycomptox-setup command
pycomptox-setup show
pycomptox-setup set YOUR_API_KEY
pycomptox-setup test
pycomptox-setup delete

# Using Python module syntax
python -m pycomptox show
python -m pycomptox set YOUR_API_KEY
python -m pycomptox test
python -m pycomptox delete
```

## Benefits of Modern Setup

### 1. Standards Compliance

- **PEP 621**: Modern declarative metadata
- **PEP 517/518**: Modern build system
- **PEP 561**: Type checking support

### 2. Better Tooling Support

- Works with all modern Python packaging tools
- Better IDE integration
- Improved type checking

### 3. Cleaner Configuration

- Single source of truth (`pyproject.toml`)
- No more scattered configuration files
- Tool configs in one place

### 4. Optional Dependencies

- Install only what you need
- Smaller default installation
- Easy to add dev tools

### 5. Entry Points

- Clean CLI interface
- Automatic script creation
- Cross-platform compatibility

## Migration from Old Setup

If you previously installed with old setup.py:

```bash
# Uninstall old version
pip uninstall pycomptox

# Install new version
pip install -e ".[dev]"
```

## Verification

Test the installation:

```python
# Check version
import pycomptox
print(pycomptox.__version__)  # 0.3.0

# Check CLI
import subprocess
result = subprocess.run(["pycomptox-setup", "show"], capture_output=True)
print(result.stdout.decode())
```

## Development Workflow

```bash
# 1. Clone and enter directory
git clone https://github.com/USEtox/PyCompTox.git
cd PyCompTox

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install in editable mode with dev tools
pip install -e ".[dev]"

# 4. Format code
black src/ tests/

# 5. Sort imports
isort src/ tests/

# 6. Type check
mypy src/pycomptox

# 7. Run tests
pytest tests/

# 8. Check coverage
pytest --cov=pycomptox tests/

# 9. Build distribution
python -m build
```

## Troubleshooting

### "No module named 'pycomptox'"

Solution: Install the package
```bash
pip install -e .
```

### "pycomptox-setup: command not found"

Solution: Reinstall with entry points
```bash
pip install -e . --force-reinstall
```

Or use Python module syntax:
```bash
python -m pycomptox show
```

### Build errors

Solution: Update build tools
```bash
pip install --upgrade pip setuptools wheel build
```

### Type checking not working

Solution: Install type stubs
```bash
pip install -e ".[dev]"
```

## Summary

PyCompTox now uses modern Python packaging with:

✅ `pyproject.toml` - Single configuration file
✅ Optional dependencies - Install only what you need
✅ Type checking support - Full PEP 561 compliance
✅ CLI entry points - `pycomptox-setup` command
✅ Tool configurations - black, mypy, pytest, coverage
✅ Modern build system - PEP 517/518 compliant
✅ Better tooling support - Works with all modern tools

The package is now following current Python packaging best practices!
