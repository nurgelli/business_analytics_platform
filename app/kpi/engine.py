# app/kpi/engine.py
from sqlalchemy import text
from app.core.logger import get_logger
from app.db.sql_loader import load_sql
from app.db.query_executer import fetch_all, fetch_one

logger = get_logger(__name__)

def get_revenue_kpis(year: int | None = None) -> dict:

    row = fetch_one("analytics/kpi/revenue_kpis.sql", {"year": year})

    return {
        "total_revenue":round(float(row["total_revenue"] or 0), 2),
        "total_profit": round(float(row["total_profit"] or 0), 2),
        "total_orders": int(row["total_orders"] or 0),
        "unique_customers": int(row["unique_customers"] or 0),
        "profit_margin_pct": float(row["profit_margin_pct"] or 0),

    }


def get_yoy_growth() -> list:

    row = fetch_all("analytics/kpi/yoy_growth.sql")

    return [{"year":row["year"],
            "revenue": round(float(row["revenue"] or 0),2,),
            "prev_revenue":(round(float(row["prev_revenue"]),2,)if row["prev_revenue"] is not None else None),
            "yoy_growth_pct":(float(row["yoy_growth_pct"]) if row["yoy_growth_pct"] is not None else None),} for row in rows]

    
   
def get_customer_retention(base_year: int, next_year: int) -> dict:

    row = fetch_all("analytics/kpi/yoy_growth.sql")

    return [{"year":row["year"],
            "revenue": round(float(row["revenue"] or 0), 2,),
            "prev_revenue":(round(float(row["prev_revenue"]),2,) if row["prev_revenue"] is not None else None),
            "yoy_growth_pct":(float(row["yoy_growth_pct"]) if row["yoy_growth_pct"] is not None else None ),} for row in rows]
  