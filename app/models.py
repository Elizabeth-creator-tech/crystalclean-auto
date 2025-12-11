from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


# User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User Model (Admin/Staff)
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='staff')  # 'admin' or 'staff'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    cars = db.relationship('Car', backref='assigned_user', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


# Service Model (Car Wash Services)
class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    cars = db.relationship('Car', backref='service', lazy='dynamic')
    
    def __repr__(self):
        return f'<Service {self.name}>'


# Car Model (Customer Jobs)
class Car(db.Model):
    __tablename__ = 'cars'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Customer Information
    customer_name = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(120))
    
    # Vehicle Information
    plate_number = db.Column(db.String(20), nullable=False, unique=True, index=True)
    car_model = db.Column(db.String(100))
    
    # Service Information
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Status and Timing
    status = db.Column(db.String(20), default='Waiting')  # Waiting, Washing, Detailing, Ready for Pickup, Completed
    time_in = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    time_out = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    def get_duration(self):
        """Calculate duration in minutes"""
        if self.time_out and self.time_in:
            delta = self.time_out - self.time_in
            return delta.total_seconds() / 60
        return None
    
    def __repr__(self):
        return f'<Car {self.plate_number}>'


# Notification Model
class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Notification {self.id}>'


# Archived Job Model (for completed jobs)
class ArchivedJob(db.Model):
    __tablename__ = 'archived_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    original_id = db.Column(db.Integer)  # Original Car ID
    
    # Customer Information
    customer_name = db.Column(db.String(120))
    customer_phone = db.Column(db.String(20))
    customer_email = db.Column(db.String(120))
    
    # Vehicle Information
    plate_number = db.Column(db.String(20), index=True)
    car_model = db.Column(db.String(100))
    
    # Service Information
    service_name = db.Column(db.String(100))
    service_price = db.Column(db.Float)
    service_duration = db.Column(db.Integer)
    
    # Staff Information
    staff_name = db.Column(db.String(120))
    staff_username = db.Column(db.String(80))
    
    # Job Details
    status = db.Column(db.String(20))
    notes = db.Column(db.Text)
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    
    # Archive timestamp
    archived_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<ArchivedJob {self.plate_number}>'