import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = os.getenv("API_PORT", "8000")
API_BASE = f"http://{API_HOST}:{API_PORT}"

ENDPOINTS = {
    "Revenue KPI": "/kpis/revenue",
    "YoY Growth": "/kpis/growth",
    "Retention": "/kpis/retention",
    "Monthly Revenue": "/sales/monthly_revenue",
    "Daily Sales": "/sales/daily_sales",
    "Revenue by Region": "/sales/revenue_by_region",
    "Top Products": "/products/top_products",
    "Category Revenue": "/products/category_sales",
    "Inventory Summary": "/products/inventory",
    "Top Customers": "/customers/",
    "Customer Lifetime": "/customers/lifetime",
    "Monthly Rank": "/analytics/window/monthly_rank",
    "Category Running Total": "/analytics/window/category_running_total",
    "Moving Average": "/analytics/window/moving_average",
    "Revenue Rollup": "/analytics/rollup_cube/revenue_rollup",
    "Category Cube": "/analytics/rollup_cube/category_cube",
    "Most Profitable Products": "/analytics/rollup_cube/most_benefit_products",
    "MV Monthly Revenue": "/analytics/materialized/monthly_revenue",
    "MV Customer Summary": "/analytics/materialized/customer_summary",
}


st.set_page_config(
    page_title="Business Analytic Visualization",
    page_icon="BA",
    layout="wide",
)


@st.cache_data(ttl=60)
def api_get(path: str, params: dict | None = None):
    response = requests.get(f"{API_BASE}{path}", params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def as_df(payload) -> pd.DataFrame:
    if payload is None:
        return pd.DataFrame()
    if isinstance(payload, dict):
        return pd.DataFrame([payload])
    return pd.DataFrame(payload)


def load_df(name: str, params: dict | None = None) -> pd.DataFrame:
    try:
        return as_df(api_get(ENDPOINTS[name], params=params))
    except Exception as exc:
        st.warning(f"{name} could not be loaded: {exc}")
        return pd.DataFrame()


def metric_value(value, prefix: str = "", suffix: str = "", decimals: int = 0) -> str:
    if value is None or pd.isna(value):
        value = 0
    return f"{prefix}{float(value):,.{decimals}f}{suffix}"


def coerce_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ("full_date", "first_purchase_date", "last_purchase_date"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def available_years(*frames: pd.DataFrame) -> list[int]:
    years: set[int] = set()
    for df in frames:
        if "year" in df.columns:
            years.update(
                pd.to_numeric(df["year"], errors="coerce").dropna().astype(int).tolist()
            )
        if "full_date" in df.columns:
            years.update(
                pd.to_datetime(df["full_date"], errors="coerce")
                .dropna()
                .dt.year.astype(int)
                .tolist()
            )
    return sorted(years)


def unique_values(frames: list[pd.DataFrame], column: str) -> list[str]:
    values: set[str] = set()
    for df in frames:
        if column in df.columns:
            values.update(df[column].dropna().astype(str).tolist())
    return sorted(values)


def apply_filters(
    df: pd.DataFrame, year: int | None, region: str, segment: str, category: str
) -> pd.DataFrame:
    if df.empty:
        return df

    filtered = coerce_dates(df)

    if year is not None:
        if "year" in filtered.columns:
            filtered = filtered[
                pd.to_numeric(filtered["year"], errors="coerce") == year
            ]
        elif "full_date" in filtered.columns:
            filtered = filtered[filtered["full_date"].dt.year == year]

    if region != "All" and "region" in filtered.columns:
        filtered = filtered[filtered["region"].astype(str) == region]
    if segment != "All" and "segment" in filtered.columns:
        filtered = filtered[filtered["segment"].astype(str) == segment]
    if category != "All" and "category" in filtered.columns:
        filtered = filtered[filtered["category"].astype(str) == category]

    return filtered


def top_records(df: pd.DataFrame, metric: str, limit: int) -> pd.DataFrame:
    if df.empty or metric not in df.columns:
        return df.head(limit)
    return df.sort_values(metric, ascending=False).head(limit)


st.title("Business Analytic Visualization")
st.caption(f"API: {API_BASE}, Last updated: {datetime.now():%Y-%m-%d %H:%M}")

monthly_df = load_df("Monthly Revenue")
daily_df = load_df("Daily Sales")
region_df = load_df("Revenue by Region")
products_df = load_df("Top Products")
category_df = load_df("Category Revenue")
inventory_df = load_df("Inventory Summary")
customers_df = load_df("Top Customers")
customer_lifetime_df = load_df("Customer Lifetime")
growth_df = load_df("YoY Growth")
moving_avg_df = load_df("Moving Average")
monthly_rank_df = load_df("Monthly Rank")
running_total_df = load_df("Category Running Total")
rollup_df = load_df("Revenue Rollup")
cube_df = load_df("Category Cube")
profitable_products_df = load_df("Most Profitable Products")
mv_monthly_df = load_df("MV Monthly Revenue")
mv_customer_df = load_df("MV Customer Summary")

all_frames = [
    monthly_df,
    daily_df,
    region_df,
    products_df,
    category_df,
    inventory_df,
    customers_df,
    customer_lifetime_df,
    growth_df,
    moving_avg_df,
    monthly_rank_df,
    running_total_df,
    rollup_df,
    cube_df,
    profitable_products_df,
    mv_monthly_df,
    mv_customer_df,
]

with st.sidebar:
    st.header("Filters")
    years = available_years(*all_frames)
    selected_year_label = st.selectbox("Year", ["All"] + years, index=0)
    selected_year = None if selected_year_label == "All" else int(selected_year_label)

    selected_region = st.selectbox(
        "Region", ["All"] + unique_values(all_frames, "region")
    )
    selected_segment = st.selectbox(
        "Segment", ["All"] + unique_values(all_frames, "segment")
    )
    selected_category = st.selectbox(
        "Category", ["All"] + unique_values(all_frames, "category")
    )
    top_n = st.slider("Top N", min_value=5, max_value=25, value=10, step=5)

    st.divider()
    st.header("Retention")
    retention_years = years or [2021, 2022, 2023]
    base_year = st.selectbox(
        "Base Year", retention_years, index=max(0, len(retention_years) - 2)
    )
    next_year = st.selectbox(
        "Comparison Year", retention_years, index=max(0, len(retention_years) - 1)
    )

filtered_monthly = apply_filters(
    monthly_df, selected_year, selected_region, selected_segment, selected_category
)
filtered_daily = apply_filters(
    daily_df, selected_year, selected_region, selected_segment, selected_category
)
filtered_region = apply_filters(
    region_df, selected_year, selected_region, selected_segment, selected_category
)
filtered_products = apply_filters(
    products_df, selected_year, selected_region, selected_segment, selected_category
)
filtered_category = apply_filters(
    category_df, selected_year, selected_region, selected_segment, selected_category
)
filtered_inventory = apply_filters(
    inventory_df, selected_year, selected_region, selected_segment, selected_category
)
filtered_customers = apply_filters(
    customers_df, selected_year, selected_region, selected_segment, selected_category
)
filtered_lifetime = apply_filters(
    customer_lifetime_df,
    selected_year,
    selected_region,
    selected_segment,
    selected_category,
)
filtered_growth = apply_filters(
    growth_df, selected_year, selected_region, selected_segment, selected_category
)
filtered_moving_avg = apply_filters(
    moving_avg_df, selected_year, selected_region, selected_segment, selected_category
)
filtered_rank = apply_filters(
    monthly_rank_df, selected_year, selected_region, selected_segment, selected_category
)
filtered_running_total = apply_filters(
    running_total_df,
    selected_year,
    selected_region,
    selected_segment,
    selected_category,
)
filtered_rollup = apply_filters(
    rollup_df, selected_year, selected_region, selected_segment, selected_category
)
filtered_cube = apply_filters(
    cube_df, selected_year, selected_region, selected_segment, selected_category
)
filtered_profitable = apply_filters(
    profitable_products_df,
    selected_year,
    selected_region,
    selected_segment,
    selected_category,
)
filtered_mv_monthly = apply_filters(
    mv_monthly_df, selected_year, selected_region, selected_segment, selected_category
)
filtered_mv_customer = apply_filters(
    mv_customer_df, selected_year, selected_region, selected_segment, selected_category
)

try:
    kpi_params = {"year": selected_year} if selected_year is not None else None
    kpi = api_get(ENDPOINTS["Revenue KPI"], params=kpi_params)
except Exception:
    kpi = {}

try:
    retention = api_get(
        ENDPOINTS["Retention"],
        params={"base_year": base_year, "next_year": next_year},
    )
except Exception:
    retention = {}

overview_tab, sales_tab, product_tab, customer_tab, advanced_tab, data_tab = st.tabs(
    [
        "Overview",
        "Sales",
        "Products",
        "Customers",
        "Advanced Analytics",
        "Data Explorer",
    ]
)

with overview_tab:
    st.subheader("Revenue KPI")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Revenue", metric_value(kpi.get("total_revenue"), "$"))
    c2.metric("Profit", metric_value(kpi.get("total_profit"), "$"))
    c3.metric(
        "Profit Margin",
        metric_value(kpi.get("profit_margin_pct"), suffix="%", decimals=2),
    )
    c4.metric("Orders", metric_value(kpi.get("total_orders")))
    c5.metric("Customers", metric_value(kpi.get("unique_customers")))

    st.subheader("Customer KPI")
    active_customers = (
        filtered_lifetime["customer_id"].nunique()
        if "customer_id" in filtered_lifetime
        else 0
    )
    avg_lifetime = (
        filtered_lifetime["lifetime_revenue"].mean()
        if "lifetime_revenue" in filtered_lifetime
        else 0
    )
    avg_order_value = (
        filtered_lifetime["average_order_value"].mean()
        if "average_order_value" in filtered_lifetime
        else 0
    )
    retained = retention.get("retained_customers", 0)
    customer_cols = st.columns(4)
    customer_cols[0].metric("Active Customers", metric_value(active_customers))
    customer_cols[1].metric("Avg Lifetime Revenue", metric_value(avg_lifetime, "$"))
    customer_cols[2].metric("Avg Order Value", metric_value(avg_order_value, "$"))
    customer_cols[3].metric("Retained Customers", metric_value(retained))

    left, right = st.columns(2)
    with left:
        if not filtered_growth.empty:
            fig = go.Figure()
            fig.add_bar(
                x=filtered_growth["year"], y=filtered_growth["revenue"], name="Revenue"
            )
            fig.add_scatter(
                x=filtered_growth["year"],
                y=filtered_growth["yoy_growth_pct"],
                name="YoY Growth %",
                yaxis="y2",
                mode="lines+markers",
            )
            fig.update_layout(
                yaxis={"title": "Revenue"},
                yaxis2={"title": "Growth %", "overlaying": "y", "side": "right"},
                legend={"orientation": "h"},
                margin={"l": 10, "r": 10, "t": 30, "b": 10},
            )
            st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=float(retention.get("retention_rate_pct", 0) or 0),
                title={"text": "Retention Rate"},
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#2f6fed"}},
            )
        )
        fig.update_layout(margin={"l": 20, "r": 20, "t": 30, "b": 10})
        st.plotly_chart(fig, use_container_width=True)

with sales_tab:
    st.subheader("Revenue, Profit and Margin")
    if not filtered_monthly.empty:
        monthly_view = filtered_monthly.copy()
        monthly_view["period"] = (
            monthly_view["year"].astype(str)
            + "-"
            + monthly_view["month"].astype(str).str.zfill(2)
        )
        monthly_view["profit_margin_pct"] = (
            monthly_view["total_profit"]
            / monthly_view["total_revenue"].replace(0, pd.NA)
            * 100
        )
        fig = px.line(
            monthly_view,
            x="period",
            y=["total_revenue", "total_profit"],
            markers=True,
        )
        st.plotly_chart(fig, use_container_width=True)

        margin_fig = px.bar(monthly_view, x="period", y="profit_margin_pct")
        st.plotly_chart(margin_fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        if not filtered_region.empty:
            fig = px.bar(filtered_region, x="region", y="total_revenue", color="region")
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        if not filtered_daily.empty:
            fig = px.area(
                coerce_dates(filtered_daily), x="full_date", y="total_revenue"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.dataframe(filtered_monthly, use_container_width=True, hide_index=True)

with product_tab:
    st.subheader("Top Products")
    top_products = top_records(filtered_products, "total_revenue", top_n)
    if not top_products.empty:
        fig = px.bar(
            top_products.sort_values("total_revenue"),
            x="total_revenue",
            y="product_name",
            color="category",
            orientation="h",
        )
        st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top_products, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Category Revenue")
        if not filtered_category.empty:
            fig = px.treemap(
                filtered_category,
                path=["category", "sub_category"],
                values="total_revenue",
                color="total_profit",
            )
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Most Profitable Products")
        profitable = top_records(filtered_profitable, "total_profit", top_n)
        if not profitable.empty:
            fig = px.bar(
                profitable.sort_values("total_profit"),
                x="total_profit",
                y="product_name",
                color="profit_margin",
                orientation="h",
            )
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Inventory Summary")
    st.dataframe(
        top_records(filtered_inventory, "total_units_sold", top_n),
        use_container_width=True,
        hide_index=True,
    )

with customer_tab:
    st.subheader("Top Customers")
    top_customers = top_records(filtered_customers, "total_revenue", top_n)
    if not top_customers.empty:
        fig = px.bar(
            top_customers.sort_values("total_revenue"),
            x="total_revenue",
            y="customer_name",
            color="segment",
            orientation="h",
        )
        st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top_customers, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Customer Lifetime")
        st.dataframe(
            top_records(filtered_lifetime, "lifetime_revenue", top_n),
            use_container_width=True,
            hide_index=True,
        )
    with c2:
        st.subheader("Customer Summary MV")
        st.dataframe(
            top_records(filtered_mv_customer, "lifetime_sales", top_n),
            use_container_width=True,
            hide_index=True,
        )

with advanced_tab:
    st.subheader("Moving Average")
    if not filtered_moving_avg.empty:
        moving_view = coerce_dates(filtered_moving_avg)
        fig = go.Figure()
        fig.add_scatter(
            x=moving_view["full_date"],
            y=moving_view["revenue"],
            name="Revenue",
            mode="lines",
        )
        fig.add_scatter(
            x=moving_view["full_date"],
            y=moving_view["moving_avg_7d"],
            name="7D Moving Avg",
            mode="lines",
        )
        st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Category Running Total")
        if not filtered_running_total.empty:
            running_view = coerce_dates(filtered_running_total)
            fig = px.line(
                running_view, x="full_date", y="cumulative_revenue", color="category"
            )
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Monthly Customer Rank")
        rank_view = top_records(filtered_rank, "monthly_revenue", top_n)
        st.dataframe(rank_view, use_container_width=True, hide_index=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Revenue Rollup")
        st.dataframe(filtered_rollup, use_container_width=True, hide_index=True)
    with c4:
        st.subheader("Category Cube")
        st.dataframe(
            top_records(filtered_cube, "revenue", top_n),
            use_container_width=True,
            hide_index=True,
        )

with data_tab:
    st.subheader("All Routed Analyses")
    datasets = {
        "Revenue KPI": as_df(kpi),
        "YoY Growth": filtered_growth,
        "Retention": as_df(retention),
        "Monthly Revenue": filtered_monthly,
        "Daily Sales": filtered_daily,
        "Revenue by Region": filtered_region,
        "Top Products": filtered_products,
        "Category Revenue": filtered_category,
        "Inventory Summary": filtered_inventory,
        "Top Customers": filtered_customers,
        "Customer Lifetime": filtered_lifetime,
        "Monthly Rank": filtered_rank,
        "Category Running Total": filtered_running_total,
        "Moving Average": filtered_moving_avg,
        "Revenue Rollup": filtered_rollup,
        "Category Cube": filtered_cube,
        "Most Profitable Products": filtered_profitable,
        "MV Monthly Revenue": filtered_mv_monthly,
        "MV Customer Summary": filtered_mv_customer,
    }
    selected_dataset = st.selectbox("Dataset", list(datasets))
    st.dataframe(datasets[selected_dataset], use_container_width=True, hide_index=True)
