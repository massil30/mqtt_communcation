import paho.mqtt.client as mqtt
import time
import random

BROKER = "broker.hivemq.com"  # Public broker for testing
PORT = 1883
TOPIC_SUB = "Device1/commands"
TOPIC_PUB = "Device1/temperature"
CLIENT_ID = "Device1Client"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC_SUB)
    print(f"Subscribed to {TOPIC_SUB}")

def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client(CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        # Simulate temperature reading
        temperature = round(random.uniform(20.0, 30.0), 2)
        client.publish(TOPIC_PUB, str(temperature))
        print(f"Published temperature: {temperature} to {TOPIC_PUB}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.loop_stop()
    client.disconnect()