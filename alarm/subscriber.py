import sqlite3

###CODE FOR ALARM RECEIVER (SUBSCRIBER)
def on_connect(client, userdata, flags, rc):
    print("Connected to broker.")
    client.subscribe(topic)
def on_message(client, userdata, msg):
    print("Alarm triggered:  {msg.payload.decode()}")

client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker)
print("Listening for sound alerts.")
client.loop_forever()   