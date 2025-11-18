"""
Test script for BioactivityAOP class.

This script demonstrates basic usage of the BioactivityAOP API client
and tests methods for retrieving Adverse Outcome Pathway (AOP) data.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pycomptox.bioactivity import BioactivityAOP


def test_aop_by_toxcast_aeid():
    """Test AOP data retrieval by ToxCast AEID."""
    
    print("="*70)
    print("Test 1: Get AOP Data by ToxCast AEID")
    print("="*70)
    
    try:
        client = BioactivityAOP()
        print("✓ BioactivityAOP client initialized successfully\n")
        
        # Test with ToxCast AEID 63
        toxcast_aeid = 63
        print(f"Fetching AOP data for ToxCast AEID {toxcast_aeid}...")
        
        aop_data = client.get_aop_data_by_toxcast_aeid(toxcast_aeid)
        
        if aop_data:
            print(f"✓ Retrieved AOP data")
            if isinstance(aop_data, list):
                print(f"  Found {len(aop_data)} AOP records")
                if len(aop_data) > 0:
                    first_record = aop_data[0]
                    print(f"  Sample record fields:")
                    print(f"    - ToxCast AEID: {first_record.get('toxcastAeid', 'N/A')}")
                    print(f"    - Entrez Gene ID: {first_record.get('entrezGeneId', 'N/A')}")
                    print(f"    - Event Number: {first_record.get('eventNumber', 'N/A')}")
                    print(f"    - AOP Number: {first_record.get('aopNumber', 'N/A')}")
            elif isinstance(aop_data, dict):
                print(f"  Data keys: {list(aop_data.keys())}")
        else:
            print("✗ No AOP data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_aop_by_event_number():
    """Test AOP data retrieval by event number."""
    
    print("="*70)
    print("Test 2: Get AOP Data by Event Number")
    print("="*70)
    
    try:
        client = BioactivityAOP()
        
        # Test with event number 18
        event_number = 18
        print(f"Fetching AOP data for Event Number {event_number}...")
        
        events = client.get_aop_data_by_event_number(event_number)
        
        if events:
            print(f"✓ Retrieved AOP event data")
            if isinstance(events, list):
                print(f"  Found {len(events)} records associated with event {event_number}")
                if len(events) > 0:
                    first_event = events[0]
                    print(f"  Sample event record:")
                    print(f"    - Event Number: {first_event.get('eventNumber', 'N/A')}")
                    print(f"    - ToxCast AEID: {first_event.get('toxcastAeid', 'N/A')}")
                    print(f"    - AOP Number: {first_event.get('aopNumber', 'N/A')}")
                    if 'eventLink' in first_event:
                        print(f"    - Event Link: {first_event['eventLink'][:50]}...")
            elif isinstance(events, dict):
                print(f"  Data keys: {list(events.keys())}")
        else:
            print("✗ No event data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_aop_by_entrez_gene_id():
    """Test AOP data retrieval by Entrez Gene ID."""
    
    print("="*70)
    print("Test 3: Get AOP Data by Entrez Gene ID")
    print("="*70)
    
    try:
        client = BioactivityAOP()
        
        # Test with Entrez Gene ID 196
        entrez_gene_id = 196
        print(f"Fetching AOP data for Entrez Gene ID {entrez_gene_id}...")
        
        gene_aops = client.get_aop_data_by_entrez_gene_id(entrez_gene_id)
        
        if gene_aops:
            print(f"✓ Retrieved AOP gene data")
            if isinstance(gene_aops, list):
                print(f"  Found {len(gene_aops)} AOP records for gene {entrez_gene_id}")
                if len(gene_aops) > 0:
                    first_record = gene_aops[0]
                    print(f"  Sample gene record:")
                    print(f"    - Entrez Gene ID: {first_record.get('entrezGeneId', 'N/A')}")
                    print(f"    - Event Number: {first_record.get('eventNumber', 'N/A')}")
                    print(f"    - ToxCast AEID: {first_record.get('toxcastAeid', 'N/A')}")
                    print(f"    - AOP Number: {first_record.get('aopNumber', 'N/A')}")
                    
                # Count unique AOPs
                unique_aops = set()
                unique_events = set()
                for record in gene_aops:
                    if 'aopNumber' in record and record['aopNumber']:
                        unique_aops.add(record['aopNumber'])
                    if 'eventNumber' in record and record['eventNumber']:
                        unique_events.add(record['eventNumber'])
                
                if unique_aops:
                    print(f"  Unique AOP pathways: {len(unique_aops)}")
                if unique_events:
                    print(f"  Unique events: {len(unique_events)}")
            elif isinstance(gene_aops, dict):
                print(f"  Data keys: {list(gene_aops.keys())}")
        else:
            print("✗ No gene AOP data returned")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_multiple_toxcast_aeids():
    """Test multiple ToxCast AEID lookups."""
    
    print("="*70)
    print("Test 4: Multiple ToxCast AEID Lookups")
    print("="*70)
    
    try:
        client = BioactivityAOP()
        
        # Test with multiple AEIDs
        aeids = [63, 100, 200]
        print(f"Fetching AOP data for {len(aeids)} ToxCast AEIDs...")
        
        all_results = {}
        for aeid in aeids:
            try:
                data = client.get_aop_data_by_toxcast_aeid(aeid)
                all_results[aeid] = data if data else []
                record_count = len(data) if isinstance(data, list) else 1 if data else 0
                print(f"  AEID {aeid}: {record_count} records")
            except Exception as e:
                print(f"  AEID {aeid}: Error - {type(e).__name__}")
                all_results[aeid] = []
        
        total_records = sum(len(records) if isinstance(records, list) else 1 if records else 0 
                           for records in all_results.values())
        print(f"\n✓ Retrieved {total_records} total AOP records across {len(aeids)} AEIDs")
        
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_input_validation():
    """Test input validation for all methods."""
    
    print("="*70)
    print("Test 5: Input Validation")
    print("="*70)
    
    try:
        client = BioactivityAOP()
        
        # Test invalid type for toxcast_aeid
        print("Testing invalid type for toxcast_aeid...")
        try:
            client.get_aop_data_by_toxcast_aeid("63")
            print("✗ Should have raised ValueError for string input")
        except (ValueError, TypeError) as e:
            print(f"✓ Correctly raised error: {e}")
        
        # Test negative value for toxcast_aeid
        print("\nTesting negative value for toxcast_aeid...")
        try:
            client.get_aop_data_by_toxcast_aeid(-1)
            print("✗ Should have raised ValueError for negative value")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
        
        # Test zero value for toxcast_aeid
        print("\nTesting zero value for toxcast_aeid...")
        try:
            client.get_aop_data_by_toxcast_aeid(0)
            print("✗ Should have raised ValueError for zero value")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
        
        # Test invalid type for event_number
        print("\nTesting invalid type for event_number...")
        try:
            client.get_aop_data_by_event_number(18.5)
            print("✗ Should have raised ValueError for float input")
        except (ValueError, TypeError) as e:
            print(f"✓ Correctly raised error: {e}")
        
        # Test negative value for entrez_gene_id
        print("\nTesting negative value for entrez_gene_id...")
        try:
            client.get_aop_data_by_entrez_gene_id(-196)
            print("✗ Should have raised ValueError for negative value")
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
            
    except Exception as e:
        print(f"✗ Unexpected error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_data_structure():
    """Test the structure of returned AOP data."""
    
    print("="*70)
    print("Test 6: AOP Data Structure Analysis")
    print("="*70)
    
    try:
        client = BioactivityAOP()
        
        # Get sample data
        toxcast_aeid = 63
        print(f"Analyzing data structure for ToxCast AEID {toxcast_aeid}...")
        
        aop_data = client.get_aop_data_by_toxcast_aeid(toxcast_aeid)
        
        if aop_data and isinstance(aop_data, list) and len(aop_data) > 0:
            first_record = aop_data[0]
            print(f"✓ Retrieved sample record\n")
            print(f"  Record structure:")
            for key, value in first_record.items():
                value_type = type(value).__name__
                value_str = str(value)[:50] if value else "None"
                print(f"    - {key}: {value_type} = {value_str}")
            
            # Check for expected fields
            expected_fields = ['toxcastAeid', 'entrezGeneId', 'eventNumber', 'aopNumber']
            print(f"\n  Expected field check:")
            for field in expected_fields:
                present = "✓" if field in first_record else "✗"
                print(f"    {present} {field}")
        else:
            print("✗ No data available for structure analysis")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_rate_limiting():
    """Test rate limiting functionality."""
    
    print("="*70)
    print("Test 7: Rate Limiting")
    print("="*70)
    
    try:
        import time
        
        # Create client with rate limiting
        delay = 0.5  # 500ms delay
        client = BioactivityAOP(time_delay_between_calls=delay)
        print(f"✓ Created client with {delay}s rate limit\n")
        
        # Make multiple requests and measure time
        aeids = [63, 100]
        print(f"Making {len(aeids)} requests with rate limiting...")
        
        start_time = time.time()
        for aeid in aeids:
            try:
                client.get_aop_data_by_toxcast_aeid(aeid)
            except Exception:
                pass  # Ignore errors, just testing rate limiting
        
        elapsed = time.time() - start_time
        expected_min = delay * (len(aeids) - 1)
        
        print(f"  Elapsed time: {elapsed:.2f}s")
        print(f"  Expected minimum: {expected_min:.2f}s")
        
        if elapsed >= expected_min:
            print(f"✓ Rate limiting working correctly")
        else:
            print(f"⚠ Rate limiting may not be working as expected")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def test_error_handling():
    """Test error handling for various scenarios."""
    
    print("="*70)
    print("Test 8: Error Handling")
    print("="*70)
    
    try:
        client = BioactivityAOP()
        
        # Test with a very large AEID that may not exist
        print("Testing with potentially non-existent AEID...")
        try:
            aeid = 999999
            data = client.get_aop_data_by_toxcast_aeid(aeid)
            if data:
                print(f"  Found data for AEID {aeid}")
            else:
                print(f"  No data found for AEID {aeid} (expected)")
        except ValueError as e:
            print(f"  ValueError: {e}")
        except Exception as e:
            print(f"  {type(e).__name__}: {str(e)[:100]}")
        
        # Test with a large event number
        print("\nTesting with large event number...")
        try:
            event = 999999
            data = client.get_aop_data_by_event_number(event)
            if data:
                print(f"  Found data for Event {event}")
            else:
                print(f"  No data found for Event {event} (expected)")
        except ValueError as e:
            print(f"  ValueError: {e}")
        except Exception as e:
            print(f"  {type(e).__name__}: {str(e)[:100]}")
        
        print("\n✓ Error handling tests completed")
            
    except ValueError as e:
        print(f"✗ ValueError: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
    
    print("\n" + "="*70 + "\n")


def main():
    """Run all tests."""
    
    print("\n" + "="*70)
    print("PyCompTox: BioactivityAOP Class Tests")
    print("="*70 + "\n")
    
    try:
        # Run all tests
        test_aop_by_toxcast_aeid()
        test_aop_by_event_number()
        test_aop_by_entrez_gene_id()
        test_multiple_toxcast_aeids()
        test_input_validation()
        test_data_structure()
        test_rate_limiting()
        test_error_handling()
        
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
