#!/usr/bin/python3
"""
Main app
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User, Base
import hashlib
import secrets
import string

# Initialize Flask app
app = Flask(__name__)

# Generate a random string of ASCII letters, digits, and punctuation
secret_key = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(32))

# Set the Flask application's secret key
app.secret_key = secret_key

# Configure SQLAlchemy to connect to the database
engine = create_engine('mysql://public:password@localhost/platform_data')

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a sessionmaker to handle database sessions
Session = sessionmaker(bind=engine)
session = Session()


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

@app.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    """
    Signup page
    """
    if request.method == 'POST':
        print("starting")
        firstname = request.form['fullname']
        print("first name")
        lastname = request.form['username']
        print("last name")
        email = request.form['email']
        password = request.form['password']

        # Hash the password using hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        new_user = User(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=hashed_password
                )
        # Adding new user to database
        session.add(new_user)
        session.commit()

        # Flash a success message
        flash('Account created successfully!', 'success')

        return redirect(url_for('index'))

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
