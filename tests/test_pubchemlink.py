"""
Tests for the PubChemLink class
"""

import pytest
import time
from pycomptox.chemical import PubChemLink


class TestPubChemLink:
    """Test suite for PubChemLink functionality"""
    
    def test_client_initialization(self):
        """Test that the client initializes correctly"""
        client = PubChemLink()
        assert client.base_url == "https://comptox.epa.gov/ctx-api"
        assert client.session is not None
        assert client.time_delay_between_calls == 0.5
    
    def test_check_existence_by_dtxsid(self):
        """Test checking PubChem GHS data for a single chemical"""
        client = PubChemLink()
        
        # Test with Bisphenol A (should have PubChem data)
        result = client.check_existence_by_dtxsid("DTXSID7020182")
        
        assert isinstance(result, dict)
        assert 'dtxsid' in result
        assert 'isSafetyData' in result
        assert 'safetyUrl' in result
        assert result['dtxsid'] == "DTXSID7020182"
        
        # If it has data, URL should be present
        if result['isSafetyData']:
            assert result['safetyUrl']
            assert 'pubchem.ncbi.nlm.nih.gov' in result['safetyUrl']
    
    def test_check_existence_invalid_dtxsid(self):
        """Test checking with an invalid DTXSID"""
        client = PubChemLink()
        
        # API may not raise an error for invalid DTXSID, just returns a result
        # So we test that it returns a valid response structure
        result = client.check_existence_by_dtxsid("INVALID123")
        assert isinstance(result, dict)
        assert 'dtxsid' in result
        assert 'isSafetyData' in result
    
    def test_check_existence_empty_dtxsid(self):
        """Test that empty DTXSID raises ValueError"""
        client = PubChemLink()
        
        with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
            client.check_existence_by_dtxsid("")
    
    def test_check_existence_by_dtxsid_batch(self):
        """Test checking PubChem GHS data for multiple chemicals"""
        client = PubChemLink()
        
        dtxsids = [
            "DTXSID7020182",  # Bisphenol A
            "DTXSID2021315"   # Caffeine
        ]
        
        results = client.check_existence_by_dtxsid_batch(dtxsids)
        
        assert isinstance(results, list)
        assert len(results) == 2
        
        for result in results:
            assert 'dtxsid' in result
            assert 'isSafetyData' in result
            assert 'safetyUrl' in result
            assert result['dtxsid'] in dtxsids
    
    def test_batch_size_limit(self):
        """Test that batch size limit is enforced"""
        client = PubChemLink()
        
        # Create a list with more than 1000 items
        too_many_dtxsids = [f"DTXSID{i}" for i in range(1001)]
        
        with pytest.raises(ValueError, match="Maximum 1000 DTXSIDs allowed"):
            client.check_existence_by_dtxsid_batch(too_many_dtxsids)
    
    def test_batch_empty_list(self):
        """Test that empty list raises ValueError"""
        client = PubChemLink()
        
        with pytest.raises(ValueError, match="dtxsids must be a non-empty list"):
            client.check_existence_by_dtxsid_batch([])
    
    def test_rate_limiting(self):
        """Test that rate limiting is enforced"""
        client = PubChemLink(rate_limit_delay=0.5, use_cache=False)
        
        start_time = time.time()
        client.check_existence_by_dtxsid("DTXSID7020182")
        client.check_existence_by_dtxsid("DTXSID2021315")
        elapsed = time.time() - start_time
        
        # Should take at least 0.5 seconds due to rate limiting
        assert elapsed >= 0.5
    
    def test_pubchemlink_import(self):
        """Test that PubChemLink can be imported from main package"""
        from pycomptox.chemical import PubChemLink
        assert PubChemLink is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
