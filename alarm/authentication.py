import sqlite3

def authenticate(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()

    return result is not None
    if authenticate("admin", "admin123"):
        print("✅ Login successful!")
    else:
        print("❌ Invalid credentials.")