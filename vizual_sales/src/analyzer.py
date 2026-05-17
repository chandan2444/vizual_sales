"""
Sales Analyzer Module
=====================
Core analysis engine that processes sales data using Pandas.

Demonstrates:
- GroupBy operations and aggregations
- Pivot tables
- Date-based analysis (monthly, quarterly trends)
- Dictionary comprehensions for result formatting
"""

import pandas as pd
import numpy as np
from typing import Any, Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class SalesAnalyzer:
    """
    Analyzes sales data and generates insights.

    Attributes:
        df (pd.DataFrame): The sales dataset to analyze.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initialize with a sales DataFrame.

        Args:
            df: Sales data with columns like date, product, category, etc.
        """
        self.df = df.copy()
        # Ensure date column is datetime
        if "date" in self.df.columns:
            self.df["date"] = pd.to_datetime(self.df["date"])
        logger.info(f"Analyzer initialized with {len(self.df)} records")

    def total_revenue(self) -> float:
        """Calculate total revenue across all sales."""
        return round(self.df["total_amount"].sum(), 2)

    def total_orders(self) -> int:
        """Count total number of orders."""
        return len(self.df)

    def average_order_value(self) -> float:
        """Calculate average order value (AOV)."""
        return round(self.df["total_amount"].mean(), 2)

    def revenue_by_category(self) -> pd.DataFrame:
        """
        Revenue breakdown by product category.
        Uses GroupBy — one of Pandas' most powerful features.

        GroupBy splits data into groups, applies a function, then combines results.
        """
        result = (
            self.df.groupby("category")["total_amount"]
            .agg(["sum", "mean", "count"])
            .rename(columns={"sum": "total_revenue", "mean": "avg_order", "count": "num_orders"})
            .sort_values("total_revenue", ascending=False)
            .round(2)
        )
        return result.reset_index()

    def revenue_by_region(self) -> pd.DataFrame:
        """Revenue and order count by region."""
        result = (
            self.df.groupby("region")
            .agg(
                total_revenue=("total_amount", "sum"),
                num_orders=("order_id", "count"),
                avg_order=("total_amount", "mean"),
            )
            .sort_values("total_revenue", ascending=False)
            .round(2)
        )
        return result.reset_index()

    def monthly_trend(self) -> pd.DataFrame:
        """
        Monthly revenue trend.
        Uses pd.Grouper to group datetime data by month.
        """
        self.df["month"] = self.df["date"].dt.to_period("M")
        result = (
            self.df.groupby("month")
            .agg(
                revenue=("total_amount", "sum"),
                orders=("order_id", "count"),
            )
            .round(2)
        )
        result.index = result.index.astype(str)
        return result.reset_index()

    def top_products(self, n: int = 10) -> pd.DataFrame:
        """Top N products by revenue."""
        result = (
            self.df.groupby("product")["total_amount"]
            .sum()
            .sort_values(ascending=False)
            .head(n)
            .round(2)
        )
        return result.reset_index().rename(columns={"total_amount": "revenue"})

    def payment_method_distribution(self) -> pd.DataFrame:
        """Sales distribution by payment method."""
        result = (
            self.df.groupby("payment_method")
            .agg(
                count=("order_id", "count"),
                revenue=("total_amount", "sum"),
            )
            .sort_values("revenue", ascending=False)
            .round(2)
        )
        return result.reset_index()

    def customer_segment_analysis(self) -> pd.DataFrame:
        """Revenue and order analysis by customer segment."""
        result = (
            self.df.groupby("customer_segment")
            .agg(
                total_revenue=("total_amount", "sum"),
                num_orders=("order_id", "count"),
                avg_order=("total_amount", "mean"),
            )
            .sort_values("total_revenue", ascending=False)
            .round(2)
        )
        return result.reset_index()

    def category_region_pivot(self) -> pd.DataFrame:
        """
        Create a pivot table: Category vs Region showing revenue.
        Pivot tables are essential for multi-dimensional analysis.
        """
        pivot = pd.pivot_table(
            self.df,
            values="total_amount",
            index="category",
            columns="region",
            aggfunc="sum",
            fill_value=0,
        ).round(2)
        return pivot

    def discount_impact(self) -> pd.DataFrame:
        """Analyze how discounts affect order values."""
        result = (
            self.df.groupby("discount_pct")
            .agg(
                num_orders=("order_id", "count"),
                avg_revenue=("total_amount", "mean"),
                total_revenue=("total_amount", "sum"),
            )
            .sort_index()
            .round(2)
        )
        return result.reset_index()

    def get_kpi_summary(self) -> Dict[str, Any]:
        """Generate a KPI summary dictionary for the dashboard."""
        return {
            "total_revenue": self.total_revenue(),
            "total_orders": self.total_orders(),
            "avg_order_value": self.average_order_value(),
            "top_category": self.revenue_by_category().iloc[0]["category"],
            "top_region": self.revenue_by_region().iloc[0]["region"],
            "unique_products": self.df["product"].nunique(),
        }

    def filter_data(
        self,
        categories: List[str] = None,
        regions: List[str] = None,
        date_start: str = None,
        date_end: str = None,
    ) -> "SalesAnalyzer":
        """
        Return a new SalesAnalyzer with filtered data.
        This pattern allows method chaining without modifying original data.
        """
        filtered = self.df.copy()

        if categories:
            filtered = filtered[filtered["category"].isin(categories)]
        if regions:
            filtered = filtered[filtered["region"].isin(regions)]
        if date_start:
            filtered = filtered[filtered["date"] >= pd.to_datetime(date_start)]
        if date_end:
            filtered = filtered[filtered["date"] <= pd.to_datetime(date_end)]

        return SalesAnalyzer(filtered)
