import sqlite3
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time

broker_address = "broker.hivemq.com"
topic_pub = "home/livingroom/light"
topic_sub = "home/livingroom/status"

def login():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    username = input("Username: ")
    password = input("Password: ")
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    if result:
        print("Login successful!\n")
        return True
    else:
        print("Login failed.")
        return False

if not login():
    exit()

command = input("Type command (ON/OFF): ").strip().upper()
if command not in ["ON", "OFF"]:
    print("Invalid command.")
    exit()

publish.single(topic_pub, command, hostname=broker_address)
print(f"Sent command: {command}")

def on_message(client, userdata, message):
    print("STATUS UPDATE:", message.payload.decode())

client = mqtt.Client()
client.on_message = on_message
client.connect(broker_address)
client.subscribe(topic_sub)
client.loop_start()
print("Waiting for light status update...")
time.sleep(5)
client.loop_stop()
