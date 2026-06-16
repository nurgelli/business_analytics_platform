from pathlib import Path

from sqlalchemy import text

from app.core.database import engine, test_connection
from app.core.logger import get_logger
from app.etl.extractor import DataExtractor
from app.etl.loader import PostgresLoader
from app.etl.transformer import Transformer

logger = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV_PATH = PROJECT_ROOT / "data" / "raw" / "superstore.csv"


def _load_key_map(table: str, natural_key: str, surrogate_key: str) -> dict:
    query = text(f"SELECT {natural_key}, {surrogate_key} FROM {table}")
    with engine.connect() as conn:
        rows = conn.execute(query).mappings().all()
    return {row[natural_key]: row[surrogate_key] for row in rows}


def run(csv_path: str | Path = DEFAULT_CSV_PATH) -> None:
    csv_path = Path(csv_path)
    if not csv_path.is_absolute():
        csv_path = PROJECT_ROOT / csv_path

    logger.info(f"[ETL] Reading CSV from {csv_path}")

    if not test_connection():
        raise RuntimeError("Database connection failed. Check POSTGRES_HOST and POSTGRES_PORT.")

    raw_df = DataExtractor(str(csv_path)).extract_csv()
    transformer = Transformer(raw_df).clean()

    dim_customer = transformer.build_dim_customer()
    dim_product = transformer.build_dim_product()
    dim_date = transformer.build_dim_date()

    loader = PostgresLoader(engine)
    loader.load_dimension(dim_customer, "dim_customer", "customer_id")
    loader.load_dimension(dim_product, "dim_product", "product_id")
    loader.load_dimension(dim_date, "dim_date", "date_sk")

    customer_map = _load_key_map("dim_customer", "customer_id", "customer_sk")
    product_map = _load_key_map("dim_product", "product_id", "product_sk")
    fact_sales = transformer.build_fact_sales(customer_map, product_map)
    loader.truncate_table("fact_sales")
    loader.load_fact(fact_sales)

    loader.refresh_materialized_views([
        "mv_monthly_revenue",
        "mv_customer_summary",
    ])

    logger.info("[ETL] Pipeline completed successfully")


if __name__ == "__main__":
    run()
