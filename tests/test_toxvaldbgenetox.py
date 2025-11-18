"""
Tests for ToxValDBGenetox hazard module.
"""

import pytest
from pycomptox.hazard import ToxValDBGenetox


@pytest.fixture
def genetox_client():
    """Create a ToxValDBGenetox client for testing."""
    return ToxValDBGenetox()


def test_initialization():
    """Test that ToxValDBGenetox client initializes correctly."""
    client = ToxValDBGenetox()
    assert client is not None
    assert isinstance(client, ToxValDBGenetox)


def test_get_summary_by_dtxsid_benzene(genetox_client):
    """Test retrieving genotoxicity summary for benzene (DTXSID0021125)."""
    result = genetox_client.get_summary_by_dtxsid("DTXSID0021125")
    assert result is not None
    assert isinstance(result, list)
    
    if result:
        # Verify structure of returned data
        assert all(isinstance(record, dict) for record in result)
        assert all('dtxsid' in record for record in result)


def test_get_summary_by_dtxsid_bisphenol_a(genetox_client):
    """Test retrieving genotoxicity summary for bisphenol A (DTXSID7020182)."""
    result = genetox_client.get_summary_by_dtxsid("DTXSID7020182")
    assert result is not None
    assert isinstance(result, list)


def test_get_summary_by_dtxsid_invalid_input(genetox_client):
    """Test that invalid inputs raise ValueError."""
    with pytest.raises(ValueError):
        genetox_client.get_summary_by_dtxsid("")
    
    with pytest.raises(ValueError):
        genetox_client.get_summary_by_dtxsid(None)
    
    with pytest.raises(ValueError):
        genetox_client.get_summary_by_dtxsid(123)


def test_get_detail_by_dtxsid_bisphenol_a(genetox_client):
    """Test retrieving detailed genotoxicity data for bisphenol A."""
    result = genetox_client.get_detail_by_dtxsid("DTXSID7020182")
    assert result is not None
    assert isinstance(result, list)
    
    if result:
        # Verify structure of returned data
        assert all(isinstance(record, dict) for record in result)
        assert all('dtxsid' in record for record in result)


def test_get_detail_by_dtxsid_with_projection(genetox_client):
    """Test retrieving detailed data with ccd projection."""
    result = genetox_client.get_detail_by_dtxsid(
        "DTXSID7020182", 
        projection="ccd-genetox-details"
    )
    assert result is not None
    assert isinstance(result, list)


def test_get_detail_by_dtxsid_invalid_input(genetox_client):
    """Test that invalid inputs raise ValueError."""
    with pytest.raises(ValueError):
        genetox_client.get_detail_by_dtxsid("")
    
    with pytest.raises(ValueError):
        genetox_client.get_detail_by_dtxsid(None)


def test_get_summary_by_dtxsid_batch(genetox_client):
    """Test batch retrieval of genotoxicity summary data."""
    dtxsids = ["DTXSID0021125", "DTXSID7020182", "DTXSID0020032"]
    result = genetox_client.get_summary_by_dtxsid_batch(dtxsids)
    
    assert result is not None
    assert isinstance(result, list)


def test_get_summary_by_dtxsid_batch_empty_list(genetox_client):
    """Test that empty list raises ValueError."""
    with pytest.raises(ValueError):
        genetox_client.get_summary_by_dtxsid_batch([])


def test_get_summary_by_dtxsid_batch_too_many(genetox_client):
    """Test that requesting more than 200 DTXSIDs raises ValueError."""
    dtxsids = [f"DTXSID{i:07d}" for i in range(201)]
    
    with pytest.raises(ValueError):
        genetox_client.get_summary_by_dtxsid_batch(dtxsids)


def test_get_detail_by_dtxsid_batch(genetox_client):
    """Test batch retrieval of detailed genotoxicity data."""
    dtxsids = ["DTXSID0021125", "DTXSID7020182"]
    
    # Note: This endpoint sometimes returns 500 errors from the API server
    # Test validates that our code handles the request correctly
    try:
        result = genetox_client.get_detail_by_dtxsid_batch(dtxsids)
        assert result is not None
        assert isinstance(result, list)
    except Exception as e:
        # If API returns 500 error, that's an API issue, not our code
        if "500 Server Error" in str(e):
            pytest.skip("API server returned 500 error - this is an API issue")
        else:
            raise


def test_get_detail_by_dtxsid_batch_with_projection(genetox_client):
    """Test batch retrieval with projection."""
    dtxsids = ["DTXSID0021125", "DTXSID7020182"]
    
    # Note: This endpoint sometimes returns 500 errors from the API server
    try:
        result = genetox_client.get_detail_by_dtxsid_batch(
            dtxsids, 
            projection="ccd-genetox-details"
        )
        assert result is not None
        assert isinstance(result, list)
    except Exception as e:
        # If API returns 500 error, that's an API issue, not our code
        if "500 Server Error" in str(e):
            pytest.skip("API server returned 500 error - this is an API issue")
        else:
            raise


def test_get_detail_by_dtxsid_batch_empty_list(genetox_client):
    """Test that empty list raises ValueError."""
    with pytest.raises(ValueError):
        genetox_client.get_detail_by_dtxsid_batch([])


def test_get_detail_by_dtxsid_batch_too_many(genetox_client):
    """Test that requesting more than 200 DTXSIDs raises ValueError."""
    dtxsids = [f"DTXSID{i:07d}" for i in range(201)]
    
    with pytest.raises(ValueError):
        genetox_client.get_detail_by_dtxsid_batch(dtxsids)


def test_caching_enabled(genetox_client):
    """Test that caching works correctly."""
    # First call
    result1 = genetox_client.get_summary_by_dtxsid("DTXSID0021125", use_cache=True)
    
    # Second call should use cache
    result2 = genetox_client.get_summary_by_dtxsid("DTXSID0021125", use_cache=True)
    
    # Results should be identical
    assert result1 == result2
