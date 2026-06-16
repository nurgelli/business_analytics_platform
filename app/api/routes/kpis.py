# app/api/routes/kpis.py
from fastapi import APIRouter, Query
from typing import Optional
from app.kpi.engine import get_revenue_kpis, get_yoy_growth, get_customer_retention
from app.api.schemas import GrowthKPI, RetentionKPI, RevenueKPI

router = APIRouter()

@router.get("/revenue", response_model=RevenueKPI)
def revenue_kpis(year: Optional[int] = Query(None, description="Filter by year")):
    return get_revenue_kpis(year=year)

@router.get("/growth", response_model=list[GrowthKPI])
def growth_kpis():
    return get_yoy_growth()

@router.get("/retention", response_model=RetentionKPI)
def retention_kpis(
    base_year: int = Query(..., description="Base year"),
    next_year: int = Query(..., description="Comparison year")
):
    return get_customer_retention(base_year, next_year)
