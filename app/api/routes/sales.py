from fastapi import APIRouter
from app.db.query_executer import execute_query
from app.api.schemas import DailySales, MonthlyRevenue, RevenueByRegion


router = APIRouter()

@router.get("/monthly_revenue", response_model=list[MonthlyRevenue])
def get_monthly_revenue():

    return execute_query("sales/monthly_revenue.sql")
  

@router.get("/daily_sales", response_model=list[DailySales])
def get_daily_sales():

    return execute_query("sales/daily_sales.sql")
  

@router.get("/revenue_by_region", response_model=list[RevenueByRegion])
def get_revenue_by_region():

    return execute_query("sales/revenue_by_region.sql")
