# app/api/routes/kpis.py
from fastapi import APIRouter, Query
from typing import Optional
from app.kpi.engine import get_revenue_kpis, get_yoy_growth, get_customer_retention

router = APIRouter()

@router.get("/revenue")
def revenue_kpis(year: Optional[int] = Query(None, description="Filter by year")):
    return get_revenue_kpis(year=year)

@router.get("/growth")
def growth_kpis():
    return get_yoy_growth()

@router.get("/retention")
def retention_kpis(
    base_year: int = Query(2021, description="Base year"),
    next_year: int = Query(2022, description="Comparison year")
):
    return get_customer_retention(base_year, next_year)