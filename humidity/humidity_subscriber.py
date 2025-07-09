import paho.mqtt.client as mqtt
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

# Callback function when message is received
def on_message(client, userdata, msg):
    humidity = msg.payload.decode()
    print(f"Received ← {humidity}% from {msg.topic}")

# Setup MQTT client
client = mqtt.Client()
client.on_message = on_message
client.connect(broker, port, 60)
client.subscribe(topic)

print(f" Subscribed to {topic}. Waiting for messages...\n")

# Run the loop forever
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nSubscriber stopped.")
    client.disconnect()
