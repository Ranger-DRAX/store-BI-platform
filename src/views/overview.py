import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils.metrics import calculate_core_kpis
from src.components.ui import (
    render_kpi_card,
    render_section_header,
    render_insight_box,
    format_currency,
    format_number
)
from src.components.charts import (
    plot_sales_profit_trend,
    PALETTE,
    apply_bi_layout
)


def render_overview_view(df: pd.DataFrame, prior_df: pd.DataFrame = None):
    """
    Render Executive Overview Tab.
    """
    if df.empty:
        st.warning("⚠️ No transactions match the current filter selection.")
        return

    # Calculate Core Executive KPIs
    kpis = calculate_core_kpis(df, prior_df)
    deltas = kpis.get("deltas", {})

    # Top Row: Executive KPI Cards
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        render_kpi_card(
            title="Total Revenue",
            value_str=format_currency(kpis["total_sales"]),
            delta=deltas.get("sales_pct"),
            is_positive_good=True,
            accent_class="kpi-accent-primary"
        )
    with col2:
        render_kpi_card(
            title="Net Profit",
            value_str=format_currency(kpis["total_profit"]),
            delta=deltas.get("profit_pct"),
            is_positive_good=True,
            accent_class="kpi-accent-success" if kpis["total_profit"] >= 0 else "kpi-accent-danger"
        )
    with col3:
        render_kpi_card(
            title="Profit Margin",
            value_str=f"{kpis['profit_margin']:.1f}%",
            delta=deltas.get("margin_pts"),
            delta_type="pts",
            is_positive_good=True,
            accent_class="kpi-accent-success" if kpis["profit_margin"] >= 12 else "kpi-accent-warning"
        )
    with col4:
        render_kpi_card(
            title="Total Orders",
            value_str=format_number(kpis["total_orders"]),
            delta=deltas.get("orders_pct"),
            is_positive_good=True,
            accent_class="kpi-accent-purple"
        )
    with col5:
        render_kpi_card(
            title="Avg Order Value",
            value_str=format_currency(kpis["avg_order_value"]),
            delta=deltas.get("aov_pct"),
            is_positive_good=True,
            accent_class="kpi-accent-cyan"
        )
    with col6:
        render_kpi_card(
            title="Avg Discount",
            value_str=f"{kpis['avg_discount']:.1f}%",
            delta=None,
            context="Effective Rate",
            accent_class="kpi-accent-warning"
        )

    # Executive Diagnostic Alert
    unprofitable_subs = df.groupby("sub_category")["profit"].sum()
    loss_making = unprofitable_subs[unprofitable_subs < 0]
    if len(loss_making) > 0:
        names = ", ".join([f"**{k}** (${abs(v):,.0f} loss)" for k, v in loss_making.items()])
        render_insight_box(
            f"Unprofitable product lines detected: {names}. Consider tightening discount thresholds for these items.",
            alert_type="warning",
            title="Executive Margin Alert"
        )
    else:
        render_insight_box(
            f"All product sub-categories in this selection are delivering positive net profit. Overall portfolio margin is healthy at {kpis['profit_margin']:.1f}%.",
            alert_type="success",
            title="Portfolio Health"
        )

    # Row 1: Trend and Category Distribution
    render_section_header("Sales Trajectory & Category Contribution", "Financial trajectory over time vs product mix")
    r1_col1, r1_col2 = st.columns([3, 2])

    with r1_col1:
        freq_opt = st.radio("Frequency Aggregation:", ["Month", "Quarter"], horizontal=True, key="overview_freq")
        trend_fig = plot_sales_profit_trend(df, freq=freq_opt)
        st.plotly_chart(trend_fig, use_container_width=True)

    with r1_col2:
        cat_agg = df.groupby("category").agg(
            sales=("sales", "sum"),
            profit=("profit", "sum")
        ).reset_index()

        cat_fig = px.pie(
            cat_agg,
            names="category",
            values="sales",
            hole=0.45,
            color="category",
            color_discrete_sequence=[PALETTE["primary"], PALETTE["teal"], PALETTE["purple"]]
        )
        cat_fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Sales: $%{value:,.2f}<br>Share: %{percent}<extra></extra>"
        )
        cat_fig = apply_bi_layout(cat_fig, "Revenue Contribution by Category", height=390)
        st.plotly_chart(cat_fig, use_container_width=True)

    # Row 2: Regional & Subcategory Performance
    render_section_header("Segment Dynamics & Regional Rankings", "Customer segments and geographic leaders")
    r2_col1, r2_col2 = st.columns([1, 1])

    with r2_col1:
        seg_agg = df.groupby(["segment", "category"]).agg(sales=("sales", "sum")).reset_index()
        seg_fig = px.bar(
            seg_agg,
            x="segment",
            y="sales",
            color="category",
            barmode="group",
            color_discrete_sequence=[PALETTE["primary"], PALETTE["teal"], PALETTE["purple"]],
            labels={"sales": "Sales ($)", "segment": "Customer Segment"}
        )
        seg_fig = apply_bi_layout(seg_fig, "Sales by Customer Segment & Category", height=360)
        seg_fig.update_layout(yaxis=dict(tickprefix="$"))
        st.plotly_chart(seg_fig, use_container_width=True)

    with r2_col2:
        top_states = df.groupby("state").agg(
            sales=("sales", "sum"),
            profit=("profit", "sum")
        ).reset_index().sort_values(by="sales", ascending=False).head(8)

        state_fig = px.bar(
            top_states,
            x="sales",
            y="state",
            orientation="h",
            color="profit",
            color_continuous_scale="Viridis",
            labels={"sales": "Sales ($)", "state": "", "profit": "Profit ($)"}
        )
        state_fig = apply_bi_layout(state_fig, "Top 8 States by Sales Revenue", height=360)
        state_fig.update_layout(
            yaxis=dict(autorange="reversed"),
            xaxis=dict(tickprefix="$")
        )
        st.plotly_chart(state_fig, use_container_width=True)
