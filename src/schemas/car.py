from pydantic import BaseModel, Field
from typing import List

class CarBase(BaseModel):
    length: float = Field(..., description="Length of the car in meters")
    weight: float = Field(..., description="Weight of the car in kilograms")
    velocity: float = Field(..., description="Maximum velocity in km/h")
    color: str = Field(..., description="Color of the car")

class CarResponse(CarBase):
    id: int

    class Config:
        from_attributes = True

class CarSearchCriteria(BaseModel):
    min_length: float | None = Field(None, description="Minimum length in meters")
    max_length: float | None = Field(None, description="Maximum length in meters")
    min_weight: float | None = Field(None, description="Minimum weight in kilograms")
    max_weight: float | None = Field(None, description="Maximum weight in kilograms")
    min_velocity: float | None = Field(None, description="Minimum velocity in km/h")
    max_velocity: float | None = Field(None, description="Maximum velocity in km/h")
    color: str | None = Field(None, description="Specific color to search for")

class CarXMLResponse(BaseModel):
    cars: List[CarResponse]