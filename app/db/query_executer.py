from app.db.sql_loader import load_sql
from app.core.database import engine



def execute_query(sql_path: str, params: dict | None = None):

    query = load_sql(sql_path)

    with engine.begin() as conn:

        result = conn.execute(text(query), params or {},)

        return [dict(row._mapping)for row in result]



def fetch_all(sql_path: str, params: dict | None = None,) -> list[dict]:

    query = load_sql(sql_path)

    with engine.begin() as conn:

        rows = conn.execute(

            text(query),

            params or {},

        ).mappings().all()

    return [
        dict(row)
        for row in rows
    ]


def fetch_one(sql_path: str, params: dict | None = None,) -> dict | None:

    query = load_sql(sql_path)

    with engine.begin() as conn:

        row = conn.execute(

            text(query),

            params or {},

        ).mappings().first()

    return (
        dict(row)
        if row
        else None
    )