FROM python:3.10.2

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app/ /code

RUN pip install --upgrade pip && \
    pip install -r /code/requirements.txt && \
    alembic revision --autogenerate -m "Init migration" && \
    alembic upgrade head

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
