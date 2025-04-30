from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# Initialize database and login manager
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # Redirect to login if not authenticated

# Create the app instance
def create_app():
    app = Flask(__name__)  # Create the app instance

    # Configuration
    app.config['SECRET_KEY'] = os.urandom(24)  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['UPLOAD_FOLDER'] = 'static/profile_pics'  # Folder for profile pictures
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file upload size (16MB)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Import models only after db is initialized
    from .models import User

    # Define user_loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .auth import auth as auth_blueprint
    from .dashboard import dashboard as dashboard_blueprint
    from .home import home as home_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
    app.register_blueprint(home_blueprint, url_prefix='/')

    # Initialize migrate instance
    migrate = Migrate(app, db)

    return app
