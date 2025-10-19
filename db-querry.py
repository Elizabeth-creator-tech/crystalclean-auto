from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # Check if Mark exists
    mark = User.query.filter_by(username='Mark').first()
    if not mark:
        mark = User(
            username='Mark',
            full_name='Mark John',
            email='admin@crystalclean.com',
            role='admin',
            is_active=True
        )
        mark.set_password('johnmark')
        db.session.add(mark)
        db.session.commit()
        print("✓ Mark created")
    else:
        print("Mark already exists")
    
    # Also create a staff user
    staff = User.query.filter_by(username='Rachel').first()
    if not staff:
        staff = User(
            username='Rachel',
            full_name='Rachel Kirui',
            email='kiruirachel@crystalclean.com',
            role='staff',
            is_active=True
        )
        staff.set_password('johnmark')
        db.session.add(staff)
        db.session.commit()
        print("✓ Rachel created")