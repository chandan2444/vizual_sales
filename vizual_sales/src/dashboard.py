"""
VizualSales Dashboard — Interactive Sales Data Visualization
Built with Streamlit + Plotly
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_generator import load_data
from src.analyzer import SalesAnalyzer

# --- Page Config ---
st.set_page_config(
    page_title="VizualSales — Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def get_data():
    """Load and cache sales data."""
    return load_data()


def format_currency(value: float) -> str:
    """Format number as Indian Rupee currency."""
    return f"₹{value:,.2f}"


def main():
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1>📊 VizualSales</h1>
        <p style="font-size: 1.1rem; color: #888;">Sales Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    df = get_data()
    analyzer = SalesAnalyzer(df)

    # --- Sidebar Filters ---
    with st.sidebar:
        st.header("🔍 Filters")

        categories = st.multiselect(
            "Categories",
            options=sorted(df["category"].unique()),
            default=sorted(df["category"].unique()),
        )
        regions = st.multiselect(
            "Regions",
            options=sorted(df["region"].unique()),
            default=sorted(df["region"].unique()),
        )
        date_range = st.date_input(
            "Date Range",
            value=(df["date"].min(), df["date"].max()),
        )

        st.divider()
        st.markdown("**Built with:**")
        st.markdown("- Python & Pandas")
        st.markdown("- Streamlit & Plotly")
        st.markdown("- NumPy")

    # Apply filters
    if len(date_range) == 2:
        filtered = analyzer.filter_data(
            categories=categories,
            regions=regions,
            date_start=str(date_range[0]),
            date_end=str(date_range[1]),
        )
    else:
        filtered = analyzer.filter_data(categories=categories, regions=regions)

    # --- KPI Metrics ---
    kpis = filtered.get_kpi_summary()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Revenue", format_currency(kpis["total_revenue"]))
    with col2:
        st.metric("📦 Total Orders", f"{kpis['total_orders']:,}")
    with col3:
        st.metric("📈 Avg Order Value", format_currency(kpis["avg_order_value"]))
    with col4:
        st.metric("🏷️ Products", kpis["unique_products"])

    st.divider()

    # --- Row 1: Monthly Trend + Category Revenue ---
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📈 Monthly Revenue Trend")
        monthly = filtered.monthly_trend()
        fig_trend = px.line(
            monthly, x="month", y="revenue",
            markers=True,
            labels={"month": "Month", "revenue": "Revenue (₹)"},
        )
        fig_trend.update_traces(line_color="#4CAF50", line_width=3)
        fig_trend.update_layout(height=350, margin=dict(t=20, b=20))
        st.plotly_chart(fig_trend, use_container_width=True)

    with col2:
        st.subheader("🏷️ Revenue by Category")
        cat_data = filtered.revenue_by_category()
        fig_pie = px.pie(
            cat_data, values="total_revenue", names="category",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_pie.update_layout(height=350, margin=dict(t=20, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

    # --- Row 2: Top Products + Regional Performance ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Top 10 Products")
        top = filtered.top_products(10)
        fig_bar = px.bar(
            top, x="revenue", y="product",
            orientation="h",
            color="revenue",
            color_continuous_scale="Viridis",
            labels={"revenue": "Revenue (₹)", "product": "Product"},
        )
        fig_bar.update_layout(
            height=400, margin=dict(t=20, b=20),
            yaxis=dict(autorange="reversed"),
            showlegend=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("🗺️ Revenue by Region")
        region_data = filtered.revenue_by_region()
        fig_region = px.bar(
            region_data, x="region", y="total_revenue",
            color="region",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            labels={"total_revenue": "Revenue (₹)", "region": "Region"},
        )
        fig_region.update_layout(height=400, margin=dict(t=20, b=20), showlegend=False)
        st.plotly_chart(fig_region, use_container_width=True)

    st.divider()

    # --- Row 3: Heatmap + Payment Methods ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔥 Category × Region Heatmap")
        pivot = filtered.category_region_pivot()
        fig_heat = px.imshow(
            pivot, text_auto=".0f",
            color_continuous_scale="YlOrRd",
            labels=dict(x="Region", y="Category", color="Revenue (₹)"),
        )
        fig_heat.update_layout(height=350, margin=dict(t=20, b=20))
        st.plotly_chart(fig_heat, use_container_width=True)

    with col2:
        st.subheader("💳 Payment Methods")
        payment_data = filtered.payment_method_distribution()
        fig_payment = px.pie(
            payment_data, values="revenue", names="payment_method",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig_payment.update_layout(height=350, margin=dict(t=20, b=20))
        st.plotly_chart(fig_payment, use_container_width=True)

    st.divider()

    # --- Row 4: Customer Segments + Discount Impact ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👥 Customer Segments")
        seg_data = filtered.customer_segment_analysis()
        fig_seg = px.bar(
            seg_data, x="customer_segment", y="total_revenue",
            color="avg_order",
            color_continuous_scale="Blues",
            labels={"total_revenue": "Revenue (₹)", "customer_segment": "Segment"},
        )
        fig_seg.update_layout(height=350, margin=dict(t=20, b=20))
        st.plotly_chart(fig_seg, use_container_width=True)

    with col2:
        st.subheader("🏷️ Discount Impact Analysis")
        disc_data = filtered.discount_impact()
        fig_disc = px.scatter(
            disc_data, x="discount_pct", y="avg_revenue",
            size="num_orders", color="total_revenue",
            color_continuous_scale="Viridis",
            labels={"discount_pct": "Discount %", "avg_revenue": "Avg Revenue (₹)"},
        )
        fig_disc.update_layout(height=350, margin=dict(t=20, b=20))
        st.plotly_chart(fig_disc, use_container_width=True)

    # --- Raw Data Explorer ---
    with st.expander("📋 View Raw Data"):
        st.dataframe(filtered.df, use_container_width=True, height=300)
        st.download_button(
            "⬇️ Download CSV",
            filtered.df.to_csv(index=False),
            "sales_data_filtered.csv",
            "text/csv",
        )


if __name__ == "__main__":
    main()
