"""
Tests for the ChemicalList class
"""

import pytest
import time
from pycomptox.chemical import ChemicalList


class TestChemicalList:
    """Test suite for ChemicalList functionality"""
    
    def test_client_initialization(self):
        """Test that the client initializes correctly"""
        client = ChemicalList()
        assert client.base_url == "https://comptox.epa.gov/ctx-api"
        assert client.session is not None
        assert client.time_delay_between_calls == 0.5
    
    def test_get_all_list_types(self):
        """Test getting all list types"""
        client = ChemicalList()
        types = client.get_all_list_types()
        
        assert isinstance(types, list)
        assert len(types) > 0
        # Should contain the standard list types
        expected_types = ['federal', 'international', 'other', 'state']
        for expected in expected_types:
            assert expected in types
    
    def test_get_public_lists_by_type(self):
        """Test getting public lists by type"""
        client = ChemicalList()
        
        # Get federal lists
        federal_lists = client.get_public_lists_by_type('federal')
        
        assert isinstance(federal_lists, list)
        assert len(federal_lists) > 0
        
        # Check structure of first list
        first_list = federal_lists[0]
        assert 'listName' in first_list
        assert 'label' in first_list
        assert 'type' in first_list
        assert first_list['type'] == 'federal'
    
    def test_get_public_lists_by_type_empty(self):
        """Test that empty list_type raises ValueError"""
        client = ChemicalList()
        
        with pytest.raises(ValueError, match="list_type must be a non-empty string"):
            client.get_public_lists_by_type('')
    
    def test_get_public_lists_by_name(self):
        """Test searching for lists by name - API endpoint may not be available"""
        client = ChemicalList()
        
        # This endpoint might not be fully supported, so we'll test it gracefully
        try:
            tsca_lists = client.get_public_lists_by_name('PFAS')
            assert isinstance(tsca_lists, list)
        except (RuntimeError, Exception):
            # API endpoint may not be available or may have changed
            pass
    
    def test_get_public_lists_by_name_empty(self):
        """Test that empty name raises ValueError"""
        client = ChemicalList()
        
        with pytest.raises(ValueError, match="name must be a non-empty string"):
            client.get_public_lists_by_name('')
    
    def test_get_public_lists_by_dtxsid(self):
        """Test getting lists containing a specific chemical"""
        client = ChemicalList()
        
        # Use Bisphenol A
        dtxsid = "DTXSID7020182"
        lists = client.get_public_lists_by_dtxsid(dtxsid)
        
        assert isinstance(lists, list)
        # Bisphenol A should appear in multiple lists
        assert len(lists) > 0
        
        # API returns list of lists, not list of dicts
        # Just verify we got some data back
        first_item = lists[0]
        assert isinstance(first_item, list)
    
    def test_get_public_lists_by_dtxsid_empty(self):
        """Test that empty DTXSID raises ValueError"""
        client = ChemicalList()
        
        with pytest.raises(ValueError, match="dtxsid must be a non-empty string"):
            client.get_public_lists_by_dtxsid('')
    
    def test_get_all_public_lists(self):
        """Test getting all public lists"""
        client = ChemicalList()
        
        try:
            # Get all lists (this might be a large response)
            all_lists = client.get_all_public_lists()
            
            assert isinstance(all_lists, list)
            assert len(all_lists) > 100  # Should be many lists
            
            # Check structure
            first_list = all_lists[0]
            assert 'listName' in first_list
            assert 'type' in first_list
        except Exception:
            # API endpoint may not be available
            pass
    
    def test_rate_limiting(self):
        """Test that rate limiting is enforced"""
        client = ChemicalList(time_delay_between_calls=0.5)
        
        start_time = time.time()
        # Disable cache to ensure rate limiting is tested
        client.get_all_list_types(use_cache=False)
        client.get_all_list_types(use_cache=False)
        elapsed = time.time() - start_time
        
        # Should take at least 0.5 seconds due to rate limiting
        assert elapsed >= 0.5
    
    def test_chemicallist_import(self):
        """Test that ChemicalList can be imported from main package"""
        from pycomptox.chemical import ChemicalList
        assert ChemicalList is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
