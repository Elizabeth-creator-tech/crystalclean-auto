from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """
    Decorator to require admin role for a route
    Usage: @admin_required
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        
        if current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('staff_dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function


def send_notification(car, status):
    """
    Send SMS/Email notification to customer
    This is a placeholder function - implement with actual SMS/Email service
    
    Args:
        car: Car object
        status: Current status of the job
    """
    # TODO: Implement actual SMS/Email sending
    # Example services: Africa's Talking (SMS), SendGrid (Email), Twilio (SMS)
    
    # For now, just log the notification
    print(f"[NOTIFICATION] To: {car.customer_phone}")
    print(f"[NOTIFICATION] Message: Your car {car.plate_number} is now {status}")
    
    # Create notification record
    from app.models import Notification
    from app import db
    
    notification = Notification(
        car_id=car.id,
        notification_type='sms',
        status=status,
        is_delivered=False  # Set to True when actually sent
    )
    db.session.add(notification)
    db.session.commit()
    
    return True


def format_phone_number(phone):
    """
    Format phone number to standard Kenyan format
    Converts 0712345678 to +254712345678
    
    Args:
        phone: Phone number string
    
    Returns:
        Formatted phone number
    """
    #we can use one line of regex too: phone = re.sub(r'[^\d+]', '', phone)

    phone = phone.strip().replace(' ', '').replace('-', '')
    
    if phone.startswith('0'):
        phone = '+254' + phone[1:]
    elif phone.startswith('254'):
        phone = '+' + phone
    elif not phone.startswith('+'):
        phone = '+254' + phone
    
    return phone


def format_currency(amount):
    """
    Format amount as Kenyan Shillings
    
    Args:
        amount: Numeric amount
    
    Returns:
        Formatted string like "KSh 1,500.00"
    """
    return f"KSh {amount:,.2f}"


def calculate_duration(time_in, time_out):
    """
    Calculate duration between two datetime objects
    
    Args:
        time_in: Start datetime
        time_out: End datetime
    
    Returns:
        Duration in minutes
    """
    if not time_out:
        return None
    
    delta = time_out - time_in
    return int(delta.total_seconds() / 60)


def get_status_color(status):
    """
    Get color class for status badge
    
    Args:
        status: Job status string
    
    Returns:
        CSS class name
    """
    status_colors = {
        'Waiting': 'badge-waiting',
        'Washing': 'badge-washing',
        'Detailing': 'badge-detailing',
        'Ready for Pickup': 'badge-ready',
        'Completed': 'badge-completed',
        'Cancelled': 'badge-cancelled'
    }
    return status_colors.get(status, 'badge-waiting')


def validate_plate_number(plate):
    """
    Validate Kenyan plate number format
    Basic validation for format like: KXX 000X
    
    Args:
        plate: Plate number string
    
    Returns:
        Boolean indicating if valid
    """
    import re
    plate = plate.upper().strip()
    
    # Basic pattern: 3 letters, space, 3 digits, 1 letter
    pattern = r'^[A-Z]{3}\s?\d{3}[A-Z]'
    
    if re.match(pattern, plate):
        return True
    return False


def generate_report_data(start_date, end_date):
    """
    Generate report data for a date range
    
    Args:
        start_date: Start date
        end_date: End date
    
    Returns:
        Dictionary with report data
    """
    from app.models import Car, Service, User
    from app import db
    from datetime import datetime
    
    # Jobs completed in range
    jobs = Car.query.filter(
        Car.status == 'Completed',
        Car.updated_at >= start_date,
        Car.updated_at <= end_date
    ).all()
    
    # Calculate revenue
    total_revenue = sum([job.service.price for job in jobs])
    
    # Average duration
    durations = [calculate_duration(job.time_in, job.time_out) for job in jobs if job.time_out]
    avg_duration = sum(durations) / len(durations) if durations else 0
    
    # Most popular service
    service_counts = {}
    for job in jobs:
        service_name = job.service.name
        service_counts[service_name] = service_counts.get(service_name, 0) + 1
    
    popular_service = max(service_counts.items(), key=lambda x: x[1])[0] if service_counts else 'N/A'
    
    return {
        'total_jobs': len(jobs),
        'total_revenue': total_revenue,
        'avg_duration': avg_duration,
        'popular_service': popular_service,
        'jobs': jobs
    }