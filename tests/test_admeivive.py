"""
Tests for ADMEIVIVE hazard module.
"""

import pytest
from pycomptox.hazard import ADMEIVIVE


@pytest.fixture
def adme_client():
    """Create an ADMEIVIVE client for testing."""
    return ADMEIVIVE()


def test_initialization():
    """Test that ADMEIVIVE client initializes correctly."""
    client = ADMEIVIVE()
    assert client is not None
    assert isinstance(client, ADMEIVIVE)


def test_get_all_data_by_dtxsid_bisphenol_a(adme_client):
    """Test retrieving ADME-IVIVE data for bisphenol A."""
    result = adme_client.get_all_data_by_dtxsid_ccd_projection("DTXSID7020182")
    
    assert result is not None
    assert isinstance(result, list)
    
    if result:
        # Verify structure
        assert all(isinstance(record, dict) for record in result)
        # Check for DTXSID field
        dtxsids = [r.get('dtxsid') for r in result if 'dtxsid' in r]
        if dtxsids:
            assert all(d == "DTXSID7020182" for d in dtxsids)


def test_get_all_data_with_projection(adme_client):
    """Test retrieving data with ccd-adme-data projection."""
    result = adme_client.get_all_data_by_dtxsid_ccd_projection(
        "DTXSID7020182",
        projection="ccd-adme-data"
    )
    
    assert result is not None
    assert isinstance(result, list)


def test_get_all_data_without_projection(adme_client):
    """Test retrieving data without projection (default)."""
    result = adme_client.get_all_data_by_dtxsid_ccd_projection("DTXSID7020182")
    
    assert result is not None
    assert isinstance(result, list)


def test_get_all_data_invalid_input(adme_client):
    """Test that invalid inputs raise ValueError."""
    with pytest.raises(ValueError):
        adme_client.get_all_data_by_dtxsid_ccd_projection("")
    
    with pytest.raises(ValueError):
        adme_client.get_all_data_by_dtxsid_ccd_projection(None)
    
    with pytest.raises(ValueError):
        adme_client.get_all_data_by_dtxsid_ccd_projection(123)


def test_different_chemicals(adme_client):
    """Test retrieving data for different chemicals."""
    dtxsids = ["DTXSID7020182", "DTXSID0021125", "DTXSID0020032"]
    
    for dtxsid in dtxsids:
        result = adme_client.get_all_data_by_dtxsid_ccd_projection(dtxsid)
        assert result is not None
        assert isinstance(result, list)


def test_caching_enabled(adme_client):
    """Test that caching works correctly."""
    # First call
    result1 = adme_client.get_all_data_by_dtxsid_ccd_projection(
        "DTXSID7020182", 
        use_cache=True
    )
    
    # Second call should use cache
    result2 = adme_client.get_all_data_by_dtxsid_ccd_projection(
        "DTXSID7020182", 
        use_cache=True
    )
    
    # Results should be identical
    assert result1 == result2


def test_data_structure(adme_client):
    """Test that returned data has expected structure."""
    result = adme_client.get_all_data_by_dtxsid_ccd_projection("DTXSID7020182")
    
    if result:
        # Each record should be a dictionary
        for record in result[:5]:  # Check first 5 records
            assert isinstance(record, dict)
            # Should have some data fields (exact fields vary by API response)
            assert len(record) > 0


def test_projection_parameter(adme_client):
    """Test that projection parameter is properly handled."""
    # With projection
    result_with = adme_client.get_all_data_by_dtxsid_ccd_projection(
        "DTXSID7020182",
        projection="ccd-adme-data"
    )
    
    # Without projection
    result_without = adme_client.get_all_data_by_dtxsid_ccd_projection(
        "DTXSID7020182",
        projection=None
    )
    
    # Both should return list results
    assert isinstance(result_with, list)
    assert isinstance(result_without, list)


def test_empty_result_handling(adme_client):
    """Test handling of chemicals with no ADME-IVIVE data."""
    # Use a DTXSID that may have no data
    result = adme_client.get_all_data_by_dtxsid_ccd_projection("DTXSID0000001")
    
    # Should return empty list or list with data
    assert isinstance(result, list)
