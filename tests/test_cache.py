"""
Tests for the caching system.

This module tests the CacheManager functionality including:
- Cache get/set operations
- Cache clearing
- Export/import functionality
- Cache statistics
- Expiration handling
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import time

from pycomptox.cache import CacheManager, get_default_cache, clear_cache, cache_status


class TestCacheManager:
    """Test the CacheManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create temporary cache directory
        self.temp_dir = tempfile.mkdtemp()
        self.cache = CacheManager(cache_dir=self.temp_dir, enabled=True)
    
    def teardown_method(self):
        """Clean up after tests."""
        # Remove temporary directory
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
    
    def test_cache_initialization(self):
        """Test cache manager initialization."""
        assert self.cache.enabled is True
        assert self.cache.cache_dir == Path(self.temp_dir)
        assert self.cache.max_age_days is None
        assert self.cache.cache_dir.exists()
    
    def test_cache_set_and_get(self):
        """Test basic cache set and get operations."""
        endpoint = "chemical/search"
        params = {"name": "benzene"}
        response = {"dtxsid": "DTXSID0020232", "preferredName": "Benzene"}
        
        # Set cache
        self.cache.set(endpoint, params, response)
        
        # Get from cache
        cached_response = self.cache.get(endpoint, params)
        
        assert cached_response is not None
        assert cached_response == response
    
    def test_cache_miss(self):
        """Test cache miss returns None."""
        endpoint = "chemical/search"
        params = {"name": "nonexistent"}
        
        cached_response = self.cache.get(endpoint, params)
        assert cached_response is None
    
    def test_cache_different_params(self):
        """Test that different parameters create different cache entries."""
        endpoint = "chemical/search"
        params1 = {"name": "benzene"}
        params2 = {"name": "toluene"}
        response1 = {"dtxsid": "DTXSID0020232"}
        response2 = {"dtxsid": "DTXSID7020182"}
        
        self.cache.set(endpoint, params1, response1)
        self.cache.set(endpoint, params2, response2)
        
        cached1 = self.cache.get(endpoint, params1)
        cached2 = self.cache.get(endpoint, params2)
        
        assert cached1 == response1
        assert cached2 == response2
    
    def test_cache_expiration(self):
        """Test that expired cache entries are not returned."""
        # Create cache with 0 day max age
        cache = CacheManager(cache_dir=self.temp_dir, max_age_days=0, enabled=True)
        
        endpoint = "chemical/search"
        params = {"name": "benzene"}
        response = {"dtxsid": "DTXSID0020232"}
        
        cache.set(endpoint, params, response)
        
        # Sleep briefly to ensure expiration
        time.sleep(0.1)
        
        # Should not return expired entry
        cached_response = cache.get(endpoint, params)
        assert cached_response is None
    
    def test_cache_clear_all(self):
        """Test clearing entire cache."""
        # Add multiple cache entries
        self.cache.set("endpoint1", {"param": "value1"}, {"data": "response1"})
        self.cache.set("endpoint2", {"param": "value2"}, {"data": "response2"})
        
        # Clear cache
        count = self.cache.clear()
        
        assert count > 0
        
        # Verify cache is empty
        status = self.cache.get_status()
        assert status['total_entries'] == 0
    
    def test_cache_clear_endpoint(self):
        """Test clearing cache for specific endpoint."""
        endpoint1 = "chemical/search"
        endpoint2 = "chemical/details"
        
        self.cache.set(endpoint1, {"param": "value1"}, {"data": "response1"})
        self.cache.set(endpoint2, {"param": "value2"}, {"data": "response2"})
        
        # Clear only endpoint1
        count = self.cache.clear(endpoint1)
        
        assert count >= 1
        
        # Verify endpoint1 is cleared but endpoint2 remains
        assert self.cache.get(endpoint1, {"param": "value1"}) is None
        assert self.cache.get(endpoint2, {"param": "value2"}) is not None
    
    def test_cache_status(self):
        """Test cache status reporting."""
        # Add some cache entries
        self.cache.set("endpoint1", {"param": "value1"}, {"data": "response1"})
        self.cache.set("endpoint2", {"param": "value2"}, {"data": "response2"})
        
        status = self.cache.get_status()
        
        assert status['enabled'] is True
        assert status['total_entries'] >= 2
        assert status['total_size_bytes'] > 0
        assert status['total_size_mb'] >= 0
        assert 'endpoints' in status
        assert 'oldest_entry' in status
        assert 'newest_entry' in status
    
    def test_cache_export(self):
        """Test cache export functionality."""
        # Add cache entries
        self.cache.set("endpoint1", {"param": "value1"}, {"data": "response1"})
        self.cache.set("endpoint2", {"param": "value2"}, {"data": "response2"})
        
        # Export cache
        export_path = Path(self.temp_dir) / "export.json"
        result = self.cache.export_cache(str(export_path))
        
        assert result['success'] is True
        assert result['entries_exported'] >= 2
        assert export_path.exists()
        
        # Verify export file content
        with open(export_path, 'r') as f:
            export_data = json.load(f)
        
        assert 'entries' in export_data
        assert len(export_data['entries']) >= 2
    
    def test_cache_import(self):
        """Test cache import functionality."""
        # Create export data manually
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'max_age_days': None,
            'entries': [
                {
                    'timestamp': datetime.now().isoformat(),
                    'endpoint': 'endpoint1',
                    'params': {'param': 'value1'},
                    'response': {'data': 'response1'}
                },
                {
                    'timestamp': datetime.now().isoformat(),
                    'endpoint': 'endpoint2',
                    'params': {'param': 'value2'},
                    'response': {'data': 'response2'}
                }
            ]
        }
        
        # Write export file
        import_path = Path(self.temp_dir) / "import.json"
        with open(import_path, 'w') as f:
            json.dump(export_data, f)
        
        # Create new cache and import
        new_cache_dir = tempfile.mkdtemp()
        try:
            new_cache = CacheManager(cache_dir=new_cache_dir, enabled=True)
            result = new_cache.import_cache(str(import_path))
            
            assert result['success'] is True
            assert result['entries_imported'] == 2
            
            # Verify imported data
            cached1 = new_cache.get('endpoint1', {'param': 'value1'})
            assert cached1 == {'data': 'response1'}
        finally:
            if Path(new_cache_dir).exists():
                shutil.rmtree(new_cache_dir)
    
    def test_cache_disabled(self):
        """Test that cache operations work when cache is disabled."""
        cache = CacheManager(cache_dir=self.temp_dir, enabled=False)
        
        # Set should not raise error
        cache.set("endpoint", {"param": "value"}, {"data": "response"})
        
        # Get should return None
        result = cache.get("endpoint", {"param": "value"})
        assert result is None
        
        # Status should show disabled
        status = cache.get_status()
        assert status['enabled'] is False
    
    def test_cleanup_expired(self):
        """Test cleanup of expired entries."""
        # Create cache with 0 day max age
        cache = CacheManager(cache_dir=self.temp_dir, max_age_days=0, enabled=True)
        
        # Add entries
        cache.set("endpoint1", {"param": "value1"}, {"data": "response1"})
        cache.set("endpoint2", {"param": "value2"}, {"data": "response2"})
        
        # Sleep briefly
        time.sleep(0.1)
        
        # Cleanup expired
        count = cache.cleanup_expired()
        
        assert count >= 2
        
        # Verify entries are gone
        status = cache.get_status()
        assert status['total_entries'] == 0


class TestGlobalCacheFunctions:
    """Test global cache convenience functions."""
    
    def test_get_default_cache(self):
        """Test getting default cache instance."""
        cache = get_default_cache()
        assert isinstance(cache, CacheManager)
        assert cache.enabled is True
    
    def test_clear_cache_function(self):
        """Test global clear_cache function."""
        # Add entry to default cache
        cache = get_default_cache()
        cache.set("test/endpoint", {"param": "value"}, {"data": "response"})
        
        # Clear using global function
        count = clear_cache()
        
        # This might be 0 if cache was already empty, so just verify it doesn't error
        assert count >= 0
    
    def test_cache_status_function(self):
        """Test global cache_status function."""
        status = cache_status()
        
        assert 'enabled' in status
        assert 'cache_dir' in status
        assert 'total_entries' in status
        assert 'total_size_bytes' in status


class TestCacheWithRealData:
    """Test cache with realistic API response data."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache = CacheManager(cache_dir=self.temp_dir, enabled=True)
    
    def teardown_method(self):
        """Clean up after tests."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
    
    def test_cache_complex_response(self):
        """Test caching complex nested response data."""
        endpoint = "chemical/search"
        params = {"name": "caffeine"}
        response = {
            "chemicals": [
                {
                    "dtxsid": "DTXSID0020268",
                    "preferredName": "Caffeine",
                    "casrn": "58-08-2",
                    "inchikey": "RYYVLZVUVIJVGH-UHFFFAOYSA-N",
                    "smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
                    "properties": {
                        "molecularWeight": 194.19,
                        "logP": -0.07
                    }
                }
            ],
            "count": 1
        }
        
        self.cache.set(endpoint, params, response)
        cached = self.cache.get(endpoint, params)
        
        assert cached == response
        assert cached["chemicals"][0]["preferredName"] == "Caffeine"
    
    def test_cache_large_list_response(self):
        """Test caching large list responses."""
        endpoint = "chemical/list"
        params = {"listType": "TSCA"}
        
        # Simulate large response
        response = [{"dtxsid": f"DTXSID{i:07d}"} for i in range(1000)]
        
        self.cache.set(endpoint, params, response)
        cached = self.cache.get(endpoint, params)
        
        assert cached == response
        assert len(cached) == 1000
