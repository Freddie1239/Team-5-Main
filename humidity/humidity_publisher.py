import paho.mqtt.client as mqtt
import time
import random
from humidity_auth import init_db, login, register

# Initialize the database
init_db()

# Ask user to register or login
action = input("Type 'r' to register or 'l' to login: ").strip().lower()
if action == 'r':
    if not register(): exit()
elif action == 'l':
    if not login(): exit()
else:
    print("Invalid option.")
    exit()

# MQTT configuration
broker = "broker.hivemq.com"
port = 1883
topic = "home/livingroom/humidity"

# Connect to MQTT broker
client = mqtt.Client()
client.connect(broker, port, 60)

print(" Publishing humidity data every 5 seconds...\n")

# Send fake humidity data every 5 seconds
try:
    while True:
        humidity = round(random.uniform(40, 70), 2)
        client.publish(topic, humidity)
        print(f"Published → {humidity}% to {topic}")
        time.sleep(5)
except KeyboardInterrupt:
    print("\nPublisher stopped.")
    client.disconnect()
