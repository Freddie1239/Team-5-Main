import sqlite3
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time

# MQTT Configuration
broker_address = "broker.hivemq.com"
topic_pub = "home/livingroom/shades"        # Command topic
topic_sub = "home/livingroom/shades/status" # Status topic

# User login function
def login():
    conn = sqlite3.connect("smart_shades.db")
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

# MQTT message callback
def on_message(client, userdata, message):
    print(f"STATUS UPDATE: {message.payload.decode()}")

# Main program
if login():
    # Set up subscriber
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker_address)
    client.subscribe(topic_sub)
    client.loop_start()

    while True:
        command = input("Type command (OPEN/CLOSE or EXIT to quit): ").strip().upper()

        if command == "EXIT":
            print("Exiting control system.")
            break
        elif command not in ["OPEN", "CLOSE"]:
            print("Invalid command.")
            continue

        # Publish the command
        publish.single(topic_pub, command, hostname=broker_address)
        print(f"Sent command: {command}")
        time.sleep(1)  # Slight delay to allow status feedback to arrive

    client.loop_stop()

