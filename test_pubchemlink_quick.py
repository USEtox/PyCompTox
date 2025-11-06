"""Quick test of PubChemLink functionality"""

from pycomptox import PubChemLink

# Initialize client
client = PubChemLink()

print("Testing PubChemLink functionality...")
print("=" * 60)

# Test 1: Single chemical lookup
print("\n1. Single Chemical Lookup")
print("-" * 60)
dtxsid = "DTXSID7020182"
result = client.check_existence_by_dtxsid(dtxsid)
print(f"DTXSID: {result['dtxsid']}")
print(f"Has PubChem GHS data: {result['isSafetyData']}")
if result['safetyUrl']:
    print(f"URL: {result['safetyUrl']}")

# Test 2: Batch lookup
print("\n2. Batch Chemical Lookup")
print("-" * 60)
dtxsids = [
    "DTXSID7020182",  # Bisphenol A
    "DTXSID2021315",  # Caffeine
    "DTXSID5020001"   # 1,2,3-Trichloropropane
]
results = client.check_existence_by_dtxsid_batch(dtxsids)
print(f"Checked {len(results)} chemicals:")
for r in results:
    status = "✓" if r['isSafetyData'] else "✗"
    print(f"  {status} {r['dtxsid']}: {r['isSafetyData']}")

print("\n" + "=" * 60)
print("✓ All tests completed successfully!")
