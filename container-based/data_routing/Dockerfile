FROM python:latest

ADD data_routing.py /

RUN pip install pymongo paho-mqtt

CMD [ "python", "./data_routing.py" ]

