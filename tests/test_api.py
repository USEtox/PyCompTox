"""
Test script for PyCompTox Chemical Search API.
This script demonstrates basic functionality and automatic API key loading.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pycomptox.chemical import Chemical


def test_api_connection():
    """Test basic API connection and functionality."""
    
    print("Initializing Chemical client (loading API key automatically)...")
    try:
        client = Chemical()  # API key will be loaded automatically
        print("✓ Client initialized successfully\n")
    except ValueError as e:
        print(f"✗ Error: {e}\n")
        print("Please set up your API key first:")
        print("  pycomptox-setup set YOUR_API_KEY")
        return
    
    # Test 1: Simple search
    print("Test 1: Searching for 'DTXSID7020182'...")
    try:
        results = client.search_by_exact_value("DTXSID7020182")
        if results:
            print(f"✓ Found chemical: {results[0]['preferredName']}")
            print(f"  DTXSID: {results[0]['dtxsid']}")
            print(f"  CAS RN: {results[0]['casrn']}")
        else:
            print("✗ No results found")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Formula search
    print("Test 2: Searching by formula 'C15H16O2'...")
    try:
        dtxsids = client.search_by_msready_formula("C15H16O2")
        print(f"✓ Found {len(dtxsids)} chemicals")
        if len(dtxsids) > 0:
            print(f"  First 3 DTXSIDs: {dtxsids[:3]}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: Substring search
    print("Test 3: Searching for chemicals containing 'Bisphenol'...")
    try:
        results = client.search_by_substring_value("Bisphenol")
        print(f"✓ Found {len(results)} chemicals")
        if len(results) > 0:
            print("  First 3 results:")
            for i, chem in enumerate(results[:3], 1):
                print(f"    {i}. {chem['preferredName']} ({chem['dtxsid']})")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "="*50)
    print("\nAll tests completed!")


def test_rate_limiting():
    """Test rate limiting functionality."""
    print("\n" + "="*50)
    print("Testing Rate Limiting")
    print("="*50 + "\n")
    
    print("Creating client with 0.5 second delay between calls...")
    client = Chemical(time_delay_between_calls=0.5)
    
    import time
    start_time = time.time()
    
    print("Making 3 consecutive API calls...")
    for i in range(3):
        call_start = time.time()
        try:
            client.search_by_exact_value(f"DTXSID702018{i}")
        except:
            pass  # Ignore errors for this test
        elapsed = time.time() - call_start
        print(f"  Call {i+1}: {elapsed:.3f} seconds")
    
    total_time = time.time() - start_time
    print(f"\nTotal time for 3 calls: {total_time:.3f} seconds")
    print(f"Expected minimum time: ~1.0 seconds (2 delays of 0.5s)")
    
    if total_time >= 1.0:
        print("✓ Rate limiting is working correctly!")
    else:
        print("⚠ Rate limiting may not be working as expected")


if __name__ == "__main__":
    print("=" * 60)
    print("PyCompTox Test Suite")
    print("=" * 60)
    print()
    
    # Run basic tests
    test_api_connection()
    
    # Optionally run rate limiting test
    if len(sys.argv) > 1 and sys.argv[1] == "--test-rate-limit":
        test_rate_limiting()
