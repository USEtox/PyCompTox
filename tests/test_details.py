"""
Test script for PyCompTox ChemicalDetails class.

This script demonstrates the complete workflow:
1. Use Chemical class to search for chemicals and get their identifiers
2. Use ChemicalDetails class to retrieve detailed information
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pycomptox.chemical import Chemical, ChemicalDetails


def test_search_and_details_workflow():
    """
    Complete workflow: Search for chemical by name/CASRN, then get details.
    """
    print("=" * 70)
    print("PyCompTox: Chemical Search → Details Workflow")
    print("=" * 70)
    print()
    
    # Initialize clients
    try:
        search_client = Chemical()
        details_client = ChemicalDetails()
        print("✓ Clients initialized successfully\n")
    except ValueError as e:
        print(f"✗ Error: {e}\n")
        print("Please set up your API key first:")
        print("  pycomptox-setup set YOUR_API_KEY")
        return
    
    # Example 1: Search by chemical name and get details
    print("=" * 70)
    print("Example 1: Search by Chemical Name → Get Full Details")
    print("=" * 70)
    try:
        chemical_name = "Bisphenol A"
        print(f"1. Searching for '{chemical_name}'...")
        search_results = search_client.search_by_exact_value(chemical_name)
        
        if search_results:
            chem = search_results[0]
            dtxsid = chem['dtxsid']
            dtxcid = chem['dtxcid']
            casrn = chem['casrn']
            print(f"   ✓ Found: {chem['preferredName']}")
            print(f"     DTXSID: {dtxsid}")
            print(f"     DTXCID: {dtxcid}")
            print(f"     CAS RN: {casrn}")
            
            print(f"\n2. Getting detailed information for {dtxsid}...")
            details = details_client.data_by_dtxsid(dtxsid)
            print(f"   ✓ Retrieved detailed data")
            print(f"     Preferred Name: {details.get('preferredName', 'N/A')}")
            iupac_name = details.get('iupacName') or 'N/A'
            print(f"     IUPAC Name: {iupac_name[:80] if iupac_name != 'N/A' else 'N/A'}...")
            print(f"     Molecular Formula: {details.get('molFormula', 'N/A')}")
            print(f"     SMILES: {details.get('smiles', 'N/A')[:60]}...")
            print(f"     InChI Key: {details.get('inchikey', 'N/A')}")
            print(f"     Monoisotopic Mass: {details.get('monoisotopicMass', 'N/A')}")
            print(f"     PubChem CID: {details.get('pubchemCid', 'N/A')}")
            print(f"     Active Assays: {details.get('activeAssays', 'N/A')} / {details.get('totalAssays', 'N/A')}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 70)
    print("Example 2: Search by CAS RN → Get Structure Details")
    print("=" * 70)
    try:
        casrn = "80-05-7"
        print(f"1. Searching for CAS RN '{casrn}'...")
        search_results = search_client.search_by_exact_value(casrn)
        
        if search_results:
            chem = search_results[0]
            dtxsid = chem['dtxsid']
            print(f"   ✓ Found: {chem['preferredName']} ({dtxsid})")
            
            print(f"\n2. Getting structure details...")
            details = details_client.data_by_dtxsid(dtxsid, projection="chemicalstructure")
            print(f"   ✓ Retrieved structure data")
            print(f"     SMILES: {details.get('smiles', 'N/A')}")
            print(f"     MS-Ready SMILES: {details.get('msReadySmiles', 'N/A')}")
            print(f"     QSAR-Ready SMILES: {details.get('qsarReadySmiles', 'N/A')}")
            print(f"     InChI: {details.get('inchiString', 'N/A')[:70]}...")
            print(f"     Has Structure Image: {details.get('hasStructureImage', 'N/A')}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 70)
    print("Example 3: Batch Search → Batch Details")
    print("=" * 70)
    try:
        chemicals = ["Caffeine", "Aspirin", "Ibuprofen"]
        print(f"1. Searching for {len(chemicals)} chemicals...")
        
        dtxsids = []
        for chem_name in chemicals:
            try:
                results = search_client.search_by_exact_value(chem_name)
                if results:
                    dtxsid = results[0]['dtxsid']
                    dtxsids.append(dtxsid)
                    print(f"   ✓ {chem_name}: {dtxsid}")
            except Exception as e:
                print(f"   ✗ {chem_name}: {e}")
        
        if dtxsids:
            print(f"\n2. Getting batch details for {len(dtxsids)} chemicals...")
            batch_details = details_client.data_by_dtxsid_batch(
                dtxsids, 
                projection="chemicalidentifier"
            )
            print(f"   ✓ Retrieved details for {len(batch_details)} chemicals")
            
            print("\n   Results:")
            for detail in batch_details:
                name = detail.get('preferredName', 'N/A')
                dtxsid = detail.get('dtxsid', 'N/A')
                casrn = detail.get('casrn', 'N/A')
                print(f"     - {name} ({dtxsid}): CAS {casrn}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 70)
    print("Example 4: Using DTXCID for Details")
    print("=" * 70)
    try:
        dtxcid = "DTXCID505"
        print(f"Getting details for DTXCID: {dtxcid}...")
        
        details = details_client.data_by_dtxcid(dtxcid, projection="compact")
        print(f"✓ Retrieved details")
        print(f"  Preferred Name: {details.get('preferredName', 'N/A')}")
        print(f"  DTXSID: {details.get('dtxsid', 'N/A')}")
        print(f"  CAS RN: {details.get('casrn', 'N/A')}")
        print(f"  InChI Key: {details.get('inchikey', 'N/A')}")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_projections():
    """Test different projection options."""
    
    print("\n" + "=" * 70)
    print("Testing Different Projection Options")
    print("=" * 70)
    print()
    
    details_client = ChemicalDetails()
    dtxsid = "DTXSID7020182"  # Bisphenol A
    
    projections = [
        ("chemicalidentifier", "Chemical Identifiers Only"),
        ("chemicalstructure", "Chemical Structure"),
        ("ntatoolkit", "NTA Toolkit"),
    ]
    
    for projection, description in projections:
        print(f"\nProjection: {projection} ({description})")
        print("-" * 70)
        try:
            details = details_client.data_by_dtxsid(dtxsid, projection=projection)
            print(f"✓ Retrieved data with {len(details)} fields")
            print(f"  Fields: {', '.join(list(details.keys())[:10])}...")
        except Exception as e:
            print(f"✗ Error: {e}")


def test_batch_operations():
    """Test batch operations with multiple identifiers."""
    
    print("\n" + "=" * 70)
    print("Testing Batch Operations")
    print("=" * 70)
    print()
    
    details_client = ChemicalDetails()
    
    # Test DTXSID batch
    print("1. Batch retrieval by DTXSIDs")
    print("-" * 70)
    try:
        dtxsids = [
            "DTXSID7020182",  # Bisphenol A
            "DTXSID2021315",  # Caffeine
            "DTXSID2023638"   # Aspirin
        ]
        print(f"Retrieving details for {len(dtxsids)} DTXSIDs...")
        
        results = details_client.data_by_dtxsid_batch(dtxsids)
        print(f"✓ Retrieved {len(results)} chemical details")
        
        for result in results:
            name = result.get('preferredName', 'N/A')
            formula = result.get('molFormula', 'N/A')
            mass = result.get('monoisotopicMass', 'N/A')
            print(f"  - {name}: {formula} (MW: {mass})")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test DTXCID batch
    print("\n2. Batch retrieval by DTXCIDs")
    print("-" * 70)
    try:
        dtxcids = ["DTXCID505", "DTXCID30182", "DTXCID20182"]
        print(f"Retrieving details for {len(dtxcids)} DTXCIDs...")
        
        results = details_client.data_by_dtxcid_batch(
            dtxcids,
            projection="chemicalidentifier"
        )
        print(f"✓ Retrieved {len(results)} chemical details")
        
        for result in results:
            name = result.get('preferredName', 'N/A')
            dtxsid = result.get('dtxsid', 'N/A')
            casrn = result.get('casrn', 'N/A')
            print(f"  - {name} ({dtxsid}): CAS {casrn}")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    # Run main workflow tests
    test_search_and_details_workflow()
    
    # Run projection tests
    test_projections()
    
    # Run batch tests
    test_batch_operations()
    
    print("\n" + "=" * 70)
    print("All tests completed!")
    print("=" * 70)
