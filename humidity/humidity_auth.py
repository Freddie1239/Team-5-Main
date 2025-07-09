import sqlite3
import hashlib

# Create users table if it doesn't exist
def init_db():
    conn = sqlite3.connect("mqtt_users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Register a user with hashed password
def register():
    conn = sqlite3.connect("mqtt_users.db")
    cursor = conn.cursor()
    username = input("Choose a username: ").strip()
    password = input("Choose a password: ").strip()

    if not username or not password:
        print(" Username and password cannot be empty.")
        return False

    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        print(" Registration successful.\n")
        return True
    except sqlite3.IntegrityError:
        print(" Username already exists.\n")
        return False
    finally:
        conn.close()

# Login with username and hashed password
def login():
    conn = sqlite3.connect("mqtt_users.db")
    cursor = conn.cursor()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and hashed_pw == result[0]:
        print(f" Login successful. Welcome, {username}!\n")
        return True
    else:
        print(" Login failed. Invalid credentials.\n")
        return False
