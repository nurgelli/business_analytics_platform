from functools import lru_cache
from pathlib import Path


class SQLLoader:
    _BASE_DIR = (Path(__file__).resolve().parents[2]/ "db"/ "queries")

    @classmethod
    @lru_cache(maxsize=128)
    def load(cls, relative_path: str) -> str:
        sql_file = cls._BASE_DIR / relative_path
        if not sql_file.exists():
            raise FileNotFoundError(f"SQL file not found: {sql_file}")
        return sql_file.read_text(encoding="utf-8").strip()

def load_sql(relative_path: str) -> str:
    
    return SQLLoader.load(relative_path)