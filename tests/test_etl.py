import pytest
import pandas as pd
from app.etl.transformer import transform

class TestTransformer:
    @pytest.fixture
    def sample_df(self):
        return pd.DataFrame({
            "Order ID":       ["CA-2022-001", "CA-2022-001", "CA-2022-002"],
            "Order Date":     ["2022-01-15",  "2022-01-15",  "2022-03-10"],
            "Ship Date":      ["2022-01-20",  "2022-01-20",  "2022-03-15"],
            "Ship Mode":      ["Standard Class", "Standard Class", "First Class"],
            "Customer ID":    ["CUST-001",    "CUST-001",    "CUST-002"],
            "Customer Name":  ["Alice",       "Alice",       "Bob"],
            "Segment":        ["Consumer",    "Consumer",    "Corporate"],
            "City":           ["New York",    "New York",    "Chicago"],
            "State":          ["New York",    "New York",    "Illinois"],
            "Country":        ["US",          "US",          "US"],
            "Region":         ["East",        "East",        "Central"],
            "Postal Code":    ["10001",       "10001",       "60601"],
            "Product ID":     ["PROD-001",    "PROD-002",    "PROD-003"],
            "Product Name":   ["Stapler",     "Chair",       "Printer"],
            "Category":       ["Office Supplies", "Furniture", "Technology"],
            "Sub-Category":   ["Fasteners",   "Chairs",      "Machines"],
            "Quantity":       [5,             1,             2],
            "Sales":          [19.95,         450.00,        758.00],
            "Discount":       [0.0,           0.1,           0.2],
            "Profit":         [3.99,          81.00,         91.0],
        })

    def test_transform_returns_dict_of_dataframes(self, sample_df):
        result = transform(sample_df)
        assert isinstance(result, dict)
        for key in ("customers", "products", "dates", "sales"):
            assert key in result, f"'{key}' transform çıktısında eksik"

    def test_customers_deduplication(self, sample_df):
        result = transform(sample_df)
        # CA-2022-001'de aynı müşteri 2 satırda var, tekil olmalı
        assert result["customers"]["customer_id"].nunique() == len(result["customers"])

    def test_date_sk_format(self, sample_df):
        result = transform(sample_df)
        # date_sk YYYYMMDD formatında integer olmalı
        date_sk = result["dates"]["date_sk"].iloc[0]
        assert isinstance(date_sk, (int,)) or str(date_sk).isdigit()
        assert len(str(date_sk)) == 8