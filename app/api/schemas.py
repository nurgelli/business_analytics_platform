from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class APIModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(APIModel):
    message: str


class RevenueKPI(APIModel):
    total_revenue: float
    total_profit: float
    total_orders: int
    unique_customers: int
    profit_margin_pct: float


class GrowthKPI(APIModel):
    year: int
    revenue: float
    prev_revenue: Optional[float] = None
    yoy_growth_pct: Optional[float] = None


class RetentionKPI(APIModel):
    base_customers: int
    retained_customers: int
    retention_rate_pct: float


class MonthlyRevenue(APIModel):
    year: int
    quarter: int
    month: int
    month_name: str
    total_orders: int
    total_quantity: int
    total_revenue: float
    total_profit: float
    average_order_value: float


class DailySales(APIModel):
    full_date: date
    total_orders: int
    total_quantity: int
    total_revenue: float
    total_profit: float


class RevenueByRegion(APIModel):
    region: str
    total_orders: int
    total_customers: int
    total_revenue: float
    total_profit: float
    average_order_value: float


class ProductBase(APIModel):
    product_sk: int
    product_id: str
    product_name: str
    category: str
    sub_category: str


class TopProduct(ProductBase):
    total_orders: int
    total_quantity: int
    total_revenue: float
    total_profit: float
    average_sale: float


class CategorySales(APIModel):
    category: str
    sub_category: str
    total_orders: int
    total_quantity: int
    total_revenue: float
    total_profit: float


class InventorySummary(ProductBase):
    total_units_sold: int
    total_revenue: float
    total_profit: float
    order_count: int


class ProductDetail(ProductBase):
    total_orders: int
    unique_customers: int
    total_quantity_sold: int
    total_revenue: float
    total_profit: float
    average_sale: float
    average_discount: float
    first_sale_date: date
    last_sale_date: date


class CustomerBase(APIModel):
    customer_sk: int
    customer_id: str
    customer_name: str
    segment: str
    region: str


class TopCustomer(CustomerBase):
    total_orders: int
    total_revenue: float
    total_profit: float
    profit_margin_pct: float


class CustomerLifetime(CustomerBase):
    total_orders: int
    total_quantity: int
    lifetime_revenue: float
    lifetime_profit: float
    average_order_value: float
    revenue_per_order: float


class CustomerOrder(APIModel):
    customer_id: str
    customer_name: str
    order_id: str
    order_date: date
    product_name: str
    category: str
    sub_category: str
    quantity: int
    sales_amount: float
    discount: float
    profit: float


class CustomerMonthlyRank(APIModel):
    customer_name: str
    segment: str
    year: int
    month: int
    monthly_revenue: float
    revenue_rank: int
    prev_month_revenue: Optional[float] = None
    month_over_month_change: Optional[float] = None


class CategoryRunningTotal(APIModel):
    full_date: date
    category: str
    daily_revenue: float
    cumulative_revenue: float


class MovingAverage(APIModel):
    full_date: date
    revenue: float
    moving_avg_7d: float


class RevenueRollup(APIModel):
    year: str
    quarter: str
    month: str
    total_revenue: float
    total_profit: float


class CategoryCube(APIModel):
    segment: str
    category: str
    region: str
    orders: int
    revenue: float
    profit: float


class MostProfitableProduct(APIModel):
    product_name: str
    category: str
    sub_category: str
    units_sold: int
    total_revenue: float
    total_profit: float
    profit_margin: float
    profit_rank: int


class MaterializedMonthlyRevenue(APIModel):
    year: int
    quarter: int
    month: int
    month_name: str
    total_orders: int
    total_customers: int
    total_quantity: int
    total_sales: float
    total_profit: float
    avg_order_value: float
    profit_margin_pct: float


class MaterializedCustomerSummary(APIModel):
    customer_sk: int
    customer_name: str
    segment: str
    order_count: int
    lifetime_sales: float
    lifetime_profit: float
    last_purchase_date: date
    first_purchase_date: date
