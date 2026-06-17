from fastapi import APIRouter

from app.api.schemas import (
    CategoryCube,
    CategoryRunningTotal,
    CustomerMonthlyRank,
    MaterializedCustomerSummary,
    MaterializedMonthlyRevenue,
    MostProfitableProduct,
    MovingAverage,
    RevenueRollup,
)
from app.db.query_executer import execute_query

router = APIRouter()


@router.get("/window/monthly_rank", response_model=list[CustomerMonthlyRank])
def get_monthly_rank():

    return execute_query("analytics/window/customer_monthly_rank.sql")


@router.get("/window/category_running_total", response_model=list[CategoryRunningTotal])
def get_running_total():

    return execute_query("analytics/window/category_running_total.sql")


@router.get("/window/moving_average", response_model=list[MovingAverage])
def get_moving_average():

    return execute_query("analytics/window/moving_average_7.sql")


@router.get("/rollup_cube/revenue_rollup", response_model=list[RevenueRollup])
def get_revenue_rollup():

    return execute_query("analytics/rollup_cube/revenue_rollup.sql")


@router.get("/rollup_cube/category_cube", response_model=list[CategoryCube])
def get_category_cube():

    return execute_query("analytics/rollup_cube/category_cube.sql")


@router.get(
    "/rollup_cube/most_benefit_products", response_model=list[MostProfitableProduct]
)
def get_benefit_products():

    return execute_query("analytics/rollup_cube/most_benefit_products.sql")


@router.get(
    "/materialized/monthly_revenue", response_model=list[MaterializedMonthlyRevenue]
)
def monthly_revenue_mv():

    return execute_query("analytics/materialized/monthly_revenue.sql")


@router.get(
    "/materialized/customer_summary", response_model=list[MaterializedCustomerSummary]
)
def customer_summary_mv():

    return execute_query("analytics/materialized/customer_summary.sql")
