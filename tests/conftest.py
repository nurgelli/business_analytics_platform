import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.api.main import app
from app.core.config import settings
from app.etl.run_pipeline import run as run_etl_pipeline


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def ensure_warehouse_data(test_engine):
    with test_engine.connect() as conn:
        fact_count = conn.execute(text("SELECT COUNT(*) FROM fact_sales")).scalar()

    if fact_count == 0:
        run_etl_pipeline()


@pytest.fixture(scope="function")
def db_session(test_engine):
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
