import pandas as pd
from sqlalchemy import text
from app.core.database import engine
from app.core.logger import get_logger

logger = get_logger(__name__)

def load_dimension(df: pd.DataFrame, table: str, conflict_col: str):
    with engine.begin() as conn:
        temp_table = f"temp_{table}"
        df.to_sql(temp_table, conn, if_exists="replace", index=False)

        cols = ", ".join(df.columns)
        update_cols = ", ".join(
            f"{c} = EXCLUDED.{c}"
            for c in df.columns if c != conflict_col
        )

        conn.execute(text(f"""
            INSERT INTO {table} ({cols})
            SELECT {cols} FROM {temp_table}
            ON CONFLICT ({conflict_col}) DO UPDATE SET {update_cols}
        """))
        conn.execute(text(f"DROP TABLE IF EXISTS {temp_table}"))

    logger.info(f"Loaded {len(df)} rows into {table}")

def load_fact(df: pd.DataFrame):
    with engine.begin() as conn:
        df.to_sql("fact_sales", conn, if_exists="append", index=False)
    logger.info(f"Loaded {len(df)} rows into fact_sales")

MATERIALIZED_VIEWS = [
    "mv_monthly_revenue",
    "mv_customer_summary",
]

def refresh_materialized_views():
    with engine.begin() as conn:
        for view in MATERIALIZED_VIEWS:
            conn.execute(text(f"REFRESH MATERIALIZED VIEW CONCURRENTLY {view}"))
    logger.info("Materialized views refreshed")