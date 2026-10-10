import os
import pandas as pd
import numpy as np
from pathlib import Path

# Streamlit cache wrapper if streamlit is imported, else dummy wrapper
try:
    import streamlit as st
    cache_decorator = st.cache_data(show_spinner=False)
except Exception:
    def cache_decorator(func):
        return func


def find_dataset_path() -> Path:
    """
    Search for Superstore dataset file in known workspace directories.
    """
    # Current script directory
    base_dir = Path(__file__).resolve().parent.parent.parent
    potential_paths = [
        base_dir / "src" / "data" / "Superstore.csv",
        base_dir / "src" / "data" / "superstore.csv",
        base_dir / "data_query" / "superstore.csv",
        base_dir / "Superstore.csv",
        Path("src/data/Superstore.csv"),
        Path("data_query/superstore.csv")
    ]
    for path in potential_paths:
        if path.exists():
            return path
    raise FileNotFoundError("Superstore dataset CSV file could not be found.")


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize DataFrame column names to lowercase snake_case.
    """
    mapping = {
        "Row ID": "row_id",
        "Order ID": "order_id",
        "Order Date": "order_date",
        "Ship Date": "ship_date",
        "Ship Mode": "ship_mode",
        "Customer ID": "customer_id",
        "Customer Name": "customer_name",
        "Segment": "segment",
        "Country": "country",
        "City": "city",
        "State": "state",
        "Postal Code": "postal_code",
        "Region": "region",
        "Product ID": "product_id",
        "Category": "category",
        "Sub-Category": "sub_category",
        "Product Name": "product_name",
        "Sales": "sales",
        "Quantity": "quantity",
        "Discount": "discount",
        "Profit": "profit",
    }
    df = df.rename(columns=mapping)
    # Also standardize any remaining columns to lowercase with underscores
    df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    return df


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Robust date parser handling DD/MM/YYYY, YYYY-MM-DD, or mixed formats.
    """
    for col in ["order_date", "ship_date"]:
        if col in df.columns:
            # First try parsing with dayfirst=True for Superstore standard format
            try:
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
            except Exception:
                df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute derived BI metrics and temporal attributes.
    """
    # Ensure numeric columns
    numeric_cols = ["sales", "quantity", "discount", "profit"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    # Date-based dimensions
    if "order_date" in df.columns:
        df["order_year"] = df["order_date"].dt.year
        df["order_month"] = df["order_date"].dt.month
        df["order_month_name"] = df["order_date"].dt.strftime("%b")
        df["order_quarter"] = "Q" + df["order_date"].dt.quarter.astype(str)
        df["order_year_month"] = df["order_date"].dt.strftime("%Y-%m")
        df["order_day_name"] = df["order_date"].dt.strftime("%a")
        df["order_week"] = df["order_date"].dt.isocalendar().week.astype(int)

    # Lead time / shipping duration (days to ship)
    if "order_date" in df.columns and "ship_date" in df.columns:
        df["ship_days"] = (df["ship_date"] - df["order_date"]).dt.days
        df["ship_days"] = df["ship_days"].fillna(0).astype(int)
        # Shipping speed performance classification
        df["fulfillment_status"] = pd.cut(
            df["ship_days"],
            bins=[-float("inf"), 2, 5, float("inf")],
            labels=["Fast (<=2 days)", "Standard (3-5 days)", "Delayed (>5 days)"]
        )

    # Financial KPIs
    # Profit margin % = (Profit / Sales) * 100
    df["profit_margin"] = np.where(df["sales"] != 0, (df["profit"] / df["sales"]) * 100.0, 0.0)
    # Unit price and estimated unit cost
    df["unit_price"] = np.where(df["quantity"] > 0, df["sales"] / df["quantity"], df["sales"])
    df["cogs"] = df["sales"] - df["profit"]  # Cost of Goods Sold
    df["unit_cogs"] = np.where(df["quantity"] > 0, df["cogs"] / df["quantity"], 0.0)

    # Discount tiers
    df["discount_pct"] = df["discount"] * 100.0
    df["discount_tier"] = pd.cut(
        df["discount"],
        bins=[-0.001, 0.0, 0.20, 0.40, 1.0],
        labels=["No Discount (0%)", "Low (1-20%)", "Moderate (21-40%)", "High (>40%)"]
    )

    # Profitability flag
    df["is_profitable"] = df["profit"] > 0

    return df


def calculate_rfm_segments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate customer RFM (Recency, Frequency, Monetary) metrics and segmentation.
    Returns customer-level summary table with segment labels.
    """
    if "order_date" not in df.columns or "customer_id" not in df.columns:
        return pd.DataFrame()

    max_d = df["order_date"].max()
    reference_date = (max_d + pd.Timedelta(days=1)) if pd.notna(max_d) else pd.Timestamp.now()

    rfm = df.groupby("customer_id").agg(
        customer_name=("customer_name", "first"),
        segment=("segment", "first"),
        region=("region", "first"),
        recency=("order_date", lambda d: (reference_date - d.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_items=("quantity", "sum")
    ).reset_index()

    rfm["avg_order_value"] = rfm["monetary"] / rfm["frequency"].clip(lower=1)

    n_cust = len(rfm)
    if n_cust < 4:
        rfm["r_score"] = 4
        rfm["f_score"] = 4
        rfm["m_score"] = 4
    else:
        # Percentile ranking (0.0 to 1.0)
        # For Recency: fewer days = higher score
        r_perc = rfm["recency"].rank(method="first", ascending=False) / n_cust
        f_perc = rfm["frequency"].rank(method="first", ascending=True) / n_cust
        m_perc = rfm["monetary"].rank(method="first", ascending=True) / n_cust

        rfm["r_score"] = pd.cut(r_perc, bins=[-0.001, 0.25, 0.50, 0.75, 1.0], labels=[1, 2, 3, 4]).astype(int)
        rfm["f_score"] = pd.cut(f_perc, bins=[-0.001, 0.25, 0.50, 0.75, 1.0], labels=[1, 2, 3, 4]).astype(int)
        rfm["m_score"] = pd.cut(m_perc, bins=[-0.001, 0.25, 0.50, 0.75, 1.0], labels=[1, 2, 3, 4]).astype(int)

    rfm["rfm_score"] = rfm["r_score"].astype(str) + rfm["f_score"].astype(str) + rfm["m_score"].astype(str)

    # Segment mapping based on R and F scores
    def assign_rfm_segment(row):
        r = row["r_score"]
        f = row["f_score"]
        if r >= 4 and f >= 4:
            return "Champions"
        elif r >= 3 and f >= 3:
            return "Loyal Customers"
        elif r >= 3 and f <= 2:
            return "Potential Loyalists"
        elif r == 4 and f == 1:
            return "New / Recent Customers"
        elif r == 2 and f >= 3:
            return "At Risk"
        elif r == 1 and f >= 3:
            return "Can't Lose Them"
        elif r == 2 and f <= 2:
            return "Needs Attention"
        elif r == 1 and f <= 2:
            return "Hibernating / Lost"
        else:
            return "Promising"

    rfm["customer_segment"] = rfm.apply(assign_rfm_segment, axis=1)
    return rfm


@cache_decorator
def load_data(file_path: str = None) -> pd.DataFrame:
    """
    Main cached loader function. Ingests data, standardizes, enriches, and tags RFM segments.
    """
    if file_path is None:
        file_path = find_dataset_path()

    df = pd.read_csv(file_path, encoding="utf-8", low_memory=False)
    df = standardize_columns(df)
    df = parse_dates(df)
    df = engineer_features(df)

    # Compute and join customer segments
    rfm_df = calculate_rfm_segments(df)
    if not rfm_df.empty:
        segment_map = rfm_df.set_index("customer_id")["customer_segment"].to_dict()
        df["rfm_segment"] = df["customer_id"].map(segment_map).fillna("Unclassified")
    else:
        df["rfm_segment"] = "Standard"

    return df
