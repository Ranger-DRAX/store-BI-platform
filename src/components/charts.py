import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, Any

# Standard US State Name to 2-letter Code mapping for Choropleth
US_STATE_TO_CODE = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "District of Columbia": "DC"
}

# Theme Configuration
CHART_FONT = dict(family="Plus Jakarta Sans, sans-serif", size=12, color="#334155")
PALETTE = {
    "primary": "#2563EB",
    "secondary": "#3B82F6",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "purple": "#8B5CF6",
    "teal": "#0D9488",
    "slate": "#64748B",
    "bg_subtle": "rgba(248, 250, 252, 0.8)",
    "grid": "#E2E8F0"
}


def apply_bi_layout(fig: go.Figure, title: str = "", height: int = 380) -> go.Figure:
    """
    Standardize layout styling for all business intelligence charts.
    """
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(family="Plus Jakarta Sans, sans-serif", size=15, color="#1E293B"),
            x=0.01,
            y=0.97
        ),
        font=CHART_FONT,
        height=height,
        margin=dict(l=20, r=20, t=45, b=25),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11)
        ),
        hoverlabel=dict(
            bgcolor="#1E293B",
            font_size=12,
            font_family="Plus Jakarta Sans, sans-serif",
            font_color="#FFFFFF"
        )
    )
    fig.update_xaxes(showgrid=True, gridcolor=PALETTE["grid"], showline=True, linecolor="#CBD5E1")
    fig.update_yaxes(showgrid=True, gridcolor=PALETTE["grid"], showline=True, linecolor="#CBD5E1")
    return fig


def plot_sales_profit_trend(df: pd.DataFrame, freq: str = "Month") -> go.Figure:
    """
    Dual-axis time series chart displaying Sales revenue (bars) and Profit (line)
    with a rolling 3-period moving average.
    """
    if df.empty or "order_date" not in df.columns:
        fig = go.Figure()
        return apply_bi_layout(fig, "No Data Available")

    df_sorted = df.copy()
    if freq == "Quarter":
        df_sorted["period"] = df_sorted["order_year"].astype(str) + "-" + df_sorted["order_quarter"]
    else:
        df_sorted["period"] = df_sorted["order_year_month"]

    grouped = df_sorted.groupby("period").agg(
        sales=("sales", "sum"),
        profit=("profit", "sum")
    ).reset_index().sort_values("period")

    grouped["sales_ma"] = grouped["sales"].rolling(window=3, min_periods=1).mean()

    fig = go.Figure()

    # Sales Bars
    fig.add_trace(go.Bar(
        x=grouped["period"],
        y=grouped["sales"],
        name="Sales Revenue",
        marker_color="rgba(37, 99, 235, 0.75)",
        marker_line=dict(color="#1D4ED8", width=1),
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>"
    ))

    # Sales Moving Average
    fig.add_trace(go.Scatter(
        x=grouped["period"],
        y=grouped["sales_ma"],
        mode="lines",
        name="3-Period Sales Trend",
        line=dict(color="#60A5FA", width=2, dash="dash"),
        hovertemplate="3-Period MA: $%{y:,.2f}<extra></extra>"
    ))

    # Profit Line on Secondary Axis
    fig.add_trace(go.Scatter(
        x=grouped["period"],
        y=grouped["profit"],
        mode="lines+markers",
        name="Net Profit",
        line=dict(color=PALETTE["success"], width=3),
        marker=dict(size=6, color="#059669"),
        yaxis="y2",
        hovertemplate="Profit: $%{y:,.2f}<extra></extra>"
    ))

    fig = apply_bi_layout(fig, f"Revenue & Profit Trajectory ({freq}ly)", height=390)

    fig.update_layout(
        yaxis=dict(
            title="Sales Revenue ($)",
            titlefont=dict(color=PALETTE["primary"]),
            tickfont=dict(color=PALETTE["primary"]),
            tickprefix="$",
            showgrid=True
        ),
        yaxis2=dict(
            title="Net Profit ($)",
            titlefont=dict(color=PALETTE["success"]),
            tickfont=dict(color=PALETTE["success"]),
            tickprefix="$",
            overlaying="y",
            side="right",
            showgrid=False
        )
    )

    return fig


def plot_seasonality_heatmap(df: pd.DataFrame, metric: str = "sales") -> go.Figure:
    """
    Heatmap displaying seasonal performance (Year vs Month).
    """
    if df.empty or "order_year" not in df.columns or "order_month" not in df.columns:
        fig = go.Figure()
        return apply_bi_layout(fig, "No Seasonality Data")

    pivot = df.pivot_table(
        index="order_year",
        columns="order_month",
        values=metric,
        aggfunc="sum",
        fill_value=0
    )

    # Convert month numbers to month names
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    pivot.columns = [month_names[m - 1] for m in pivot.columns]

    metric_label = "Sales Revenue ($)" if metric == "sales" else "Net Profit ($)"
    colorscale = "Blues" if metric == "sales" else "Greens"

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.astype(str).tolist(),
        colorscale=colorscale,
        colorbar=dict(title=metric_label),
        hovertemplate="<b>%{y} - %{x}</b><br>Value: $%{z:,.2f}<extra></extra>"
    ))

    fig = apply_bi_layout(fig, f"Annual Seasonality Heatmap ({metric_label})", height=320)
    fig.update_layout(xaxis_title="Month", yaxis_title="Fiscal Year")
    return fig


def plot_subcategory_margin_bar(df: pd.DataFrame) -> go.Figure:
    """
    Horizontal bar chart of sub-categories ranked by Sales, color-coded by Profit Margin %.
    Highlights profitable vs margin-dilutive product categories.
    """
    if df.empty or "sub_category" not in df.columns:
        fig = go.Figure()
        return apply_bi_layout(fig, "No Subcategory Data")

    summary = df.groupby("sub_category").agg(
        sales=("sales", "sum"),
        profit=("profit", "sum")
    ).reset_index()

    summary["profit_margin"] = np.where(
        summary["sales"] > 0,
        (summary["profit"] / summary["sales"]) * 100.0,
        0.0
    )
    summary = summary.sort_values(by="sales", ascending=True)

    # Color scale: green for high margin, red for negative margin
    colors = [
        PALETTE["danger"] if m < 0 else (PALETTE["warning"] if m < 15 else PALETTE["success"])
        for m in summary["profit_margin"]
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=summary["sub_category"],
        x=summary["sales"],
        orientation="h",
        marker=dict(color=colors),
        text=[f"${s:,.0f} | Margin: {m:.1f}%" for s, m in zip(summary["sales"], summary["profit_margin"])],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.2f}<br>Profit Margin: %{customdata:.2f}%<extra></extra>",
        customdata=summary["profit_margin"]
    ))

    fig = apply_bi_layout(fig, "Sub-Category Sales Volume & Profit Margin Health", height=500)
    fig.update_layout(
        xaxis=dict(title="Total Sales ($)", tickprefix="$"),
        yaxis=dict(title=""),
        margin=dict(r=120)
    )
    return fig


def plot_pareto_chart(pareto_df: pd.DataFrame, summary: Dict[str, Any], top_n: int = 30) -> go.Figure:
    """
    Pareto 80/20 dual-axis chart showing individual contributions and cumulative curve.
    """
    if pareto_df.empty:
        fig = go.Figure()
        return apply_bi_layout(fig, "No Pareto Data")

    display_df = pareto_df.head(top_n).copy()

    fig = go.Figure()

    # Individual Sales Bar
    fig.add_trace(go.Bar(
        x=display_df["product_name"].str[:28] + "...",
        y=display_df["sales"],
        name="Product Sales",
        marker_color="rgba(37, 99, 235, 0.7)",
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>"
    ))

    # Cumulative Percentage Line
    fig.add_trace(go.Scatter(
        x=display_df["product_name"].str[:28] + "...",
        y=display_df["cumulative_pct"],
        mode="lines+markers",
        name="Cumulative %",
        line=dict(color=PALETTE["danger"], width=2.5),
        yaxis="y2",
        hovertemplate="Cumulative: %{y:.1f}%<extra></extra>"
    ))

    # 80% Benchmark Reference Line
    fig.add_shape(
        type="line",
        x0=0,
        x1=1,
        xref="paper",
        y0=80,
        y1=80,
        yref="y2",
        line=dict(color="#DC2626", width=2, dash="dash")
    )

    fig.add_annotation(
        text="80% Revenue Cutoff",
        xref="paper",
        yref="y2",
        x=0.02,
        y=82,
        showarrow=False,
        font=dict(color="#DC2626", size=11, family="Plus Jakarta Sans, sans-serif")
    )

    fig = apply_bi_layout(fig, f"Pareto 80/20 Distribution (Top {top_n} Products)", height=420)
    fig.update_layout(
        xaxis=dict(tickangle=-45),
        yaxis=dict(title="Sales Revenue ($)", tickprefix="$"),
        yaxis2=dict(
            title="Cumulative Revenue (%)",
            ticksuffix="%",
            overlaying="y",
            side="right",
            range=[0, 105],
            showgrid=False
        )
    )
    return fig


def plot_bcg_quadrant_matrix(bcg_df: pd.DataFrame) -> go.Figure:
    """
    Strategic Portfolio Matrix (Sales Volume vs Profit Margin %).
    Separates entities into Stars, Cash Cows, Opportunities, and Underperformers.
    """
    if bcg_df.empty:
        fig = go.Figure()
        return apply_bi_layout(fig, "No Portfolio Data")

    color_map = {
        "Stars (High Vol / High Margin)": PALETTE["success"],
        "Cash Cows (High Vol / Low Margin)": PALETTE["primary"],
        "Opportunities (Low Vol / High Margin)": PALETTE["purple"],
        "Underperformers (Low Vol / Low Margin)": PALETTE["danger"]
    }

    fig = px.scatter(
        bcg_df,
        x="total_sales",
        y="profit_margin",
        size="total_quantity",
        color="quadrant",
        color_discrete_map=color_map,
        hover_name="sub_category",
        hover_data={"total_sales": ":$,.2f", "profit_margin": ":.1f%", "total_profit": ":$,.2f", "total_quantity": ":,"},
        labels={
            "total_sales": "Sales Volume ($)",
            "profit_margin": "Profit Margin (%)",
            "quadrant": "Strategic Classification"
        }
    )

    # Add Median Quadrant Dividers
    sales_mid = bcg_df["sales_median"].iloc[0]
    margin_mid = bcg_df["margin_median"].iloc[0]

    fig.add_vline(x=sales_mid, line_dash="dash", line_color="#94A3B8", annotation_text="Median Sales", annotation_position="top left")
    fig.add_hline(y=margin_mid, line_dash="dash", line_color="#94A3B8", annotation_text="Median Margin", annotation_position="bottom right")

    fig = apply_bi_layout(fig, "Strategic Portfolio Quadrant Matrix (BCG Framework)", height=430)
    fig.update_layout(
        xaxis=dict(tickprefix="$", showgrid=True),
        yaxis=dict(ticksuffix="%", showgrid=True)
    )
    return fig


def plot_us_state_choropleth(df: pd.DataFrame, metric: str = "sales") -> go.Figure:
    """
    Interactive United States Map (Choropleth) for Sales, Profit, or Profit Margin %.
    """
    if df.empty or "state" not in df.columns:
        fig = go.Figure()
        return apply_bi_layout(fig, "No Geographic Data")

    state_agg = df.groupby("state").agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
        quantity=("quantity", "sum")
    ).reset_index()

    state_agg["profit_margin"] = np.where(
        state_agg["sales"] > 0,
        (state_agg["profit"] / state_agg["sales"]) * 100.0,
        0.0
    )
    state_agg["state_code"] = state_agg["state"].map(US_STATE_TO_CODE)
    state_agg = state_agg.dropna(subset=["state_code"])

    metric_name = "Sales ($)" if metric == "sales" else ("Profit ($)" if metric == "profit" else "Profit Margin (%)")
    target_col = "sales" if metric == "sales" else ("profit" if metric == "profit" else "profit_margin")
    color_scale = "Blues" if metric == "sales" else ("Greens" if metric == "profit" else "Spectral")

    fig = px.choropleth(
        state_agg,
        locations="state_code",
        locationmode="USA-states",
        color=target_col,
        scope="usa",
        color_continuous_scale=color_scale,
        hover_name="state",
        hover_data={
            "state_code": False,
            "sales": ":$,.2f",
            "profit": ":$,.2f",
            "profit_margin": ":.1f%",
            "orders": ":,"
        },
        labels={target_col: metric_name}
    )

    fig.update_layout(
        geo=dict(bgcolor="rgba(0,0,0,0)", lakecolor="#F1F5F9"),
        margin=dict(l=0, r=0, t=35, b=0),
        height=380,
        title=dict(
            text=f"<b>Geographic Distribution: State {metric_name}</b>",
            font=dict(family="Plus Jakarta Sans, sans-serif", size=15, color="#1E293B"),
            x=0.02
        )
    )
    return fig


def plot_rfm_segments(rfm_df: pd.DataFrame) -> go.Figure:
    """
    Treemap displaying Customer RFM Segments weighted by Monetary Value.
    """
    if rfm_df.empty or "customer_segment" not in rfm_df.columns:
        fig = go.Figure()
        return apply_bi_layout(fig, "No RFM Data")

    seg_summary = rfm_df.groupby("customer_segment").agg(
        customer_count=("customer_id", "count"),
        total_revenue=("monetary", "sum"),
        total_profit=("total_profit", "sum"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean")
    ).reset_index()

    fig = px.treemap(
        seg_summary,
        path=["customer_segment"],
        values="total_revenue",
        color="total_profit",
        color_continuous_scale="RdYlGn",
        hover_data={
            "customer_count": ":,",
            "total_revenue": ":$,.2f",
            "total_profit": ":$,.2f",
            "avg_recency": ":.1f days",
            "avg_frequency": ":.1f orders"
        },
        labels={
            "total_revenue": "Total Sales",
            "total_profit": "Net Profit ($)",
            "customer_count": "Customers"
        }
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=35, b=10),
        height=380,
        title=dict(
            text="<b>Customer RFM Segmentation Treemap (Sized by Sales, Colored by Profit)</b>",
            font=dict(family="Plus Jakarta Sans, sans-serif", size=15, color="#1E293B"),
            x=0.01
        )
    )
    return fig


def plot_discount_vs_profit(df: pd.DataFrame) -> go.Figure:
    """
    Diagnostic analysis showing the Discount Cliff where profit margins turn negative.
    """
    if df.empty or "discount" not in df.columns or "profit_margin" not in df.columns:
        fig = go.Figure()
        return apply_bi_layout(fig, "No Discount Data")

    # Group by discrete discount percentages
    grouped = df.groupby(df["discount"].round(2)).agg(
        avg_margin=("profit_margin", "mean"),
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        order_count=("order_id", "count")
    ).reset_index()

    grouped["discount_pct"] = grouped["discount"] * 100.0

    colors = [PALETTE["danger"] if m < 0 else PALETTE["success"] for m in grouped["avg_margin"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grouped["discount_pct"],
        y=grouped["avg_margin"],
        marker=dict(color=colors),
        hovertemplate="<b>Discount: %{x:.0f}%</b><br>Average Margin: %{y:.1f}%<extra></extra>"
    ))

    fig.add_hline(y=0, line_color="#0F172A", line_width=1.5)

    # Highlight threshold
    fig.add_vrect(
        x0=20, x1=max(grouped["discount_pct"]),
        fillcolor="rgba(239, 68, 68, 0.12)",
        line_width=0,
        annotation_text="Severe Margin Erosion Zone (>20% Discount)",
        annotation_position="top right"
    )

    fig = apply_bi_layout(fig, "Discount Sensitivity & Margin Erosion Curve", height=350)
    fig.update_layout(
        xaxis=dict(title="Discount Level (%)", ticksuffix="%"),
        yaxis=dict(title="Average Profit Margin (%)", ticksuffix="%")
    )
    return fig


def plot_shipping_duration(df: pd.DataFrame) -> go.Figure:
    """
    Logistics lead time distribution across Shipping Modes.
    """
    if df.empty or "ship_mode" not in df.columns or "ship_days" not in df.columns:
        fig = go.Figure()
        return apply_bi_layout(fig, "No Shipping Data")

    fig = px.box(
        df,
        x="ship_mode",
        y="ship_days",
        color="ship_mode",
        color_discrete_sequence=[PALETTE["primary"], PALETTE["teal"], PALETTE["purple"], PALETTE["warning"]],
        points="outliers",
        labels={"ship_mode": "Shipping Mode", "ship_days": "Lead Time (Days to Ship)"}
    )

    fig = apply_bi_layout(fig, "Fulfillment Lead Time (Order-to-Ship Days by Mode)", height=350)
    fig.update_layout(showlegend=False)
    return fig


def plot_scenario_waterfall(sim_results: Dict[str, Any]) -> go.Figure:
    """
    Waterfall chart illustrating bridge from Baseline Profit to Simulated Profit.
    """
    base_p = sim_results["baseline"]["profit"]
    sim_p = sim_results["simulated"]["profit"]
    p_delta = sim_results["variance"]["profit_delta"]

    # Decompose into illustrative bridge components
    fig = go.Figure(go.Waterfall(
        name="Profit Bridge",
        orientation="v",
        measure=["absolute", "relative", "total"],
        x=["Baseline Net Profit", "Simulated Variance", "Projected Net Profit"],
        textposition="outside",
        text=[f"${base_p:,.0f}", f"{'+' if p_delta>=0 else ''}${p_delta:,.0f}", f"${sim_p:,.0f}"],
        y=[base_p, p_delta, sim_p],
        connector={"line": {"color": "#94A3B8"}},
        decreasing={"marker": {"color": PALETTE["danger"]}},
        increasing={"marker": {"color": PALETTE["success"]}},
        totals={"marker": {"color": PALETTE["primary"]}}
    ))

    fig = apply_bi_layout(fig, "Executive P&L Profitability Bridge", height=360)
    fig.update_layout(yaxis=dict(title="Net Profit ($)", tickprefix="$"))
    return fig
