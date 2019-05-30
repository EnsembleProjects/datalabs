FROM jupyter/scipy-notebook:latest

USER root
RUN useradd -ms /bin/bash datalabs
ADD db.ipynb /home/datalabs
ADD jupyterhub_config.py /etc/jupyter/
ADD login.html /opt/conda/share/jupyterhub/custom-templates/login.html
ADD datalabs-logo.png /opt/conda/share/jupyterhub/static/images/datalabs-logo.png
RUN conda install -y pymongo psycopg2
ENTRYPOINT jupyterhub -f /etc/jupyter/jupyterhub_config.py

