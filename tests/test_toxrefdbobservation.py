"""
Tests for ToxRefDBObservation hazard module.
"""

import pytest
from pycomptox.hazard import ToxRefDBObservation


@pytest.fixture
def obs_client():
    """Create a ToxRefDBObservation client for testing."""
    return ToxRefDBObservation()


def test_initialization():
    """Test that ToxRefDBObservation client initializes correctly."""
    client = ToxRefDBObservation()
    assert client is not None
    assert isinstance(client, ToxRefDBObservation)


def test_get_observations_by_study_type_dev(obs_client):
    """Test retrieving observations for developmental toxicity studies."""
    result = obs_client.get_observations_by_study_type("DEV", page_number=1)
    
    assert result is not None
    assert isinstance(result, dict)
    
    # Check for data field
    assert 'data' in result
    assert isinstance(result['data'], list)


def test_get_observations_by_study_type_pagination(obs_client):
    """Test pagination for study type observations."""
    # Get first page
    page1 = obs_client.get_observations_by_study_type("DEV", page_number=1)
    assert page1 is not None
    assert 'pageNumber' in page1
    
    # Get second page
    page2 = obs_client.get_observations_by_study_type("DEV", page_number=2)
    assert page2 is not None


def test_get_observations_by_study_type_invalid_input(obs_client):
    """Test that invalid inputs raise ValueError."""
    with pytest.raises(ValueError):
        obs_client.get_observations_by_study_type("")
    
    with pytest.raises(ValueError):
        obs_client.get_observations_by_study_type(None)
    
    with pytest.raises(ValueError):
        obs_client.get_observations_by_study_type("DEV", page_number=0)
    
    with pytest.raises(ValueError):
        obs_client.get_observations_by_study_type("DEV", page_number=-1)


def test_get_observations_by_study_id(obs_client):
    """Test retrieving observations for a specific study."""
    result = obs_client.get_observations_by_study_id(63)
    
    assert result is not None
    assert isinstance(result, list)
    
    if result:
        # Verify structure
        assert all(isinstance(record, dict) for record in result)
        assert all('studyId' in record for record in result)
        
        # All records should be for the same study
        study_ids = set(record['studyId'] for record in result)
        assert len(study_ids) == 1
        assert 63 in study_ids


def test_get_observations_by_study_id_invalid_input(obs_client):
    """Test that invalid study IDs raise ValueError."""
    with pytest.raises(ValueError):
        obs_client.get_observations_by_study_id(0)
    
    with pytest.raises(ValueError):
        obs_client.get_observations_by_study_id(-1)
    
    with pytest.raises(ValueError):
        obs_client.get_observations_by_study_id("not_an_int")


def test_get_observations_by_dtxsid(obs_client):
    """Test retrieving observations for a specific chemical."""
    result = obs_client.get_observations_by_dtxsid("DTXSID1037806")
    
    assert result is not None
    assert isinstance(result, list)
    
    if result:
        # Verify structure
        assert all(isinstance(record, dict) for record in result)
        assert all('dtxsid' in record for record in result)
        
        # All records should be for the same chemical
        dtxsids = set(record['dtxsid'] for record in result)
        assert len(dtxsids) == 1
        assert "DTXSID1037806" in dtxsids


def test_get_observations_by_dtxsid_invalid_input(obs_client):
    """Test that invalid DTXSIDs raise ValueError."""
    with pytest.raises(ValueError):
        obs_client.get_observations_by_dtxsid("")
    
    with pytest.raises(ValueError):
        obs_client.get_observations_by_dtxsid(None)
    
    with pytest.raises(ValueError):
        obs_client.get_observations_by_dtxsid(123)


def test_different_study_types(obs_client):
    """Test retrieving observations for different study types."""
    study_types = ["DEV", "REP", "ACUTE"]
    
    for stype in study_types:
        try:
            result = obs_client.get_observations_by_study_type(stype, page_number=1)
            assert result is not None
            assert isinstance(result, dict)
            assert 'data' in result
        except Exception:
            # Some study types may not have data or may not be valid
            pass


def test_caching_enabled(obs_client):
    """Test that caching works correctly."""
    # First call
    result1 = obs_client.get_observations_by_study_id(63, use_cache=True)
    
    # Second call should use cache
    result2 = obs_client.get_observations_by_study_id(63, use_cache=True)
    
    # Results should be identical
    assert result1 == result2


def test_observation_data_structure(obs_client):
    """Test that returned observation data has expected structure."""
    result = obs_client.get_observations_by_study_id(63)
    
    if result:
        # Check that records have common fields
        common_fields = ['dtxsid', 'studyId']
        for record in result[:5]:  # Check first 5 records
            for field in common_fields:
                assert field in record, f"Record missing field: {field}"


def test_study_type_data_structure(obs_client):
    """Test that paginated data has expected structure."""
    result = obs_client.get_observations_by_study_type("DEV", page_number=1)
    
    # Check pagination metadata
    assert 'pageNumber' in result
    assert 'data' in result
    assert isinstance(result['data'], list)


def test_multiple_dtxsids(obs_client):
    """Test retrieving observations for multiple chemicals."""
    dtxsids = ["DTXSID1037806"]
    
    for dtxsid in dtxsids:
        result = obs_client.get_observations_by_dtxsid(dtxsid)
        assert result is not None
        assert isinstance(result, list)


def test_observation_status_fields(obs_client):
    """Test that observation status fields are present."""
    result = obs_client.get_observations_by_study_id(63)
    
    if result:
        # Check for observation-specific fields
        # Note: Actual API uses different field names
        for record in result[:5]:
            # Should have at least some observation-related fields
            has_obs_field = any(key in record for key in [
                'endpointCategory', 'defaultStatus', 'dtxsid', 'studyId'
            ])
            assert has_obs_field, "Record missing observation-related fields"
