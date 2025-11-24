from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError, EqualTo
from app.models import User, Service, Car
from flask_login import current_user


class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')


class AddCarForm(FlaskForm):
    """Form to add a new car/job"""
    # Customer Information
    customer_name = StringField('Customer Name', validators=[DataRequired(), Length(max=120)])
    customer_phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    customer_email = StringField('Email', validators=[Optional(), Email()])
    
    # Vehicle Information
    plate_number = StringField('Plate Number', validators=[DataRequired(), Length(max=20)])
    car_model = StringField('Car Model', validators=[Optional(), Length(max=100)])
    
    # Service Information
    service_id = SelectField('Service', coerce=int, validators=[DataRequired()])
    assigned_user_id = SelectField('Assign to Staff', coerce=int, validators=[DataRequired()])
    notes = TextAreaField('Additional Notes', validators=[Optional()])
    
    def validate_plate_number(self, field):
        """Check if plate number already exists"""
        plate = field.data.upper().strip()
        existing = Car.query.filter_by(plate_number=plate).first()
        if existing:
            raise ValidationError('This plate number is already registered in the system.')


class EditCarForm(FlaskForm):
    """Form to edit an existing car/job"""
    # Customer Information
    customer_name = StringField('Customer Name', validators=[DataRequired(), Length(max=120)])
    customer_phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    customer_email = StringField('Email', validators=[Optional(), Email()])
    
    # Vehicle Information
    plate_number = StringField('Plate Number', validators=[DataRequired(), Length(max=20)])
    car_model = StringField('Car Model', validators=[Optional(), Length(max=100)])
    
    # Service Information
    service_id = SelectField('Service', coerce=int, validators=[DataRequired()])
    assigned_user_id = SelectField('Assign to Staff', coerce=int, validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('Waiting', 'Waiting'),
        ('Washing', 'Washing'),
        ('Detailing', 'Detailing'),
        ('Ready for Pickup', 'Ready for Pickup'),
        ('Completed', 'Completed')
    ], validators=[DataRequired()])
    notes = TextAreaField('Additional Notes', validators=[Optional()])


class AddServiceForm(FlaskForm):
    """Form to add a new service"""
    name = StringField('Service Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    price = FloatField('Price (KSh)', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()])
    
    def validate_name(self, field):
        """Check if service name already exists"""
        existing = Service.query.filter_by(name=field.data.strip()).first()
        if existing:
            raise ValidationError('A service with this name already exists.')
    
    def validate_price(self, field):
        """Validate price is positive"""
        if field.data <= 0:
            raise ValidationError('Price must be greater than 0.')
    
    def validate_duration(self, field):
        """Validate duration is positive"""
        if field.data <= 0:
            raise ValidationError('Duration must be greater than 0.')


class EditServiceForm(FlaskForm):
    """Form to edit an existing service"""
    name = StringField('Service Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    price = FloatField('Price (KSh)', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()])
    
    def validate_price(self, field):
        """Validate price is positive"""
        if field.data <= 0:
            raise ValidationError('Price must be greater than 0.')
    
    def validate_duration(self, field):
        """Validate duration is positive"""
        if field.data <= 0:
            raise ValidationError('Duration must be greater than 0.')


class AddUserForm(FlaskForm):
    """Form to add a new user"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('staff', 'Staff')], validators=[DataRequired()])
    is_active = BooleanField('Active', default=True)
    
    def validate_username(self, field):
        """Check if username already exists"""
        existing = User.query.filter_by(username=field.data.strip()).first()
        if existing:
            raise ValidationError('This username is already taken.')
    
    def validate_email(self, field):
        """Check if email already exists"""
        existing = User.query.filter_by(email=field.data.strip()).first()
        if existing:
            raise ValidationError('This email is already registered.')


class EditUserForm(FlaskForm):
    """Form to edit an existing user"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('staff', 'Staff')], validators=[DataRequired()])
    is_active = BooleanField('Active')


class UpdateStatusForm(FlaskForm):
    """Form to update job status"""
    status = SelectField('Status', choices=[
        ('Waiting', 'Waiting'),
        ('Washing', 'Washing'),
        ('Detailing', 'Detailing'),
        ('Ready for Pickup', 'Ready for Pickup'),
        ('Completed', 'Completed')
    ], validators=[DataRequired()])

#USERS CAN CHANGE PROFILE/EDIT
class UpdateProfileForm(FlaskForm):
    """Form for users to update their own profile"""
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password (required for verification)', validators=[DataRequired()])
    new_password = PasswordField('New Password (leave blank to keep current)', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[Optional()])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('staff', 'Staff')], validators=[Optional()])
    
    def validate_new_password(self, field):
        """Validate new password if provided"""
        if field.data and not self.confirm_password.data:
            raise ValidationError('Please confirm your new password.')
    
    def validate_confirm_password(self, field):
        """Validate password confirmation matches"""
        if field.data and field.data != self.new_password.data:
            raise ValidationError('Passwords do not match.')
    
    def validate_email(self, field):
        """Check if email is already used by another user"""
        # Import here to avoid circular imports
        from app.models import User
        from flask_login import current_user
        
        existing = User.query.filter_by(email=field.data.strip()).first()
        if existing and existing.id != current_user.id:
            raise ValidationError('This email is already registered by another user.')
