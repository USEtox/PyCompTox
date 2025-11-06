"""
Complete integration test for PyCompTox v0.4.0

Tests all four main API classes working together.
"""

from pycomptox import Chemical, ChemicalDetails, ChemicalProperties, ExtraData, __version__

print(f"PyCompTox version: {__version__}")
print("=" * 60)

# Test 1: Chemical Search
print("\n1. Testing Chemical Search...")
chem = Chemical()
results = chem.search_by_starting_value("caffeine")
assert len(results) > 0
dtxsid = results[0]['dtxsid']
print(f"   ✓ Found {len(results)} results for 'caffeine'")
print(f"   ✓ First result: {results[0]['preferredName']} ({dtxsid})")

# Test 2: Chemical Details
print("\n2. Testing Chemical Details...")
details = ChemicalDetails()
info = details.data_by_dtxsid(dtxsid, projection="chemicaldetailall")
assert 'preferredName' in info
assert 'molFormula' in info
print(f"   ✓ Got details for {info['preferredName']}")
print(f"   ✓ Formula: {info.get('molFormula', 'N/A')}")
print(f"   ✓ Weight: {info.get('molWeight', 'N/A')}")

# Test 3: Chemical Properties
print("\n3. Testing Chemical Properties...")
props = ChemicalProperties()
summary = props.get_property_summary_by_dtxsid(dtxsid)
predicted = props.get_predicted_properties_by_dtxsid(dtxsid)
experimental = props.get_experimental_properties_by_dtxsid(dtxsid)
assert len(summary) > 0
print(f"   ✓ Property summary: {len(summary)} properties")
print(f"   ✓ Predicted properties: {len(predicted)}")
print(f"   ✓ Experimental properties: {len(experimental)}")

# Test 4: Extra Data
print("\n4. Testing Extra Data...")
extra = ExtraData()
refs = extra.get_data_by_dtxsid(dtxsid)
assert 'refs' in refs
assert 'pubmed' in refs
print(f"   ✓ Total references: {refs['refs']}")
print(f"   ✓ PubMed citations: {refs['pubmed']}")
print(f"   ✓ Patents: {refs['googlePatent']}")
print(f"   ✓ Literature: {refs['literature']}")

# Test 5: Batch Operations
print("\n5. Testing Batch Operations...")
dtxsids = ["DTXSID7020182", "DTXSID2021315", "DTXSID5020001"]
batch_results = extra.get_data_by_dtxsid_batch(dtxsids)
assert len(batch_results) > 0
print(f"   ✓ Batch query returned {len(batch_results)} results")
for r in batch_results:
    print(f"     - {r['dtxsid']}: {r['refs']} references")

# Test 6: Complete Workflow
print("\n6. Testing Complete Workflow...")
print("   Searching for 'bisphenol A'...")
search_results = chem.search_by_starting_value("bisphenol A")
if search_results:
    bpa_dtxsid = search_results[0]['dtxsid']
    print(f"   ✓ Found: {search_results[0]['preferredName']}")
    
    bpa_details = details.data_by_dtxsid(bpa_dtxsid)
    print(f"   ✓ CASRN: {bpa_details.get('casrn', 'N/A')}")
    
    bpa_props = props.get_property_summary_by_dtxsid(bpa_dtxsid)
    print(f"   ✓ Properties: {len(bpa_props)}")
    
    bpa_refs = extra.get_data_by_dtxsid(bpa_dtxsid)
    print(f"   ✓ References: {bpa_refs['refs']}")

print("\n" + "=" * 60)
print("✅ ALL INTEGRATION TESTS PASSED!")
print("=" * 60)
print("\nPyCompTox v0.4.0 is fully operational!")
print("\nAvailable modules:")
print("  - Chemical (search)")
print("  - ChemicalDetails (detailed information)")
print("  - ChemicalProperties (properties data)")
print("  - ExtraData (reference counts)")
print("\nFor documentation, run: mkdocs serve")
