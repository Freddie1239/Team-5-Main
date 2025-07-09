import random
import time
import paho.mqtt.publish as publish

broker_address = "broker.hivemq.com"
topic = "home/livingroom/light"

print("LDR simulation running... (Ctrl+C to stop)")

try:
    while True:
        simulated_brightness = random.randint(0, 100)  # 0 = dark, 100 = bright
        print(f"Brightness: {simulated_brightness}")

        if simulated_brightness < 30:
            publish.single(topic, "ON", hostname=broker_address)
            print("Auto-triggered: Light turned ON due to low brightness")
        if simulated_brightness> 30:
            publish.single(topic, "OFF", hostname=broker_address)
            print("Auto-triggered: Light turned OFF due to enough brightness")
        time.sleep(10)  # check every 10 seconds
except KeyboardInterrupt:
    print("LDR simulation stopped.")
