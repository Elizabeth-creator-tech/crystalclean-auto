#from flask import Markup
from flask import render_template, redirect, url_for, flash, request, current_app as app, jsonify
from markupsafe import Markup #allows python not assume hyper link.
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, date, timedelta
from app import db
from app.models import User, Service, Car, Notification, ArchivedJob #classes
from app.forms import (LoginForm, AddCarForm, EditCarForm, AddServiceForm, 
                       EditServiceForm, AddUserForm, EditUserForm, UpdateStatusForm)
from app.utils import admin_required, send_notification

def kenya_time(dt):
    """Convert UTC to Kenya time (UTC+3)"""
    if dt is None:
        return None
    return dt + timedelta(hours=3)

def get_today_start_end_utc():
    """Get today's date range in UTC for Kenya timezone
    Kenya is UTC+3, so we need to adjust the UTC queries accordingly
    """
    # Current time in Kenya
    now_kenya = datetime.utcnow() + timedelta(hours=3)
    today_kenya = now_kenya.date()
    
    # Start of today in Kenya time, converted to UTC
    start_of_day_kenya = datetime.combine(today_kenya, datetime.min.time())
    start_of_day_utc = start_of_day_kenya - timedelta(hours=3)
    
    # End of today in Kenya time, converted to UTC
    end_of_day_kenya = datetime.combine(today_kenya, datetime.max.time())
    end_of_day_utc = end_of_day_kenya - timedelta(hours=3)
    
    return start_of_day_utc, end_of_day_utc

def auto_archive_old_jobs():
    """Automatically archive completed jobs older than 24 hours"""
    cutoff_time = datetime.utcnow() - timedelta(hours=24)
    
    old_completed_jobs = Car.query.filter(
        Car.status == 'Completed',
        Car.time_out != None,
        Car.time_out < cutoff_time
    ).all()
    
    archived_count = 0
    for job in old_completed_jobs:
        # Create archive record
        duration = job.get_duration()
        archived = ArchivedJob(
            original_id=job.id,
            plate_number=job.plate_number,
            car_model=job.car_model,
            customer_name=job.customer_name,
            customer_phone=job.customer_phone,
            customer_email=job.customer_email,
            service_name=job.service.name,
            service_price=job.service.price,
            service_duration=job.service.duration,
            staff_name=job.assigned_user.full_name if job.assigned_user else None,
            staff_username=job.assigned_user.username if job.assigned_user else None,
            status=job.status,
            notes=job.notes,
            time_in=job.time_in,
            time_out=job.time_out,
            duration_minutes=int(duration) if duration else None,
            archived_at=datetime.utcnow()
        )
        db.session.add(archived)
        db.session.delete(job)
        archived_count += 1
    
    if archived_count > 0:
        db.session.commit()
        print(f"[AUTO-ARCHIVE] Archived {archived_count} completed jobs older than 24 hours")
    
    return archived_count


# AUTHENTICATION ROUTES


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('staff_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        print(f"\n=== LOGIN ATTEMPT ===")
        print(f"Username: {form.username.data}")
        print(f"Password: {form.password.data}")
        
        user = User.query.filter_by(username=form.username.data).first()
        print(f"User found in DB: {user}")
        
        if user:
            pwd_check = user.check_password(form.password.data)
            print(f"Password check result: {pwd_check}")
        
        if user is None or not user.check_password(form.password.data):
            print("LOGIN FAILED: Invalid credentials")
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
        
        if not user.is_active:
            print("LOGIN FAILED: User inactive")
            flash(Markup('Your account was deactivated. Please contact admin at <a href="mailto:admin@crystalclean.com">admin@crystalclean.com</a>'), 'error')
            return redirect(url_for('login'))
        
        print(f"LOGIN SUCCESS: Logging in user {user.username}")
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome back, {user.full_name}!', 'success')
        
        if user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('staff_dashboard'))
    
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))



# ADMIN DASHBOARD


@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard with statistics and job list"""
    # Auto-archive old jobs on each dashboard load
    auto_archive_old_jobs()
    
    # Get today's date range in UTC
    start_of_day_utc, end_of_day_utc = get_today_start_end_utc()
    
    # Total jobs created today (using time_in which is when job was created)
    total_jobs = Car.query.filter(
        Car.time_in >= start_of_day_utc,
        Car.time_in <= end_of_day_utc
    ).count()
    
    # Jobs in progress (any day, not completed)
    in_progress = Car.query.filter(
        Car.status.in_(['Waiting', 'Washing', 'Detailing', 'Ready for Pickup'])
    ).count()
    
    # Jobs completed today (based on time_out) - INCLUDING STILL IN DATABASE
    completed_today = Car.query.filter(
        Car.status == 'Completed',
        Car.time_out != None,
        Car.time_out >= start_of_day_utc,
        Car.time_out <= end_of_day_utc
    ).count()
    
    # Calculate revenue for jobs completed today
    completed_jobs_today = Car.query.filter(
        Car.status == 'Completed',
        Car.time_out != None,
        Car.time_out >= start_of_day_utc,
        Car.time_out <= end_of_day_utc
    ).all()
    
    revenue = sum([job.service.price for job in completed_jobs_today])
    
    # Get all active jobs (not completed) + completed jobs from today
    active_cars = Car.query.filter(
        db.or_(
            Car.status != 'Completed',
            db.and_(
                Car.status == 'Completed',
                Car.time_out >= start_of_day_utc,
                Car.time_out <= end_of_day_utc
            )
        )
    ).order_by(Car.time_in.desc()).all()
    
    # Convert times to Kenya timezone for display
    for car in active_cars:
        car.time_in_display = kenya_time(car.time_in)
        car.time_out_display = kenya_time(car.time_out)
    
    stats = {
        'total_jobs': total_jobs,
        'in_progress': in_progress,
        'completed': completed_today,
        'revenue': f'{revenue:,.0f}'
    }
    
    return render_template('admin_dashboard.html', stats=stats, cars=active_cars)



# DATA MANAGEMENT ROUTES


@app.route('/admin/archive-now', methods=['POST']) #when data sends post request here, the archive_now() is called 
@login_required #ensures that only logged-in users can access this route
@admin_required
def archive_now():
    """Manually trigger archiving of completed jobs"""
    archived_count = auto_archive_old_jobs()
    
    if archived_count > 0:
        flash(f'Successfully archived {archived_count} completed jobs!', 'success')
    else:
        flash('No completed jobs to archive at this time.', 'info')
    
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/clear-today', methods=['POST'])
@login_required
@admin_required
def clear_today_data():
    """Clear today's active jobs (move completed to archive, delete rest)"""
    start_of_day_utc, end_of_day_utc = get_today_start_end_utc()
    
    # Get today's jobs
    todays_jobs = Car.query.filter(
        Car.time_in >= start_of_day_utc,
        Car.time_in <= end_of_day_utc
    ).all()
    
    completed_count = 0
    deleted_count = 0
    
    for job in todays_jobs:
        if job.status == 'Completed' and job.time_out:
            # Archive completed jobs
            duration = job.get_duration()
            archived = ArchivedJob(
                original_id=job.id,
                plate_number=job.plate_number,
                car_model=job.car_model,
                customer_name=job.customer_name,
                customer_phone=job.customer_phone,
                customer_email=job.customer_email,
                service_name=job.service.name,
                service_price=job.service.price,
                service_duration=job.service.duration,
                staff_name=job.assigned_user.full_name if job.assigned_user else None,
                staff_username=job.assigned_user.username if job.assigned_user else None,
                status=job.status,
                notes=job.notes,
                time_in=job.time_in,
                time_out=job.time_out,
                duration_minutes=int(duration) if duration else None,
                archived_at=datetime.utcnow()
            )
            db.session.add(archived)
            completed_count += 1
        
        # Delete job from active table
        db.session.delete(job)
        deleted_count += 1
    
    db.session.commit()
    flash(f'Cleared {deleted_count} jobs from today ({completed_count} archived, {deleted_count - completed_count} deleted)', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/analytics')
@login_required
@admin_required
def analytics():
    """Full analytics page with archived data"""
    # Total archived jobs
    total_archived = ArchivedJob.query.count()
    
    # Total revenue (all time from archives)
    total_revenue = db.session.query(db.func.sum(ArchivedJob.service_price)).scalar() or 0
    
    # Most popular service
    popular_services = db.session.query(
        ArchivedJob.service_name,
        db.func.count(ArchivedJob.id).label('count'),
        db.func.sum(ArchivedJob.service_price).label('revenue')
    ).group_by(ArchivedJob.service_name).order_by(db.desc('count')).limit(10).all()
    
    # Top customers (by number of visits)
    top_customers = db.session.query(
        ArchivedJob.customer_name,
        ArchivedJob.customer_phone,
        db.func.count(ArchivedJob.id).label('visits'),
        db.func.sum(ArchivedJob.service_price).label('total_spent')
    ).group_by(ArchivedJob.customer_name, ArchivedJob.customer_phone).order_by(
        db.desc('visits')
    ).limit(10).all()
    
    # Staff performance (all time)
    staff_stats = db.session.query(
        ArchivedJob.staff_name,
        db.func.count(ArchivedJob.id).label('jobs_done'),
        db.func.avg(ArchivedJob.duration_minutes).label('avg_duration')
    ).filter(ArchivedJob.staff_name != None).group_by(
        ArchivedJob.staff_name
    ).order_by(db.desc('jobs_done')).all()
    
    # Average duration per service
    service_durations = db.session.query(
        ArchivedJob.service_name,
        db.func.avg(ArchivedJob.duration_minutes).label('avg_duration'),
        db.func.min(ArchivedJob.duration_minutes).label('min_duration'),
        db.func.max(ArchivedJob.duration_minutes).label('max_duration')
    ).filter(ArchivedJob.duration_minutes != None).group_by(
        ArchivedJob.service_name
    ).all()
    
    return render_template('analytics.html',
                         total_archived=total_archived,
                         total_revenue=total_revenue,
                         popular_services=popular_services,
                         top_customers=top_customers,
                         staff_stats=staff_stats,
                         service_durations=service_durations)


@app.route('/admin/archived-jobs')
@login_required
@admin_required
def view_archived_jobs():
    """View all archived jobs with search and pagination"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = ArchivedJob.query
    
    # Search filter
    if search:
        query = query.filter(
            db.or_(
                ArchivedJob.plate_number.ilike(f'%{search}%'),
                ArchivedJob.customer_name.ilike(f'%{search}%'),
                ArchivedJob.customer_phone.ilike(f'%{search}%')
            )
        )
    
    # Paginate results
    archived_jobs = query.order_by(ArchivedJob.archived_at.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    
    return render_template('archived_jobs.html', 
                         archived_jobs=archived_jobs,
                         search=search)


@app.route('/admin/delete-archive/<int:archive_id>', methods=['POST'])
@login_required
@admin_required
def delete_archived_job(archive_id):
    """Delete a specific archived job"""
    archived = ArchivedJob.query.get_or_404(archive_id)
    plate = archived.plate_number
    db.session.delete(archived)
    db.session.commit()
    flash(f'Archived job for {plate} deleted permanently!', 'success')
    return redirect(url_for('view_archived_jobs'))


@app.route('/admin/clear-all-archives', methods=['POST'])
@login_required
@admin_required
def clear_all_archives():
    """Delete ALL archived jobs (with confirmation)"""
    count = ArchivedJob.query.count()
    ArchivedJob.query.delete()
    db.session.commit()
    flash(f'Permanently deleted {count} archived jobs!', 'warning')
    return redirect(url_for('analytics'))



# STAFF DASHBOARD


@app.route('/staff/dashboard')
@login_required
def staff_dashboard():
    """Staff dashboard with assigned tasks"""
    # Get today's date range in UTC
    start_of_day_utc, end_of_day_utc = get_today_start_end_utc()
    
    # Get assigned cars that are NOT completed yet
    assigned_cars = Car.query.filter(
        Car.assigned_user_id == current_user.id,
        Car.status != 'Completed'
    ).order_by(Car.time_in.desc()).all()
    
    # Get completed cars today (based on completion time) - STILL IN DATABASE
    completed_cars = Car.query.filter(
        Car.assigned_user_id == current_user.id,
        Car.status == 'Completed',
        Car.time_out != None,
        Car.time_out >= start_of_day_utc,
        Car.time_out <= end_of_day_utc
    ).order_by(Car.time_out.desc()).all()
    
    # Convert times to Kenya timezone for display
    for car in assigned_cars + completed_cars:
        car.time_in_display = kenya_time(car.time_in)
        car.time_out_display = kenya_time(car.time_out)
    
    stats = {
        'assigned': len(assigned_cars),
        'in_progress': len([c for c in assigned_cars if c.status in ['Washing', 'Detailing']]),
        'completed_today': len(completed_cars)
    }
    
    return render_template('staff_dashboard.html', 
                         stats=stats, 
                         assigned_cars=assigned_cars,
                         completed_cars=completed_cars)



# CAR/JOB MANAGEMENT


@app.route('/cars/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_car():
    """Add a new car/job"""
    form = AddCarForm()
    form.service_id.choices = [(s.id, f"{s.name} - KSh {s.price}") 
                               for s in Service.query.filter_by(is_active=True).all()]
    form.assigned_user_id.choices = [(u.id, u.full_name) 
                                     for u in User.query.filter_by(role='staff', is_active=True).all()]
    
    if form.validate_on_submit():
        car = Car(
            plate_number=form.plate_number.data.upper().strip(),
            car_model=form.car_model.data,
            customer_name=form.customer_name.data,
            customer_phone=form.customer_phone.data,
            customer_email=form.customer_email.data,
            service_id=form.service_id.data,
            assigned_user_id=form.assigned_user_id.data,
            notes=form.notes.data,
            status='Waiting',
            time_in=datetime.utcnow()
        )
        db.session.add(car)
        db.session.commit()
        flash(f'Job for {car.plate_number} added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('add_car.html', form=form)


@app.route('/cars/edit/<int:car_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_car(car_id):
    """Edit an existing car/job"""
    car = Car.query.get_or_404(car_id)
    form = EditCarForm(obj=car)
    form.service_id.choices = [(s.id, f"{s.name} - KSh {s.price}") 
                               for s in Service.query.filter_by(is_active=True).all()]
    form.assigned_user_id.choices = [(u.id, u.full_name) 
                                     for u in User.query.filter_by(role='staff', is_active=True).all()]
    
    if form.validate_on_submit():
        car.customer_name = form.customer_name.data
        car.customer_phone = form.customer_phone.data
        car.customer_email = form.customer_email.data
        car.plate_number = form.plate_number.data.upper().strip()
        car.car_model = form.car_model.data
        car.service_id = form.service_id.data
        car.assigned_user_id = form.assigned_user_id.data
        car.status = form.status.data
        car.notes = form.notes.data
        
        if form.status.data == 'Completed' and not car.time_out:
            car.time_out = datetime.utcnow()
        
        db.session.commit()
        flash(f'Job for {car.plate_number} updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    # Set display times
    car.time_in_display = kenya_time(car.time_in)
    car.time_out_display = kenya_time(car.time_out)
    
    return render_template('edit_car.html', form=form, car=car)


@app.route('/cars/delete/<int:car_id>', methods=['POST'])
@login_required
@admin_required
def delete_car(car_id):
    """Delete a car/job"""
    car = Car.query.get_or_404(car_id)
    plate = car.plate_number
    db.session.delete(car)
    db.session.commit()
    flash(f'Job for {plate} deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/cars/update-status/<int:car_id>', methods=['POST'])
@login_required
def update_status(car_id):
    """Update job status"""
    car = Car.query.get_or_404(car_id)
    
    if current_user.role != 'admin' and car.assigned_user_id != current_user.id:
        flash('You are not authorized to update this job.', 'error')
        return redirect(url_for('staff_dashboard'))
    
    new_status = request.form.get('status')
    if new_status:
        old_status = car.status
        car.status = new_status
        
        if new_status == 'Completed' and not car.time_out:
            car.time_out = datetime.utcnow()
        
        db.session.commit()
        flash(f'Status updated from "{old_status}" to "{new_status}"', 'success')
    
    if request.is_json:
        # Calculate today's revenue
        start_of_day_utc, end_of_day_utc = get_today_start_end_utc()
        completed_jobs_today = Car.query.filter(
            Car.status == 'Completed',
            Car.time_out != None,
            Car.time_out >= start_of_day_utc,
            Car.time_out <= end_of_day_utc
        ).all()
        revenue = sum([job.service.price for job in completed_jobs_today])
        
        return jsonify({
            'status': car.status,
            'revenue': f'{revenue:,.0f}'
        })
    
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('staff_dashboard'))



# SERVICE MANAGEMENT


@app.route('/services')
@login_required
@admin_required
def manage_services():
    """Manage services page"""
    services = Service.query.order_by(Service.name).all()
    add_form = AddServiceForm()
    edit_form = EditServiceForm()
    return render_template('manage_services.html', 
                         services=services, 
                         add_form=add_form, 
                         edit_form=edit_form)


@app.route('/services/add', methods=['POST'])
@login_required
@admin_required
def add_service():
    """Add a new service"""
    form = AddServiceForm()
    if form.validate_on_submit():
        service = Service(
            name=form.name.data.strip(),
            description=form.description.data,
            price=form.price.data,
            duration=form.duration.data,
            is_active=True
        )
        db.session.add(service)
        db.session.commit()
        flash(f'Service "{service.name}" added successfully!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')
    return redirect(url_for('manage_services'))


@app.route('/services/edit/<int:service_id>', methods=['POST'])
@login_required
@admin_required
def edit_service(service_id):
    """Edit an existing service"""
    service = Service.query.get_or_404(service_id)
    form = EditServiceForm()
    if form.validate_on_submit():
        service.name = form.name.data.strip()
        service.description = form.description.data
        service.price = form.price.data
        service.duration = form.duration.data
        db.session.commit()
        flash(f'Service "{service.name}" updated successfully!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')
    return redirect(url_for('manage_services'))


@app.route('/services/delete/<int:service_id>', methods=['POST'])
@login_required
@admin_required
def delete_service(service_id):
    """Delete a service"""
    service = Service.query.get_or_404(service_id)
    if service.cars.count() > 0:
        flash(f'Cannot delete "{service.name}" - it is currently assigned to jobs.', 'error')
        return redirect(url_for('manage_services'))
    service_name = service.name
    db.session.delete(service)
    db.session.commit()
    flash(f'Service "{service_name}" deleted successfully!', 'success')
    return redirect(url_for('manage_services'))



# USER MANAGEMENT


@app.route('/users')
@login_required
@admin_required
def manage_users():
    """Manage users page"""
    users = User.query.order_by(User.username).all()
    add_form = AddUserForm()
    edit_form = EditUserForm()
    return render_template('manage_users.html', 
                         users=users, 
                         add_form=add_form, 
                         edit_form=edit_form)


@app.route('/users/add', methods=['POST'])
@login_required
@admin_required
def add_user():
    """Add a new user"""
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            full_name=form.full_name.data,
            email=form.email.data.strip(),
            role=form.role.data,
            is_active=form.is_active.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'User "{user.username}" added successfully!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')
    return redirect(url_for('manage_users'))


@app.route('/users/edit/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Edit an existing user"""
    user = User.query.get_or_404(user_id)
    form = EditUserForm()
    if form.validate_on_submit():
        user.username = form.username.data.strip()
        user.full_name = form.full_name.data
        user.email = form.email.data.strip()
        user.role = form.role.data
        user.is_active = form.is_active.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash(f'User "{user.username}" updated successfully!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')
    return redirect(url_for('manage_users'))


@app.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account!', 'error')
        return redirect(url_for('manage_users'))
    if Car.query.filter_by(assigned_user_id=user.id).count() > 0:
        flash(f'Cannot delete "{user.username}" - they have jobs assigned.', 'error')
        return redirect(url_for('manage_users'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'User "{username}" deleted successfully!', 'success')
    return redirect(url_for('manage_users'))



# REPORTS


@app.route('/reports')
@login_required
@admin_required
def reports():
    """Reports and analytics page (Today's data)"""
    # Get today's date range in UTC
    start_of_day_utc, end_of_day_utc = get_today_start_end_utc()
    
    # Jobs created today
    daily_jobs = Car.query.filter(
        Car.time_in >= start_of_day_utc,
        Car.time_in <= end_of_day_utc
    ).count()
    
    # Revenue from jobs completed today
    completed_jobs_today = Car.query.filter(
        Car.status == 'Completed',
        Car.time_out != None,
        Car.time_out >= start_of_day_utc,
        Car.time_out <= end_of_day_utc
    ).all()
    
    daily_revenue = sum([job.service.price for job in completed_jobs_today])
    
    # Staff performance for today
    staff_performance = db.session.query(
        User.full_name,
        db.func.count(Car.id).label('jobs_completed')
    ).join(Car, User.id == Car.assigned_user_id).filter(
        User.role == 'staff',
        Car.status == 'Completed',
        Car.time_out != None,
        Car.time_out >= start_of_day_utc,
        Car.time_out <= end_of_day_utc
    ).group_by(User.id, User.full_name).all()
    
    # Popular services (all time)
    popular_services = db.session.query(
        Service.name,
        db.func.count(Car.id).label('times_booked')
    ).join(Car).filter(
        Car.status == 'Completed'
    ).group_by(Service.id, Service.name).order_by(
        db.desc('times_booked')
    ).limit(5).all()
    
    return render_template('reports.html',
                         daily_jobs=daily_jobs,
                         daily_revenue=daily_revenue,
                         staff_performance=staff_performance,
                         popular_services=popular_services)



# ERROR HANDLERS


@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('errors/500.html'), 500