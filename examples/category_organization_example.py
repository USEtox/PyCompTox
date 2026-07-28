"""
Example demonstrating category-based organization of PyCompTox API.

This example shows how to use the new category-based access pattern
to work with chemical, bioactivity, and exposure data.
"""

from pycomptox import chemical, bioactivity, exposure


def main():
    """Demonstrate category-based API access."""
    
    print("=" * 70)
    print("PyCompTox Category-Based API Organization Example")
    print("=" * 70)
    
    # 1. Chemical Category - Find and characterize a chemical
    print("\n1. CHEMICAL CATEGORY - Search and Properties")
    print("-" * 70)
    
    chem = chemical.Chemical()
    print("Searching for 'caffeine'...")
    results = chem.search_by_starting_value("caffeine")
    
    if results:
        dtxsid = results[0]['dtxsid']
        name = results[0].get('preferredName', 'N/A')
        print(f"Found: {name} ({dtxsid})")
        
        # Get properties
        props = chemical.ChemicalProperties()
        prop_data = props.retrieve_properties_by_dtxsid(dtxsid)
        
        print(f"Molecular Weight: {prop_data.get('molecularWeight', 'N/A')}")
        print(f"Molecular Formula: {prop_data.get('molecularFormula', 'N/A')}")
        print(f"SMILES: {prop_data.get('smiles', 'N/A')[:50]}...")
    
    # 2. Bioactivity Category - Check for bioactivity data
    print("\n2. BIOACTIVITY CATEGORY - Toxicity Data")
    print("-" * 70)
    
    bio_data = bioactivity.BioactivityData()
    print(f"Checking bioactivity data for {dtxsid}...")
    
    try:
        summary = bio_data.get_summary_by_dtxsid(dtxsid)
        if summary:
            print(f"Found {len(summary)} bioactivity records")
            if summary:
                first = summary[0]
                print(f"Sample assay: {first.get('assayName', 'N/A')}")
        else:
            print("No bioactivity data available")
    except Exception as e:
        print(f"Bioactivity data not available: {str(e)[:50]}")
    
    # 3. Exposure Category - Multiple data sources
    print("\n3. EXPOSURE CATEGORY - Usage and Exposure")
    print("-" * 70)
    
    # Check functional use
    func_use = exposure.FunctionalUse()
    print(f"Checking functional use for {dtxsid}...")
    
    try:
        uses = func_use.get_functional_use_by_dtxsid(dtxsid)
        if uses:
            print(f"Found {len(uses)} functional uses:")
            for use in uses[:3]:  # Show first 3
                print(f"  - {use.get('functionName', 'N/A')}")
        else:
            print("No functional use data available")
    except Exception as e:
        print(f"Functional use not available: {str(e)[:50]}")
    
    # Check list presence
    lists = exposure.ListPresence()
    print(f"\nChecking regulatory/screening lists...")
    
    try:
        presence = lists.get_list_presence_data_by_dtxsid(dtxsid)
        if presence:
            present_lists = [p['listName'] for p in presence if p.get('isPresent')]
            if present_lists:
                print(f"Found on {len(present_lists)} lists:")
                for list_name in present_lists[:5]:  # Show first 5
                    print(f"  - {list_name}")
        else:
            print("No list presence data available")
    except Exception as e:
        print(f"List presence not available: {str(e)[:50]}")
    
    # Demonstrate mixed access pattern
    print("\n4. MIXED ACCESS PATTERNS")
    print("-" * 70)
    print("You can also use direct imports alongside category imports:")
    
    # This still works!
    from pycomptox import Chemical, ExposurePrediction
    
    chem_direct = Chemical()
    exp_direct = ExposurePrediction()
    
    print("✓ Direct import: Chemical()")
    print("✓ Category import: chemical.Chemical()")
    print("Both patterns work seamlessly together!")
    
    print("\n" + "=" * 70)
    print("Example complete! See CATEGORY_ORGANIZATION.md for more details.")
    print("=" * 70)


if __name__ == "__main__":
    main()
