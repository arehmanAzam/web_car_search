from fastapi import APIRouter, Depends, HTTPException, Response,status
from sqlalchemy.orm import Session
from typing import List
import xml.etree.ElementTree as ET
from dicttoxml import dicttoxml

from src.schemas.car import CarSearchCriteria, CarResponse,CarBase
from config.database import get_db
from src.services.car_service import CarService
router = APIRouter()


@router.post("/cars", response_model=CarResponse)
async def add_car(
    car: CarBase,
    db: Session = Depends(get_db)
):
    car_service = CarService(db)
    return car_service.create_car(car)



@router.delete("/cars/{car_id}")
async def remove_car(
    car_id: int,
    db: Session = Depends(get_db)
):
    car_service = CarService(db)
    car_service.delete_car(car_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/cars/search", response_model=List[CarResponse])
async def search_cars(
    criteria: CarSearchCriteria,
    db: Session = Depends(get_db)
):
    car_service = CarService(db)
    return car_service.search_cars(criteria)

@router.post("/cars/search/xml")
async def search_cars_xml(
    criteria: CarSearchCriteria,
    db: Session = Depends(get_db)
):
    car_service = CarService(db)
    cars = car_service.search_cars(criteria)
    
    xml_data = dicttoxml(
        [car.dict() for car in cars], 
        custom_root='cars', 
        attr_type=False
    )
    
    return Response(
        content=xml_data,
        media_type="application/xml"
    )