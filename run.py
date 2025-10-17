from app import create_app, db
from app.models import User, Service, Car, Notification

# Create Flask application
app = create_app()


# Shell context for Flask CLI
@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'Service': Service,
        'Car': Car,
        'Notification': Notification
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
