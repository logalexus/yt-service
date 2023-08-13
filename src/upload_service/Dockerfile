FROM python:3.11.2-slim-buster

RUN apt-get update
RUN apt-get install wget -y
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome*.deb --yes

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . ./
