from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel
from models.vehicle import Vehicle

class Driver(BaseModel):
    __tablename__ = 'drivers'
    driver_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    license_number = Column(String(20), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    vehicle = relationship("Vehicle", back_populates="driver", uselist=False)  
