# Installation Guide

## Modern Setup (Recommended)

PyCompTox now uses modern Python packaging standards (PEP 621) with `pyproject.toml`.

### Quick Install

```bash
# Install from source
pip install .

# Install with development dependencies
pip install -e ".[dev]"

# Install with notebook support
pip install -e ".[notebook]"

# Install everything
pip install -e ".[all]"
```

### Install Options

**Standard Installation:**
```bash
pip install .
```
Installs only the core dependencies (requests).

**Development Installation:**
```bash
pip install -e ".[dev]"
```
Includes:
- pytest, pytest-cov (testing)
- black (code formatting)
- flake8 (linting)
- mypy (type checking)
- types-requests (type stubs)

**Notebook Support:**
```bash
pip install -e ".[notebook]"
```
Includes:
- jupyter (notebooks)
- pandas (data analysis)
- matplotlib (visualization)

**Everything:**
```bash
pip install -e ".[all]"
```
Includes all optional dependencies.

### Editable Install

For development, use editable mode (-e flag):

```bash
# Editable install with dev dependencies
pip install -e ".[dev]"
```

This allows you to make changes to the code without reinstalling.

## Build Distribution

To build distribution packages:

```bash
# Install build tools
pip install build

# Build wheel and source distribution
python -m build
```

This creates:
- `dist/pycomptox-0.3.0-py3-none-any.whl` (wheel)
- `dist/pycomptox-0.3.0.tar.gz` (source)

## Configuration Files

### pyproject.toml

All project metadata and build configuration is in `pyproject.toml`:
- Package metadata (name, version, description)
- Dependencies
- Optional dependencies (dev, notebook, all)
- Tool configurations (black, mypy, pytest, coverage)

### setup.py

The `setup.py` file is now a minimal shim for backward compatibility with older tools. All configuration is in `pyproject.toml`.

### MANIFEST.in

Controls which files are included in source distributions:
- Documentation (README, LICENSE, docs/)
- Type information (py.typed)
- Tests (optional)

## Type Checking Support

PyCompTox is fully typed and includes a `py.typed` marker file (PEP 561), enabling:

```bash
# Type check your code that uses PyCompTox
mypy your_script.py
```

## Command-Line Interface

After installation, you can use the CLI:

```bash
# Save API key
pycomptox-setup set YOUR_API_KEY

# Show configuration
pycomptox-setup show

# Test API connection
pycomptox-setup test

# Delete API key
pycomptox-setup delete
```

Or use Python module syntax:

```bash
python -m pycomptox set YOUR_API_KEY
```

## Virtual Environment (Recommended)

Always use a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Unix/macOS)
source venv/bin/activate

# Install PyCompTox
pip install -e ".[dev]"
```

## Verify Installation

```python
import pycomptox
print(pycomptox.__version__)  # Should print: 0.3.0

# Check available classes
from pycomptox.chemical import Chemical, ChemicalDetails, ChemicalProperties
```

## Development Workflow

1. **Clone repository:**
   ```bash
   git clone https://github.com/USEtox/PyCompTox.git
   cd PyCompTox
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install in editable mode with dev dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Run tests:**
   ```bash
   pytest tests/
   ```

5. **Format code:**
   ```bash
   black src/ tests/
   ```

6. **Type check:**
   ```bash
   mypy src/pycomptox
   ```

7. **Lint:**
   ```bash
   flake8 src/ tests/
   ```

## Troubleshooting

### "No module named 'pycomptox'"

Make sure you installed the package:
```bash
pip install -e .
```

### Import errors after changes

If you installed in editable mode, Python should pick up changes automatically. If not:
```bash
pip install -e . --force-reinstall --no-deps
```

### Type checking issues

Install type stubs:
```bash
pip install types-requests
```

### Build errors

Make sure you have the latest build tools:
```bash
pip install --upgrade pip setuptools wheel build
```

## Requirements

- Python 3.8 or higher
- pip (usually comes with Python)
- Internet connection (for API access)

## Platform Support

PyCompTox is pure Python and works on:
- ✓ Windows
- ✓ macOS
- ✓ Linux
- ✓ Any platform with Python 3.8+

## Getting Help

- GitHub Issues: https://github.com/USEtox/PyCompTox/issues
- Documentation: https://github.com/USEtox/PyCompTox/blob/main/README.md
