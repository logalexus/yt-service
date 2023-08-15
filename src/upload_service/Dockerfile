FROM python:3.10-alpine

RUN apk update && \
    apk add wget chromium

# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
#     apk add ./google-chrome*.deb

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./ ./
