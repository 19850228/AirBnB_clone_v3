import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt


class User(BaseModel, Base):
    """Representation of a user"""

    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password_hash = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    places = relationship("Place", backref="user")
    reviews = relationship("Review", backref="user")

    def __init__(self, *args, **kwargs):
        """Initializes a user"""
        super().__init__(*args, **kwargs)

        if 'password' in kwargs:
            self.set_password(kwargs['password'])

    def set_password(self, password: str) -> None:
        """Sets the user's password securely"""
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password: str) -> bool:
        """Checks if the provided password matches the user's password"""
        return bcrypt.verify(password, self.password_hash)
