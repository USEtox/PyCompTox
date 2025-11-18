"""
Tests for ToxRefDB Summary module.

This test suite covers the ToxRefDBSummary class functionality including:
- Client initialization
- Study type retrieval
- Study ID retrieval
- DTXSID retrieval
- Input validation
- Error handling
- Caching functionality
"""

import pytest
from pycomptox.hazard import ToxRefDBSummary


@pytest.fixture
def toxref_summary_client():
    """Fixture to provide a ToxRefDBSummary client instance."""
    return ToxRefDBSummary()


def test_client_initialization(toxref_summary_client):
    """Test that the client initializes correctly."""
    assert toxref_summary_client is not None
    assert hasattr(toxref_summary_client, 'get_data_by_study_type')
    assert hasattr(toxref_summary_client, 'get_data_by_study_id')
    assert hasattr(toxref_summary_client, 'get_data_by_dtxsid')


def test_get_data_by_study_type_dev(toxref_summary_client):
    """Test retrieving summary data by study type (DEV)."""
    study_type = "DEV"
    data = toxref_summary_client.get_data_by_study_type(study_type)
    
    assert data is not None
    assert isinstance(data, list)
    
    # Should have study summaries for DEV type
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)


def test_get_data_by_study_id(toxref_summary_client):
    """Test retrieving summary data by study ID."""
    study_id = 63
    data = toxref_summary_client.get_data_by_study_id(study_id)
    
    assert data is not None
    assert isinstance(data, list)
    
    # Study 63 should have summary information
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)


def test_get_data_by_dtxsid(toxref_summary_client):
    """Test retrieving summary data by DTXSID."""
    dtxsid = "DTXSID1037806"
    data = toxref_summary_client.get_data_by_dtxsid(dtxsid)
    
    assert data is not None
    assert isinstance(data, list)
    
    # This chemical should have ToxRefDB summary data
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)


def test_get_data_by_study_type_empty_string(toxref_summary_client):
    """Test that empty study type raises ValueError."""
    with pytest.raises(ValueError, match="study_type must be a non-empty string"):
        toxref_summary_client.get_data_by_study_type("")


def test_get_data_by_study_type_none(toxref_summary_client):
    """Test that None study type raises ValueError."""
    with pytest.raises(ValueError, match="study_type must be a non-empty string"):
        toxref_summary_client.get_data_by_study_type(None)


def test_get_data_by_study_id_invalid(toxref_summary_client):
    """Test that invalid study ID raises ValueError."""
    with pytest.raises(ValueError, match="study_id must be a positive integer"):
        toxref_summary_client.get_data_by_study_id(0)


def test_get_data_by_study_id_negative(toxref_summary_client):
    """Test that negative study ID raises ValueError."""
    with pytest.raises(ValueError, match="study_id must be a positive integer"):
        toxref_summary_client.get_data_by_study_id(-5)


def test_get_data_by_study_id_wrong_type(toxref_summary_client):
    """Test that non-integer study ID raises ValueError."""
    with pytest.raises(ValueError, match="study_id must be a positive integer"):
        toxref_summary_client.get_data_by_study_id("63")


def test_get_data_by_dtxsid_empty_string(toxref_summary_client):
    """Test that empty DTXSID raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        toxref_summary_client.get_data_by_dtxsid("")


def test_get_data_by_dtxsid_none(toxref_summary_client):
    """Test that None DTXSID raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        toxref_summary_client.get_data_by_dtxsid(None)


def test_get_data_by_dtxsid_wrong_type(toxref_summary_client):
    """Test that non-string DTXSID raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        toxref_summary_client.get_data_by_dtxsid(12345)


def test_caching_study_type(toxref_summary_client):
    """Test that caching works for study type requests."""
    study_type = "DEV"
    
    # First call - should fetch from API
    data1 = toxref_summary_client.get_data_by_study_type(study_type, use_cache=True)
    
    # Second call - should use cache
    data2 = toxref_summary_client.get_data_by_study_type(study_type, use_cache=True)
    
    # Results should be identical
    assert data1 == data2


def test_caching_study_id(toxref_summary_client):
    """Test that caching works for study ID requests."""
    study_id = 63
    
    # First call - should fetch from API
    data1 = toxref_summary_client.get_data_by_study_id(study_id, use_cache=True)
    
    # Second call - should use cache
    data2 = toxref_summary_client.get_data_by_study_id(study_id, use_cache=True)
    
    # Results should be identical
    assert data1 == data2


def test_caching_dtxsid(toxref_summary_client):
    """Test that caching works for DTXSID requests."""
    dtxsid = "DTXSID1037806"
    
    # First call - should fetch from API
    data1 = toxref_summary_client.get_data_by_dtxsid(dtxsid, use_cache=True)
    
    # Second call - should use cache
    data2 = toxref_summary_client.get_data_by_dtxsid(dtxsid, use_cache=True)
    
    # Results should be identical
    assert data1 == data2


def test_no_caching(toxref_summary_client):
    """Test that caching can be disabled."""
    dtxsid = "DTXSID1037806"
    
    # Call with use_cache=False should work
    data = toxref_summary_client.get_data_by_dtxsid(dtxsid, use_cache=False)
    
    assert data is not None
    assert isinstance(data, list)
