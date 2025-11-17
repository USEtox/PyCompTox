# Product Data

The `ProductData` class provides access to consumer product data from the EPA CompTox Dashboard, including product composition and Product Use Category (PUC) classifications.

## Overview

Product data includes:

- **Product Composition**: Chemicals found in consumer products
- **Product Use Categories (PUC)**: Hierarchical product classifications
- **Product Names and Manufacturers**: Detailed product information
- **Batch Operations**: Efficient processing of multiple chemicals

## Quick Start

```python
from pycomptox import ProductData

# Initialize the client
prod_data = ProductData()

# Get product data for a chemical
dtxsid = "DTXSID0020232"
products = prod_data.products_data_by_dtxsid(dtxsid)

# Get all PUC categories
puc_list = prod_data.list_all_puc_product()

# Batch operation
dtxsids = ["DTXSID0020232", "DTXSID7020182"]
batch_data = prod_data.product_data_by_dtxsid_batch(dtxsids)
```

## API Methods

### Products Data by DTXSID

```python
prod_data = ProductData()
products = prod_data.products_data_by_dtxsid("DTXSID0020232")

for product in products:
    print(f"Product: {product.get('productName')}")
    print(f"Manufacturer: {product.get('manufacturer')}")
    print(f"PUC: {product.get('pucCode')}")
```

### List All PUC Products

```python
puc_list = prod_data.list_all_puc_product()

for puc in puc_list:
    print(f"{puc.get('pucCode')}: {puc.get('pucDescription')}")
```

### Batch Operations

```python
dtxsids = ["DTXSID0020232", "DTXSID7020182"]
batch_data = prod_data.product_data_by_dtxsid_batch(dtxsids)

for result in batch_data:
    print(f"{result.get('dtxsid')}: {result.get('productName')}")
```

## API Reference

For complete API details, see [ProductData API Reference](api/productdata.md).
