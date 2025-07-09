import sqlite3
import getpass

def setup_database():
    conn = sqlite3.connect("cctv_system.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS motion_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            sensor_id TEXT,
            message TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS motion_summary (
            date TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
    ''')

    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))

    conn.commit()
    conn.close()

def login_local_user():
    username = input("Enter system username: ")
    password = getpass.getpass("Enter system password: ")

    conn = sqlite3.connect("cctv_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    return user is not None

def get_mqtt_credentials():
    print("=== MQTT Broker Login ===")
    username = input("MQTT Username: ")
    password = getpass.getpass("MQTT Password: ")
    return username, password

if __name__ == "__main__":
    setup_database()
    if login_local_user():
        print("System login successful.")
        mqtt_user, mqtt_pass = get_mqtt_credentials()
        print(f"Use these credentials for broker: {mqtt_user} / {mqtt_pass}")
    else:
        print("System login failed.")