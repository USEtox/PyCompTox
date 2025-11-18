"""
Tests for the AssaySearch class.

This test suite covers:
- Search by starting value (prefix match)
- Search by exact value (exact match)
- Search by substring value (contains match)
- URL encoding of search values
- Rate limiting
- Error handling
"""

import pytest
import time
from pycomptox.bioactivity import AssaySearch


@pytest.fixture
def search_client():
    """Create an AssaySearch instance for testing."""
    return AssaySearch()


def test_search_by_starting_value_default(search_client):
    """Test searching for assays by starting value with default parameters."""
    results = search_client.search_by_starting_value("ATG_S")
    
    # Should return a list
    assert isinstance(results, list)
    assert len(results) > 0
    
    # Check that all results start with the search value
    for result in results:
        assert "searchValue" in result
        assert result["searchValue"].startswith("ATG_S")
        
    # Verify result structure
    first_result = results[0]
    assert "id" in first_result
    assert "aeid" in first_result
    assert "searchName" in first_result
    assert "searchValueDesc" in first_result


def test_search_by_starting_value_with_top_limit(search_client):
    """Test searching with top parameter to limit results."""
    top_limit = 10
    results = search_client.search_by_starting_value("ATG_", top=top_limit)
    
    assert isinstance(results, list)
    # Results should not exceed the limit (API may return fewer)
    assert len(results) <= top_limit


def test_search_by_exact_value(search_client):
    """Test searching for assays by exact value."""
    results = search_client.search_by_exact_value("ATG_STAT3_CIS")
    
    assert isinstance(results, list)
    assert len(results) > 0
    
    # Should find exact match
    found_exact = False
    for result in results:
        if result["searchValue"] == "ATG_STAT3_CIS":
            found_exact = True
            break
    
    assert found_exact, "Exact match not found in results"
    
    # Verify result structure
    first_result = results[0]
    assert "id" in first_result
    assert "aeid" in first_result
    assert "searchValue" in first_result
    assert "searchValueDesc" in first_result


def test_search_by_substring_value(search_client):
    """Test searching for assays by substring."""
    results = search_client.search_by_substring_value("STAT3")
    
    assert isinstance(results, list)
    assert len(results) > 0
    
    # Check that all results contain the substring
    for result in results:
        assert "searchValue" in result
        # Substring should appear in searchValue or searchName
        search_value = result["searchValue"].upper()
        search_name = result.get("searchName", "").upper()
        assert "STAT3" in search_value or "STAT3" in search_name


def test_search_by_substring_with_top_limit(search_client):
    """Test substring search with top parameter."""
    top_limit = 15
    results = search_client.search_by_substring_value("ATG", top=top_limit)
    
    assert isinstance(results, list)
    assert len(results) <= top_limit


def test_url_encoding_with_special_characters(search_client):
    """Test that search values with special characters are properly URL encoded."""
    # This should not raise an exception even with special characters
    try:
        # Using a simple search that might contain special chars in synonyms
        results = search_client.search_by_starting_value("ATG_")
        assert isinstance(results, list)
    except ValueError:
        # It's OK if no data is found, we just want to ensure no encoding errors
        pass


def test_search_result_field_types(search_client):
    """Test that result fields have expected data types."""
    results = search_client.search_by_starting_value("ATG_S", top=5)
    
    assert len(results) > 0
    
    for result in results:
        # Check field types
        assert isinstance(result.get("id"), int)
        assert isinstance(result.get("aeid"), int)
        assert isinstance(result.get("searchName"), str)
        assert isinstance(result.get("searchValue"), str)
        assert isinstance(result.get("searchValueDesc"), str)


def test_invalid_search_value(search_client):
    """Test searching with a value that returns no results."""
    # Using a very unlikely search string - API returns empty list, not error
    result = search_client.search_by_exact_value("ZZZZZZZZZZZ_NONEXISTENT_12345")
    assert result == []
    assert len(result) == 0


def test_client_initialization_with_api_key():
    """Test that client can be initialized with explicit API key."""
    from pycomptox.config import load_api_key
    api_key = load_api_key()
    
    if api_key:
        client = AssaySearch(api_key=api_key)
        assert client.api_key == api_key


def test_rate_limiting(search_client):
    """Test that rate limiting works correctly."""
    # Create a client with rate limiting and cache disabled
    client_with_delay = AssaySearch(time_delay_between_calls=0.5, use_cache=False)
    
    start_time = time.time()
    
    # Make two consecutive calls
    client_with_delay.search_by_starting_value("ATG_", top=5)
    client_with_delay.search_by_starting_value("ATG_", top=5)
    
    elapsed_time = time.time() - start_time
    
    # Should take at least 0.5 seconds due to rate limiting
    assert elapsed_time >= 0.5


def test_different_search_methods_consistency(search_client):
    """Test that different search methods work with the same values."""
    search_value = "ATG_STAT3_CIS"
    
    # Exact search should find it
    exact_results = search_client.search_by_exact_value(search_value)
    assert len(exact_results) > 0
    
    # Starting with search should find it
    starting_results = search_client.search_by_starting_value("ATG_STAT3", top=100)
    assert len(starting_results) > 0
    
    # Substring search should find it
    substring_results = search_client.search_by_substring_value("STAT3_CIS", top=100)
    assert len(substring_results) > 0


def test_empty_results_handling(search_client):
    """Test handling of searches that should return no results."""
    # Very specific non-existent value - API returns empty list
    result = search_client.search_by_exact_value("NONEXISTENT_ASSAY_XYZ_999")
    assert result == []
    assert len(result) == 0


# Manual test runner for development
if __name__ == "__main__":
    print("Running AssaySearch tests manually...")
    client = AssaySearch()
    
    print("\n1. Testing search by starting value:")
    results = client.search_by_starting_value("ATG_S", top=3)
    for r in results[:3]:
        print(f"   - {r['searchValue']}: {r['searchValueDesc']}")
    
    print("\n2. Testing search by exact value:")
    results = client.search_by_exact_value("ATG_STAT3_CIS")
    print(f"   Found {len(results)} exact matches")
    if results:
        print(f"   First: {results[0]['searchValue']}")
    
    print("\n3. Testing search by substring:")
    results = client.search_by_substring_value("STAT3", top=3)
    for r in results[:3]:
        print(f"   - {r['searchValue']}")
    
    print("\n✓ All manual tests completed!")
