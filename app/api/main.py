# app/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import kpis, sales, customers, products, analytics
from app.core.database import test_connection
from app.core.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Business Analytics API",
    description="Sales Data Warehouse KPI and Analytics API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(kpis.router,      prefix="/kpis",      tags=["KPIs"])
app.include_router(sales.router,     prefix="/sales",     tags=["Sales"])
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(products.router, prefix="/products", tags=["Products"])

@app.get("/health", tags=["System"])
def health_check():
    db_ok = test_connection()
    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "connected" if db_ok else "disconnected"
    }

@app.get("/", tags=["System"])
def root():
    return {"message": "Business Analytics API", "docs": "/docs"}