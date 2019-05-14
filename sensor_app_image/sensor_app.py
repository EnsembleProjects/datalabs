import paho.mqtt.client as mqtt
from pymongo import MongoClient
import json
import datetime
import sys

def on_connect(client, userdata, flags, rc):
    client.subscribe("sensors")
    print("Subscribed to topic 'sensors'", file=sys.stderr)

def on_message(client, userdata, message):
    data = json.loads(str(message.payload.decode("utf-8")))
    data['timestamp'] = datetime.datetime.utcnow()
    try:
        mongo_client = MongoClient('mongo_container',27017)
        db = mongo_client.sensor
        sensors = db.sensors
        sensors.insert_one(data)
    except:
        print("Couldn't connect to mongo...", file=sys.stderr)

print("Sensor_App service...")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
try:
    print("Connecting to mosquitto...", file=sys.stderr)
    client.connect("mosquitto", 1883)
    print("Connected to mosquitto...", file=sys.stderr)
    client.loop_forever()
except:
    print("Couldn't connect to mosquitto...", file=sys.stderr)

