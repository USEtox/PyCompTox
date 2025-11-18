"""
Tests for ExtraData API functionality.

These tests verify the ExtraData class methods for retrieving reference
counts and metadata from the CompTox Dashboard.
"""

import pytest
from pycomptox.chemical import ExtraData


@pytest.fixture
def extra_client():
    """Create an ExtraData client for testing."""
    return ExtraData()


class TestExtraData:
    """Test suite for ExtraData class."""
    
    def test_client_initialization(self, extra_client):
        """Test that ExtraData client initializes correctly."""
        assert extra_client is not None
        assert extra_client.api_key is not None
        assert extra_client.base_url == "https://comptox.epa.gov/ctx-api"
    
    def test_get_data_by_dtxsid(self, extra_client):
        """Test retrieving extra data for a single chemical."""
        dtxsid = "DTXSID7020182"  # Bisphenol A
        
        try:
            result = extra_client.get_data_by_dtxsid(dtxsid)
            
            # Check response structure
            assert isinstance(result, dict)
            assert 'dtxsid' in result
            assert 'dtxcid' in result
            assert 'refs' in result
            assert 'googlePatent' in result
            assert 'literature' in result
            assert 'pubmed' in result
            
            # Check values
            assert result['dtxsid'] == dtxsid
            assert isinstance(result['refs'], int)
            assert isinstance(result['pubmed'], int)
            assert isinstance(result['googlePatent'], int)
            assert isinstance(result['literature'], int)
            
            print(f"✓ Extra data for {dtxsid}:")
            print(f"  Total refs: {result['refs']}")
            print(f"  PubMed: {result['pubmed']}")
            print(f"  Patents: {result['googlePatent']}")
            print(f"  Literature: {result['literature']}")
            
        except ValueError as e:
            if "not found" in str(e).lower():
                pytest.skip(f"Endpoint not available: {e}")
            else:
                raise
    
    def test_get_data_by_dtxsid_invalid(self, extra_client):
        """Test error handling for invalid DTXSID."""
        invalid_dtxsid = "INVALID123"
        
        with pytest.raises(Exception):  # API raises HTTPError (400)
            extra_client.get_data_by_dtxsid(invalid_dtxsid)
    
    def test_get_data_by_dtxsid_batch(self, extra_client):
        """Test batch retrieval of extra data."""
        dtxsids = [
            "DTXSID7020182",  # Bisphenol A
            "DTXSID2021315",  # Caffeine
            "DTXSID5020001"   # 1,2,3-Trichloropropane
        ]
        
        try:
            results = extra_client.get_data_by_dtxsid_batch(dtxsids)
            
            # Check response structure
            assert isinstance(results, list)
            assert len(results) > 0
            
            # Check each result
            for data in results:
                assert isinstance(data, dict)
                assert 'dtxsid' in data
                assert 'refs' in data
                assert 'pubmed' in data
                assert 'googlePatent' in data
                assert 'literature' in data
            
            # Verify we got results for our DTXSIDs
            returned_dtxsids = {d['dtxsid'] for d in results}
            for dtxsid in dtxsids:
                if dtxsid in returned_dtxsids:
                    print(f"✓ Found data for {dtxsid}")
            
            print(f"\n✓ Batch request returned {len(results)} results")
            
        except ValueError as e:
            if "not found" in str(e).lower():
                pytest.skip(f"Endpoint not available: {e}")
            else:
                raise
    
    def test_batch_size_limit(self, extra_client):
        """Test that batch size limit is enforced."""
        # Create a list with more than 1000 DTXSIDs
        too_many_dtxsids = [f"DTXSID{i:010d}" for i in range(1001)]
        
        with pytest.raises(ValueError, match="Maximum 1000 DTXSIDs"):
            extra_client.get_data_by_dtxsid_batch(too_many_dtxsids)
    
    def test_rate_limiting(self):
        """Test rate limiting functionality."""
        extra_with_delay = ExtraData(time_delay_between_calls=0.5, use_cache=False)
        
        import time
        start_time = time.time()
        
        try:
            # Make two requests
            extra_with_delay.get_data_by_dtxsid("DTXSID7020182")
            extra_with_delay.get_data_by_dtxsid("DTXSID2021315")
            
            elapsed = time.time() - start_time
            
            # Should take at least 0.5 seconds due to rate limiting
            assert elapsed >= 0.5, f"Rate limiting not working: {elapsed}s"
            print(f"✓ Rate limiting working: {elapsed:.2f}s for 2 calls")
            
        except ValueError as e:
            if "not found" in str(e).lower():
                pytest.skip(f"Endpoint not available: {e}")
            else:
                raise


def test_extradata_import():
    """Test that ExtraData can be imported from package."""
    from pycomptox.chemical import ExtraData
    assert ExtraData is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
