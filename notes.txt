Developing a Cloud-Native Wireless Sensor DataLab

What is a cloud-native application? ...

A DataLab brings together data, analytical techniques and computational resources for a specific purpose. This purpose could potentially
cover a wide range of possibilities, e.g. exploratory investigations of datasets, learning about innovative statistical techniques, developing an 
understanding of particular application areas, or integrating different modelling approaches.

The basic premise here is to start with the idea of a (very) simple sensor DataLab built using a traditional client-server model, 
then develop this through stages into a containerised application and finally a cloud-native application.

It is hoped that as well as documenting the steps taken I will also reflect on the pros and cons of various decisions en-route.


A Wireless Sensor DataLab has been chosen because it raises some interesting architectural questions for the system due to the streaming nature of the 
data and because of the physical topology with limited resources. It is perhaps also interesting because it gives us an opportunity to think about what
a DataLab would look like that brought real-time streaming data together with historical data.

So, what is the purpose of this Wireless Sensor Datalab? I think just to explore the characteristics of the streaming sensor data using a variety of
techniques. As it develops, this will become more precise over time. 

However, let's not forget that the main objective of this work is to document (and reflect upon) the approach used to move from a traditional software
architecture to a cloud-native architecture.



Main components:


1. Virtual Network for containers to network on and use dns lookup for other containers:
docker network create -d bridge bridge_network

2. Sensor emulators:
Python scripts publishing to a MQTT message broker

3. MQTT Message Broker container:
docker pull eclipse-mosquitto
docker run -it --name mosquitto --network=bridge_network -p 1883:1883 -p 9001:9001 eclipse-mosquitto

4. Sensor application container (subscribes to message broker and sends received messages to a database container)

sensor_app.py:

from pymongo import MongoClient
import json
import datetime

mongo_client = MongoClient('mongo_container',27017)
db = mongo_client.sensor
sensors = db.sensors

def on_connect(client, userdata, flags, rc):
    client.subscribe("sensors")

def on_message(client, userdata, message):
        data = json.loads(str(message.payload.decode("utf-8")))
        data['timestamp'] = datetime.datetime.utcnow()
        sensors.insert_one(data)
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mosquitto")
client.loop_forever()

Dockerfile:

FROM python:latest
ADD sensor_app.py /
RUN pip install pymongo paho-mqtt
CMD [ "python", "./sensor_app.py" ]

docker build -t sensor_app .
docker run --network=bridge_network sensor_app

5. MongoDB container

docker pull mongo
docker run --name mongo_container --network=bridge_network -p 27017:27017 -d mongo:latest

6. PostgreSQL container

docker pull postgres
docker run --network=bridge_network --name postgres_db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres

7. Jupyter Notebook container

Dockerfile:

FROM jupyter/scipy-notebook:latest
ADD db.ipynb /home/jovyan
RUN conda install -y pymongo psycopg2 

docker build -t jupyter_notebook .
docker run --name jupyter_notebook --network=bridge_network -p 8888:8888 jupyter_notebook 

8. Create Docker Compose file

docker-compose.yml

version: '3'
services:
  jupyter-notebook:
    image: "jupyter_notebook"
    ports:
      - "8888:8888"
  sensor_app:
    image: "sensor_app"
    depends_on:
        - "mosquitto"
        - "mongo_container"
  mongo_container:
    image: "mongo"
    ports:
        - "27017:27017"
  postgres_db:
    environment:
      - POSTGRES_PASSWORD=postgres
    image: "postgres"
  mosquitto:
    image: "eclipse-mosquitto"
    ports:
        - "1883:1883"

9. Run sensor emulators
mosquitto_pub -t sensors -m '{"name": "sensor1"}'

NOTES

1. mosquitto_pub -t sensors -m "{'name': 'sensor1'}" (i.e. single and double quotes swapped) seems to fail on JSON loads - testing req.Apparently, this is a restriction of the JSON format.
[json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes:]

2. db.ipynb had read permissions for owner only and jupyter failed to open it in container - testing req.
		


