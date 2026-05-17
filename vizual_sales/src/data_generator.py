"""
Sales Data Generator
====================
Generates realistic sample sales data for the dashboard.

Demonstrates:
- Random data generation with NumPy
- Dict/List comprehensions
- CSV file I/O with Pandas
- Date range generation
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Data directory
DATA_DIR = Path(__file__).parent.parent / "data"


# --- Product Catalog ---
PRODUCTS = {
    "Electronics": [
        {"name": "Wireless Headphones", "base_price": 2499},
        {"name": "Smart Watch", "base_price": 4999},
        {"name": "Bluetooth Speaker", "base_price": 1999},
        {"name": "USB-C Hub", "base_price": 1299},
        {"name": "Mechanical Keyboard", "base_price": 3499},
    ],
    "Clothing": [
        {"name": "Cotton T-Shirt", "base_price": 599},
        {"name": "Denim Jeans", "base_price": 1499},
        {"name": "Running Shoes", "base_price": 2999},
        {"name": "Formal Shirt", "base_price": 1299},
        {"name": "Winter Jacket", "base_price": 3999},
    ],
    "Home & Kitchen": [
        {"name": "Coffee Maker", "base_price": 2499},
        {"name": "Air Purifier", "base_price": 5999},
        {"name": "Vacuum Cleaner", "base_price": 4499},
        {"name": "Blender", "base_price": 1799},
        {"name": "Iron Press", "base_price": 999},
    ],
    "Books": [
        {"name": "Python Crash Course", "base_price": 499},
        {"name": "Clean Code", "base_price": 699},
        {"name": "System Design", "base_price": 599},
        {"name": "Data Science Handbook", "base_price": 799},
        {"name": "Atomic Habits", "base_price": 399},
    ],
}

REGIONS = ["North", "South", "East", "West", "Central"]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Cash on Delivery", "Net Banking"]
CUSTOMER_SEGMENTS = ["New", "Returning", "Premium", "Wholesale"]


def generate_sales_data(
    num_records: int = 1000,
    start_date: str = "2025-01-01",
    end_date: str = "2026-05-17",
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate a realistic sales dataset.

    Args:
        num_records: Number of sales transactions to generate.
        start_date: Start date for the date range.
        end_date: End date for the date range.
        seed: Random seed for reproducibility.

    Returns:
        DataFrame with sales transaction data.
    """
    np.random.seed(seed)

    # Generate random dates within range
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    dates = np.random.choice(date_range, size=num_records)

    # Build records using list comprehension
    records: List[Dict[str, Any]] = []
    for i in range(num_records):
        # Pick random category and product
        category = np.random.choice(list(PRODUCTS.keys()))
        product = np.random.choice(PRODUCTS[category])

        # Add price variation (+/- 20%)
        price = product["base_price"] * np.random.uniform(0.8, 1.2)
        quantity = np.random.choice([1, 1, 1, 2, 2, 3])  # Weighted towards 1
        discount_pct = np.random.choice([0, 0, 0, 5, 10, 15, 20])  # Weighted towards 0

        total = round(price * quantity * (1 - discount_pct / 100), 2)

        records.append({
            "order_id": f"ORD-{10000 + i}",
            "date": pd.Timestamp(dates[i]),
            "product": product["name"],
            "category": category,
            "unit_price": round(price, 2),
            "quantity": quantity,
            "discount_pct": discount_pct,
            "total_amount": total,
            "region": np.random.choice(REGIONS),
            "payment_method": np.random.choice(PAYMENT_METHODS),
            "customer_segment": np.random.choice(CUSTOMER_SEGMENTS),
        })

    df = pd.DataFrame(records)
    df = df.sort_values("date").reset_index(drop=True)

    logger.info(f"Generated {len(df)} sales records from {start_date} to {end_date}")
    return df


def save_data(df: pd.DataFrame, filename: str = "sales_data.csv") -> Path:
    """Save DataFrame to CSV in the data directory."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filepath = DATA_DIR / filename
    df.to_csv(filepath, index=False)
    logger.info(f"Saved data to {filepath}")
    return filepath


def load_data(filename: str = "sales_data.csv") -> pd.DataFrame:
    """Load sales data from CSV. Generates if file doesn't exist."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        logger.info("Data file not found. Generating new dataset...")
        df = generate_sales_data()
        save_data(df, filename)
        return df
    df = pd.read_csv(filepath, parse_dates=["date"])
    logger.info(f"Loaded {len(df)} records from {filepath}")
    return df


# --- Run directly to generate data ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    df = generate_sales_data(num_records=1000)
    path = save_data(df)
    print(f"✅ Generated {len(df)} records → {path}")
    print(f"\nSample data:")
    print(df.head(5).to_string())
    print(f"\nCategories: {df['category'].unique()}")
    print(f"Regions: {df['region'].unique()}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Total revenue: ₹{df['total_amount'].sum():,.2f}")
