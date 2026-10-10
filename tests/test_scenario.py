import unittest
import pandas as pd
from src.utils.metrics import simulate_what_if


class TestScenario(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "sales": [1000.0, 2000.0],
            "profit": [200.0, 400.0],
            "discount": [0.10, 0.10]
        })

    def test_baseline_matches(self):
        # 0% changes across all levers
        res = simulate_what_if(
            self.df,
            price_change_pct=0.0,
            discount_change_pct=0.0,
            volume_change_pct=0.0,
            cost_change_pct=0.0
        )
        base = res["baseline"]
        proj = res["simulated"]
        var = res["variance"]

        self.assertEqual(base["sales"], 3000.0)
        self.assertEqual(base["profit"], 600.0)
        self.assertAlmostEqual(base["margin"], 20.0, places=2)

        self.assertAlmostEqual(proj["sales"], base["sales"], places=2)
        self.assertAlmostEqual(proj["profit"], base["profit"], places=2)
        self.assertAlmostEqual(var["sales_delta"], 0.0, places=2)
        self.assertAlmostEqual(var["profit_delta"], 0.0, places=2)

    def test_price_increase_improves_profit(self):
        # 10% price increase
        res = simulate_what_if(
            self.df,
            price_change_pct=10.0,
            discount_change_pct=0.0,
            volume_change_pct=0.0,
            cost_change_pct=0.0
        )
        self.assertGreater(res["simulated"]["profit"], res["baseline"]["profit"])
        self.assertGreater(res["simulated"]["margin"], res["baseline"]["margin"])

    def test_cost_inflation_erodes_margin(self):
        # 10% cost increase
        res = simulate_what_if(
            self.df,
            price_change_pct=0.0,
            discount_change_pct=0.0,
            volume_change_pct=0.0,
            cost_change_pct=10.0
        )
        self.assertLess(res["simulated"]["profit"], res["baseline"]["profit"])
        self.assertLess(res["simulated"]["margin"], res["baseline"]["margin"])

    def test_empty_dataframe_graceful(self):
        empty_df = pd.DataFrame(columns=["sales", "profit", "discount"])
        res = simulate_what_if(empty_df, 5.0, 0.0, 5.0, 0.0)
        self.assertEqual(res["baseline"]["sales"], 0.0)
        self.assertEqual(res["simulated"]["sales"], 0.0)


if __name__ == "__main__":
    unittest.main()
