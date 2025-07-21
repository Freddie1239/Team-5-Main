# smartshades_control.py

import sqlite3
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time

# MQTT Configuration
broker_address = "broker.hivemq.com"
topic_pub = "home/livingroom/shades"   # Command topic
topic_sub = "home/livingroom/shades/status"  # Status topic

def login():
    conn = sqlite3.connect("smart_shades.db")  # Connect to your DB
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

def on_message(client, userdata, message):
    print("STATUS UPDATE:", message.payload.decode())

if login():
    command = input("Type command (OPEN/CLOSE): ").strip().upper()
    if command not in ["OPEN", "CLOSE"]:
        print("Invalid command.")
        exit()

    # Send command via MQTT
    publish.single(topic_pub, command, hostname=broker_address)
    print(f"Sent command: {command}")

    # Subscribe to receive shade status
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker_address)
    client.subscribe(topic_sub)
    client.loop_start()

    print("Waiting for shade status update...")
    time.sleep(5)

    client.loop_stop()
