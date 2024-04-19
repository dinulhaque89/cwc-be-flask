from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.review import Review
from marshmallow import fields, EXCLUDE

class ReviewSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        load_instance = True
        unknown = EXCLUDE 
    
    rating = fields.Integer()
    comments = fields.String()
