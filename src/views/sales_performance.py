import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.components.ui import (
    render_section_header,
    render_insight_box,
    format_currency,
    format_number
)
from src.components.charts import (
    plot_seasonality_heatmap,
    plot_discount_vs_profit,
    PALETTE,
    apply_bi_layout
)


def render_sales_performance_view(df: pd.DataFrame):
    """
    Render Sales & Financial Deep Dive tab.
    """
    if df.empty:
        st.warning("⚠️ No data available for selected criteria.")
        return

    render_section_header("Revenue Growth & Seasonality Patterns", "Time series behavior, seasonality matrices, and cyclical peaks")

    # Time Trend & Seasonality Heatmap
    col1, col2 = st.columns([1, 1])

    with col1:
        metric_choice = st.selectbox("Seasonality Metric:", ["sales", "profit"], format_func=lambda x: "Sales Revenue" if x == "sales" else "Net Profit", key="seas_metric")
        heat_fig = plot_seasonality_heatmap(df, metric=metric_choice)
        st.plotly_chart(heat_fig, use_container_width=True)

    with col2:
        # Cumulative Sales Curve by Year
        if "order_year" in df.columns and "order_date" in df.columns:
            df_cum = df.sort_values("order_date").copy()
            df_cum["day_of_year"] = df_cum["order_date"].dt.dayofyear

            cum_fig = go.Figure()
            for year, group in df_cum.groupby("order_year"):
                group_daily = group.groupby("day_of_year")["sales"].sum().reset_index()
                group_daily["cum_sales"] = group_daily["sales"].cumsum()
                cum_fig.add_trace(go.Scatter(
                    x=group_daily["day_of_year"],
                    y=group_daily["cum_sales"],
                    mode="lines",
                    name=f"FY {year}",
                    hovertemplate=f"FY {year}<br>Day %{{x}}: $%{{y:,.0f}}<extra></extra>"
                ))

            cum_fig = apply_bi_layout(cum_fig, "Cumulative Revenue Run-Rate by Year", height=320)
            cum_fig.update_layout(
                xaxis_title="Day of Fiscal Year (1 - 365)",
                yaxis=dict(title="Cumulative Sales ($)", tickprefix="$")
            )
            st.plotly_chart(cum_fig, use_container_width=True)
        else:
            st.info("Temporal date attributes unavailable for cumulative curve.")

    # Discount Diagnostics & Margin Erosion
    render_section_header("Discount Strategy & Margin Dilution Analysis", "Evaluating discount elasticity and profit erosion thresholds")

    d_col1, d_col2 = st.columns([3, 2])

    with d_col1:
        disc_fig = plot_discount_vs_profit(df)
        st.plotly_chart(disc_fig, use_container_width=True)

    with d_col2:
        # Discount tier breakdown table
        if "discount_tier" in df.columns:
            tier_summary = df.groupby("discount_tier", observed=False).agg(
                orders=("order_id", "nunique"),
                sales=("sales", "sum"),
                profit=("profit", "sum")
            ).reset_index()
            tier_summary["profit_margin"] = (tier_summary["profit"] / tier_summary["sales"] * 100).fillna(0.0)

            st.markdown("#### Discount Tier Performance")
            for _, r in tier_summary.iterrows():
                margin_color = "#10B981" if r["profit_margin"] >= 15 else ("#EF4444" if r["profit_margin"] < 0 else "#F59E0B")
                st.markdown(f"""
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 10px 14px; border-radius: 8px; margin-bottom: 8px;">
                        <div style="font-weight: 700; color: #1E293B;">{r['discount_tier']}</div>
                        <div style="display: flex; justify-content: space-between; font-size: 13px; color: #64748B; margin-top: 4px;">
                            <span>Sales: <b>${r['sales']:,.0f}</b></span>
                            <span>Orders: <b>{r['orders']:,}</b></span>
                            <span>Margin: <b style="color: {margin_color};">{r['profit_margin']:.1f}%</b></span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    # Executive Takeaway
    render_insight_box(
        "Discounts above 20% show negative average profitability across all departments. Transactions with 50%+ discounts generate significant operating losses. Superstore should establish automated guardrails capping sales rep discount discretion at 20%.",
        alert_type="warning",
        title="Pricing Policy Recommendation"
    )
