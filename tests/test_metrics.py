import unittest
import pandas as pd
import numpy as np
from src.utils.metrics import (
    calculate_core_kpis,
    calculate_pareto,
    calculate_bcg_matrix
)


class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "order_id": ["O1", "O2", "O3", "O4"],
            "product_name": ["Product A", "Product B", "Product A", "Product C"],
            "sub_category": ["Chairs", "Tables", "Chairs", "Storage"],
            "sales": [500.0, 300.0, 200.0, 100.0],
            "profit": [100.0, -30.0, 50.0, 20.0],
            "quantity": [5, 2, 2, 1],
            "discount": [0.0, 0.4, 0.1, 0.0]
        })

    def test_calculate_core_kpis_base(self):
        kpis = calculate_core_kpis(self.df)
        self.assertEqual(kpis["total_sales"], 1100.0)
        self.assertEqual(kpis["total_profit"], 140.0)
        self.assertEqual(kpis["total_orders"], 4)
        self.assertEqual(kpis["total_units"], 10)
        self.assertEqual(kpis["avg_order_value"], 275.0)  # 1100 / 4
        # Margin = (140 / 1100) * 100 = 12.727%
        self.assertAlmostEqual(kpis["profit_margin"], 12.727, places=2)

    def test_calculate_core_kpis_with_prior(self):
        prior_df = pd.DataFrame({
            "order_id": ["P1", "P2"],
            "sales": [800.0, 200.0],
            "profit": [100.0, 0.0],
            "quantity": [8, 2],
            "discount": [0.1, 0.1]
        })
        kpis = calculate_core_kpis(self.df, prior_df=prior_df)
        deltas = kpis["deltas"]
        self.assertIn("sales_pct", deltas)
        self.assertIn("profit_pct", deltas)
        self.assertIn("margin_pts", deltas)
        # Sales: 1100 vs 1000 = +10.0%
        self.assertAlmostEqual(deltas["sales_pct"], 10.0, places=1)
        # Profit: 140 vs 100 = +40.0%
        self.assertAlmostEqual(deltas["profit_pct"], 40.0, places=1)

    def test_calculate_pareto(self):
        pareto_df, summary = calculate_pareto(self.df, dimension="product_name", metric="sales")
        self.assertFalse(pareto_df.empty)
        self.assertIn("cumulative_pct", pareto_df.columns)
        self.assertIn("entity_rank", pareto_df.columns)

        # Check total reaches 100%
        self.assertAlmostEqual(pareto_df["cumulative_pct"].iloc[-1], 100.0, places=1)

        # Check summary metrics exist
        self.assertIn("top_20_share", summary)
        self.assertIn("total_entities", summary)
        self.assertEqual(summary["total_entities"], 3)  # Product A, B, C

    def test_calculate_bcg_matrix(self):
        bcg_df = calculate_bcg_matrix(self.df, dimension="sub_category")
        self.assertFalse(bcg_df.empty)
        self.assertIn("quadrant", bcg_df.columns)
        self.assertIn("profit_margin", bcg_df.columns)

        # Chairs total sales = 700, profit = 150 -> margin = ~21.4%
        chairs_row = bcg_df[bcg_df["sub_category"] == "Chairs"].iloc[0]
        self.assertAlmostEqual(chairs_row["total_sales"], 700.0)
        self.assertAlmostEqual(chairs_row["total_profit"], 150.0)

        # Tables total sales = 300, profit = -30 -> margin = -10.0% (Underperformer)
        tables_row = bcg_df[bcg_df["sub_category"] == "Tables"].iloc[0]
        self.assertAlmostEqual(tables_row["profit_margin"], -10.0)


if __name__ == "__main__":
    unittest.main()
