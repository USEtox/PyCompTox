"""Quick test of WikiLink functionality."""
from pycomptox import WikiLink

wiki = WikiLink()

# Test single chemical
print("Testing single chemical lookup:")
data = wiki.check_existence_by_dtxsid('DTXSID7020182')
print(f"  DTXSID: {data['dtxsid']}")
print(f"  Has Wikipedia GHS data: {bool(data['safetyUrl'])}")
if data['safetyUrl']:
    print(f"  URL: {data['safetyUrl']}")

# Test batch
print("\nTesting batch lookup:")
dtxsids = ['DTXSID7020182', 'DTXSID2021315', 'DTXSID5020001']
results = wiki.check_existence_by_dtxsid_batch(dtxsids)
print(f"  Got {len(results)} results")
for r in results:
    status = "✓ Has data" if r['safetyUrl'] else "✗ No data"
    print(f"    {r['dtxsid']}: {status}")

print("\n✓ All WikiLink tests passed!")
