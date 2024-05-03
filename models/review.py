from sqlalchemy import Column, Integer, String, ForeignKey, Index
from models.base import BaseModel
from app import db
from models.booking import Booking
from models.user import User
from models.driver import Driver

class Review(BaseModel):
    __tablename__ = 'reviews'
    review_id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.booking_id'))
    passenger_id = Column(Integer, ForeignKey('users.user_id'))
    driver_id = Column(Integer, ForeignKey('drivers.driver_id'))
    rating = Column(Integer)
    comments = Column(String(300))

    __table_args__ = (
        Index('idx_driver_id', 'driver_id'), 
    )