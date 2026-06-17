# app/etl/loader.py

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from app.core.logger import get_logger

logger = get_logger(__name__)


class PostgresLoader:
    def __init__(self, engine: Engine):
        self.engine = engine

    def load_dimension(self, df: pd.DataFrame, table: str, conflict_col: str) -> None:

        if df.empty:
            logger.warning(f"{table} Empty dataframe, skipping load.")
            return

        with self.engine.begin() as conn:
            temp_table = f"temp_{table}"

            # Stage data
            df.to_sql(temp_table, conn, if_exists="replace", index=False)

            cols = ", ".join(df.columns)

            update_cols = ", ".join(
                f"{col} = EXCLUDED.{col}" for col in df.columns if col != conflict_col
            )

            query = text(f"""
                INSERT INTO {table} ({cols})
                SELECT {cols}
                FROM {temp_table}
                ON CONFLICT ({conflict_col})
                DO UPDATE SET {update_cols}
            """)

            conn.execute(query)
            conn.execute(text(f"DROP TABLE IF EXISTS {temp_table}"))

        logger.info(f"[DIMENSION] Loaded {len(df)} rows into {table}")

    def load_fact(self, df: pd.DataFrame, table: str = "fact_sales") -> None:

        if df.empty:
            logger.warning(f"{table} Empty dataframe, skipping load.")
            return

        with self.engine.begin() as conn:
            df.to_sql(table, conn, if_exists="append", index=False)

        logger.info(f"FACT Loaded {len(df)} rows into {table}")

    def truncate_table(self, table: str) -> None:

        with self.engine.begin() as conn:
            conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY"))

        logger.info(f"{table} Truncated before full refresh")

    def refresh_materialized_views(self, views: list[str]) -> None:

        if not views:
            logger.warning("No materialized views provided")
            return

        with self.engine.connect().execution_options(
            isolation_level="AUTOCOMMIT"
        ) as conn:
            for view in views:
                conn.execute(text(f"REFRESH MATERIALIZED VIEW CONCURRENTLY {view}"))

        logger.info(f"Refreshed {len(views)} materialized views")

    def bulk_load(self, operations: list[dict]) -> None:

        for op in operations:
            op_type = op.get("type")

            if op_type == "dim":
                self.load_dimension(
                    df=op["df"], table=op["table"], conflict_col=op["conflict"]
                )

            elif op_type == "fact":
                self.load_fact(df=op["df"], table=op.get("table", "fact_sales"))

            else:
                logger.error(f"Unknown operation type {op_type}")
