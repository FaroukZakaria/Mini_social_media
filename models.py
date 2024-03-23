#!/usr/bin/python3
"""
Created models are here
"""


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


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
    # Define the one-to-many relationship with Post
    user_posts = relationship('Post', back_populates='author')

    def __repr__(self):
        return "<User(id={}, first name={}, last name={}, email={})>".format(
                self.id,
                self.firstname,
                self.lastname,
                self.email
                )

class Post(Base):
     __tablename__ = 'posts'

     id = Column(Integer, primary_key=True)
     content = Column(String(60), nullable=False)
     author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
     author = relationship("User", back_populates="user_posts")

     def __repr__(self):
         return "<Post(id={}, content={}, author={})>".format(
                self.id,
                self.content,
                self.author
                )
