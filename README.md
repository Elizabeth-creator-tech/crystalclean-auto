CrystalClean Auto - Complete Documentation
=============================================

Overview
--------

CrystalClean Auto is a comprehensive web-based car wash management system built with Flask. It provides an intuitive interface for managing jobs, services, staff, and customer vehicles with real-time status tracking and role-based access control.


Getting Started
---------------

Prerequisites

Before you begin, ensure you have the following installed on your system:

• Python 3.7 or higher
• pip (Python package installer)
• A text editor or IDE (Visual Studio Code, PyCharm, etc.)

Backend Files Required

To set up CrystalClean Auto, you'll need to paste the following files into your project directory:

Core Application Files:
  • app/models.py - Database model definitions
  • app/__init__.py - Flask application initialization
  • app/forms.py - Flask-WTF form definitions
  • app/routes.py - All URL routes and view logic
  • app/utils.py - Helper functions and utilities
  • config.py - Configuration settings
  • run.py - Application entry point

Database & Templates:
  • app/database/seed_data.py - Initial database seeding with demo data
  • app/templates/reports.html - Reports and analytics page

Optional Assets:
  • app/static/images/logo.png - Main logo
  • app/static/images/crystal-clean.png - Secondary logo


Installation
------------

Step 1: Create a Virtual Environment

Navigate to your project directory and create a Python virtual environment. This keeps your project dependencies isolated from your system Python installation.

    cd crystalclean
    python -m venv venv


Step 2: Activate the Virtual Environment

On Windows:

    venv\Scripts\activate

On macOS/Linux:

    source venv/bin/activate

After activation, your terminal prompt should display (venv) at the beginning.


Step 3: Install Dependencies

Install all required Python packages from the requirements.txt file:

    pip install -r requirements.txt

This will install Flask, Flask-SQLAlchemy, Flask-WTF, and other necessary dependencies.


Step 4: Add Logo Images (Optional)

Create the images directory and add your logo files:

    app/static/images/
    ├── logo.png
    └── crystal-clean.png

If you don't add logos, the application will still function but display placeholder text instead.


Running the Application
-----------------------

Start the Development Server

Once your virtual environment is activated and dependencies are installed, start the application:

    python run.py

The application will launch and be accessible at:

    http://localhost:5000

You should see output in your terminal indicating the server is running and ready to accept connections.


Project Structure
-----------------

Understanding the project layout will help you navigate and customize the application:

PROJECT DIRECTORY STRUCTURE
----------------------------

File/Folder                          Description
================================================================================

ROOT LEVEL:
  config.py                          Main application configuration settings
  run.py                             Entry point to start the application
  requirements.txt                   List of all Python dependencies
  app.db                             SQLite database file (auto-created)

APP FOLDER (app/):
  __init__.py                        Flask app initialization and setup
  routes.py                          All URL routes and view handlers
  models.py                          Database models (User, Job, Service, Vehicle)
  forms.py                           Flask-WTF form definitions
  utils.py                           Helper functions and utility methods

STATIC FOLDER (app/static/):
  css/style.css                      Main application stylesheet
  js/main.js                         Client-side JavaScript code
  images/                            Folder for logos and image files
    logo.png                         Main application logo
    crystal-clean.png                Secondary logo or branding image

TEMPLATES FOLDER (app/templates/):
  base.html                          Base template with navigation and layout
  index.html                         Login page
  dashboard.html                     Admin dashboard with statistics
  staff_dashboard.html               Staff member dashboard with tasks
  jobs.html                          Job management page
  services.html                      Service management page
  users.html                         User and staff management page
  reports.html                       Reports and analytics page
  error_404.html                     Custom 404 Not Found page
  error_500.html                     Custom 500 Server Error page

DATABASE FOLDER (app/database/):
  seed_data.py                       Script for initial database seeding

INSTANCE FOLDER (instance/):
  config.py                          Auto-generated instance configuration

ENVIRONMENT FOLDER (venv/):
  (Virtual environment folder)       Python virtual environment directory


Core Features
-------------

CrystalClean Auto comes packed with powerful features designed for car wash business management:

User Authentication and Role-Based Access

The system supports two user roles with different access levels and permissions:

Admin Role provides full access to all features including user management, service configuration, comprehensive reporting, and system settings. Admins can view dashboards with business statistics and manage all aspects of the operation.

Staff Role offers limited access focused on job management. Staff members can view assigned tasks, update job statuses, and track their assigned work without access to administrative functions.

Comprehensive Dashboard System

The Admin Dashboard displays key business metrics including total jobs, revenue statistics, service performance, and staff activity summaries. Staff members see a personalized dashboard showing only their assigned jobs with quick-action buttons for status updates.

Job Management System

Create, read, update, and delete jobs with full lifecycle management. Assign jobs to specific staff members, track customer information, manage vehicle details, and monitor job progression through multiple status stages.

Real-Time Status Tracking

Jobs progress through a well-defined workflow: Waiting → Washing → Detailing → Ready → Completed. Update statuses on the fly, and the system maintains a complete history of all status changes for reporting and accountability.

Service Configuration

Manage the services your business offers including service names, descriptions, and pricing. Add new services as your business expands or remove services that are no longer offered. Edit service details at any time.

Staff Management

Create user accounts for staff members, assign roles, manage permissions, and track staff activity. View which staff members are assigned to specific jobs and their current workload.

Advanced Search and Filtering

Quickly locate jobs, services, or users using the built-in search functionality. Filter results by status, date range, assigned staff, or other relevant criteria to find exactly what you need.

Reports and Analytics

Generate detailed reports on business performance, job completion rates, revenue by service type, staff productivity, and more. Visualize trends and make data-driven decisions with comprehensive analytics.

Responsive Design

The interface works seamlessly on desktop computers, tablets, and mobile devices. Staff can update job statuses from anywhere using any device connected to the internet.

Professional Error Handling

Custom-designed error pages for common HTTP errors (404 Not Found, 500 Server Error) provide helpful information and navigation options instead of generic error messages.


Authentication and Access Control
----------------------------------

Default Login Credentials

The system comes with pre-configured demo accounts for testing:

Admin Account:
  Username: admin
  Password: admin123

Staff Accounts:
  Username: john | Password: staff123
  Username: mary | Password: staff123

Accessing the Application

1. Navigate to http://localhost:5000 in your web browser
2. Enter your credentials on the login page
3. Click the login button
4. You'll be redirected to your role-appropriate dashboard

Security Notes

In a production environment, you should change these default credentials and implement additional security measures such as password hashing, HTTPS, and regular security audits.


Using the System
----------------

Logging In as Admin

Step 1: Open your browser and go to http://localhost:5000

Step 2: Enter the admin credentials provided above and click Login

Step 3: You'll see the Admin Dashboard with business statistics and access to all features

Adding a New Job

Step 1: Click "Add New Job" from the main navigation menu

Step 2: Fill in the customer details including name, phone number, and email

Step 3: Enter vehicle information such as make, model, year, and license plate

Step 4: Select the service(s) to be performed from the available options

Step 5: Assign the job to a staff member from the dropdown list

Step 6: Click Submit to create the job

The job will now appear in the job list with an initial status of "Waiting".

Logging In as Staff

Step 1: Logout by clicking the Logout button

Step 2: Log back in with staff credentials (e.g., john / staff123)

Step 3: You'll see your Staff Dashboard showing only jobs assigned to you

Step 4: Click on any job to view details

Step 5: Use the status dropdown to update the job progress (Washing → Detailing → Ready → Completed)

Managing Services

Step 1: Click "Services" in the main navigation

Step 2: View all available services in a table format

Step 3: To add a new service, click "Add Service" and fill in the details

Step 4: To edit a service, click the edit icon next to the service name

Step 5: To remove a service, click the delete icon (you may need to delete associated jobs first)

Managing Users/Staff

Step 1: Click "Users" in the main navigation (Admin only)

Step 2: View all system users in the user list

Step 3: To add a new staff member, click "Add User" and provide their details

Step 4: To edit user information, click the edit icon next to their name

Step 5: To remove a user account, click the delete icon (ensure no jobs are assigned first)

Viewing Reports

Step 1: Click "Reports" in the main navigation

Step 2: Review analytics on job completion rates, service popularity, and staff performance

Step 3: Use date filters to view historical data or focus on specific time periods

Step 4: Export or print reports as needed (if export functionality is enabled)


Troubleshooting
---------------

Module Not Found Error

If you receive a "ModuleNotFoundError" when running the application, it means some dependencies are not installed.

Solution:

    pip install -r requirements.txt

Verify that your virtual environment is activated (you should see (venv) in your terminal prompt) before installing.

No Such Table Error

If the application crashes with a "No such table" error, the database hasn't been properly initialized or seeded.

Solution:

Delete the existing database file and restart the server. The application will automatically create a new database with seed data:

On Windows:

    del app.db
    python run.py

On macOS/Linux:

    rm app.db
    python run.py

Port 5000 Already in Use

If you see an error stating that port 5000 is already in use, another application is using that port.

Solution:

Open run.py and change the port number:

    app.run(debug=True, host='0.0.0.0', port=5001)

Then restart the application:

    python run.py

The app will now run on http://localhost:5001

Virtual Environment Not Activating

If you have trouble activating your virtual environment, ensure you're in the correct directory and using the right command for your operating system.

On Windows: Use backslashes in the path: venv\Scripts\activate

On macOS/Linux: Use forward slashes: source venv/bin/activate

Database Corruption

If the database becomes corrupted or you want to reset to a clean state, follow the "No Such Table Error" solution above.


Enhancement Opportunities
--------------------------

CrystalClean Auto provides a solid foundation for a car wash management system. Consider these enhancements to add more functionality:

SMS Notifications

Integrate with Africa's Talking API to send SMS notifications to customers when their jobs are ready for pickup or when status changes occur. This keeps customers informed without manual calls.

Email Notifications

Integrate with SendGrid or Gmail SMTP to send automated email confirmations when jobs are created, updated, or completed. Include job status updates and receipt information.

Reports Export

Add functionality to export reports in PDF or Excel format. Allow users to generate reports on demand and download them for archival or sharing with stakeholders.

Customer Portal

Create a separate interface where customers can log in, view their vehicles, submit wash requests, and track the real-time status of their car without needing staff assistance.

Payment Integration

Integrate with M-Pesa or other mobile payment gateways to enable customers to pay directly through the system. Automate receipt generation and payment reconciliation.

Advanced Scheduling

Implement appointment scheduling where customers can book specific time slots for their car wash, and staff receives notifications of upcoming appointments.

Photo Documentation

Allow staff to attach before/after photos of vehicles as jobs progress through the workflow for quality assurance and customer communication.

Customer Management

Expand the user system to include customer profiles with complete history of services, payments, and vehicle information for personalized service.

Inventory Management

Track supplies and materials used in car wash services, set reorder points, and get alerts when inventory runs low.


Support and Troubleshooting Tips
--------------------------------

When encountering issues:

1. Check Terminal Output: Look at the terminal running your application for error messages. They often provide clues about what went wrong.

2. Verify Virtual Environment: Confirm your virtual environment is activated by checking for (venv) in your terminal prompt.

3. Check Dependencies: Run pip install -r requirements.txt to ensure all dependencies are properly installed.

4. Browser Cache: If you see outdated content, try clearing your browser cache or doing a hard refresh (Ctrl+Shift+Delete).

5. Database Reset: If in doubt, delete app.db and restart the server to get a fresh database with seed data.

6. Port Issues: If port 5000 is in use, change it in run.py to an alternative port like 5001.

7. Check File Paths: Ensure all files are in the correct directories as shown in the project structure.


Conclusion
----------

CrystalClean Auto is a powerful, user-friendly solution for managing car wash operations. With its intuitive interface, comprehensive feature set, and scalable architecture, it provides everything needed to run an efficient car wash business. The built-in demo data and accounts make it easy to get started and explore the system's capabilities.

For questions or issues not covered in this documentation, review the application code in the respective files or reach out to the development team for support.