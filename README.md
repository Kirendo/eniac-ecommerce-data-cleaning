# Eniac Order Data: Cleaning & Storytelling

End-to-end data cleaning and exploratory analysis on a real e-commerce order export: fixing a recurring price-formatting bug, deciding when a "clean-looking" column still isn't trustworthy, and turning the result into a few business-relevant charts.

## Business context

Eniac is an online retailer of Apple accessories and peripherals. This analysis works with the order, order-line, and product catalogue data to understand where revenue actually comes from and how much demand is lost before it ever becomes a sale.

## What this project demonstrates

- Diagnosing a non-obvious data quality bug (prices stored with an ambiguous thousands separator) by comparing raw values against a SKU's own price history, not just by checking for nulls
- Making — and documenting — a judgment call to *exclude* a column (`promo_price`) because it fails a sanity check, rather than blindly trusting or "fixing" it
- Building cleaning logic as testable, reusable functions (`src/cleaning.py`) instead of one-off notebook cells
- Turning cleaned data into a small set of charts that answer specific business questions, not just visualising for its own sake

## Key findings

- **Conversion, not revenue, is the headline problem.** Of ~227k orders started, only **20.5%** ever reach `Completed`; **52%** never leave the shopping-basket stage.
- **~12% of order lines** had a price stored with an ambiguous thousands separator (e.g. `"2.565.99"` for €2,565.99), silently breaking naive numeric parsing.
- **`promo_price` is unreliable**: after fixing the same formatting bug, it's *higher* than the regular price for 85% of products (median ratio ~8.5x) — the opposite of what a promotional price should do — so it's dropped from the analysis rather than used.
- **Apple accounts for roughly half of all product revenue**, with November 2017 standing out as a clear seasonal (Black Friday / holiday) peak in monthly revenue.

## Repo structure

```
notebooks/   eda_data_cleaning_storytelling.ipynb — already executed, all outputs visible
src/         cleaning.py — reusable, documented cleaning functions
exports/     aggregated CSVs + chart images produced by the notebook
data/        notes on the data source (raw files not included — see data/README.md)
```

## Tools

Python, pandas, matplotlib, seaborn, Jupyter.

## Reproducing

```
pip install -r requirements.txt
```

Drop the four raw CSVs into `data/raw/` (see `data/README.md` for the expected schema) and run the notebook top to bottom. The notebook in this repo is already executed, so the charts and findings above are visible without needing the raw data at all.
