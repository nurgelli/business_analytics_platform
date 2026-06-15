from fastapi import APIRouter
from sqlalchemy import text
from app.db.query_executer import execute_query


router = APIRouter()

@router.get("/window/monthly_rank")
def get_monthly_rank():

    return execute_query("analytics/window/customer_monthly_rank.sql")

@router.get("/window/category_running_total")
def get_monthly_rank():

    return execute_query("analytics/window/category_running_total.sql")

@router.get("/window/moving_average")
def get_monthly_rank():

    return execute_query("analytics/window/moving_average_7.sql")

@router.get("/rollup_cube/revenue_rollup")
def get_monthly_rank():

    return execute_query("analytics/rollup_cube/revenue_rollup.sql")

@router.get("/rollup_cube/category_cube")
def get_monthly_rank():

    return execute_query("analytics/rollup_cube/category_cube.sql")

@router.get("/rollup_cube/most_benefit_products")
def get_monthly_rank():

    return execute_query("analytics/rollup_cube/most_benefit_products.sql")


@router.get("/materialized/monthly-revenue")
def monthly_revenue_mv():

    return execute_query(
        "analytics/materialized/monthly_revenue.sql"
    )

@router.get("/materialized/customer-summary")
def monthly_revenue_mv():

    return execute_query(
        "analytics/materialized/customer_summary.sql"
    )