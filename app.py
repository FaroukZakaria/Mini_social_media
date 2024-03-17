#!/usr/bin/python3
"""
Main app
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy to connect to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://demo:password@localhost/platform_data'


# Initialize SQLAlchemy
db = SQLAlchemy(app)

##############################################################################


@app.route('/', strict_slashes=False)
def index():
    """
    Home
    """
    return render_template('index.html')

# PLACEHOLDER FOR MORE ROUTES


class User(db.Model):
    """
    User Model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


if __name__ == "__main__":
    try:
        # Try to create a connection to the database
        # db.create_all()
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        # If an error occurs, print the error message
        app.logger.error("Error connecting to the database:", e)
