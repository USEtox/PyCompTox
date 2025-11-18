"""
Test script for BioactivityData class.

This script demonstrates basic usage of the BioactivityData API client
and tests various methods for retrieving bioactivity data.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pycomptox.bioactivity import BioactivityData


def test_bioactivity_summary():
    """Test bioactivity summary methods."""
    
    print("="*70)
    print("Test 1: Get Summary by DTXSID")
    print("="*70)
    
    try:
        client = BioactivityData()
        print("✓ BioactivityData client initialized successfully\n")
        
        # Test with Bisphenol A
        dtxsid = "DTXSID7020182"
        print(f"Fetching bioactivity summary for {dtxsid}...")
        
        summary = client.get_summary_by_dtxsid(dtxsid)
        
        if summary:
            print(f"✓ Retrieved summary data")
            if isinstance(summary, list):
                print(f"  Found {len(summary)} summary records")
                if len(summary) > 0:
                    print(f"  Sample fields: {list(summary[0].keys())[:5]}")
            elif isinstance(summary, dict):
                print(f"  Summary keys: {list(summary.keys())[:5]}")
        else:
            print("✗ No summary data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_bioactivity_summary_by_tissue():
    """Test bioactivity summary filtered by tissue."""
    
    print("="*70)
    print("Test 2: Get Summary by DTXSID and Tissue")
    print("="*70)
    
    try:
        client = BioactivityData()
        
        dtxsid = "DTXSID7024241"
        tissue = "liver"
        print(f"Fetching bioactivity summary for {dtxsid} (tissue: {tissue})...")
        
        summary = client.get_summary_by_dtxsid_and_tissue(dtxsid, tissue)
        
        if summary:
            print(f"✓ Retrieved tissue-specific summary data")
            if isinstance(summary, list):
                print(f"  Found {len(summary)} records for liver tissue")
                if len(summary) > 0:
                    first_record = summary[0]
                    print(f"  Chemical: {first_record.get('chemicalName', 'N/A')}")
                    print(f"  Tissue: {first_record.get('tissue', 'N/A')}")
            elif isinstance(summary, dict):
                print(f"  Chemical: {summary.get('chemicalName', 'N/A')}")
                print(f"  Tissue: {summary.get('tissue', 'N/A')}")
        else:
            print("✗ No summary data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_bioactivity_by_aeid():
    """Test bioactivity data retrieval by AEID."""
    
    print("="*70)
    print("Test 3: Get Summary by AEID")
    print("="*70)
    
    try:
        client = BioactivityData()
        
        aeid = "3032"
        print(f"Fetching summary for AEID {aeid}...")
        
        summary = client.get_summary_by_aeid(aeid)
        
        if summary:
            print(f"✓ Retrieved AEID summary")
            if isinstance(summary, dict):
                print(f"  AEID: {summary.get('aeid', 'N/A')}")
                print(f"  Active MC: {summary.get('activeMc', 'N/A')}")
                print(f"  Total MC: {summary.get('totalMc', 'N/A')}")
                print(f"  Active SC: {summary.get('activeSc', 'N/A')}")
                print(f"  Total SC: {summary.get('totalSc', 'N/A')}")
        else:
            print("✗ No summary data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_bioactivity_data_by_spid():
    """Test bioactivity data retrieval by SPID."""
    
    print("="*70)
    print("Test 4: Get Data by SPID")
    print("="*70)
    
    try:
        client = BioactivityData()
        
        spid = "EPAPLT0232A03"
        print(f"Fetching data for SPID {spid}...")
        
        data = client.get_data_by_spid(spid)
        
        if data:
            print(f"✓ Retrieved SPID data")
            if isinstance(data, list):
                print(f"  Found {len(data)} records")
                if len(data) > 0:
                    print(f"  Sample fields: {list(data[0].keys())[:5]}")
            elif isinstance(data, dict):
                print(f"  Data keys: {list(data.keys())[:5]}")
        else:
            print("✗ No data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_bioactivity_data_by_m4id():
    """Test bioactivity data retrieval by M4ID."""
    
    print("="*70)
    print("Test 5: Get Data by M4ID")
    print("="*70)
    
    try:
        client = BioactivityData()
        
        m4id = "1135145"
        print(f"Fetching data for M4ID {m4id}...")
        
        data = client.get_data_by_m4id(m4id)
        
        if data:
            print(f"✓ Retrieved M4ID data")
            if isinstance(data, dict):
                print(f"  Data keys: {list(data.keys())[:5]}")
        else:
            print("✗ No data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_bioactivity_data_with_projection():
    """Test bioactivity data retrieval with projection."""
    
    print("="*70)
    print("Test 6: Get Data by DTXSID with Projection")
    print("="*70)
    
    try:
        client = BioactivityData()
        
        dtxsid = "DTXSID7020182"
        print(f"Fetching data for {dtxsid} with toxcast-summary-plot projection...")
        
        data = client.get_data_by_dtxsid_and_projection(
            dtxsid, 
            projection="toxcast-summary-plot"
        )
        
        if data:
            print(f"✓ Retrieved projected data")
            if isinstance(data, list):
                print(f"  Found {len(data)} records")
            elif isinstance(data, dict):
                print(f"  Data keys: {list(data.keys())[:5]}")
        else:
            print("✗ No data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_aed_data():
    """Test AED data retrieval."""
    
    print("="*70)
    print("Test 7: Get AED Data by DTXSID")
    print("="*70)
    
    try:
        client = BioactivityData()
        
        dtxsid = "DTXSID5021209"
        print(f"Fetching AED data for {dtxsid}...")
        
        data = client.get_aed_data_by_dtxsid(dtxsid)
        
        if data:
            print(f"✓ Retrieved AED data")
            if isinstance(data, list):
                print(f"  Found {len(data)} AED records")
            elif isinstance(data, dict):
                print(f"  Data keys: {list(data.keys())[:5]}")
        else:
            print("✗ No AED data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_batch_operations():
    """Test batch operations."""
    
    print("="*70)
    print("Test 8: Batch Operations")
    print("="*70)
    
    try:
        client = BioactivityData()
        
        # Test batch DTXSID search
        dtxsids = ["DTXSID7020182", "DTXSID9026974"]
        print(f"Fetching bioactivity data for {len(dtxsids)} DTXSIDs (batch)...")
        
        data = client.find_bioactivity_data_by_dtxsid_batch(dtxsids)
        
        if data:
            print(f"✓ Retrieved batch data")
            if isinstance(data, list):
                print(f"  Found {len(data)} total records")
            elif isinstance(data, dict):
                print(f"  Data keys: {list(data.keys())[:5]}")
        else:
            print("✗ No batch data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_batch_aeid():
    """Test batch AEID operations."""
    
    print("="*70)
    print("Test 9: Batch AEID Operations")
    print("="*70)
    
    try:
        client = BioactivityData()
        
        # Test batch AEID search
        aeids = [3032, 3033]
        print(f"Fetching bioactivity data for {len(aeids)} AEIDs (batch)...")
        
        data = client.find_bioactivity_data_by_aeid_batch(aeids)
        
        if data:
            print(f"✓ Retrieved batch AEID data")
            if isinstance(data, list):
                print(f"  Found {len(data)} total records")
            elif isinstance(data, dict):
                print(f"  Data keys: {list(data.keys())[:5]}")
        else:
            print("✗ No batch AEID data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_input_validation():
    """Test input validation."""
    
    print("="*70)
    print("Test 10: Input Validation")
    print("="*70)
    
    try:
        client = BioactivityData()
        
        # Test empty string validation
        print("Testing empty string validation...")
        try:
            client.get_summary_by_dtxsid("")
            print("✗ Should have raised ValueError for empty string")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
        
        # Test invalid type validation
        print("\nTesting invalid type validation...")
        try:
            client.get_summary_by_dtxsid(12345)
            print("✗ Should have raised ValueError for invalid type")
        except (ValueError, TypeError) as e:
            print(f"✓ Correctly raised error: {e}")
        
        # Test batch with non-list
        print("\nTesting batch with non-list...")
        try:
            client.find_bioactivity_data_by_dtxsid_batch("DTXSID7020182")
            print("✗ Should have raised ValueError for non-list")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
        
        # Test batch with empty list
        print("\nTesting batch with empty list...")
        try:
            client.find_bioactivity_data_by_dtxsid_batch([])
            print("✗ Should have raised ValueError for empty list")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
            
    except Exception as e:
        print(f"✗ Unexpected error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def main():
    """Run all tests."""
    
    print("\n" + "="*70)
    print("PyCompTox: BioactivityData Class Tests")
    print("="*70 + "\n")
    
    try:
        # Run all tests
        test_bioactivity_summary()
        test_bioactivity_summary_by_tissue()
        test_bioactivity_by_aeid()
        test_bioactivity_data_by_spid()
        test_bioactivity_data_by_m4id()
        test_bioactivity_data_with_projection()
        test_aed_data()
        test_batch_operations()
        test_batch_aeid()
        test_input_validation()
        
        print("="*70)
        print("All tests completed!")
        print("="*70)
        
    except ValueError as e:
        print(f"\n✗ Setup Error: {e}")
        print("\nPlease set up your API key first:")
        print("  from pycomptox import save_api_key")
        print("  save_api_key('YOUR_API_KEY')")
        print("\nOr set the COMPTOX_API_KEY environment variable")


if __name__ == "__main__":
    main()
