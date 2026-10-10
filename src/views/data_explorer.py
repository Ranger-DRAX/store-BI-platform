import streamlit as st
import pandas as pd
from src.components.ui import (
    render_section_header,
    format_currency,
    format_number
)


def render_data_explorer_view(df: pd.DataFrame):
    """
    Render Ad-Hoc Data Explorer & BI Report Builder tab.
    """
    if df.empty:
        st.warning("⚠️ No data available to explore with current filter criteria.")
        return

    render_section_header("Ad-Hoc Pivot & Aggregation Builder", "Dynamically group and summarize metrics across business dimensions")

    # Group By Builder
    p_col1, p_col2 = st.columns([1, 2])

    dimension_options = ["category", "sub_category", "segment", "region", "state", "ship_mode", "rfm_segment"]
    avail_dims = [d for d in dimension_options if d in df.columns]

    with p_col1:
        group_dims = st.multiselect(
            "Select Grouping Dimensions:",
            options=avail_dims,
            default=["category", "sub_category"] if "sub_category" in avail_dims else [avail_dims[0]],
            key="pivot_dims"
        )

    with p_col2:
        if group_dims:
            pivot_df = df.groupby(group_dims).agg(
                sales=("sales", "sum"),
                profit=("profit", "sum"),
                quantity=("quantity", "sum"),
                orders=("order_id", "nunique"),
                avg_discount=("discount", "mean")
            ).reset_index()

            pivot_df["profit_margin"] = (pivot_df["profit"] / pivot_df["sales"] * 100).fillna(0.0)
            pivot_df = pivot_df.sort_values(by="sales", ascending=False)

            st.dataframe(
                pivot_df.rename(columns={
                    "sales": "Sales ($)",
                    "profit": "Profit ($)",
                    "profit_margin": "Margin (%)",
                    "quantity": "Units Sold",
                    "orders": "Orders",
                    "avg_discount": "Avg Discount"
                }),
                column_config={
                    "Sales ($)": st.column_config.NumberColumn(format="$%.2f"),
                    "Profit ($)": st.column_config.NumberColumn(format="$%.2f"),
                    "Margin (%)": st.column_config.NumberColumn(format="%.1f%%"),
                    "Avg Discount": st.column_config.NumberColumn(format="%.2f")
                },
                hide_index=True,
                use_container_width=True
            )

            # Download Pivot CSV
            pivot_csv = pivot_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Aggregated Summary (CSV)",
                data=pivot_csv,
                file_name="superstore_aggregated_summary.csv",
                mime="text/csv",
                key="dl_pivot_csv"
            )

    # Granular Transaction Explorer
    render_section_header("Transactional Ledger & Export Engine", "Search, filter, inspect granular order records, and download")

    search_query = st.text_input(
        "🔍 Search transactions by Customer Name, Order ID, or Product:",
        "",
        key="table_search"
    )

    filtered_view = df.copy()
    if search_query.strip():
        q = search_query.strip().lower()
        filtered_view = filtered_view[
            filtered_view["customer_name"].astype(str).str.lower().str.contains(q) |
            filtered_view["order_id"].astype(str).str.lower().str.contains(q) |
            filtered_view["product_name"].astype(str).str.lower().str.contains(q)
        ]

    # Column selection
    default_cols = [
        "order_id", "order_date", "customer_name", "segment", "region", "state",
        "category", "sub_category", "product_name", "sales", "quantity", "discount", "profit"
    ]
    all_cols = filtered_view.columns.tolist()
    valid_defaults = [c for c in default_cols if c in all_cols]

    selected_cols = st.multiselect(
        "Customize Table Columns:",
        options=all_cols,
        default=valid_defaults,
        key="table_cols"
    )

    st.markdown(f"Displaying **{len(filtered_view):,}** rows")
    st.dataframe(
        filtered_view[selected_cols].head(500),
        use_container_width=True,
        hide_index=True
    )

    # Export Buttons
    e_col1, e_col2 = st.columns([1, 3])
    with e_col1:
        csv_data = filtered_view.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_data,
            file_name="superstore_filtered_transactions.csv",
            mime="text/csv",
            key="dl_trans_csv"
        )
