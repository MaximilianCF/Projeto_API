import pytest
from app.core.database import create_db_and_tables

@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    create_db_and_tables()
