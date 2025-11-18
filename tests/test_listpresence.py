"""
Test script for ListPresence class.

This script demonstrates basic usage of the ListPresence API client
and tests various methods for retrieving list presence data.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pycomptox.exposure import ListPresence


def test_list_presence_tags():
    """Test get all list presence tags."""
    
    print("="*70)
    print("Test 1: Get All List Presence Tags")
    print("="*70)
    
    try:
        client = ListPresence()
        print("✓ ListPresence client initialized successfully\n")
        
        print("Fetching all list presence tags...")
        
        data = client.list_presence_tags()
        
        if data:
            print(f"✓ Retrieved tags")
            if isinstance(data, list):
                print(f"  Found {len(data)} tags")
                if len(data) > 0:
                    print(f"  Sample fields: {list(data[0].keys())[:5]}")
        else:
            print("✗ No data returned")
            
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_list_presence_by_dtxsid():
    """Test list presence data by DTXSID."""
    
    print("="*70)
    print("Test 2: Get List Presence Data by DTXSID")
    print("="*70)
    
    try:
        client = ListPresence()
        
        # Test with a common chemical
        dtxsid = "DTXSID0020232"
        print(f"Fetching list presence data for {dtxsid}...")
        
        data = client.list_presence_data_by_dtxsid(dtxsid)
        
        if data:
            print(f"✓ Retrieved list presence data")
            if isinstance(data, list):
                print(f"  Found {len(data)} list presence records")
        else:
            print("✗ No data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_batch_operation():
    """Test batch operation for multiple DTXSIDs."""
    
    print("="*70)
    print("Test 3: Batch List Presence by DTXSIDs")
    print("="*70)
    
    try:
        client = ListPresence()
        
        dtxsids = ["DTXSID0020232", "DTXSID0020245"]
        print(f"Fetching list presence data for {len(dtxsids)} chemicals...")
        
        data = client.list_presence_data_by_dtxsid_batch(dtxsids)
        
        if data:
            print(f"✓ Retrieved batch data")
            if isinstance(data, list):
                print(f"  Found {len(data)} records")
        else:
            print("✗ No data returned")
            
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_input_validation():
    """Test input validation."""
    
    print("="*70)
    print("Test 4: Input Validation")
    print("="*70)
    
    try:
        client = ListPresence()
        
        # Test with empty string
        print("Testing with empty DTXSID...")
        try:
            client.list_presence_data_by_dtxsid("")
            print("✗ Should have raised ValueError")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
        
        # Test batch with empty list
        print("\nTesting batch with empty list...")
        try:
            client.list_presence_data_by_dtxsid_batch([])
            print("✗ Should have raised ValueError")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
            
    except Exception as e:
        print(f"✗ Unexpected error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    test_list_presence_tags()
    test_list_presence_by_dtxsid()
    test_batch_operation()
    test_input_validation()
    print("\n" + "="*70)
    print("All ListPresence tests completed!")
    print("="*70)
