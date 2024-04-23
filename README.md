# Mini_social_media

## Setup

### Required Dependencies:
- Python
- Flask 3.0.0
- Werkzeug 3.0.1
- MySQL
#### Note:
Change sql credentials in app.py if you want to try the app yourself

### Installation:
#### For PC:
1. Install Python from the official website.
2. Install Flask and Werkzeug using pip: ```pip install Flask==3.0.0 Werkzeug==3.0.1```
3. Install MySQL from the official website.

#### For Linux:
1. Install Python 3.8.10 using your package manager: ```sudo apt install python```
2. Install Flask and Werkzeug using pip: ```pip install Flask==3.0.0 Werkzeug==3.0.1```
3. Install MySQL using your package manager: ```sudo apt install mysql-server``` and ```sudo apt install mysql```

## Running the Application
- Use the command `./app.py` to start the application.
- The website can be accessed at `http://localhost:5000`.

### Note for Linux Users using vagrant:
- If running the site on a browser, edit the Vagrantfile located in `c/users/<user>` to port forward 5000 from host to 5000 on guest.

## Characteristics
- Home page displaying posts (if any created).
- Users page showcasing user activities.
- Login/signup functionality.
- Profile page showing user's details (displays "Me" if visitor's own profile).
- Edit/Delete post options for authors and admins.
- Commenting functionality.
- Viewing posts and respective likes.
