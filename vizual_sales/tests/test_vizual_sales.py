"""
Tests for SalesPulse — Data Generator, Analyzer
Run with: pytest tests/ -v
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_generator import generate_sales_data, PRODUCTS, REGIONS
from src.analyzer import SalesAnalyzer


class TestDataGenerator:
    """Test the sales data generator."""

    def test_generates_correct_number_of_records(self):
        df = generate_sales_data(num_records=100)
        assert len(df) == 100

    def test_has_required_columns(self):
        df = generate_sales_data(num_records=10)
        required = ["order_id", "date", "product", "category", "unit_price",
                     "quantity", "discount_pct", "total_amount", "region",
                     "payment_method", "customer_segment"]
        for col in required:
            assert col in df.columns, f"Missing column: {col}"

    def test_categories_are_valid(self):
        df = generate_sales_data(num_records=200)
        valid_categories = set(PRODUCTS.keys())
        actual_categories = set(df["category"].unique())
        assert actual_categories.issubset(valid_categories)

    def test_regions_are_valid(self):
        df = generate_sales_data(num_records=200)
        actual = set(df["region"].unique())
        assert actual.issubset(set(REGIONS))

    def test_prices_are_positive(self):
        df = generate_sales_data(num_records=100)
        assert (df["unit_price"] > 0).all()
        assert (df["total_amount"] > 0).all()

    def test_seed_reproducibility(self):
        df1 = generate_sales_data(num_records=50, seed=42)
        df2 = generate_sales_data(num_records=50, seed=42)
        pd.testing.assert_frame_equal(df1, df2)

    def test_dates_are_sorted(self):
        df = generate_sales_data(num_records=100)
        assert df["date"].is_monotonic_increasing


class TestSalesAnalyzer:
    """Test the SalesAnalyzer class."""

    @pytest.fixture
    def analyzer(self):
        df = generate_sales_data(num_records=500, seed=42)
        return SalesAnalyzer(df)

    def test_total_revenue(self, analyzer):
        revenue = analyzer.total_revenue()
        assert isinstance(revenue, float)
        assert revenue > 0

    def test_total_orders(self, analyzer):
        assert analyzer.total_orders() == 500

    def test_average_order_value(self, analyzer):
        aov = analyzer.average_order_value()
        assert aov > 0
        # AOV should be between min and max total_amount
        assert aov <= analyzer.df["total_amount"].max()

    def test_revenue_by_category(self, analyzer):
        result = analyzer.revenue_by_category()
        assert isinstance(result, pd.DataFrame)
        assert "category" in result.columns
        assert "total_revenue" in result.columns
        assert len(result) == len(PRODUCTS)

    def test_revenue_by_region(self, analyzer):
        result = analyzer.revenue_by_region()
        assert len(result) == len(REGIONS)
        assert "total_revenue" in result.columns

    def test_monthly_trend(self, analyzer):
        result = analyzer.monthly_trend()
        assert "month" in result.columns
        assert "revenue" in result.columns
        assert len(result) > 0

    def test_top_products(self, analyzer):
        result = analyzer.top_products(5)
        assert len(result) == 5
        # Results should be sorted descending
        assert result["revenue"].is_monotonic_decreasing

    def test_payment_distribution(self, analyzer):
        result = analyzer.payment_method_distribution()
        assert "payment_method" in result.columns
        assert len(result) > 0

    def test_customer_segment_analysis(self, analyzer):
        result = analyzer.customer_segment_analysis()
        assert "customer_segment" in result.columns
        assert "total_revenue" in result.columns

    def test_pivot_table(self, analyzer):
        pivot = analyzer.category_region_pivot()
        assert isinstance(pivot, pd.DataFrame)
        assert pivot.shape[0] == len(PRODUCTS)  # categories
        assert pivot.shape[1] == len(REGIONS)   # regions

    def test_kpi_summary(self, analyzer):
        kpis = analyzer.get_kpi_summary()
        assert "total_revenue" in kpis
        assert "total_orders" in kpis
        assert kpis["total_orders"] == 500

    def test_filter_by_category(self, analyzer):
        filtered = analyzer.filter_data(categories=["Electronics"])
        assert all(filtered.df["category"] == "Electronics")
        assert filtered.total_orders() < analyzer.total_orders()

    def test_filter_by_region(self, analyzer):
        filtered = analyzer.filter_data(regions=["North"])
        assert all(filtered.df["region"] == "North")

    def test_discount_impact(self, analyzer):
        result = analyzer.discount_impact()
        assert "discount_pct" in result.columns
        assert "avg_revenue" in result.columns
