"""
Test script for DemographicExposure class.

This script demonstrates basic usage of the DemographicExposure API client
and tests various methods for retrieving demographic exposure prediction data.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pycomptox.exposure import DemographicExposure


def test_demographic_prediction_by_dtxsid():
    """Test demographic SEEM prediction by DTXSID."""
    
    print("="*70)
    print("Test 1: Get Demographic SEEM Prediction by DTXSID")
    print("="*70)
    
    try:
        client = DemographicExposure()
        print("✓ DemographicExposure client initialized successfully\n")
        
        # Test with a common chemical
        dtxsid = "DTXSID0020232"
        print(f"Fetching demographic SEEM prediction for {dtxsid}...")
        
        data = client.prediction_SEEMs_data_by_dtxsid(dtxsid)
        
        if data:
            print(f"✓ Retrieved demographic prediction data")
            if isinstance(data, list):
                print(f"  Found {len(data)} prediction records")
                if len(data) > 0:
                    print(f"  Sample fields: {list(data[0].keys())[:5]}")
        else:
            print("✗ No data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_with_projection():
    """Test with custom projection parameter."""
    
    print("="*70)
    print("Test 2: Test with Projection Parameter")
    print("="*70)
    
    try:
        client = DemographicExposure()
        
        dtxsid = "DTXSID0020232"
        projection = "ccd-demographic"
        print(f"Fetching prediction for {dtxsid} with projection: {projection}...")
        
        data = client.prediction_SEEMs_data_by_dtxsid(dtxsid, projection=projection)
        
        if data:
            print(f"✓ Retrieved prediction data with projection")
            if isinstance(data, list):
                print(f"  Found {len(data)} records")
        else:
            print("✗ No data returned")
            
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_batch_operation():
    """Test batch operation for multiple DTXSIDs."""
    
    print("="*70)
    print("Test 3: Batch Demographic SEEM Prediction by DTXSIDs")
    print("="*70)
    
    try:
        client = DemographicExposure()
        
        dtxsid_list = ["DTXSID0020232", "DTXSID0020267"]
        print(f"Fetching demographic predictions for {len(dtxsid_list)} chemicals...")
        
        data = client.prediction_SEEMs_data_by_dtxsid_batch(dtxsid_list)
        
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
        client = DemographicExposure()
        
        # Test with empty string
        print("Testing with empty DTXSID...")
        try:
            client.prediction_SEEMs_data_by_dtxsid("")
            print("✗ Should have raised ValueError")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
        
        # Test batch with empty list
        print("\nTesting batch with empty list...")
        try:
            client.prediction_SEEMs_data_by_dtxsid_batch([])
            print("✗ Should have raised ValueError")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
            
    except Exception as e:
        print(f"✗ Unexpected error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    test_demographic_prediction_by_dtxsid()
    test_with_projection()
    test_batch_operation()
    test_input_validation()
    print("\n" + "="*70)
    print("All DemographicExposure tests completed!")
    print("="*70)
