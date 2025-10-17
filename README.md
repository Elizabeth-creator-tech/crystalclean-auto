 CrystalClean Auto - Setup Instructions

Backend Files to Paste

 1. Core Backend Files
Paste these into your project:

- `app/models.py` ← From artifact "models.py - Database Models"
- `app/__init__.py` ← From artifact "__init__.py - Flask App Initialization"
- `app/forms.py` ← From artifact "forms.py - Flask-WTF Forms"
- `app/routes.py` ← From artifact "routes.py - COMPLETE (Merge Part 1 & 2)"
- `app/utils.py` ← From artifact "utils.py - Helper Functions"
- `app/database/seed_data.py` ← From artifact "seed_data.py - Initial Database Seeding"
- `config.py` (root) ← From artifact "config.py - Configuration Settings"
- `run.py` (root) ← From artifact "run.py - Application Entry Point"
- `app/templates/reports.html` ← From artifact "reports.html - Reports Page"



 Installation Steps

 Step 1: Create Virtual Environment
```bash
cd crystalclean
python -m venv venv
```

 Step 2: Activate Virtual Environment
Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

 Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

 Step 4: Add Logo Images (Optional)
Place your logo files in:
- `app/static/images/logo.png`
- `app/static/images/crystal-clean.png`



 ▶️ Running the Application

 Start the Server
```bash
python run.py
```

The application will start at: http://localhost:5000



 Default Login Credentials

 Admin Account:
- Username: `admin`
- Password: `admin123`

 Staff Accounts:
- Username: `john` | Password: `staff123`
- Username: `mary` | Password: `staff123`



 # Testing the System

 1. Login as Admin
- Go to http://localhost:5000
- Login with admin credentials
- You should see the Admin Dashboard

 2. Add a Job
- Click "Add New Job"
- Fill in customer and vehicle details
- Select service and assign to staff
- Submit

 3. Login as Staff
- Logout and login with staff credentials
- You should see assigned jobs
- Update job status using the dropdown

 4. Test Services & Users
- Go to "Services" menu
- Add, edit, or delete services
- Go to "Users" menu
- Add, edit staff members



Project Structure

```
crystalclean/
├── app/
│   ├── __init__.py           # App initialization
│   ├── routes.py             # All URL routes
│   ├── models.py             # Database models
│   ├── forms.py              # Form definitions
│   ├── utils.py              # Helper functions
│   ├── static/
│   │   ├── css/style.css     # Styling
│   │   ├── js/main.js        # JavaScript
│   │   └── images/           # Add logos here
│   ├── templates/            # All HTML files
│   └── database/
│       └── seed_data.py      # Initial data seeding
├── instance/
│   └── config.py             (Auto-generated)
├── venv/                     (Virtual environment)
├── app.db                    (Auto-generated database)
├── config.py                 # Configuration
├── run.py                    # Entry point
└── requirements.txt          # Dependencies
```



Troubleshooting

 Issue: "Module not found" error
Solution:
```bash
pip install -r requirements.txt
```

 Issue: "No such table" error
Solution: Delete `app.db` and restart the server. The database will be recreated with seed data.
```bash
del app.db   Windows
rm app.db    Mac/Linux
python run.py
```

 Issue: Port 5000 already in use
Solution: Change port in `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)   Change to 5001
```


Features Implemented

:.: User Authentication (Admin & Staff roles)  
:.: Admin Dashboard with statistics  
:.: Staff Dashboard with task management  
:.: Job/Car Management (Add, Edit, Delete, Update Status)  
:.: Service Management (Add, Edit, Delete)  
:.: User Management (Add, Edit, Delete)  
:.: Real-time Status Tracking (Waiting → Washing → Detailing → Ready → Completed)  
:.: Reports & Analytics  
:.: Search Functionality  
:.: Responsive Design  
:.: Friendly Error Pages (404, 500)  



Next Steps (Optional Enhancements)

1. SMS Notifications: Integrate Africa's Talking API
2. Email Notifications: Integrate SendGrid or Gmail SMTP
3. Export Reports: Add PDF/Excel export functionality
4. Customer Portal: Allow customers to track their car status
5. Payment Integration: Add M-Pesa payment gateway



Support

If you encounter any issues:
1. Check the terminal for error messages
3. Verify virtual environment is activated
4. Check that all dependencies are installed
