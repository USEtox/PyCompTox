"""
Example usage of the PyCompTox Chemical Search API.

This script demonstrates all available search methods.
The API key will be loaded automatically from saved configuration.

To set up your API key, run:
    pycomptox-setup set YOUR_API_KEY
"""

import sys
from pathlib import Path

# Add the src directory to the path so we can import pycomptox
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pycomptox import Chemical


def main():
    # Initialize the Chemical client (API key loaded automatically)
    try:
        client = Chemical()
        print("✓ API key loaded successfully\n")
    except ValueError as e:
        print(f"Error: {e}\n")
        print("Please set up your API key first:")
        print("  pycomptox-setup set YOUR_API_KEY")
        return
    
    print("=== PyCompTox Chemical Search Examples ===\n")
    
    # Example 1: Search by starting value
    print("1. Searching for chemicals starting with 'Bisphenol'...")
    try:
        results = client.search_by_starting_value("Bisphenol")
        print(f"   Found {len(results)} chemicals")
        if results:
            print(f"   First result: {results[0]['preferredName']} ({results[0]['dtxsid']})")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 2: Search by exact value
    print("2. Searching for exact match 'DTXSID7020182'...")
    try:
        results = client.search_by_exact_value("DTXSID7020182")
        print(f"   Found {len(results)} chemical(s)")
        if results:
            chem = results[0]
            print(f"   Name: {chem['preferredName']}")
            print(f"   DTXSID: {chem['dtxsid']}")
            print(f"   CAS RN: {chem['casrn']}")
            print(f"   SMILES: {chem['smiles'][:50]}..." if len(chem['smiles']) > 50 else f"   SMILES: {chem['smiles']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 3: Search by substring
    print("3. Searching for chemicals containing 'phenol'...")
    try:
        results = client.search_by_substring_value("phenol")
        print(f"   Found {len(results)} chemicals")
        print("   First 5 results:")
        for i, chem in enumerate(results[:5], 1):
            print(f"      {i}. {chem['preferredName']} ({chem['dtxsid']})")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 4: Search by MS-ready formula
    print("4. Searching for chemicals with MS-ready formula 'C15H16O2'...")
    try:
        dtxsids = client.search_by_msready_formula("C15H16O2")
        print(f"   Found {len(dtxsids)} chemicals")
        print(f"   First 5 DTXSIDs: {dtxsids[:5]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 5: Search by exact formula
    print("5. Searching for chemicals with exact formula 'C15H16O2'...")
    try:
        dtxsids = client.search_by_exact_formula("C15H16O2")
        print(f"   Found {len(dtxsids)} chemicals")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 6: Search MS-ready by mass range
    print("6. Searching for MS-ready chemicals with mass 200.9-200.95...")
    try:
        dtxsids = client.search_ms_ready_by_mass_range(200.9, 200.95)
        print(f"   Found {len(dtxsids)} chemicals")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 7: Get count by MS-ready formula
    print("7. Getting count of chemicals with MS-ready formula 'C15H16O2'...")
    try:
        count = client.search_chemical_count_by_ms_ready_formula("C15H16O2")
        print(f"   Count: {count}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 8: Get count by exact formula
    print("8. Getting count of chemicals with exact formula 'C15H16O2'...")
    try:
        count = client.search_chemical_count_by_exact_formula("C15H16O2")
        print(f"   Count: {count}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n=== Examples completed ===")


if __name__ == "__main__":
    main()
