FROM python:3.11

LABEL title "Assorted Python 3 code"
LABEL maintainer "Diego / Kartones"
LABEL url "https://kartones.net"

# Define environment vars to expose to container here
# ENV <key> <value>

# Env vars sent from docker-compose or docker build
ARG uid=1000
ARG gid=1000

RUN getent group $gid || groupadd --gid $gid python-assorted
RUN getent passwd $uid || useradd -m -u $uid -g $gid python-assorted

RUN chown -R $uid:$gid /usr/local

RUN apt-get clean && apt-get -y update && apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libportmidi-dev libjpeg-dev python3-setuptools python3-dev python3-numpy

USER $uid

COPY requirements.txt /code/requirements.txt


RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
