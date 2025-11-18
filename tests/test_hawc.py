"""
Tests for HAWC (Health Assessment Workspace Collaborative) module.

This test suite covers the HAWC class functionality including:
- Client initialization
- DTXSID retrieval
- Input validation
- Error handling
- Caching functionality
"""

import pytest
from pycomptox.hazard import HAWC


@pytest.fixture
def hawc_client():
    """Fixture to provide a HAWC client instance."""
    return HAWC()


def test_client_initialization(hawc_client):
    """Test that the client initializes correctly."""
    assert hawc_client is not None
    assert hasattr(hawc_client, 'get_ccd_hawc_link_mapper_by_dtxsid')


def test_get_ccd_hawc_link_mapper_by_dtxsid_formaldehyde(hawc_client):
    """Test retrieving HAWC links for formaldehyde (DTXSID7020182)."""
    dtxsid = "DTXSID7020182"
    data = hawc_client.get_ccd_hawc_link_mapper_by_dtxsid(dtxsid)
    
    assert data is not None
    assert isinstance(data, list)
    
    # Formaldehyde may have HAWC assessments
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)
        # Should have link information
        # May include: dtxsid, hawcUrl, assessmentName, etc.


def test_get_ccd_hawc_link_mapper_by_dtxsid_benzene(hawc_client):
    """Test retrieving HAWC links for benzene (DTXSID0021125)."""
    dtxsid = "DTXSID0021125"
    data = hawc_client.get_ccd_hawc_link_mapper_by_dtxsid(dtxsid)
    
    assert data is not None
    assert isinstance(data, list)
    
    # Check structure if data exists
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)


def test_get_ccd_hawc_link_mapper_empty_string(hawc_client):
    """Test that empty string raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        hawc_client.get_ccd_hawc_link_mapper_by_dtxsid("")


def test_get_ccd_hawc_link_mapper_none(hawc_client):
    """Test that None raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        hawc_client.get_ccd_hawc_link_mapper_by_dtxsid(None)


def test_get_ccd_hawc_link_mapper_wrong_type(hawc_client):
    """Test that non-string input raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        hawc_client.get_ccd_hawc_link_mapper_by_dtxsid(12345)


def test_caching(hawc_client):
    """Test that caching works for HAWC requests."""
    dtxsid = "DTXSID7020182"
    
    # First call - should fetch from API
    data1 = hawc_client.get_ccd_hawc_link_mapper_by_dtxsid(dtxsid, use_cache=True)
    
    # Second call - should use cache
    data2 = hawc_client.get_ccd_hawc_link_mapper_by_dtxsid(dtxsid, use_cache=True)
    
    # Results should be identical
    assert data1 == data2


def test_no_caching(hawc_client):
    """Test that caching can be disabled."""
    dtxsid = "DTXSID7020182"
    
    # Calls with use_cache=False should work
    data = hawc_client.get_ccd_hawc_link_mapper_by_dtxsid(dtxsid, use_cache=False)
    
    assert data is not None
    assert isinstance(data, list)
