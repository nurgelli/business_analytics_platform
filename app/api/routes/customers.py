from fastapi import APIRouter
from sqlalchemy import text
from app.db.query_executer import execute_query



router = APIRouter()

@router.get("/top_customer")
def get_top_customers():

    return execute_query("customers/top_customers.sql")
    

@router.get("/lifetime")
def get_customer_lifetime_val():

    return execute_query("customers/customer_lifetime.sql")


@router.get("/{customer_id}/orders")
def get_customer_orders(customer_id: str,):

    return execute_query("customers/customer_orders.sql", customer_id=customer_id)
