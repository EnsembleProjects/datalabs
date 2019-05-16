### Developing a Cloud-Native Wireless Sensor DataLab

#### What is a cloud-native application?

[Various definitions - extract key characteristics]


#### What is a DataLab?

A DataLab brings together data, analytical techniques and computational resources for a specific purpose. This purpose could potentially
cover a wide range of possibilities, e.g. exploratory investigations of datasets, learning about innovative statistical techniques, developing an 
understanding of particular application areas, or integrating different modelling approaches.

The basic premise here is to start with the idea of a (very) simple sensor DataLab built using a traditional client-server model, 
then develop this through stages into a containerised application and finally a cloud-native application.

It is hoped that as well as documenting the steps taken I will also reflect on the pros and cons of various decisions en-route.

#### A Wireless Sensor DataLab

A Wireless Sensor DataLab has been chosen because it raises some interesting architectural questions for the system due to the streaming nature of the 
data and because of the physical topology with limited resources. It is perhaps also interesting because it gives us an opportunity to think about what
a DataLab would look like that brought real-time streaming data together with historical data.

So, what is the purpose of this Wireless Sensor Datalab? I think just to explore the characteristics of the streaming sensor data using a variety of
techniques. As it develops, this will become more precise over time. 

However, let's not forget that the main objective of this work is to document (and reflect upon) the approach used to move from a traditional software
architecture to a cloud-native architecture.

#### Main Architectural Components of a Wireless Sensor DataLab



1. **Virtual Network:** Used for container networking and for simple dns lookup.<br>
`docker network create -d bridge bridge_network`

2. **Sensor Emulators:** Python scripts publishing to a MQTT message broker.

3. **MQTT Message Broker container:** Used for publish/subscribe to message topics. Image pulled directly from [https://hub.docker.com/_/eclipse-mosquitto]().<br>
`docker pull eclipse-mosquitto`  
`docker run -it --name mosquitto --network=bridge_network -p 1883:1883 -p 9001:9001 eclipse-mosquitto`  

4. **Sensor application:** Subscribes to message broker and sends received sensor data to a streaming data database. This would be a convient place for quality control and addition of meta-data if required.<br> 
`docker build -t sensor_app .`  
`docker run --network=bridge_network sensor_app`

5. **Streamed Data Database:** Populated with sensor data as it arrives on the MQTT message bus. The database chosen here is the document-based database MongoDB. Image pulled directly from [https://hub.docker.com/_/mongo]().<br> 
`docker pull mongo`  
`docker run --name mongo_db --network=bridge_network -p 27017:27017 -d mongo:latest`  

6. **Processed Data Database:** Populated with processed data. The database chosen here is the relational database PostgreSQL. Image pulled directly from [https://hub.docker.com/_/postgres]().<br>
`docker pull postgres`  
`docker run --network=bridge_network --name postgres_db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres`  

7. **Jupyter Notebook:** The application front-end is based upon the SciPy container published by Jupyter with the addtion of python libraries for the database connections and a simple Jupyter notebook to test database connections. Initial image pulled directly from [https://hub.docker.com/r/jupyter/scipy-notebook]().<br>
`Dockerfile:`  
`FROM jupyter/scipy-notebook:latest`  
`ADD db.ipynb /home/jovyan`  
`RUN conda install -y pymongo psycopg2`  
``  
`docker build -t jupyter_notebook .`    
`docker run --name jupyter_notebook --network=bridge_network -p 8888:8888 jupyter_notebook`     

8. **DataLab Composition:** The DataLab application is composed from these services and uses `docker-compose` to do this composition. The docker-compose file describing the compostion is [docker-compose.yml](https://github.com/digsci/datalabs/blob/master/docker-compose.yml)<br>


9. Run sensor emulators
mosquitto_pub -t sensors -m '{"name": "sensor1"}'

10. Move to Kubernetes deployment

[...]

NOTES

1. mosquitto_pub -t sensors -m "{'name': 'sensor1'}" (i.e. single and double quotes swapped) seems to fail on JSON loads - testing req.Apparently, this is a restriction of the JSON format.
[json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes:]

2. db.ipynb had read permissions for owner only and jupyter failed to open it in container - testing req.
		


