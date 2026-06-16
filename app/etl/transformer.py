import pandas as pd
from app.core.logger import get_logger

logger = get_logger(__name__)


class Transformer:
    """
    ETL transformation layer:
    - data cleaning
    - dimension building
    - fact table construction
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    # -----------------------------
    # CORE CLEANING
    # -----------------------------
    def clean(self) -> "Transformer":
        """Normalize schema + handle missing values + type casting"""

        # normalize column names
        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
        )

        # datetime conversion
        for col in ["order_date", "ship_date"]:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors="coerce")

        # missing handling
        if "postal_code" in self.df.columns:
            self.df["postal_code"] = (
                self.df["postal_code"]
                .fillna("UNKNOWN")
                .astype(str)
            )

        # critical keys validation
        self.df = self.df.dropna(subset=[
            "order_id",
            "customer_id",
            "product_id"
        ])

        logger.info(f"[Transformer] Cleaned rows: {len(self.df)}")
        return self

    # -----------------------------
    # DATE UTIL
    # -----------------------------
    @staticmethod
    def create_date_key(date: pd.Timestamp) -> int:
        if pd.isna(date):
            return None
        return int(date.strftime("%Y%m%d"))

    # -----------------------------
    # DIMENSIONS
    # -----------------------------
    def build_dim_customer(self) -> pd.DataFrame:
        return (
            self.df[[
                "customer_id", "customer_name", "segment",
                "city", "state", "country", "region", "postal_code"
            ]]
            .drop_duplicates(subset=["customer_id"])
            .reset_index(drop=True)
        )

    def build_dim_product(self) -> pd.DataFrame:
        return (
            self.df[[
                "product_id", "product_name", "category", "sub_category"
            ]]
            .drop_duplicates(subset=["product_id"])
            .reset_index(drop=True)
        )

    def build_dim_date(self) -> pd.DataFrame:
        dates = pd.concat([
            self.df.get("order_date"),
            self.df.get("ship_date")
        ]).dropna().unique()

        date_series = pd.Series(pd.to_datetime(dates))

        dim_date = pd.DataFrame({
            "date_sk": date_series.dt.strftime("%Y%m%d").astype(int),
            "full_date": date_series,
            "year": date_series.dt.year,
            "quarter": date_series.dt.quarter,
            "month": date_series.dt.month,
            "month_name": date_series.dt.strftime("%B"),
            "week": date_series.dt.isocalendar().week.astype(int),
            "day_of_week": date_series.dt.dayofweek,
            "day_name": date_series.dt.strftime("%A"),
            "is_weekend": date_series.dt.dayofweek >= 5
        })

        dim_date = (
            dim_date
            .drop_duplicates(subset=["date_sk"])
            .sort_values("date_sk")
            .reset_index(drop=True)
        )

        return dim_date

    # -----------------------------
    # FACT TABLE
    # -----------------------------
    def build_fact_sales(
        self,
        customer_map: dict,
        product_map: dict
    ) -> pd.DataFrame:

        fact = self.df.copy()

        fact["order_date_sk"] = fact["order_date"].apply(self.create_date_key)
        fact["ship_date_sk"] = fact["ship_date"].apply(self.create_date_key)

        fact["customer_sk"] = fact["customer_id"].map(customer_map)
        fact["product_sk"] = fact["product_id"].map(product_map)

        fact = fact[[
            "order_id",
            "order_date_sk",
            "ship_date_sk",
            "customer_sk",
            "product_sk",
            "ship_mode",
            "quantity",
            "sales",
            "discount",
            "profit"
        ]].rename(columns={"sales": "sales_amount"})

        logger.info(f"[Transformer] Fact rows: {len(fact)}")
        return fact

    # -----------------------------
    # PIPELINE WRAPPER (OPTIONAL)
    # -----------------------------
    def run(self) -> pd.DataFrame:
        """If you want simple execution chain"""
        return self.clean().df


def transform(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Build all warehouse-ready dataframes from a raw Superstore dataframe.
    """
    transformer = Transformer(df).clean()

    return {
        "customers": transformer.build_dim_customer(),
        "products": transformer.build_dim_product(),
        "dates": transformer.build_dim_date(),
        "sales": transformer.df,
    }
