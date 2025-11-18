"""
Test script for ProductData class.

This script demonstrates basic usage of the ProductData API client
and tests various methods for retrieving product data.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pycomptox.exposure import ProductData


def test_products_data_by_dtxsid():
    """Test product data by DTXSID."""
    
    print("="*70)
    print("Test 1: Get Product Data by DTXSID")
    print("="*70)
    
    try:
        client = ProductData()
        print("✓ ProductData client initialized successfully\n")
        
        # Test with a common chemical
        dtxsid = "DTXSID0020232"
        print(f"Fetching product data for {dtxsid}...")
        
        data = client.products_data_by_dtxsid(dtxsid)
        
        if data:
            print(f"✓ Retrieved product data")
            if isinstance(data, list):
                print(f"  Found {len(data)} product records")
                if len(data) > 0:
                    print(f"  Sample fields: {list(data[0].keys())[:5]}")
        else:
            print("✗ No data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_list_all_puc():
    """Test list all PUC product data."""
    
    print("="*70)
    print("Test 2: Get All PUC Product Data")
    print("="*70)
    
    try:
        client = ProductData()
        
        print("Fetching all PUC product data...")
        
        data = client.list_all_puc_product()
        
        if data:
            print(f"✓ Retrieved PUC data")
            if isinstance(data, list):
                print(f"  Found {len(data)} PUC records")
        else:
            print("✗ No data returned")
            
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_batch_operation():
    """Test batch operation for multiple DTXSIDs."""
    
    print("="*70)
    print("Test 3: Batch Product Data by DTXSIDs")
    print("="*70)
    
    try:
        client = ProductData()
        
        dtxsid_list = ["DTXSID0020232", "DTXSID7020182"]
        print(f"Fetching product data for {len(dtxsid_list)} chemicals...")
        
        data = client.product_data_by_dtxsid_batch(dtxsid_list)
        
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
        client = ProductData()
        
        # Test with empty string
        print("Testing with empty DTXSID...")
        try:
            client.products_data_by_dtxsid("")
            print("✗ Should have raised ValueError")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
        
        # Test batch with empty list
        print("\nTesting batch with empty list...")
        try:
            client.product_data_by_dtxsid_batch([])
            print("✗ Should have raised ValueError")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
            
    except Exception as e:
        print(f"✗ Unexpected error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    test_products_data_by_dtxsid()
    test_list_all_puc()
    test_batch_operation()
    test_input_validation()
    print("\n" + "="*70)
    print("All ProductData tests completed!")
    print("="*70)
