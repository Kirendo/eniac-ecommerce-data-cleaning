# Data

The raw order export (`orders.csv`, `orderlines.csv`, `products.csv`, `brands.csv`) isn't included in this repo. It originates from real anonymised order data from Eniac, an online Apple-accessories retailer, provided as training material during my Data Science & AI program — not a dataset with a clear public redistribution license, so it isn't bundled here.

What's included instead:

- `src/cleaning.py` — the cleaning functions, fully documented and independent of the raw files
- `notebooks/eda_data_cleaning_storytelling.ipynb` — already executed, so all outputs (tables, stats, charts) are visible without needing the raw data
- `exports/` — the aggregated CSVs and chart images produced by the notebook

## Expected schema (for reference)

| Table | Columns |
|---|---|
| `orders` | `order_id`, `created_date`, `total_paid`, `state` |
| `orderlines` | `id`, `id_order`, `product_id`, `product_quantity`, `sku`, `unit_price`, `date` |
| `products` | `sku`, `name`, `desc`, `price`, `promo_price`, `in_stock`, `type` |
| `brands` | `short` (SKU prefix), `long` (brand name) |

If you have access to an equivalent order export, drop the four CSVs into `data/raw/` and the notebook will run end to end.
