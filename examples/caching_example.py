"""
Example demonstrating the caching system in PyCompTox.

This script shows how to:
1. Use automatic caching
2. Measure performance improvements
3. Manage cache (status, clear, export/import)
4. Configure cache settings
"""

import time
from pycomptox import chemical, cache_status, clear_cache, export_cache, import_cache


def demonstrate_basic_caching():
    """Demonstrate basic caching functionality."""
    print("=" * 70)
    print("1. BASIC CACHING")
    print("=" * 70)
    
    chem = chemical.Chemical()
    
    # Clear cache for demo
    clear_cache("chemical/search")
    
    print("\nSearching for 'caffeine' (first time - will cache)...")
    start = time.time()
    results1 = chem.search_by_starting_value("caffeine")
    time1 = time.time() - start
    
    if results1:
        print(f"Found: {results1[0].get('preferredName', 'N/A')}")
        print(f"DTXSID: {results1[0].get('dtxsid', 'N/A')}")
    print(f"Time: {time1:.3f} seconds")
    
    print("\nSearching for 'caffeine' again (from cache)...")
    start = time.time()
    results2 = chem.search_by_starting_value("caffeine")
    time2 = time.time() - start
    
    print(f"Found: {results2[0].get('preferredName', 'N/A')}")
    print(f"Time: {time2:.3f} seconds")
    print(f"Speedup: {time1/time2:.1f}x faster!")


def demonstrate_cache_bypass():
    """Demonstrate bypassing the cache."""
    print("\n" + "=" * 70)
    print("2. BYPASSING CACHE")
    print("=" * 70)
    
    chem = chemical.Chemical()
    
    print("\nGetting data WITH cache...")
    start = time.time()
    results1 = chem.search_by_starting_value("benzene", use_cache=True)
    time1 = time.time() - start
    print(f"Time: {time1:.3f} seconds")
    
    print("\nGetting data WITHOUT cache (fresh from API)...")
    start = time.time()
    results2 = chem.search_by_starting_value("benzene", use_cache=False)
    time2 = time.time() - start
    print(f"Time: {time2:.3f} seconds")


def demonstrate_cache_status():
    """Demonstrate cache status and statistics."""
    print("\n" + "=" * 70)
    print("3. CACHE STATUS")
    print("=" * 70)
    
    status = cache_status()
    
    print(f"\nCache enabled: {status['enabled']}")
    print(f"Cache directory: {status['cache_dir']}")
    print(f"Max age (days): {status['max_age_days'] or 'Unlimited'}")
    print(f"\nTotal entries: {status['total_entries']}")
    print(f"Total size: {status['total_size_mb']} MB ({status['total_size_bytes']:,} bytes)")
    
    if status['endpoints']:
        print("\nEntries by endpoint:")
        for endpoint, count in sorted(status['endpoints'].items()):
            print(f"  {endpoint}: {count} entries")
    
    if status['oldest_entry']:
        print(f"\nOldest entry: {status['oldest_entry']}")
    if status['newest_entry']:
        print(f"Newest entry: {status['newest_entry']}")


def demonstrate_cache_export_import():
    """Demonstrate cache export and import."""
    print("\n" + "=" * 70)
    print("4. CACHE EXPORT/IMPORT")
    print("=" * 70)
    
    import tempfile
    import os
    
    # Export cache
    export_file = os.path.join(tempfile.gettempdir(), "pycomptox_cache_export.json")
    
    print(f"\nExporting cache to: {export_file}")
    result = export_cache(export_file)
    
    if result.get('success'):
        print(f"✓ Exported {result['entries_exported']} entries")
        print(f"  File size: {result['file_size_mb']} MB")
        
        # Show how to import (but don't actually do it to avoid duplicates)
        print(f"\nTo import this cache later:")
        print(f"  from pycomptox import import_cache")
        print(f"  result = import_cache('{export_file}')")
        
        # Clean up
        if os.path.exists(export_file):
            os.remove(export_file)
            print(f"\n(Export file removed for demo cleanup)")
    else:
        print(f"✗ Export failed: {result.get('message')}")


def demonstrate_cache_clearing():
    """Demonstrate cache clearing."""
    print("\n" + "=" * 70)
    print("5. CACHE CLEARING")
    print("=" * 70)
    
    # Get initial status
    status_before = cache_status()
    print(f"\nCache entries before: {status_before['total_entries']}")
    
    # Clear specific endpoint
    if status_before['total_entries'] > 0:
        endpoints = list(status_before['endpoints'].keys())
        if endpoints:
            endpoint_to_clear = endpoints[0]
            print(f"\nClearing cache for: {endpoint_to_clear}")
            count = clear_cache(endpoint_to_clear)
            print(f"Cleared {count} entries")
    
    # Show updated status
    status_after = cache_status()
    print(f"\nCache entries after: {status_after['total_entries']}")


def demonstrate_performance_comparison():
    """Demonstrate performance benefits of caching."""
    print("\n" + "=" * 70)
    print("6. PERFORMANCE COMPARISON")
    print("=" * 70)
    
    chem = chemical.Chemical()
    chemicals = ["caffeine", "benzene", "toluene", "aspirin", "ethanol"]
    
    # Clear cache for fair comparison
    clear_cache("chemical/search")
    
    print("\nFirst pass (populating cache)...")
    times_uncached = []
    for name in chemicals:
        start = time.time()
        chem.search_by_starting_value(name)
        elapsed = time.time() - start
        times_uncached.append(elapsed)
        print(f"  {name}: {elapsed:.3f}s")
    
    print("\nSecond pass (from cache)...")
    times_cached = []
    for name in chemicals:
        start = time.time()
        chem.search_by_starting_value(name)
        elapsed = time.time() - start
        times_cached.append(elapsed)
        print(f"  {name}: {elapsed:.3f}s")
    
    avg_uncached = sum(times_uncached) / len(times_uncached)
    avg_cached = sum(times_cached) / len(times_cached)
    
    print(f"\nAverage time (uncached): {avg_uncached:.3f}s")
    print(f"Average time (cached): {avg_cached:.3f}s")
    print(f"Speedup: {avg_uncached/avg_cached:.1f}x faster")


def demonstrate_custom_cache_config():
    """Demonstrate custom cache configuration."""
    print("\n" + "=" * 70)
    print("7. CUSTOM CACHE CONFIGURATION")
    print("=" * 70)
    
    from pycomptox import CacheManager
    import tempfile
    
    # Create custom cache with expiration
    custom_cache_dir = tempfile.mkdtemp()
    
    custom_cache = CacheManager(
        cache_dir=custom_cache_dir,
        max_age_days=7,  # Expire after 7 days
        enabled=True
    )
    
    print(f"\nCreated custom cache:")
    print(f"  Location: {custom_cache_dir}")
    print(f"  Max age: 7 days")
    
    # Use custom cache with client
    chem = chemical.Chemical(cache_manager=custom_cache)
    
    print("\nUsing custom cache for searches...")
    chem.search_by_starting_value("acetone")
    
    status = custom_cache.get_status()
    print(f"  Entries in custom cache: {status['total_entries']}")
    
    # Cleanup
    import shutil
    shutil.rmtree(custom_cache_dir)
    print(f"\n(Custom cache directory cleaned up)")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("PyCompTox Caching System Demonstration")
    print("=" * 70)
    
    try:
        demonstrate_basic_caching()
        demonstrate_cache_bypass()
        demonstrate_cache_status()
        demonstrate_cache_export_import()
        demonstrate_cache_clearing()
        demonstrate_performance_comparison()
        demonstrate_custom_cache_config()
        
        print("\n" + "=" * 70)
        print("Demonstration Complete!")
        print("=" * 70)
        print("\nKey takeaways:")
        print("  • Caching is automatic and enabled by default")
        print("  • Provides 100-1000x speedup for repeated requests")
        print("  • Use use_cache=False to bypass when needed")
        print("  • Monitor with cache_status() to manage size")
        print("  • Export/import for sharing or backup")
        print("\nFor more information, see: docs/CACHING.md")
        
    except Exception as e:
        print(f"\n✗ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
