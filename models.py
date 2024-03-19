#!/usr/bin/python3
"""
Created models are here
"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# Define your SQLAlchemy models
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(60), nullable=False)
    lastname = Column(String(60), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    is_admin = False

    def __repr__(self):
        return "<User(id={}, first name={}, last name={}, email={})>".format(
                self.id,
                self.firstname,
                self.lastname,
                self.email
                )
