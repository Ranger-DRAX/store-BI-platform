import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple


def calculate_core_kpis(df: pd.DataFrame, prior_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Compute core executive business intelligence KPIs with optional period-over-period deltas.
    """
    if df.empty:
        return {
            "total_sales": 0.0,
            "total_profit": 0.0,
            "profit_margin": 0.0,
            "total_orders": 0,
            "total_units": 0,
            "avg_order_value": 0.0,
            "avg_discount": 0.0,
            "deltas": {}
        }

    total_sales = float(df["sales"].sum())
    total_profit = float(df["profit"].sum())
    profit_margin = float((total_profit / total_sales * 100.0) if total_sales != 0 else 0.0)
    total_orders = int(df["order_id"].nunique())
    total_units = int(df["quantity"].sum())
    avg_order_value = float(total_sales / total_orders if total_orders > 0 else 0.0)
    avg_discount = float(df["discount"].mean() * 100.0 if "discount" in df.columns else 0.0)

    deltas = {}
    if prior_df is not None and not prior_df.empty:
        p_sales = float(prior_df["sales"].sum())
        p_profit = float(prior_df["profit"].sum())
        p_margin = float((p_profit / p_sales * 100.0) if p_sales != 0 else 0.0)
        p_orders = int(prior_df["order_id"].nunique())
        p_units = int(prior_df["quantity"].sum())
        p_aov = float(p_sales / p_orders if p_orders > 0 else 0.0)

        deltas["sales_pct"] = ((total_sales - p_sales) / p_sales * 100.0) if p_sales != 0 else 0.0
        deltas["profit_pct"] = ((total_profit - p_profit) / abs(p_profit) * 100.0) if p_profit != 0 else 0.0
        deltas["margin_pts"] = profit_margin - p_margin
        deltas["orders_pct"] = ((total_orders - p_orders) / p_orders * 100.0) if p_orders != 0 else 0.0
        deltas["units_pct"] = ((total_units - p_units) / p_units * 100.0) if p_units != 0 else 0.0
        deltas["aov_pct"] = ((avg_order_value - p_aov) / p_aov * 100.0) if p_aov != 0 else 0.0

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "profit_margin": profit_margin,
        "total_orders": total_orders,
        "total_units": total_units,
        "avg_order_value": avg_order_value,
        "avg_discount": avg_discount,
        "deltas": deltas
    }


def calculate_pareto(df: pd.DataFrame, dimension: str = "product_name", metric: str = "sales") -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    Perform Pareto 80/20 cumulative analysis.
    Returns the enriched DataFrame sorted descending with cumulative percentages,
    and a summary dict.
    """
    if df.empty or dimension not in df.columns or metric not in df.columns:
        return pd.DataFrame(), {"top_20_share": 0.0, "total_entities": 0, "entities_for_80_pct": 0}

    grouped = df.groupby(dimension)[metric].sum().reset_index()
    grouped = grouped.sort_values(by=metric, ascending=False).reset_index(drop=True)

    total_metric = grouped[metric].sum()
    if total_metric <= 0:
        return grouped, {"top_20_share": 0.0, "total_entities": len(grouped), "entities_for_80_pct": 0}

    grouped["cumulative_value"] = grouped[metric].cumsum()
    grouped["cumulative_pct"] = (grouped["cumulative_value"] / total_metric) * 100.0

    total_count = len(grouped)
    grouped["entity_rank"] = np.arange(1, total_count + 1)
    grouped["entity_pct"] = (grouped["entity_rank"] / total_count) * 100.0

    # Calculate 80/20 key checkpoints
    top_20_idx = int(np.ceil(total_count * 0.20))
    top_20_share = grouped.loc[:max(0, top_20_idx - 1), "cumulative_pct"].iloc[-1] if total_count > 0 else 0.0

    # How many entities make up 80%?
    eighty_pct_entities = len(grouped[grouped["cumulative_pct"] <= 80.0]) + 1
    eighty_pct_entities = min(eighty_pct_entities, total_count)

    summary = {
        "top_20_share": float(top_20_share),
        "total_entities": total_count,
        "entities_for_80_pct": eighty_pct_entities,
        "pct_entities_for_80": float((eighty_pct_entities / total_count) * 100.0) if total_count > 0 else 0.0
    }

    return grouped, summary


def calculate_bcg_matrix(df: pd.DataFrame, dimension: str = "sub_category") -> pd.DataFrame:
    """
    Classify categories or products into Strategic BI Quadrants (Sales Volume vs Profit Margin).
    Quadrants:
    - Stars: High Sales & High Margin
    - Cash Cows: High Sales & Low/Moderate Margin
    - Question Marks / Growth: Low Sales & High Margin
    - Underperformers: Low Sales & Low/Negative Margin
    """
    if df.empty or dimension not in df.columns:
        return pd.DataFrame()

    matrix = df.groupby(dimension).agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        avg_discount=("discount", "mean")
    ).reset_index()

    matrix["profit_margin"] = np.where(
        matrix["total_sales"] > 0,
        (matrix["total_profit"] / matrix["total_sales"]) * 100.0,
        0.0
    )

    sales_median = matrix["total_sales"].median()
    margin_median = matrix["profit_margin"].median()

    def classify_quadrant(row):
        high_sales = row["total_sales"] >= sales_median
        high_margin = row["profit_margin"] >= margin_median
        if high_sales and high_margin:
            return "Stars (High Vol / High Margin)"
        elif high_sales and not high_margin:
            return "Cash Cows (High Vol / Low Margin)"
        elif not high_sales and high_margin:
            return "Opportunities (Low Vol / High Margin)"
        else:
            return "Underperformers (Low Vol / Low Margin)"

    matrix["quadrant"] = matrix.apply(classify_quadrant, axis=1)
    matrix["sales_median"] = sales_median
    matrix["margin_median"] = margin_median

    return matrix


def simulate_what_if(
    df: pd.DataFrame,
    price_change_pct: float,
    discount_change_pct: float,
    volume_change_pct: float,
    cost_change_pct: float
) -> Dict[str, Any]:
    """
    Simulate financial impact under custom executive assumptions.
    - price_change_pct: % change in baseline list prices (e.g., +5.0)
    - discount_change_pct: % change in average discounts (e.g., -10.0 means tighter discount policy)
    - volume_change_pct: % change in unit sales volume (e.g., +8.0)
    - cost_change_pct: % change in Cost of Goods Sold / COGS inflation (e.g., +3.0)
    """
    base_sales = float(df["sales"].sum()) if not df.empty else 0.0
    base_profit = float(df["profit"].sum()) if not df.empty else 0.0
    base_cogs = base_sales - base_profit
    base_margin = (base_profit / base_sales * 100.0) if base_sales > 0 else 0.0

    volume_mult = 1.0 + (volume_change_pct / 100.0)
    price_mult = 1.0 + (price_change_pct / 100.0)
    # If baseline discount is d, adjusted discount is d * (1 + discount_change_pct/100)
    base_avg_discount = float(df["discount"].mean()) if not df.empty and "discount" in df.columns else 0.15
    new_avg_discount = max(0.0, min(0.9, base_avg_discount * (1.0 + discount_change_pct / 100.0)))
    discount_effect = (1.0 - new_avg_discount) / max(0.01, (1.0 - base_avg_discount))

    # Simulated Sales
    sim_sales = base_sales * volume_mult * price_mult * discount_effect

    # Simulated COGS
    cost_mult = 1.0 + (cost_change_pct / 100.0)
    sim_cogs = base_cogs * volume_mult * cost_mult

    # Simulated Profit
    sim_profit = sim_sales - sim_cogs
    sim_margin = (sim_profit / sim_sales * 100.0) if sim_sales > 0 else 0.0

    return {
        "baseline": {
            "sales": base_sales,
            "cogs": base_cogs,
            "profit": base_profit,
            "margin": base_margin
        },
        "simulated": {
            "sales": sim_sales,
            "cogs": sim_cogs,
            "profit": sim_profit,
            "margin": sim_margin
        },
        "variance": {
            "sales_delta": sim_sales - base_sales,
            "sales_delta_pct": ((sim_sales - base_sales) / base_sales * 100.0) if base_sales > 0 else 0.0,
            "profit_delta": sim_profit - base_profit,
            "profit_delta_pct": ((sim_profit - base_profit) / abs(base_profit) * 100.0) if base_profit != 0 else 0.0,
            "margin_delta_pts": sim_margin - base_margin
        }
    }
