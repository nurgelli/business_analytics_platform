class TestSystemEndpoints:
    def test_root_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "Business Analytics API" in response.json()["message"]

    def test_health_check_structure(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        body = response.json()
        assert "status" in body
        assert "database" in body
        assert body["status"] in ("healthy", "degraded")


class TestSalesEndpoints:
    def test_monthly_revenue_returns_list(self, client):
        response = client.get("/sales/monthly_revenue")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_daily_sales_returns_list(self, client):
        response = client.get("/sales/daily_sales")
        assert response.status_code == 200

    def test_revenue_by_region_returns_list(self, client):
        response = client.get("/sales/revenue_by_region")
        assert response.status_code == 200


class TestCustomerEndpoints:
    def test_customers_returns_list(self, client):
        response = client.get("/customers/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestAnalyticsEndpoints:
    def test_monthly_rank_returns_list(self, client):
        response = client.get("/analytics/window/monthly_rank")
        assert response.status_code == 200

    def test_monthly_revenue_mv(self, client):
        response = client.get("/analytics/materialized/monthly_revenue")
        assert response.status_code == 200

    def test_customer_summary_mv(self, client):
        response = client.get("/analytics/materialized/customer_summary")
        assert response.status_code == 200


class TestKpiEndpoints:
    def test_revenue_kpis(self, client):
        response = client.get("/kpis/revenue")
        assert response.status_code == 200

    def test_yoy_growth(self, client):
        response = client.get("/kpis/growth")
        assert response.status_code == 200

    def test_customer_retention_valid_params(self, client):
        response = client.get("/kpis/retention?base_year=2022&next_year=2023")
        assert response.status_code == 200
        body = response.json()
        assert "retention_rate_pct" in body

    def test_customer_retention_missing_params(self, client):
        response = client.get("/kpis/retention")
        assert response.status_code == 422  # Unprocessable Entity — parametre eksik
