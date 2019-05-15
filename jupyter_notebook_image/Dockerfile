FROM jupyter/scipy-notebook:latest
ADD db.ipynb /home/jovyan
ADD architecture.png /home/jovyan
ADD jupyter_notebook_config.py /home/jovyan/.jupyter/
RUN conda install -y pymongo psycopg2

