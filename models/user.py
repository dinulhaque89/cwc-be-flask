from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy_utils import PhoneNumberType
from models.base import BaseModel
from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property



class User(BaseModel):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=True)
    role = Column(Enum('passenger', 'driver', 'admin', name='user_roles'))
    name = Column(String(100))
    mobile_phone = Column(PhoneNumberType())

    @hybrid_property
    def password(self):
        pass

    @password.setter
    def password(self, plaintext_password):
        password_hash = bcrypt.generate_password_hash(plaintext_password)
        print(f"Generated password hash: {password_hash}")
        self.password_hash = password_hash.decode('utf-8')

    def verify_password(self, password):
        print(f"Stored password hash: {self.password_hash}")
        return bcrypt.check_password_hash(self.password_hash.encode('utf-8'), password)

    def set_password(self, password):
        self.password = password 