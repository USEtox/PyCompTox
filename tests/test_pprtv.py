"""
Tests for the PPRTV (Provisional Peer-Reviewed Toxicity Values) class.

This test suite covers:
- PPRTV data retrieval by DTXSID
- Error handling for invalid inputs
- Client initialization
"""

import pytest
from pycomptox.hazard import PPRTV


@pytest.fixture
def pprtv_client():
    """Create a PPRTV instance for testing."""
    return PPRTV()


def test_client_initialization(pprtv_client):
    """Test that PPRTV client initializes correctly."""
    assert pprtv_client is not None
    assert pprtv_client.base_url == "https://comptox.epa.gov/ctx-api"
    assert pprtv_client.api_key is not None


def test_get_pprtv_data_by_dtxsid(pprtv_client):
    """Test getting PPRTV data by DTXSID."""
    # Test with a known chemical (Benzene)
    dtxsid = "DTXSID7020182"
    result = pprtv_client.get_all_pprtv_chemical_by_dtxsid(dtxsid)
    
    # Should return a list (may be empty if no PPRTV data exists)
    assert isinstance(result, list)


def test_get_pprtv_data_structure(pprtv_client):
    """Test that PPRTV data has expected structure when data exists."""
    # Test with several chemicals to find one with PPRTV data
    test_dtxsids = [
        "DTXSID7020182",  # Benzene
        "DTXSID5020001",  # Acephate
        "DTXSID2020024",  # Aniline
    ]
    
    for dtxsid in test_dtxsids:
        result = pprtv_client.get_all_pprtv_chemical_by_dtxsid(dtxsid)
        
        if result and len(result) > 0:
            # Check expected fields exist
            first_record = result[0]
            
            # These fields should exist (though may be None/empty)
            expected_fields = [
                'id', 'dtxsid', 'pprtvSubstanceId', 'name', 'casrn',
                'lastRevision', 'pprtvAssessment', 'irisLink',
                'rfcValue', 'rfdValue', 'woe'
            ]
            
            for field in expected_fields:
                assert field in first_record, f"Field '{field}' not found in PPRTV data"
            
            # If we found data, we've verified the structure
            break


def test_invalid_dtxsid_empty_string(pprtv_client):
    """Test handling of empty string DTXSID."""
    with pytest.raises(ValueError, match="must be a non-empty string"):
        pprtv_client.get_all_pprtv_chemical_by_dtxsid("")


def test_invalid_dtxsid_none(pprtv_client):
    """Test handling of None DTXSID."""
    with pytest.raises(ValueError, match="must be a non-empty string"):
        pprtv_client.get_all_pprtv_chemical_by_dtxsid(None)


def test_invalid_dtxsid_wrong_type(pprtv_client):
    """Test handling of non-string DTXSID."""
    with pytest.raises(ValueError, match="must be a non-empty string"):
        pprtv_client.get_all_pprtv_chemical_by_dtxsid(12345)


def test_client_initialization_with_api_key():
    """Test that client can be initialized with explicit API key."""
    from pycomptox.config import load_api_key
    api_key = load_api_key()
    
    if api_key:
        client = PPRTV(api_key=api_key)
        assert client.api_key == api_key


def test_caching_functionality(pprtv_client):
    """Test that caching works correctly."""
    dtxsid = "DTXSID7020182"
    
    # First call (should hit API)
    result1 = pprtv_client.get_all_pprtv_chemical_by_dtxsid(dtxsid, use_cache=True)
    
    # Second call (should use cache)
    result2 = pprtv_client.get_all_pprtv_chemical_by_dtxsid(dtxsid, use_cache=True)
    
    # Results should be identical
    assert result1 == result2


def test_no_cache_option(pprtv_client):
    """Test that cache can be disabled."""
    dtxsid = "DTXSID7020182"
    
    # Call with cache disabled
    result = pprtv_client.get_all_pprtv_chemical_by_dtxsid(dtxsid, use_cache=False)
    
    # Should still return valid data
    assert isinstance(result, list)


# Manual test runner for development
if __name__ == "__main__":
    print("Running PPRTV tests manually...")
    client = PPRTV()
    
    print("\n1. Testing PPRTV data retrieval:")
    test_chemicals = [
        ("DTXSID7020182", "Benzene"),
        ("DTXSID5020001", "Acephate"),
        ("DTXSID2020024", "Aniline"),
    ]
    
    for dtxsid, name in test_chemicals:
        print(f"\n   Testing {name} ({dtxsid}):")
        try:
            data = client.get_all_pprtv_chemical_by_dtxsid(dtxsid)
            if data:
                print(f"   ✓ Found {len(data)} PPRTV record(s)")
                if len(data) > 0:
                    record = data[0]
                    print(f"     - Name: {record.get('name', 'N/A')}")
                    print(f"     - CASRN: {record.get('casrn', 'N/A')}")
                    if record.get('rfcValue'):
                        print(f"     - RfC: {record['rfcValue']} mg/m³")
                    if record.get('rfdValue'):
                        print(f"     - RfD: {record['rfdValue']} mg/kg-day")
                    if record.get('woe'):
                        print(f"     - Weight of Evidence: {record['woe']}")
            else:
                print(f"   - No PPRTV data available")
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    print("\n2. Testing error handling:")
    try:
        client.get_all_pprtv_chemical_by_dtxsid("")
        print("   ✗ Should have raised ValueError for empty string")
    except ValueError:
        print("   ✓ Correctly raised ValueError for empty string")
    
    print("\n✓ All manual tests completed!")
