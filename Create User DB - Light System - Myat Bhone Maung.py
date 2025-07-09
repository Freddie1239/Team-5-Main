import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create SQL Database
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
""")

# Assign user info to variables
user1 = ("tom", "123tom")
user2 = ("tomsbro", "123tombro")

# Load user info
cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?)", user1)
cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?)", user2)

conn.commit()
conn.close()

# Print using formatted strings
print(f"users.db created with users: {user1[0]} / {user1[1]}, {user2[0]} / {user2[1]}")
