from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    with app.app_context():
        from app import routes
        
        db.create_all()
        
        create_default_users()
    
    return app

def create_default_users():
    from app.models import User
    
    print(" STARTING USER CREATION ")
    
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
        print(f"Processing user: {user_data['username']}")
        try:
            existing_user = User.query.filter(
                (User.username == user_data['username']) | 
                (User.email == user_data['email'])
            ).first()
            
            print(f"Existing user check: {existing_user}")
            
            if existing_user:
                print(f"⊘ User exists: {existing_user.username}, updating to {user_data['username']}...")
                existing_user.username = user_data['username']
                existing_user.full_name = user_data['full_name']
                existing_user.email = user_data['email']
                existing_user.set_password(user_data['password'])
                existing_user.role = user_data['role']
                existing_user.is_active = True
                db.session.commit()
                print(f"✓ Updated user: {user_data['username']} as {user_data['role']}")
            else:
                print(f"Creating new user: {user_data['username']}")
                user = User(
                    username=user_data['username'],
                    full_name=user_data['full_name'],
                    email=user_data['email'],
                    role=user_data['role'],
                    is_active=True
                )
                user.set_password(user_data['password'])
                db.session.add(user)
                db.session.commit()
                print(f"✓ Created new user: {user_data['username']} as {user_data['role']}")
                
        except Exception as e:
            print(f"✗ ERROR with {user_data['username']}: {str(e)}")
            db.session.rollback()
    
    print("USER CREATION COMPLETE")