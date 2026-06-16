from fastapi import APIRouter, HTTPException
from app.db.query_executer import execute_query, fetch_one
from app.api.schemas import CategorySales, InventorySummary, ProductDetail, TopProduct

router = APIRouter()

@router.get("/top_products", response_model=list[TopProduct])
def get_top_products():

    return execute_query("products/top_products.sql")


@router.get("/category_sales", response_model=list[CategorySales])
def get_category_sales():

    return execute_query("products/category_sales.sql")


@router.get("/inventory", response_model=list[InventorySummary])
def get_inventory():
    return execute_query("products/inventory_summary.sql")


@router.get("/{product_id}", response_model=ProductDetail)
def get_product_details(product_id: str):

    row = fetch_one("products/product_details.sql", {"product_id": product_id})

    if row is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return row



