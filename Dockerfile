FROM python:latest
ENV DEBIAN_FRONTEND noninteractive
COPY task1/ /usr/task/
WORKDIR /usr/task/
RUN apt-get update && apt-get install -y apt-utils \
    && apt-get -y install locales
RUN apt-get install -y python3-pip python-psycopg2 && pip3 install setuptools influxdb PyQt5 pyqtgraph \
    && apt-get install -y pyqt5-dev-tools
CMD ["python3", "imitation_loop.py", "&", "python3", "graphic.py"]