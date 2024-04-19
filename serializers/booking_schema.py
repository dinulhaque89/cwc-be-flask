from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.booking import Booking
from models.user import User
from models.driver import Driver
from marshmallow import fields
from serializers.user_schema import UserSchema
from serializers.driver_schema import DriverSchema


class BookingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        load_instance = True
        include_fk = True
        passenger_id = auto_field()
        driver_id = auto_field()
    
    passenger = fields.Nested('UserSchema', only=('name', 'email'), dump_only=True)
    driver = fields.Nested('DriverSchema', only=('name', 'license_number'), dump_only=True)