import os

# Set DATABASE_URL before any app imports so database.py doesn't raise
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_TEST_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    """Create tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_transaction():
    """Valid transaction payload for reuse across tests."""
    return {
        "description": "Test Salary",
        "amount": 50000,
        "type": "income",
        "category": "salary",
        "date": "2026-03-01",
    }


@pytest.fixture
def sample_expense():
    """Valid expense payload for reuse across tests."""
    return {
        "description": "Groceries",
        "amount": 2500,
        "type": "expense",
        "category": "food",
        "date": "2026-03-02",
    }
