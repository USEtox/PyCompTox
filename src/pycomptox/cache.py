"""
Cache management for PyCompTox API requests.

This module provides a flexible caching system for API responses to reduce
network traffic and improve performance. The cache uses a file-based storage
system with JSON serialization.

Features:
    - Unlimited cache size by default
    - Automatic cache invalidation based on age
    - Export/import functionality for cache portability
    - Cache statistics and management
    - Per-request cache control

Author: PyCompTox Contributors
License: MIT
"""

import os
import json
import hashlib
import time
from pathlib import Path
from typing import Any, Dict, Optional, List
from datetime import datetime, timedelta
import shutil


class CacheManager:
    """
    Manages caching of API responses to disk.
    
    The cache is organized by API endpoint and request parameters, with each
    cached response stored as a separate JSON file. This allows for efficient
    lookups and easy management.
    
    Args:
        cache_dir (str, optional): Directory for cache storage. If not provided,
            uses a default directory in the user's home folder.
        max_age_days (int, optional): Maximum age of cache entries in days.
            Entries older than this are considered stale. None means no expiration.
            Default is None (unlimited).
        enabled (bool): Whether caching is enabled. Default is True.
    
    Example:
        >>> cache = CacheManager()
        >>> # Cache a response
        >>> cache.set("chemical/search", {"name": "benzene"}, {"dtxsid": "DTXSID..."})
        >>> # Retrieve from cache
        >>> result = cache.get("chemical/search", {"name": "benzene"})
    """
    
    def __init__(
        self,
        cache_dir: Optional[str] = None,
        max_age_days: Optional[int] = None,
        enabled: bool = True
    ):
        """Initialize the cache manager."""
        if cache_dir is None:
            # Use default cache directory in user's home
            home = Path.home()
            cache_dir = home / ".pycomptox" / "cache"
        
        self.cache_dir = Path(cache_dir)
        self.max_age_days = max_age_days
        self.enabled = enabled
        
        # Create cache directory if it doesn't exist
        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _generate_key(self, endpoint: str, params: Dict[str, Any]) -> str:
        """
        Generate a unique cache key for an endpoint and parameters.
        
        Args:
            endpoint: API endpoint identifier
            params: Request parameters
        
        Returns:
            A unique hash key for this request
        """
        # Create a stable string representation of the request
        params_str = json.dumps(params, sort_keys=True)
        key_str = f"{endpoint}:{params_str}"
        
        # Generate SHA256 hash
        return hashlib.sha256(key_str.encode()).hexdigest()
    
    def _get_cache_file(self, endpoint: str, params: Dict[str, Any]) -> Path:
        """
        Get the cache file path for an endpoint and parameters.
        
        Args:
            endpoint: API endpoint identifier
            params: Request parameters
        
        Returns:
            Path to the cache file
        """
        # Create subdirectory for endpoint
        endpoint_dir = self.cache_dir / endpoint.replace("/", "_")
        endpoint_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename from hash
        key = self._generate_key(endpoint, params)
        return endpoint_dir / f"{key}.json"
    
    def get(self, endpoint: str, params: Dict[str, Any]) -> Optional[Any]:
        """
        Retrieve a cached response.
        
        Args:
            endpoint: API endpoint identifier
            params: Request parameters
        
        Returns:
            Cached response data if found and valid, None otherwise
        """
        if not self.enabled:
            return None
        
        cache_file = self._get_cache_file(endpoint, params)
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            # Check if cache is expired
            if self.max_age_days is not None:
                cached_time = datetime.fromisoformat(cached_data['timestamp'])
                max_age = timedelta(days=self.max_age_days)
                
                if datetime.now() - cached_time > max_age:
                    # Cache expired, delete it
                    cache_file.unlink()
                    return None
            
            return cached_data['response']
        
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # Corrupted cache file, delete it
            cache_file.unlink()
            return None
    
    def set(self, endpoint: str, params: Dict[str, Any], response: Any) -> None:
        """
        Store a response in the cache.
        
        Args:
            endpoint: API endpoint identifier
            params: Request parameters
            response: Response data to cache
        """
        if not self.enabled:
            return
        
        cache_file = self._get_cache_file(endpoint, params)
        
        cached_data = {
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'params': params,
            'response': response
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cached_data, f, indent=2)
        except (IOError, TypeError) as e:
            # Silently fail on cache write errors
            pass
    
    def clear(self, endpoint: Optional[str] = None) -> int:
        """
        Clear cached entries.
        
        Args:
            endpoint: Optional endpoint to clear. If None, clears all cache.
        
        Returns:
            Number of entries cleared
        """
        if not self.enabled or not self.cache_dir.exists():
            return 0
        
        count = 0
        
        if endpoint is None:
            # Clear entire cache
            for item in self.cache_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                    count += 1
                elif item.is_file():
                    item.unlink()
                    count += 1
        else:
            # Clear specific endpoint
            endpoint_dir = self.cache_dir / endpoint.replace("/", "_")
            if endpoint_dir.exists():
                for cache_file in endpoint_dir.glob("*.json"):
                    cache_file.unlink()
                    count += 1
        
        return count
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get cache status information.
        
        Returns:
            Dictionary with cache statistics including:
                - enabled: Whether cache is enabled
                - cache_dir: Path to cache directory
                - total_entries: Total number of cached entries
                - total_size_bytes: Total size of cache in bytes
                - total_size_mb: Total size of cache in MB
                - endpoints: Dictionary of endpoint names and entry counts
                - oldest_entry: Timestamp of oldest cache entry
                - newest_entry: Timestamp of newest cache entry
        """
        status = {
            'enabled': self.enabled,
            'cache_dir': str(self.cache_dir),
            'max_age_days': self.max_age_days,
            'total_entries': 0,
            'total_size_bytes': 0,
            'total_size_mb': 0.0,
            'endpoints': {},
            'oldest_entry': None,
            'newest_entry': None
        }
        
        if not self.enabled or not self.cache_dir.exists():
            return status
        
        oldest = None
        newest = None
        
        # Scan cache directory
        for endpoint_dir in self.cache_dir.iterdir():
            if not endpoint_dir.is_dir():
                continue
            
            endpoint_name = endpoint_dir.name.replace("_", "/")
            entry_count = 0
            
            for cache_file in endpoint_dir.glob("*.json"):
                entry_count += 1
                status['total_entries'] += 1
                
                # Get file size
                file_size = cache_file.stat().st_size
                status['total_size_bytes'] += file_size
                
                # Get timestamps
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)
                        timestamp = datetime.fromisoformat(cached_data['timestamp'])
                        
                        if oldest is None or timestamp < oldest:
                            oldest = timestamp
                        if newest is None or timestamp > newest:
                            newest = timestamp
                except (json.JSONDecodeError, KeyError, ValueError):
                    pass
            
            if entry_count > 0:
                status['endpoints'][endpoint_name] = entry_count
        
        # Convert size to MB
        status['total_size_mb'] = round(status['total_size_bytes'] / (1024 * 1024), 2)
        
        # Format timestamps
        if oldest:
            status['oldest_entry'] = oldest.isoformat()
        if newest:
            status['newest_entry'] = newest.isoformat()
        
        return status
    
    def export_cache(self, export_path: str) -> Dict[str, Any]:
        """
        Export the entire cache to a single JSON file.
        
        Args:
            export_path: Path where to save the exported cache
        
        Returns:
            Dictionary with export statistics
        """
        if not self.enabled or not self.cache_dir.exists():
            return {'success': False, 'message': 'Cache is disabled or empty'}
        
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'max_age_days': self.max_age_days,
            'entries': []
        }
        
        entry_count = 0
        
        # Collect all cache entries
        for endpoint_dir in self.cache_dir.iterdir():
            if not endpoint_dir.is_dir():
                continue
            
            for cache_file in endpoint_dir.glob("*.json"):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)
                        export_data['entries'].append(cached_data)
                        entry_count += 1
                except (json.JSONDecodeError, IOError):
                    pass
        
        # Write export file
        export_path = Path(export_path)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)
        
        file_size = export_path.stat().st_size
        
        return {
            'success': True,
            'export_path': str(export_path),
            'entries_exported': entry_count,
            'file_size_bytes': file_size,
            'file_size_mb': round(file_size / (1024 * 1024), 2)
        }
    
    def import_cache(self, import_path: str, overwrite: bool = False) -> Dict[str, Any]:
        """
        Import cache from an exported JSON file.
        
        Args:
            import_path: Path to the exported cache file
            overwrite: Whether to overwrite existing cache entries
        
        Returns:
            Dictionary with import statistics
        """
        if not self.enabled:
            return {'success': False, 'message': 'Cache is disabled'}
        
        import_path = Path(import_path)
        
        if not import_path.exists():
            return {'success': False, 'message': f'Import file not found: {import_path}'}
        
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
        except json.JSONDecodeError as e:
            return {'success': False, 'message': f'Invalid JSON file: {e}'}
        
        imported = 0
        skipped = 0
        
        for entry in import_data.get('entries', []):
            endpoint = entry.get('endpoint')
            params = entry.get('params')
            response = entry.get('response')
            
            if not endpoint or params is None or response is None:
                skipped += 1
                continue
            
            cache_file = self._get_cache_file(endpoint, params)
            
            # Check if entry already exists
            if cache_file.exists() and not overwrite:
                skipped += 1
                continue
            
            # Import the entry
            try:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(entry, f, indent=2)
                imported += 1
            except IOError:
                skipped += 1
        
        return {
            'success': True,
            'import_path': str(import_path),
            'entries_imported': imported,
            'entries_skipped': skipped,
            'total_entries': len(import_data.get('entries', []))
        }
    
    def cleanup_expired(self) -> int:
        """
        Remove expired cache entries.
        
        Returns:
            Number of entries removed
        """
        if not self.enabled or self.max_age_days is None:
            return 0
        
        if not self.cache_dir.exists():
            return 0
        
        count = 0
        max_age = timedelta(days=self.max_age_days)
        now = datetime.now()
        
        for endpoint_dir in self.cache_dir.iterdir():
            if not endpoint_dir.is_dir():
                continue
            
            for cache_file in endpoint_dir.glob("*.json"):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)
                    
                    cached_time = datetime.fromisoformat(cached_data['timestamp'])
                    
                    if now - cached_time > max_age:
                        cache_file.unlink()
                        count += 1
                
                except (json.JSONDecodeError, KeyError, ValueError, IOError):
                    # Remove corrupted files
                    cache_file.unlink()
                    count += 1
        
        return count


# Global cache instance
_default_cache = None


def get_default_cache() -> CacheManager:
    """
    Get the default global cache instance.
    
    Returns:
        The default CacheManager instance
    """
    global _default_cache
    if _default_cache is None:
        _default_cache = CacheManager()
    return _default_cache


def set_default_cache(cache: CacheManager) -> None:
    """
    Set the default global cache instance.
    
    Args:
        cache: CacheManager instance to use as default
    """
    global _default_cache
    _default_cache = cache


def clear_cache(endpoint: Optional[str] = None) -> int:
    """
    Clear the default cache.
    
    Args:
        endpoint: Optional endpoint to clear. If None, clears all cache.
    
    Returns:
        Number of entries cleared
    """
    return get_default_cache().clear(endpoint)


def cache_status() -> Dict[str, Any]:
    """
    Get status of the default cache.
    
    Returns:
        Dictionary with cache statistics
    """
    return get_default_cache().get_status()


def export_cache(export_path: str) -> Dict[str, Any]:
    """
    Export the default cache to a file.
    
    Args:
        export_path: Path where to save the exported cache
    
    Returns:
        Dictionary with export statistics
    """
    return get_default_cache().export_cache(export_path)


def import_cache(import_path: str, overwrite: bool = False) -> Dict[str, Any]:
    """
    Import cache from a file into the default cache.
    
    Args:
        import_path: Path to the exported cache file
        overwrite: Whether to overwrite existing cache entries
    
    Returns:
        Dictionary with import statistics
    """
    return get_default_cache().import_cache(import_path, overwrite)
