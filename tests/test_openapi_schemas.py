from app.api.main import app

def test_openapi_contains_response_models():
    schema = app.openapi()
    schemas = schema["components"]["schemas"]

    expected = {
        "RevenueKPI",
        "GrowthKPI",
        "RetentionKPI",
        "MonthlyRevenue",
        "DailySales",
        "RevenueByRegion",
        "TopProduct",
        "CategorySales",
        "InventorySummary",
        "ProductDetail",
        "TopCustomer",
        "CustomerLifetime",
        "CustomerOrder",
        "CustomerMonthlyRank",
        "CategoryRunningTotal",
        "MovingAverage",
        "RevenueRollup",
        "CategoryCube",
        "MostProfitableProduct",
        "MaterializedMonthlyRevenue",
        "MaterializedCustomerSummary",
    }

    assert expected <= set(schemas)


def test_key_routes_declare_200_response_schema():
    schema = app.openapi()

    routes = [
        ("/kpis/revenue", "get"),
        ("/sales/monthly_revenue", "get"),
        ("/products/top_products", "get"),
        ("/customers/", "get"),
        ("/analytics/window/moving_average", "get"),
        ("/analytics/materialized/monthly_revenue", "get"),
    ]

    for path, method in routes:
        response = schema["paths"][path][method]["responses"]["200"]
        assert "schema" in response["content"]["application/json"]
