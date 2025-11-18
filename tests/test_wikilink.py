"""
Tests for WikiLink API functionality.

These tests verify the WikiLink class methods for checking Wikipedia GHS
Safety data availability from the CompTox Dashboard.
"""

import pytest
from pycomptox.chemical import WikiLink


@pytest.fixture
def wiki_client():
    """Create a WikiLink client for testing."""
    return WikiLink()


class TestWikiLink:
    """Test suite for WikiLink class."""
    
    def test_client_initialization(self, wiki_client):
        """Test that WikiLink client initializes correctly."""
        assert wiki_client is not None
        assert wiki_client.api_key is not None
        assert wiki_client.base_url == "https://comptox.epa.gov/ctx-api"
    
    def test_check_existence_by_dtxsid(self, wiki_client):
        """Test checking Wikipedia GHS data for a single chemical."""
        dtxsid = "DTXSID7020182"  # Bisphenol A
        
        try:
            result = wiki_client.check_existence_by_dtxsid(dtxsid)
            
            # Check response structure
            assert isinstance(result, dict)
            assert 'dtxsid' in result
            assert 'safetyUrl' in result
            
            # Check values
            assert result['dtxsid'] == dtxsid
            assert isinstance(result['safetyUrl'], str)
            
            print(f"✓ Wikipedia check for {dtxsid}:")
            if result['safetyUrl']:
                print(f"  Has GHS data: {result['safetyUrl']}")
            else:
                print(f"  No GHS data available")
            
        except ValueError as e:
            if "not found" in str(e).lower():
                pytest.skip(f"Endpoint not available: {e}")
            else:
                raise
    
    def test_check_existence_invalid_dtxsid(self, wiki_client):
        """Test handling of invalid DTXSID."""
        invalid_dtxsid = "INVALID123"
        
        try:
            result = wiki_client.check_existence_by_dtxsid(invalid_dtxsid)
            # API may return empty result instead of error
            assert isinstance(result, dict)
            print(f"✓ Invalid DTXSID handled: {result}")
        except (ValueError, RuntimeError) as e:
            # Also acceptable if API raises error
            print(f"✓ Invalid DTXSID raised error: {e}")
    
    def test_check_existence_by_dtxsid_batch(self, wiki_client):
        """Test batch Wikipedia GHS data check."""
        dtxsids = [
            "DTXSID7020182",  # Bisphenol A
            "DTXSID2021315",  # Caffeine
            "DTXSID5020001"   # 1,2,3-Trichloropropane
        ]
        
        try:
            results = wiki_client.check_existence_by_dtxsid_batch(dtxsids)
            
            # Check response structure
            assert isinstance(results, list)
            assert len(results) > 0
            
            # Check each result
            for result in results:
                assert isinstance(result, dict)
                assert 'dtxsid' in result
                assert 'safetyUrl' in result
            
            # Count chemicals with Wikipedia data
            with_data = sum(1 for r in results if r['safetyUrl'])
            print(f"\n✓ Batch request returned {len(results)} results")
            print(f"✓ {with_data}/{len(results)} chemicals have Wikipedia GHS data")
            
            for result in results:
                status = "✓" if result['safetyUrl'] else "✗"
                print(f"  {status} {result['dtxsid']}")
            
        except ValueError as e:
            if "not found" in str(e).lower():
                pytest.skip(f"Endpoint not available: {e}")
            else:
                raise
    
    def test_batch_size_limit(self, wiki_client):
        """Test that batch size limit is enforced."""
        # Create a list with more than 1000 DTXSIDs
        too_many_dtxsids = [f"DTXSID{i:010d}" for i in range(1001)]
        
        with pytest.raises(ValueError, match="Maximum 1000 DTXSIDs"):
            wiki_client.check_existence_by_dtxsid_batch(too_many_dtxsids)
    
    def test_rate_limiting(self):
        """Test rate limiting functionality."""
        wiki_with_delay = WikiLink(time_delay_between_calls=0.5, use_cache=False)
        
        import time
        start_time = time.time()
        
        try:
            # Make two requests
            wiki_with_delay.check_existence_by_dtxsid("DTXSID7020182")
            wiki_with_delay.check_existence_by_dtxsid("DTXSID2021315")
            
            elapsed = time.time() - start_time
            
            # Should take at least 0.5 seconds due to rate limiting
            assert elapsed >= 0.5, f"Rate limiting not working: {elapsed}s"
            print(f"✓ Rate limiting working: {elapsed:.2f}s for 2 calls")
            
        except ValueError as e:
            if "not found" in str(e).lower():
                pytest.skip(f"Endpoint not available: {e}")
            else:
                raise


def test_wikilink_import():
    """Test that WikiLink can be imported from package."""
    from pycomptox.chemical import WikiLink
    assert WikiLink is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
