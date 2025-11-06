"""Quick test of ChemicalList functionality"""

from pycomptox import ChemicalList

# Initialize client
client = ChemicalList()

print("Testing ChemicalList functionality...")
print("=" * 60)

# Test 1: Get all list types
print("\n1. Getting All List Types")
print("-" * 60)
types = client.get_all_list_types()
print(f"Available list types: {types}")

# Test 2: Get federal lists
print("\n2. Getting Federal Lists")
print("-" * 60)
federal_lists = client.get_public_lists_by_type('federal')
print(f"Found {len(federal_lists)} federal lists")
for lst in federal_lists[:3]:
    print(f"  • {lst['label']}: {lst['chemicalCount']} chemicals")

# Test 3: Get all public lists (just count)
print("\n3. Getting All Public Lists")
print("-" * 60)
all_lists = client.get_all_public_lists()
print(f"Total public lists: {len(all_lists)}")

# Show summary by type
from collections import Counter
types_count = Counter(lst['type'] for lst in all_lists)
for list_type, count in types_count.items():
    print(f"  {list_type}: {count} lists")

print("\n" + "=" * 60)
print("✓ All tests completed successfully!")
