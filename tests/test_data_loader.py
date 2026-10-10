import unittest
import pandas as pd
import numpy as np
from pathlib import Path
from src.utils.data_loader import (
    find_dataset_path,
    standardize_columns,
    parse_dates,
    engineer_features,
    calculate_rfm_segments,
    load_data
)


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.sample_raw_data = pd.DataFrame({
            "Row ID": [1, 2, 3],
            "Order ID": ["CA-2016-1001", "CA-2016-1001", "CA-2017-1002"],
            "Order Date": ["08/11/2016", "08/11/2016", "15/04/2017"],
            "Ship Date": ["11/11/2016", "11/11/2016", "20/04/2017"],
            "Ship Mode": ["Second Class", "Second Class", "Standard Class"],
            "Customer ID": ["CG-12520", "CG-12520", "AA-10480"],
            "Customer Name": ["Claire Gute", "Claire Gute", "Andrew Allen"],
            "Segment": ["Consumer", "Consumer", "Corporate"],
            "Country": ["United States", "United States", "United States"],
            "City": ["Henderson", "Henderson", "Concord"],
            "State": ["Kentucky", "Kentucky", "North Carolina"],
            "Postal Code": [42420, 42420, 28027],
            "Region": ["South", "South", "South"],
            "Product ID": ["FUR-BO-100", "FUR-CH-200", "OFF-PA-300"],
            "Category": ["Furniture", "Furniture", "Office Supplies"],
            "Sub-Category": ["Bookcases", "Chairs", "Paper"],
            "Product Name": ["Bookcase Deluxe", "Ergonomic Chair", "Copy Paper"],
            "Sales": [260.0, 740.0, 100.0],
            "Quantity": [2, 3, 5],
            "Discount": [0.0, 0.1, 0.2],
            "Profit": [40.0, 180.0, 20.0]
        })

    def test_find_dataset_path(self):
        path = find_dataset_path()
        self.assertTrue(path.exists(), f"Dataset path {path} does not exist.")
        self.assertTrue(path.is_file(), f"Dataset path {path} is not a file.")

    def test_standardize_columns(self):
        df = standardize_columns(self.sample_raw_data.copy())
        expected_cols = ["row_id", "order_id", "order_date", "ship_date", "ship_mode",
                         "customer_id", "customer_name", "segment", "country", "city",
                         "state", "postal_code", "region", "product_id", "category",
                         "sub_category", "product_name", "sales", "quantity", "discount", "profit"]
        for col in expected_cols:
            self.assertIn(col, df.columns, f"Expected column {col} was missing after standardization.")

    def test_parse_dates(self):
        df = standardize_columns(self.sample_raw_data.copy())
        df = parse_dates(df)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df["order_date"]))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df["ship_date"]))
        # Verify 08/11/2016 parsed as 8th of November 2016
        first_date = df["order_date"].iloc[0]
        self.assertEqual(first_date.year, 2016)
        self.assertEqual(first_date.month, 11)
        self.assertEqual(first_date.day, 8)

    def test_engineer_features(self):
        df = standardize_columns(self.sample_raw_data.copy())
        df = parse_dates(df)
        df = engineer_features(df)

        # Check temporal features
        self.assertIn("order_year", df.columns)
        self.assertIn("order_month", df.columns)
        self.assertIn("order_quarter", df.columns)
        self.assertIn("order_year_month", df.columns)

        # Check lead time
        self.assertIn("ship_days", df.columns)
        self.assertEqual(df["ship_days"].iloc[0], 3)  # 11 - 8 = 3 days

        # Check financial metrics
        self.assertIn("profit_margin", df.columns)
        self.assertIn("unit_price", df.columns)
        self.assertIn("cogs", df.columns)

        # First row: sales 260, profit 40 -> margin = (40 / 260) * 100 = 15.38%
        expected_margin = (40.0 / 260.0) * 100.0
        self.assertAlmostEqual(df["profit_margin"].iloc[0], expected_margin, places=2)

        # COGS = 260 - 40 = 220
        self.assertEqual(df["cogs"].iloc[0], 220.0)

    def test_calculate_rfm_segments(self):
        df = standardize_columns(self.sample_raw_data.copy())
        df = parse_dates(df)
        df = engineer_features(df)
        rfm = calculate_rfm_segments(df)

        self.assertFalse(rfm.empty)
        self.assertIn("customer_id", rfm.columns)
        self.assertIn("recency", rfm.columns)
        self.assertIn("frequency", rfm.columns)
        self.assertIn("monetary", rfm.columns)
        self.assertIn("customer_segment", rfm.columns)
        self.assertEqual(len(rfm), 2)  # 2 distinct customers

    def test_load_data_end_to_end(self):
        df = load_data()
        self.assertGreater(len(df), 9000, "Superstore dataset should contain over 9,000 rows.")
        self.assertIn("profit_margin", df.columns)
        self.assertIn("rfm_segment", df.columns)
        self.assertIn("order_year", df.columns)


if __name__ == "__main__":
    unittest.main()
