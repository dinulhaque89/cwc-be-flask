from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from models.base import BaseModel

class Vehicle(BaseModel):
    __tablename__ = 'vehicles'
    vehicle_id = Column(Integer, primary_key=True)
    driver_id = Column(Integer, ForeignKey('drivers.driver_id'), unique=True)  
    make = Column(String(50))
    model = Column(String(50))
    year = Column(Integer)
    license_plate = Column(String(20), unique=True)
    is_active = Column(Boolean, default=True)
    driver = relationship("Driver", back_populates="vehicle", uselist=False)