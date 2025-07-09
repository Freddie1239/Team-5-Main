import schedule
import time
import paho.mqtt.publish as publish

broker_address = "broker.hivemq.com"
topic = "home/livingroom/light"

def turn_on_light():
    publish.single(topic, "ON", hostname=broker_address)
    print("Scheduled: Light turned ON")

def turn_off_light():
    publish.single(topic, "OFF", hostname=broker_address)
    print("Scheduled: Light turned OFF")

#Note that this schedule system work with winter time(UTC+0)
schedule.every().day.at("14:23").do(turn_on_light)
schedule.every().day.at("14:24").do(turn_off_light)

print("Scheduler started... waiting for scheduled time (Ctrl+C to stop)")

#Loop to keep checking every second
while True:
    schedule.run_pending()
    time.sleep(1)

