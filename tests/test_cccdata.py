"""
Test script for CCCData class.

This script demonstrates basic usage of the CCCData API client
and tests various methods for retrieving Chemical and Products Categories data.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pycomptox.exposure import CCCData


def test_product_use_category():
    """Test product use category by DTXSID."""
    
    print("="*70)
    print("Test 1: Get Product Use Category by DTXSID")
    print("="*70)
    
    try:
        client = CCCData()
        print("✓ CCCData client initialized successfully\n")
        
        # Test with a common chemical
        dtxsid = "DTXSID7020182"  # Bisphenol A
        print(f"Fetching product use category for {dtxsid}...")
        
        data = client.product_use_category_by_dtxsid(dtxsid)
        
        if data:
            print(f"✓ Retrieved product use category data")
            if isinstance(data, list):
                print(f"  Found {len(data)} PUC records")
                if len(data) > 0:
                    print(f"  Sample record: {data[0]}")
            else:
                print(f"  Data type: {type(data)}")
        else:
            print("✗ No data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_production_volume():
    """Test production volume by DTXSID."""
    
    print("="*70)
    print("Test 2: Get Production Volume by DTXSID")
    print("="*70)
    
    try:
        client = CCCData()
        
        dtxsid = "DTXSID7020182"
        print(f"Fetching production volume for {dtxsid}...")
        
        data = client.production_volume_by_dtxsid(dtxsid)
        
        if data:
            print(f"✓ Retrieved production volume data")
            print(f"  Data type: {type(data)}")
            if isinstance(data, list) and len(data) > 0:
                print(f"  Found {len(data)} records")
        else:
            print("✗ No data returned")
            
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_input_validation():
    """Test input validation."""
    
    print("="*70)
    print("Test 3: Input Validation")
    print("="*70)
    
    try:
        client = CCCData()
        
        # Test with empty string
        print("Testing with empty DTXSID...")
        try:
            client.product_use_category_by_dtxsid("")
            print("✗ Should have raised ValueError")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
        
        # Test with None
        print("\nTesting with None DTXSID...")
        try:
            client.product_use_category_by_dtxsid(None)
            print("✗ Should have raised ValueError")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
            
    except Exception as e:
        print(f"✗ Unexpected error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    test_product_use_category()
    test_production_volume()
    test_input_validation()
    print("\n" + "="*70)
    print("All CCCData tests completed!")
    print("="*70)
