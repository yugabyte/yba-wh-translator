# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install Flask requests

COPY . .

USER 1001

#RUN mkdir /tmp/clientcerts

#VOLUME /tmp/clientcerts

CMD [ "python3", "mgshook.py"]
