FROM jupyter/scipy-notebook:latest

USER root
RUN useradd -ms /bin/bash datalabs
ADD db.ipynb /home/datalabs
ADD jupyterhub_config.py /etc/jupyter/
#RUN conda install -y pymongo psycopg2
ENTRYPOINT jupyterhub -f /etc/jupyter/jupyterhub_config.py

