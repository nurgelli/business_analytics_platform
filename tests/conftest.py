import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.api.main import app
from app.core.config import settings
from app.core.database import get_db

# ── Test DB oturumu (fixture) ──────────────────────────────────────────────
@pytest.fixture(scope="session")
def test_engine():
    """CI'da POSTGRES_PORT=5432, localda .env'deki 5432 kullanılır."""
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(test_engine):
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

# ── FastAPI test client ────────────────────────────────────────────────────
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c