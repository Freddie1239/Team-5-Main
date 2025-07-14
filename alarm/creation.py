import sqlite3

# Create/connect to database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')
# Add sample users (hashed passwords are better in real systems)
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("user1", "pass456"))
conn.commit()
conn.close()
print("✅ User database created and populated.")