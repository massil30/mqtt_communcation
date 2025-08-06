import paho.mqtt.client as mqtt
import time
import random
from dotenv import load_dotenv
import os

# MQTT broker details
BROKER = "test.mosquitto.org"  # You can replace this with your broker IP
PORT = 1883
CLIENT_ID = "PythonMQTTClient"
TOPIC_SUB = "Device1/temperature"
TOPIC_PUB = "Device1/temperature"

# Called when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to broker")
        client.subscribe(TOPIC_SUB)
    else:
        print(f"❌ Failed to connect, return code {rc}")

# Called when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(f"📩 Message received on {msg.topic}: {msg.payload.decode()}")

def publish_temperature(client):
    # Simulate temperature value
    temperature = round(random.uniform(20.0, 30.0), 2)
    result = client.publish(TOPIC_PUB, f"{temperature}")
    status = result[0]
    if status == 0:
        print(f"📤 Sent temperature: {temperature}°C")
    else:
        print("❌ Failed to send message")

def main():
    client = mqtt.Client(client_id=CLIENT_ID)

    # Assign callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to broker
    client.connect(BROKER, PORT, keepalive=60)

    # Start network loop
    client.loop_start()

    try:
        while True:
            publish_temperature(client)
            time.sleep(2)
    except KeyboardInterrupt:
        print("🛑 Exiting...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
