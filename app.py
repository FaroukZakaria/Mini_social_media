#!/usr/bin/python3
"""
Main app
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User, Base, Post
import hashlib
import secrets
import string
import os

# Initialize Flask app
app = Flask(__name__)

# Generate a random string of ASCII letters, digits, and punctuation
secret_key = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(32))

# Set the Flask application's secret key
app.secret_key = secret_key

# Define the default upload folder location
app.config['UPLOAD_FOLDER'] = '/static/profile_pictures/'

# Configure SQLAlchemy to connect to the database
engine = create_engine('mysql://public:password@localhost/platform_data')

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a sessionmaker to handle database sessions
Session = sessionmaker(bind=engine)
dbsession = Session()


##############################################################################


@app.route('/', strict_slashes=False)
def index():
    """
    Home
    """
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """
    Login page
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Get the given information from database
        user = dbsession.query(User).filter_by(email=email).first()

        # Check if credentials are correct
        if user and user.password == hashlib.sha256(password.encode()).hexdigest():
            # Set up the session for the user
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            session['user_firstname'] = user.firstname
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Log out. Adding a log out route is only for organization of code
    and more complex operations in future if possible. I preferred this
    method over just making the logout button act as a submit button (HTML)
    """
    session.clear()

    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    """
    Signup page
    """
    if request.method == 'POST':
        firstname = request.form['fullname']
        lastname = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password using hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        new_user = User(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=hashed_password,
                picture="/static/default_profile_picture.jpg"
                )
        # Adding new user to database
        dbsession.add(new_user)
        dbsession.commit()

        # Flash a success message
        flash('Account created successfully!', 'success')

        return redirect(url_for('login'))

    return render_template('signup.html')
    
@app.route('/addPost', methods=['GET', 'POST'], strict_slashes=False)
def add_post():
    
    if request.method == 'POST':
        if 'user_id' in session:
            author_id = session['user_id']
            author = dbsession.query(User).get(author_id)
            content = request.form['content']

            if content:
                new_post = Post(
                        author=author,
                        content=content
                        )
                # Adding new pst to database
                dbsession.add(new_post)
                dbsession.commit()
                flash('Post created successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Content is required.', 'error')
                return redirect(url_for('addPost'))
        else:
            flash('You must be logged in to create a post.', 'error')
            return redirect(url_for('login'))
    return render_template('post.html')

@app.route('/posts')
def show_posts():
    
    posts = dbsession.query(Post).all()
    
    authors = {}
    for post in posts:
        author = dbsession.query(User).get(post.author_id)
        authors[post.id] = f"{author.firstname} {author.lastname}"
    return render_template('posts.html', posts=posts, authors=authors)

@app.route('/posts/<int:post_id>', strict_slashes=False)
def view_post(post_id):
    
    post = dbsession.query(Post).get(post_id)
    if post:
        author = dbsession.query(User).get(post.author_id)
        return render_template('viewPost.html', post=post, author=author)
    else:
        return "Post not found", 404

@app.route('/users')
def users():
    """
    All users page
    """
    if request.method == 'POST':
        query = request.form.get('query', '')
        search_res = [
                user for user in users if query.lower()
                in user['firstname'].lower()
                or query.lower()
                in user['lastname'].lower()
                ]
        return render_template('users.html', users=search_res, query=query)
    else:
        users = dbsession.query(User).all()
        return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def user_profile(user_id):
    """
    Show user profile
    """
    if 'user_id' in session:
        curr_user = session['user_id']

    user = dbsession.query(User).get(user_id)
    if user:
        if 'user_id' in session:
            curr_user = session['user_id']
            is_current_user = (user.id == curr_user)
        else:
            is_current_user = False
        return render_template('profile.html', user=user, is_current_user=is_current_user)
    else:
        return "User not found", 404

@app.route('/about', strict_slashes=False)
def about():
    """
    About page
    """
    return render_template('about.html')

@app.route('/navbar')
def navbar():
    """
    Navigation bar at top
    """
    return render_template('navbar.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'new_picture' not in request.files:
        flash('No uploaded files', 'error')
        return redirect(url_for('profile'))
    new_picture = request.files['new_picture']

    if new_picture.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('profile'))
    filename = str(user_id) + '.jpg'
    file_path = '/static/profile_pictures/' + filename
    new_picture.save(file_path)

    flash('Uploaded successfully', 'success')
    return redirect(url_for('profile'))

@app.route('/change_picture', methods=['POST'])
def change_picture():
    if 'user_id' in session:
        user_id = session['user_id']
        if 'new_picture' in request.files:
            new_picture = request.files['new_picture']
            if new_picture.content_length > 1048576:  # Limit file size to 1MB
                flash('File size is too large. Please upload a file under 1MB.', 'error')
                return redirect(url_for('profile'))

            pic = dbsession.query(User).get(user_id).picture
            if pic != "/static/profile_pictures/default.jpg":
                # Code here to change the existing record to something else in database
                pass

            filename = f"{user_id}.jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                new_picture.save(filepath)
            except IOError as e:
                flash('Error saving file: {}'.format(e), 'error')
                return redirect(url_for('profile'))


            user = dbsession.query(User).get(user_id)
            user.picture = '/static/profile_pictures/' + filename
            dbsession.commit()
            flash('Profile picture updated successfully!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('No file uploaded!', 'error')
            return redirect(url_for('profile'))
    else:
        flash('You must be logged in to change your profile picture.', 'error')
        return redirect(url_for('login'))

# PLACEHOLDER FOR MORE ROUTES


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
