# app/etl/transformer.py
import pandas as pd
import numpy as np
from app.core.logger import get_logger

logger = get_logger(__name__)

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # column cleaning
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # date column convertion
    for col in ["order_date", "ship_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    # miss values
    df["postal_code"] = df["postal_code"].fillna("UNKNOWN").astype(str)
    df = df.dropna(subset=["order_id", "customer_id", "product_id"])

    logger.info(f"Cleaned dataframe: {len(df)} rows remaining")
    return df

def create_date_key(date: pd.Timestamp) -> int:
    return int(date.strftime("%Y%m%d"))

def build_dim_customer(df: pd.DataFrame) -> pd.DataFrame:
    return df[[
        "customer_id", "customer_name", "segment",
        "city", "state", "country", "region", "postal_code"
    ]].drop_duplicates(subset=["customer_id"]).reset_index(drop=True)

def build_dim_product(df: pd.DataFrame) -> pd.DataFrame:
    return df[[
        "product_id", "product_name", "category", "sub_category"
    ]].drop_duplicates(subset=["product_id"]).reset_index(drop=True)

def build_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    dates = pd.concat([df["order_date"], df["ship_date"]]).dropna().unique()
    date_series = pd.Series(pd.to_datetime(dates))

    dim_date = pd.DataFrame({
        "date_sk":    date_series.dt.strftime("%Y%m%d").astype(int),
        "full_date":  date_series,
        "year":       date_series.dt.year,
        "quarter":    date_series.dt.quarter,
        "month":      date_series.dt.month,
        "month_name": date_series.dt.strftime("%B"),
        "week":       date_series.dt.isocalendar().week.astype(int),
        "day_of_week":date_series.dt.dayofweek,
        "day_name":   date_series.dt.strftime("%A"),
        "is_weekend": date_series.dt.dayofweek >= 5
    }).drop_duplicates(subset=["date_sk"]).sort_values("date_sk")

    return dim_date

def build_fact_sales(
    df: pd.DataFrame,
    customer_map: dict,
    product_map: dict
) -> pd.DataFrame:
    fact = df.copy()
    fact["order_date_sk"] = fact["order_date"].apply(create_date_key)
    fact["ship_date_sk"]  = fact["ship_date"].apply(create_date_key)
    fact["customer_sk"]   = fact["customer_id"].map(customer_map)
    fact["product_sk"]    = fact["product_id"].map(product_map)

    return fact[[
        "order_id", "order_date_sk", "ship_date_sk",
        "customer_sk", "product_sk", "ship_mode",
        "quantity", "sales", "discount", "profit"
    ]].rename(columns={"sales": "sales_amount"})