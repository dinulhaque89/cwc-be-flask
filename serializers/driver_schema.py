from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.driver import Driver
from marshmallow import EXCLUDE

class DriverSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Driver
        load_instance = True
        unknown = EXCLUDE 
