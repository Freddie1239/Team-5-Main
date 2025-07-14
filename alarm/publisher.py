import paho.mqtt.client as mqtt
import time 
import sqlite3
import random        #Simulates sound input

broker = "broker.hivemq.com"
topic = "home/livingroom/sound"
client_id = "sound_detctor"
client = mqtt.Client(client_id)
client.connect(broker)
threshold = 70      #Sound level threshold

###CODE FOR SOUND DETECTOR (PUBLISHER)
print("Sound detector running. Ctrl+C to stop.")
try: 
    while True:
        sound_level = random.randint(30,100)
        print("f Sound level: {sound_level}")
        if sound_level > threshold:
            client.publish(topic, "SOUND_ALERT")
            print("Loud sound detected! Alert sent.")
        time.sleep(2)
except KeyboardInterrupt:
    print("Stopped by user")  

           