# dashboard/app.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

API_BASE = "http://fastapi:8000"  # Docker içi; local için: http://localhost:8000

st.set_page_config(
    page_title="Business Analytics Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Analytics Platform")
st.caption(f"Data Warehouse | Star Schema | Advanced SQL | Last updated: {datetime.now():%Y-%m-%d %H:%M}")

# --- KPI CARDS ---
st.header("Key Performance Indicators")

try:
    kpi = requests.get(f"{API_BASE}/kpis/revenue").json()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Revenue",    f"${kpi['total_revenue']:,.0f}")
    col2.metric("Total Profit",     f"${kpi['total_profit']:,.0f}")
    col3.metric("Profit Margin",    f"{kpi['profit_margin_pct']}%")
    col4.metric("Total Orders",     f"{kpi['total_orders']:,}")
    col5.metric("Unique Customers", f"{kpi['unique_customers']:,}")

except Exception as e:
    st.error(f"API connection error: {e}")

# --- GROWTH CHART ---
st.header("Year-over-Year Revenue Growth")

try:
    growth = requests.get(f"{API_BASE}/kpis/growth").json()
    df_growth = pd.DataFrame(growth)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_growth["year"], y=df_growth["revenue"],
                         name="Revenue", marker_color="#1f77b4"))
    fig.add_trace(go.Scatter(x=df_growth["year"], y=df_growth["yoy_growth_pct"],
                              name="YoY Growth %", yaxis="y2",
                              line=dict(color="#ff7f0e", width=3)))

    fig.update_layout(
        yaxis=dict(title="Revenue ($)"),
        yaxis2=dict(title="Growth %", overlaying="y", side="right"),
        legend=dict(orientation="h")
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Growth data error: {e}")

# --- RETENTION ---
st.header("Customer Retention Analysis")

col1, col2 = st.columns(2)
base_year = col1.selectbox("Base Year", [2020, 2021, 2022], index=1)
next_year = col2.selectbox("Comparison Year", [2021, 2022, 2023], index=1)

try:
    ret = requests.get(
        f"{API_BASE}/kpis/retention",
        params={"base_year": base_year, "next_year": next_year}
    ).json()

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=ret["retention_rate_pct"],
        title={"text": "Retention Rate (%)"},
        gauge={"axis": {"range": [0, 100]},
               "bar": {"color": "#2ecc71"},
               "steps": [
                   {"range": [0, 40], "color": "#e74c3c"},
                   {"range": [40, 70], "color": "#f39c12"},
                   {"range": [70, 100], "color": "#27ae60"}
               ]}
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

except Exception as e:
    st.error(f"Retention data error: {e}")