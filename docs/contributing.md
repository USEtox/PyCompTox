# Contributing to PyCompTox

Thank you for your interest in contributing to PyCompTox! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bugfix
4. Make your changes
5. Run tests to ensure everything works
6. Submit a pull request

## Development Setup

### Clone and Install

```bash
git clone https://github.com/YOUR_USERNAME/PyCompTox.git
cd PyCompTox

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev,docs]"
```

### Set Up API Key

```bash
pycomptox-setup set YOUR_API_KEY
```

## Code Style

We follow PEP 8 and use several tools to maintain code quality:

### Black (Code Formatting)

```bash
black src/ tests/
```

### Flake8 (Linting)

```bash
flake8 src/ tests/
```

### MyPy (Type Checking)

```bash
mypy src/
```

## Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_search.py
```

### Run with Coverage

```bash
pytest --cov=pycomptox --cov-report=html
```

### Run Specific Test

```bash
pytest tests/test_search.py::TestChemicalSearch::test_search_by_name
```

## Writing Tests

Tests are located in the `tests/` directory. Each module has a corresponding test file:

- `src/pycomptox/search.py` → `tests/test_search.py`
- `src/pycomptox/details.py` → `tests/test_details.py`
- etc.

### Test Structure

```python
import pytest
from pycomptox.chemical import Chemical

@pytest.fixture
def chem_client():
    """Create a Chemical client for testing."""
    return Chemical()

class TestChemicalSearch:
    """Test suite for Chemical search functionality."""
    
    def test_search_by_name(self, chem_client):
        """Test name-based chemical search."""
        results = chem_client.search_by_name("caffeine")
        assert len(results) > 0
        assert 'dtxsid' in results[0]
```

## Documentation

### Build Documentation

```bash
# Install docs dependencies
pip install -e ".[docs]"

# Serve documentation locally
mkdocs serve

# Build static site
mkdocs build
```

### Documentation Structure

- `docs/index.md` - Main documentation page
- `docs/api/` - API reference documentation
- `docs/*.md` - User guides and tutorials

### Docstring Style

We use Google-style docstrings:

```python
def search_by_name(self, name: str) -> List[Dict[str, Any]]:
    """
    Search for chemicals by name.
    
    Args:
        name: Chemical name to search for
        
    Returns:
        List of dictionaries containing chemical data
        
    Raises:
        ValueError: If name is empty
        RuntimeError: If API request fails
        
    Example:
        >>> chem = Chemical()
        >>> results = chem.search_by_name("caffeine")
        >>> print(results[0]['dtxsid'])
        DTXSID2021315
    """
    pass
```

## Pull Request Process

1. **Create a Branch**: Use descriptive names like `feature/add-xyz` or `fix/issue-123`
2. **Write Tests**: Add tests for new features or bugfixes
3. **Update Documentation**: Update docs if adding new features
4. **Run Tests**: Ensure all tests pass
5. **Format Code**: Run `black` and `flake8`
6. **Commit Changes**: Use clear, descriptive commit messages
7. **Submit PR**: Provide a clear description of your changes

### Commit Message Format

```
Short summary (50 chars or less)

More detailed explanation if needed. Wrap at 72 characters.

- Bullet points are okay
- Reference issues: Fixes #123
```

## Feature Requests

Open an issue on GitHub with:

- Clear description of the feature
- Use case and motivation
- Example usage (if applicable)

## Bug Reports

Open an issue on GitHub with:

- PyCompTox version
- Python version
- Operating system
- Complete error traceback
- Minimal code to reproduce the issue

### Bug Report Template

```markdown
**Environment:**
- PyCompTox version: 0.4.0
- Python version: 3.12
- OS: Windows 10

**Description:**
Brief description of the bug

**Code to Reproduce:**
```python
from pycomptox.chemical import Chemical
chem = Chemical()
# ... code that triggers the bug
```

**Error:**
```
Full error traceback here
```

**Expected Behavior:**
What you expected to happen
```

## Code Review

All submissions require review. We'll provide feedback on:

- Code quality and style
- Test coverage
- Documentation
- Design decisions

## Release Process

1. Update version in `pyproject.toml` and `src/pycomptox/__init__.py`
2. Update `CHANGELOG.md`
3. Create a git tag
4. Build and publish to PyPI

## Questions?

Open an issue or start a discussion on GitHub.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
