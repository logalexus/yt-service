FROM python:3.10.6-slim-buster

RUN apt-get update
RUN apt-get install ffmpeg -y

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./app ./

ENV PYTHONPATH=/app