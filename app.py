#!/usr/bin/python3
"""
Main app
"""

from flask import Flask, render_template
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User, Base

# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy to connect to the database
engine = create_engine('mysql://public:password@localhost/platform_data')

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a sessionmaker to handle database sessions
Session = sessionmaker(bind=engine)
session = Session()

#print(session.query(User).all())


##############################################################################


@app.route('/', strict_slashes=False)
def index():
    """
    Home
    """
    return render_template('index.html')

@app.route('/login', strict_slashes=False)
def login():
    """
    Login page
    """
    return render_template('login.html')

@app.route('/signup', strict_slashes=False)
def signup():
    """
    Signup page
    """
    return render_template('signup.html')

@app.route('/about', strict_slashes=False)
def about():
    """
    About page
    """
    return render_template('about.html')

# PLACEHOLDER FOR MORE ROUTES


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
