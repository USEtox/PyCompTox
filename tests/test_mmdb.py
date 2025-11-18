"""
Test script for MMDB class.

This script demonstrates basic usage of the MMDB API client
and tests various methods for retrieving Molecular Modeling Database data.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pycomptox.exposure import MMDB


def test_harmonized_single_sample_by_medium():
    """Test harmonized single-sample by medium."""
    
    print("="*70)
    print("Test 1: Get Harmonized Single-Sample by Medium")
    print("="*70)
    
    try:
        client = MMDB()
        print("✓ MMDB client initialized successfully\n")
        
        # Test with surface water
        medium = "surface water"
        print(f"Fetching single-sample data for medium: {medium}...")
        
        data = client.harmonized_single_sample_by_medium(medium)
        
        if data:
            print(f"✓ Retrieved single-sample data")
            if isinstance(data, dict):
                print(f"  Response keys: {list(data.keys())}")
                if 'data' in data and isinstance(data['data'], list):
                    print(f"  Found {len(data['data'])} sample records")
        else:
            print("✗ No data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_pagination():
    """Test pagination with page_number parameter."""
    
    print("="*70)
    print("Test 2: Test Pagination")
    print("="*70)
    
    try:
        client = MMDB()
        
        medium = "surface water"
        page_number = 2
        print(f"Fetching page {page_number} for medium: {medium}...")
        
        data = client.harmonized_single_sample_by_medium(medium, page_number=page_number)
        
        if data:
            print(f"✓ Retrieved page {page_number}")
            if isinstance(data, dict):
                print(f"  Response type: {type(data)}")
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
        client = MMDB()
        
        # Test with empty string
        print("Testing with empty medium...")
        try:
            client.harmonized_single_sample_by_medium("")
            print("✗ Should have raised ValueError")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
        
        # Test with invalid page number
        print("\nTesting with invalid page_number...")
        try:
            client.harmonized_single_sample_by_medium("surface water", page_number=0)
            print("✗ Should have raised ValueError")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
            
    except Exception as e:
        print(f"✗ Unexpected error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    test_harmonized_single_sample_by_medium()
    test_pagination()
    test_input_validation()
    print("\n" + "="*70)
    print("All MMDB tests completed!")
    print("="*70)
