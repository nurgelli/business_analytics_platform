from fastapi import APIRouter
from app.db.query_executer import execute_query, fetch_one

router = APIRouter()

@router.get("/top_products")
def get_top_products():

    return execute_query("products/top_products.sql")


@router.get("/category_sales")
def get_category_sales():

    return execute_query("products/category_sales.sql")


@router.get("/inventory")
def get_inventory():
    return execute_query("products/inventory_summary.sql")


@router.get('/{product_id}')
def get_product_details(product_id: str):

    row = fetch_one("products/product_details.sql", {"product_id": product_id})

    if row is None:
        return {"message": "Product not found"}

    return row



