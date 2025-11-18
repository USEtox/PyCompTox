"""
Test script for FunctionalUse class.

This script demonstrates basic usage of the FunctionalUse API client
and tests various methods for retrieving functional use data.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pycomptox.exposure import FunctionalUse


def test_functional_use_by_dtxsid():
    """Test functional use by DTXSID."""
    
    print("="*70)
    print("Test 1: Get Functional Use by DTXSID")
    print("="*70)
    
    try:
        client = FunctionalUse()
        print("✓ FunctionalUse client initialized successfully\n")
        
        # Test with a common chemical
        dtxsid = "DTXSID0020232"
        print(f"Fetching functional use data for {dtxsid}...")
        
        data = client.functiona_use_by_dtxsid(dtxsid)
        
        if data:
            print(f"✓ Retrieved functional use data")
            if isinstance(data, list):
                print(f"  Found {len(data)} functional use records")
                if len(data) > 0:
                    print(f"  Sample fields: {list(data[0].keys())[:5]}")
        else:
            print("✗ No data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_functional_use_probability():
    """Test functional use probability by DTXSID."""
    
    print("="*70)
    print("Test 2: Get Functional Use Probability by DTXSID")
    print("="*70)
    
    try:
        client = FunctionalUse()
        
        dtxsid = "DTXSID0020232"
        print(f"Fetching functional use probability for {dtxsid}...")
        
        data = client.functional_use_probability_by_dtxsid(dtxsid)
        
        if data:
            print(f"✓ Retrieved probability data")
            if isinstance(data, list):
                print(f"  Found {len(data)} probability records")
        else:
            print("✗ No data returned")
            
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_functional_use_categories():
    """Test get all functional use categories."""
    
    print("="*70)
    print("Test 3: Get All Functional Use Categories")
    print("="*70)
    
    try:
        client = FunctionalUse()
        
        print("Fetching all functional use categories...")
        
        data = client.functiona_use_categories()
        
        if data:
            print(f"✓ Retrieved categories")
            if isinstance(data, list):
                print(f"  Found {len(data)} categories")
        else:
            print("✗ No data returned")
            
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_batch_operation():
    """Test batch operation for multiple DTXSIDs."""
    
    print("="*70)
    print("Test 4: Batch Functional Use by DTXSIDs")
    print("="*70)
    
    try:
        client = FunctionalUse()
        
        dtxsids = ["DTXSID0020232", "DTXSID7020182"]
        print(f"Fetching functional use data for {len(dtxsids)} chemicals...")
        
        data = client.functional_use_by_dtxsid_batch(dtxsids)
        
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
    print("Test 5: Input Validation")
    print("="*70)
    
    try:
        client = FunctionalUse()
        
        # Test with empty string
        print("Testing with empty DTXSID...")
        try:
            client.functiona_use_by_dtxsid("")
            print("✗ Should have raised ValueError")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
        
        # Test batch with empty list
        print("\nTesting batch with empty list...")
        try:
            client.functional_use_by_dtxsid_batch([])
            print("✗ Should have raised ValueError")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
            
    except Exception as e:
        print(f"✗ Unexpected error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    test_functional_use_by_dtxsid()
    test_functional_use_probability()
    test_functional_use_categories()
    test_batch_operation()
    test_input_validation()
    print("\n" + "="*70)
    print("All FunctionalUse tests completed!")
    print("="*70)
