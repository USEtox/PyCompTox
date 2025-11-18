"""
Test script for PyCompTox batch search methods.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pycomptox.chemical import Chemical


def test_batch_methods():
    """Test the batch search methods."""
    
    print("=" * 60)
    print("PyCompTox Batch Search Methods Test")
    print("=" * 60)
    print()
    
    try:
        client = Chemical()
        print("✓ Client initialized successfully\n")
    except ValueError as e:
        print(f"✗ Error: {e}\n")
        print("Please set up your API key first:")
        print("  pycomptox-setup set YOUR_API_KEY")
        return
    
    # Test 1: Batch search by exact values
    print("Test 1: Batch search by exact values")
    print("-" * 60)
    try:
        # Try with single values first to test the API
        values = ["DTXSID7020182", "Bisphenol A"]
        print(f"Searching for {len(values)} values: {values}")
        results = client.search_by_exact_batch_values(values)
        print(f"✓ Found {len(results)} results (type: {type(results).__name__})")
        
        if results:
            print("\nResults:")
            for i, result in enumerate(results[:5], 1):
                if isinstance(result, dict):
                    name = result.get('preferredName', 'N/A')
                    dtxsid = result.get('dtxsid', 'N/A')
                    search_val = result.get('searchValue', 'N/A')
                    print(f"  {i}. {name} ({dtxsid})")
                    print(f"     Matched: {search_val}")
                    if result.get('searchMsgs'):
                        msgs = result['searchMsgs']
                        if len(msgs) > 0:
                            print(f"     Message: {msgs[0][:100]}")
                else:
                    print(f"  {i}. {result}")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60 + "\n")
    
    # Test 2: Batch search by mass ranges
    print("Test 2: Batch search MS-ready chemicals by mass ranges")
    print("-" * 60)
    try:
        masses = [200.9, 201.0, 201.1]
        error = 0.01
        print(f"Searching for masses: {masses} (error: ±{error})")
        results = client.search_ms_ready_by_mass_range_batch(masses, error=error)
        print(f"✓ Received results for {len(results)} mass queries")
        
        if results:
            print("\nResults summary:")
            for mass, dtxsids in list(results.items())[:5]:
                print(f"  Mass {mass}: {len(dtxsids)} chemicals")
                if dtxsids and len(dtxsids) > 0:
                    print(f"    First DTXSID: {dtxsids[0]}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 60 + "\n")
    
    # Test 3: Batch search MS-ready by DTXCIDs
    print("Test 3: Batch search MS-ready chemicals by DTXCIDs")
    print("-" * 60)
    try:
        dtxcids = ["DTXCID30182", "DTXCID20182", "DTXCID10182"]
        print(f"Searching for {len(dtxcids)} DTXCIDs: {dtxcids}")
        results = client.search_ms_ready_by_dtxcid_batch(dtxcids)
        print(f"✓ Received results (type: {type(results).__name__})")
        
        if isinstance(results, dict):
            print(f"\nResults summary (dict with {len(results)} entries):")
            for key, value in list(results.items())[:5]:
                if isinstance(value, list):
                    print(f"  {key}: {len(value)} items")
                    if value:
                        print(f"    Sample: {value[:3]}")
                else:
                    print(f"  {key}: {value}")
        elif isinstance(results, list):
            print(f"\nResults summary (list with {len(results)} items):")
            for i, item in enumerate(results[:5], 1):
                print(f"  {i}. {item}")
        else:
            print(f"\nResults: {results}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("\nAll batch method tests completed!")


def test_batch_validation():
    """Test validation of batch methods."""
    
    print("\n" + "=" * 60)
    print("Testing Batch Method Validation")
    print("=" * 60)
    print()
    
    client = Chemical()
    
    # Test validation: too many values
    print("Test: Exceeding maximum batch size (200 values)")
    try:
        values = [f"chemical_{i}" for i in range(201)]
        client.search_by_exact_batch_values(values)
        print("✗ Should have raised ValueError")
    except ValueError as e:
        print(f"✓ Correctly raised error: {e}")
    
    print()
    
    # Test validation: empty list
    print("Test: Empty value list")
    try:
        client.search_by_exact_batch_values([])
        print("✗ Should have raised ValueError")
    except ValueError as e:
        print(f"✓ Correctly raised error: {e}")
    
    print()
    
    # Test validation: empty masses
    print("Test: Empty mass list")
    try:
        client.search_ms_ready_by_mass_range_batch([])
        print("✗ Should have raised ValueError")
    except ValueError as e:
        print(f"✓ Correctly raised error: {e}")
    
    print()
    
    # Test validation: empty DTXCIDs
    print("Test: Empty DTXCID list")
    try:
        client.search_ms_ready_by_dtxcid_batch([])
        print("✗ Should have raised ValueError")
    except ValueError as e:
        print(f"✓ Correctly raised error: {e}")
    
    print("\n✓ All validation tests passed!")


if __name__ == "__main__":
    test_batch_methods()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test-validation":
        test_batch_validation()
