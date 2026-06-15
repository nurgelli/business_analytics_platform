from fastapi import APIRouter
from app.db.query_executer import execute_query


router = APIRouter()

@router.get("/monthly_revenue")
def get_monthly_revenue():

    return execute_query("sales/monthly_revenue.sql")
  

@router.get("/daily_sales")
def get_daily_sales():

    return execute_query("sales/daily_sales.sql")
  

@router.get("/revenue_by_region")
def get_revenue_by_region():

    return execute_query("sales/revenue_by_region.sql")
