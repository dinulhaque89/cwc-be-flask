from datetime import datetime
from app import db  


class BaseModel(db.Model):
    """
    Custom base class that includes ID, creation, and update timestamps.
    This class provides common fields and utility methods to all models.
    """
    __abstract__ = True 

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """
        Saves the current object instance to the database.
        """
        db.session.add(self)
        db.session.commit()

    def remove(self):
        """
        Removes the current object instance from the database.
        """
        db.session.delete(self)
        db.session.commit()