"""
Tests for ToxRefDB Effects module.

This test suite covers the ToxRefDBEffects class functionality including:
- Client initialization
- Study type retrieval
- Study ID retrieval
- DTXSID retrieval
- Input validation
- Error handling
- Caching functionality
"""

import pytest
from pycomptox.hazard import ToxRefDBEffects


@pytest.fixture
def toxref_client():
    """Fixture to provide a ToxRefDBEffects client instance."""
    return ToxRefDBEffects()


def test_client_initialization(toxref_client):
    """Test that the client initializes correctly."""
    assert toxref_client is not None
    assert hasattr(toxref_client, 'get_data_by_study_type')
    assert hasattr(toxref_client, 'get_data_by_study_id')
    assert hasattr(toxref_client, 'get_data_by_dtxsid')


def test_get_data_by_study_type_dev(toxref_client):
    """Test retrieving effects data by study type (DEV)."""
    study_type = "DEV"
    data = toxref_client.get_data_by_study_type(study_type)
    
    assert data is not None
    assert isinstance(data, dict)
    
    # Should have paginated structure
    if 'data' in data:
        assert isinstance(data['data'], list)


def test_get_data_by_study_type_with_page(toxref_client):
    """Test retrieving effects data with specific page number."""
    study_type = "DEV"
    data = toxref_client.get_data_by_study_type(study_type, page_number=2)
    
    assert data is not None
    assert isinstance(data, dict)


def test_get_data_by_study_id(toxref_client):
    """Test retrieving effects data by study ID."""
    study_id = 63
    data = toxref_client.get_data_by_study_id(study_id)
    
    assert data is not None
    assert isinstance(data, list)
    
    # Study 63 should have effect records
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)


def test_get_data_by_dtxsid(toxref_client):
    """Test retrieving effects data by DTXSID."""
    dtxsid = "DTXSID1037806"
    data = toxref_client.get_data_by_dtxsid(dtxsid)
    
    assert data is not None
    assert isinstance(data, list)
    
    # This chemical should have ToxRefDB data
    if len(data) > 0:
        record = data[0]
        assert isinstance(record, dict)
        assert 'dtxsid' in record


def test_get_data_by_study_type_empty_string(toxref_client):
    """Test that empty study type raises ValueError."""
    with pytest.raises(ValueError, match="study_type must be a non-empty string"):
        toxref_client.get_data_by_study_type("")


def test_get_data_by_study_type_invalid_page(toxref_client):
    """Test that invalid page number raises ValueError."""
    with pytest.raises(ValueError, match="page_number must be a positive integer"):
        toxref_client.get_data_by_study_type("DEV", page_number=0)


def test_get_data_by_study_type_negative_page(toxref_client):
    """Test that negative page number raises ValueError."""
    with pytest.raises(ValueError, match="page_number must be a positive integer"):
        toxref_client.get_data_by_study_type("DEV", page_number=-1)


def test_get_data_by_study_id_invalid(toxref_client):
    """Test that invalid study ID raises ValueError."""
    with pytest.raises(ValueError, match="study_id must be a positive integer"):
        toxref_client.get_data_by_study_id(0)


def test_get_data_by_study_id_negative(toxref_client):
    """Test that negative study ID raises ValueError."""
    with pytest.raises(ValueError, match="study_id must be a positive integer"):
        toxref_client.get_data_by_study_id(-5)


def test_get_data_by_study_id_wrong_type(toxref_client):
    """Test that non-integer study ID raises ValueError."""
    with pytest.raises(ValueError, match="study_id must be a positive integer"):
        toxref_client.get_data_by_study_id("63")


def test_get_data_by_dtxsid_empty_string(toxref_client):
    """Test that empty DTXSID raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        toxref_client.get_data_by_dtxsid("")


def test_get_data_by_dtxsid_none(toxref_client):
    """Test that None DTXSID raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        toxref_client.get_data_by_dtxsid(None)


def test_get_data_by_dtxsid_wrong_type(toxref_client):
    """Test that non-string DTXSID raises ValueError."""
    with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
        toxref_client.get_data_by_dtxsid(12345)


def test_caching_study_type(toxref_client):
    """Test that caching works for study type requests."""
    study_type = "DEV"
    
    # First call - should fetch from API
    data1 = toxref_client.get_data_by_study_type(study_type, use_cache=True)
    
    # Second call - should use cache
    data2 = toxref_client.get_data_by_study_type(study_type, use_cache=True)
    
    # Results should be identical
    assert data1 == data2


def test_caching_study_id(toxref_client):
    """Test that caching works for study ID requests."""
    study_id = 63
    
    # First call - should fetch from API
    data1 = toxref_client.get_data_by_study_id(study_id, use_cache=True)
    
    # Second call - should use cache
    data2 = toxref_client.get_data_by_study_id(study_id, use_cache=True)
    
    # Results should be identical
    assert data1 == data2


def test_caching_dtxsid(toxref_client):
    """Test that caching works for DTXSID requests."""
    dtxsid = "DTXSID1037806"
    
    # First call - should fetch from API
    data1 = toxref_client.get_data_by_dtxsid(dtxsid, use_cache=True)
    
    # Second call - should use cache
    data2 = toxref_client.get_data_by_dtxsid(dtxsid, use_cache=True)
    
    # Results should be identical
    assert data1 == data2


def test_no_caching(toxref_client):
    """Test that caching can be disabled."""
    dtxsid = "DTXSID1037806"
    
    # Call with use_cache=False should work
    data = toxref_client.get_data_by_dtxsid(dtxsid, use_cache=False)
    
    assert data is not None
    assert isinstance(data, list)
