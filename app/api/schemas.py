from pydantic import BaseModel
from typing import Optional

class RevenueKPI(BaseModel):
    total_revenue: float
    total_profit: float
    total_orders: int
    unique_customers: int
    profit_margin_pct: float

class GrowthKPI(BaseModel):
    year: int
    revenue: float
    prev_revenue: Optional[float]
    yoy_growth_pct: Optional[float]