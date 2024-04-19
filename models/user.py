from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy_utils import PasswordType, PhoneNumberType
from models.base import BaseModel
from app import db
from werkzeug.security import generate_password_hash



class User(BaseModel):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)

    password_hash = Column(PasswordType(
    schemes=['pbkdf2_sha256'],
    deprecated=['auto'],))

    role = Column(Enum('passenger', 'driver', 'admin', name='user_roles'))
    name = Column(String(100))
    mobile_phone = Column(PhoneNumberType())


    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)