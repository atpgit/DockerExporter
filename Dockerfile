FROM python:3-windowsservercore

RUN mkdir /src
WORKDIR /src

ADD prometheus.py /src

RUN pip install docker

RUN pip install prometheus_client

RUN pip install flask

RUN pip install uwsgi

CMD [ "python", "./prometheus.py" ]