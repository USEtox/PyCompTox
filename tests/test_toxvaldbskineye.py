"""
Tests for ToxValDB Skin and Eye Irritation module.

This test suite covers the ToxValDBSkinEye class functionality including:
- Client initialization
- Single DTXSID retrieval
- Batch DTXSID retrieval
- Input validation
- Error handling
- Caching functionality
"""

import pytest
from pycomptox.hazard import ToxValDBSkinEye


@pytest.fixture
def skineye_client():
    """Fixture to provide a ToxValDBSkinEye client instance."""
    return ToxValDBSkinEye()


def test_client_initialization(skineye_client):
    """Test that the client initializes correctly."""
    assert skineye_client is not None
    assert hasattr(skineye_client, 'get_data_by_dtxsid')
    assert hasattr(skineye_client, 'get_data_by_dtxsid_batch')


def test_get_data_by_dtxsid_benzene(skineye_client):
    """Test retrieving skin/eye irritation data for benzene."""
    dtxsid = "DTXSID0021125"
    data = skineye_client.get_data_by_dtxsid(dtxsid)
    
    assert data is not None
    assert isinstance(data, list)
    
    # Check structure if data exists
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)
        assert 'dtxsid' in record


def test_get_data_by_dtxsid_batch(skineye_client):
    """Test retrieving skin/eye data for multiple chemicals."""
    dtxsids = ["DTXSID0021125", "DTXSID7020182", "DTXSID0020032"]
    data = skineye_client.get_data_by_dtxsid_batch(dtxsids)
    
    assert data is not None
    assert isinstance(data, list)
    
    # Check structure if data exists
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)
        assert 'dtxsid' in record


def test_get_data_by_dtxsid_empty_string(skineye_client):
    """Test that empty string raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        skineye_client.get_data_by_dtxsid("")


def test_get_data_by_dtxsid_none(skineye_client):
    """Test that None raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        skineye_client.get_data_by_dtxsid(None)


def test_get_data_by_dtxsid_wrong_type(skineye_client):
    """Test that non-string input raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        skineye_client.get_data_by_dtxsid(12345)


def test_get_data_by_dtxsid_batch_empty_list(skineye_client):
    """Test that empty list raises ValueError."""
    with pytest.raises(ValueError, match="dtxsids list cannot be empty"):
        skineye_client.get_data_by_dtxsid_batch([])


def test_get_data_by_dtxsid_batch_too_many(skineye_client):
    """Test that more than 200 DTXSIDs raises ValueError."""
    dtxsids = [f"DTXSID{i:07d}" for i in range(201)]
    with pytest.raises(ValueError, match="Maximum 200 DTXSIDs allowed"):
        skineye_client.get_data_by_dtxsid_batch(dtxsids)


def test_caching_single(skineye_client):
    """Test that caching works for single DTXSID requests."""
    dtxsid = "DTXSID0021125"
    
    # First call - should fetch from API
    data1 = skineye_client.get_data_by_dtxsid(dtxsid, use_cache=True)
    
    # Second call - should use cache
    data2 = skineye_client.get_data_by_dtxsid(dtxsid, use_cache=True)
    
    # Results should be identical
    assert data1 == data2


def test_caching_batch(skineye_client):
    """Test that caching works for batch requests."""
    dtxsids = ["DTXSID0021125", "DTXSID7020182"]
    
    # First call - should fetch from API
    data1 = skineye_client.get_data_by_dtxsid_batch(dtxsids, use_cache=True)
    
    # Second call - should use cache
    data2 = skineye_client.get_data_by_dtxsid_batch(dtxsids, use_cache=True)
    
    # Results should be identical
    assert data1 == data2


def test_no_caching(skineye_client):
    """Test that caching can be disabled."""
    dtxsid = "DTXSID0021125"
    
    # Calls with use_cache=False should work
    data = skineye_client.get_data_by_dtxsid(dtxsid, use_cache=False)
    
    assert data is not None
    assert isinstance(data, list)
