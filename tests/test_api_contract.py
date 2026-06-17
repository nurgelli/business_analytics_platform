from typing import Any

import pytest


def assert_fields(row: dict[str, Any], fields: set[str]) -> None:
    assert fields <= set(row), f"Missing fields: {fields - set(row)}"


def first_row(client, path: str) -> dict[str, Any]:
    response = client.get(path)
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload, f"{path} returned no rows"
    return payload[0]


@pytest.mark.parametrize(
    ("path", "fields"),
    [
        (
            "/sales/monthly_revenue",
            {
                "year",
                "quarter",
                "month",
                "month_name",
                "total_orders",
                "total_quantity",
                "total_revenue",
                "total_profit",
                "average_order_value",
            },
        ),
        (
            "/sales/daily_sales",
            {
                "full_date",
                "total_orders",
                "total_quantity",
                "total_revenue",
                "total_profit",
            },
        ),
        (
            "/sales/revenue_by_region",
            {
                "region",
                "total_orders",
                "total_customers",
                "total_revenue",
                "total_profit",
                "average_order_value",
            },
        ),
        (
            "/products/top_products",
            {
                "product_sk",
                "product_id",
                "product_name",
                "category",
                "sub_category",
                "total_orders",
                "total_quantity",
                "total_revenue",
                "total_profit",
                "average_sale",
            },
        ),
        (
            "/products/category_sales",
            {
                "category",
                "sub_category",
                "total_orders",
                "total_quantity",
                "total_revenue",
                "total_profit",
            },
        ),
        (
            "/products/inventory",
            {
                "product_sk",
                "product_id",
                "product_name",
                "category",
                "sub_category",
                "total_units_sold",
                "total_revenue",
                "total_profit",
                "order_count",
            },
        ),
        (
            "/customers/",
            {
                "customer_sk",
                "customer_id",
                "customer_name",
                "segment",
                "region",
                "total_orders",
                "total_revenue",
                "total_profit",
                "profit_margin_pct",
            },
        ),
        (
            "/customers/lifetime",
            {
                "customer_sk",
                "customer_id",
                "customer_name",
                "segment",
                "region",
                "total_orders",
                "total_quantity",
                "lifetime_revenue",
                "lifetime_profit",
                "average_order_value",
                "revenue_per_order",
            },
        ),
        (
            "/analytics/window/monthly_rank",
            {
                "customer_name",
                "segment",
                "year",
                "month",
                "monthly_revenue",
                "revenue_rank",
                "prev_month_revenue",
                "month_over_month_change",
            },
        ),
        (
            "/analytics/window/category_running_total",
            {"full_date", "category", "daily_revenue", "cumulative_revenue"},
        ),
        (
            "/analytics/window/moving_average",
            {"full_date", "revenue", "moving_avg_7d"},
        ),
        (
            "/analytics/rollup_cube/revenue_rollup",
            {"year", "quarter", "month", "total_revenue", "total_profit"},
        ),
        (
            "/analytics/rollup_cube/category_cube",
            {"segment", "category", "region", "orders", "revenue", "profit"},
        ),
        (
            "/analytics/rollup_cube/most_benefit_products",
            {
                "product_name",
                "category",
                "sub_category",
                "units_sold",
                "total_revenue",
                "total_profit",
                "profit_margin",
                "profit_rank",
            },
        ),
        (
            "/analytics/materialized/monthly_revenue",
            {
                "year",
                "quarter",
                "month",
                "month_name",
                "total_orders",
                "total_customers",
                "total_quantity",
                "total_sales",
                "total_profit",
                "avg_order_value",
                "profit_margin_pct",
            },
        ),
        (
            "/analytics/materialized/customer_summary",
            {
                "customer_sk",
                "customer_name",
                "segment",
                "order_count",
                "lifetime_sales",
                "lifetime_profit",
                "last_purchase_date",
                "first_purchase_date",
            },
        ),
    ],
)
def test_list_endpoint_contracts(client, path, fields):
    assert_fields(first_row(client, path), fields)


def test_revenue_kpi_contract(client):
    response = client.get("/kpis/revenue")
    assert response.status_code == 200
    body = response.json()

    assert_fields(
        body,
        {
            "total_revenue",
            "total_profit",
            "total_orders",
            "unique_customers",
            "profit_margin_pct",
        },
    )
    assert body["total_revenue"] > 0
    assert body["total_orders"] > 0


def test_revenue_kpi_year_filter_changes_scope(client):
    all_years = client.get("/kpis/revenue").json()
    year_2016 = client.get("/kpis/revenue", params={"year": 2016}).json()

    assert year_2016["total_revenue"] > 0
    assert year_2016["total_revenue"] < all_years["total_revenue"]


def test_growth_contract_and_ordering(client):
    response = client.get("/kpis/growth")
    assert response.status_code == 200
    rows = response.json()

    assert rows
    assert [row["year"] for row in rows] == sorted(row["year"] for row in rows)
    assert rows[0]["prev_revenue"] is None


def test_retention_contract(client):
    response = client.get(
        "/kpis/retention", params={"base_year": 2016, "next_year": 2017}
    )
    assert response.status_code == 200
    body = response.json()

    assert_fields(body, {"base_customers", "retained_customers", "retention_rate_pct"})
    assert 0 <= body["retention_rate_pct"] <= 100


def test_product_detail_and_not_found(client):
    product = first_row(client, "/products/top_products")

    detail_response = client.get(f"/products/{product['product_id']}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["product_id"] == product["product_id"]
    assert_fields(detail, {"first_sale_date", "last_sale_date", "average_discount"})

    missing_response = client.get("/products/DOES-NOT-EXIST")
    assert missing_response.status_code == 404


def test_customer_orders_contract(client):
    customer = first_row(client, "/customers/")

    response = client.get(f"/customers/{customer['customer_id']}/orders")
    assert response.status_code == 200
    rows = response.json()
    assert rows
    assert_fields(
        rows[0],
        {
            "customer_id",
            "customer_name",
            "order_id",
            "order_date",
            "product_name",
            "category",
            "sub_category",
            "quantity",
            "sales_amount",
            "discount",
            "profit",
        },
    )
