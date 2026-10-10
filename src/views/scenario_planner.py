import streamlit as st
import pandas as pd
import numpy as np
from src.utils.metrics import simulate_what_if
from src.components.ui import (
    render_kpi_card,
    render_section_header,
    render_insight_box,
    format_currency
)
from src.components.charts import (
    plot_scenario_waterfall,
    PALETTE,
    apply_bi_layout
)
import plotly.express as px


def render_scenario_planner_view(df: pd.DataFrame):
    """
    Render Executive What-If Sensitivity Planner tab.
    """
    if df.empty:
        st.warning("⚠️ Baseline dataset is empty. Adjust filters to load transactions.")
        return

    render_section_header("Strategic What-If Scenario Simulator", "Simulate executive policy decisions, pricing elasticity, and cost inflation")

    # Simulation Parameter Sliders
    st.markdown("#### 🎛️ Simulation Decision Levers")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        price_adj = st.slider(
            "Price Adjustment (%):",
            min_value=-20.0,
            max_value=20.0,
            value=0.0,
            step=0.5,
            help="Simulate general increase or decrease in baseline list pricing",
            key="sim_price"
        )
    with col2:
        disc_adj = st.slider(
            "Discount Policy Shift (%):",
            min_value=-50.0,
            max_value=50.0,
            value=0.0,
            step=5.0,
            help="Negative percentage means tighter discount discipline (e.g., -20% reduces average discount by 20%)",
            key="sim_disc"
        )
    with col3:
        vol_adj = st.slider(
            "Sales Volume Demand (%):",
            min_value=-30.0,
            max_value=50.0,
            value=0.0,
            step=1.0,
            help="Projected change in total units purchased",
            key="sim_vol"
        )
    with col4:
        cost_adj = st.slider(
            "COGS / Cost Inflation (%):",
            min_value=-20.0,
            max_value=30.0,
            value=0.0,
            step=1.0,
            help="Change in supplier costs and procurement overhead",
            key="sim_cost"
        )

    # Run Simulation
    sim = simulate_what_if(
        df,
        price_change_pct=price_adj,
        discount_change_pct=disc_adj,
        volume_change_pct=vol_adj,
        cost_change_pct=cost_adj
    )

    base = sim["baseline"]
    proj = sim["simulated"]
    var = sim["variance"]

    # Comparative Executive Cards
    st.markdown("#### 📊 Projected Financial Results vs Baseline")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        render_kpi_card(
            title="Projected Revenue",
            value_str=format_currency(proj["sales"]),
            delta=var["sales_delta_pct"],
            context=f"Variance: {format_currency(var['sales_delta'])}",
            accent_class="kpi-accent-primary"
        )
    with c2:
        render_kpi_card(
            title="Projected COGS",
            value_str=format_currency(proj["cogs"]),
            delta=((proj["cogs"] - base["cogs"]) / base["cogs"] * 100) if base["cogs"] > 0 else 0,
            is_positive_good=False,
            context=f"Variance: {format_currency(proj['cogs'] - base['cogs'])}",
            accent_class="kpi-accent-warning"
        )
    with c3:
        render_kpi_card(
            title="Projected Net Profit",
            value_str=format_currency(proj["profit"]),
            delta=var["profit_delta_pct"],
            context=f"Delta: {format_currency(var['profit_delta'])}",
            accent_class="kpi-accent-success" if var["profit_delta"] >= 0 else "kpi-accent-danger"
        )
    with c4:
        render_kpi_card(
            title="Projected Margin",
            value_str=f"{proj['margin']:.1f}%",
            delta=var["margin_delta_pts"],
            delta_type="pts",
            context=f"Baseline: {base['margin']:.1f}%",
            accent_class="kpi-accent-purple"
        )

    # Visualizations Row: Waterfall Bridge and Sensitivity Matrix
    render_section_header("P&L Profit Variance Bridge & Sensitivity Heatmap", "Decomposing value drivers and multi-variable matrix")

    v_col1, v_col2 = st.columns([1, 1])

    with v_col1:
        waterfall_fig = plot_scenario_waterfall(sim)
        st.plotly_chart(waterfall_fig, use_container_width=True)

    with v_col2:
        # Sensitivity Table: Price vs Volume grid on Net Profit
        price_steps = [-10, -5, 0, 5, 10]
        vol_steps = [-10, -5, 0, 5, 10]
        sens_data = []

        for p in price_steps:
            row_data = []
            for v in vol_steps:
                s = simulate_what_if(df, price_change_pct=p, discount_change_pct=disc_adj, volume_change_pct=v, cost_change_pct=cost_adj)
                row_data.append(s["simulated"]["profit"])
            sens_data.append(row_data)

        sens_df = pd.DataFrame(
            sens_data,
            index=[f"Price {p:+d}%" for p in price_steps],
            columns=[f"Vol {v:+d}%" for v in vol_steps]
        )

        sens_fig = px.imshow(
            sens_df,
            labels=dict(x="Volume Shift", y="Price Shift", color="Net Profit ($)"),
            x=sens_df.columns,
            y=sens_df.index,
            color_continuous_scale="RdYlGn",
            text_auto="$,.0f"
        )
        sens_fig = apply_bi_layout(sens_fig, "Price vs Volume Sensitivity Matrix (Net Profit $)", height=360)
        st.plotly_chart(sens_fig, use_container_width=True)

    # Executive Strategic Commentary
    if var["profit_delta"] > 0:
        render_insight_box(
            f"Simulated policy creates an estimated profit increase of **{format_currency(var['profit_delta'])}** (+{var['profit_delta_pct']:.1f}%), expanding profit margin by **{var['margin_delta_pts']:+.1f} percentage points**.",
            alert_type="success",
            title="Strategic Financial Value Add"
        )
    elif var["profit_delta"] < 0:
        render_insight_box(
            f"Simulated scenario would compress profit by **{format_currency(abs(var['profit_delta']))}** (-{abs(var['profit_delta_pct']):.1f}%), reducing operating margin by **{abs(var['margin_delta_pts']):.1f} percentage points**.",
            alert_type="warning",
            title="Margin Dilution Warning"
        )
    else:
        render_insight_box(
            "Current sliders match baseline operations. Adjust price, discount, volume, or cost parameters above to simulate strategic scenarios.",
            alert_type="info",
            title="Baseline Simulation Ready"
        )
