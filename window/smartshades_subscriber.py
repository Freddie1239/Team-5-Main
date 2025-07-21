# smartshades_subscriber.py

import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
import pytz

# Connect to or create the SQLite database
conn = sqlite3.connect("shade_log.db")
cursor = conn.cursor()

# Create the log table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT,
        timestamp TEXT
    )
''')
conn.commit()

# Callback: When an MQTT message is received
def on_message(client, userdata, msg):
    payload = msg.payload.decode()

    # Get time in local timezone
    uk = pytz.timezone("Europe/London")
    timestamp = datetime.now(uk).strftime('%Y-%m-%d %H:%M:%S')

    # Insert command into the database
    cursor.execute("INSERT INTO log (status, timestamp) VALUES (?, ?)", (payload, timestamp))
    conn.commit()

    print(f"Shade status: {payload} at {timestamp}")

# MQTT setup
client = mqtt.Client()
client.connect("broker.hivemq.com", 1883, 60)
client.subscribe("home/livingroom/shades")
client.on_message = on_message

print("Listening for commands from smartphone...")

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Stopping...")
finally:
    conn.close()
