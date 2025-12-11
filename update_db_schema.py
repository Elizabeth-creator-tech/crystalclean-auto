
import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), 'app.db')

def upgrade_db():
    print(f"Connecting to database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'phone_number' in columns:
            print("Column 'phone_number' already exists in 'users' table.")
        else:
            print("Adding 'phone_number' column to 'users' table...")
            cursor.execute("ALTER TABLE users ADD COLUMN phone_number VARCHAR(20)")
            conn.commit()
            print("Successfully added 'phone_number' column.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    upgrade_db()
