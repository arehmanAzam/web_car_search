from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.models.models import Car
from src.schemas.car import CarSearchCriteria, CarBase
from fastapi import HTTPException, status

class CarService:
    def __init__(self, db: Session):
        self.db = db

    def create_car(self, car: CarBase):
        db_car = Car(
            length=car.length,
            weight=car.weight,
            velocity=car.velocity,
            color=car.color
        )
        self.db.add(db_car)
        try:
            self.db.commit()
            self.db.refresh(db_car)
            return db_car
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create car"
            )

    def delete_car(self, car_id: int):
        car = self.db.query(Car).filter(Car.id == car_id).first()
        if not car:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found"
            )
        try:
            self.db.delete(car)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete car"
            )


    def search_cars(self, criteria: CarSearchCriteria):
        query = self.db.query(Car)
        
        if criteria.min_length is not None:
            query = query.filter(Car.length >= criteria.min_length)
        if criteria.max_length is not None:
            query = query.filter(Car.length <= criteria.max_length)
            
        if criteria.min_weight is not None:
            query = query.filter(Car.weight >= criteria.min_weight)
        if criteria.max_weight is not None:
            query = query.filter(Car.weight <= criteria.max_weight)
            
        if criteria.min_velocity is not None:
            query = query.filter(Car.velocity >= criteria.min_velocity)
        if criteria.max_velocity is not None:
            query = query.filter(Car.velocity <= criteria.max_velocity)
            
        if criteria.color is not None:
            query = query.filter(Car.color == criteria.color)
        return query.all()