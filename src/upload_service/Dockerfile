FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install --no-install-recommends -y wget

WORKDIR /app

COPY ./chrome_114_amd64.deb ./

RUN apt-get install ./chrome_114_amd64.deb --yes

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./app ./

ENV PYTHONPATH=/app
