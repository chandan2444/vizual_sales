# 📊 VizualSales — Sales Data Visualization Dashboard

A Python data visualization project that analyzes sales data, generates insights, and presents them through an interactive Streamlit dashboard with Plotly charts.

## 🏗️ Architecture

```
vizual_sales/
├── src/
│   ├── data_generator.py    # Generates realistic sample sales data
│   ├── analyzer.py          # Data analysis engine (Pandas)
│   └── dashboard.py         # Interactive Streamlit + Plotly dashboard
├── tests/
│   └── test_vizual_sales.py # Unit tests with pytest
├── data/                    # CSV data storage
├── requirements.txt
├── Dockerfile
└── README.md
```

## 🔑 Key Python Concepts

- **Pandas**: GroupBy, pivot tables, aggregations, filtering
- **Data Visualization**: Plotly charts (bar, line, pie, heatmap, scatter)
- **OOP**: Analyzer class with encapsulated logic
- **List/Dict Comprehensions**: Data transformation
- **Type Hints**: Full type annotation
- **File I/O**: CSV read/write operations

## 🚀 Quick Start

```bash
pip install -r requirements.txt

# Generate sample data
python -m src.data_generator

# Launch dashboard
streamlit run src/dashboard.py
```

## 📊 Dashboard Features

- **Revenue Overview**: Monthly trends, YoY growth
- **Product Analysis**: Top products, category breakdown
- **Regional Performance**: Sales by region with heatmaps
- **Customer Insights**: Segment analysis, repeat purchase rates
- **Interactive Filters**: Date range, category, region selectors
