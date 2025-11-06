"""Quick test of ExtraData functionality."""
from pycomptox import ExtraData

extra = ExtraData()

# Test single chemical
print("Testing single chemical lookup:")
data = extra.get_data_by_dtxsid('DTXSID7020182')
print(f"  DTXSID: {data['dtxsid']}")
print(f"  Total refs: {data['refs']}")
print(f"  PubMed: {data['pubmed']}")
print(f"  Patents: {data['googlePatent']}")
print(f"  Literature: {data['literature']}")

# Test batch
print("\nTesting batch lookup:")
dtxsids = ['DTXSID7020182', 'DTXSID2021315', 'DTXSID5020001']
results = extra.get_data_by_dtxsid_batch(dtxsids)
print(f"  Got {len(results)} results")
for r in results:
    print(f"    {r['dtxsid']}: {r['refs']} total refs, {r['pubmed']} PubMed")

print("\n✓ All ExtraData tests passed!")
