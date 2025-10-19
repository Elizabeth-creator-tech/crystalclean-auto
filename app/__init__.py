from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints/routes
    with app.app_context():
        from app import routes
        
        # Create database tables
        db.create_all()
        
        # Create default users
        create_default_users()
    
    return app


def create_default_users():
    """Create default users if they don't exist"""
    from app.models import User
    
    users_to_create = [
        {
            'username': 'Mark',
            'full_name': 'Mark John',
            'email': 'admin@crystalclean.com',
            'role': 'admin',
            'password': 'johnmark'
        },
        {
            'username': 'Rachel',
            'full_name': 'Rachel Kirui',
            'email': 'kiruirachel@crystalclean.com',
            'role': 'staff',
            'password': 'johnmark'
        }
    ]
    
    for user_data in users_to_create:
        existing = User.query.filter_by(username=user_data['username']).first()
        if not existing:
            user = User(
                username=user_data['username'],
                full_name=user_data['full_name'],
                email=user_data['email'],
                role=user_data['role'],
                is_active=True
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            print(f"✓ Created user: {user_data['username']}")
    
    db.session.commit()