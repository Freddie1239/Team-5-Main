# create_shades_user_db.py
import sqlite3

# Connect to (or create) the SQLite database named 'smart_shades.db'
conn = sqlite3.connect("smart_shades.db")
cursor = conn.cursor()

# Create a table called 'users' with 'username' as the primary key and 'password'
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
""")

# Insert test users
cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?)", ("alex", "shade123"))
cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?)", ("jordan", "winshade456"))

# Save (commit) the changes to the database
conn.commit()
conn.close()

print("smart_shades.db created with user: alex / shade123")
print("smart_shades.db created with user: jordan / winshade456")
