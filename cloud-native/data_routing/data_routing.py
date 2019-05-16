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
        mongo_client = MongoClient('mongo_db',27017)
        db = mongo_client.sensor
        sensors = db.sensors
        sensors.insert_one(data)
    except:
        print("Couldn't connect to mongo_db", file=sys.stderr)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
try:
    client.connect("mosquitto", 1883)
    client.loop_forever()
except:
    print("Couldn't connect to mosquitto", file=sys.stderr)

