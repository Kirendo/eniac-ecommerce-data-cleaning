"""
Cleaning functions for the Eniac order data.

Biggest issue in the raw files: prices above ~1000 have an extra dot
as thousands separator (e.g. "2.565.99" instead of 2565.99), which
breaks normal float parsing. fix_price_string deals with that.
"""

import pandas as pd


def fix_price_string(value) -> float | None:
    """Turn a price string like '2.565.99' into a float (2565.99).

    If there's more than one dot, everything except the last gets removed.
    Returns None for anything that can't be parsed.
    """
    text = str(value)
    if text in ("nan", "None", ""):
        return None
    parts = text.split(".")
    if len(parts) > 2:
        text = "".join(parts[:-1]) + "." + parts[-1]
    try:
        return float(text)
    except ValueError:
        return None


def clean_orders(orders_raw: pd.DataFrame) -> pd.DataFrame:
    """Parse dates, drop rows where total_paid is missing."""
    orders = orders_raw.copy()
    orders["created_date"] = pd.to_datetime(orders["created_date"])
    before = len(orders)
    orders = orders.dropna(subset=["total_paid"])
    dropped = before - len(orders)
    if dropped:
        print(f"clean_orders: dropped {dropped} rows with missing total_paid")
    return orders


def clean_orderlines(orderlines_raw: pd.DataFrame) -> pd.DataFrame:
    """Fix prices, parse dates, add a price_is_reliable flag.

    Prices <= 0 or more than 5x off from the SKU's median get flagged
    instead of dropped -- makes it easier to see what's weird.
    """
    orderlines = orderlines_raw.copy()
    orderlines["date"] = pd.to_datetime(orderlines["date"])
    orderlines["unit_price"] = orderlines["unit_price"].apply(fix_price_string)

    sku_median = (
        orderlines.loc[orderlines["unit_price"] > 0]
        .groupby("sku")["unit_price"]
        .median()
    )
    orderlines = orderlines.merge(
        sku_median.rename("sku_median_price"), on="sku", how="left"
    )
    ratio = orderlines["unit_price"] / orderlines["sku_median_price"]
    orderlines["price_is_reliable"] = (
        (orderlines["unit_price"] > 0) & ratio.between(0.2, 5)
    )

    orderlines["brand_code"] = orderlines["sku"].str[:3]
    orderlines["line_revenue"] = orderlines["unit_price"] * orderlines["product_quantity"]
    return orderlines


def clean_products(products_raw: pd.DataFrame) -> pd.DataFrame:
    """Fix price formatting and drop promo_price.

    promo_price should be lower than the regular price but after fixing
    the thousands separator it's actually higher for ~85% of products
    (median is about 8.5x the normal price). Doesn't make sense, so I dropped it.
    """
    products = products_raw.copy()
    products["price"] = products["price"].apply(fix_price_string)
    products = products.drop(columns=["promo_price"])
    return products
