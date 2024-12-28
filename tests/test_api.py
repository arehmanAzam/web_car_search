# tests/test_api.py
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.models.models import Base
from config.database import get_db
import pytest

# Test database setup
SQLALCHEMY_DATABASE_URL = "postgresql://abdul:Rehman123@localhost:5432/car_search"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_car(test_db):
    car_data = {
        "length": 4.5,
        "weight": 1500,
        "velocity": 200,
        "color": "red"
    }
    response = client.post("/api/v1/cars", json=car_data)
    assert response.status_code == 201
    data = response.json()
    assert data["length"] == car_data["length"]
    assert data["color"] == car_data["color"]

def test_search_cars(test_db):
    # First create a test car
    car_data = {
        "length": 4.5,
        "weight": 1500,
        "velocity": 200,
        "color": "red"
    }
    client.post("/api/v1/cars", json=car_data)
    
    # Test search
    search_criteria = {"color": "red"}
    response = client.post("/api/v1/cars/search", json=search_criteria)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["color"] == "red"

def test_search_cars_xml(test_db):
    # First create a test car
    car_data = {
        "length": 4.5,
        "weight": 1500,
        "velocity": 200,
        "color": "blue"
    }
    client.post("/api/v1/cars", json=car_data)
    
    # Test XML search
    search_criteria = {"color": "blue"}
    response = client.post("/api/v1/cars/search/xml", json=search_criteria)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/xml"
    assert b"<color>blue</color>" in response.content

def test_delete_car(test_db):
    # First create a car to delete
    car_data = {
        "length": 4.5,
        "weight": 1500,
        "velocity": 200,
        "color": "red"
    }
    response = client.post("/api/v1/cars", json=car_data)
    car_id = response.json()["id"]
    
    # Test deletion
    response = client.delete(f"/api/v1/cars/{car_id}")
    assert response.status_code == 204