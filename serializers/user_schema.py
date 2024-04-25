from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.user import User
from marshmallow import EXCLUDE, fields

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        unknown = EXCLUDE 

   # Add a plaintext password field for input
    password = fields.String(load_only=True)

    name = fields.String(dump_only=True)
    email = fields.String(dump_only=True)
    mobile_phone = fields.String(dump_only=True)