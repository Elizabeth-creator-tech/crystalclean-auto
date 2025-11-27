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
    
    with db.session.no_autoflush:
        for user_data in users_to_create:
            try:
                existing_user = User.query.filter(
                    (User.username == user_data['username']) | 
                    (User.email == user_data['email'])
                ).first()
                
                if not existing_user:
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
                else:
                    print(f"⊘ User already exists: {user_data['username']}")
                    
            except Exception as e:
                print(f"✗ Error creating {user_data['username']}: {str(e)}")
                db.session.rollback()
    
    try:
        db.session.commit()
        print("✓ All users processed successfully")
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error committing users: {str(e)}")