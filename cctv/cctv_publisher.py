
import paho.mqtt.client as mqtt
from datetime import datetime, time as dtime
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

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()  # Enable TLS

client.connect(BROKER, PORT, 60)
client.loop_start()

print("Publisher started. Press Ctrl+C to stop.")

try:
    while True:
        current_time = datetime.now().time()
        if dtime(6, 0) <= current_time <= dtime(22, 0):
            message = f"Motion detected at {datetime.now().isoformat()}"
            client.publish(TOPIC, message)
            print("Published:", message)
        else:
            print("⏸Outside monitoring hours.")
        time.sleep(10)
except KeyboardInterrupt:
    print("Publisher stopped.")
finally:
    client.loop_stop()
    client.disconnect()
