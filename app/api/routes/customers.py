from fastapi import APIRouter

from app.api.schemas import CustomerLifetime, CustomerOrder, TopCustomer
from app.db.query_executer import execute_query

router = APIRouter()


@router.get("/", response_model=list[TopCustomer])
def get_customers():

    return execute_query("customers/top_customers.sql")


@router.get("/top_customer", response_model=list[TopCustomer])
def get_top_customers():

    return execute_query("customers/top_customers.sql")


@router.get("/lifetime", response_model=list[CustomerLifetime])
def get_customer_lifetime_val():

    return execute_query("customers/customer_lifetime.sql")


@router.get("/{customer_id}/orders", response_model=list[CustomerOrder])
def get_customer_orders(
    customer_id: str,
):

    return execute_query("customers/customer_orders.sql", {"customer_id": customer_id})
