from functools import lru_cache
from pathlib import Path


class SQLLoader:
    """
    Loads SQL files from db/queries.

    Example
    -------
    SQLLoader.load("sales/monthly_revenue.sql")
    SQLLoader.load("customers/top_customers.sql")
    """

    _BASE_DIR = (
        Path(__file__).resolve().parents[2]
        / "db"
        / "queries"
    )

    @classmethod
    @lru_cache(maxsize=128)
    def load(cls, relative_path: str) -> str:
        """
        Read and cache an SQL file.

        Parameters
        ----------
        relative_path : str
            Relative path under db/queries.

        Returns
        -------
        str
            SQL query text.
        """

        sql_file = cls._BASE_DIR / relative_path

        if not sql_file.exists():
            raise FileNotFoundError(
                f"SQL file not found: {sql_file}"
            )

        return sql_file.read_text(
            encoding="utf-8"
        ).strip()


def load_sql(relative_path: str) -> str:
    """
    Convenience wrapper.

    Example
    -------
    query = load_sql("sales/monthly_revenue.sql")
    """

    return SQLLoader.load(relative_path)