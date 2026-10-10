import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

from src.utils.data_loader import load_data
from src.components.ui import (
    load_custom_css,
    render_dashboard_header,
    render_filter_summary
)
from src.views.overview import render_overview_view
from src.views.sales_performance import render_sales_performance_view
from src.views.product_intelligence import render_product_intelligence_view
from src.views.customer_analytics import render_customer_analytics_view
from src.views.logistics_geo import render_logistics_geo_view
from src.views.scenario_planner import render_scenario_planner_view
from src.views.data_explorer import render_data_explorer_view

# Streamlit Page Configuration
st.set_page_config(
    page_title="Superstore Business Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom Modern BI CSS
load_custom_css()


def main():
    # 1. Ingest Data
    try:
        raw_df = load_data()
    except Exception as e:
        st.error(f"❌ Failed to load dataset: {e}")
        st.info("Ensure `Superstore.csv` exists in `src/data/` or `data_query/`.")
        return

    # 2. Sidebar Branding & Filtering Controls
    with st.sidebar:
        logo_path = Path("src/images/logo.png")
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
        else:
            st.markdown("### 🏢 SUPERSTORE BI")

        st.markdown("---")
        st.markdown("### 🎯 Global BI Filters")

        # Date Range Filter
        min_date = raw_df["order_date"].min().date() if "order_date" in raw_df.columns else datetime(2014, 1, 1).date()
        max_date = raw_df["order_date"].max().date() if "order_date" in raw_df.columns else datetime(2017, 12, 31).date()

        date_preset = st.selectbox(
            "Calendar Window:",
            options=["All Time", "FY 2017", "FY 2016", "FY 2015", "FY 2014", "Custom Range"],
            index=0
        )

        prior_df = None
        filter_date_str = "All Time"

        if date_preset == "All Time":
            start_date, end_date = min_date, max_date
            filter_date_str = f"{start_date.strftime('%b %Y')} - {end_date.strftime('%b %Y')}"
        elif date_preset == "FY 2017":
            start_date, end_date = datetime(2017, 1, 1).date(), datetime(2017, 12, 31).date()
            filter_date_str = "FY 2017"
            prior_df = raw_df[(raw_df["order_date"].dt.year == 2016)]
        elif date_preset == "FY 2016":
            start_date, end_date = datetime(2016, 1, 1).date(), datetime(2016, 12, 31).date()
            filter_date_str = "FY 2016"
            prior_df = raw_df[(raw_df["order_date"].dt.year == 2015)]
        elif date_preset == "FY 2015":
            start_date, end_date = datetime(2015, 1, 1).date(), datetime(2015, 12, 31).date()
            filter_date_str = "FY 2015"
            prior_df = raw_df[(raw_df["order_date"].dt.year == 2014)]
        elif date_preset == "FY 2014":
            start_date, end_date = datetime(2014, 1, 1).date(), datetime(2014, 12, 31).date()
            filter_date_str = "FY 2014"
        else:
            date_range = st.date_input(
                "Custom Date Range:",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            if isinstance(date_range, tuple) and len(date_range) == 2:
                start_date, end_date = date_range
                filter_date_str = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
                delta_days = (end_date - start_date).days
                p_end = start_date - timedelta(days=1)
                p_start = p_end - timedelta(days=delta_days)
                prior_df = raw_df[(raw_df["order_date"].dt.date >= p_start) & (raw_df["order_date"].dt.date <= p_end)]
            else:
                start_date, end_date = min_date, max_date

        # Multi-select Dimension Filters
        regions = sorted(raw_df["region"].dropna().unique().tolist())
        selected_regions = st.multiselect("Territory / Region:", options=regions, default=regions)

        segments = sorted(raw_df["segment"].dropna().unique().tolist())
        selected_segments = st.multiselect("Customer Segment:", options=segments, default=segments)

        categories = sorted(raw_df["category"].dropna().unique().tolist())
        selected_categories = st.multiselect("Product Category:", options=categories, default=categories)

        # Dynamic subcategory based on category selection
        subcat_df = raw_df[raw_df["category"].isin(selected_categories)] if selected_categories else raw_df
        subcats = sorted(subcat_df["sub_category"].dropna().unique().tolist())
        selected_subcats = st.multiselect("Sub-Category:", options=subcats, default=[])

        ship_modes = sorted(raw_df["ship_mode"].dropna().unique().tolist())
        selected_ship_modes = st.multiselect("Ship Mode:", options=ship_modes, default=ship_modes)

        # Filter Reset Button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reset to Default Filters", use_container_width=True):
            st.rerun()

        st.markdown("---")
        st.markdown("""
            <div style="font-size: 11px; color: #64748B; line-height: 1.4;">
                <b>Superstore BI Platform v2.0</b><br>
                Engineered for Business Intelligence Analysts, Strategy Teams, and Executives.
            </div>
        """, unsafe_allow_html=True)

    # 3. Apply Filters to Dataset
    df = raw_df.copy()
    if "order_date" in df.columns:
        df = df[(df["order_date"].dt.date >= start_date) & (df["order_date"].dt.date <= end_date)]

    if selected_regions:
        df = df[df["region"].isin(selected_regions)]
        if prior_df is not None:
            prior_df = prior_df[prior_df["region"].isin(selected_regions)]

    if selected_segments:
        df = df[df["segment"].isin(selected_segments)]
        if prior_df is not None:
            prior_df = prior_df[prior_df["segment"].isin(selected_segments)]

    if selected_categories:
        df = df[df["category"].isin(selected_categories)]
        if prior_df is not None:
            prior_df = prior_df[prior_df["category"].isin(selected_categories)]

    if selected_subcats:
        df = df[df["sub_category"].isin(selected_subcats)]
        if prior_df is not None:
            prior_df = prior_df[prior_df["sub_category"].isin(selected_subcats)]

    if selected_ship_modes:
        df = df[df["ship_mode"].isin(selected_ship_modes)]
        if prior_df is not None:
            prior_df = prior_df[prior_df["ship_mode"].isin(selected_ship_modes)]

    # 4. Top Header Banner
    render_dashboard_header(
        total_records=len(df),
        date_range_str=filter_date_str
    )

    # Active Filters Summary
    active_filters_meta = {
        "date_range": filter_date_str,
        "region": selected_regions if len(selected_regions) < len(regions) else None,
        "category": selected_categories if len(selected_categories) < len(categories) else None,
        "segment": selected_segments if len(selected_segments) < len(segments) else None,
        "ship_mode": selected_ship_modes if len(selected_ship_modes) < len(ship_modes) else None
    }
    render_filter_summary(active_filters_meta)

    # 5. Executive Tab Navigation
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Executive Overview",
        "📈 Sales & Financials",
        "📦 Product Portfolio (BCG & Pareto)",
        "👥 Customer RFM Intelligence",
        "🚚 Logistics & Regional Map",
        "🔮 What-If Scenario Planner",
        "📋 Data Explorer & Export"
    ])

    with tab1:
        render_overview_view(df, prior_df)

    with tab2:
        render_sales_performance_view(df)

    with tab3:
        render_product_intelligence_view(df)

    with tab4:
        render_customer_analytics_view(df)

    with tab5:
        render_logistics_geo_view(df)

    with tab6:
        render_scenario_planner_view(df)

    with tab7:
        render_data_explorer_view(df)


if __name__ == "__main__":
    main()
