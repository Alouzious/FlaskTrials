from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db  # Import db from the app context
from datetime import datetime

# User model class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    profile_picture = db.Column(db.String(120), nullable=True, default='default.jpg')  # Profile picture column

    def __init__(self, username, email, password, dob, country, profile_picture='default.jpg'):
        """Initialize a new User instance."""
        self.username = username
        self.email = email
        self.set_password(password)
        self.dob = dob
        self.country = country
        self.profile_picture = profile_picture

    # Set password (hashed)
    def set_password(self, password):
        """Hashes the password before storing it."""
        self.password_hash = generate_password_hash(password)

    # Check password (compare with hash)
    def check_password(self, password):
        """Compares a hashed password to the given password."""
        return check_password_hash(self.password_hash, password)

    # Method to return the full file path for the profile image
    def get_profile_picture(self):
        """Returns the path for the user's profile picture."""
        return 'static/profile_pics/' + self.profile_picture

    def __repr__(self):
        """Returns a string representation of the User object."""
        return f"<User {self.username}>"
