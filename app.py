#!/usr/bin/python3
"""
Main app
"""

from flask import Flask, render_template
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy to connect to the database
engine = create_engine('mysql://public:password@localhost/platform_data')


# Define a declarative base
Base = declarative_base()


# Define your SQLAlchemy models
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username}, email={self.email})>'

# Create the tables in the database
Base.metadata.create_all(engine)

##############################################################################


@app.route('/', strict_slashes=False)
def index():
    """
    Home
    """
    return render_template('index.html')

# PLACEHOLDER FOR MORE ROUTES


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
