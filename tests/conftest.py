import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# add parent directory to sys.path to allow imports
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.infrastructure.database import Base, get_db
from src.main import app

# creating a separate database for tests
db_folder = "./tests/database"
os.makedirs(db_folder, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_folder}/users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Pytest fixtures for session and client
@pytest.fixture(scope="function")
def db_session():
    """
    Create and return new sqlalchemy session for a tests. 
    """
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    """
    The tests use the client to send API requests without affecting the real database.
    """
    # Override get_db для FastAPI
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)