"""
Tests for ToxValDB (Toxicity Values Database) module.

This test suite covers the ToxValDB class functionality including:
- Client initialization
- Single DTXSID retrieval
- Batch DTXSID retrieval
- Input validation
- Error handling
- Caching functionality
"""

import pytest
from pycomptox.hazard import ToxValDB


@pytest.fixture
def toxval_client():
    """Fixture to provide a ToxValDB client instance."""
    return ToxValDB()


def test_client_initialization(toxval_client):
    """Test that the client initializes correctly."""
    assert toxval_client is not None
    assert hasattr(toxval_client, 'get_data_by_dtxsid')
    assert hasattr(toxval_client, 'get_data_by_dtxsid_batch')


def test_get_data_by_dtxsid_benzene(toxval_client):
    """Test retrieving ToxValDB data for benzene (DTXSID0021125)."""
    dtxsid = "DTXSID0021125"
    data = toxval_client.get_data_by_dtxsid(dtxsid)
    
    assert data is not None
    assert isinstance(data, list)
    
    # Benzene should have toxicity values
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)
        assert 'dtxsid' in record
        # Should have toxicity value information
        # May include: toxvalType, toxvalNumeric, toxvalUnits, etc.


def test_get_data_by_dtxsid_batch(toxval_client):
    """Test retrieving ToxValDB data for multiple chemicals."""
    # Benzene, Formaldehyde, Arsenic - well-studied chemicals
    dtxsids = ["DTXSID0021125", "DTXSID7020182", "DTXSID0020032"]
    data = toxval_client.get_data_by_dtxsid_batch(dtxsids)
    
    assert data is not None
    assert isinstance(data, list)
    
    # Should have data for at least some of these chemicals
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)
        assert 'dtxsid' in record


def test_get_data_by_dtxsid_empty_string(toxval_client):
    """Test that empty string raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        toxval_client.get_data_by_dtxsid("")


def test_get_data_by_dtxsid_none(toxval_client):
    """Test that None raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        toxval_client.get_data_by_dtxsid(None)


def test_get_data_by_dtxsid_wrong_type(toxval_client):
    """Test that non-string input raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        toxval_client.get_data_by_dtxsid(12345)


def test_get_data_by_dtxsid_batch_empty_list(toxval_client):
    """Test that empty list raises ValueError."""
    with pytest.raises(ValueError, match="dtxsids list cannot be empty"):
        toxval_client.get_data_by_dtxsid_batch([])


def test_get_data_by_dtxsid_batch_too_many(toxval_client):
    """Test that more than 200 DTXSIDs raises ValueError."""
    dtxsids = [f"DTXSID{i:07d}" for i in range(201)]
    with pytest.raises(ValueError, match="Maximum 200 DTXSIDs allowed"):
        toxval_client.get_data_by_dtxsid_batch(dtxsids)


def test_caching_single(toxval_client):
    """Test that caching works for single DTXSID requests."""
    dtxsid = "DTXSID0021125"
    
    # First call - should fetch from API
    data1 = toxval_client.get_data_by_dtxsid(dtxsid, use_cache=True)
    
    # Second call - should use cache
    data2 = toxval_client.get_data_by_dtxsid(dtxsid, use_cache=True)
    
    # Results should be identical
    assert data1 == data2


def test_caching_batch(toxval_client):
    """Test that caching works for batch requests."""
    dtxsids = ["DTXSID0021125", "DTXSID7020182"]
    
    # First call - should fetch from API
    data1 = toxval_client.get_data_by_dtxsid_batch(dtxsids, use_cache=True)
    
    # Second call - should use cache
    data2 = toxval_client.get_data_by_dtxsid_batch(dtxsids, use_cache=True)
    
    # Results should be identical
    assert data1 == data2


def test_no_caching(toxval_client):
    """Test that caching can be disabled."""
    dtxsid = "DTXSID0021125"
    
    # Calls with use_cache=False should work
    data = toxval_client.get_data_by_dtxsid(dtxsid, use_cache=False)
    
    assert data is not None
    assert isinstance(data, list)
