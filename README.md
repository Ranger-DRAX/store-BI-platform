# 📊 Superstore Executive Business Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Tests](https://img.shields.io/badge/Tests-Passing-success.svg?logo=pytest&logoColor=white)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade **Business Intelligence & Financial Analytics Platform** engineered in Python and Streamlit. Designed specifically for **BI Analysts, Corporate Strategy Executives, and Operations Leaders**, this application transforms raw retail transactions into actionable decision intelligence, profit diagnostics, customer segmentation, and predictive sensitivity modeling.

---

## 🌟 Executive Highlights & BI Capabilities

### 1. 📊 Executive Performance Dashboard
- **North Star Financial Metrics**: Live tracking of **Total Revenue**, **Net Profit**, **Gross Margin %**, **Total Order Count**, **Average Order Value (AOV)**, and **Discount Exposure**.
- **Period-over-Period (YoY) Deltas**: Automated baseline variance analysis tracking revenue momentum, margin basis point fluctuations, and order frequency changes.
- **Dynamic Executive Alerts**: Automated rule-based alerts flagging loss-making sub-categories and margin dilution in real time.

### 2. 📈 Sales & Financial Diagnostics
- **Time-Series Decomposition**: Configurable monthly and quarterly trend trajectories with a 3-period moving average smoothing line.
- **Fiscal Seasonality Heatmap**: Year-over-month comparative matrix identifying cyclical demand spikes and Q4 holiday surges.
- **Discount Elasticity & Cliff Analysis**: Deep diagnostic pinpointing the threshold where discounting turns margin-dilutive (empirically identifying negative margins on promotions exceeding 20%).
- **Cumulative Annual Run-Rate Curves**: Fiscal-year pacing curves comparing daily sales velocity across operating years.

### 3. 📦 Strategic Product Portfolio Intelligence
- **BCG Growth-Share / Margin-Volume Matrix**: Automatically classifies product categories into:
  - **⭐ Stars**: High Sales Volume & High Profit Margin.
  - **🐄 Cash Cows**: High Sales Volume & Stable/Lower Margin.
  - **🚀 Opportunities**: Emerging lines with High Margin but Low Volume.
  - **⚠️ Underperformers**: Margin-dilutive lines requiring SKU rationalization.
- **Pareto (80/20) Revenue Concentration**: Identifies the exact percentage and count of SKUs that drive 80% of aggregate revenue, surfacing revenue risk and catalog dependencies.
- **SKU Profit Extremes**: Side-by-side executive ledgers ranking the **Top 10 Value Creators** vs. **Top 10 Profit Drains**.

### 4. 👥 Customer Intelligence & RFM Segmentation
- **Recency, Frequency, Monetary (RFM) Valuation**: Algorithmic segmentation categorizing customers into behavioral cohorts:
  - *Champions*, *Loyal Customers*, *Potential Loyalists*, *New Accounts*, *At Risk*, *Needs Attention*, and *Hibernating*.
- **Interactive RFM Treemap**: Visualizes customer cohorts sized by gross sales and colored by net profit contribution.
- **Strategic CRM Playbook**: Action-oriented retention protocols, upsell triggers, and loyalty incentive strategies per cohort.
- **Strategic Account Ledger**: Tracks top enterprise accounts by lifetime spend, order frequency, and average basket size.

### 5. 🚚 Logistics, Supply Chain & Geographic Heatmap
- **Interactive US Choropleth Map**: State-level penetration map switchable between Sales Volume, Net Profit, and Profit Margin %.
- **Fulfillment Lead Time (Order-to-Ship SLA)**: Lead time boxplots and median delivery speeds by shipping carrier tier (*Same Day*, *First Class*, *Second Class*, *Standard Class*).
- **Territory Margin Analysis**: Regional performance breakdowns highlighting operational variance between West, East, Central, and South operating hubs.

### 6. 🔮 Executive What-If Scenario Planner
- **Real-Time Financial Simulator**: Empowers leadership to test strategic pricing and cost assumptions:
  - **Price Elasticity Slider** (-20% to +20%)
  - **Discount Policy Discipline** (-50% to +50%)
  - **Demand Volume Fluctuation** (-30% to +50%)
  - **COGS / Inflationary Cost Adjustment** (-20% to +30%)
- **P&L Variance Bridge (Waterfall Chart)**: Visually deconstructs variance from baseline net profit to simulated net profit.
- **Multi-Variable Sensitivity Matrix**: 2D heat matrix evaluating the joint profitability impact of simultaneous price and volume shifts.

### 7. 📋 Ad-Hoc Data Explorer & Report Builder
- **Dynamic Pivot Aggregator**: Multi-dimension grouping across category, sub-category, region, customer segment, and RFM status.
- **Granular Ledger Search**: Instant multi-attribute search filtering by Order ID, Customer Name, or Product.
- **One-Click Export**: Immediate download of filtered transactional datasets and pivot summaries in CSV format.

---

## 🏗️ Repository Architecture

```
Superstore-Sales-Dashboard-with-Streamlit-main/
│
├── app.py                     # Main Streamlit application entry point & layout orchestrator
├── requirements.txt           # Production package dependencies
├── README.md                  # Comprehensive documentation & architecture guide
│
├── .streamlit/
│   └── config.toml            # Executive theme styling (colors, layout, fonts)
│
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── ui.py              # CSS styles, metric cards, banners, KPI badges
│   │   └── charts.py          # Corporate Plotly visual components (BCG, Pareto, Map, etc.)
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_loader.py     # Ingestion, date parsing, feature engineering, RFM scoring
│   │   └── metrics.py         # BI metric formulas, BCG classifier, Pareto logic, simulation engine
│   │
│   ├── views/
│   │   ├── __init__.py
│   │   ├── overview.py             # 1. Executive Overview tab
│   │   ├── sales_performance.py    # 2. Sales & Financial Diagnostics tab
│   │   ├── product_intelligence.py # 3. Product Portfolio (BCG & Pareto) tab
│   │   ├── customer_analytics.py   # 4. Customer RFM Intelligence tab
│   │   ├── logistics_geo.py        # 5. Logistics & Regional Map tab
│   │   ├── scenario_planner.py     # 6. What-If Scenario Planner tab
│   │   └── data_explorer.py        # 7. Ad-Hoc Explorer & Export tab
│   │
│   ├── data/
│   │   ├── Superstore.csv          # Primary transaction dataset
│   │   └── superstore_original.xls # Original legacy Excel archive
│   │
│   └── images/
│       └── logo.png                # Corporate brand asset
│
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py    # Tests for ingestion, feature extraction, and RFM
│   ├── test_metrics.py        # Tests for KPI calculations, Pareto 80/20, BCG matrix
│   ├── test_scenario.py       # Tests for what-if simulation calculations
│   └── run_tests.py           # Standalone automated test runner script
│
└── data_query/
    ├── db.sql                 # SQL schema & PostgreSQL ingestion scripts
    └── superstore.csv         # Normalized database-ready CSV
```

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
Ensure you have **Python 3.10+** installed.

### 2. Clone and Setup Environment
```bash
# Navigate to project directory
cd "Superstore-Sales-Dashboard-with-Streamlit-main"

# Create a virtual environment (recommended)
python -m venv venv

# Activate environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### 3. Launch the Dashboard
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

---

## 🧪 Testing & Validation

The codebase includes comprehensive unit tests verifying data pipeline reliability, financial formulas, and scenario algorithms:

```bash
# Run the automated test runner:
python tests/run_tests.py

# Or run using pytest:
pytest tests/ -v
```

### Verified Test Cases:
- **`TestDataLoader`**: Validates file path resolution, column standardization, multi-format datetime parsing (`dayfirst=True`), feature derivations (`ship_days`, `profit_margin`, `cogs`), and quantile/percentile RFM scoring.
- **`TestMetrics`**: Validates executive KPI aggregation, Period-over-Period variance deltas, Pareto 80/20 cumulative sum math, and BCG median-split classification.
- **`TestScenario`**: Validates zero-baseline fidelity, price sensitivity accretion, discount policy elasticity, and cost inflation margin erosion.

---

## 📐 Data Dictionary & Business Metric Definitions

| Metric / Attribute | Definition | Business Relevance |
| :--- | :--- | :--- |
| **Sales Revenue** | $\sum \text{Sales}$ | Top-line transaction gross revenue |
| **Cost of Goods Sold (COGS)** | $\text{Sales} - \text{Profit}$ | Direct procurement and product inventory cost |
| **Net Profit** | $\sum \text{Profit}$ | Operating bottom-line contribution |
| **Profit Margin %** | $\frac{\text{Net Profit}}{\text{Sales Revenue}} \times 100$ | Margin efficiency; benchmarks department profitability |
| **Average Order Value (AOV)** | $\frac{\text{Sales Revenue}}{\text{Distinct Orders}}$ | Basket size; indicator of bundling and cross-sell health |
| **Fulfillment Lead Time** | $\text{Ship Date} - \text{Order Date}$ (days) | Carrier efficiency; customer delivery SLA latency |
| **Discount Tier** | Categorized into $0\%$, $1\text{--}20\%$, $21\text{--}40\%$, $>40\%$ | Diagnoses promo elasticity and profit destruction thresholds |
| **RFM Cohort** | Quantile scores across Recency, Frequency, Spend | Prioritizes high-LTV customer accounts vs churn risks |

---

## 💼 Built for BI & Analytics Professionals

- **Modular & Maintainable**: Separated into dedicated data ingestion, analytical metric, visualization, and view layers.
- **Performance Optimized**: Streamlit caching (`@st.cache_data`) minimizes redundant computations across filter adjustments.
- **Executive UI/UX**: Professional navy and slate styling, interactive Plotly visualizations with currency formatting, hover details, and responsive layout.

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
#   s t o r e - B I - p l a t f o r m  
 