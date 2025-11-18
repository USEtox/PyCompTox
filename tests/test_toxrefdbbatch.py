"""
Tests for ToxRefDB Batch module.

This test suite covers the ToxRefDBBatch class functionality including:
- Client initialization
- Batch DTXSID retrieval
- Input validation
- Error handling
- Caching functionality
"""

import pytest
from pycomptox.hazard import ToxRefDBBatch


@pytest.fixture
def toxref_batch_client():
    """Fixture to provide a ToxRefDBBatch client instance."""
    return ToxRefDBBatch()


def test_client_initialization(toxref_batch_client):
    """Test that the client initializes correctly."""
    assert toxref_batch_client is not None
    assert hasattr(toxref_batch_client, 'get_data_by_dtxsid_batch')


def test_get_data_by_dtxsid_batch_single(toxref_batch_client):
    """Test retrieving ToxRefDB data for a single chemical."""
    dtxsids = ["DTXSID1037806"]
    data = toxref_batch_client.get_data_by_dtxsid_batch(dtxsids)
    
    assert data is not None
    assert isinstance(data, list)
    
    # This chemical should have ToxRefDB data
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)
        assert 'dtxsid' in record


def test_get_data_by_dtxsid_batch_multiple(toxref_batch_client):
    """Test retrieving ToxRefDB data for multiple chemicals."""
    dtxsids = ["DTXSID1037806", "DTXSID0021125", "DTXSID7020182"]
    data = toxref_batch_client.get_data_by_dtxsid_batch(dtxsids)
    
    assert data is not None
    assert isinstance(data, list)
    
    # Should have data for at least some chemicals
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)
        assert 'dtxsid' in record


def test_get_data_by_dtxsid_batch_empty_list(toxref_batch_client):
    """Test that empty list raises ValueError."""
    with pytest.raises(ValueError, match="dtxsids list cannot be empty"):
        toxref_batch_client.get_data_by_dtxsid_batch([])


def test_get_data_by_dtxsid_batch_too_many(toxref_batch_client):
    """Test that more than 200 DTXSIDs raises ValueError."""
    dtxsids = [f"DTXSID{i:07d}" for i in range(201)]
    with pytest.raises(ValueError, match="Maximum 200 DTXSIDs allowed"):
        toxref_batch_client.get_data_by_dtxsid_batch(dtxsids)


def test_caching(toxref_batch_client):
    """Test that caching works for batch requests."""
    dtxsids = ["DTXSID1037806", "DTXSID0021125"]
    
    # First call - should fetch from API
    data1 = toxref_batch_client.get_data_by_dtxsid_batch(dtxsids, use_cache=True)
    
    # Second call - should use cache
    data2 = toxref_batch_client.get_data_by_dtxsid_batch(dtxsids, use_cache=True)
    
    # Results should be identical
    assert data1 == data2


def test_no_caching(toxref_batch_client):
    """Test that caching can be disabled."""
    dtxsids = ["DTXSID1037806"]
    
    # Calls with use_cache=False should work
    data = toxref_batch_client.get_data_by_dtxsid_batch(dtxsids, use_cache=False)
    
    assert data is not None
    assert isinstance(data, list)
