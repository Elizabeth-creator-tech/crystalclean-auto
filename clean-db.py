from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # Keep Mark (ID: 1) and Rachel (ID: 6) - change Rachel's ID if you want a different staff member
    keep_ids = [1, 6]
    
    # Delete all other users
    users_to_delete = User.query.filter(User.id.notin_(keep_ids)).all()
    
    print(f"Deleting {len(users_to_delete)} users:")
    for user in users_to_delete:
        print(f"  - {user.username} ({user.role})")
        db.session.delete(user)
    
    db.session.commit()
    print("\n✓ Done. Remaining users:")
    
    remaining = User.query.all()
    for user in remaining:
        print(f"  - {user.username} ({user.role})")