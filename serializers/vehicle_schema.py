from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.vehicle import Vehicle
from marshmallow import EXCLUDE

class VehicleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicle
        load_instance = True
        unknown = EXCLUDE 
