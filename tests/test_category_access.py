"""
Test script to verify category-based access to PyCompTox API.

This script demonstrates both access patterns:
1. Direct import of classes
2. Category-based namespace access
"""

def test_direct_imports():
    """Test traditional direct import pattern."""
    print("Testing direct imports...")
    
    # Import individual classes from their modules
    from pycomptox.chemical import Chemical, ChemicalProperties
    from pycomptox.bioactivity import AssaySearch, BioactivityData
    from pycomptox.exposure import ExposurePrediction, FunctionalUse, CCCData
    
    # Verify classes can be instantiated
    chem = Chemical()
    props = ChemicalProperties()
    assay = AssaySearch()
    bio = BioactivityData()
    exp = ExposurePrediction()
    func = FunctionalUse()
    ccc = CCCData()
    
    print("✓ Direct imports work correctly")


def test_category_imports():
    """Test category-based import pattern."""
    print("\nTesting category-based imports...")
    
    # Import category submodules
    from pycomptox import chemical, bioactivity, exposure
    
    # Verify category modules exist and have classes
    assert hasattr(chemical, 'Chemical')
    assert hasattr(chemical, 'ChemicalProperties')
    assert hasattr(chemical, 'ChemicalDetails')
    
    assert hasattr(bioactivity, 'AssaySearch')
    assert hasattr(bioactivity, 'BioactivityData')
    assert hasattr(bioactivity, 'BioactivityAOP')
    
    assert hasattr(exposure, 'ExposurePrediction')
    assert hasattr(exposure, 'FunctionalUse')
    assert hasattr(exposure, 'CCCData')
    assert hasattr(exposure, 'MMDB')
    
    # Verify classes can be instantiated via category access
    chem = chemical.Chemical()
    props = chemical.ChemicalProperties()
    assay = bioactivity.AssaySearch()
    bio = bioactivity.BioactivityData()
    exp = exposure.ExposurePrediction()
    func = exposure.FunctionalUse()
    
    print("✓ Category-based imports work correctly")


def test_namespace_access():
    """Test package namespace access pattern."""
    print("\nTesting namespace access...")
    
    # Import package with alias
    import pycomptox as pct
    
    # Verify category modules are accessible
    assert hasattr(pct, 'chemical')
    assert hasattr(pct, 'bioactivity')
    assert hasattr(pct, 'exposure')
    
    # Verify classes can be instantiated via namespace
    chem = pct.chemical.Chemical()
    props = pct.chemical.ChemicalProperties()
    assay = pct.bioactivity.AssaySearch()
    exp = pct.exposure.ExposurePrediction()
    
    print("✓ Namespace access works correctly")


def test_all_chemical_classes():
    """Test all chemical module classes."""
    print("\nTesting all chemical classes...")
    from pycomptox import chemical
    
    classes = ['Chemical', 'ChemicalDetails', 'ChemicalProperties', 
               'ChemSynonym', 'ChemicalList', 'ExtraData', 
               'WikiLink', 'PubChemLink']
    
    for cls_name in classes:
        assert hasattr(chemical, cls_name), f"Missing {cls_name}"
        cls = getattr(chemical, cls_name)
        instance = cls()
        print(f"  ✓ {cls_name}")
    
    print("✓ All chemical classes accessible")


def test_all_bioactivity_classes():
    """Test all bioactivity module classes."""
    print("\nTesting all bioactivity classes...")
    from pycomptox import bioactivity
    
    classes = ['AssaySearch', 'AssayBioactivity', 'BioactivityModel',
               'BioactivityData', 'BioactivityAOP', 'AnalyticalQC']
    
    for cls_name in classes:
        assert hasattr(bioactivity, cls_name), f"Missing {cls_name}"
        cls = getattr(bioactivity, cls_name)
        instance = cls()
        print(f"  ✓ {cls_name}")
    
    print("✓ All bioactivity classes accessible")


def test_all_exposure_classes():
    """Test all exposure module classes."""
    print("\nTesting all exposure classes...")
    from pycomptox import exposure
    
    classes = ['CCCData', 'MMDB', 'FunctionalUse', 'ProductData',
               'HTTKData', 'ListPresence', 'ExposurePrediction',
               'DemographicExposure']
    
    for cls_name in classes:
        assert hasattr(exposure, cls_name), f"Missing {cls_name}"
        cls = getattr(exposure, cls_name)
        instance = cls()
        print(f"  ✓ {cls_name}")
    
    print("✓ All exposure classes accessible")


def main():
    """Run all tests."""
    print("=" * 60)
    print("PyCompTox Category-Based Access Test Suite")
    print("=" * 60)
    
    try:
        test_direct_imports()
        test_category_imports()
        test_namespace_access()
        test_all_chemical_classes()
        test_all_bioactivity_classes()
        test_all_exposure_classes()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nBoth access patterns work correctly:")
        print("  1. Direct: from pycomptox import Chemical")
        print("  2. Category: from pycomptox import chemical")
        print("              chem = chemical.Chemical()")
        print("  3. Namespace: import pycomptox as pct")
        print("                chem = pct.chemical.Chemical()")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
