from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.review import Review
from marshmallow import fields, EXCLUDE

class ReviewSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        load_instance = True
        unknown = EXCLUDE 
    
    review_id = fields.Integer(dump_only=True)
    booking_id = fields.Integer()
    passenger_id = fields.Integer()
    driver_id = fields.Integer()
    rating = fields.Integer()
    comments = fields.String()
