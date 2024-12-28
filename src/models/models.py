from sqlalchemy import Column, Integer, String, Float
from config.database import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    length = Column(Float, index=True)  # in meters
    weight = Column(Float, index=True)  # in kilograms
    velocity = Column(Float, index=True)  # in km/h
    color = Column(String, index=True)