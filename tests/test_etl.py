import pandas as pd
import pytest

from app.etl.extractor import DataExtractor
from app.etl.transformer import Transformer, transform


class TestTransformer:
    @pytest.fixture
    def sample_df(self):
        return pd.DataFrame(
            {
                "Order ID": ["CA-2022-001", "CA-2022-001", "CA-2022-002"],
                "Order Date": ["2022-01-15", "2022-01-15", "2022-03-10"],
                "Ship Date": ["2022-01-20", "2022-01-20", "2022-03-15"],
                "Ship Mode": ["Standard Class", "Standard Class", "First Class"],
                "Customer ID": ["CUST-001", "CUST-001", "CUST-002"],
                "Customer Name": ["Alice", "Alice", "Bob"],
                "Segment": ["Consumer", "Consumer", "Corporate"],
                "City": ["New York", "New York", "Chicago"],
                "State": ["New York", "New York", "Illinois"],
                "Country": ["US", "US", "US"],
                "Region": ["East", "East", "Central"],
                "Postal Code": ["10001", "10001", "60601"],
                "Product ID": ["PROD-001", "PROD-002", "PROD-003"],
                "Product Name": ["Stapler", "Chair", "Printer"],
                "Category": ["Office Supplies", "Furniture", "Technology"],
                "Sub-Category": ["Fasteners", "Chairs", "Machines"],
                "Quantity": [5, 1, 2],
                "Sales": [19.95, 450.00, 758.00],
                "Discount": [0.0, 0.1, 0.2],
                "Profit": [3.99, 81.00, 91.0],
            }
        )

    def test_transform_returns_dict_of_dataframes(self, sample_df):
        result = transform(sample_df)

        assert isinstance(result, dict)
        for key in ("customers", "products", "dates", "sales"):
            assert key in result
            assert isinstance(result[key], pd.DataFrame)

    def test_customers_deduplication(self, sample_df):
        result = transform(sample_df)

        assert result["customers"]["customer_id"].nunique() == len(result["customers"])

    def test_date_sk_format(self, sample_df):
        result = transform(sample_df)
        date_sk = result["dates"]["date_sk"].iloc[0]

        assert isinstance(date_sk, int) or str(date_sk).isdigit()
        assert len(str(date_sk)) == 8

    def test_clean_normalizes_columns_and_dates(self, sample_df):
        cleaned = Transformer(sample_df).clean().df

        assert "order_id" in cleaned.columns
        assert "sub_category" in cleaned.columns
        assert pd.api.types.is_datetime64_any_dtype(cleaned["order_date"])
        assert pd.api.types.is_datetime64_any_dtype(cleaned["ship_date"])

    def test_fact_sales_uses_surrogate_keys(self, sample_df):
        transformer = Transformer(sample_df).clean()
        fact = transformer.build_fact_sales(
            customer_map={"CUST-001": 10, "CUST-002": 20},
            product_map={"PROD-001": 100, "PROD-002": 200, "PROD-003": 300},
        )

        assert set(fact["customer_sk"]) == {10, 20}
        assert set(fact["product_sk"]) == {100, 200, 300}
        assert "sales_amount" in fact.columns
        assert "sales" not in fact.columns

    def test_extractor_reads_cp1252_csv(self, tmp_path):
        csv_path = tmp_path / "sample.csv"
        csv_path.write_bytes("name,amount\nA\xa0B,1\n".encode("cp1252"))

        df = DataExtractor(str(csv_path)).extract_csv()

        assert len(df) == 1
        assert df.loc[0, "amount"] == 1
