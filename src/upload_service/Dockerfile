FROM python:3.10-slim-buster as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

FROM base as builder

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base as runtime

COPY --from=builder /.venv /.venv

ENV PATH="/.venv/bin:$PATH"
 
RUN apt-get update && \
    apt-get install --no-install-recommends -y wget

WORKDIR /app

COPY ./bin/ ./

RUN apt-get install ./chrome_114_amd64.deb --yes

COPY ./app ./

ENV PYTHONPATH=/app
