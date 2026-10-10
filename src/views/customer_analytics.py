import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils.data_loader import calculate_rfm_segments
from src.components.ui import (
    render_section_header,
    render_insight_box,
    format_currency,
    format_number
)
from src.components.charts import (
    plot_rfm_segments,
    PALETTE,
    apply_bi_layout
)


def render_customer_analytics_view(df: pd.DataFrame):
    """
    Render Customer Intelligence & RFM Segmentation tab.
    """
    if df.empty or "customer_id" not in df.columns:
        st.warning("⚠️ No customer records match the current filter selection.")
        return

    render_section_header("Customer RFM Segmentation Matrix", "Recency, Frequency, and Monetary valuation model")

    # Compute RFM for filtered dataset
    rfm_df = calculate_rfm_segments(df)

    if not rfm_df.empty:
        # Treemap
        treemap_fig = plot_rfm_segments(rfm_df)
        st.plotly_chart(treemap_fig, use_container_width=True)

        # Segment KPI Metrics Summary
        seg_kpis = rfm_df.groupby("customer_segment").agg(
            customers=("customer_id", "count"),
            total_sales=("monetary", "sum"),
            total_profit=("total_profit", "sum"),
            avg_recency=("recency", "mean"),
            avg_orders=("frequency", "mean")
        ).reset_index()

        total_rev = seg_kpis["total_sales"].sum()
        total_cust = seg_kpis["customers"].sum()
        seg_kpis["rev_share"] = (seg_kpis["total_sales"] / total_rev * 100) if total_rev > 0 else 0
        seg_kpis["margin"] = (seg_kpis["total_profit"] / seg_kpis["total_sales"] * 100) if total_rev > 0 else 0

        st.markdown("#### Segment Distribution & Value Profile")
        st.dataframe(
            seg_kpis.rename(columns={
                "customer_segment": "Segment",
                "customers": "Customer Count",
                "total_sales": "Total Sales ($)",
                "total_profit": "Net Profit ($)",
                "margin": "Margin (%)",
                "rev_share": "Rev Share (%)",
                "avg_recency": "Avg Recency (Days)",
                "avg_orders": "Avg Orders"
            }),
            column_config={
                "Total Sales ($)": st.column_config.NumberColumn(format="$%.2f"),
                "Net Profit ($)": st.column_config.NumberColumn(format="$%.2f"),
                "Margin (%)": st.column_config.NumberColumn(format="%.1f%%"),
                "Rev Share (%)": st.column_config.NumberColumn(format="%.1f%%"),
                "Avg Recency (Days)": st.column_config.NumberColumn(format="%.0f days"),
                "Avg Orders": st.column_config.NumberColumn(format="%.1f")
            },
            hide_index=True,
            use_container_width=True
        )

    # Top Strategic Customer Accounts
    render_section_header("Top 15 Strategic Customer Accounts", "High-value enterprise and consumer client relationships")
    top_custs = rfm_df.sort_values(by="monetary", ascending=False).head(15)

    c_col1, c_col2 = st.columns([3, 2])
    with c_col1:
        st.dataframe(
            top_custs[["customer_name", "segment", "customer_segment", "monetary", "total_profit", "frequency", "avg_order_value"]].rename(columns={
                "customer_name": "Customer Name",
                "segment": "Market Segment",
                "customer_segment": "RFM Group",
                "monetary": "Lifetime Sales ($)",
                "total_profit": "Net Profit ($)",
                "frequency": "Orders",
                "avg_order_value": "AOV ($)"
            }),
            column_config={
                "Lifetime Sales ($)": st.column_config.NumberColumn(format="$%.2f"),
                "Net Profit ($)": st.column_config.NumberColumn(format="$%.2f"),
                "AOV ($)": st.column_config.NumberColumn(format="$%.2f")
            },
            hide_index=True,
            use_container_width=True
        )

    with c_col2:
        # Segment Action Playbook
        st.markdown("#### 📘 RFM Marketing Playbook")
        st.markdown("""
        - **🏆 Champions**: Reward with VIP loyalty perks, early access to new product lines, and personal account managers.
        - **💎 Loyal Customers**: Upsell higher-margin technology solutions and offer bundle incentives.
        - **⚠️ At Risk**: Trigger automated win-back campaigns and personalized re-engagement incentives.
        - **❄️ Hibernating / Lost**: Deliver aggressive clearance promotions or re-evaluate marketing outreach spend.
        """)

    render_insight_box(
        "Champions and Loyal Customers represent the majority of cumulative enterprise profitability despite constituting less than 35% of total account count. Prioritize retention and dedicated account support for accounts in the 'At Risk' quadrant.",
        alert_type="success",
        title="CRM Strategic Insight"
    )
