import streamlit as st
import pandas as pd
import plotly.express as px
from src.components.ui import (
    render_section_header,
    render_insight_box,
    format_currency
)
from src.components.charts import (
    plot_us_state_choropleth,
    plot_shipping_duration,
    PALETTE,
    apply_bi_layout
)


def render_logistics_geo_view(df: pd.DataFrame):
    """
    Render Geographic & Logistics Diagnostics tab.
    """
    if df.empty:
        st.warning("⚠️ No geographical or shipping records match the current filter selection.")
        return

    render_section_header("Geographic Market Penetration & Profitability", "State-level choropleth visualization and regional metrics")

    # Map Controls
    map_metric = st.radio(
        "Select Map Metric:",
        ["sales", "profit", "margin"],
        format_func=lambda x: "Sales Revenue ($)" if x == "sales" else ("Net Profit ($)" if x == "profit" else "Profit Margin (%)"),
        horizontal=True,
        key="geo_metric"
    )

    map_fig = plot_us_state_choropleth(df, metric=map_metric)
    st.plotly_chart(map_fig, use_container_width=True)

    # Regional Performance Comparison
    render_section_header("Regional Matrix & Supply Chain KPIs", "Performance across West, East, Central, and South regions")

    r_col1, r_col2 = st.columns([1, 1])

    with r_col1:
        reg_summary = df.groupby("region").agg(
            sales=("sales", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "nunique"),
            avg_ship_days=("ship_days", "mean") if "ship_days" in df.columns else ("sales", "count")
        ).reset_index()

        reg_summary["profit_margin"] = (reg_summary["profit"] / reg_summary["sales"] * 100).fillna(0.0)

        reg_fig = px.bar(
            reg_summary,
            x="region",
            y="sales",
            color="profit_margin",
            color_continuous_scale="RdYlGn",
            labels={"sales": "Total Sales ($)", "region": "Region", "profit_margin": "Margin (%)"}
        )
        reg_fig = apply_bi_layout(reg_fig, "Regional Revenue with Margin Indicator", height=350)
        reg_fig.update_layout(yaxis=dict(tickprefix="$"))
        st.plotly_chart(reg_fig, use_container_width=True)

    with r_col2:
        st.markdown("#### Regional Summary Table")
        st.dataframe(
            reg_summary.rename(columns={
                "region": "Region",
                "sales": "Sales ($)",
                "profit": "Profit ($)",
                "profit_margin": "Margin (%)",
                "orders": "Orders",
                "avg_ship_days": "Avg Lead Time (Days)"
            }),
            column_config={
                "Sales ($)": st.column_config.NumberColumn(format="$%.2f"),
                "Profit ($)": st.column_config.NumberColumn(format="$%.2f"),
                "Margin (%)": st.column_config.NumberColumn(format="%.1f%%"),
                "Avg Lead Time (Days)": st.column_config.NumberColumn(format="%.1f days")
            },
            hide_index=True,
            use_container_width=True
        )

    # Shipping Duration & Fulfillment Lead Time
    render_section_header("Order Fulfillment Lead Time & Logistics SLA", "Dispatch latency and shipping carrier mode efficiency")

    s_col1, s_col2 = st.columns([3, 2])

    with s_col1:
        ship_fig = plot_shipping_duration(df)
        st.plotly_chart(ship_fig, use_container_width=True)

    with s_col2:
        if "ship_mode" in df.columns:
            ship_mode_agg = df.groupby("ship_mode").agg(
                orders=("order_id", "nunique"),
                sales=("sales", "sum"),
                avg_days=("ship_days", "mean")
            ).reset_index()

            st.markdown("#### Carrier Mode Fulfillment SLA")
            for _, r in ship_mode_agg.iterrows():
                st.markdown(f"""
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 10px 14px; border-radius: 8px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="color: #1E293B;">{r['ship_mode']}</strong>
                            <span style="background: #EFF6FF; color: #2563EB; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600;">
                                {r['avg_days']:.1f} avg days
                            </span>
                        </div>
                        <div style="font-size: 12px; color: #64748B; margin-top: 4px;">
                            Volume: {r['orders']:,} orders (${r['sales']:,.0f})
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    render_insight_box(
        "Central and South regions exhibit lower overall profit margins than West and East, driven by heavier discount promotional reliance. Standard Class shipping accounts for over 59% of order volume with a reliable 4-day delivery cycle.",
        alert_type="info",
        title="Supply Chain & Territory Takeaway"
    )
