FROM python:3.12-bullseye

WORKDIR /usr/grade/src

RUN apt-get update -y && \
    apt-get install libgl1 -y && \
    apt-get install tzdata -y

ENV PYTHONUNBUFFERED=1 \
    TZ="Europe/Moscow"

RUN pip install --upgrade pip --no-cache-dir && \
    pip install poetry --no-cache-dir

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

COPY . .
