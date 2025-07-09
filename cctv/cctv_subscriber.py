
import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime, date
import schedule
import time
from cctv_login_interface import setup_database, login_local_user, get_mqtt_credentials

# === Setup system ===
setup_database()
if not login_local_user():
    print("System login failed.")
    exit()

USERNAME, PASSWORD = get_mqtt_credentials()

# === MQTT Config ===
BROKER = "f219f07e213344afa63f9ad8bd21e81d.s1.eu.hivemq.cloud"
PORT = 8883
TOPIC = "home/livingroom/cctv"

# === DB setup ===
conn = sqlite3.connect("cctv_system.db", check_same_thread=False)
cursor = conn.cursor()

def log_sensor_message(sensor_id, message):
    timestamp = datetime.now().isoformat()
    cursor.execute("INSERT INTO motion_logs (timestamp, sensor_id, message) VALUES (?, ?, ?)",
                   (timestamp, sensor_id, message))
    conn.commit()

def update_motion_count():
    today = str(date.today())
    cursor.execute("SELECT count FROM motion_summary WHERE date=?", (today,))
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE motion_summary SET count = count + 1 WHERE date=?", (today,))
    else:
        cursor.execute("INSERT INTO motion_summary (date, count) VALUES (?, ?)", (today, 1))
    conn.commit()

def daily_report():
    today = str(date.today())
    cursor.execute("SELECT count FROM motion_summary WHERE date=?", (today,))
    row = cursor.fetchone()
    count = row[0] if row else 0
    print(f"[DAILY REPORT] Motion detections today ({today}): {count}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(TOPIC)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    sensor_id = msg.topic.split("/")[-1]
    print(f"Received from {sensor_id}: {message}")
    log_sensor_message(sensor_id, message)
    update_motion_count()

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()  # TLS for secure connection

client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)

schedule.every().day.at("23:59").do(daily_report)

print("Monitoring started. Press Ctrl+C to stop.")
client.loop_start()

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Monitoring stopped.")
finally:
    client.loop_stop()
    conn.close()
