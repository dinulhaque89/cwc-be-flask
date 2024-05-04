from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Time
from sqlalchemy.ext.hybrid import hybrid_property
from app import db

from models.base import BaseModel

class Booking(BaseModel):
    __tablename__ = 'bookings'
    booking_id = Column(Integer, primary_key=True)
    passenger_id = Column(Integer, ForeignKey('users.user_id'))
    driver_id = Column(Integer, ForeignKey('drivers.driver_id'), nullable=True)
    status = Column(String(50), nullable=True)
    start_location = Column(String(200))
    end_location = Column(String(200))
    booking_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time, nullable=True)
    status = Column(String(50))
    fare = Column(Float)

