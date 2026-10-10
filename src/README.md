# Source Architecture (`src/`)

This directory houses the modular business intelligence core components:

- **`utils/`**:
  - `data_loader.py`: Ingestion pipeline, multi-format date parsing, schema normalization, financial metrics derivation, and customer RFM calculation.
  - `metrics.py`: Executive KPI computations, Period-over-Period variance deltas, Pareto 80/20 analysis, BCG quadrant classification, and What-If scenario financial simulation model.
- **`components/`**:
  - `ui.py`: Corporate BI CSS styles, custom executive metric cards, alert banners, and filter indicators.
  - `charts.py`: High-performance Plotly visual components with unified corporate palettes (Sales/Profit trends, Seasonality Heatmaps, BCG Quadrant Scatter, Pareto 80/20 Curves, US State Choropleth, RFM Treemaps, Shipping Boxplots, P&L Waterfall Bridges).
- **`views/`**:
  - `overview.py`: Executive summary with North Star KPIs, category breakdown, and loss-making alerts.
  - `sales_performance.py`: Deep-dive sales and financial diagnostics, seasonality heatmap, and discount margin cliff.
  - `product_intelligence.py`: Strategic BCG matrix, Pareto SKU concentration, and top/bottom SKU profitability tables.
  - `customer_analytics.py`: Customer RFM segmentation, lifetime value analysis, and CRM action playbooks.
  - `logistics_geo.py`: Interactive US State choropleth map, regional performance, and shipping SLA diagnostics.
  - `scenario_planner.py`: Executive What-If sensitivity simulator with pricing, discount, and cost levers.
  - `data_explorer.py`: Ad-hoc aggregation pivot builder, transaction ledger search, and CSV export.
- **`data/`**:
  - Contains `Superstore.csv` primary transaction dataset.
- **`images/`**:
  - Contains branding assets (`logo.png`).
