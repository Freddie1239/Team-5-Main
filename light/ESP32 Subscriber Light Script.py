import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
import pytz

broker = "broker.hivemq.com"
topic = "home/livingroom/light"
status_topic = "home/livingroom/status"

# Database setup
conn = sqlite3.connect("light_log.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT,
        timestamp TEXT
    )
""")
conn.commit()

# Track last known status to prevent duplicate logs
last_status = None

def on_message(client, userdata, msg):
    global last_status
    payload = msg.payload.decode()

    # Handle optional source (e.g., "ON|SENSOR")
    parts = payload.split("|")
    status = parts[0].strip().upper()

    # Skip if status hasn't changed
    if status == last_status:
        print(f"Ignored duplicate: {status}")
        return

    if status not in ["ON", "OFF"]:
        print("Invalid command received:", status)
        return

    # Update last_status
    last_status = status

    # Timestamp (UK time)
    uk = pytz.utc
    timestamp = datetime.now(uk).strftime("%Y-%m-%d %H:%M:%S")

    # Log to DB
    cursor.execute("INSERT INTO log (status, timestamp) VALUES (?, ?)", (status, timestamp))
    conn.commit()

    print(f"Light status: {status} at {timestamp}")
    client.publish(status_topic, f"{status} at {timestamp}")

client = mqtt.Client()
client.on_message = on_message
client.connect(broker)
client.subscribe(topic)

print("ESP32 Simulation: Listening for commands...")
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Exiting...")
finally:
    conn.close()
