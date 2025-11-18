"""
Tests for IRIS (Integrated Risk Information System) module.

This test suite covers the IRIS class functionality including:
- Client initialization
- DTXSID retrieval
- Input validation
- Error handling
- Caching functionality
"""

import pytest
from pycomptox.hazard import IRIS


@pytest.fixture
def iris_client():
    """Fixture to provide an IRIS client instance."""
    return IRIS()


def test_client_initialization(iris_client):
    """Test that the client initializes correctly."""
    assert iris_client is not None
    assert hasattr(iris_client, 'get_data_by_dtxsid')


def test_get_data_by_dtxsid_formaldehyde(iris_client):
    """Test retrieving IRIS data for formaldehyde (DTXSID7020182)."""
    dtxsid = "DTXSID7020182"
    data = iris_client.get_data_by_dtxsid(dtxsid)
    
    assert data is not None
    assert isinstance(data, list)
    
    # Formaldehyde has an IRIS assessment
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)
        # Should have IRIS assessment information


def test_get_data_by_dtxsid_benzene(iris_client):
    """Test retrieving IRIS data for benzene (DTXSID0021125)."""
    dtxsid = "DTXSID0021125"
    data = iris_client.get_data_by_dtxsid(dtxsid)
    
    assert data is not None
    assert isinstance(data, list)
    
    # Benzene may have IRIS assessment
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)


def test_get_data_by_dtxsid_empty_string(iris_client):
    """Test that empty string raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        iris_client.get_data_by_dtxsid("")


def test_get_data_by_dtxsid_none(iris_client):
    """Test that None raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        iris_client.get_data_by_dtxsid(None)


def test_get_data_by_dtxsid_wrong_type(iris_client):
    """Test that non-string input raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        iris_client.get_data_by_dtxsid(12345)


def test_caching(iris_client):
    """Test that caching works for IRIS requests."""
    dtxsid = "DTXSID7020182"
    
    # First call - should fetch from API
    data1 = iris_client.get_data_by_dtxsid(dtxsid, use_cache=True)
    
    # Second call - should use cache
    data2 = iris_client.get_data_by_dtxsid(dtxsid, use_cache=True)
    
    # Results should be identical
    assert data1 == data2


def test_no_caching(iris_client):
    """Test that caching can be disabled."""
    dtxsid = "DTXSID7020182"
    
    # Calls with use_cache=False should work
    data = iris_client.get_data_by_dtxsid(dtxsid, use_cache=False)
    
    assert data is not None
    assert isinstance(data, list)
