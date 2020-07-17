FROM python:latest
ENV DEBIAN_FRONTEND noninteractive
COPY . /usr/task/
WORKDIR /usr/task/
RUN apt-get update && apt-get install -y apt-utils \
    && apt-get -y install locales
RUN apt-get install -y python3-pip python-psycopg2 && pip3 install setuptools influxdb PyQt5 pyqtgraph \
    && apt-get install -y pyqt5-dev-tools && pip3 install fastapi asyncio hbmqtt uvicorn
CMD ["python3", "-m", "task3and4.full_interface"]