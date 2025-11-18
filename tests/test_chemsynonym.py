"""
Tests for ChemSynonym API client.

This module contains tests for chemical synonym retrieval functionality.
"""

import pytest
from pycomptox.chemical import ChemSynonym


@pytest.fixture
def synonym_client():
    """Create a ChemSynonym client for testing."""
    return ChemSynonym()


def test_get_synonyms_by_dtxsid_default(synonym_client):
    """Test getting synonyms with default projection (structured view)."""
    dtxsid = "DTXSID7020182"  # Bisphenol A
    
    result = synonym_client.get_synonyms_by_dtxsid(dtxsid)
    
    # Verify response structure
    assert isinstance(result, dict)
    assert "dtxsid" in result
    assert result["dtxsid"] == dtxsid
    
    # Check expected fields exist
    expected_fields = ["beilstein", "alternateCasrn", "dtxsid", "pcCode",
                       "deletedCasrn", "other", "valid", "good"]
    for field in expected_fields:
        assert field in result
    
    # Verify lists are returned
    assert isinstance(result.get("valid", []), list)
    assert isinstance(result.get("good", []), list)
    
    # Bisphenol A should have valid synonyms
    assert len(result.get("valid", [])) > 0
    
    print(f"\n✓ Found {len(result.get('valid', []))} valid synonyms")
    print(f"  Sample synonyms: {result.get('valid', [])[:3]}")


def test_get_synonyms_by_dtxsid_ccd_projection(synonym_client):
    """Test getting synonyms with ccd-synonyms projection (flat list)."""
    dtxsid = "DTXSID7020182"  # Bisphenol A
    
    result = synonym_client.get_synonyms_by_dtxsid(dtxsid, projection="ccd-synonyms")
    
    # Should return a list of synonym objects
    assert isinstance(result, list)
    assert len(result) > 0
    
    # Check structure of first item
    first_item = result[0]
    assert isinstance(first_item, dict)
    assert "synonym" in first_item
    assert "quality" in first_item
    
    # Verify synonym and quality are strings
    assert isinstance(first_item["synonym"], str)
    assert isinstance(first_item.get("quality"), (str, type(None)))
    
    print(f"\n✓ Found {len(result)} synonyms with quality ratings")
    print(f"  Sample: {first_item['synonym']} (quality: {first_item.get('quality')})")


def test_get_synonyms_different_chemicals(synonym_client):
    """Test getting synonyms for different chemicals."""
    test_chemicals = {
        "DTXSID7020182": "Bisphenol A",
        "DTXSID2021315": "Caffeine"
    }
    
    for dtxsid, name in test_chemicals.items():
        result = synonym_client.get_synonyms_by_dtxsid(dtxsid)
        
        assert isinstance(result, dict)
        assert result["dtxsid"] == dtxsid
        assert len(result.get("valid", [])) > 0
        
        print(f"\n✓ {name} ({dtxsid}): {len(result.get('valid', []))} valid synonyms")


def test_get_synonyms_batch_single(synonym_client):
    """Test batch synonym retrieval with single DTXSID."""
    dtxsids = ["DTXSID7020182"]

    results = synonym_client.get_synonyms_by_dtxsid_batch(dtxsids)

    # Should return a list (API may return duplicates)
    assert isinstance(results, list)
    assert len(results) >= 1    # Check structure
    result = results[0]
    assert isinstance(result, dict)
    assert "dtxsid" in result
    assert result["dtxsid"] == dtxsids[0]
    
    print(f"\n✓ Batch request successful for 1 chemical")


def test_get_synonyms_batch_multiple(synonym_client):
    """Test batch synonym retrieval with multiple DTXSIDs."""
    dtxsids = [
        "DTXSID7020182",  # Bisphenol A
        "DTXSID2021315"   # Caffeine
    ]
    
    results = synonym_client.get_synonyms_by_dtxsid_batch(dtxsids)

    # Should return a list
    assert isinstance(results, list)
    assert len(results) >= 2

    # Check that all requested DTXSIDs are present
    returned_dtxsids = {r["dtxsid"] for r in results}
    for dtxsid in dtxsids:
        assert dtxsid in returned_dtxsids    # Verify each has valid synonyms
    for result in results:
        assert isinstance(result, dict)
        assert "dtxsid" in result
        assert "valid" in result
        
    print(f"\n✓ Batch request successful for {len(dtxsids)} chemicals")
    for result in results:
        valid_count = len(result.get("valid", []))
        print(f"  {result['dtxsid']}: {valid_count} valid synonyms")


def test_get_synonyms_batch_max_limit(synonym_client):
    """Test that batch request rejects more than 1000 DTXSIDs."""
    # Create a list with 1001 DTXSIDs
    dtxsids = [f"DTXSID{i:07d}" for i in range(1001)]
    
    with pytest.raises(ValueError) as exc_info:
        synonym_client.get_synonyms_by_dtxsid_batch(dtxsids)
    
    assert "1000 DTXSIDs" in str(exc_info.value)
    print(f"\n✓ Correctly rejected batch with {len(dtxsids)} DTXSIDs")


def test_synonym_fields_content(synonym_client):
    """Test that synonym fields contain expected data types and content."""
    dtxsid = "DTXSID7020182"  # Bisphenol A
    
    result = synonym_client.get_synonyms_by_dtxsid(dtxsid)
    
    # Test valid synonyms
    if result.get("valid"):
        assert all(isinstance(syn, str) for syn in result["valid"])
        assert len(result["valid"]) > 0
        print(f"\n✓ Valid synonyms: {result['valid'][:3]}...")
    
    # Test good quality synonyms
    if result.get("good"):
        assert all(isinstance(syn, str) for syn in result["good"])
        print(f"✓ Good quality synonyms: {result['good'][:3]}...")
    
    # Test alternate CAS numbers if present
    if result.get("alternateCasrn"):
        assert all(isinstance(cas, str) for cas in result["alternateCasrn"])
        print(f"✓ Alternate CAS numbers: {result['alternateCasrn']}")


def test_invalid_dtxsid(synonym_client):
    """Test handling of invalid DTXSID."""
    invalid_dtxsid = "INVALID123"
    
    with pytest.raises(Exception):  # API raises HTTPError (400)
        synonym_client.get_synonyms_by_dtxsid(invalid_dtxsid)
    
    print(f"\n✓ Correctly handled invalid DTXSID: {invalid_dtxsid}")


def test_projection_parameter(synonym_client):
    """Test that projection parameter changes response structure."""
    dtxsid = "DTXSID7020182"
    
    # Default projection
    default_result = synonym_client.get_synonyms_by_dtxsid(dtxsid)
    assert isinstance(default_result, dict)
    
    # CCD projection
    ccd_result = synonym_client.get_synonyms_by_dtxsid(dtxsid, projection="ccd-synonyms")
    assert isinstance(ccd_result, list)
    
    print(f"\n✓ Different projections return different structures")
    print(f"  Default: dict with {len(default_result)} keys")
    print(f"  CCD: list with {len(ccd_result)} items")


def test_batch_returns_all_fields(synonym_client):
    """Test that batch requests return all expected fields."""
    dtxsids = ["DTXSID7020182", "DTXSID2021315"]
    
    results = synonym_client.get_synonyms_by_dtxsid_batch(dtxsids)
    
    expected_fields = ["dtxsid", "valid", "good", "other", "beilstein",
                       "alternateCasrn", "deletedCasrn", "pcCode"]
    
    for result in results:
        for field in expected_fields:
            assert field in result, f"Missing field: {field}"
    
    print(f"\n✓ All expected fields present in batch results")


def test_client_initialization_with_api_key(synonym_client):
    """Test that client initializes properly."""
    assert synonym_client.api_key is not None
    assert synonym_client.base_url == "https://comptox.epa.gov/ctx-api"
    assert synonym_client.time_delay_between_calls == 0.0
    
    print(f"\n✓ ChemSynonym client initialized successfully")


def test_rate_limiting():
    """Test that rate limiting works."""
    import time
    
    client = ChemSynonym(time_delay_between_calls=0.5)
    
    start_time = time.time()
    # Use different DTXSIDs to avoid cache
    client.get_synonyms_by_dtxsid("DTXSID7020182", use_cache=False)
    client.get_synonyms_by_dtxsid("DTXSID2021315", use_cache=False)
    elapsed_time = time.time() - start_time
    
    # Should take at least 0.5 seconds due to rate limiting
    assert elapsed_time >= 0.5
    
    print(f"\n✓ Rate limiting working: {elapsed_time:.2f}s for 2 calls")


if __name__ == "__main__":
    # Run tests manually for development
    client = ChemSynonym()
    
    print("=" * 70)
    print("ChemSynonym API Tests")
    print("=" * 70)
    
    print("\n1. Testing default synonym retrieval...")
    test_get_synonyms_by_dtxsid_default(client)
    
    print("\n2. Testing CCD projection...")
    test_get_synonyms_by_dtxsid_ccd_projection(client)
    
    print("\n3. Testing different chemicals...")
    test_get_synonyms_different_chemicals(client)
    
    print("\n4. Testing batch retrieval...")
    test_get_synonyms_batch_multiple(client)
    
    print("\n5. Testing synonym field content...")
    test_synonym_fields_content(client)
    
    print("\n" + "=" * 70)
    print("All manual tests completed successfully!")
    print("=" * 70)
