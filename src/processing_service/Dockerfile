FROM python:3.10-alpine

RUN apk update && \
    apk add ffmpeg 

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./app ./

ENV PYTHONPATH=/app