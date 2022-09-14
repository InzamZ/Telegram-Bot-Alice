# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

CMD python3 /tgb/main.py TOKEN