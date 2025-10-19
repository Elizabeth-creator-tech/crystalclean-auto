# CrystalClean Auto - Complete Documentation

## Overview

CrystalClean Auto is a comprehensive web-based car wash management system built with Flask. It provides an intuitive interface for managing jobs, services, staff, and customer vehicles with real-time status tracking and role-based access control. The system uses PostgreSQL for reliable data persistence.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.7 or higher
- pip (Python package installer)
- A text editor or IDE (Visual Studio Code, PyCharm, etc.)

### Backend Files Required

To set up CrystalClean Auto, you'll need to paste the following files into your project directory:

**Core Application Files:**
- `app/models.py` - Database model definitions
- `app/__init__.py` - Flask application initialization
- `app/forms.py` - Flask-WTF form definitions
- `app/routes.py` - All URL routes and view logic
- `app/utils.py` - Helper functions and utilities
- `config.py` - Configuration settings
- `run.py` - Application entry point

**Database & Templates:**
- `app/templates/` - All HTML templates
- `app/static/` - CSS, JavaScript, and images

**Optional Assets:**
- `app/static/images/logo.png` - Main logo
- `app/static/images/crystal-clean.png` - Secondary logo

## Installation

### Step 1: Create a Virtual Environment

Navigate to your project directory and create a Python virtual environment:

```bash
cd crystalclean
python -m venv venv
```

### Step 2: Activate the Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

After activation, your terminal prompt should display `(venv)` at the beginning.

### Step 3: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

**Your requirements.txt should include:**
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- WTForms
- psycopg2-binary (for PostgreSQL support)

### Step 4: Configure Environment Variables (For Deployment)

For Render or other hosting platforms, set these environment variables:

- `DATABASE_URL` - PostgreSQL connection string (format: `postgresql://user:password@host:port/database`)
- `SECRET_KEY` - A strong secret key for sessions

## Running the Application

### Start the Development Server

Once your virtual environment is activated and dependencies are installed:

```bash
python run.py
```

The application will launch and be accessible at:

```
http://localhost:5000
```

## Project Structure

```
crystalclean/
├── app/
│   ├── __init__.py              # Flask app initialization with default users
│   ├── routes.py                # All URL routes and view handlers
│   ├── models.py                # Database models
│   ├── forms.py                 # Flask-WTF form definitions
│   ├── utils.py                 # Helper functions
│   ├── static/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── images/
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── admin_dashboard.html
│       ├── staff_dashboard.html
│       ├── manage_users.html
│       ├── manage_services.html
│       ├── add_car.html
│       ├── edit_car.html
│       ├── analytics.html
│       ├── archived_jobs.html
│       └── reports.html
├── migrations/                  # Flask-Migrate database migrations
├── config.py                    # Configuration settings
├── run.py                       # Entry point
└── requirements.txt             # Python dependencies
```

## Core Features

### User Authentication and Role-Based Access

The system supports two user roles:

**Admin Role** - Full access to all features including user management, service configuration, comprehensive reporting, job management, and system settings.

**Staff Role** - Limited access focused on job management. Staff members can view assigned tasks and update job statuses.

### Default Users

The system automatically creates two default users on first run:

- **Admin:** Username: `Mark`, Password: `johnmark`
- **Staff:** Username: `Rachel`, Password: `johnmark`

You can add additional users through the UI after logging in.

### Comprehensive Dashboard System

**Admin Dashboard** - Displays key business metrics including total jobs today, jobs in progress, completed jobs, and daily revenue.

**Staff Dashboard** - Shows only jobs assigned to that staff member with quick-action buttons for status updates.

### Job Management System

- Create, read, update, and delete jobs with full lifecycle management
- Assign jobs to specific staff members
- Track customer information and vehicle details
- Monitor job progression through status stages: Waiting → Washing → Detailing → Ready for Pickup → Completed

### Job Archiving

Completed jobs older than 24 hours are automatically archived. You can also manually archive or clear old data through the admin panel.

### Service Configuration

Manage services your business offers including names, descriptions, pricing, and duration. Add or remove services as your business evolves.

### Staff Management

Create and manage user accounts for staff members with role-based permissions. View staff performance and job assignments.

### Advanced Search and Filtering

Quickly locate jobs, services, or users using built-in search functionality. Filter results by status, date range, or other relevant criteria.

### Reports and Analytics

Generate detailed reports on business performance, job completion rates, revenue by service type, staff productivity, and customer data.

### Responsive Design

The interface works seamlessly on desktop computers, tablets, and mobile devices.

## Authentication and Access Control

### Default Login Credentials

**Admin Account:**
- Username: `Mark`
- Password: `johnmark`

**Staff Account:**
- Username: `Rachel`
- Password: `johnmark`

### Accessing the Application

1. Navigate to `http://localhost:5000` in your web browser
2. Enter your credentials on the login page
3. Click the login button
4. You'll be redirected to your role-appropriate dashboard

### Adding New Users

1. Log in as an admin
2. Click "Users" in the main navigation
3. Click "Add User" and provide their details
4. New users can now log in with their credentials

## Deployment to Render

### Prerequisites

- GitHub repository with your code
- Render account (https://render.com)
- PostgreSQL database (created in Render)

### Deployment Steps

1. **Create PostgreSQL Database on Render:**
   - Go to Render dashboard
   - Click "New +" → "PostgreSQL"
   - Name it and create the database
   - Copy the "External Database URL"

2. **Set Environment Variables:**
   - Go to your web service settings
   - Click "Environment"
   - Add `DATABASE_URL` with the PostgreSQL connection string
   - Add `SECRET_KEY` with a strong random string

3. **Deploy Code:**
   ```bash
   git add .
   git commit -m "Deploy to Render with PostgreSQL"
   git push origin main
   ```

4. **Wait for Deployment:**
   - Render will automatically build and deploy your app
   - Takes 2-5 minutes
   - Check logs for any errors

5. **Access Your App:**
   - Visit `https://your-app-name.onrender.com`
   - Log in with Mark/johnmark

### Important Notes

- Use PostgreSQL for production (not SQLite) for data persistence
- The system automatically creates default users on first deployment
- Any additional users you add through the UI will persist in the PostgreSQL database
- Data persists across redeployments

## Troubleshooting

### Module Not Found Error

If you receive a `ModuleNotFoundError`, install dependencies:

```bash
pip install -r requirements.txt
```

### Database Connection Error on Render

Ensure your `DATABASE_URL` environment variable is correctly set:

1. Go to your Render service → Environment
2. Verify the `DATABASE_URL` matches your PostgreSQL connection string
3. Redeploy your service

### Port 5000 Already in Use

Change the port in `run.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Users Not Persisting on Render

This means you're using SQLite instead of PostgreSQL. Verify:

1. PostgreSQL database is created on Render
2. `DATABASE_URL` environment variable is set correctly
3. `psycopg2-binary` is in your `requirements.txt`

### Delete User Function Not Working

The delete function checks if a user has assigned jobs. If they do, the deletion is prevented with an error message. Reassign their jobs to another staff member first, then try deleting.

## Enhancement Opportunities

- SMS notifications via Africa's Talking API
- Email notifications via SendGrid
- Export reports to PDF or Excel
- Customer portal for job tracking
- Payment integration with M-Pesa
- Advanced appointment scheduling
- Photo documentation for jobs
- Extended customer profile management
- Inventory tracking system

## Support

When encountering issues:

1. Check terminal output for error messages
2. Verify virtual environment is activated `(venv)` in prompt
3. Ensure all dependencies are installed
4. Check database connectivity
5. Review application logs in terminal or Render dashboard
6. Verify environment variables are correctly set