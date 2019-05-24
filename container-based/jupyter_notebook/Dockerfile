FROM jupyter/scipy-notebook:latest
ADD db.ipynb /home/jovyan
ADD architecture.png /home/jovyan
ADD jupyterhub_config.py /home/jovyan/
RUN conda install -y pymongo psycopg2
ENTRYPOINT jupyterhub -f /home/jovyan/jupyterhub_config.py

