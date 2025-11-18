"""
Test script for ChemicalProperties class.

This script demonstrates basic usage of the ChemicalProperties API client.
"""

import sys
sys.path.insert(0, '../src')

from pycomptox.chemical import Chemical, ChemicalProperties

def main():
    print("="*70)
    print("PyCompTox: Chemical Properties Tests")
    print("="*70)
    print()
    
    try:
        # Initialize clients
        searcher = Chemical()
        props = ChemicalProperties()
        print("✓ Clients initialized successfully\n")
        
        # Test 1: Find a chemical
        print("="*70)
        print("Test 1: Property Summary for Bisphenol A")
        print("="*70)
        
        results = searcher.search_by_exact_value("Bisphenol A")
        if results:
            dtxsid = results[0]['dtxsid']
            print(f"✓ Found: {results[0]['preferredName']} ({dtxsid})\n")
            
            # Get property summary
            try:
                summary = props.get_property_summary_by_dtxsid(dtxsid)
                print(f"✓ Retrieved {len(summary)} property summaries")
                
                # Display first 5
                for i, prop in enumerate(summary[:5], 1):
                    exp_med = prop.get('experimentalMedian')
                    pred_med = prop.get('predictedMedian')
                    unit = prop.get('unit', '')
                    
                    print(f"  {i}. {prop['propName']} ({unit})")
                    if exp_med:
                        print(f"     Experimental Median: {exp_med}")
                    if pred_med:
                        print(f"     Predicted Median: {pred_med}")
            except ValueError as e:
                print(f"⚠ Property summary endpoint not available: {e}")
        
        # Test 2: Predicted properties
        print("\n" + "="*70)
        print("Test 2: Predicted Properties")
        print("="*70)
        
        predicted = props.get_predicted_properties_by_dtxsid(dtxsid)
        print(f"✓ Retrieved {len(predicted)} predicted properties")
        
        # Show first 5
        for i, prop in enumerate(predicted[:5], 1):
            print(f"  {i}. {prop['propName']}: {prop['propValue']} {prop.get('propUnit', '')}")
            print(f"     Model: {prop['modelName']}")
        
        # Test 3: Experimental properties
        print("\n" + "="*70)
        print("Test 3: Experimental Properties")
        print("="*70)
        
        experimental = props.get_experimental_properties_by_dtxsid(dtxsid)
        print(f"✓ Retrieved {len(experimental)} experimental measurements")
        
        # Show first 5
        for i, prop in enumerate(experimental[:5], 1):
            print(f"  {i}. {prop['propName']}: {prop['propValue']} {prop.get('propUnit', '')}")
            print(f"     Source: {prop.get('sourceName', 'N/A')}")
        
        # Test 4: Environmental fate
        print("\n" + "="*70)
        print("Test 4: Environmental Fate Properties")
        print("="*70)
        
        fate = props.get_fate_summary_by_dtxsid(dtxsid)
        print(f"✓ Retrieved {len(fate)} fate property summaries")
        
        for i, prop in enumerate(fate[:5], 1):
            pred_med = prop.get('predictedMedian')
            unit = prop.get('unit', '')
            print(f"  {i}. {prop['propName']}: {pred_med} {unit}")
        
        # Test 5: Available property names
        print("\n" + "="*70)
        print("Test 5: Available Property Names")
        print("="*70)
        
        pred_names = props.get_predicted_property_names()
        print(f"✓ Available predicted properties: {len(pred_names)}")
        print("  First 10:")
        for prop in pred_names[:10]:
            print(f"    - {prop['propertyName']}")
        
        exp_names = props.get_all_experimental_property_names()
        print(f"\n✓ Available experimental properties: {len(exp_names)}")
        print("  First 10:")
        for prop in exp_names[:10]:
            print(f"    - {prop['propertyName']}")
        
        # Test 6: Batch operations
        print("\n" + "="*70)
        print("Test 6: Batch Operations")
        print("="*70)
        
        # Find multiple chemicals
        chemical_names = ["Caffeine", "Aspirin", "Ibuprofen"]
        dtxsids = []
        
        for name in chemical_names:
            results = searcher.search_by_exact_value(name)
            if results:
                dtxsid_found = results[0]['dtxsid']
                dtxsids.append(dtxsid_found)
                print(f"✓ {name}: {dtxsid_found}")
        
        # Get batch predicted properties
        batch_predicted = props.get_predicted_properties_by_dtxsid_batch(dtxsids)
        print(f"\n✓ Batch predicted properties: {len(batch_predicted)} total")
        
        # Group by chemical
        by_chem = {}
        for prop in batch_predicted:
            sid = prop['dtxsid']
            if sid not in by_chem:
                by_chem[sid] = []
            by_chem[sid].append(prop)
        
        for sid, props_list in by_chem.items():
            print(f"  {sid}: {len(props_list)} properties")
        
        print("\n" + "="*70)
        print("All tests completed successfully!")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
