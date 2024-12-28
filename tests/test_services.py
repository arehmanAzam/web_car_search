# tests/test_services.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.services.car_service import CarService
from src.models.models import Base, Car
from src.schemas.car import CarBase, CarSearchCriteria

# Test database setup
SQLALCHEMY_DATABASE_URL = "postgresql://abdul:Rehman123@localhost:5432/car_search_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def car_service(db_session):
    return CarService(db_session)

def test_create_car(car_service):
    car_data = CarBase(
        length=4.5,
        weight=1500,
        velocity=200,
        color="red"
    )
    car = car_service.create_car(car_data)
    assert car.length == 4.5
    assert car.color == "red"

def test_search_cars(car_service, db_session):
    # Create test cars
    car1 = Car(length=4.5, weight=1500, velocity=200, color="red")
    car2 = Car(length=5.0, weight=1600, velocity=180, color="blue")
    db_session.add(car1)
    db_session.add(car2)
    db_session.commit()

    # Test search by color
    criteria = CarSearchCriteria(color="red")
    results = car_service.search_cars(criteria)
    assert len(results) == 1
    assert results[0].color == "red"

    # Test search by multiple criteria
    criteria = CarSearchCriteria(
        length=4.5,
        velocity=200
    )
    results = car_service.search_cars(criteria)
    assert len(results) == 1
    assert results[0].length == 4.5

def test_delete_car(car_service, db_session):
    # Create a car to delete
    car = Car(length=4.5, weight=1500, velocity=200, color="red")
    db_session.add(car)
    db_session.commit()

    # Test deletion
    car_service.delete_car(car.id)
    result = db_session.query(Car).filter(Car.id == car.id).first()
    assert result is None