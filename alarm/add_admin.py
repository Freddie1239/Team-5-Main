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

username = input("Enter username: ")
password = input("Enter password: ")

if not authenticate(username, password):
    print("❌ Authentication failed. Exiting.")
    exit()
else:
    print("🔐 Authenticated as:", username)