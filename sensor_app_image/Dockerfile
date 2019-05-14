FROM python:latest

ADD sensor_app.py /

RUN pip install pymongo paho-mqtt

CMD [ "python", "./sensor_app.py" ]

