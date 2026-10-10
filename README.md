# Superstore Executive Business Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=flat&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=flat&logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)

An enterprise-grade **Business Intelligence & Financial Analytics Platform** engineered with Python, Streamlit, and Plotly. Designed specifically for **BI Analysts, Corporate Strategy Executives, and Operations Leaders**, this application transforms retail transactions into actionable decision intelligence, profit diagnostics, customer RFM segmentation, and real-time sensitivity modeling.

---

## Table of Contents
- [Executive Overview](#executive-overview)
- [Key Features & Analytics Frameworks](#key-features--analytics-frameworks)
- [Repository Architecture](#repository-architecture)
- [Quickstart & Installation](#quickstart--installation)
- [Automated Testing](#automated-testing)
- [Business Metrics Glossary](#business-metrics-glossary)
- [License](#license)

---

## Executive Overview

The platform provides multi-dimensional diagnostic analytics across retail sales operations:
- **Financial Health**: Evaluates net margins, discount elasticity, and cost drivers.
- **Product Strategy**: Identifies growth opportunities and margin drains using BCG matrix and Pareto 80/20 analysis.
- **Customer Segmentation**: Segments customers using Recency, Frequency, and Monetary (RFM) scoring.
- **Logistics & SLAs**: Tracks delivery speed and carrier reliability across United States territories.
- **Executive Simulation**: Interactive What-If simulation engine to forecast P&L changes before making pricing or operational shifts.

---

## Key Features & Analytics Frameworks

### 1. Executive Performance Dashboard
- **North Star Metrics**: Tracks Total Revenue, Net Profit, Gross Margin %, Total Orders, Average Order Value (AOV), and Average Discount %.
- **Period-over-Period (YoY) Deltas**: Compares live performance against preceding operating periods with automated percentage and basis point variance indicators.
- **Dynamic Executive Alerts**: Automated warnings highlighting unprofitable sub-categories and margin dilution in real time.

### 2. Sales & Financial Diagnostics
- **Time-Series Analysis**: Monthly and quarterly trend trajectories with a 3-period moving average smoothing line.
- **Annual Seasonality Matrix**: Year-over-month heatmaps identifying recurring peaks and holiday demand surges.
- **Discount Margin Erosion Curve**: Pinpoints the "Discount Cliff" where high promotional discounts lead to negative margins (identifying net losses on discounts over 20%).
- **Cumulative Revenue Run-Rate**: Pacing curves tracking daily revenue velocity across fiscal years.

### 3. Strategic Product Portfolio Intelligence
- **BCG Margin-Volume Matrix**: Automatically categorizes products and sub-categories into four strategic quadrants:
  - **Stars**: High Sales Volume & High Profit Margin.
  - **Cash Cows**: High Sales Volume & Stable/Lower Margin.
  - **Opportunities**: Emerging lines with High Margin but Low Volume.
  - **Underperformers**: Margin-dilutive lines requiring pricing review or SKU rationalization.
- **Pareto (80/20) Concentration**: Calculates the percentage and count of SKUs that generate 80% of total revenue.
- **SKU Profit Extremes**: Side-by-side ledgers ranking the **Top 10 Value Creators** vs. **Top 10 Profit Drains**.

### 4. Customer Intelligence & RFM Segmentation
- **RFM Valuation Model**: Algorithmic scoring categorizing accounts into behavioral cohorts:
  - *Champions*, *Loyal Customers*, *Potential Loyalists*, *New Accounts*, *At Risk*, *Needs Attention*, and *Hibernating*.
- **Interactive RFM Treemap**: Visualizes customer cohorts sized by gross sales and colored by net profit contribution.
- **CRM Strategic Playbook**: Actionable retention and upselling recommendations tailored to each customer group.
- **Top Enterprise Accounts**: Rankings by lifetime spend, order frequency, and average order value.

### 5. Logistics, Supply Chain & Geographic Diagnostics
- **Interactive US Choropleth Map**: State-level penetration map switchable between Sales Volume, Net Profit, and Profit Margin %.
- **Fulfillment Lead Time (Order-to-Ship SLA)**: Lead time boxplots and median delivery speeds by shipping carrier tier (*Same Day*, *First Class*, *Second Class*, *Standard Class*).
- **Territory Margin Breakdown**: Regional performance comparisons across West, East, Central, and South hubs.

### 6. Executive What-If Scenario Planner
- **Real-Time Financial Simulator**: Interactive decision levers to forecast business impact:
  - **Price Adjustment** (-20% to +20%)
  - **Discount Policy Discipline** (-50% to +50%)
  - **Demand Volume Fluctuation** (-30% to +50%)
  - **COGS / Inflationary Cost Adjustment** (-20% to +30%)
- **P&L Variance Bridge (Waterfall Chart)**: Visualizes step-by-step profit adjustments from baseline to simulated outcomes.
- **Price vs. Volume Sensitivity Grid**: 2D heat matrix evaluating the joint profitability impact of simultaneous price and demand shifts.

### 7. Ad-Hoc Data Explorer & Report Builder
- **Dynamic Pivot Aggregator**: Multi-dimension grouping across category, sub-category, region, customer segment, and RFM status.
- **Granular Ledger Search**: Multi-attribute search filtering by Order ID, Customer Name, or Product.
- **One-Click Export**: Immediate download of filtered transactional datasets and pivot summaries in CSV format.

---

## Repository Architecture

```text
Superstore-Sales-Dashboard/
|-- app.py                     # Main Streamlit application entry point
|-- requirements.txt           # Production package dependencies
|-- README.md                  # Project documentation & architecture guide
|-- LICENSE                    # MIT License
|
|-- .streamlit/
|   `-- config.toml            # Executive theme styling (colors, layout, fonts)
|
|-- src/
|   |-- components/
|   |   |-- __init__.py
|   |   |-- ui.py              # Custom CSS styles, metric cards, banners, KPI badges
|   |   `-- charts.py          # Plotly visual components (BCG, Pareto, Choropleth, etc.)
|   |
|   |-- utils/
|   |   |-- __init__.py
|   |   |-- data_loader.py     # Ingestion, date parsing, feature engineering, RFM scoring
|   |   `-- metrics.py         # BI metric formulas, BCG classifier, Pareto logic, simulator
|   |
|   |-- views/
|   |   |-- __init__.py
|   |   |-- overview.py             # 1. Executive Overview tab
|   |   |-- sales_performance.py    # 2. Sales & Financial Diagnostics tab
|   |   |-- product_intelligence.py # 3. Product Portfolio (BCG & Pareto) tab
|   |   |-- customer_analytics.py   # 4. Customer RFM Intelligence tab
|   |   |-- logistics_geo.py        # 5. Logistics & Regional Map tab
|   |   |-- scenario_planner.py     # 6. What-If Scenario Planner tab
|   |   `-- data_explorer.py        # 7. Ad-Hoc Explorer & Export tab
|   |
|   |-- data/
|   |   |-- Superstore.csv          # Primary transaction dataset
|   |   `-- superstore_original.xls # Original legacy Excel archive
|   |
|   `-- images/
|       `-- logo.png                # Corporate brand asset
|
|-- tests/
|   |-- __init__.py
|   |-- test_data_loader.py    # Tests for ingestion, feature extraction, and RFM
|   |-- test_metrics.py        # Tests for KPI calculations, Pareto 80/20, BCG matrix
|   |-- test_scenario.py       # Tests for what-if simulation calculations
|   `-- run_tests.py           # Standalone automated test runner script
|
`-- data_query/
    |-- db.sql                 # SQL schema & PostgreSQL ingestion scripts
    `-- superstore.csv         # Normalized database-ready CSV
