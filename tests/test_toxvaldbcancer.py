"""
Tests for ToxValDB Cancer Summary module.

This test suite covers the ToxValDBCancer class functionality including:
- Client initialization
- Single DTXSID retrieval
- Batch DTXSID retrieval
- Input validation
- Error handling
- Caching functionality
"""

import pytest
from pycomptox.hazard import ToxValDBCancer


@pytest.fixture
def cancer_client():
    """Fixture to provide a ToxValDBCancer client instance."""
    return ToxValDBCancer()


def test_client_initialization(cancer_client):
    """Test that the client initializes correctly."""
    assert cancer_client is not None
    assert hasattr(cancer_client, 'get_data_by_dtxsid')
    assert hasattr(cancer_client, 'get_data_by_dtxsid_batch')


def test_get_data_by_dtxsid_benzene(cancer_client):
    """Test retrieving cancer data for benzene (DTXSID0021125)."""
    dtxsid = "DTXSID0021125"
    data = cancer_client.get_data_by_dtxsid(dtxsid)
    
    assert data is not None
    assert isinstance(data, list)
    
    # Benzene is a known carcinogen, should have cancer data
    if len(data) > 0:
        # Check that records have expected structure
        record = data[0]
        assert isinstance(record, dict)
        assert 'dtxsid' in record
        # May have fields like: source, classification, woe, cancerType, etc.


def test_get_data_by_dtxsid_batch(cancer_client):
    """Test retrieving cancer data for multiple chemicals."""
    # Benzene, Formaldehyde, Arsenic - known carcinogens
    dtxsids = ["DTXSID0021125", "DTXSID7020182", "DTXSID0020032"]
    data = cancer_client.get_data_by_dtxsid_batch(dtxsids)
    
    assert data is not None
    assert isinstance(data, list)
    
    # Should have data for at least some of these chemicals
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)
        assert 'dtxsid' in record


def test_get_data_by_dtxsid_empty_string(cancer_client):
    """Test that empty string raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        cancer_client.get_data_by_dtxsid("")


def test_get_data_by_dtxsid_none(cancer_client):
    """Test that None raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        cancer_client.get_data_by_dtxsid(None)


def test_get_data_by_dtxsid_wrong_type(cancer_client):
    """Test that non-string input raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        cancer_client.get_data_by_dtxsid(12345)


def test_get_data_by_dtxsid_batch_empty_list(cancer_client):
    """Test that empty list raises ValueError."""
    with pytest.raises(ValueError, match="dtxsids list cannot be empty"):
        cancer_client.get_data_by_dtxsid_batch([])


def test_get_data_by_dtxsid_batch_too_many(cancer_client):
    """Test that more than 200 DTXSIDs raises ValueError."""
    dtxsids = [f"DTXSID{i:07d}" for i in range(201)]
    with pytest.raises(ValueError, match="Maximum 200 DTXSIDs allowed"):
        cancer_client.get_data_by_dtxsid_batch(dtxsids)


def test_caching_single(cancer_client):
    """Test that caching works for single DTXSID requests."""
    dtxsid = "DTXSID0021125"
    
    # First call - should fetch from API
    data1 = cancer_client.get_data_by_dtxsid(dtxsid, use_cache=True)
    
    # Second call - should use cache
    data2 = cancer_client.get_data_by_dtxsid(dtxsid, use_cache=True)
    
    # Results should be identical
    assert data1 == data2


def test_caching_batch(cancer_client):
    """Test that caching works for batch requests."""
    dtxsids = ["DTXSID0021125", "DTXSID7020182"]
    
    # First call - should fetch from API
    data1 = cancer_client.get_data_by_dtxsid_batch(dtxsids, use_cache=True)
    
    # Second call - should use cache
    data2 = cancer_client.get_data_by_dtxsid_batch(dtxsids, use_cache=True)
    
    # Results should be identical
    assert data1 == data2


def test_no_caching(cancer_client):
    """Test that caching can be disabled."""
    dtxsid = "DTXSID0021125"
    
    # Calls with use_cache=False should work
    data = cancer_client.get_data_by_dtxsid(dtxsid, use_cache=False)
    
    assert data is not None
    assert isinstance(data, list)
