FROM jupyter/scipy-notebook:latest
USER root
RUN useradd -ms /bin/bash datalabs
USER jovyan
ADD db.ipynb /home/jovyan
ADD jupyterhub_config.py /home/jovyan/
RUN conda install -y pymongo psycopg2
ENTRYPOINT jupyterhub -f jupyterhub_config.py

